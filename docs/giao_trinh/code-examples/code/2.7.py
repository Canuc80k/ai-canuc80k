# -*- coding: utf-8 -*-
# Code mẫu — Gradient boosting

# Ví dụ 1: Một stump sửa phần dư
import numpy as np

x = np.array([[0.], [1.], [2.], [3.]])
y = np.array([1., 1., 3., 3.])
initial = np.full(len(y), y.mean())
residual_to_fix = y - initial
left = x[:, 0] <= 1.
manual_left = residual_to_fix[left].mean()
manual_right = residual_to_fix[~left].mean()
print("F0:", initial.tolist())
print("phần dư y - F0:", residual_to_fix.tolist())
print("bản sửa trái / phải:", manual_left, manual_right)
assert np.allclose(initial, 2.)
assert np.isclose(manual_left, -1.) and np.isclose(manual_right, 1.)

from sklearn.tree import DecisionTreeRegressor

for learning_rate in [1.0, 0.5]:
    prediction = np.full(len(y), y.mean())
    for stage in range(3):
        correction = DecisionTreeRegressor(max_depth=1, random_state=0)
        correction.fit(x, y - prediction)
        prediction += learning_rate * correction.predict(x)
        mse = np.mean((prediction - y) ** 2)
        print("lr =", learning_rate, "vòng", stage + 1,
              "dự đoán:", prediction.round(3).tolist(),
              "MSE:", round(float(mse), 4))


# Ví dụ 2: Chọn số vòng bằng validation sau từng vòng
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(31)
x = np.linspace(0., 8., 180)
y = np.sin(1.7 * x) + rng.normal(0., 0.22, len(x))
X = x[:, None]
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.20, random_state=11
)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_dev, y_dev, test_size=0.25, random_state=8
)

params = dict(max_depth=3, learning_rate=0.1, random_state=0)
full = GradientBoostingRegressor(n_estimators=180, **params).fit(X_train, y_train)
valid_losses = np.array([
    mean_squared_error(y_valid, prediction)
    for prediction in full.staged_predict(X_valid)
])
best_round = int(np.argmin(valid_losses)) + 1
print("vòng tốt nhất:", best_round)
print("MSE valid vòng 1 / tốt nhất / cuối:",
      round(float(valid_losses[0]), 3),
      round(float(valid_losses[best_round - 1]), 3),
      round(float(valid_losses[-1]), 3))

selected = GradientBoostingRegressor(n_estimators=best_round, **params).fit(
    X_train, y_train
)
test_mse = mean_squared_error(y_test, selected.predict(X_test))
print("MSE test sau khi khóa số vòng:", round(float(test_mse), 3))
assert 1 <= best_round <= 180
assert np.isfinite(test_mse)


# Ví dụ 3: So hai tốc độ học với cùng 180 cây
import numpy as np
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

X, y = make_friedman1(n_samples=280, n_features=5, noise=1.2, random_state=8)
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.20, random_state=10
)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_dev, y_dev, test_size=0.25, random_state=2
)

validation_rows = []
for learning_rate in [0.20, 0.05]:
    model = GradientBoostingRegressor(
        n_estimators=180, max_depth=2, learning_rate=learning_rate,
        random_state=0
    ).fit(X_train, y_train)
    valid_mae = mean_absolute_error(y_valid, model.predict(X_valid))
    validation_rows.append((learning_rate, float(valid_mae)))
    print("lr =", learning_rate, "MAE valid:", round(float(valid_mae), 3))

best_lr, best_valid_mae = min(validation_rows, key=lambda row: row[1])
X_fit = np.vstack([X_train, X_valid])
y_fit = np.concatenate([y_train, y_valid])
chosen = GradientBoostingRegressor(
    n_estimators=180, max_depth=2, learning_rate=best_lr, random_state=0
).fit(X_fit, y_fit)
test_mae = mean_absolute_error(y_test, chosen.predict(X_test))
print("lr chọn:", best_lr,
      "valid đã chọn:", round(best_valid_mae, 3),
      "MAE test:", round(float(test_mae), 3))
print("3 cặp target / dự đoán:", np.column_stack([
    y_test[:3], chosen.predict(X_test[:3])
]).round(3).tolist())
assert best_lr in {0.05, 0.2}
assert np.isfinite(test_mae)

