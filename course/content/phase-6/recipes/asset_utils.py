"""Đọc asset local có receipt; không tải weights, không chạy remote code."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"


def require_environment():
    versions = {}
    for name in ["torch", "transformers", "tokenizers", "safetensors"]:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as error:
            raise RuntimeError(f"Thiếu package {name}; chuẩn bị môi trường được phép trước khi chạy") from error
    return versions


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_asset(directory, manifest_path, expected_repo, expected_license="apache-2.0"):
    root = Path(directory).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Asset path phải là thư mục local")
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    if manifest.get("repo_id") != expected_repo:
        raise ValueError("Repo ID của manifest không khớp recipe")
    if manifest.get("license") != expected_license or manifest.get("license_reviewed") is not True:
        raise ValueError("Cần license đúng và xác nhận đã đọc điều kiện trong manifest")
    if re.fullmatch(r"[0-9a-f]{40}", manifest.get("revision", "")) is None:
        raise ValueError("Revision phải là commit SHA cụ thể, không dùng main hoặc placeholder")
    expected_files = manifest.get("files")
    if not isinstance(expected_files, dict) or not expected_files:
        raise ValueError("Manifest phải liệt kê SHA-256 các file asset")
    actual_names = {str(path.relative_to(root)).replace("\\", "/")
                    for path in root.rglob("*") if path.is_file()}
    if set(expected_files) != actual_names:
        raise ValueError("Tập file asset khác manifest; dùng thư mục snapshot gọn có receipt ngoài asset")
    for name, expected_digest in expected_files.items():
        path = (root / name).resolve(strict=True)
        if not path.is_relative_to(root):
            raise ValueError("File manifest vượt ngoài asset root")
        if re.fullmatch(r"[0-9a-f]{64}", expected_digest) is None or sha256(path) != expected_digest:
            raise ValueError(f"Hash không khớp: {name}")
    if "config.json" not in expected_files:
        raise ValueError("Asset thiếu config.json")
    if not any(name.endswith(".safetensors") for name in expected_files):
        raise ValueError("Recipe yêu cầu weights safetensors local")
    if not any(Path(name).name.upper().startswith("LICENSE") for name in expected_files):
        raise ValueError("Asset cần giữ file license để đọc lại")
    return root, manifest


def choose_device(requested):
    import torch
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("Yêu cầu CUDA nhưng môi trường không có CUDA khả dụng")
    return torch.device(requested)
