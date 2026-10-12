# -*- coding: utf-8 -*-
# Data split và cross-validation — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
from sklearn.model_selection import train_test_split

labels = np.array([1, 1, 1] + [0] * 9)
row_ids = np.arange(len(labels))
train_ids, valid_ids = train_test_split(
    row_ids, test_size=0.25, random_state=13, stratify=labels
)
print("Số mẫu train/valid:", len(train_ids), len(valid_ids))
print("Số nhãn 1 train/valid:", labels[train_ids].sum(), labels[valid_ids].sum())
print("Trùng hàng:", len(set(train_ids) & set(valid_ids)))

# Bước 2
from sklearn.model_selection import GroupKFold

groups = np.repeat(np.arange(6), 3)
X_group = np.zeros((18, 1))                 # chỉ dùng để minh họa chỉ số
y_group = np.repeat([0, 1, 0, 1, 0, 1], 3)
all_ids = np.arange(18)
train_ids, valid_ids = train_test_split(
    all_ids, test_size=1/3, random_state=13
)
shared = set(groups[train_ids]) & set(groups[valid_ids])
print("Random split, người trùng:", sorted(map(int, shared)))

group_cv = GroupKFold(n_splits=3)
for fold, (train_ids, valid_ids) in enumerate(
    group_cv.split(X_group, y_group, groups), start=1
):
    shared = set(groups[train_ids]) & set(groups[valid_ids])
    assert not shared
    print(f"Fold {fold}: valid groups={sorted(map(int, set(groups[valid_ids])))}, trùng={len(shared)}")

# Bước 3
from sklearn.model_selection import TimeSeriesSplit

weeks = np.arange(12)
time_cv = TimeSeriesSplit(n_splits=3, test_size=2, gap=1)
for fold, (train_ids, valid_ids) in enumerate(time_cv.split(weeks), start=1):
    assert weeks[train_ids].max() < weeks[valid_ids].min()
    print(f"Fold {fold}: train={train_ids.tolist()}, valid={valid_ids.tolist()}")

# Bước 4
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = make_classification(
    n_samples=96, n_features=4, n_informative=3,
    n_redundant=0, random_state=13,
)
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=13)
oof_probability = np.full(len(y), np.nan)
times_scored = np.zeros(len(y), dtype=int)
fold_scores = []
for fold, (train_ids, valid_ids) in enumerate(cv.split(X, y), start=1):
    model = LogisticRegression(max_iter=500).fit(X[train_ids], y[train_ids])
    probability = model.predict_proba(X[valid_ids])[:, 1]
    oof_probability[valid_ids] = probability       # ghi về đúng vị trí gốc
    times_scored[valid_ids] += 1
    score = accuracy_score(y[valid_ids], probability >= 0.5)
    fold_scores.append(score)
    print(f"Fold {fold}: n={len(valid_ids)}, accuracy={score:.3f}")
assert np.all(times_scored == 1)
assert np.isfinite(oof_probability).all()
print("OOF shape:", oof_probability.shape)
print(f"Mean fold accuracy={np.mean(fold_scores):.3f}")
print(f"Pooled OOF accuracy={accuracy_score(y, oof_probability >= 0.5):.3f}")
