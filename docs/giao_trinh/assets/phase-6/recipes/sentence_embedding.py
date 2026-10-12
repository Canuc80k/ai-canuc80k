"""Recipe multilingual sentence embedding: ASSET_NOT_RUN trong lượt soạn.

python sentence_embedding.py --asset ABS_DIR --manifest ABS_JSON --device cpu
"""
import argparse
import json
import torch
from transformers import AutoModel, AutoTokenizer
from asset_utils import inspect_asset, require_environment, choose_device

REPO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    args = parser.parse_args()
    versions = require_environment()
    root, manifest = inspect_asset(args.asset, args.manifest, REPO)
    device = choose_device(args.device)
    tokenizer = AutoTokenizer.from_pretrained(root, local_files_only=True, trust_remote_code=False)
    model = AutoModel.from_pretrained(root, local_files_only=True, trust_remote_code=False,
                                      use_safetensors=True).to(device).eval()
    pooling_path = root / "1_Pooling" / "config.json"
    sentence_config_path = root / "sentence_bert_config.json"
    pooling = json.loads(pooling_path.read_text(encoding="utf-8"))
    if not pooling.get("pooling_mode_mean_tokens") or pooling.get("pooling_mode_cls_token"):
        raise ValueError("Snapshot không khớp mean pooling của recipe")
    sentence_config = json.loads(sentence_config_path.read_text(encoding="utf-8"))
    max_length = int(sentence_config["max_seq_length"])
    documents = ["Hướng dẫn đặt lại mật khẩu", "Cách mượn sách thư viện", "Xem thời khóa biểu"]
    queries = ["Tôi quên thông tin đăng nhập", "Tôi muốn mượn sách", "Lịch học ở đâu?"]

    def encode(texts):
        lengths = [len(tokenizer(text)["input_ids"]) for text in texts]
        if max(lengths) > max_length:
            raise ValueError("Có văn bản vượt max_seq_length; cần recipe chia đoạn thay vì cắt âm thầm")
        batch = tokenizer(texts, padding=True, truncation=False, return_tensors="pt").to(device)
        with torch.no_grad():
            hidden = model(**batch).last_hidden_state
            weight = batch["attention_mask"].unsqueeze(-1).to(hidden.dtype)
            vectors = (hidden * weight).sum(1) / weight.sum(1).clamp_min(1)
            return torch.nn.functional.normalize(vectors, dim=-1)

    scores = (encode(queries) @ encode(documents).T).cpu()
    print(json.dumps({"repo_id": REPO, "revision": manifest["revision"], "versions": versions,
                      "max_length": max_length, "scores": scores.tolist(),
                      "top1": scores.argmax(1).tolist()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
