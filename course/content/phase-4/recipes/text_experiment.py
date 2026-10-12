"""Optional real DistilBERT feature/head/full/LoRA experiment from local assets.

No network calls or package installation. Model assets and CSV splits are required.
Run modes as separate processes with identical CSVs/seed/token budget for comparison.
"""
from pathlib import Path
import argparse
import gc
import importlib.util
import time
import numpy as np
from common import (checked_asset, check_text_splits, device_checked, environment,
                    read_text_split, reviewed_note, sha256, write_json)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--train", required=True)
    parser.add_argument("--valid", required=True)
    parser.add_argument("--data-review", required=True, help="source/license/split review note")
    parser.add_argument("--mode", choices=["features", "head", "full", "lora"], required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--max-steps", type=int, default=20)
    parser.add_argument("--rank", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.max_steps <= 80 or args.batch_size < 1 or args.rank < 1:
        parser.error("Small trial only: 1..80 steps, positive batch size/rank")
    if args.mode == "lora" and importlib.util.find_spec("peft") is None:
        raise SystemExit("PEFT is unavailable. Use a project virtual environment; this recipe does not install it.")
    asset, manifest, manifest_hash = checked_asset(args.asset, "distilbert/distilbert-base-uncased")
    train, valid = read_text_split(args.train), read_text_split(args.valid)
    labels = check_text_splits(train, valid)
    if len(train) + len(valid) > 2000:
        raise ValueError("This is a small trial recipe (<=2000 rows); prepare a reviewed small split first")
    data_review = reviewed_note(args.data_review)
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Choose a new experiment output directory")
    out.mkdir(parents=True, exist_ok=True)

    import torch
    from torch import nn
    from transformers import AutoConfig, AutoModel, AutoModelForSequenceClassification, AutoTokenizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, f1_score
    torch.set_num_threads(1)
    torch.manual_seed(7)
    torch.set_default_dtype(torch.float32)
    device = device_checked(torch, args.device)
    config = AutoConfig.from_pretrained(asset, local_files_only=True, trust_remote_code=False)
    if config.model_type != "distilbert" or not 1 <= args.max_length <= config.max_position_embeddings:
        raise ValueError("Wrong model type or max-length outside model context")
    tokenizer = AutoTokenizer.from_pretrained(asset, local_files_only=True, trust_remote_code=False)
    label_to_id = {name: i for i, name in enumerate(labels)}
    y_train = np.array([label_to_id[r["label"]] for r in train])
    y_valid = np.array([label_to_id[r["label"]] for r in valid])

    def tokens(rows):
        encoded = tokenizer([r["text"] for r in rows], padding=True, truncation=True,
                            max_length=args.max_length, return_tensors="pt")
        return {k: v.to(device) for k, v in encoded.items()}

    report = {"mode": args.mode, "environment": environment(torch), "arguments": vars(args),
              "asset_manifest_sha256": manifest_hash, "model_id": manifest["model_id"],
              "revision": manifest["revision"], "data_review": data_review,
              "train_sha256": sha256(args.train), "valid_sha256": sha256(args.valid),
              "train_rows": len(train), "valid_rows": len(valid), "labels": labels,
              "precision": "float32", "seed": 7, "test_evaluated": False,
              "recipe_sha256": sha256(__file__)}
    if args.mode == "features":
        model = AutoModel.from_pretrained(asset, local_files_only=True, trust_remote_code=False,
                                         use_safetensors=True).to(device).eval()

        def embeddings(rows):
            batches = []
            with torch.no_grad():
                for start in range(0, len(rows), args.batch_size):
                    encoded = tokens(rows[start:start + args.batch_size])
                    hidden = model(**encoded).last_hidden_state
                    weights = encoded["attention_mask"].unsqueeze(-1).float()
                    pooled = (hidden * weights).sum(1) / weights.sum(1).clamp_min(1)
                    batches.append(pooled.cpu().numpy())
            return np.concatenate(batches)

        if device.type == "cuda":
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
        started = time.perf_counter()
        Z_train, Z_valid = embeddings(train), embeddings(valid)
        if device.type == "cuda":
            torch.cuda.synchronize()
        extraction_seconds = time.perf_counter() - started
        started = time.perf_counter()
        probe = LogisticRegression(C=1, max_iter=500).fit(Z_train, y_train)
        predictions = probe.predict(Z_valid)
        head_seconds = time.perf_counter() - started
        linear_scores = Z_valid @ probe.coef_.T + probe.intercept_
        if linear_scores.shape[1] == 1:
            independent = np.where(linear_scores[:, 0] > 0, probe.classes_[1], probe.classes_[0])
        else:
            independent = probe.classes_[linear_scores.argmax(1)]
        if not np.array_equal(predictions, independent):
            raise ValueError("Linear probe predictions differ from independent coefficient computation")
        replay = embeddings(valid[:min(2, len(valid))])
        if not np.allclose(replay, Z_valid[:len(replay)], atol=1e-5, rtol=1e-5):
            raise ValueError("Recomputed embedding differs from cache")
        report.update({"pooling": "masked mean including special tokens", "feature_dim": Z_train.shape[1],
                       "extraction_seconds": extraction_seconds, "head_seconds": head_seconds,
                       "head_trainable_parameters": int(probe.coef_.size + probe.intercept_.size),
                       "accuracy": float(accuracy_score(y_valid, predictions)),
                       "macro_f1": float(f1_score(y_valid, predictions, average="macro", zero_division=0)),
                       "coefficient_prediction_match": True, "cache_replay_match": True})
        np.savez(out / "features_and_head.npz", train_ids=[r["id"] for r in train],
                 valid_ids=[r["id"] for r in valid], train=Z_train, valid=Z_valid,
                 coef=probe.coef_, intercept=probe.intercept_, classes=probe.classes_, labels=labels)
        peak_memory = torch.cuda.max_memory_allocated() if device.type == "cuda" else None
    else:
        id_to_label = {i: name for name, i in label_to_id.items()}
        model = AutoModelForSequenceClassification.from_pretrained(
            asset, local_files_only=True, trust_remote_code=False, use_safetensors=True,
            num_labels=len(labels), id2label=id_to_label, label2id=label_to_id)
        if args.mode == "head":
            for parameter in model.distilbert.parameters():
                parameter.requires_grad_(False)
        if args.mode == "lora":
            from peft import LoraConfig, TaskType, get_peft_model
            targets = [n for n, m in model.named_modules() if n.endswith(("q_lin", "v_lin")) and isinstance(m, nn.Linear)]
            if not targets or len(targets) != 2 * config.n_layers:
                raise ValueError("Unexpected DistilBERT target modules; review architecture before LoRA")
            lora = LoraConfig(task_type=TaskType.SEQ_CLS, r=args.rank, lora_alpha=2 * args.rank,
                              lora_dropout=0.05, target_modules=["q_lin", "v_lin"],
                              modules_to_save=["pre_classifier", "classifier"], init_lora_weights=True)
            model = get_peft_model(model, lora)
            report["target_modules"] = targets
        model.to(device)
        learned = [p for p in model.parameters() if p.requires_grad]
        if args.mode == "full":
            backbone = list(model.distilbert.parameters())
            backbone_ids = {id(p) for p in backbone}
            head = [p for p in learned if id(p) not in backbone_ids]
            groups = [{"params": backbone, "lr": 1e-5}, {"params": head, "lr": 1e-3}]
        else:
            groups = [{"params": learned, "lr": 1e-3}]
        optimizer = torch.optim.AdamW(groups, weight_decay=0.01)
        criterion = nn.CrossEntropyLoss()

        def evaluate():
            model.eval()
            logits, loss_sum = [], 0.0
            with torch.no_grad():
                for start in range(0, len(valid), args.batch_size):
                    end = min(start + args.batch_size, len(valid))
                    values = model(**tokens(valid[start:end])).logits
                    target = torch.tensor(y_valid[start:end], device=device)
                    loss_sum += criterion(values, target).item() * (end - start)
                    logits.append(values.cpu().numpy())
            values = np.concatenate(logits)
            prediction = values.argmax(1)
            return loss_sum / len(valid), float(f1_score(y_valid, prediction, average="macro", zero_division=0)), values

        if device.type == "cuda":
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
        started = time.perf_counter()
        best_key, best_state, best_step, history = None, None, None, []
        order, position = torch.randperm(len(train)).tolist(), 0
        for step in range(1, args.max_steps + 1):
            if position >= len(order):
                order, position = torch.randperm(len(train)).tolist(), 0
            chosen = order[position:position + args.batch_size]
            position += len(chosen)
            model.train()
            if args.mode == "head":
                model.distilbert.eval()
            optimizer.zero_grad(set_to_none=True)
            values = model(**tokens([train[i] for i in chosen])).logits
            target = torch.tensor(y_train[chosen], device=device)
            loss = criterion(values, target)
            loss.backward()
            optimizer.step()
            if step == 1 or step % 10 == 0 or step == args.max_steps:
                val_loss, val_f1, _ = evaluate()
                history.append({"step": step, "train_batch_loss": loss.item(), "valid_loss": val_loss, "macro_f1": val_f1})
                key = (val_f1, -val_loss)
                if best_key is None or key > best_key:
                    best_key, best_step = key, step
                    best_state = {n: t.detach().cpu().clone() for n, t in model.state_dict().items()}
        model.load_state_dict(best_state)
        val_loss, val_f1, saved_logits = evaluate()
        if device.type == "cuda":
            torch.cuda.synchronize()
        report.update({"train_plus_validation_seconds": time.perf_counter() - started,
                       "trainable_parameters": sum(p.numel() for p in learned),
                       "selection": "highest macro-F1, then lowest loss", "best_step": best_step,
                       "history": history, "valid_loss": val_loss, "macro_f1": val_f1,
                       "accuracy": float(accuracy_score(y_valid, saved_logits.argmax(1)))})
        peak_memory = torch.cuda.max_memory_allocated() if device.type == "cuda" else None
        saved = out / ("adapter" if args.mode == "lora" else "model")
        model.save_pretrained(saved, safe_serialization=True)
        tokenizer.save_pretrained(saved)
        del optimizer, learned, best_state, model, groups, values, loss
        if args.mode == "full":
            del backbone, head
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
        if args.mode == "lora":
            from peft import PeftModel
            base = AutoModelForSequenceClassification.from_pretrained(
                asset, local_files_only=True, trust_remote_code=False, use_safetensors=True,
                num_labels=len(labels), id2label=id_to_label, label2id=label_to_id)
            model = PeftModel.from_pretrained(base, saved, local_files_only=True, is_trainable=False)
        else:
            model = AutoModelForSequenceClassification.from_pretrained(
                saved, local_files_only=True, trust_remote_code=False, use_safetensors=True)
        model.to(device)
        _, _, reloaded_logits = evaluate()
        matches = np.allclose(saved_logits, reloaded_logits, atol=1e-5, rtol=1e-5)
        if not matches:
            raise ValueError("Saved/reloaded logits differ")
        report["reload_logits_match"] = bool(matches)
    report["peak_cuda_allocated_bytes"] = peak_memory
    report["memory_note"] = "CUDA allocator peak, not total device memory; CPU peak memory was not measured"
    report["status"] = "OFFLINE_TRIAL_COMPLETED"
    write_json(out / "RESULT.json", report)
    print(f"{args.mode}: validation macro-F1={report['macro_f1']:.4f}. Receipt: {out / 'RESULT.json'}")


if __name__ == "__main__":
    main()
