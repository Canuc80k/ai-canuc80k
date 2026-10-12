"""Recipe text-to-text pretrained: ASSET_NOT_RUN trong lượt soạn."""
import argparse
import json
import time
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from asset_utils import inspect_asset, require_environment, choose_device

REPO = "google/flan-t5-small"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--prompt", default="Summarize in one sentence: The school library opens on Monday. Students can borrow two books.")
    parser.add_argument("--max-new-tokens", type=int, default=48)
    args = parser.parse_args()
    if not 1 <= args.max_new_tokens <= 256:
        raise ValueError("Output budget cần nằm trong 1..256 cho recipe nhỏ")
    versions = require_environment()
    root, manifest = inspect_asset(args.asset, args.manifest, REPO)
    device = choose_device(args.device)
    tokenizer = AutoTokenizer.from_pretrained(root, local_files_only=True, trust_remote_code=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(root, local_files_only=True,
        trust_remote_code=False, use_safetensors=True).to(device).eval()
    batch = tokenizer(args.prompt, return_tensors="pt", truncation=False).to(device)
    if batch["input_ids"].shape[1] > 256:
        raise ValueError("Input vượt budget 256 của recipe; chưa chạy chia đoạn")
    if device.type == "cuda":
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    with torch.no_grad():
        output = model.generate(**batch, do_sample=False, max_new_tokens=args.max_new_tokens)
    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    print(json.dumps({"repo_id": REPO, "revision": manifest["revision"], "versions": versions,
        "prompt": args.prompt, "output": tokenizer.decode(output[0], skip_special_tokens=True),
        "seconds": elapsed, "output_tokens": int(output.shape[1]),
        "peak_allocated_bytes": torch.cuda.max_memory_allocated() if device.type == "cuda" else None},
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
