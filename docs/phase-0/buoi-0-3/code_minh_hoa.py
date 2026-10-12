# -*- coding: utf-8 -*-
import numpy as np

# Ba mẫu, mỗi mẫu là ma trận 4 hàng, 5 cột.
x = np.arange(1, 61, dtype=float).reshape(3, 4, 5)
print("shape:", x.shape)
print("Hàng cuối của mẫu đầu:", x[0, -1])
# Giữ chiều để broadcasting trừ đúng mean của từng mẫu.
mean = x.mean(axis=(1, 2), keepdims=True)
std = x.std(axis=(1, 2), keepdims=True)
z = (x - mean) / std
print("Mean từng mẫu:", mean.ravel())
print("Mean sau chuẩn hóa:", z.mean(axis=(1, 2)).round(6))
print("Std sau chuẩn hóa:", z.std(axis=(1, 2)).round(6))
assert z.shape == x.shape
assert np.allclose(z.mean(axis=(1, 2)), 0)
