# -*- coding: utf-8 -*-
# Regularization — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

rng = np.random.default_rng(1)
n, k = 100, 30
area = rng.uniform(30, 120, n)
dist = rng.uniform(1, 15, n)
junk = rng.normal(size=(n, k))                       # 30 cột không liên quan đến giá
y = 0.05 * area - 0.15 * dist + 1.0 + rng.normal(0, 0.4, n)

X = np.column_stack([area, dist, junk])              # (100, 32)
X_tr, X_te, y_tr, y_te = X[:40], X[40:], y[:40], y[40:]
mu, sigma = X_tr.mean(axis=0), X_tr.std(axis=0)
A_tr, A_te = (X_tr - mu) / sigma, (X_te - mu) / sigma
print(A_tr.shape, A_te.shape)

# Bước 2
def r2(y_hat, y):
    return 1 - np.mean((y_hat - y) ** 2) / np.var(y)

def fit_ols(A, y):
    Ab = np.column_stack([A, np.ones(len(A))])
    theta = np.linalg.lstsq(Ab, y, rcond=None)[0]
    return theta[:-1], theta[-1]

w, b = fit_ols(A_tr, y_tr)
print("R2 train:", round(r2(A_tr @ w + b, y_tr), 3), " R2 test:", round(r2(A_te @ w + b, y_te), 3))
print("2 hệ số thật:", w[:2].round(2), " |hệ số rác| lớn nhất:", np.abs(w[2:]).max().round(2))

# Bước 3
def fit_ridge(A, y, lam):
    a_mean, y_mean = A.mean(axis=0), y.mean()
    Ac, yc = A - a_mean, y - y_mean
    w = np.linalg.solve(Ac.T @ Ac + lam * np.eye(A.shape[1]), Ac.T @ yc)
    return w, y_mean - a_mean @ w

from sklearn.linear_model import Ridge
w, b = fit_ridge(A_tr, y_tr, 3.0)
model = Ridge(alpha=3.0).fit(A_tr, y_tr)
print(np.allclose(w, model.coef_), np.allclose(b, model.intercept_))

# Bước 4
for lam in [0, 0.1, 1, 3, 10, 30, 100]:
    w, b = fit_ridge(A_tr, y_tr, lam)
    print(f"lambda = {lam:>5}: R2 train = {r2(A_tr @ w + b, y_tr):.3f}   R2 test = {r2(A_te @ w + b, y_te):.3f}")

# Bước 5
def soft(z, t):
    return np.sign(z) * np.maximum(np.abs(z) - t, 0)

def fit_lasso(A, y, lam, sweeps=500):
    a_mean, y_mean = A.mean(axis=0), y.mean()
    Ac, yc = A - a_mean, y - y_mean
    w = np.zeros(A.shape[1])
    col_sq = (Ac ** 2).sum(axis=0)
    for _ in range(sweeps):
        for j in range(len(w)):
            r_j = yc - Ac @ w + Ac[:, j] * w[j]       # phần dư khi bỏ đặc trưng j
            w[j] = soft(Ac[:, j] @ r_j, lam) / col_sq[j]
    return w, y_mean - a_mean @ w

w, b = fit_lasso(A_tr, y_tr, 8.0)
print("giữ lại các cột:", np.nonzero(w)[0], " hệ số:", w[w != 0].round(3))
print("R2 test:", round(r2(A_te @ w + b, y_te), 3))

# Bước 6
from sklearn.linear_model import Lasso
model = Lasso(alpha=8.0 / 40, tol=1e-10, max_iter=100000).fit(A_tr, y_tr)
print(np.allclose(w, model.coef_, atol=1e-6), np.allclose(b, model.intercept_, atol=1e-6))

# Bước 7
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

alpha_grid = np.logspace(-3, 3, 13)
for name, estimator in [("Ridge", Ridge()), ("Lasso", Lasso(max_iter=10000))]:
    pipeline = make_pipeline(StandardScaler(), estimator)
    step_name = name.lower()
    search = GridSearchCV(pipeline, {step_name + "__alpha": alpha_grid}, cv=5)
    search.fit(X_tr, y_tr)
    alpha = search.best_params_[step_name + "__alpha"]
    coef = search.best_estimator_[-1].coef_
    print(f"{name}: alpha = {alpha:.4g}  R2 test = {search.score(X_te, y_te):.3f}  "
          f"số hệ số khác 0 = {np.count_nonzero(coef)}")
    print(f"       2 hệ số thật = {coef[:2].round(3)}  |hệ số rác| lớn nhất = {np.abs(coef[2:]).max():.3f}")

# Bước 8
B = X_tr[:, :2]                                     # diện tích (m²), khoảng cách (km)
for unit, scale in [("km", 1), ("m", 1000)]:
    M = B * np.array([1, scale])                     # khoảng cách đo bằng km hoặc bằng m
    m = Ridge(alpha=1000).fit(M, y_tr)
    print(f"khoảng cách theo {unit:>2}: hệ số quy về mỗi km = {m.coef_[1] * scale:.3f}")
