# -*- coding: utf-8 -*-
# Đạo hàm và gradient — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

def f(x):
    return x ** 2

for h in [1, 0.1, 0.01, 0.001]:
    print(h, round((f(3 + h) - f(3)) / h, 6))

# Bước 2
def numeric(g, x, h=1e-6):
    return (g(x + h) - g(x - h)) / (2 * h)

x = 2.0
tests = [("x^3", lambda t: t ** 3, 3 * x ** 2),
         ("e^x", np.exp, np.exp(x)),
         ("log x", np.log, 1 / x),
         ("3x^2 - 4x + 1", lambda t: 3 * t ** 2 - 4 * t + 1, 6 * x - 4)]
for name, g, exact in tests:
    print(f"{name:14s} công thức {exact:.6f}  sai phân {numeric(g, x):.6f}")

# Bước 3
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

for z in [0.0, 2.0, 5.0]:
    s = sigmoid(z)
    print(z, round(s * (1 - s), 4), round(numeric(sigmoid, z), 4))

w, x, y = 1.0, 2.0, 6.0
loss = lambda w: (w * x - y) ** 2
print(2 * (w * x - y) * x, round(numeric(loss, w), 4))

# Bước 4
def bowl(v):
    return v[0] ** 2 + v[1] ** 2

def grad_numeric(g, v, h=1e-6):
    out = np.zeros_like(v)
    for i in range(len(v)):
        e = np.zeros_like(v)
        e[i] = h
        out[i] = (g(v + e) - g(v - e)) / (2 * h)
    return out

v = np.array([1.0, 2.0])
print(2 * v, np.round(grad_numeric(bowl, v), 6))

# Bước 5
def descend(eta, steps, w=0.0):
    path = []
    for _ in range(steps):
        grad = 2 * (w * x - y) * x
        w = w - eta * grad
        path.append(round(w, 4))
    return path

print(descend(0.05, 6))
print(descend(0.05, 30)[-1])
print(descend(0.3, 6))

# Bước 6
xs = np.array([1.0, 2.0])
ys = np.array([2.0, 5.0])
w = 0.0
for step in range(3):
    err = w * xs - ys
    grad = np.mean(2 * err * xs)
    print(step, round(w, 4), round(np.mean(err ** 2), 4), round(grad, 4))
    w -= 0.1 * grad

# Bước 7
rng = np.random.default_rng(0)
X = rng.normal(size=(5, 3))
y_vec = rng.normal(size=5)
w_vec = rng.normal(size=3)

def mse(w):
    return np.mean((X @ w - y_vec) ** 2)

exact = 2 / len(y_vec) * X.T @ (X @ w_vec - y_vec)
approx = grad_numeric(mse, w_vec)
wrong = 1 / len(y_vec) * X.T @ (X @ w_vec - y_vec)     # quên số 2
rel = lambda a, b: np.linalg.norm(a - b) / np.linalg.norm(a + b)
print(np.round(exact, 6))
print(np.round(approx, 6))
print(f"đúng: {rel(exact, approx):.1e}   quên số 2: {rel(wrong, approx):.1e}")
