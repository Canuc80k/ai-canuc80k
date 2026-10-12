"""Logistic regression và softmax: lọc thư rác và nhận dạng chữ số viết tay.

Code đi kèm bài 2.3, chạy từ đầu đến cuối theo đúng thứ tự các phần trong bài.
Cần: numpy, scikit-learn. Chạy: python 2.3.py
"""
import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import log_loss


# ---------- Dữ liệu ----------

def make_spam(seed=20, n=400, n_train=300):
    """Mỗi email: (số link, số từ quảng cáo). Nhãn sinh từ log-odds = 1.1·links + 0.9·kw − 4.5."""
    rng = np.random.default_rng(seed)
    links = rng.poisson(2.0, n)
    kw = rng.poisson(1.5, n)
    z_true = 1.1 * links + 0.9 * kw - 4.5
    y = (rng.random(n) < 1 / (1 + np.exp(-z_true))).astype(float)
    X = np.column_stack([links, kw]).astype(float)
    return X[:n_train], X[n_train:], y[:n_train], y[n_train:]


# ---------- Logistic regression tự cài ----------

def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def loss(theta, X, y, eps=1e-12):
    """Binary cross-entropy; theta = (w_1, ..., w_d, b)."""
    p = np.clip(sigmoid(X @ theta[:-1] + theta[-1]), eps, 1 - eps)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


def grad(theta, X, y):
    r = sigmoid(X @ theta[:-1] + theta[-1]) - y          # p − y, shape (n,)
    return np.append(X.T @ r / len(y), r.mean())


def gd(X, y, lr, epochs):
    theta = np.zeros(X.shape[1] + 1)
    history = []
    for _ in range(epochs):
        history.append(loss(theta, X, y))
        theta -= lr * grad(theta, X, y)
    return theta, history


def numerical_grad(f, theta, h=1e-5):
    g = np.zeros_like(theta)
    for j in range(len(theta)):
        e = np.zeros_like(theta)
        e[j] = h
        g[j] = (f(theta + e) - f(theta - e)) / (2 * h)
    return g


def rel_error(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))


# ---------- Softmax ----------

def softmax(Z):
    Z = Z - Z.max(axis=-1, keepdims=True)                # trừ max: không đổi kết quả, không tràn số
    E = np.exp(Z)
    return E / E.sum(axis=-1, keepdims=True)


def fit_softmax(X, t, K, C=1.0, lr=2.0, epochs=5000):
    """Softmax regression với phạt L2 giống LogisticRegression(C=C) của scikit-learn."""
    n = len(t)
    Y = np.eye(K)[t]                                     # one-hot, (n, K)
    lam = 1 / (C * n)
    W, b = np.zeros((X.shape[1], K)), np.zeros(K)
    for _ in range(epochs):
        G = (softmax(X @ W + b) - Y) / n                 # p − one-hot, (n, K)
        W -= lr * (X.T @ G + lam * W)
        b -= lr * G.sum(axis=0)
    return W, b


