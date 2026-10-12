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

# Bước 4
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

X_num, y = make_classification(n_samples=3000, n_features=8, n_informative=5, flip_y=0.08, random_state=1)
rng = np.random.default_rng(1)
df = pd.DataFrame(X_num, columns=[f"f{i}" for i in range(8)])
df["city"] = rng.choice(["HN", "HCM", "DN", "HP", "CT"], size=len(df))
y = np.where(df["city"].isin(["HN", "DN"]) & (rng.random(len(df)) < 0.25), 1, y)   # thành phố có ảnh hưởng thật
df["city"] = df["city"].astype("category")
train, test = df.iloc[:2400], df.iloc[2400:]
y_train, y_test = y[:2400], y[2400:]

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
oof = np.zeros(len(train))
test_pred = np.zeros(len(test))
for k, (tr, va) in enumerate(folds.split(train, y_train)):
    model = lgb.LGBMClassifier(learning_rate=0.05, n_estimators=2000, num_leaves=15,
                               subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                               random_state=0, verbose=-1, n_jobs=1)
    model.fit(train.iloc[tr], y_train[tr], eval_set=[(train.iloc[va], y_train[va])],
              eval_metric="auc", callbacks=[lgb.early_stopping(100, verbose=False)])
    oof[va] = model.predict_proba(train.iloc[va])[:, 1]
    test_pred += model.predict_proba(test)[:, 1] / folds.n_splits
    print(f"fold {k}: cây tốt nhất {model.best_iteration_}, AUC {roc_auc_score(y_train[va], oof[va]):.3f}")
print("AUC out-of-fold:", round(roc_auc_score(y_train, oof), 3))
print("AUC test (trung bình 5 model):", round(roc_auc_score(y_test, test_pred), 3))

# Bước 5
import xgboost as xgb

oof_xgb = np.zeros(len(train))
for k, (tr, va) in enumerate(folds.split(train, y_train)):
    model = xgb.XGBClassifier(learning_rate=0.05, n_estimators=2000, max_depth=4, subsample=0.8,
                              colsample_bytree=0.8, enable_categorical=True, tree_method="hist",
                              early_stopping_rounds=100, eval_metric="auc", random_state=0, n_jobs=1)
    model.fit(train.iloc[tr], y_train[tr], eval_set=[(train.iloc[va], y_train[va])], verbose=False)
    oof_xgb[va] = model.predict_proba(train.iloc[va])[:, 1]
print("AUC OOF XGBoost:", round(roc_auc_score(y_train, oof_xgb), 3))
print("AUC OOF trung bình hai thư viện:", round(roc_auc_score(y_train, (oof + oof_xgb) / 2), 3))
