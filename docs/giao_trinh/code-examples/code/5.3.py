# -*- coding: utf-8 -*-
# Code mẫu — Augmentation và transfer learning

# Ví dụ 1: Lật ảnh thì phải lật cả box và mask
import numpy as np

mask = np.zeros((4, 8), dtype=np.uint8)
mask[1:3, 1:4] = 1
image = 30 + 180 * mask.astype(np.int16)
box = np.array([1, 1, 4, 3])

def flip_box(box, width):
    x1, y1, x2, y2 = box
    return np.array([width - x2, y1, width - x1, y2])

flipped_image = np.flip(image, axis=1).copy()
flipped_mask = np.flip(mask, axis=1).copy()
flipped_box = flip_box(box, image.shape[1])
print("Mask trước:")
print(mask)
print("Mask sau:")
print(flipped_mask)
print("Box sau:", flipped_box.tolist())
print("Diện tích trước/sau:", int(mask.sum()), int(flipped_mask.sum()))
assert np.array_equal(flipped_image > 100, flipped_mask == 1)
assert np.array_equal(flip_box(flipped_box, 8), box)
assert np.array_equal(np.flip(flipped_mask, axis=1), mask)


# Ví dụ 2: Resize mask, và nhãn có hướng
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
mask = torch.tensor([[[[0., 2.], [0., 2.]]]])
nearest = F.interpolate(mask, size=(2, 4), mode="nearest")
bilinear = F.interpolate(mask, size=(2, 4), mode="bilinear", align_corners=False)
print("Nearest, hàng đầu:", nearest[0, 0, 0].tolist())
print("Bilinear, hàng đầu:", bilinear[0, 0, 0].tolist())
assert set(nearest.unique().tolist()) <= {0.0, 2.0}
assert 0.5 in bilinear.unique().tolist()

left_arrow = torch.tensor([[0, 1, 0, 0], [1, 1, 1, 1], [0, 1, 0, 0]])
right_arrow = left_arrow.flip(1)
label_after_flip = {"trái": "phải", "phải": "trái"}["trái"]
print("Mũi tên sau lật:", right_arrow.tolist())
print("Nhãn sau lật:", label_after_flip)


# Ví dụ 3: Học lớp đầu ra, và phát hiện thống kê vẫn bị đổi
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(53)
encoder = nn.Sequential(nn.Conv2d(1, 4, 3, padding=1), nn.BatchNorm2d(4),
                        nn.ReLU(), nn.AdaptiveAvgPool2d(1), nn.Flatten(1))
head = nn.Linear(4, 2)
images = torch.stack([torch.zeros(1, 6, 6), torch.ones(1, 6, 6)] * 3)
labels = torch.tensor([0, 1] * 3)
for p in encoder.parameters():
    p.requires_grad_(False)
encoder.eval()
optimizer = torch.optim.SGD(head.parameters(), lr=0.5)
before = {name: value.clone() for name, value in encoder.state_dict().items()}
head_before = head.weight.detach().clone()
with torch.no_grad():
    features = encoder(images)
for step in range(20):
    optimizer.zero_grad()
    loss = nn.functional.cross_entropy(head(features), labels)
    loss.backward()
    optimizer.step()
print("Features:", tuple(features.shape))
print("Encoder cả parameter/buffer giữ nguyên:",
      all(torch.equal(value, encoder.state_dict()[name]) for name, value in before.items()))
print("Head đã đổi:", not torch.equal(head_before, head.weight))
assert all(p.grad is None for p in encoder.parameters())
assert not torch.equal(head_before, head.weight)

running_before = encoder[1].running_mean.clone()
encoder.train()
with torch.no_grad():
    encoder(images)
print("Parameter còn đóng băng:", all(not p.requires_grad for p in encoder.parameters()))
print("Running mean đã đổi:", not torch.equal(running_before, encoder[1].running_mean))
encoder.eval()
assert not torch.equal(running_before, encoder[1].running_mean)

