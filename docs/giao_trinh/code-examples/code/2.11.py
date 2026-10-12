# -*- coding: utf-8 -*-
# Code mẫu — Feature engineering

# Ví dụ 1: Để 23 giờ nằm cạnh 0 giờ
import numpy as np

hours = np.array([0., 1., 12., 23.])
angle = 2 * np.pi * hours / 24
encoded = np.column_stack([np.sin(angle), np.cos(angle)])
print("(giờ, sin, cos):", np.column_stack([hours, encoded]).round(3).tolist())
print("khoảng cách 23–0 thô / chu kỳ:",
      abs(hours[3] - hours[0]), round(float(np.linalg.norm(encoded[3] - encoded[0])), 3))
print("khoảng cách 12–0 chu kỳ:", round(float(np.linalg.norm(encoded[2] - encoded[0])), 3))
print("norm mỗi hàng:", np.linalg.norm(encoded, axis=1).round(3).tolist())
assert np.allclose(np.linalg.norm(encoded, axis=1), 1.)


# Ví dụ 2: Feature quá khứ không được đổi khi sửa target hiện tại
import numpy as np
import pandas as pd

history = pd.DataFrame({
    "shop": ["A", "B", "A", "A", "B", "A"],
    "hour": [3, 2, 1, 4, 1, 2],
    "sales": [6., 9., 4., 10., 2., 8.],
})

def historical_features(frame):
    result = frame.sort_values(["shop", "hour"]).reset_index(drop=True).copy()
    result["lag_1"] = result.groupby("shop")["sales"].shift(1)
    result["mean_prev_2"] = result.groupby("shop")["sales"].transform(
        lambda series: series.shift(1).rolling(2, min_periods=2).mean()
    )
    return result

features = historical_features(history)
print(features.to_string(index=False))
at_hour_3 = (features["shop"] == "A") & (features["hour"] == 3)
print("A giờ 3: lag / mean:",
      features.loc[at_hour_3, ["lag_1", "mean_prev_2"]].to_numpy().tolist())
assert features.loc[at_hour_3, "mean_prev_2"].iloc[0] == (4 + 8) / 2

changed = history.copy()
changed.loc[(changed["shop"] == "A") & (changed["hour"] == 3), "sales"] = 600.
changed_features = historical_features(changed)
valid_columns = ["lag_1", "mean_prev_2"]
print("feature giờ 3 không đổi:", np.allclose(
    features.loc[at_hour_3, valid_columns], changed_features.loc[at_hour_3, valid_columns]
))
wrong = features.groupby("shop")["sales"].transform(lambda s: s.rolling(2).mean())
wrong_changed = changed_features.groupby("shop")["sales"].transform(lambda s: s.rolling(2).mean())
print("rolling chưa shift tại giờ 3:",
      float(wrong[at_hour_3].iloc[0]), "->", float(wrong_changed[at_hour_3].iloc[0]))
assert np.allclose(features.loc[at_hour_3, valid_columns],
                   changed_features.loc[at_hour_3, valid_columns])


# Ví dụ 3: Mã hiếm có thể giấu chính đáp án trong feature
import numpy as np
from sklearn.preprocessing import TargetEncoder

X = np.array([["A"], ["B"], ["C"], ["D"], ["E"], ["F"]], dtype=object)
y = np.array([5., 8., 11., 20., 25., 30.])
unsafe_encoder = TargetEncoder(target_type="continuous", smooth=0., cv=3, shuffle=False)
unsafe_train = unsafe_encoder.fit(X, y).transform(X)
safe_encoder = TargetEncoder(target_type="continuous", smooth=0., cv=3, shuffle=False)
cross_fitted = safe_encoder.fit_transform(X, y)
new_customer = safe_encoder.transform(np.array([["NEW"]], dtype=object))
print("target:", y.tolist())
print("fit rồi transform train:", unsafe_train.ravel().round(3).tolist())
print("fit_transform cross-fitting:", cross_fitted.ravel().round(3).tolist())
print("mã mới / mean train:", round(float(new_customer[0, 0]), 3), round(float(y.mean()), 3))
assert np.allclose(unsafe_train.ravel(), y)
assert np.allclose(cross_fitted[:2].ravel(), y[2:].mean())


# Ví dụ 4: Ước tính thời gian di chuyển bằng quãng đường chia tốc độ
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(31)
distance = rng.uniform(2, 30, 90)
speed = rng.uniform(20, 60, 90)
route = np.where(np.arange(90) % 2 == 0, "city", "outer")
y = 60 * distance / speed + 4 * (route == "city") + rng.normal(0, 0.5, 90)
frame = pd.DataFrame({"km": distance, "speed": speed, "route": route})
frame["travel_minutes"] = 60 * frame["km"] / frame["speed"]
folds = list(KFold(3, shuffle=True, random_state=4).split(frame))
for name, numeric_columns in [
    ("cột gốc", ["km", "speed"]),
    ("thêm tỷ số", ["km", "speed", "travel_minutes"]),
]:
    preprocessing = ColumnTransformer([
        ("number", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_columns),
        ("route", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["route"]),
    ])
    pipeline = make_pipeline(preprocessing, Ridge(alpha=1.))
    mae = -cross_val_score(pipeline, frame, y, cv=folds,
                           scoring="neg_mean_absolute_error", n_jobs=1)
    print(name, "MAE từng fold:", mae.round(3).tolist(), "mean:", round(float(mae.mean()), 3))

fitted = pipeline.fit(frame, y)  # Biến pipeline lúc này là cấu hình có tỷ số, từ vòng lặp cuối.
new_trip = pd.DataFrame({"km": [10.], "speed": [40.], "route": ["rural"]})
new_trip["travel_minutes"] = 60 * new_trip["km"] / new_trip["speed"]
transformed = fitted[0].transform(new_trip)
print("tên cột:", fitted[0].get_feature_names_out().tolist())
print("shape / mã tuyến mới:", transformed.shape, transformed[0, -2:].tolist())
print("dự đoán phút:", fitted.predict(new_trip).round(3).tolist())
assert np.allclose(transformed[0, -2:], 0.)

