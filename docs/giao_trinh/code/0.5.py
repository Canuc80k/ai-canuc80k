# -*- coding: utf-8 -*-
# Vector và ma trận — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

a = np.array([3.0, 1.0])
b = np.array([1.0, 2.0])
print(a + b, 2 * a, a - b)

# Bước 2
p = np.array([1.0, 2.0])
q = np.array([4.0, 6.0])
d = q - p
print(d, np.linalg.norm(d), np.sqrt((d ** 2).sum()), np.abs(d).sum())

# Bước 3
w = np.array([0.1, 0.8, -0.3])          # giờ tự học, điểm HK1, số buổi vắng
x = np.array([6.0, 7.5, 1.0])           # học sinh A
print(w @ x, (w * x).sum(), w @ x + 1.0)

def cosine(u, v):
    return u @ v / (np.linalg.norm(u) * np.linalg.norm(v))

meo = np.array([0.9, 0.8, 0.1])
cho = np.array([0.8, 0.9, 0.2])
oto = np.array([0.1, 0.2, 0.9])
print(round(cosine(meo, cho), 3), round(cosine(meo, oto), 3))

# Bước 4
X = np.array([[6.0, 7.5, 1.0],
              [2.0, 6.0, 4.0],
              [10.0, 8.5, 0.0],
              [4.0, 5.5, 2.0]])
b = 1.0
print(X.shape, w.shape, (X @ w).shape)
print(X @ w + b)
print([round(float(row @ w + b), 1) for row in X])

# Bước 5
W = np.array([[0.1, -0.2],
              [0.8, 0.5],
              [-0.3, 0.4]])
H = X @ W
print(H.shape)
print(np.round(H, 2))
print(X.T.shape, W.T.shape)
try:
    W @ X
except ValueError as e:
    print("W @ X lỗi:", e)
I = np.eye(3)
print(np.allclose(X @ I, X))

# Bước 6
square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)   # mỗi hàng một đỉnh
M = np.array([[2.0, 1.0],
              [0.0, 1.0]])
print(square @ M.T)
