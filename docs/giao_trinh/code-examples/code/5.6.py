# -*- coding: utf-8 -*-
# Code mẫu — Image segmentation

# Ví dụ 1: Bỏ sót toàn bộ vật thể mà accuracy vẫn cao
import numpy as np

def metrics(prediction, target):
    p, g = np.asarray(prediction, bool), np.asarray(target, bool)
    assert p.shape == g.shape
    intersection = int((p & g).sum())
    union = int((p | g).sum())
    total = int(p.sum() + g.sum())
    return (float((p == g).mean()),
            1.0 if union == 0 else intersection / union,
            1.0 if total == 0 else 2 * intersection / total)

target = np.zeros((10, 10), dtype=bool)
target[2:4, 2:4] = True
all_background = np.zeros_like(target)
partial = target.copy()
partial[3, 3] = False
partial[0, 0] = True
for name, prediction in [("Toàn nền", all_background), ("Tìm một phần", partial)]:
    print(name, "accuracy/IoU/Dice:", [round(v, 4) for v in metrics(prediction, target)])
print("Hai mask rỗng:", metrics(all_background, all_background))
assert metrics(all_background, target) == (0.96, 0.0, 0.0)
assert metrics(partial, target)[1:] == (0.6, 0.75)


# Ví dụ 2: Một U-Net nhỏ tìm hình chữ nhật sáng
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

torch.set_num_threads(1)
torch.manual_seed(56)

def make_rectangles(count, seed):
    rng = np.random.default_rng(seed)
    masks = np.zeros((count, 1, 8, 8), dtype=np.float32)
    for i in range(count):
        row, col = rng.integers(1, 5, size=2)
        masks[i, 0, row:row + 3, col:col + 2] = 1
    images = np.clip(0.1 + 0.8 * masks + rng.normal(0, 0.04, masks.shape), 0, 1)
    return torch.tensor(images, dtype=torch.float32), torch.from_numpy(masks)

train_x, train_y = make_rectangles(16, 1)
valid_x, valid_y = make_rectangles(4, 2)
print("Ảnh:", tuple(train_x.shape))
print("Mask đầu:")
print(train_y[0, 0].int().numpy())
print("Pixel foreground mỗi ảnh:", train_y.sum((1, 2, 3)).int().tolist())

class SmallUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encode = nn.Sequential(nn.Conv2d(1, 4, 3, padding=1), nn.ReLU())
        self.middle = nn.Sequential(nn.Conv2d(4, 8, 3, padding=1), nn.ReLU())
        self.decode = nn.Sequential(nn.Conv2d(12, 4, 3, padding=1), nn.ReLU())
        self.head = nn.Conv2d(4, 1, 1)

    def forward(self, x):
        skip = self.encode(x)
        low = self.middle(F.max_pool2d(skip, 2))
        up = F.interpolate(low, size=skip.shape[-2:], mode="nearest")
        return self.head(self.decode(torch.cat([skip, up], dim=1)))

model = SmallUNet()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
# Hệ số tính từ mask train, không dùng nhãn validation.
positive_weight = (train_y.numel() - train_y.sum()) / train_y.sum()
criterion = nn.BCEWithLogitsLoss(pos_weight=positive_weight.reshape(1))
with torch.no_grad():
    before = criterion(model(valid_x), valid_y).item()
print("Logits batch hai ảnh:", tuple(model(train_x[:2]).shape))
print("pos_weight:", round(positive_weight.item(), 4))
for step in range(80):
    optimizer.zero_grad()
    loss = criterion(model(train_x), train_y)
    loss.backward()
    optimizer.step()
model.eval()
with torch.no_grad():
    logits = model(valid_x)
    after = criterion(logits, valid_y).item()
    prediction = logits.sigmoid() >= 0.5
g = valid_y.bool()
intersection = (prediction & g).sum((1, 2, 3))
union = (prediction | g).sum((1, 2, 3))
iou = intersection.float() / union
print("Valid BCE trước/sau:", round(before, 4), round(after, 4))
print("IoU từng ảnh:", [round(v, 4) for v in iou.tolist()])
print("Ảnh kích thước lẻ:", tuple(model(torch.zeros(1, 1, 9, 7)).shape))
assert after < before and iou.mean().item() > 0.8
assert model(torch.zeros(1, 1, 9, 7)).shape == (1, 1, 9, 7)


# Ví dụ 3: RLE phải đúng thứ tự và đúng điểm bắt đầu
import numpy as np

def encode(mask):
    mask = np.asarray(mask)
    assert np.isin(mask, [0, 1]).all()
    values = mask.astype(np.uint8).ravel(order="C")
    changes = np.flatnonzero(np.diff(np.r_[0, values, 0])) + 1
    changes[1::2] -= changes[::2]
    return changes.tolist()

def decode(runs, shape):
    assert len(runs) % 2 == 0
    flat = np.zeros(np.prod(shape), dtype=np.uint8)
    end_previous = 0
    for start, length in zip(runs[::2], runs[1::2]):
        assert start > end_previous and length > 0
        assert start - 1 + length <= len(flat)
        flat[start - 1:start - 1 + length] = 1
        end_previous = start - 1 + length
    return flat.reshape(shape, order="C")

mask = np.array([[0, 1, 0], [1, 1, 0]], dtype=np.uint8)
for name, m in [("Mẫu", mask), ("Rỗng", np.zeros_like(mask)), ("Kín", np.ones_like(mask))]:
    runs = encode(m)
    print(name, runs, "round trip:", np.array_equal(m, decode(runs, m.shape)))
assert encode(mask) == [2, 1, 4, 2]
wrong_order = decode(encode(mask), mask.shape).ravel().reshape(mask.shape, order="F")
print("Cùng bytes, đọc theo cột có đúng mask:", np.array_equal(mask, wrong_order))
assert not np.array_equal(mask, wrong_order)

