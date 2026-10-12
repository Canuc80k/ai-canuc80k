# -*- coding: utf-8 -*-
# Code mẫu — CNN và ResNet

# Ví dụ 1: Học phân biệt nét đứng và nét ngang
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(52)

def make_lines(count, seed):
    rng = np.random.default_rng(seed)
    images = np.zeros((count, 1, 8, 8), dtype=np.float32)
    labels = np.arange(count) % 2
    for i, label in enumerate(labels):
        position = int(rng.integers(2, 5))
        if label == 0:
            images[i, 0, 1:7, position:position + 2] = 1
        else:
            images[i, 0, position:position + 2, 1:7] = 1
    images = np.clip(images + rng.normal(0, 0.04, images.shape), 0, 1)
    return torch.tensor(images, dtype=torch.float32), torch.tensor(labels)

train_x, train_y = make_lines(40, 1)
valid_x, valid_y = make_lines(20, 2)
print("Train:", tuple(train_x.shape), torch.bincount(train_y).tolist())
print("Một ảnh đứng, threshold 0.5:")
print((train_x[0, 0] >= 0.5).int().numpy())

model = nn.Sequential(
    nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(4, 4, 3, padding=1), nn.ReLU(),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(1), nn.Linear(4, 2),
)
shapes = []
batch = train_x[:2]
with torch.no_grad():
    for layer in model:
        batch = layer(batch)
        shapes.append(tuple(batch.shape))
print("Shape qua từng lớp:", shapes)
print("Tham số:", sum(p.numel() for p in model.parameters()))
optimizer = torch.optim.Adam(model.parameters(), lr=0.03)

def measure(x, y):
    model.eval()
    with torch.no_grad():
        logits = model(x)
        return (nn.functional.cross_entropy(logits, y).item(),
                (logits.argmax(1) == y).float().mean().item())

before = measure(valid_x, valid_y)
for step in range(70):
    model.train()
    optimizer.zero_grad()
    loss = nn.functional.cross_entropy(model(train_x), train_y)
    loss.backward()
    optimizer.step()
after = measure(valid_x, valid_y)
print("Valid loss/accuracy trước:", [round(v, 4) for v in before])
print("Valid loss/accuracy sau:", [round(v, 4) for v in after])
assert tuple(model(valid_x[:1]).shape) == (1, 2)
assert after[0] < before[0] and after[1] >= 0.9


# Ví dụ 2: Nhánh bằng 0 có giữ được cả giá trị âm không?
import torch
from torch import nn

torch.set_num_threads(1)
branch = nn.Conv2d(1, 1, 1, bias=False)
with torch.no_grad():
    branch.weight.zero_()
x = torch.tensor([[[[2., -1.]]]], requires_grad=True)
before_relu = x + branch(x)
after_relu = torch.relu(before_relu)
after_relu.sum().backward()
print("Trước ReLU:", before_relu.detach().flatten().tolist())
print("Sau ReLU:", after_relu.detach().flatten().tolist())
print("Gradient theo x:", x.grad.flatten().tolist())
assert before_relu.detach().flatten().tolist() == [2.0, -1.0]
assert x.grad.flatten().tolist() == [1.0, 0.0]


# Ví dụ 3: Đổi số kênh và thu nhỏ ảnh bằng conv 1×1
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(523)
x = torch.ones(2, 4, 8, 8)
main = nn.Conv2d(4, 8, 3, stride=2, padding=1)
skip = nn.Conv2d(4, 8, 1, stride=2, bias=False)
a, b = main(x), skip(x)
result = torch.relu(a + b)
print("Nhánh chính:", tuple(a.shape))
print("Skip projection:", tuple(b.shape))
print("Kết quả:", tuple(result.shape))
print("Số ô input/output:", x.numel(), result.numel())
assert a.shape == b.shape == (2, 8, 4, 4)

