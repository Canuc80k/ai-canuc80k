"""LLM pretrained inference + evaluator. ASSET_NOT_RUN trong lượt soạn.

Không tải weights; CPU float32 hoặc CUDA float16, không cần bitsandbytes/accelerate.
"""
import argparse
import json
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from asset_utils import inspect_asset, require_environment, choose_device
from extraction_task import make_messages, DEV_EXAMPLES, validate_answer

REPO = "Qwen/Qwen2.5-0.5B-Instruct"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--max-new-tokens", type=int, default=96)
    parser.add_argument("--zero-shot", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.max_new_tokens <= 256:
        raise ValueError("Output budget cần trong 1..256")
    versions = require_environment()
    root, manifest = inspect_asset(args.asset, args.manifest, REPO)
    device = choose_device(args.device)
    dtype = torch.float16 if device.type == "cuda" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(root, local_files_only=True, trust_remote_code=False)
    if not tokenizer.chat_template:
        raise ValueError("Asset không có chat template instruct")
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(root, local_files_only=True,
        trust_remote_code=False, use_safetensors=True, torch_dtype=dtype).to(device).eval()
    if model.config.model_type != "qwen2":
        raise ValueError("Config không khớp họ kiến trúc đã chọn")
    torch.manual_seed(66)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
    results = []
    schema_count, exact_count = 0, 0
    field_count = {"date": 0, "students": 0}
    for notice, gold in DEV_EXAMPLES:
        messages = make_messages(notice, use_few_shot=not args.zero_shot)
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        batch = tokenizer(prompt, add_special_tokens=False, return_tensors="pt").to(device)
        input_length = int(batch["input_ids"].shape[1])
        context_limit = int(model.config.max_position_embeddings)
        if input_length > 512 or input_length + args.max_new_tokens > context_limit:
            raise ValueError("Input vượt budget recipe/context của model; không cắt âm thầm")
        if device.type == "cuda":
            torch.cuda.synchronize()
        start = time.perf_counter()
        with torch.no_grad():
            sequence = model.generate(**batch, do_sample=False,
                max_new_tokens=args.max_new_tokens, pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id, use_cache=True)
        if device.type == "cuda":
            torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        new_tokens = sequence[0, input_length:]
        raw = tokenizer.decode(new_tokens, skip_special_tokens=True)
        valid, reason, answer = validate_answer(raw)
        exact = valid and answer == gold
        schema_count += valid
        exact_count += exact
        for name in field_count:
            field_count[name] += valid and answer[name] == gold[name]
        results.append({"notice": notice, "gold": gold, "raw": raw, "parsed": answer,
            "schema_valid": valid, "reason": reason, "exact": exact,
            "seconds": elapsed, "input_tokens": input_length, "output_tokens": int(new_tokens.numel()),
            "reached_budget": int(new_tokens.numel()) == args.max_new_tokens})
    config = model.config
    receipt = {"repo_id": REPO, "revision": manifest["revision"], "versions": versions,
        "device": str(device), "dtype": str(dtype), "few_shot": not args.zero_shot,
        "config": {"layers": config.num_hidden_layers, "attention_heads": config.num_attention_heads,
                   "kv_heads": config.num_key_value_heads, "hidden_size": config.hidden_size},
        "schema_valid": schema_count, "exact_match": exact_count, "n": len(DEV_EXAMPLES),
        "field_correct": field_count,
        "peak_allocated_bytes": torch.cuda.max_memory_allocated() if device.type == "cuda" else None,
        "cases": results}
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
