# -*- coding: utf-8 -*-
# Code mẫu — Linear regression

# Ví dụ 1: Ước lượng tiền thuê xe theo số giờ
import numpy as np

hours = np.array([1., 2., 3.])
cost = np.array([50., 70., 90.])
# Cột toàn số 1 đại diện cho phí ban đầu. Thứ tự tham số là (phí mỗi giờ, phí ban đầu).
A = np.column_stack([hours, np.ones(len(hours))])
theta, _, rank, _ = np.linalg.lstsq(A, cost, rcond=None)
prediction = A @ theta
residual = prediction - cost
print("hệ số:", theta.round(3).tolist())
print("dự đoán train:", prediction.round(3).tolist())
print("2.5 giờ:", round(float(np.array([2.5, 1.]) @ theta), 3))
print("hạng / số cột:", rank, "/", A.shape[1])
assert np.allclose(theta, [20., 30.])
assert np.allclose(A.T @ residual, 0.)

A_duplicate = np.column_stack([hours, 60 * hours, np.ones(len(hours))])
theta_duplicate, _, rank_duplicate, _ = np.linalg.lstsq(
    A_duplicate, cost, rcond=None
)
print("hạng / số cột:", rank_duplicate, "/", A_duplicate.shape[1])
print("hệ số giờ + 60 × hệ số phút:",
      round(float(theta_duplicate[0] + 60 * theta_duplicate[1]), 3))
print("dự đoán vẫn khớp:", np.allclose(A_duplicate @ theta_duplicate, cost))
assert rank_duplicate < A_duplicate.shape[1]


# Ví dụ 2: Một bước học làm tham số thay đổi thế nào?
import numpy as np

x = np.array([1., 2., 3.])
y = np.array([2., 3., 5.])
A = np.column_stack([x, np.ones(len(x))])

def loss(theta):
    pred = A @ theta
    assert pred.shape == y.shape  # Chặn lỗi broadcasting tạo ra ma trận lỗi n×n.
    return np.mean((pred - y) ** 2)

theta = np.zeros(2)
gradient = 2 * A.T @ (A @ theta - y) / len(y)
print("gradient:", gradient.round(4).tolist())
print("loss trước:", round(float(loss(theta)), 4))
theta -= 0.1 * gradient
print("tham số sau 1 bước:", theta.round(4).tolist())
print("loss sau:", round(float(loss(theta)), 4))

largest_curvature = np.linalg.eigvalsh(2 * A.T @ A / len(y))[-1]
print("ngưỡng learning rate:", round(float(2 / largest_curvature), 4))
for rate in [0.1, 0.3]:
    theta = np.zeros(2)
    checkpoints = []
    for step in range(31):
        if step in [0, 1, 10, 30]:
            checkpoints.append(round(float(loss(theta)), 4))
        theta -= rate * 2 * A.T @ (A @ theta - y) / len(y)
    print("lr =", rate, "loss ở bước 0,1,10,30:", checkpoints)


# Ví dụ 3: Định giá căn hộ, và kiểm phần dư
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(21)
area = rng.uniform(40, 100, 80)
distance = rng.uniform(1, 12, 80)
X = np.column_stack([area, distance])
y = 0.04 * area - 0.10 * distance + 0.7 + rng.normal(0, 0.12, 80)
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.25, random_state=4
)
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_valid)
print("hệ số (diện tích, khoảng cách):", model.coef_.round(4).tolist())
print("intercept:", round(float(model.intercept_), 4))
print("MAE baseline / mô hình:",
      round(mean_absolute_error(y_valid, baseline.predict(X_valid)), 4),
      round(mean_absolute_error(y_valid, pred), 4))
print("(thật, dự đoán, phần dư) 4 hàng:",
      np.column_stack([y_valid, pred, pred - y_valid])[:4].round(3).tolist())

unit_factor = np.array([1., 1000.])
model_m = LinearRegression().fit(X_train * unit_factor, y_train)
print("hệ số mỗi mét:", round(float(model_m.coef_[1]), 7))
print("hệ số quy về mỗi km:", round(float(model_m.coef_[1] * 1000), 4))
print("dự đoán không đổi:",
      np.allclose(pred, model_m.predict(X_valid * unit_factor)))
queries = np.array([[70., 5.], [140., 5.]])
print("căn 70 và 140 m², cùng cách 5 km:", model.predict(queries).round(3).tolist())
assert np.allclose(pred, model_m.predict(X_valid * unit_factor))

