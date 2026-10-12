# -*- coding: utf-8 -*-
# Code mẫu — Random forest

# Ví dụ 1: Một lượt bootstrap và hai cách gộp
import numpy as np

rng = np.random.default_rng(7)
draw = rng.integers(0, 5, size=5)
seen = np.unique(draw)
oob = np.setdiff1d(np.arange(5), seen)
print("rút:", draw.tolist())
print("đã thấy:", seen.tolist(), "OOB:", oob.tolist())

tree_probabilities = np.array([0.9, 0.4, 0.4])
mean_probability = tree_probabilities.mean()
votes_for_one = int(np.sum(tree_probabilities > 0.5))
print("trung bình xác suất:", round(float(mean_probability), 3))
print("phiếu lớp 1:", votes_for_one, "/", len(tree_probabilities))
assert np.all(np.isin(oob, [0, 1, 2, 3, 4]))
assert np.isclose(mean_probability, 17 / 30)
assert votes_for_one == 1

for rho in [0.5, 0.1]:
    variance_of_mean = rho + (1. - rho) / 100
    print("rho =", rho, "phương sai trung bình:", round(variance_of_mean, 3))
assert np.isclose(0.5 + 0.5 / 100, 0.505)
assert np.isclose(0.1 + 0.9 / 100, 0.109)


# Ví dụ 2: Đo OOB và độ đa dạng trên tập giữ lại
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=220, n_features=6, n_informative=3, n_redundant=0,
    class_sep=0.8, flip_y=0.08, random_state=12
)
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=4
)

for label, max_features in [("all", 1.0), ("sqrt", "sqrt")]:
    forest = RandomForestClassifier(
        n_estimators=60, max_features=max_features, oob_score=True,
        random_state=0, n_jobs=1
    ).fit(X_train, y_train)
    tree_predictions = np.array([
        tree.predict(X_valid) for tree in forest.estimators_
    ])
    pair_disagreements = [
        np.mean(tree_predictions[i] != tree_predictions[j])
        for i, j in [(0, 1), (0, 2), (1, 2)]
    ]
    print(label, "valid:", round(accuracy_score(y_valid, forest.predict(X_valid)), 3),
          "OOB:", round(float(forest.oob_score_), 3),
          "bất đồng 3 cặp:", np.round(pair_disagreements, 3).tolist())
    assert len(forest.estimators_) == 60


# Ví dụ 3: Importance, cột tương quan và một thay đổi có kiểm soát
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(23)
n = 240
tin_hieu_a = rng.normal(size=n)
tin_hieu_b = tin_hieu_a + rng.normal(0., 0.35, n)
nhieu = rng.normal(size=n)
y = (tin_hieu_a + rng.normal(0., 0.8, n) > 0).astype(int)
X = np.column_stack([tin_hieu_a, tin_hieu_b, nhieu])
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=5
)

forest = RandomForestClassifier(
    n_estimators=80, max_features="sqrt", random_state=0, n_jobs=1
).fit(X_train, y_train)
permutation = permutation_importance(
    forest, X_valid, y_valid, n_repeats=10, random_state=0,
    scoring="accuracy", n_jobs=1
)
print("valid:", round(accuracy_score(y_valid, forest.predict(X_valid)), 3))
print("impurity:", forest.feature_importances_.round(3).tolist())
print("permutation valid:", permutation.importances_mean.round(3).tolist())
assert permutation.importances_mean.shape == (3,)

for leaf_size in [1, 5, 12]:
    candidate = RandomForestClassifier(
        n_estimators=80, max_features="sqrt", min_samples_leaf=leaf_size,
        random_state=0, n_jobs=1
    ).fit(X_train, y_train)
    print("min_samples_leaf =", leaf_size,
          "train:", round(accuracy_score(y_train, candidate.predict(X_train)), 3),
          "valid:", round(accuracy_score(y_valid, candidate.predict(X_valid)), 3))

