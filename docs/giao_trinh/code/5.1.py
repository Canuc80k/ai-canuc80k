# -*- coding: utf-8 -*-
# Convolution và pooling — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

image = np.array([[1, 2, 0],
                  [0, 1, 3],
                  [2, 1, 0]], dtype=float)
kernel = np.array([[1, 0],
                   [0, 2]], dtype=float)

def correlate_valid(image, kernel):
    height, width = image.shape
    kh, kw = kernel.shape
    result = np.zeros((height - kh + 1, width - kw + 1))
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            window = image[row:row + kh, col:col + kw]
            result[row, col] = np.sum(window * kernel)
    return result

feature_map = correlate_valid(image, kernel)
print(feature_map)

# Bước 2
def output_size(size, kernel_size, padding=0, stride=1, dilation=1):
    covered = dilation * (kernel_size - 1) + 1
    return (size + 2 * padding - covered) // stride + 1

print(output_size(7, 3, padding=1, stride=2))
print(output_size(7, 3, dilation=2))

# Bước 3
import torch
from torch import nn

torch.set_num_threads(1)
x = torch.tensor(image, dtype=torch.float32)[None, None]
layer = nn.Conv2d(1, 1, kernel_size=2, bias=False)
with torch.no_grad():
    layer.weight.copy_(torch.tensor(kernel, dtype=torch.float32)[None, None])
    y = layer(x)
print(tuple(y.shape))
print(np.allclose(y[0, 0].numpy(), feature_map))

rgb_layer = nn.Conv2d(3, 8, 3, padding=1)
print(sum(parameter.numel() for parameter in rgb_layer.parameters()))
print(tuple(rgb_layer(torch.zeros(2, 3, 7, 7)).shape))

# Bước 4
print(nn.MaxPool2d(2)(y).flatten().tolist())
print(nn.AvgPool2d(2)(y).flatten().tolist())
left = torch.tensor([[[[0., 4., 0., 0.]]]])
right = torch.tensor([[[[0., 0., 4., 0.]]]])
pool = nn.MaxPool2d((1, 2))
print(pool(left).flatten().tolist())
print(pool(right).flatten().tolist())

window = y.detach().clone().requires_grad_(True)
nn.MaxPool2d(2)(window).sum().backward()
print(window.grad[0, 0].tolist())
