# -*- coding: utf-8 -*-
# Gradient boosting — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
from sklearn.tree import DecisionTreeRegressor

xb = np.array([[0.], [1.], [2.], [3.]])
yb = np.array([1., 1., 3., 3.])
prediction = np.full(len(yb), yb.mean())
learning_rate = 0.5
for stage in range(3):
    residual_to_fix = yb - prediction
    correction = DecisionTreeRegressor(max_depth=1, random_state=0)
    correction.fit(xb, residual_to_fix)
    prediction = prediction + learning_rate * correction.predict(xb)
    mse_now = np.mean((prediction - yb) ** 2)
    print(stage + 1, prediction.tolist(), round(float(mse_now), 6))

# Bước 2
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

X_stage, y_stage = make_friedman1(n_samples=250, noise=4.0, random_state=3)   # phi tuyến, nhiễu lớn
X_train, X_valid, y_train, y_valid = train_test_split(X_stage, y_stage, test_size=0.3, random_state=8)
boost = GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.1, random_state=0)
boost.fit(X_train, y_train)
train_losses = [np.mean((pred - y_train) ** 2) for pred in boost.staged_predict(X_train)]
valid_losses = [np.mean((pred - y_valid) ** 2) for pred in boost.staged_predict(X_valid)]
best_round = int(np.argmin(valid_losses)) + 1
print("vòng chọn:", best_round)
print("MSE train, vòng chọn và vòng cuối:", round(float(train_losses[best_round - 1]), 2), round(float(train_losses[-1]), 2))
print("MSE valid, vòng chọn và vòng cuối:", round(float(valid_losses[best_round - 1]), 2), round(float(valid_losses[-1]), 2))

# Bước 3
from sklearn.datasets import make_friedman1
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split

X, y = make_friedman1(n_samples=5000, noise=1.0, random_state=0)   # quan hệ phi tuyến có tương tác
X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.2, random_state=0)
model = HistGradientBoostingRegressor(learning_rate=0.05, max_iter=2000, max_leaf_nodes=31,
                                      early_stopping=True, validation_fraction=0.1,
                                      n_iter_no_change=50, random_state=0)
model.fit(X_tr, y_tr)
print("số cây:", model.n_iter_, " R2 validation:", round(model.score(X_va, y_va), 3))
