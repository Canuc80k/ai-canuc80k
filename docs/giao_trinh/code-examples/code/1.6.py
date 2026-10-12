# -*- coding: utf-8 -*-
# Code mẫu — Regression và ranking metrics

# Ví dụ 1: Một lỗi lớn làm hai metric chọn hai model khác nhau
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score

y = np.array([5.0, 10.0, 15.0])
prediction = np.array([6.0, 9.0, 18.0])
residual = prediction - y
manual_mae = np.abs(residual).mean()
manual_mse = (residual ** 2).mean()
assert np.isclose(manual_mae, mean_absolute_error(y, prediction))
assert np.isclose(manual_mse, mean_squared_error(y, prediction))
print("Phần dư, phút:", residual.tolist())
print(f"MAE={manual_mae:.3f} phút, MSE={manual_mse:.3f} phút²")
print(f"RMSE={root_mean_squared_error(y, prediction):.3f} phút, R2={r2_score(y, prediction):.3f}")
for name, pred in [("A", y + [0, 0, 6]), ("B", y + [3, 3, 3])]:
    print(f"{name}: MAE={mean_absolute_error(y, pred):.3f}, RMSE={root_mean_squared_error(y, pred):.3f}")


# Ví dụ 2: Đổi loss là đổi luôn baseline hằng số tốt nhất
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

X_train = np.zeros((4, 1))
y_train = np.array([2.0, 2.0, 2.0, 10.0])
for strategy in ["mean", "median"]:
    model = DummyRegressor(strategy=strategy).fit(X_train, y_train)
    prediction = model.predict(X_train)
    print(f"{strategy}: hằng số={prediction[0]:.1f}, MAE={mean_absolute_error(y_train, prediction):.1f}, MSE={mean_squared_error(y_train, prediction):.1f}")


# Ví dụ 3: Cùng sai một phút, nhưng tỉ lệ sai khác hẳn nhau
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

y = np.array([1.0, 100.0])
prediction = np.array([2.0, 101.0])
relative_errors = np.abs(prediction - y) / np.abs(y)
print("Lỗi tương đối từng bài:", relative_errors.tolist())
print(f"MAE={mean_absolute_error(y, prediction):.2f} phút, MAPE={100 * mean_absolute_percentage_error(y, prediction):.2f}%")
zero_y = np.array([0.0, 10.0])
zero_prediction = np.array([1.0, 10.0])
print("Có target 0:", bool(np.any(zero_y == 0)))
print(f"MAPE thư viện với target 0={mean_absolute_percentage_error(zero_y, zero_prediction):.3e}")


# Ví dụ 4: Từ score tạo ranking, rồi tự tính AP@3
import numpy as np

def ap_at_k(ranking, relevant, k):
    if k < 1:
        raise ValueError("k phải dương")
    top = list(ranking[:k])
    if len(top) != len(set(top)):
        raise ValueError("Duplicate trong top k")
    relevant = set(relevant)
    if not relevant:
        return 0.0
    hits = 0
    contribution = 0.0
    for position, item in enumerate(top, start=1):
        if item in relevant:
            hits += 1
            contribution += hits / position  # Chỉ cộng precision tại những vị trí trúng bài phù hợp.
    return contribution / min(len(relevant), k)

scores = {
    "Q1": {"P1": 0.9, "P2": 0.8, "P3": 0.7, "P4": 0.2},
    "Q2": {"P1": 0.9, "P2": 0.8, "P3": 0.2},
}
relevant = {"Q1": {"P1", "P3"}, "Q2": {"P2"}}
ap_scores = []
for query, item_scores in scores.items():
    ranking = sorted(item_scores, key=lambda item: (-item_scores[item], item))[:3]
    ap = ap_at_k(ranking, relevant[query], 3)
    ap_scores.append(ap)
    print(f"{query}: top3={ranking}, AP@3={ap:.6f}")
assert np.isclose(ap_scores[0], (1 + 2/3) / 2)
assert np.isclose(ap_scores[1], 1/2)
print(f"MAP@3={np.mean(ap_scores):.6f}")

improved = ["P1", "P3", "P2"]
print(f"Q1 đưa hit lên hạng 2: AP@3={ap_at_k(improved, relevant['Q1'], 3):.6f}")
assert ap_at_k(["P1"], {"P1", "P3"}, 3) == 0.5
assert ap_at_k(["P1"], set(), 3) == 0.0
try:
    ap_at_k(["P1", "P1", "P2"], relevant["Q1"], 3)
except ValueError as error:
    print("Chặn bảng sai:", error)

