# -*- coding: utf-8 -*-
# Code mẫu — Generalization

# Ví dụ 1: Một nhãn ghi sai kéo dự đoán đi xa tới đâu?
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

X_train = np.array([[0.0], [2.0], [4.0], [6.0]])
clean = np.array([0.0, 2.0, 4.0, 6.0])
noisy = np.array([0.0, 2.0, 8.0, 6.0])
query = np.array([[3.8]])
for k in [1, 3]:
    clean_model = KNeighborsRegressor(n_neighbors=k).fit(X_train, clean)
    noisy_model = KNeighborsRegressor(n_neighbors=k).fit(X_train, noisy)
    before = clean_model.predict(query)[0]
    after = noisy_model.predict(query)[0]
    train_mse = np.mean((noisy_model.predict(X_train) - noisy) ** 2)
    print(f"k={k}: trước={before:.3f}, sau={after:.3f}, đổi={after-before:.3f}, train MSE={train_mse:.3f}")


# Ví dụ 2: Cùng dữ liệu, ba mức linh hoạt
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

rng = np.random.default_rng(121)
def sample(n):
    X = rng.uniform(0, 1, (n, 1))
    y = np.sin(2 * np.pi * X[:, 0]) + rng.normal(0, 0.2, n)
    return X, y

X_train, y_train = sample(60)
X_valid, y_valid = sample(180)
for k in [1, 9, 60]:
    model = KNeighborsRegressor(n_neighbors=k).fit(X_train, y_train)
    train_error = mean_squared_error(y_train, model.predict(X_train))
    valid_error = mean_squared_error(y_valid, model.predict(X_valid))
    print(f"k={k:2d}: train MSE={train_error:.4f}, valid MSE={valid_error:.4f}")

# Khi k bằng số điểm train và trọng số đều nhau, mọi truy vấn đều nhận cùng một giá trị là trung bình train.
flat = KNeighborsRegressor(n_neighbors=60).fit(X_train, y_train)
assert np.allclose(flat.predict([[0.1], [0.9]]), y_train.mean())
print("k=60 dự đoán hằng số:", round(float(y_train.mean()), 4))


# Ví dụ 3: Learning curve thay đổi số mẫu, không thay đổi số epoch
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold, learning_curve

rng = np.random.default_rng(122)
X = rng.uniform(0, 1, (280, 1))
y = np.sin(2 * np.pi * X[:, 0]) + rng.normal(0, 0.2, 280)
cv = KFold(n_splits=4, shuffle=True, random_state=122)
sizes, train_scores, valid_scores = learning_curve(
    KNeighborsRegressor(n_neighbors=7), X, y, cv=cv,
    train_sizes=[21, 70, 210], scoring="neg_mean_squared_error",
    shuffle=True, random_state=122, n_jobs=1,
)
for n, train, valid in zip(sizes, -train_scores.mean(axis=1), -valid_scores.mean(axis=1)):
    print(f"n={n:3d}: train MSE={train:.4f}, valid MSE={valid:.4f}")
print("Phương sai nhiễu giả:", round(0.2 ** 2, 4))

