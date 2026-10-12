# -*- coding: utf-8 -*-
# Code mẫu — Ensemble

# Ví dụ 1: Trung bình xác suất có thể khác bỏ phiếu đa số
import numpy as np

P = np.array([[0.51, 0.51, 0.01], [0.9, 0.6, 0.6],
              [0.2, 0.8, 0.7], [0.8, 0.1, 0.1]])
assert P.shape == (4, 3)  # Hàng là mẫu, cột là model. Mọi cột đều là xác suất lớp 1.
hard = ((P >= 0.5).sum(axis=1) >= 2).astype(int)
mean = P.mean(axis=1)
manual = np.array([sum(row) / len(row) for row in P])
assert np.allclose(mean, manual)
print("majority:", hard.tolist())
print("mean xác suất:", mean.round(3).tolist())
print("nhãn từ mean:", (mean >= 0.5).astype(int).tolist())

# Cùng một mẫu, nhưng model B lưu các cột lớp theo thứ tự ngược lại.
A = np.array([0.8, 0.2])
B, classes_B = np.array([0.3, 0.7]), [1, 0]
aligned_B = B[[classes_B.index(label) for label in [0, 1]]]
print("mean chưa/sau căn lớp:", ((A + B) / 2).round(2).tolist(),
      ((A + aligned_B) / 2).round(2).tolist())
assert np.allclose((A + aligned_B) / 2, [0.75, 0.25])


# Ví dụ 2: Gộp xác suất sau khi hiệu chỉnh trên dữ liệu train
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss

X, y = make_moons(n_samples=240, noise=0.25, random_state=84)
train_rows, held_rows = train_test_split(np.arange(len(y)), test_size=0.4,
                                        random_state=1, stratify=y)
val_rows, audit_rows = train_test_split(held_rows, test_size=0.5,
                                       random_state=2, stratify=y[held_rows])
assert not (set(train_rows) & set(held_rows))
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=3)
estimators = {
    "linear": make_pipeline(StandardScaler(), LogisticRegression(max_iter=300)),
    "tree": DecisionTreeClassifier(max_depth=3, min_samples_leaf=4, random_state=4)
}
models = {}
for name, estimator in estimators.items():
    calibrated = CalibratedClassifierCV(estimator, method="sigmoid", cv=cv,
                                         ensemble=False, n_jobs=1)
    calibrated.fit(X[train_rows], y[train_rows])
    assert calibrated.classes_.tolist() == [0, 1]
    models[name] = calibrated
print("train/validation/audit:", len(train_rows), len(val_rows), len(audit_rows))
for split_name, rows in [("validation", val_rows), ("audit", audit_rows)]:
    predictions = np.stack([model.predict_proba(X[rows]) for model in models.values()])
    assert predictions.shape == (2, 48, 2)  # Trục: model, mẫu, lớp.
    average = predictions.mean(axis=0)
    assert np.allclose(average.sum(axis=1), 1)
    for name, probability in list(zip(models, predictions)) + [("mean", average)]:
        print(split_name, name, "log-loss:", f"{log_loss(y[rows], probability):.4f}")


# Ví dụ 3: Gộp theo thứ hạng khi đề chấm thứ tự
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

y = np.array([0, 0, 1, 0, 1, 0, 1, 1])
scores = np.array([[0.1, 3.0], [0.2, 2.0], [0.7, 8.0], [0.4, 1.0],
                   [0.8, 9.0], [0.3, 4.0], [0.35, 6.0], [0.9, 2.5]])
ranks = pd.DataFrame(scores).rank(axis=0, method="average").to_numpy()
assert np.array_equal(ranks[:, 1], pd.Series(scores[:, 1] * 10).rank().to_numpy())
combined = ((ranks - 0.5) / len(y)).mean(axis=1)
positive, negative = combined[y == 1], combined[y == 0]
manual_auc = np.mean([float(p > n) + 0.5 * float(p == n)
                      for p in positive for n in negative])
assert np.isclose(manual_auc, roc_auc_score(y, combined))
print("rank gộp:", combined.round(3).tolist())
print("AUC A/B/rank:", [round(roc_auc_score(y, s), 3)
                        for s in [scores[:, 0], scores[:, 1], combined]])
print("số cặp dương-âm kiểm:", len(positive) * len(negative))


# Ví dụ 4: Model tầng trên chỉ học từ dự đoán out-of-fold
import numpy as np
from sklearn.base import clone
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import log_loss

X, y = make_moons(n_samples=240, noise=0.30, random_state=184)
train_rows, val_rows = train_test_split(np.arange(len(y)), test_size=0.25,
                                       random_state=5, stratify=y)
Xt, yt, Xv, yv = X[train_rows], y[train_rows], X[val_rows], y[val_rows]
bases = [make_pipeline(StandardScaler(), LogisticRegression(max_iter=300)),
         DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=6)]
folds = list(StratifiedKFold(n_splits=3, shuffle=True, random_state=7).split(Xt, yt))
oof = np.zeros((len(yt), len(bases)))
filled = np.zeros_like(oof, dtype=int)
for fit_rows, held_rows in folds:
    assert not (set(fit_rows) & set(held_rows))
    for column, prototype in enumerate(bases):
        fitted = clone(prototype).fit(Xt[fit_rows], yt[fit_rows])
        assert fitted.classes_.tolist() == [0, 1]
        oof[held_rows, column] = fitted.predict_proba(Xt[held_rows])[:, 1]
        filled[held_rows, column] += 1
assert np.all(filled == 1)
meta = LogisticRegression(C=1.0, max_iter=300).fit(oof, yt)

full_models = [clone(prototype).fit(Xt, yt) for prototype in bases]
val_features = np.column_stack([model.predict_proba(Xv)[:, 1] for model in full_models])
assert not (set(train_rows) & set(val_rows))
stacked = meta.predict_proba(val_features)[:, 1]
print("OOF/validation feature shapes:", oof.shape, val_features.shape)
print("mỗi ô OOF được điền đúng một lần:", bool(np.all(filled == 1)))
for name, probability in [("linear", val_features[:, 0]), ("tree", val_features[:, 1]),
                          ("mean", val_features.mean(axis=1)), ("stack", stacked)]:
    distribution = np.column_stack([1 - probability, probability])
    print(name, "cùng validation log-loss:", f"{log_loss(yv, distribution):.4f}")

