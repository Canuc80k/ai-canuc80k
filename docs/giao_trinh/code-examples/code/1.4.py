# -*- coding: utf-8 -*-
# Code mẫu — Pipeline và data leakage

# Ví dụ 1: Validation lén làm đổi median và cả thước đo
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

train = np.array([[10.0], [20.0], [np.nan]])
valid = np.array([[100.0]])
correct = SimpleImputer(strategy="median").fit(train)
leaked = SimpleImputer(strategy="median").fit(np.vstack([train, valid]))
print("Median chỉ train:", correct.statistics_.tolist())
print("Median có nhìn validation, cách sai:", leaked.statistics_.tolist())
print("Train điền đúng:", correct.transform(train).ravel().tolist())

scaler = StandardScaler().fit([[10.0], [20.0]])
print("100 dùng thang train:", scaler.transform(valid).ravel().tolist())
print("100 fit thang riêng, cách sai:", StandardScaler().fit_transform(valid).ravel().tolist())


# Ví dụ 2: Bảng có cả số, chữ, và một danh mục chưa từng gặp
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression

train = pd.DataFrame({
    "registered": [10.0, 20.0, np.nan, 10.0, 20.0, 30.0],
    "slot": ["sang", "sang", "sang", "chieu", "chieu", "chieu"],
})
y = np.array([20, 40, 40, 25, 45, 65])
numeric = Pipeline([
    ("fill", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])
preprocess = ColumnTransformer([
    ("num", numeric, ["registered"]),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["slot"]),
])
model = Pipeline([("prep", preprocess), ("regression", LinearRegression())])
model.fit(train, y)
fitted_prep = model.named_steps["prep"]
median = fitted_prep.named_transformers_["num"].named_steps["fill"].statistics_[0]
print("Median train đã học:", float(median))
print("Tên feature sau biến đổi:", fitted_prep.get_feature_names_out().tolist())
assert median == train["registered"].median()

new = pd.DataFrame({"registered": [25.0, 25.0], "slot": ["sang", "toi"]})
transformed = fitted_prep.transform(new)
print("Shape mới:", transformed.shape)
print("One-hot buổi tối:", transformed[1, 1:].tolist())
print("Dự đoán sáng/tối:", np.round(model.predict(new), 2).tolist())


# Ví dụ 3: Kiểm median được học trong từng fold
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit, cross_validate

X = np.arange(10, 130, 10, dtype=float).reshape(-1, 1)
y = 2 * X[:, 0] + 5
X[[2, 8], 0] = np.nan
pipeline = Pipeline([
    ("fill", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
    ("regression", Ridge(alpha=1.0)),
])
folds = list(TimeSeriesSplit(n_splits=3, test_size=2).split(X))
result = cross_validate(
    pipeline, X, y, cv=folds, scoring="neg_mean_absolute_error",
    return_estimator=True, n_jobs=1,
)
for fold, ((train_ids, valid_ids), estimator) in enumerate(zip(folds, result["estimator"]), start=1):
    learned = float(estimator.named_steps["fill"].statistics_[0])
    expected = float(np.nanmedian(X[train_ids, 0]))
    assert learned == expected
    print(f"Fold {fold}: train đến hàng {int(train_ids[-1])}, median={learned:.1f}, kiểm train={expected:.1f}")
print("Median toàn bảng, không dùng cho fold:", float(np.nanmedian(X[:, 0])))

