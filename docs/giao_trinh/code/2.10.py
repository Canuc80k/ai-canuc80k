# -*- coding: utf-8 -*-
# Clustering — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

values = np.array([[0.], [1.], [5.], [6.]])
centers = np.array([[0.], [6.]])
distance2 = np.sum((values[:, None, :] - centers[None, :, :]) ** 2, axis=2)
assigned = np.argmin(distance2, axis=1)
before = np.sum(distance2[np.arange(len(values)), assigned])
new_centers = np.array([values[assigned == k].mean(axis=0) for k in range(2)])
after = np.sum((values - new_centers[assigned]) ** 2)
print("gán:", assigned.tolist())
print("tâm mới:", new_centers.ravel().tolist())
print("inertia:", float(before), "->", float(after))

# Bước 2
from sklearn.cluster import DBSCAN

density_points = np.array([[0.], [0.1], [0.2], [0.35], [3.]])
db = DBSCAN(eps=0.16, min_samples=3).fit(density_points)
print("nhãn cụm:", db.labels_.tolist())
print("core:", db.core_sample_indices_.tolist())
assert db.labels_[-1] == -1

# Bước 3
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

X, y = make_moons(n_samples=400, noise=0.06, random_state=0)
X = StandardScaler().fit_transform(X)
for name, model in [("K-Means", KMeans(n_clusters=2, n_init=10, random_state=0)),
                    ("DBSCAN ", DBSCAN(eps=0.3, min_samples=5))]:
    labels = model.fit_predict(X)
    print(name, "ARI =", round(adjusted_rand_score(y, labels), 2),
          " silhouette =", round(silhouette_score(X, labels), 2))
