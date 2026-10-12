"""Optional real CLIP / GPT-2 inference from reviewed, hashed local assets.

No download, installation or training. CLIP uses one declared prompt per class.
GPT-2 scores explicit prompt IDs followed by separately-tokenized candidate IDs.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import time
import numpy as np
from common import checked_asset, device_checked, environment, reviewed_note, sha256, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["clip", "gpt2"], required=True)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--input", required=True, help="CLIP CSV or GPT-2 JSON")
    parser.add_argument("--data-review", required=True)
    parser.add_argument("--classes", help="CLIP JSON mapping class name to one prompt")
    parser.add_argument("--image-root", help="allowed root for relative image paths in CLIP CSV")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("batch-size must be positive")
    repo = "openai/clip-vit-base-patch32" if args.mode == "clip" else "openai-community/gpt2"
    asset, manifest, manifest_hash = checked_asset(args.asset, repo)
    review = reviewed_note(args.data_review)
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Choose a new result directory")
    out.mkdir(parents=True, exist_ok=True)
    import torch
    torch.set_num_threads(1)
    torch.set_default_dtype(torch.float32)
    device = device_checked(torch, args.device)
    report = {"mode": args.mode, "environment": environment(torch), "arguments": vars(args),
              "model_id": repo, "revision": manifest["revision"], "asset_manifest_sha256": manifest_hash,
              "data_review": review, "input_sha256": sha256(args.input),
              "recipe_sha256": sha256(__file__), "trained_on_target_labels": False}

    if args.mode == "clip":
        if not args.classes or not args.image_root:
            parser.error("clip needs --classes and --image-root")
        from PIL import Image
        from transformers import CLIPModel, CLIPProcessor
        from sklearn.metrics import accuracy_score, f1_score
        classes = json.loads(Path(args.classes).read_text(encoding="utf-8"))
        if len(classes) < 2 or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in classes.items()):
            raise ValueError("classes must map at least two class names to non-empty prompt strings")
        names, prompts = list(classes), list(classes.values())
        with Path(args.input).open(encoding="utf-8-sig", newline="") as source:
            rows = list(csv.DictReader(source))
        if not rows or len(rows) > 2000 or not {"id", "image"}.issubset(rows[0]):
            raise ValueError("Need 1..2000 image CSV rows with id,image and optional label")
        if any(not r["id"].strip() for r in rows) or len({r["id"] for r in rows}) != len(rows):
            raise ValueError("Missing or duplicate image IDs")
        root = Path(args.image_root).resolve()
        paths = []
        for row in rows:
            path = (root / row["image"]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                raise ValueError("Image path is missing or outside --image-root")
            paths.append(path)
        have_labels = all(r.get("label", "").strip() for r in rows)
        if any(r.get("label", "").strip() for r in rows) and not have_labels:
            raise ValueError("Either all image rows have labels or none do")
        if have_labels and not {r["label"] for r in rows}.issubset(names):
            raise ValueError("Unknown validation class")
        model = CLIPModel.from_pretrained(asset, local_files_only=True, trust_remote_code=False,
                                          use_safetensors=True).to(device).eval()
        processor = CLIPProcessor.from_pretrained(asset, local_files_only=True)
        all_logits = []
        image_receipt = [{"id": row["id"], "path": row["image"], "sha256": sha256(path)} for row, path in zip(rows, paths)]
        if device.type == "cuda":
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
        started = time.perf_counter()
        with torch.inference_mode():
            for start in range(0, len(rows), args.batch_size):
                pictures = []
                for path in paths[start:start + args.batch_size]:
                    with Image.open(path) as source:
                        pictures.append(source.convert("RGB"))
                encoded = processor(text=prompts, images=pictures, padding=True, truncation=False, return_tensors="pt")
                if encoded["input_ids"].shape[1] > model.config.text_config.max_position_embeddings:
                    raise ValueError("Prompt exceeds CLIP text context; rewrite rather than silently truncate")
                encoded = {k: v.to(device) for k, v in encoded.items()}
                logits = model(**encoded).logits_per_image
                if tuple(logits.shape) != (len(pictures), len(names)):
                    raise ValueError("Unexpected CLIP logits shape")
                all_logits.append(logits.cpu().numpy())
        if device.type == "cuda":
            torch.cuda.synchronize()
        values = np.concatenate(all_logits)
        predicted = [names[i] for i in values.argmax(1)]
        report.update({"inference_seconds": time.perf_counter() - started, "classes": classes,
                       "classes_sha256": sha256(args.classes), "images": image_receipt, "rows": len(rows),
                       "evaluation": None, "protocol": "one fixed prompt per class; no target-label tuning"})
        if have_labels:
            truth = [r["label"] for r in rows]
            report["evaluation"] = {"accuracy": float(accuracy_score(truth, predicted)),
                                     "macro_f1": float(f1_score(truth, predicted, labels=names, average="macro", zero_division=0))}
        with (out / "predictions.csv").open("w", encoding="utf-8", newline="") as target:
            writer = csv.writer(target)
            writer.writerow(["id", "label"])
            writer.writerows((row["id"], label) for row, label in zip(rows, predicted))
        np.save(out / "logits.npy", values)
    else:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        request = json.loads(Path(args.input).read_text(encoding="utf-8"))
        prompt, candidates = request["prompt"], request["candidates"]
        if not isinstance(prompt, str) or not prompt or not candidates or len(candidates) > 20:
            raise ValueError("Need non-empty prompt and 1..20 candidates")
        if not all(isinstance(c, str) and c for c in candidates) or len(set(candidates)) != len(candidates):
            raise ValueError("Candidates must be non-empty unique strings")
        tokenizer = AutoTokenizer.from_pretrained(asset, local_files_only=True, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(asset, local_files_only=True, trust_remote_code=False,
                                                    use_safetensors=True).to(device).eval()
        prefix = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        if not prefix:
            raise ValueError("Prompt has no tokens")
        limit = getattr(model.config, "n_positions", None) or getattr(model.config, "max_position_embeddings", None)
        if not limit:
            raise ValueError("Unknown model context limit; inspect config before scoring")
        results = []
        if device.type == "cuda":
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
        started = time.perf_counter()
        with torch.inference_mode():
            for candidate in candidates:
                suffix = tokenizer(candidate, add_special_tokens=False)["input_ids"]
                if not suffix or len(prefix) + len(suffix) > limit:
                    raise ValueError("Candidate empty or prompt+candidate exceeds context; no truncation performed")
                ids = torch.tensor([prefix + suffix], dtype=torch.long, device=device)
                masked = ids.clone()
                masked[:, :len(prefix)] = -100
                output = model(input_ids=ids, labels=masked)
                log_probs = output.logits[:, :-1].log_softmax(-1)
                token_logs = log_probs.gather(2, ids[:, 1:].unsqueeze(-1)).squeeze(-1)
                continuation = token_logs[0, len(prefix) - 1:]
                if len(continuation) != len(suffix):
                    raise ValueError("Shift/mask mismatch")
                total, mean = continuation.sum().item(), continuation.mean().item()
                if not math.isclose(-mean, output.loss.item(), rel_tol=1e-5, abs_tol=1e-5):
                    raise ValueError("Continuation score does not match model masked-label loss")
                results.append({"candidate": candidate, "tokens": suffix, "token_count": len(suffix),
                                "token_log_probabilities": continuation.cpu().tolist(),
                                "sum_log_prob": total, "mean_log_prob": mean,
                                "continuation_perplexity": math.exp(-mean)})
        if device.type == "cuda":
            torch.cuda.synchronize()
        report.update({"scoring_seconds": time.perf_counter() - started, "prompt": prompt, "prompt_ids": prefix,
                       "results": results, "sum_choice": max(results, key=lambda r: r["sum_log_prob"])["candidate"],
                       "mean_choice": max(results, key=lambda r: r["mean_log_prob"])["candidate"],
                       "tokenization": "tokenize prompt/candidate separately; concatenate explicit IDs",
                       "evaluation": None, "not_a_corpus_perplexity": True})
    report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated() if device.type == "cuda" else None
    report["memory_note"] = "CUDA allocator peak; CPU peak memory was not measured"
    report["status"] = "OFFLINE_TRIAL_COMPLETED"
    write_json(out / "RESULT.json", report)
    print(f"Completed {args.mode}. Review receipt: {out / 'RESULT.json'}")


if __name__ == "__main__":
    main()
