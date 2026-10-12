# -*- coding: utf-8 -*-
# Logistic regression và softmax — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

rng = np.random.default_rng(20)
n = 400
links = rng.poisson(2.0, n)                           # số đường link
kw = rng.poisson(1.5, n)                              # số từ quảng cáo
z_true = 1.1 * links + 0.9 * kw - 4.5                 # quy luật thật, mô hình không được biết
y = (rng.random(n) < 1 / (1 + np.exp(-z_true))).astype(float)   # 1 = spam

X = np.column_stack([links, kw]).astype(float)        # (400, 2)
X_tr, X_te, y_tr, y_te = X[:300], X[300:], y[:300], y[300:]
print(X_tr.shape, X_te.shape, " tỉ lệ spam:", y.mean())
print(X[:4], y[:4])

# Bước 2
from sklearn.linear_model import LinearRegression

lin = LinearRegression().fit(X_tr, y_tr)
p_lin = lin.predict(X_tr)
print("dự đoán nhỏ nhất:", p_lin.min().round(2), " lớn nhất:", p_lin.max().round(2))
print("số email có 'xác suất' ngoài [0, 1]:", np.sum((p_lin < 0) | (p_lin > 1)))

# Bước 3
def link_threshold(model):
    """Số link tại đó đường thẳng cắt mức 0.5."""
    return (0.5 - model.intercept_) / model.coef_[0]

def accuracy_at(t):
    """Accuracy trên tập test khi coi email có từ t link trở lên là spam."""
    return np.mean((X_te[:, 0] >= t) == y_te)

L_tr = X_tr[:, :1]                                    # chỉ số link, shape (300, 1)
extra = np.repeat(np.arange(15, 25), 2)[:, None]      # 20 email siêu spam
L_more, y_more = np.vstack([L_tr, extra]), np.append(y_tr, np.ones(20))

for name, L, yy in [("300 email gốc    ", L_tr, y_tr), ("thêm 20 siêu spam", L_more, y_more)]:
    t = link_threshold(LinearRegression().fit(L, yy))
    print(f"{name}: ngưỡng = {t:.2f} link   accuracy test = {accuracy_at(t):.2f}")

# Bước 4
from sklearn.linear_model import LogisticRegression

for name, L, yy in [("300 email gốc    ", L_tr, y_tr), ("thêm 20 siêu spam", L_more, y_more)]:
    m = LogisticRegression(C=np.inf).fit(L, yy)
    t = -m.intercept_[0] / m.coef_[0, 0]
    print(f"{name}: ngưỡng = {t:.2f} link   accuracy test = {accuracy_at(t):.2f}")

# Bước 5
def sigmoid(z):
    # sigmoid(z) = exp(-log(1 + exp(-z))), tính ổn định
    return np.exp(-np.logaddexp(0., -z))

def loss(theta, X, y):
    logits = X @ theta[:-1] + theta[-1]
    # cross-entropy tính thẳng từ logits: không tràn số, không cần kẹp
    return np.mean(np.logaddexp(0., logits) - y * logits)

def grad(theta, X, y):
    r = sigmoid(X @ theta[:-1] + theta[-1]) - y       # p − y, shape (n,)
    return np.append(X.T @ r / len(y), r.mean())

# Bước 6
def numerical_grad(f, theta, h=1e-5):
    g = np.zeros_like(theta)
    for j in range(len(theta)):
        e = np.zeros_like(theta)
        e[j] = h
        g[j] = (f(theta + e) - f(theta - e)) / (2 * h)
    return g

def rel_error(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))

theta0 = np.random.default_rng(1).normal(size=3)
num = numerical_grad(lambda t: loss(t, X_tr, y_tr), theta0)
print(f"sai số tương đối: {rel_error(grad(theta0, X_tr, y_tr), num):.1e}")

# Bước 7
theta = np.zeros(3)
history = []
for epoch in range(5000):
    history.append(loss(theta, X_tr, y_tr))
    theta -= 0.5 * grad(theta, X_tr, y_tr)

print("w =", theta[:2].round(3), "  b =", theta[2].round(3))
print("loss ban đầu:", round(history[0], 4), "  sau 5000 vòng:", round(history[-1], 4))

