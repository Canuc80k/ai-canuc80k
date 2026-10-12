# -*- coding: utf-8 -*-
# Code mẫu — Phân tích hành vi model

# Ví dụ 1: Accuracy bằng nhau mà dựa vào hai thứ khác nhau
import numpy as np

vertical = np.zeros((8, 8))
horizontal = np.zeros((8, 8))
vertical[2:6, 3:5] = 1
horizontal[3:5, 2:6] = 1
orientation_filter = (horizontal - vertical) / 4
labels = np.array([0, 1, 0, 1])
images = np.stack([vertical if label == 0 else horizontal for label in labels])
images[:, :2, :2] = labels[:, None, None]
changed = images.copy()
changed[:, :2, :2] = 1 - labels[:, None, None]

def predict_pair(batch):
    corner = batch[:, :2, :2].mean((1, 2))
    orientation = (batch * orientation_filter).sum((1, 2))
    return (corner >= 0.5).astype(int), (orientation > 0).astype(int)

assert np.array_equal(images[:, 2:, 2:], changed[:, 2:, 2:])
for name, batch in [("Nguồn", images), ("Đảo dấu góc", changed)]:
    a, b = predict_pair(batch)
    print(name, "A/B accuracy:", float((a == labels).mean()), float((b == labels).mean()))
    print("A/B prediction:", a.tolist(), b.tolist())
print("Shape score đứng/ngang:",
      float((vertical * orientation_filter).sum()), float((horizontal * orientation_filter).sum()))
assert predict_pair(changed)[0].tolist() == [1, 0, 1, 0]
assert predict_pair(changed)[1].tolist() == labels.tolist()


# Ví dụ 2: Che từng vùng, rồi so điểm của cùng một lớp
import numpy as np

vertical = np.zeros((8, 8)); vertical[2:6, 3:5] = 1
horizontal = np.zeros((8, 8)); horizontal[3:5, 2:6] = 1
orientation_filter = (horizontal - vertical) / 4
original = horizontal.copy(); original[:2, :2] = 1
cover_corner = original.copy(); cover_corner[:2, :2] = 0
cover_shape = original.copy(); cover_shape[2:6, 2:6] = 0
batch = np.stack([original, cover_corner, cover_shape])
corner_logit = 8 * (batch[:, :2, :2].mean((1, 2)) - 0.5)
shape_logit = 6 * (batch * orientation_filter).sum((1, 2))
sigmoid = lambda z: 1 / (1 + np.exp(-z))
print("Thứ tự: gốc, che góc, che nét")
print("A, P(lớp 1):", sigmoid(corner_logit).round(4).tolist())
print("B, P(lớp 1):", sigmoid(shape_logit).round(4).tolist())
assert sigmoid(corner_logit)[0] == sigmoid(corner_logit)[2]
assert sigmoid(shape_logit)[0] == sigmoid(shape_logit)[1]
assert sigmoid(shape_logit)[2] == 0.5


# Ví dụ 3: Saliency có khớp với việc thay một pixel thật không?
from pathlib import Path
import torch
import matplotlib.pyplot as plt

torch.set_num_threads(1)
plt.rcParams["svg.hashsalt"] = "vision-5.9-saliency"
vertical = torch.zeros(8, 8); vertical[2:6, 3:5] = 1
horizontal = torch.zeros(8, 8); horizontal[3:5, 2:6] = 1
orientation_filter = (horizontal - vertical) / 4
image = horizontal.clone().requires_grad_(True)
score = 3 * (image * orientation_filter).sum()
score.backward()
saliency = image.grad.abs()
epsilon = 0.001
changed = image.detach().clone(); changed[3, 2] += epsilon
finite_difference = (3 * (changed * orientation_filter).sum() - score.detach()) / epsilon
print("Score lớp ngang:", score.item())
print("Gradient tại (3,2):", image.grad[3, 2].item())
print("Sai phân hữu hạn:", round(finite_difference.item(), 4))
print("Tổng |gradient| vùng góc:", saliency[:2, :2].sum().item())
print("Số pixel gradient khác 0:", int((saliency > 0).sum()))
assert torch.isclose(finite_difference, image.grad[3, 2], atol=1e-3)
assert saliency[:2, :2].sum() == 0

fig, axes = plt.subplots(2, 1, figsize=(4, 5))
for axis, values, title in [(axes[0], image.detach().numpy(), "Ảnh đầu vào"),
                             (axes[1], saliency.numpy(), "|Gradient|")]:
    axis.imshow(values, cmap="magma", vmin=0, vmax=1)
    axis.set_title(title, fontsize=13)
    axis.set_xticks([]); axis.set_yticks([])
fig.tight_layout()
Path("fig").mkdir(exist_ok=True)
fig.savefig("fig/5.9-saliency-code.svg", metadata={"Date": None})
plt.show()
plt.close(fig)
print("Hình:", "fig/5.9-saliency-code.svg")

