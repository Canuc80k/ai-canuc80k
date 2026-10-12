# -*- coding: utf-8 -*-
# Code mẫu — Clustering

# Ví dụ 1: Một vòng K-Means với khởi tạo lệch
import numpy as np

X = np.array([[1.], [2.], [9.], [10.], [11.]])
centers = np.array([[1.], [2.]])
for step in range(3):
    # Ma trận n×k: hàng i là khoảng cách bình phương từ điểm i tới từng tâm.
    distance2 = np.sum((X[:, None, :] - centers[None, :, :])**2, axis=2)
    labels = distance2.argmin(axis=1)
    before = float(distance2[np.arange(len(X)), labels].sum())
    new_centers = centers.copy()
    for cluster in range(len(centers)):
        members = X[labels == cluster]
        if len(members):
            new_centers[cluster] = members.mean(axis=0)
        # Cụm rỗng thì giữ tâm cũ, để khỏi lấy trung bình của mảng rỗng ra NaN.
    after = float(np.sum((X - new_centers[labels])**2))
    print("vòng", step + 1, "nhãn:", labels.tolist(),
          "tâm mới:", new_centers.ravel().round(3).tolist(),
          "inertia:", round(before, 3), "->", round(after, 3))
    assert after <= before + 1e-12
    centers = new_centers


# Ví dụ 2: Một điểm ít hàng xóm vẫn có thể thuộc cụm
import numpy as np
from sklearn.cluster import DBSCAN

X = np.array([[0.], [0.1], [0.2], [0.35], [3.]])
for eps in [0.16, 0.08]:
    distance = np.abs(X - X.T)
    counts = (distance <= eps).sum(axis=1)
    model = DBSCAN(eps=eps, min_samples=3).fit(X)
    core = np.zeros(len(X), dtype=bool)
    core[model.core_sample_indices_] = True
    kinds = ["core" if core[i] else "noise" if model.labels_[i] == -1 else "border"
             for i in range(len(X))]
    print("eps =", eps, "số hàng xóm:", counts.tolist())
    print("nhãn:", model.labels_.tolist(), "loại:", kinds)
    assert np.array_equal(core, counts >= 3)


# Ví dụ 3: Đổi đơn vị làm đổi cách chia nhóm
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler

X = np.array([[0., 0.], [0., 1.], [10., 0.], [10., 1.]])
raw_partitions, scaled_partitions = [], []
for unit, factor in [("m²", 1.), ("cm²", 10000.)]:
    measured = X * np.array([1., factor])
    raw = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(measured)
    scaled = StandardScaler().fit_transform(measured)
    normalized = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(scaled)
    raw_partitions.append(raw)
    scaled_partitions.append(normalized)
    print(unit, "nhãn thô / chuẩn hóa:", raw.tolist(), normalized.tolist())
print("ARI giữa hai thang thô:", round(adjusted_rand_score(*raw_partitions), 3))
print("ARI giữa hai thang chuẩn hóa:", round(adjusted_rand_score(*scaled_partitions), 3))
assert adjusted_rand_score(*scaled_partitions) == 1.


# Ví dụ 4: Hai dải cong và hai cách chấm điểm
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

X, reference = make_moons(n_samples=240, noise=0.045, random_state=30)
Z = StandardScaler().fit_transform(X)
models = [
    ("K-Means", KMeans(n_clusters=2, n_init=10, random_state=0)),
    ("DBSCAN", DBSCAN(eps=0.28, min_samples=5)),
]
for name, model in models:
    labels = model.fit_predict(Z)
    retained = labels != -1
    clusters = len(set(labels[retained]))
    print(name, "số cụm / số noise:", clusters, int((~retained).sum()),
          "ARI toàn bộ:", round(adjusted_rand_score(reference, labels), 3))
    if 2 <= clusters < retained.sum():
        # Bỏ các điểm noise khi tính silhouette, và ghi rõ đã chấm trên tập nào.
        silhouette = silhouette_score(Z[retained], labels[retained])
        print("silhouette trên điểm không-noise:", round(silhouette, 3))
    else:
        print("silhouette: chưa đủ điều kiện")

