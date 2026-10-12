# -*- coding: utf-8 -*-
# NumPy — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int64)
print(a.shape, a.ndim, a.size, a.dtype)
print(np.zeros((2, 3)).dtype, np.arange(6).reshape(2, 3).tolist())
print(np.linspace(0, 1, 5))
print(np.arange(12).reshape(3, -1).shape)    # -1: NumPy tự tính trục còn lại

# Bước 2
big = np.array([2**62], dtype=np.int64)
print(big * 4, big.dtype)

pixels = np.array([200, 100], dtype=np.uint8)   # ảnh thường lưu bằng uint8, giá trị 0..255
print(pixels + 100)

x = np.array([1, 2, 3])
x[0] = 2.7                                       # gán số thực vào mảng nguyên: bị cắt
print(x)

# Bước 3
z = np.array([-2.0, 0.0, 1.0, 3.0])
print(1 / (1 + np.exp(-z)))                      # sigmoid của bài 2.3, cho cả mảng
print(z > 0, (z > 0).sum(), (z > 0).mean())
print(np.where(z > 0, z, 0.0))                   # ReLU: giữ số dương, số âm thành 0
print(np.clip(z, -1, 1), z.max(), z.argmax())

# Bước 4
import math
from timeit import repeat

rng = np.random.default_rng(0)
z = rng.normal(size=200_000)
zs = z.tolist()

def sigmoid_loop(values):
    return [1 / (1 + math.exp(-value)) for value in values]

def sigmoid_numpy(values):
    return 1 / (1 + np.exp(-values))

p_loop = sigmoid_loop(zs)
p_vec = sigmoid_numpy(z)
assert np.allclose(p_loop, p_vec)
t_loop = min(repeat(lambda: sigmoid_loop(zs), repeat=5, number=3)) / 3
t_vec = min(repeat(lambda: sigmoid_numpy(z), repeat=5, number=3)) / 3
print(np.allclose(p_loop, p_vec), p_vec.shape)
print("NumPy nhanh hơn vòng lặp:", t_vec < t_loop)

# Bước 5
a = np.arange(12).reshape(3, 4)
print(a)
print(a[1, 2], a[:, 0], a[-1, ::2])
print(a[[0, 2]].shape, a[a % 5 == 0])

# Bước 6
a = np.arange(6)
s = a[1:4]                  # view
s[0] = 100
print(a)

f = a[[1, 2, 3]]            # fancy indexing: luôn là bản sao
f[0] = -1
print(a, np.shares_memory(a, s), np.shares_memory(a, f))

# Bước 7
scores = np.array([[9, 8, 7],
                   [5, 6, 4],
                   [4, 4, 5],
                   [9, 8, 10],
                   [7, 8, 10]], dtype=float)       # (5 học sinh, 3 môn)
print(scores.mean(axis=0))                         # trung bình từng môn
print(scores.mean(axis=1).round(2))                # trung bình từng học sinh
print(scores.argmax(axis=1), scores.max())

# Bước 8
imgs = rng.random((100, 28, 28))
print(imgs.mean(axis=0).shape)                     # ảnh trung bình
print(imgs.mean(axis=(1, 2)).shape)                # độ sáng trung bình của từng ảnh
print(imgs.mean(axis=(1, 2), keepdims=True).shape)

# Bước 9
joined = np.concatenate([scores[:2], scores[2:]], axis=0)
two_sessions = np.stack([scores, scores], axis=0)
print(joined.shape, np.array_equal(joined, scores))
print(two_sessions.shape)    # (buổi, học sinh, môn)

# Bước 10
mu = scores.mean(axis=0)
sigma = scores.std(axis=0)
sigma_safe = np.where(sigma == 0, 1.0, sigma)
Z = (scores - mu) / sigma_safe
print(Z.shape, Z.mean(axis=0).round(6), Z.std(axis=0))

# Bước 11
row_mean = scores.mean(axis=1)
try:
    scores - row_mean
except ValueError as e:
    print("ValueError:", e)
print((scores - scores.mean(axis=1, keepdims=True)).shape)

# Bước 12
A = np.array([[0.0, 0.0], [3.0, 4.0]])
B = np.array([[0.0, 4.0], [3.0, 0.0]])
diff = A[:, None, :] - B[None, :, :]  # (2, 1, 2) - (1, 2, 2) -> (2, 2, 2)
D = np.sqrt((diff ** 2).sum(axis=-1))
print(diff.shape, D.shape)
print(D)
print(diff.nbytes)

# Bước 13
y = np.array([1.0, 2.0, 3.0])                      # (3,): nhãn thật
y_hat = np.array([[1.0], [2.0], [3.0]])            # (3, 1): dự đoán, đúng hoàn toàn
print((y_hat - y).shape)
print("MSE sai:", np.mean((y_hat - y) ** 2), "  MSE đúng:", np.mean((y_hat.ravel() - y) ** 2))

# Bước 14
def mse(y_hat, y):
    assert y_hat.shape == y.shape, (y_hat.shape, y.shape)
    return np.mean((y_hat - y) ** 2)

try:
    mse(y_hat, y)
except AssertionError as e:
    print("AssertionError:", e)

# Bước 15
M = np.array([[2.0, 1.0], [1.0, 3.0]])
v = np.array([1.0, 2.0])
print(M @ v, M * v)
print(M.T @ M)
print(np.linalg.solve(M, v), np.linalg.norm(v))

# Bước 16
rng = np.random.default_rng(42)
print(rng.integers(0, 10, size=5), rng.normal(size=2).round(3))
print(rng.permutation(5), rng.choice(["A", "B", "C"], size=4))
rng2 = np.random.default_rng(42)
print(rng2.integers(0, 10, size=5))                # cùng seed: cùng dãy số
