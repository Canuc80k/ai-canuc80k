# -*- coding: utf-8 -*-
# Code mẫu — Decision tree

# Ví dụ 1: Tìm ngưỡng bằng Gini
import numpy as np

x = np.array([1., 2., 3., 4., 5., 6.])
y = np.array([0, 0, 1, 0, 1, 1])

def gini(labels):
    counts = np.bincount(labels, minlength=2)
    p = counts / len(labels)
    return 1.0 - np.sum(p ** 2)

parent = gini(y)
thresholds = (x[:-1] + x[1:]) / 2
gains = []
for threshold in thresholds:
    left = x <= threshold
    right = ~left
    weighted_after = left.mean() * gini(y[left]) + right.mean() * gini(y[right])
    gain = parent - weighted_after
    gains.append((float(threshold), float(gain)))
    print("t =", threshold, "gain =", round(float(gain), 3),
          "sizes =", int(left.sum()), int(right.sum()))

best_threshold, best_gain = max(gains, key=lambda item: item[1])
print("Gini cha:", round(float(parent), 3))
print("ngưỡng tốt nhất:", best_threshold, "gain:", round(best_gain, 3))
assert best_threshold == 2.5
assert np.isclose(best_gain, 0.25)

x_tied = np.array([1., 1., 2., 4.])
y_tied = np.array([0, 1, 1, 1])
all_midpoints = (x_tied[:-1] + x_tied[1:]) / 2
valid_midpoints = all_midpoints[x_tied[:-1] < x_tied[1:]]
print("mọi trung điểm:", all_midpoints.tolist())
print("ngưỡng tạo nhóm mới:", valid_midpoints.tolist())
assert np.allclose(valid_midpoints, [1.5, 3.0])


# Ví dụ 2: Giữ lại một tập để chọn độ sâu và mức cắt tỉa
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=180, n_features=5, n_informative=3, n_redundant=0,
    class_sep=0.75, flip_y=0.12, random_state=14
)
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=9
)

depth_rows = []
for depth in [1, 2, 3, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    depth_rows.append((depth, int(tree.get_n_leaves()),
                       accuracy_score(y_train, tree.predict(X_train)),
                       accuracy_score(y_valid, tree.predict(X_valid))))
print("depth / lá / train / valid:", [
    (d, leaves, round(train, 3), round(valid, 3))
    for d, leaves, train, valid in depth_rows
])

probe = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
path = probe.cost_complexity_pruning_path(X_train, y_train)
alphas = np.unique(path.ccp_alphas)
positions = np.linspace(0, len(alphas) - 1, num=min(7, len(alphas)), dtype=int)
alpha_candidates = alphas[positions]
pruned_rows = []
for alpha in alpha_candidates:
    tree = DecisionTreeClassifier(ccp_alpha=float(alpha), random_state=0).fit(
        X_train, y_train
    )
    pruned_rows.append((float(alpha), int(tree.get_n_leaves()),
                        accuracy_score(y_valid, tree.predict(X_valid))))
best_alpha, best_leaves, best_valid = max(pruned_rows, key=lambda row: row[2])
print("alpha / lá / valid:", [
    (round(alpha, 5), leaves, round(valid, 3))
    for alpha, leaves, valid in pruned_rows
])
print("alpha chọn:", round(best_alpha, 5),
      "lá:", best_leaves, "valid:", round(best_valid, 3))
assert 0.0 <= best_valid <= 1.0
assert best_leaves >= 1


# Ví dụ 3: Feature importance không chứng minh nguyên nhân
import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(17)
n = 160
gio_tu_hoc = rng.uniform(0., 10., n)
ma_ngau_nhien = rng.permutation(n) / n
y = (gio_tu_hoc + rng.normal(0., 1.6, n) > 5.0).astype(int)
X = np.column_stack([gio_tu_hoc, ma_ngau_nhien])
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=6
)

deep = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
constrained = DecisionTreeClassifier(max_depth=3, min_samples_leaf=8,
                                     random_state=0).fit(X_train, y_train)
for name, model in [("sâu", deep), ("giới hạn", constrained)]:
    print(name, "lá:", model.get_n_leaves(),
          "train:", round(accuracy_score(y_train, model.predict(X_train)), 3),
          "valid:", round(accuracy_score(y_valid, model.predict(X_valid)), 3))

permutation = permutation_importance(
    deep, X_valid, y_valid, n_repeats=10, random_state=0,
    scoring="accuracy", n_jobs=1
)
print("impurity:", deep.feature_importances_.round(3).tolist())
print("permutation valid:", permutation.importances_mean.round(3).tolist())
assert permutation.importances_mean.shape == (2,)
assert np.isfinite(permutation.importances_mean).all()

