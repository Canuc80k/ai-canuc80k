# -*- coding: utf-8 -*-
# Linear regression — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

rng = np.random.default_rng(0)
n = 200
area = rng.uniform(30, 120, n)                                # diện tích, m²
dist = rng.uniform(1, 15, n)                                  # khoảng cách đến trung tâm, km
y = 0.05 * area - 0.15 * dist + 1.0 + rng.normal(0, 0.3, n)   # giá, tỷ đồng

X = np.column_stack([area, dist])
print(X.shape, y.shape)
print(X[:3].round(1))
print(y[:3].round(2))

# Bước 2
def predict(X, w, b):
    return X @ w + b

def mse(y_hat, y):
    return np.mean((y_hat - y) ** 2)

print(mse(np.full(n, y.mean()), y))   # đoán mọi căn đều có giá trung bình
print(y.var())

# Bước 3
Xb = np.column_stack([X, np.ones(n)])            # thêm cột 1, shape (200, 3)
theta = np.linalg.solve(Xb.T @ Xb, Xb.T @ y)     # giải hệ phương trình chuẩn
w_cf, b_cf = theta[:2], theta[2]
print(w_cf.round(4), round(b_cf, 4))
print(mse(predict(X, w_cf, b_cf), y))
print(predict(np.array([70, 8]), w_cf, b_cf))    # căn hộ ở đầu bài

# Bước 4
def loss(theta, X, y):                   # theta = (w_1, ..., w_d, b)
    return mse(predict(X, theta[:-1], theta[-1]), y)

def grad(theta, X, y):
    weights = theta[:-1]
    bias = theta[-1]
    residual = predict(X, weights, bias) - y  # (n,)
    grad_weights = 2 * (X.T @ residual) / len(y)  # (d,)
    grad_bias = 2 * residual.mean()               # một số
    return np.append(grad_weights, grad_bias)

def gd(X, y, lr, epochs):
    theta = np.zeros(X.shape[1] + 1)
    history = []
    for _ in range(epochs):
        history.append(loss(theta, X, y))
        theta -= lr * grad(theta, X, y)
    return theta, history

# Bước 5
def numerical_grad(f, theta, h=1e-5):
    g = np.zeros_like(theta)
    for j in range(len(theta)):
        e = np.zeros_like(theta)
        e[j] = h
        g[j] = (f(theta + e) - f(theta - e)) / (2 * h)
    return g

def rel_error(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))

theta0 = rng.normal(size=3)                    # một điểm bất kỳ
f = lambda t: loss(t, X, y)
print(rel_error(grad(theta0, X, y), numerical_grad(f, theta0)))

def grad_buggy(theta, X, y):                   # quên hệ số 2
    r = predict(X, theta[:-1], theta[-1]) - y
    return np.append(1 / len(y) * X.T @ r, r.mean())

print(rel_error(grad_buggy(theta0, X, y), numerical_grad(f, theta0)))

# Bước 6
for lr in [1e-3, 2e-4, 1e-4]:
    theta_gd, hist = gd(X, y, lr, 1000)
    print(f"lr = {lr:g}: loss sau 1000 vòng = {hist[-1]:.4g}")
print(theta_gd.round(3))                      # lr = 1e-4

# Bước 7
H = 2 / n * Xb.T @ Xb
eig = np.linalg.eigvalsh(H)          # trị riêng, xếp tăng dần
print(2 / eig[-1])                    # learning rate lớn nhất còn hội tụ
print(eig[-1] / eig[0])               # số điều kiện

# Bước 8
mu, sigma = X.mean(axis=0), X.std(axis=0)
Xs = (X - mu) / sigma
Xsb = np.column_stack([Xs, np.ones(n)])
eig_s = np.linalg.eigvalsh(2 / n * Xsb.T @ Xsb)
print(2 / eig_s[-1], eig_s[-1] / eig_s[0])

for lr in [0.01, 0.1, 0.5, 1.0]:
    theta_s, hist = gd(Xs, y, lr, 100)
    print(f"lr = {lr:g}: loss sau 100 vòng = {hist[-1]:.4g}")

# Bước 9
theta_s, _ = gd(Xs, y, 0.1, 200)
w_gd = theta_s[:2] / sigma
b_gd = theta_s[2] - np.sum(theta_s[:2] * mu / sigma)
print(w_gd.round(4), round(b_gd, 4))

# Bước 10
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
model = LinearRegression().fit(X_tr, y_tr)
print(model.coef_.round(4), round(model.intercept_, 4))
print(model.score(X_tr, y_tr), model.score(X_te, y_te))

# Bước 11
full = LinearRegression().fit(X, y)
print(np.allclose(full.coef_, w_cf), np.allclose(full.intercept_, b_cf))
print(np.allclose(w_gd, w_cf), np.allclose(b_gd, b_cf))

# Bước 12
ns = np.array([1e3, 2e3, 5e3, 1e4, 2e4, 5e4])
t = np.array([0.0011, 0.0042, 0.026, 0.098, 0.41, 2.47])    # giây, đo trên máy nhà
k, c = np.polyfit(np.log(ns), np.log(t), 1)                  # least squares bậc 1
print(round(k, 2))
print(np.exp(c) * 2e5 ** k)                                  # dự đoán cho n = 2·10⁵