def main():
    X_tr, X_te, y_tr, y_te = make_spam()
    print("== Dữ liệu spam ==")
    print(f"train {X_tr.shape}, test {X_te.shape}, tỉ lệ spam train = {y_tr.mean():.3f}")

    print("\n== Linear regression trên nhãn 0/1 ==")
    p_lin = LinearRegression().fit(X_tr, y_tr).predict(X_tr)
    print(f"dự đoán từ {p_lin.min():.2f} đến {p_lin.max():.2f}; {np.sum((p_lin < 0) | (p_lin > 1))} email ngoài [0, 1]")

    L_tr = X_tr[:, :1]
    extra = np.repeat(np.arange(15, 25), 2)[:, None]     # 20 email siêu spam
    L_more, y_more = np.vstack([L_tr, extra]), np.append(y_tr, np.ones(20))
    acc_at = lambda t: np.mean((X_te[:, 0] >= t) == y_te)
    for name, L, yy in [("300 email gốc    ", L_tr, y_tr), ("thêm 20 siêu spam", L_more, y_more)]:
        lin = LinearRegression().fit(L, yy)
        t_lin = (0.5 - lin.intercept_) / lin.coef_[0]
        lg = LogisticRegression(C=np.inf).fit(L, yy)
        t_log = -lg.intercept_[0] / lg.coef_[0, 0]
        print(f"{name}: ngưỡng linear = {t_lin:.2f} (acc {acc_at(t_lin):.2f})   "
              f"ngưỡng logistic = {t_log:.2f} (acc {acc_at(t_log):.2f})")

    print("\n== Kiểm tra gradient ==")
    theta0 = np.random.default_rng(1).normal(size=3)
    num = numerical_grad(lambda t: loss(t, X_tr, y_tr), theta0)
    print(f"sai số tương đối = {rel_error(grad(theta0, X_tr, y_tr), num):.1e}")

    print("\n== Gradient descent ==")
    theta, history = gd(X_tr, y_tr, 0.5, 5000)
    print(f"w = {theta[:2].round(3)}   b = {theta[2]:.3f}   (quy luật thật: 1.1, 0.9, −4.5)")
    print(f"loss ban đầu = {history[0]:.4f} (= log 2)   sau 5000 vòng = {history[-1]:.4f}")
    model = LogisticRegression(C=np.inf).fit(X_tr, y_tr)
    same = np.allclose(theta, np.append(model.coef_[0], model.intercept_), atol=1e-3)
    print(f"scikit-learn: w = {model.coef_[0].round(3)}   b = {model.intercept_[0]:.3f}   trùng: {same}")

    print("\n== Đọc hệ số qua odds ==")
    print(f"thêm 1 link: odds × {np.exp(model.coef_[0, 0]):.2f}   thêm 1 từ quảng cáo: odds × {np.exp(model.coef_[0, 1]):.2f}")
    emails = np.array([[1, 1], [2, 1], [7, 1], [8, 1]])
    print("P(spam) cho (1,1), (2,1), (7,1), (8,1):", model.predict_proba(emails)[:, 1].round(3))

    print("\n== Ngưỡng quyết định trên 100 email test ==")
    p_te = model.predict_proba(X_te)[:, 1]
    for t in [0.3, 0.5, 0.9]:
        block = p_te >= t
        print(f"ngưỡng {t}: chặn đúng {np.sum(block & (y_te == 1)):>2} spam, "
              f"chặn nhầm {np.sum(block & (y_te == 0)):>2} thư thật, lọt {np.sum(~block & (y_te == 1)):>2} spam")
    print(f"accuracy = {model.score(X_te, y_te):.2f}   mốc luôn đoán 'không spam' = {np.mean(y_te == 0):.2f}")
    base = np.full(len(y_te), y_tr.mean())
    print(f"log loss: mốc = {log_loss(y_te, base):.3f}   mô hình = {log_loss(y_te, p_te):.3f}   "
          f"nộp nhãn thay xác suất = {log_loss(y_te, model.predict(X_te)):.3f}")

    print("\n== Softmax không tràn số ==")
    z = np.array([2.0, 1.0, 0.0])
    print("softmax(2, 1, 0) =", softmax(z).round(3), "  cộng 1000 vào mọi logit:", softmax(z + 1000).round(3))

    print("\n== Softmax regression trên chữ số viết tay ==")
    D, t = load_digits(return_X_y=True)
    D = D / 16
    idx = np.random.default_rng(0).permutation(len(t))
    D, t = D[idx], t[idx]
    D_tr, D_te, t_tr, t_te = D[:1300], D[1300:], t[:1300], t[1300:]
    W, b = fit_softmax(D_tr, t_tr, K=10)
    pred = np.argmax(D_te @ W + b, axis=1)
    sk = LogisticRegression(C=1.0, max_iter=1000).fit(D_tr, t_tr)
    print(f"tự cài: accuracy = {np.mean(pred == t_te):.3f}   scikit-learn: accuracy = {sk.score(D_te, t_te):.3f}")
    print(f"nhãn trùng: {np.mean(sk.predict(D_te) == pred):.3f}   "
          f"xác suất lệch lớn nhất: {np.abs(sk.predict_proba(D_te) - softmax(D_te @ W + b)).max():.3f}")


if __name__ == "__main__":
    main()
