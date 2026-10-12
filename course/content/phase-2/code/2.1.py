"""Linear regression: định giá căn hộ từ diện tích và khoảng cách.

Code đi kèm bài 2.1, chạy từ đầu đến cuối theo đúng thứ tự các phần trong bài.
Cần: numpy, scikit-learn. Chạy: python 2.1.py
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


# ---------- Dữ liệu và mô hình ----------

def make_data(n=200, seed=0):
    """n căn hộ: giá = 0.05·diện tích − 0.15·khoảng cách + 1 + nhiễu (tỷ đồng)."""
    rng = np.random.default_rng(seed)
    area = rng.uniform(30, 120, n)                # m²
    dist = rng.uniform(1, 15, n)                  # km đến trung tâm
    y = 0.05 * area - 0.15 * dist + 1.0 + rng.normal(0, 0.3, n)
    return np.column_stack([area, dist]), y       # X: (n, 2), y: (n,)


def predict(X, w, b):
    return X @ w + b


def mse(y_hat, y):
    assert y_hat.shape == y.shape, (y_hat.shape, y.shape)   # chặn broadcasting âm thầm
    return np.mean((y_hat - y) ** 2)


# ---------- Nghiệm đóng ----------

def fit_closed_form(X, y):
    """Giải hệ phương trình chuẩn X̃ᵀX̃ θ = X̃ᵀy, với X̃ = [X, 1]."""
    Xb = np.column_stack([X, np.ones(len(X))])
    theta = np.linalg.solve(Xb.T @ Xb, Xb.T @ y)
    return theta[:-1], theta[-1]


# ---------- Gradient descent ----------

def loss(theta, X, y):
    """theta = (w_1, ..., w_d, b)."""
    return mse(predict(X, theta[:-1], theta[-1]), y)


def grad(theta, X, y):
    r = predict(X, theta[:-1], theta[-1]) - y               # phần dư, shape (n,)
    return np.append(2 / len(y) * X.T @ r, 2 * r.mean())


def gd(X, y, lr, epochs):
    theta = np.zeros(X.shape[1] + 1)
    history = []
    for _ in range(epochs):
        history.append(loss(theta, X, y))
        theta -= lr * grad(theta, X, y)
    return theta, history


# ---------- Kiểm tra gradient ----------

def numerical_grad(f, theta, h=1e-5):
    g = np.zeros_like(theta)
    for j in range(len(theta)):
        e = np.zeros_like(theta)
        e[j] = h
        g[j] = (f(theta + e) - f(theta - e)) / (2 * h)
    return g


def rel_error(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))


# ---------- Learning rate và chuẩn hóa ----------

def lr_limit(X):
    """Ngưỡng 2/λ_max và số điều kiện của Hessian H = (2/n) X̃ᵀX̃."""
    Xb = np.column_stack([X, np.ones(len(X))])
    eig = np.linalg.eigvalsh(2 / len(X) * Xb.T @ Xb)
    return 2 / eig[-1], eig[-1] / eig[0]


def standardize(X):
    mu, sigma = X.mean(axis=0), X.std(axis=0)
    return (X - mu) / sigma, mu, sigma


def to_original_scale(theta_s, mu, sigma):
    """Đổi trọng số học trên z = (x − μ)/σ về đơn vị gốc."""
    w = theta_s[:-1] / sigma
    b = theta_s[-1] - np.sum(theta_s[:-1] * mu / sigma)
    return w, b


def main():
    X, y = make_data()

    print("== Dữ liệu ==")
    print(f"X: {X.shape}   y: {y.shape}")
    print(f"Mốc đoán trung bình: MSE = {mse(np.full_like(y, y.mean()), y):.4f}   Var(y) = {y.var():.4f}")

    print("\n== Nghiệm đóng ==")
    w_cf, b_cf = fit_closed_form(X, y)
    print(f"w = {w_cf.round(4)}   b = {b_cf:.4f}")
    print(f"MSE = {mse(predict(X, w_cf, b_cf), y):.4f}")
    print(f"Căn 70 m², cách trung tâm 8 km: {predict(np.array([70, 8]), w_cf, b_cf):.2f} tỷ")

    print("\n== Kiểm tra gradient ==")
    theta0 = np.random.default_rng(1).normal(size=3)
    f = lambda t: loss(t, X, y)
    print(f"grad đúng:            sai số tương đối {rel_error(grad(theta0, X, y), numerical_grad(f, theta0)):.1e}")
    buggy = lambda t, X, y: grad(t, X, y) / 2                 # mô phỏng lỗi quên hệ số 2
    print(f"grad quên hệ số 2:    sai số tương đối {rel_error(buggy(theta0, X, y), numerical_grad(f, theta0)):.3f}")

    print("\n== Learning rate trên dữ liệu gốc ==")
    limit, kappa = lr_limit(X)
    print(f"Ngưỡng 2/λ_max = {limit:.2e}   số điều kiện = {kappa:.0f}")
    with np.errstate(over="ignore", invalid="ignore"):         # loss nổ sẽ tràn số; bỏ cảnh báo cho gọn
        for lr in [1e-3, 2e-4, 1e-4]:
            _, hist = gd(X, y, lr, 1000)
            print(f"lr = {lr:.0e}: loss sau 1000 vòng = {hist[-1]:.4g}")

    print("\n== Sau khi chuẩn hóa ==")
    Xs, mu, sigma = standardize(X)
    limit, kappa = lr_limit(Xs)
    print(f"Ngưỡng 2/λ_max = {limit:.3f}   số điều kiện = {kappa:.2f}")
    with np.errstate(over="ignore", invalid="ignore"):
        for lr in [0.01, 0.1, 0.5, 1.0]:
            _, hist = gd(Xs, y, lr, 100)
            print(f"lr = {lr:<4}: loss sau 100 vòng = {hist[-1]:.4g}")
    theta_s, _ = gd(Xs, y, 0.1, 200)
    w_gd, b_gd = to_original_scale(theta_s, mu, sigma)
    print(f"Đổi về đơn vị gốc: w = {w_gd.round(4)}   b = {b_gd:.4f}")

    print("\n== scikit-learn ==")
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
    model = LinearRegression().fit(X_tr, y_tr)
    print(f"R² train = {model.score(X_tr, y_tr):.3f}   R² test = {model.score(X_te, y_te):.3f}")
    full = LinearRegression().fit(X, y)
    same = np.allclose(full.coef_, w_cf) and np.allclose(full.intercept_, b_cf)
    print(f"Trùng nghiệm đóng: {same}   trùng gradient descent: {np.allclose(w_gd, w_cf) and np.allclose(b_gd, b_cf)}")

    print("\n== Đoán độ phức tạp ==")
    ns = np.array([1e3, 2e3, 5e3, 1e4, 2e4, 5e4])
    t = np.array([0.0011, 0.0042, 0.026, 0.098, 0.41, 2.47])   # giây
    k, c = np.polyfit(np.log(ns), np.log(t), 1)
    print(f"Hệ số góc = {k:.2f}   dự đoán n = 2·10⁵: {np.exp(c) * 2e5 ** k:.0f} giây")


if __name__ == "__main__":
    main()
