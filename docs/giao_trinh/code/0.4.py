# -*- coding: utf-8 -*-
# Hàm số, mũ và log — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

def to_f(c):
    return 1.8 * c + 32

c = np.array([-10, 0, 10, 20, 30])
f = to_f(c)
print(f)
print(np.diff(f) / np.diff(c))

# Bước 2
x = np.array([-5, -1, 0, 1, 2, 5, 10])
print([round(float(v), 4) for v in np.exp(x)])
print(np.exp(2 + 3), np.exp(2) * np.exp(3))

# Bước 3
with np.errstate(over="ignore"):
    print(np.exp(np.array([700.0, 710.0])))

# Bước 4
print(np.log2(8), np.log10(1000), np.log(np.e))
print(np.log(3 * 7), np.log(3) + np.log(7))
p = np.full(1100, 0.5)
print(np.prod(p[:1000]), np.prod(p))
print(np.sum(np.log(p[:1000])), np.sum(np.log(p)))

# Bước 5
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

z = np.array([-6, -2, 0, 2, 6])
print(np.round(sigmoid(z), 4))
print(np.round(sigmoid(z) + sigmoid(-z), 4))
logit = np.log(0.8 / 0.2)
print(round(logit, 4), sigmoid(logit))

# Bước 6
def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()

z = np.array([2.0, 1.0, 0.0])
print(np.round(softmax(z), 4), round(softmax(z).sum(), 6))
print(np.round(softmax(z + 100), 4))
big = np.array([1000.0, 999.0, 998.0])
print(np.round(softmax(big), 4))
with np.errstate(over="ignore", invalid="ignore"):
    print(np.exp(big) / np.exp(big).sum())

# Bước 7
p_true = np.array([0.99, 0.9, 0.5, 0.1, 0.01])
print(np.round(-np.log(p_true), 3))

# Bước 8
A = np.array([0.9, 0.8, 0.6, 0.4])    # xác suất model A dành cho đáp án đúng
B = np.array([0.6, 0.6, 0.6, 0.05])
for name, p in [("A", A), ("B", B)]:
    print(name, "accuracy", (p > 0.5).mean(), "log-loss", round(-np.log(p).mean(), 3))

# Bước 9
z = np.array([2.0, 1.0, 0.0])
p = softmax(z)
print(np.round(p, 3), np.round(-np.log(p), 3))
z2 = np.array([2.0, 2.0, 0.0])
print(np.round(softmax(z2), 3), round(-np.log(softmax(z2)[1]), 3))
