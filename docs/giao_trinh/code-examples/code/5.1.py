# -*- coding: utf-8 -*-
# Code mẫu — Convolution và pooling

# Ví dụ 1: Một bộ lọc đọc bốn cửa sổ trên ảnh 3×3
import numpy as np
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
image = np.array([[1, 2, 0], [0, 1, 3], [2, 1, 0]], dtype=np.float32)
kernel = np.array([[1, 0], [0, 2]], dtype=np.float32)
manual = np.empty((2, 2), dtype=np.float32)
for row in range(2):
    for col in range(2):
        window = image[row:row + 2, col:col + 2]
        manual[row, col] = (window * kernel).sum()

# Hai trục đầu là batch và kênh, không phải kích thước cửa sổ.
x = torch.from_numpy(image)[None, None]
weight = torch.from_numpy(kernel)[None, None]
actual = F.conv2d(x, weight)
assert np.array_equal(manual, np.array([[3, 8], [2, 1]]))
assert np.array_equal(manual, actual[0, 0].numpy())
print("Tính tay:", manual.astype(int).tolist())
print("PyTorch:", actual[0, 0].int().tolist())
print("Shape:", tuple(actual.shape))


# Ví dụ 2: Thêm viền số 0, rồi bước cách hai ô
import numpy as np
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
image = np.arange(1, 10, dtype=np.float32).reshape(3, 3)
padding, stride, size = 1, 2, 3
padded = np.pad(image, padding)
out_size = (image.shape[0] + 2 * padding - size) // stride + 1
manual = np.zeros((out_size, out_size), dtype=np.float32)
for row in range(out_size):
    for col in range(out_size):
        top, left = row * stride, col * stride
        manual[row, col] = padded[top:top + size, left:left + size].sum()
y = F.conv2d(torch.from_numpy(image)[None, None],
             torch.ones(1, 1, size, size), padding=padding, stride=stride)
assert np.array_equal(manual, np.array([[12, 16], [24, 28]]))
assert np.array_equal(y[0, 0].numpy(), manual)
print("Ảnh:", image.astype(int).tolist())
print("Padding 1, stride 2:", y[0, 0].int().tolist())
print("Chiều đầu ra:", out_size)


# Ví dụ 3: Một điểm sáng dịch qua ranh giới pooling
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
signals = torch.tensor([[[[0., 4., 0., 0.]]],
                        [[[0., 0., 4., 0.]]]])
maximum = F.max_pool2d(signals, kernel_size=(1, 2))
average = F.avg_pool2d(signals, kernel_size=(1, 2))
print("Max:", maximum[:, 0, 0].tolist())
print("Average:", average[:, 0, 0].tolist())

# jump là khoảng cách trên ảnh gốc giữa hai ô kề nhau ở đầu ra.
field, jump = 1, 1
for name, kernel_size, stride in [("conv", 3, 1), ("pool", 2, 2), ("conv", 3, 1)]:
    field += (kernel_size - 1) * jump
    jump *= stride
    print(name, "vùng nhìn/jump:", field, jump)
assert maximum[0, 0, 0].tolist() == [4.0, 0.0]
assert maximum[1, 0, 0].tolist() == [0.0, 4.0]
assert (field, jump) == (8, 2)

