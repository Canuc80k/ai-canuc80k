"""Preflight hoặc inference CPU với checkpoint/thư mục model đã có.

Mặc định chỉ preflight. Không tải mạng, không cài package.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def validate_file(path, description):
    if not path or not Path(path).is_file():
        raise ValueError(f"Thiếu {description}: {path}")
    return Path(path).resolve()


def metadata_for(args, kind, classes):
    checkpoint = validate_file(args.checkpoint, "state dict")
    metadata_path = validate_file(args.metadata, "metadata JSON")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("kind") != kind:
        raise ValueError(f"kind phải là {kind}")
    if metadata.get("sha256", "").lower() != digest(checkpoint):
        raise ValueError("SHA-256 checkpoint không khớp metadata")
    names = metadata.get("class_names")
    if not isinstance(names, list) or len(names) != classes:
        raise ValueError(f"class_names cần đúng {classes} phần tử")
    return checkpoint, names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["classifier", "detector", "clip", "diffusion"])
    parser.add_argument("--checkpoint")
    parser.add_argument("--metadata")
    parser.add_argument("--model-dir")
    parser.add_argument("--image")
    parser.add_argument("--texts", nargs="+")
    parser.add_argument("--prompt")
    parser.add_argument("--output")
    parser.add_argument("--score-threshold", type=float, default=0.5)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    packages = ["numpy", "PIL", "torch", "torchvision", "transformers", "diffusers"]
    available = {name: importlib.util.find_spec(name) is not None for name in packages}
    print(json.dumps({"module_discovery": available, "device": "cpu",
                      "asset_inference": "NOT_RUN"}, ensure_ascii=False))
    if not args.task:
        print("PREFLIGHT_ONLY: chọn task và asset trước khi chạy.")
        return
    required = ["torch", "PIL"]
    required += ["torchvision"] if args.task in ["classifier", "detector"] else []
    required += ["transformers"] if args.task == "clip" else []
    required += ["diffusers", "transformers"] if args.task == "diffusion" else []
    if any(not available[name] for name in required):
        raise ValueError("Thiếu dependency: " + ", ".join(n for n in required if not available[n]))
    if args.task in ["classifier", "detector"]:
        kind, classes = (("resnet18_imagenet_v1", 1000) if args.task == "classifier"
                         else ("fasterrcnn_resnet50_fpn_coco_v1", 91))
        checkpoint, class_names = metadata_for(args, kind, classes)
        validate_file(args.image, "ảnh")
    else:
        if not args.model_dir or not Path(args.model_dir).is_dir():
            raise ValueError("Thiếu thư mục model cục bộ")
        model_dir = Path(args.model_dir).resolve()
        config = "config.json" if args.task == "clip" else "model_index.json"
        validate_file(model_dir / config, config)
        if args.task == "clip":
            validate_file(args.image, "ảnh")
            if not args.texts:
                raise ValueError("CLIP cần --texts")
        elif not args.prompt or not args.output:
            raise ValueError("Diffusion cần --prompt và --output")
    if not args.run:
        print("PREFLIGHT_PASS: đã kiểm các điều kiện tệp; chưa import/nạp model/inference.")
        return
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    import torch
    from PIL import Image
    torch.set_num_threads(1)
    torch.manual_seed(5)
    if args.task == "classifier":
        from torchvision.models import resnet18, ResNet18_Weights
        model = resnet18(weights=None)
        state = torch.load(checkpoint, map_location="cpu", weights_only=True)
        model.load_state_dict(state, strict=True)
        model.eval()
        image = Image.open(args.image).convert("RGB")
        transform = ResNet18_Weights.IMAGENET1K_V1.transforms()
        with torch.inference_mode():
            scores = model(transform(image)[None]).softmax(1)[0]
        index = int(scores.argmax())
        print({"index": index, "name": class_names[index], "score": float(scores[index])})
    elif args.task == "detector":
        from torchvision.models.detection import fasterrcnn_resnet50_fpn
        from torchvision.transforms.functional import pil_to_tensor
        model = fasterrcnn_resnet50_fpn(weights=None, weights_backbone=None)
        state = torch.load(checkpoint, map_location="cpu", weights_only=True)
        model.load_state_dict(state, strict=True)
        model.eval()
        image = Image.open(args.image).convert("RGB")
        tensor = pil_to_tensor(image).float() / 255
        with torch.inference_mode():
            result = model([tensor])[0]
        selected = result["scores"] >= args.score_threshold
        for box, label, score in zip(result["boxes"][selected],
                                     result["labels"][selected], result["scores"][selected]):
            print({"box_xyxy": box.tolist(), "class_id": int(label),
                   "name": class_names[int(label)], "score": float(score)})
    elif args.task == "clip":
        from transformers import CLIPModel, CLIPProcessor
        processor = CLIPProcessor.from_pretrained(model_dir, local_files_only=True)
        model = CLIPModel.from_pretrained(model_dir, local_files_only=True,
                                         use_safetensors=True).eval()
        image = Image.open(args.image).convert("RGB")
        batch = processor(text=args.texts, images=image, padding=True, return_tensors="pt")
        with torch.inference_mode():
            result = model(**batch)
        similarities = result.logits_per_image[0]
        print({"texts": args.texts, "scaled_similarities": similarities.tolist(),
               "relative_probabilities": similarities.softmax(0).tolist()})
    else:
        from diffusers import StableDiffusionPipeline
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_dir, local_files_only=True, use_safetensors=True,
            torch_dtype=torch.float32,
        ).to("cpu")
        generator = torch.Generator(device="cpu").manual_seed(5)
        result = pipeline(args.prompt, width=256, height=256, num_inference_steps=10,
                          generator=generator)
        output = Path(args.output).resolve()
        if output.exists():
            raise ValueError("Output đã tồn tại; chọn tệp mới để giữ kết quả cũ")
        output.parent.mkdir(parents=True, exist_ok=True)
        result.images[0].save(output)
        print({"output": str(output), "seed": 5, "steps": 10, "size": [256, 256]})
    print("ASSET_INFERENCE_COMPLETE: chỉ suy luận mẫu đã cung cấp, chưa tính benchmark.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, ImportError, RuntimeError, OSError) as error:
        print(f"NOT_RUN_OR_FAILED: {error}", file=sys.stderr)
        sys.exit(2)
