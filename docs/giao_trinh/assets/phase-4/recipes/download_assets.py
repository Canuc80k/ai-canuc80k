"""Explicit online preparation only; no download occurs without --download.

Requires a pinned 40-hex Hub revision and a saved source/license review note.
This does not install packages, upload files, or train models.
"""
from pathlib import Path
import argparse
import os
import re
from common import reviewed_note, sha256, write_json

MODELS = {
    "distilbert": ("distilbert/distilbert-base-uncased", "apache-2.0"),
    "clip": ("openai/clip-vit-base-patch32", "mit"),
    "gpt2": ("openai-community/gpt2", "mit"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODELS, required=True)
    parser.add_argument("--revision", required=True, help="exact 40-hex commit from the model repository")
    parser.add_argument("--license-review", required=True, help="UTF-8 note with sources, license terms and intended use")
    parser.add_argument("--dest", required=True)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-fA-F]{40}", args.revision):
        parser.error("--revision must be an exact 40-hex commit, not main")
    review = reviewed_note(args.license_review)
    if not args.download:
        raise SystemExit("No download requested. Read the asset/license requirements; add --download for online preparation.")
    dest = Path(args.dest).resolve()
    if dest.exists() and any(dest.iterdir()):
        raise ValueError("Destination is not empty; choose a new asset directory")
    repo, reviewed_license = MODELS[args.model]
    os.environ["HF_HUB_OFFLINE"] = "0"
    from huggingface_hub import HfApi, snapshot_download
    info = HfApi().model_info(repo, revision=args.revision)
    if info.sha.lower() != args.revision.lower():
        raise ValueError("Resolved commit differs from requested commit")
    metadata_license = getattr(info.card_data, "license", None)
    if metadata_license and metadata_license != reviewed_license:
        raise ValueError(f"Model card license changed: {metadata_license}; review source before use")
    snapshot_download(repo_id=repo, revision=args.revision, local_dir=dest,
                      allow_patterns=["*.json", "*.txt", "*.model", "*.safetensors", "README.md", "LICENSE*"])
    files = []
    for path in sorted(dest.rglob("*")):
        if path.is_file() and ".cache" not in path.relative_to(dest).parts:
            files.append({"path": path.relative_to(dest).as_posix(), "bytes": path.stat().st_size,
                          "sha256": sha256(path)})
    if not (dest / "config.json").is_file() or not list(dest.glob("*.safetensors")):
        raise ValueError("Incomplete asset: need config and root Safetensors weights")
    write_json(dest / "ASSET.json", {"model_id": repo, "revision": info.sha,
               "reviewed_license": reviewed_license, "model_card_license": metadata_license,
               "license_review": review, "files": files,
               "status": "DOWNLOADED_NOT_YET_VALIDATED_OFFLINE"})
    print(f"Prepared {repo} at {info.sha}: {len(files)} hashed files. Run offline recipe next.")


if __name__ == "__main__":
    main()
