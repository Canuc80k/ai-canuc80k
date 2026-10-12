"""Regularization: Ridge và Lasso trên dữ liệu căn hộ có 30 cột rác.

Code đi kèm bài 2.2, chạy từ đầu đến cuối theo đúng thứ tự các phần trong bài.
Cần: numpy, scikit-learn. Chạy: python 2.2.py
"""
import numpy as np
from sklearn.linear_model import Lasso, LassoCV, Ridge, RidgeCV


# ---------- Dữ liệu ----------

def make_data(seed=1, n=100, k=30, n_train=40):
    """Giá = 0.05·diện tích − 0.15·khoảng cách + 1 + nhiễu, kèm k cột không liên quan."""
    rng = np.random.default_rng(seed)
    area = rng.uniform(30, 120, n)
    dist = rng.uniform(1, 15, n)
    junk = rng.normal(size=(n, k))
    y = 0.05 * area - 0.15 * dist + 1.0 + rng.normal(0, 0.4, n)
    X = np.column_stack([area, dist, junk])
    return X[:n_train], X[n_train:], y[:n_train], y[n_train:]


def standardize(X_tr, X_te):
    """Chuẩn hóa bằng trung bình và độ lệch chuẩn của tập train."""
    mu, sigma = X_tr.mean(axis=0), X_tr.std(axis=0)
    return (X_tr - mu) / sigma, (X_te - mu) / sigma


def r2(y_hat, y):
    return 1 - np.mean((y_hat - y) ** 2) / np.var(y)


# ---------- Ridge: nghiệm đóng, không phạt bias ----------

def fit_ridge(A, y, lam):
    """Cực tiểu Σ r² + λ‖w‖². Trừ trung bình để không phạt b."""
    a_mean, y_mean = A.mean(axis=0), y.mean()
    Ac, yc = A - a_mean, y - y_mean
    w = np.linalg.solve(Ac.T @ Ac + lam * np.eye(A.shape[1]), Ac.T @ yc)
    return w, y_mean - a_mean @ w


# ---------- Lasso: coordinate descent với soft-thresholding ----------

def soft(z, t):
    return np.sign(z) * np.maximum(np.abs(z) - t, 0)


def fit_lasso(A, y, lam, sweeps=500):
    """Cực tiểu ½ Σ r² + λ‖w‖₁, cập nhật lần lượt từng w_j."""
    a_mean, y_mean = A.mean(axis=0), y.mean()
    Ac, yc = A - a_mean, y - y_mean
    w = np.zeros(A.shape[1])
    col_sq = (Ac ** 2).sum(axis=0)
    for _ in range(sweeps):
        for j in range(len(w)):
            r_j = yc - Ac @ w + Ac[:, j] * w[j]        # phần dư khi bỏ đặc trưng j
            w[j] = soft(Ac[:, j] @ r_j, lam) / col_sq[j]
    return w, y_mean - a_mean @ w


def main():
    X_tr, X_te, y_tr, y_te = make_data()
    A_tr, A_te = standardize(X_tr, X_te)
    n = len(y_tr)

    print("== Linear regression không phạt ==")
    w, b = fit_ridge(A_tr, y_tr, 0.0)
    print(f"R² train = {r2(A_tr @ w + b, y_tr):.3f}   R² test = {r2(A_te @ w + b, y_te):.3f}")
    print(f"|hệ số rác| lớn nhất = {np.abs(w[2:]).max():.2f}")

    print("\n== Ridge theo λ ==")
    for lam in [0.1, 1, 3, 10, 30, 100]:
        w, b = fit_ridge(A_tr, y_tr, lam)
        print(f"λ = {lam:>5}: R² train = {r2(A_tr @ w + b, y_tr):.3f}   R² test = {r2(A_te @ w + b, y_te):.3f}")
    w, b = fit_ridge(A_tr, y_tr, 3.0)
    ref = Ridge(alpha=3.0).fit(A_tr, y_tr)
    print("Trùng scikit-learn Ridge:", np.allclose(w, ref.coef_) and np.allclose(b, ref.intercept_))

    print("\n== Lasso ==")
    w, b = fit_lasso(A_tr, y_tr, 8.0)
    print(f"λ = 8: giữ lại các cột {np.nonzero(w)[0]}, hệ số {w[w != 0].round(3)}, R² test = {r2(A_te @ w + b, y_te):.3f}")
    ref = Lasso(alpha=8.0 / n, tol=1e-10, max_iter=100000).fit(A_tr, y_tr)
    print("Trùng scikit-learn Lasso (alpha = λ/n):", np.allclose(w, ref.coef_, atol=1e-6))

    print("\n== Chọn λ bằng cross-validation ==")
    ridge = RidgeCV(alphas=np.logspace(-2, 3, 11)).fit(A_tr, y_tr)
    lasso = LassoCV(cv=5, random_state=0).fit(A_tr, y_tr)
    print(f"RidgeCV: alpha = {ridge.alpha_:.2f}   R² test = {ridge.score(A_te, y_te):.3f}")
    print(f"LassoCV: alpha = {lasso.alpha_:.3f}   giữ {(lasso.coef_ != 0).sum()} cột   R² test = {lasso.score(A_te, y_te):.3f}")

    print("\n== Đơn vị đo ảnh hưởng mức phạt (chưa chuẩn hóa) ==")
    B = X_tr[:, :2]
    for unit, scale in [("km", 1), ("m", 1000)]:
        m = Ridge(alpha=1000).fit(B * np.array([1, scale]), y_tr)
        print(f"khoảng cách theo {unit:>2}: hệ số quy về mỗi km = {m.coef_[1] * scale:.3f}")


if __name__ == "__main__":
    main()
