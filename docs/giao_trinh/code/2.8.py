# -*- coding: utf-8 -*-
# SVM — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

w_margin = np.array([3., 4.])
b_margin = -10.
points_margin = np.array([[2., 1.], [3., 2.], [2., 1.1]])
labels_signed = np.array([1., 1., 1.])
scores = points_margin @ w_margin + b_margin
distances = np.abs(scores) / np.linalg.norm(w_margin)
hinge = np.maximum(0., 1. - labels_signed * scores)
print("score:", scores.round(3).tolist())
print("khoảng cách:", distances.round(3).tolist())
print("hinge:", hinge.round(3).tolist())

# Bước 2
x_kernel = np.array([1., 2.])
z_kernel = np.array([3., 4.])
def phi2(v):
    a, b = v
    return np.array([a * a, np.sqrt(2.) * a * b, b * b])

print(round(float(phi2(x_kernel) @ phi2(z_kernel)), 6))
print(float((x_kernel @ z_kernel) ** 2))
assert np.allclose(phi2(x_kernel) @ phi2(z_kernel), (x_kernel @ z_kernel) ** 2)

# Bước 3
from sklearn.datasets import make_moons
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_moons(n_samples=500, noise=0.25, random_state=0)
model = make_pipeline(StandardScaler(), SVC(kernel="rbf"))
grid = GridSearchCV(model, {"svc__C": [0.1, 1, 10, 100], "svc__gamma": [0.01, 0.1, 1, 10]}, cv=5)
grid.fit(X, y)
print(grid.best_params_, round(grid.best_score_, 3))
print("số vector hỗ trợ:", grid.best_estimator_[-1].n_support_.sum(), "trên", len(X))
