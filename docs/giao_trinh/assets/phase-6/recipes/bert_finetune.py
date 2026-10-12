"""Fine-tune pretrained DistilmBERT cho head câu/token. ASSET_NOT_RUN.

Dataset local JSON: label_names, train, validation.
sequence: mỗi row có text, label (label name).
token: mỗi row có tokens, labels (danh sách label names theo từ).
Nên có group cho người viết/tài liệu; không được trùng group giữa hai split.
"""
import argparse
import copy
import json
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import f1_score
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          AutoModelForTokenClassification, DataCollatorWithPadding,
                          DataCollatorForTokenClassification)
from asset_utils import inspect_asset, require_environment, choose_device

REPO = "distilbert/distilbert-base-multilingual-cased"


def read_data(path, task):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    names = data["label_names"]
    if not names or len(names) != len(set(names)):
        raise ValueError("label_names phải không rỗng và không trùng")
    if task == "token" and any(name != "O" and not name.startswith(("B-", "I-")) for name in names):
        raise ValueError("Metric recipe token yêu cầu BIO labels")
    train, valid = data["train"], data["validation"]
    if not train or not valid:
        raise ValueError("Cần cả train và validation")
    key = "text" if task == "sequence" else "tokens"
    train_keys = {json.dumps(row[key], ensure_ascii=False) for row in train}
    valid_keys = {json.dumps(row[key], ensure_ascii=False) for row in valid}
    if train_keys & valid_keys:
        raise ValueError("Có mẫu trùng giữa train và validation")
    train_groups = {row["group"] for row in train if "group" in row}
    valid_groups = {row["group"] for row in valid if "group" in row}
    if train_groups & valid_groups:
        raise ValueError("Group bị chia qua train/validation")
    return names, train, valid


def encode_rows(rows, tokenizer, label_to_id, task, max_length):
    features = []
    for row in rows:
        if task == "sequence":
            item = tokenizer(row["text"], truncation=False)
            item["labels"] = label_to_id[row["label"]]
        else:
            if len(row["tokens"]) != len(row["labels"]):
                raise ValueError("Số từ và nhãn không khớp")
            item = tokenizer(row["tokens"], is_split_into_words=True, truncation=False)
            aligned, previous = [], None
            for word_id in item.word_ids():
                if word_id is None or word_id == previous:
                    aligned.append(-100)
                else:
                    aligned.append(label_to_id[row["labels"][word_id]])
                previous = word_id
            item["labels"] = aligned
        if len(item["input_ids"]) > max_length:
            raise ValueError("Mẫu vượt max_length; chuẩn bị recipe chia đoạn/alignment rồi chạy lại")
        features.append(dict(item))
    return features


def entity_spans(tags):
    """Trả các (loại, start, end exclusive); I không nối đúng được mở thành span mới."""
    spans = set()
    active_type, start = None, None
    for index, tag in enumerate(list(tags) + ["O"]):
        prefix, kind = ("O", None) if tag == "O" else tag.split("-", 1)
        continuing = prefix == "I" and active_type == kind
        if active_type is not None and not continuing:
            spans.add((active_type, start, index))
            active_type, start = None, None
        if prefix in {"B", "I"} and not continuing:
            active_type, start = kind, index
    return spans


def evaluate(model, loader, device, task, names):
    predictions, labels = [], []
    model.eval()
    with torch.no_grad():
        for batch in loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            guessed = model(**batch).logits.argmax(-1).cpu()
            gold = batch["labels"].cpu()
            if task == "sequence":
                predictions.extend(guessed.tolist())
                labels.extend(gold.tolist())
            else:
                for pred_row, gold_row in zip(guessed, gold):
                    keep = gold_row.ne(-100)
                    predictions.append([names[index] for index in pred_row[keep].tolist()])
                    labels.append([names[index] for index in gold_row[keep].tolist()])
    if task == "sequence":
        return {"macro_f1": float(f1_score(labels, predictions, labels=list(range(len(names))),
                                          average="macro", zero_division=0))}
    correct, predicted_count, gold_count = 0, 0, 0
    for pred_tags, gold_tags in zip(predictions, labels):
        pred_spans, gold_spans = entity_spans(pred_tags), entity_spans(gold_tags)
        correct += len(pred_spans & gold_spans)
        predicted_count += len(pred_spans)
        gold_count += len(gold_spans)
    precision = correct / predicted_count if predicted_count else 0.0
    recall = correct / gold_count if gold_count else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"entity_f1": f1, "precision": precision, "recall": recall,
            "gold_entities": gold_count, "predicted_entities": predicted_count}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--task", choices=["sequence", "token"], default="sequence")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--head-only", action="store_true")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not 1 <= args.epochs <= 20 or not 1 <= args.batch_size <= 32 or not 1 <= args.max_length <= 512:
        raise ValueError("Epoch/batch/length vượt budget recipe nhỏ")
    if not 0 < args.lr < 1:
        raise ValueError("Learning rate cần dương và nhỏ hơn 1")
    versions = require_environment()
    root, manifest = inspect_asset(args.asset, args.manifest, REPO)
    device = choose_device(args.device)
    names, train, valid = read_data(args.data, args.task)
    label_to_id = {name: index for index, name in enumerate(names)}
    tokenizer = AutoTokenizer.from_pretrained(root, local_files_only=True,
                                              trust_remote_code=False, use_fast=True)
    torch.manual_seed(63)
    model_class = AutoModelForSequenceClassification if args.task == "sequence" else AutoModelForTokenClassification
    model = model_class.from_pretrained(root, num_labels=len(names), id2label=dict(enumerate(names)),
        label2id=label_to_id, local_files_only=True, trust_remote_code=False, use_safetensors=True)
    if args.head_only:
        for parameter in model.base_model.parameters():
            parameter.requires_grad_(False)
    model.to(device)
    collator_class = DataCollatorWithPadding if args.task == "sequence" else DataCollatorForTokenClassification
    collator = collator_class(tokenizer)
    train_features = encode_rows(train, tokenizer, label_to_id, args.task, args.max_length)
    valid_features = encode_rows(valid, tokenizer, label_to_id, args.task, args.max_length)
    train_loader = DataLoader(train_features, batch_size=args.batch_size, shuffle=True, collate_fn=collator)
    valid_loader = DataLoader(valid_features, batch_size=args.batch_size, shuffle=False, collate_fn=collator)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr)
    best_score, best_state, history = -1.0, None, []
    metric_name = "macro_f1" if args.task == "sequence" else "entity_f1"
    for epoch in range(args.epochs):
        model.train()
        if args.head_only:
            model.base_model.eval()
        for batch in train_loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            optimizer.zero_grad()
            loss = model(**batch).loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
        metric = evaluate(model, valid_loader, device, args.task, names)
        history.append({"epoch": epoch + 1, **metric})
        if metric[metric_name] > best_score:
            best_score = metric[metric_name]
            best_state = copy.deepcopy({key: value.cpu() for key, value in model.state_dict().items()})
    model.load_state_dict(best_state)
    output = Path(args.output).resolve()
    if output.exists():
        raise ValueError("Output đã tồn tại; chọn thư mục mới để giữ checkpoint trước")
    model.save_pretrained(output, safe_serialization=True)
    tokenizer.save_pretrained(output)
    receipt = {"repo_id": REPO, "revision": manifest["revision"], "versions": versions,
               "task": args.task, "head_only": args.head_only, "history": history,
               "best_validation": best_score, "label_names": names}
    (output / "run-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
