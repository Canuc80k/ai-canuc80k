"""Fine-tune TinyUNet 5.6 trên ảnh/mask cục bộ, CPU, mặc định chỉ preflight."""
import argparse
import hashlib
from pathlib import Path
import sys
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F


class TinyUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encode = nn.Sequential(nn.Conv2d(1, 4, 3, padding=1), nn.ReLU())
        self.middle = nn.Sequential(nn.Conv2d(4, 8, 3, padding=1), nn.ReLU())
        self.decode = nn.Sequential(nn.Conv2d(12, 4, 3, padding=1), nn.ReLU())
        self.output = nn.Conv2d(4, 1, 1)

    def forward(self, images):
        skip = self.encode(images)
        low = self.middle(F.max_pool2d(skip, 2))
        up = F.interpolate(low, size=skip.shape[-2:], mode="nearest")
        return self.output(self.decode(torch.cat([skip, up], dim=1)))


class Masks(Dataset):
    def __init__(self, directory, size):
        directory = Path(directory)
        image_dir, mask_dir = directory / "images", directory / "masks"
        if not image_dir.is_dir() or not mask_dir.is_dir():
            raise ValueError(f"Thiếu images/masks trong {directory}")
        image_paths = [p for p in image_dir.iterdir()
                       if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg"]]
        images = {p.stem: p for p in image_paths}
        if len(images) != len(image_paths):
            raise ValueError("Ảnh có basename trùng giữa các extension")
        masks = {p.stem: p for p in mask_dir.iterdir() if p.is_file() and p.suffix.lower() == ".png"}
        if not images or set(images) != set(masks):
            raise ValueError("Ảnh và mask phải có cùng tập basename, không rỗng")
        self.pairs = [(images[key], masks[key]) for key in sorted(images)]
        self.size = size
        for image_path, mask_path in self.pairs:
            with Image.open(image_path) as image, Image.open(mask_path) as mask:
                if image.size != mask.size:
                    raise ValueError(f"Lệch size: {image_path.name}")
                values = np.unique(np.asarray(mask))
                if mask.mode not in ["1", "L"] or not set(values.tolist()) <= {0, 1, 255}:
                    raise ValueError(f"Mask phải nhị phân: {mask_path.name}")

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, index):
        image_path, mask_path = self.pairs[index]
        with Image.open(image_path) as image:
            image = image.convert("L").resize((self.size, self.size), Image.Resampling.BILINEAR)
            x = np.asarray(image, dtype=np.float32).copy() / 255
        with Image.open(mask_path) as mask:
            mask = mask.convert("L").resize((self.size, self.size), Image.Resampling.NEAREST)
            y = (np.asarray(mask) > 0).astype(np.float32)
        return torch.from_numpy(x[None]), torch.from_numpy(y[None])


def mean_dice(model, loader):
    model.eval()
    scores = []
    with torch.inference_mode():
        for images, masks in loader:
            predicted = model(images).sigmoid() >= 0.5
            target = masks.bool()
            intersection = (predicted & target).sum(dim=(1, 2, 3)).float()
            total = predicted.sum(dim=(1, 2, 3)) + target.sum(dim=(1, 2, 3))
            dice = torch.where(total == 0, 1.0, 2 * intersection / total.clamp_min(1))
            scores.extend(dice.tolist())
    return float(np.mean(scores))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--checkpoint")
    parser.add_argument("--sha256")
    parser.add_argument("--from-scratch", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.epochs <= 20 or not 16 <= args.size <= 256:
        raise ValueError("CPU recipe: epochs 1..20, size 16..256")
    train = Masks(Path(args.data) / "train", args.size)
    valid = Masks(Path(args.data) / "valid", args.size)
    print({"train": len(train), "valid": len(valid), "size": args.size,
           "device": "cpu", "split": "đã chia trước theo nguồn"})
    if not args.run:
        print("PREFLIGHT_PASS: dữ liệu hợp schema; chưa train.")
        return
    if bool(args.checkpoint) == bool(args.from_scratch):
        raise ValueError("Chọn đúng một: --checkpoint hoặc --from-scratch")
    if not args.output:
        raise ValueError("Cần --output cho checkpoint mới")
    output = Path(args.output).resolve()
    if output.exists():
        raise ValueError("Output đã tồn tại; chọn tên mới")
    torch.set_num_threads(1)
    torch.manual_seed(56)
    model = TinyUNet()
    if args.checkpoint:
        path = Path(args.checkpoint)
        if not path.is_file() or not args.sha256:
            raise ValueError("Thiếu checkpoint hoặc SHA-256")
        if hashlib.sha256(path.read_bytes()).hexdigest() != args.sha256.lower():
            raise ValueError("SHA-256 không khớp")
        state = torch.load(path, map_location="cpu", weights_only=True)
        if "state_dict" in state:
            state = state["state_dict"]
        model.load_state_dict(state, strict=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    train_loader = DataLoader(train, batch_size=2, shuffle=True, num_workers=0)
    valid_loader = DataLoader(valid, batch_size=2, shuffle=False, num_workers=0)
    best_score = -1.0
    for epoch in range(args.epochs):
        model.train()
        for images, masks in train_loader:
            optimizer.zero_grad()
            loss = F.binary_cross_entropy_with_logits(model(images), masks)
            loss.backward()
            optimizer.step()
        score = mean_dice(model, valid_loader)
        print({"epoch": epoch + 1, "valid_mean_dice": score})
        if score > best_score:
            best_score = score
            best_state = {name: value.detach().clone() for name, value in model.state_dict().items()}
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"state_dict": best_state, "size": args.size,
                "valid_mean_dice": best_score, "threshold": 0.5}, output)
    restored = TinyUNet()
    restored.load_state_dict(torch.load(output, map_location="cpu", weights_only=True)["state_dict"])
    restored.eval()
    with torch.inference_mode():
        images, _ = next(iter(valid_loader))
        print({"reloaded_output_shape": tuple(restored(images).shape),
               "checkpoint": str(output)})


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, RuntimeError) as error:
        print(f"NOT_RUN_OR_FAILED: {error}", file=sys.stderr)
        sys.exit(2)