# Bước 8
model = LogisticRegression(C=np.inf).fit(X_tr, y_tr)
print("scikit-learn: w =", model.coef_[0].round(3), "  b =", model.intercept_.round(3))
print("trùng gradient descent:", np.allclose(theta, np.append(model.coef_[0], model.intercept_), atol=1e-3))

# Bước 9
w = model.coef_[0]
print("thêm 1 link: odds nhân", np.exp(w[0]).round(2), "  thêm 1 từ quảng cáo: odds nhân", np.exp(w[1]).round(2))

emails = np.array([[1, 1], [2, 1], [7, 1], [8, 1]])     # (số link, số từ quảng cáo)
print("P(spam):", model.predict_proba(emails)[:, 1].round(3))

# Bước 10
p_te = model.predict_proba(X_te)[:, 1]
print("predict trùng p > 0.5:", np.array_equal(model.predict(X_te), (p_te > 0.5).astype(float)))
for t in [0.3, 0.5, 0.9]:
    block = p_te >= t
    print(f"ngưỡng {t}: chặn đúng {np.sum(block & (y_te == 1)):>2} spam, "
          f"chặn nhầm {np.sum(block & (y_te == 0)):>2} thư thật, lọt {np.sum(~block & (y_te == 1)):>2} spam")
print("accuracy:", model.score(X_te, y_te), "  luôn đoán 'không spam':", np.mean(y_te == 0))

# Bước 11
from sklearn.metrics import log_loss

base = np.full(len(y_te), y_tr.mean())
print("log loss mốc:", round(log_loss(y_te, base), 3), "  mô hình:", round(log_loss(y_te, p_te), 3))

# Bước 12
def softmax_naive(z):
    e = np.exp(z)
    return e / e.sum()

def softmax(Z):
    Z = Z - Z.max(axis=-1, keepdims=True)             # trừ max từng hàng, kết quả không đổi
    E = np.exp(Z)
    return E / E.sum(axis=-1, keepdims=True)

z = np.array([2.0, 1.0, 0.0])
print(softmax(z).round(3))
print(softmax_naive(z + 1000), softmax(z + 1000).round(3))

# Bước 13
from sklearn.datasets import load_digits

D, t = load_digits(return_X_y=True)
D = D / 16                                            # điểm ảnh về [0, 1]
idx = np.random.default_rng(0).permutation(len(t))
D, t = D[idx], t[idx]
D_tr, D_te, t_tr, t_te = D[:1300], D[1300:], t[:1300], t[1300:]
print(D_tr.shape, D_te.shape)

# Bước 14
n, K = len(t_tr), 10
Y = np.eye(K)[t_tr]                                   # one-hot, (1300, 10)
lam = 1 / (1.0 * n)                                   # khớp C = 1
W, b = np.zeros((D_tr.shape[1], K)), np.zeros(K)
for epoch in range(5000):
    G = (softmax(D_tr @ W + b) - Y) / n               # (1300, 10)
    W -= 2.0 * (D_tr.T @ G + lam * W)
    b -= 2.0 * G.sum(axis=0)

pred = np.argmax(D_te @ W + b, axis=1)
print("tự cài:       accuracy test =", round(np.mean(pred == t_te), 3))

sk = LogisticRegression(C=1.0, max_iter=1000).fit(D_tr, t_tr)
print("scikit-learn: accuracy test =", round(sk.score(D_te, t_te), 3))
print("nhãn trùng nhau:", np.mean(sk.predict(D_te) == pred),
      "  xác suất lệch lớn nhất:", np.abs(sk.predict_proba(D_te) - softmax(D_te @ W + b)).max().round(3))

# Bước 15
p = np.array([1.0, 0.0])
yy = np.array([0.0, 0.0])
print(-np.mean(yy * np.log(p) + (1 - yy) * np.log(1 - p)))
print(-np.mean(yy * np.log(np.clip(p, 1e-12, 1 - 1e-12)) + (1 - yy) * np.log(1 - np.clip(p, 1e-12, 1 - 1e-12))))

# Bước 16
print("nộp xác suất:", round(log_loss(y_te, p_te), 3), "  nộp nhãn:", round(log_loss(y_te, model.predict(X_te)), 3))
