# -*- coding: utf-8 -*-
# Kiểm tra khóa 1 — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error

rng = np.random.default_rng(12)
X = rng.normal(size=(120, 3))
y = 6 + X @ np.array([1.2, 0.8, 0.3]) + rng.normal(0, 0.4, 120)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=4)
folds = list(KFold(3, shuffle=True, random_state=9).split(X_train))
candidates = {
    "median": DummyRegressor(strategy="median"),
    "ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.)),
}
for name, model in candidates.items():
    scores = -cross_val_score(model, X_train, y_train, cv=folds, scoring="neg_mean_absolute_error")
    print(name, "MAE từng fold:", scores.round(3).tolist(), "mean:", round(scores.mean(), 3))

# Bước 2
selected = candidates["ridge"].fit(X_train, y_train)
predictions = selected.predict(X_test)
assert predictions.shape == y_test.shape
assert np.isfinite(predictions).all()
print("test MAE:", round(mean_absolute_error(y_test, predictions), 3))
sample_ids = np.arange(len(X_test)) + 1000
assert len(np.unique(sample_ids)) == len(sample_ids)
print("3 hàng đầu:", list(zip(sample_ids[:3].tolist(), predictions[:3].round(3).tolist())))
