# -*- coding: utf-8 -*-
# Code mẫu — Vision Transformer

# Ví dụ 1: Ảnh 4×4 thành bốn token
import torch
from torch import nn

torch.set_num_threads(1)
image = torch.arange(16, dtype=torch.float32).reshape(1, 1, 4, 4)
windows = image.unfold(2, 2, 2).unfold(3, 2, 2)
# Đưa trục hàng và cột của patch lên trước các trục bên trong patch, rồi mới gộp.
patches = windows.permute(0, 2, 3, 1, 4, 5).reshape(1, 4, 4)
projection = nn.Linear(4, 3, bias=False)
with torch.no_grad():
    projection.weight.copy_(torch.tensor([[1., 0., 0., 0.],
                                          [0., 1., 0., 0.],
                                          [0.25, 0.25, 0.25, 0.25]]))
tokens = projection(patches)
print("Patch:", patches[0].int().tolist())
print("Token:", tokens[0].detach().tolist())
assert patches[0, 0].tolist() == [0, 1, 4, 5]

patch_conv = nn.Conv2d(1, 3, 2, stride=2, bias=False)
with torch.no_grad():
    patch_conv.weight.copy_(projection.weight.reshape(3, 1, 2, 2))
    via_conv = patch_conv(image).flatten(2).transpose(1, 2)
print("Linear trùng conv:", torch.allclose(tokens, via_conv))
assert torch.allclose(tokens, via_conv)


# Ví dụ 2: Một query chọn đọc hai patch
import math
import torch

torch.set_num_threads(1)
q = torch.tensor([[1., 0.]])
k = torch.tensor([[1., 0.], [0., 1.]])
v = torch.tensor([[10.], [20.]])
scores = q @ k.T / math.sqrt(k.shape[1])
weights = scores.softmax(dim=-1)
result = weights @ v
print("Điểm đã scale:", [[round(v, 4) for v in row] for row in scores.tolist()])
print("Trọng số:", [[round(v, 4) for v in row] for row in weights.tolist()])
print("Tổng trọng số:", weights.sum(-1).tolist())
print("Thông tin sau đọc:", round(result.item(), 4))
assert torch.allclose(weights.sum(-1), torch.ones(1))
assert 10 < result.item() < 20
assert weights[0, 0] > weights[0, 1]


# Ví dụ 3: Đổi chỗ nội dung nhưng giữ nguyên vị trí
import math
import torch

torch.set_num_threads(1)
tokens = torch.tensor([[1., 0.], [0., 1.], [-1., 0.], [0., -1.]])
positions = torch.tensor([[0., 0.], [0., 0.4], [0.8, 0.], [0., -0.8]])
order = torch.tensor([2, 0, 3, 1])

def attend_mean(sequence):
    weights = (sequence @ sequence.T / math.sqrt(2)).softmax(-1)
    return (weights @ sequence).mean(0)

plain = attend_mean(tokens)
plain_shuffled = attend_mean(tokens[order])
positioned = attend_mean(tokens + positions)
content_moved = attend_mean(tokens[order] + positions)
both_moved = attend_mean((tokens + positions)[order])
print("Không position, đảo token vẫn trùng:", torch.allclose(plain, plain_shuffled, atol=1e-6))
print("Đảo cả nội dung và mã vị trí vẫn trùng:", torch.allclose(positioned, both_moved, atol=1e-6))
print("Chỉ đổi nội dung tại vị trí cố định còn trùng:",
      torch.allclose(positioned, content_moved, atol=1e-6))
print("Số ô attention, ảnh 4×4 rồi 8×8, patch 2:", 4**2, 16**2)
assert torch.allclose(plain, plain_shuffled, atol=1e-6)
assert torch.allclose(positioned, both_moved, atol=1e-6)
assert not torch.allclose(positioned, content_moved, atol=1e-6)

