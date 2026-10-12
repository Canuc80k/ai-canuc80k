# -*- coding: utf-8 -*-
# Decision tree — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

def gini(labels):
    counts = np.bincount(labels, minlength=2)
    probabilities = counts / len(labels)
    return 1.0 - np.sum(probabilities ** 2)

x_small = np.array([1., 2., 3., 4.])
y_small = np.array([0, 0, 1, 1])
best = None
for threshold in [1.5, 2.5, 3.5]:
    left = x_small <= threshold
    right = ~left
    after = left.mean() * gini(y_small[left]) + right.mean() * gini(y_small[right])
    gain = gini(y_small) - after
    print(threshold, round(float(gain), 3))
    if best is None or gain > best[0]:
        best = (gain, threshold)
print("ngưỡng:", best[1])
assert best[1] == 2.5

# Bước 2
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text

X, y = load_breast_cancer(return_X_y=True)
for depth in [1, 3, 5, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0)
    print(depth, round(cross_val_score(tree, X, y, cv=5).mean(), 3))

tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
print(export_text(tree, feature_names=list(load_breast_cancer().feature_names)))
