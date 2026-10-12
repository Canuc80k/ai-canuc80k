# -*- coding: utf-8 -*-
# Code mẫu — Kiểm tra khóa 1

# Ví dụ 1: Dự đoán điểm buổi luyện từ một bảng thiếu dữ liệu
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(41)
previous = rng.uniform(3, 9, 120)
hours = rng.uniform(0, 8, 120)
mode = np.where(np.arange(120) % 2 == 0, "group", "solo")
target = 0.65 * previous + 0.4 * hours + 0.7 * (mode == "group") + rng.normal(0, 0.3, 120)
frame = pd.DataFrame({"id": np.arange(1000, 1120), "previous": previous,
                      "hours": hours, "mode": mode})
frame.loc[::13, "previous"] = np.nan
frame.loc[::17, "hours"] = np.nan
dev, test, y_dev, y_test = train_test_split(frame, target, test_size=0.25, random_state=2)
feature_columns = ["previous", "hours", "mode"]
X_dev, X_test = dev[feature_columns], test[feature_columns]
print("số hàng phát triển / test:", len(dev), len(test))
print("4 hàng phát triển:")
print(X_dev.head(4).round(2).to_string(index=False))
print("số NaN phát triển:", X_dev[["previous", "hours"]].isna().sum().to_dict())
assert set(dev["id"]).isdisjoint(set(test["id"]))

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

def make_preprocessor(scale):
    number_steps = [SimpleImputer(strategy="median", add_indicator=True)]
    if scale:
        number_steps.append(StandardScaler())
    return ColumnTransformer([
        ("number", make_pipeline(*number_steps), ["previous", "hours"]),
        ("mode", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["mode"]),
    ])

candidates = {
    "median": DummyRegressor(strategy="median"),
    "ridge": make_pipeline(make_preprocessor(True), Ridge(alpha=1.)),
    "tree": make_pipeline(make_preprocessor(False),
                           DecisionTreeRegressor(max_depth=4, min_samples_leaf=5, random_state=0)),
}
folds = list(KFold(3, shuffle=True, random_state=9).split(X_dev))
cv_errors = {}
for name, model in candidates.items():
    errors = -cross_val_score(model, X_dev, y_dev, cv=folds,
                              scoring="neg_mean_absolute_error", n_jobs=1)
    cv_errors[name] = errors.mean()
    print(name, "MAE từng fold:", errors.round(3).tolist(), "mean:", round(float(errors.mean()), 3))
selected_name = min(cv_errors, key=cv_errors.get)
print("chọn từ CV:", selected_name)

from sklearn.metrics import mean_absolute_error

chosen = candidates[selected_name].fit(X_dev, y_dev)
pred = chosen.predict(X_test)
submission = pd.DataFrame({"id": test["id"].to_numpy(), "prediction": pred})
assert pred.shape == y_test.shape and np.isfinite(pred).all()
assert submission["id"].is_unique
assert np.array_equal(submission["id"], test["id"])
print("test MAE:", round(mean_absolute_error(y_test, pred), 3))
print("5 hàng đầu ra:")
print(submission.head(5).round(3).to_string(index=False))
missing = X_test[["previous", "hours"]].isna().any(axis=1).to_numpy()
for label, mask in [("đủ input", ~missing), ("thiếu input", missing)]:
    if mask.any():
        print(label, "n =", int(mask.sum()), "MAE =",
              round(mean_absolute_error(y_test[mask], pred[mask]), 3))


# Ví dụ 2: Lỗi shape và lỗi ID đều chạy được, không báo gì
import numpy as np
import pandas as pd

ids = np.array([103, 101, 102])
truth = np.array([2., 4., 8.])
pred = np.array([3., 4., 7.])
pred_column = pred[:, None]
wrong_difference = pred_column - truth
print("shape lỗi:", wrong_difference.shape)
print("MAE sai do broadcasting:", round(float(np.abs(wrong_difference).mean()), 3))
print("MAE đúng:", round(float(np.abs(pred_column.ravel() - truth).mean()), 3))
assert pred_column.ravel().shape == truth.shape

correct = pd.DataFrame({"id": ids, "prediction": pred})
wrong = pd.DataFrame({"id": np.sort(ids), "prediction": pred})
reference = pd.DataFrame({"id": ids, "truth": truth})
for name, table in [("giữ cặp ID–pred", correct), ("sort chỉ ID", wrong)]:
    checked = reference.merge(table, on="id", validate="one_to_one", sort=False)
    mae = np.abs(checked["prediction"] - checked["truth"]).mean()
    print(name, "MAE ghép theo ID:", round(float(mae), 3))
print("bảng đúng sau khi sort cả hàng:")
print(correct.sort_values("id").to_string(index=False))

