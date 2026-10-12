# -*- coding: utf-8 -*-
# Feature engineering — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
import pandas as pd

history = pd.DataFrame({"shop": ["A", "A", "A", "B", "B"],
                        "time": [1, 2, 3, 1, 2],
                        "sales": [5., 7., 6., 3., 4.]})
history = history.sort_values(["shop", "time"])
history["lag_1"] = history.groupby("shop")["sales"].shift(1)
history["mean_prev_2"] = history.groupby("shop")["sales"].transform(
    lambda s: s.shift(1).rolling(2, min_periods=2).mean()
)
print(history.to_string(index=False))
assert history.loc[2, "mean_prev_2"] == 6.

# Bước 2
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

train_features = pd.DataFrame({"size": [10., np.nan, 30.], "shop": ["A", "B", "A"]})
new_features = pd.DataFrame({"size": [20.], "shop": ["C"]})
numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
preprocessor = ColumnTransformer([
    ("number", numeric, ["size"]),
    ("category", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["shop"]),
])
encoded_train = preprocessor.fit_transform(train_features)
encoded_new = preprocessor.transform(new_features)
print("shape:", encoded_train.shape, encoded_new.shape)
print("mẫu mới:", encoded_new.round(3).tolist())

# Bước 3
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "time": pd.date_range("2026-10-01", periods=6, freq="h"),
    "shop": ["A", "B", "A", "A", "B", "A"],
    "sales": [5, 3, 7, 6, 4, 9],
})
df["hour_sin"] = np.sin(2 * np.pi * df["time"].dt.hour / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["time"].dt.hour / 24)
df["lag_1"] = df.groupby("shop")["sales"].shift(1)
df["roll_mean_2"] = df.groupby("shop")["sales"].transform(lambda s: s.shift(1).rolling(2).mean())
df["shop_count"] = df.groupby("shop").cumcount()  # số lần đã xuất hiện trước hàng hiện tại
print(df.drop(columns="time").round(2).to_string())
