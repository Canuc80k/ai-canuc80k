# -*- coding: utf-8 -*-
# Random forest — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

rng_boot = np.random.default_rng(7)
draw = rng_boot.integers(0, 5, size=5)
seen = np.unique(draw)
oob = np.setdiff1d(np.arange(5), seen)
print("rút:", draw.tolist())
print("đã thấy:", seen.tolist(), "OOB:", oob.tolist())
probabilities = np.array([0.9, 0.4, 0.4])
print("trung bình:", round(float(probabilities.mean()), 3))
print("phiếu lớp 1:", int(np.sum(probabilities > 0.5)))

# Bước 2
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
tree = DecisionTreeClassifier(random_state=0)
forest = RandomForestClassifier(n_estimators=80, oob_score=True, n_jobs=1, random_state=0)
print("một cây:", round(cross_val_score(tree, X, y, cv=5).mean(), 3))
print("rừng:   ", round(cross_val_score(forest, X, y, cv=5).mean(), 3))
print("OOB:    ", round(forest.fit(X, y).oob_score_, 3))
