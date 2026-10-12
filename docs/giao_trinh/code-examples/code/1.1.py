# -*- coding: utf-8 -*-
# Code mẫu — Bài toán học máy

# Ví dụ 1: Chọn thông tin để chuẩn bị ghế
import pandas as pd

sessions = pd.DataFrame({
    "session_id": ["S01", "S02", "S03"],
    "registered": [20, 30, 40],
    "rain_forecast": [0.0, 0.5, 1.0],
    "attendance": [18, 23, 28],
})
features = ["registered", "rain_forecast"]
X = sessions[features]             # Bảng hai chiều: mỗi hàng là một buổi, mỗi cột là một feature.
y = sessions["attendance"]         # Target là vector một chiều, và không được nằm trong X.

print("X/y shape:", X.shape, y.shape)
print("Feature:", X.columns.tolist())
print("Nhãn nếu hỏi có ít nhất 25 người:", (y >= 25).astype(int).tolist())
assert "attendance" not in X.columns
assert "session_id" not in X.columns


# Ví dụ 2: So baseline với một quy luật tuyến tính
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

train = pd.DataFrame({
    "registered": [10, 20, 30, 10, 20, 30],
    "rain_forecast": [0, 0, 0, 1, 1, 1],
    "attendance": [10, 18, 26, 4, 12, 20],
})
valid = pd.DataFrame({
    "registered": [25, 15],
    "rain_forecast": [0.5, 0.5],
    "attendance": [20, 10],
})
columns = ["registered", "rain_forecast"]
models = {"mean": DummyRegressor(), "linear": LinearRegression()}
valid_errors = {}
for name, model in models.items():
    model.fit(train[columns], train["attendance"])
    prediction = model.predict(valid[columns])
    valid_errors[name] = mean_absolute_error(valid["attendance"], prediction)
    print(f"{name}: prediction={np.round(prediction, 2).tolist()}, MAE={valid_errors[name]:.2f} người")

chosen = min(valid_errors, key=valid_errors.get)
print("Chọn bằng validation:", chosen)
print("Hệ số linear:", np.round(models["linear"].coef_, 2).tolist())


# Ví dụ 3: Dự đoán đúng, nhưng ghép nhầm mã buổi
from io import StringIO
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

train = pd.DataFrame({"registered": [10, 20, 30, 40]})
y_train = np.array([9, 17, 25, 33])
model = LinearRegression().fit(train, y_train)
new = pd.DataFrame({
    "session_id": ["S09", "S07", "S08"],
    "registered": [35, 15, 25],
})
prediction = np.round(model.predict(new[["registered"]]), 2)
result = pd.DataFrame({"session_id": new["session_id"], "attendance": prediction})
read_back = pd.read_csv(StringIO(result.to_csv(index=False)))
assert read_back.columns.tolist() == ["session_id", "attendance"]
assert read_back["session_id"].tolist() == new["session_id"].tolist()
assert read_back["session_id"].is_unique
assert np.isfinite(read_back["attendance"]).all()
print(read_back.to_string(index=False))

wrong = result.copy()
wrong["attendance"] = np.sort(prediction)  # Số hàng vẫn đúng, nhưng mỗi dự đoán đã sang tay buổi khác.
print("Ghép đúng sau khi sort riêng prediction:", wrong.equals(result))

