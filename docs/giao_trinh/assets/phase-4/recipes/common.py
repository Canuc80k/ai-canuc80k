"""Local asset/data checks shared by the optional real-model recipes."""
from pathlib import Path
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import sys


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reviewed_note(path):
    path = Path(path).resolve()
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("License/source review note is empty")
    return {"text": text, "sha256": sha256(path)}


def checked_asset(directory, expected_model):
    directory = Path(directory).resolve()
    manifest_path = directory / "ASSET.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["model_id"] != expected_model:
        raise ValueError(f"Expected {expected_model}, got {manifest['model_id']}")
    if not manifest.get("license_review", {}).get("text"):
        raise ValueError("Asset has no saved license/source review")
    for row in manifest["files"]:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Manifest contains an unsafe relative path")
        actual = (directory / relative).resolve()
        if not actual.is_relative_to(directory) or actual.is_symlink():
            raise ValueError("Asset file escapes asset directory")
        if sha256(actual) != row["sha256"]:
            raise ValueError(f"Asset hash mismatch: {relative}")
    if not (directory / "config.json").is_file():
        raise ValueError("Missing config.json")
    if not list(directory.glob("*.safetensors")):
        raise ValueError("Recipe requires local Safetensors weights")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    return directory, manifest, sha256(manifest_path)


def environment(torch):
    packages = {}
    for name in ["torch", "transformers", "huggingface-hub", "safetensors", "peft", "scikit-learn", "numpy", "pillow"]:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {"python": sys.version.split()[0], "platform": platform.platform(),
            "packages": packages, "cuda_available": torch.cuda.is_available()}


def device_checked(torch, requested):
    if requested == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA requested but unavailable; use --device cpu for a small trial")
    return torch.device(requested)


def read_text_split(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError("Empty text split")
    required = {"id", "text", "label", "group"}
    if not required.issubset(rows[0]):
        raise ValueError("CSV needs id,text,label,group columns")
    for row in rows:
        for key in required:
            row[key] = row[key].strip()
            if not row[key]:
                raise ValueError(f"Empty {key} in text CSV")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate IDs within split")
    return rows


def check_text_splits(train, valid):
    for key in ["id", "group"]:
        if {r[key] for r in train} & {r[key] for r in valid}:
            raise ValueError(f"Train/validation overlap in {key}")
    # Catch exact text duplicates even when IDs/groups were changed.
    normalize = lambda text: " ".join(text.lower().split())
    if {normalize(r["text"]) for r in train} & {normalize(r["text"]) for r in valid}:
        raise ValueError("Exact normalized text overlap across train/validation")
    labels = sorted({r["label"] for r in train})
    if len(labels) < 2 or not {r["label"] for r in valid}.issubset(labels):
        raise ValueError("Need at least two train labels and no unknown validation labels")
    return labels


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
