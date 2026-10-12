"""Offline local assets recipe for Whisper ASR / HuBERT-wav2vec2 embeddings.

No downloads, no package installation, no random model fallback.
--check validates paths/config/WAV/manifest without loading weights.
--self-check only checks array/scorer/length arithmetic, not pretrained inference.
See README.md for manifest and exact invocation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import sys
import time

import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def pcm_to_float(array):
    array = np.asarray(array)
    if array.dtype == np.uint8:
        result = (array.astype(np.float32) - 128) / 128
    elif np.issubdtype(array.dtype, np.signedinteger):
        divisor = float(2 ** (np.iinfo(array.dtype).bits - 1))
        result = array.astype(np.float32) / divisor
    elif np.issubdtype(array.dtype, np.floating):
        result = array.astype(np.float32)
    else:
        raise ValueError(f"unsupported WAV dtype: {array.dtype}")
    if result.ndim == 2:
        result = result.mean(axis=1)  # Explicit mean downmix; check phase before real use.
    if result.ndim != 1 or result.size == 0:
        raise ValueError("WAV must contain nonempty mono or channel-last stereo data")
    if not np.isfinite(result).all():
        raise ValueError("nonfinite audio values")
    return result


def load_audio(path, expected_rate, maximum_seconds):
    rate, raw = wavfile.read(path)
    if not isinstance(rate, int) or rate <= 0:
        raise ValueError("invalid sample rate")
    waveform = pcm_to_float(raw)
    duration = len(waveform) / rate
    if duration > maximum_seconds:
        raise ValueError(f"{path.name}: {duration:.2f}s exceeds {maximum_seconds}s; chunking is not implemented")
    if rate != expected_rate:
        factor = math.gcd(rate, expected_rate)
        waveform = resample_poly(waveform, expected_rate // factor, rate // factor).astype(np.float32)
    return waveform, {"original_sample_rate": rate, "sample_rate": expected_rate,
                      "duration_seconds": duration, "num_samples": len(waveform),
                      "silent": bool(np.max(np.abs(waveform)) < 1e-8),
                      "peak": float(np.max(np.abs(waveform)))}


def token_errors(reference, prediction):
    left, right = reference.lower().split(), prediction.lower().split()
    previous = list(range(len(right) + 1))
    for row, token in enumerate(left, start=1):
        current = [row]
        for column, predicted_token in enumerate(right, start=1):
            current.append(min(previous[column] + 1, current[column - 1] + 1,
                               previous[column - 1] + (token != predicted_token)))
        previous = current
    return previous[-1], len(left)


def output_length(length, kernels, strides):
    if len(kernels) != len(strides) or not kernels:
        raise ValueError("invalid convolution kernel/stride config")
    for kernel, stride in zip(kernels, strides):
        length = (length - kernel) // stride + 1
        if length <= 0:
            raise ValueError("waveform is too short for feature encoder")
    return length


def versions():
    result = {"python": sys.version.split()[0]}
    for package in ["numpy", "scipy", "torch", "transformers", "scikit-learn", "safetensors"]:
        try:
            result[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            result[package] = "NOT_INSTALLED"
    return result


def weight_files(checkpoint):
    single = checkpoint / "model.safetensors"
    index = checkpoint / "model.safetensors.index.json"
    if single.is_file():
        return [single]
    if index.is_file():
        mapping = json.loads(index.read_text(encoding="utf-8"))["weight_map"]
        files = []
        for relative in sorted(set(mapping.values())):
            path = (checkpoint / relative).resolve()
            if not path.is_relative_to(checkpoint) or not path.is_file():
                raise ValueError("missing or escaping safetensors shard")
            files.append(path)
        return [index, *files]
    raise ValueError("local model.safetensors or indexed safetensors shards are required")


def preflight(args):
    if args.checkpoint is None or args.manifest is None:
        raise ValueError("--checkpoint and --manifest are required for check/run")
    checkpoint = Path(args.checkpoint).resolve()
    manifest_path = Path(args.manifest).resolve()
    if not checkpoint.is_dir() or not manifest_path.is_file():
        raise ValueError("ASSETS_REQUIRED: checkpoint directory or manifest file is missing")
    config_path = checkpoint / "config.json"
    processor_path = checkpoint / "preprocessor_config.json"
    if not config_path.is_file() or not processor_path.is_file():
        raise ValueError("config.json and preprocessor_config.json are required")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    preprocessing = json.loads(processor_path.read_text(encoding="utf-8"))
    model_type = config.get("model_type")
    accepted = {"whisper"} if args.task == "asr" else {"hubert", "wav2vec2"}
    if model_type not in accepted:
        raise ValueError(f"adapter {args.task} does not support model_type={model_type}; use its own documented adapter")
    expected_rate = preprocessing.get("sampling_rate")
    if type(expected_rate) is not int or expected_rate <= 0:
        raise ValueError("processor sampling_rate must be a positive integer")
    files = weight_files(checkpoint)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("normalization") != "lowercase_whitespace":
        raise ValueError("recipe metric requires explicit normalization=lowercase_whitespace; adapt to the real scorer")
    data_root = (manifest_path.parent / manifest["data_root"]).resolve()
    records = manifest.get("records", [])
    if not records:
        raise ValueError("manifest has no records")
    seen_ids, grouped_splits, checked = set(), {}, []
    for row in records:
        identifier, group, split = row.get("id"), row.get("group"), row.get("split")
        if not isinstance(identifier, str) or not identifier or identifier in seen_ids:
            raise ValueError("missing or duplicate sample ID")
        if not isinstance(group, str) or not group or split not in {"train", "validation"}:
            raise ValueError("each record needs group and train/validation split")
        if group in grouped_splits and grouped_splits[group] != split:
            raise ValueError(f"group leakage: {group}")
        grouped_splits[group] = split
        seen_ids.add(identifier)
        path = (data_root / row["path"]).resolve()
        if not path.is_relative_to(data_root) or not path.is_file() or path.suffix.lower() != ".wav":
            raise ValueError(f"missing/escaping/non-WAV input for {identifier}")
        if args.task == "asr" and not isinstance(row.get("reference"), str):
            raise ValueError("ASR records require string reference")
        if args.task == "embedding" and type(row.get("label")) is not int:
            raise ValueError("embedding records require integer class label")
        _, audio_info = load_audio(path, expected_rate, args.maximum_seconds)
        checked.append({**row, "absolute_path": str(path), "sha256": digest(path), **audio_info})
    if not any(row["split"] == "validation" for row in checked):
        raise ValueError("validation records required")
    if args.task == "embedding":
        class_names = manifest.get("class_names")
        if not isinstance(class_names, list) or len(class_names) < 2 or len(set(class_names)) != len(class_names):
            raise ValueError("unique class_names in output-column order required")
        if any(row["label"] not in range(len(class_names)) for row in checked):
            raise ValueError("class label outside class_names mapping")
        train_labels = {row["label"] for row in checked if row["split"] == "train"}
        if train_labels != set(range(len(class_names))):
            raise ValueError("train must contain every class for this linear probe recipe")
    required_packages = ["numpy", "scipy", "torch", "transformers", "safetensors"]
    if args.task == "embedding":
        required_packages.append("scikit-learn")
    for package in required_packages:
        if versions()[package] == "NOT_INSTALLED":
            raise ValueError(f"missing dependency {package}; prepare a task virtual environment, no automatic installation")
    metadata_files = [config_path, processor_path]
    for name in ["tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt", "generation_config.json"]:
        if (checkpoint / name).is_file():
            metadata_files.append(checkpoint / name)
    receipt = {
        "state": "PREFLIGHT_ONLY_WEIGHTS_NOT_LOADED",
        "task": args.task,
        "checkpoint": str(checkpoint),
        "model_type": model_type,
        "manifest": str(manifest_path),
        "manifest_sha256": digest(manifest_path),
        "normalization": "lowercase_whitespace",
        "versions": versions(),
        "checkpoint_sha256": {str(path.relative_to(checkpoint)): digest(path) for path in [*metadata_files, *files]},
        "records": checked,
    }
    return config, manifest, receipt


def run_asr(args, receipt):
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    import torch
    checkpoint = receipt["checkpoint"]
    processor = WhisperProcessor.from_pretrained(checkpoint, local_files_only=True)
    model, loading = WhisperForConditionalGeneration.from_pretrained(
        checkpoint, local_files_only=True, use_safetensors=True, output_loading_info=True
    )
    if loading.get("missing_keys") or loading.get("mismatched_keys"):
        raise ValueError("checkpoint has missing/mismatched weights; random fallback is forbidden")
    model = model.to(device="cpu", dtype=torch.float32).eval()
    model.generation_config.forced_decoder_ids = None
    results = []
    started = time.perf_counter()
    for row in receipt["records"]:
        if row["split"] != "validation":
            continue
        waveform, _ = load_audio(Path(row["absolute_path"]), row["sample_rate"], args.maximum_seconds)
        inputs = processor(waveform, sampling_rate=row["sample_rate"], return_tensors="pt", return_attention_mask=True)
        before = time.perf_counter()
        with torch.inference_mode():
            token_ids = model.generate(**inputs, language=args.language, task="transcribe",
                                       max_new_tokens=256, do_sample=False)
        prediction = processor.batch_decode(token_ids, skip_special_tokens=True)[0]
        errors, reference_tokens = token_errors(row["reference"], prediction)
        results.append({"id": row["id"], "group": row["group"], "reference": row["reference"],
                        "prediction": prediction, "errors": errors, "reference_tokens": reference_tokens,
                        "silent": row["silent"], "duration_seconds": row["duration_seconds"],
                        "inference_seconds": time.perf_counter() - before})
    denominator = sum(row["reference_tokens"] for row in results)
    if denominator == 0:
        raise ValueError("corpus reference has no tokens; define an empty-reference policy before reporting WER")
    receipt.update(state="ASR_RUN_WITH_LOCAL_CHECKPOINT", language=args.language, task_token="transcribe",
                   total_seconds=time.perf_counter() - started,
                   corpus_wer=sum(row["errors"] for row in results) / denominator, predictions=results)


def run_embeddings(args, config, manifest, receipt, output):
    from transformers import AutoFeatureExtractor, AutoModel
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
    import torch
    extractor = AutoFeatureExtractor.from_pretrained(receipt["checkpoint"], local_files_only=True)
    model, loading = AutoModel.from_pretrained(receipt["checkpoint"], local_files_only=True,
                                             use_safetensors=True, output_loading_info=True)
    if loading.get("missing_keys") or loading.get("mismatched_keys"):
        raise ValueError("encoder checkpoint has missing/mismatched weights; no random replacement")
    model = model.to(device="cpu", dtype=torch.float32).eval()
    kernels, strides = config["conv_kernel"], config["conv_stride"]
    vectors = []
    started = time.perf_counter()
    for row in receipt["records"]:
        waveform, _ = load_audio(Path(row["absolute_path"]), row["sample_rate"], args.maximum_seconds)
        inputs = extractor(waveform, sampling_rate=row["sample_rate"], return_tensors="pt")
        # One clip at a time: no batch padding. Do not invent a waveform attention mask
        # when the checkpoint's extractor deliberately omits it.
        with torch.inference_mode():
            hidden = model(**inputs).last_hidden_state
        valid_length = output_length(len(waveform), kernels, strides)
        if hidden.shape[1] != valid_length:
            raise ValueError("encoder length differs from unpadded convolution recipe; inspect config")
        frame_mask = torch.arange(hidden.shape[1])[None, :] < valid_length
        pooled = (hidden * frame_mask[..., None]).sum(dim=1) / frame_mask.sum(dim=1, keepdim=True)
        vector = pooled[0].numpy()
        if not np.isfinite(vector).all():
            raise ValueError("nonfinite pretrained embedding")
        vectors.append(vector)
    vectors = np.stack(vectors)
    targets = np.array([row["label"] for row in receipt["records"]])
    train = np.array([row["split"] == "train" for row in receipt["records"]])
    valid = ~train
    classifier = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=7))
    classifier.fit(vectors[train], targets[train])
    prediction = classifier.predict(vectors[valid])
    probability = classifier.predict_proba(vectors[valid])
    np.savez_compressed(output / "embedding-probe.npz", vectors=vectors, labels=targets,
                        ids=np.array([row["id"] for row in receipt["records"]]),
                        split=np.array([row["split"] for row in receipt["records"]]),
                        scaler_mean=classifier[0].mean_, scaler_scale=classifier[0].scale_,
                        coefficients=classifier[1].coef_, intercept=classifier[1].intercept_,
                        classes=classifier[1].classes_, valid_predictions=prediction, valid_probabilities=probability)
    receipt.update(state="EMBEDDING_PROBE_RUN_WITH_LOCAL_CHECKPOINT", vector_shape=list(vectors.shape),
                   class_names=manifest["class_names"], total_seconds=time.perf_counter() - started,
                   accuracy=float(accuracy_score(targets[valid], prediction)),
                   macro_f1=float(f1_score(targets[valid], prediction, average="macro", labels=classifier[1].classes_)),
                   confusion_matrix=confusion_matrix(targets[valid], prediction, labels=classifier[1].classes_).tolist())


def self_check():
    assert np.allclose(pcm_to_float(np.array([-32768, 0, 32767], np.int16)), [-1, 0, 32767 / 32768])
    assert np.allclose(pcm_to_float(np.array([0, 128, 255], np.uint8)), [-1, 0, 127 / 128])
    assert np.allclose(pcm_to_float(np.zeros(4, np.float32)), 0)
    kernels, strides = [10, 3, 3, 3, 3, 2, 2], [5, 2, 2, 2, 2, 2, 2]
    assert output_length(16000, kernels, strides) == 49
    assert output_length(32000, kernels, strides) == 99
    assert token_errors("em học ai hôm nay", "em học toán nay") == (2, 5)
    assert token_errors("", "a b") == (2, 0)
    print(json.dumps({"state": "SELF_CHECK_PASS_NO_PRETRAINED_INFERENCE", "pcm_cases": 3,
                      "encoder_lengths": [49, 99], "edit_distance_cases": 2,
                      "versions": versions()}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=["asr", "embedding"], default="asr")
    parser.add_argument("--checkpoint")
    parser.add_argument("--manifest")
    parser.add_argument("--out")
    parser.add_argument("--language", default="vietnamese")
    parser.add_argument("--maximum-seconds", type=float, default=30.0)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--run", action="store_true")
    action.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.maximum_seconds <= 0 or args.maximum_seconds > 30:
        raise ValueError("this short-clip CPU recipe supports 0 < maximum-seconds <= 30")
    if args.self_check:
        self_check()
        return
    config, manifest, receipt = preflight(args)
    if args.check:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return
    if args.out is None:
        raise ValueError("--out is required for an actual run")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    output = Path(args.out).resolve()
    output.mkdir(parents=True, exist_ok=True)
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(7)
    if args.task == "asr":
        run_asr(args, receipt)
    else:
        run_embeddings(args, config, manifest, receipt, output)
    (output / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in receipt.items()
                      if key not in {"records", "checkpoint_sha256", "predictions"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, ImportError, RuntimeError) as error:
        print(f"RECIPE_STOP: {error}", file=sys.stderr)
        sys.exit(2)
