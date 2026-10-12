# -*- coding: utf-8 -*-
# Dimensionality reduction — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
from sklearn.decomposition import PCA

X_pca = np.array([[-2., -1.], [-1., -1.], [1., 1.], [2., 1.]])
center = X_pca.mean(axis=0)
X_centered = X_pca - center
U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)
components = Vt[:1].T
coordinates = X_centered @ components
reconstructed = coordinates @ components.T + center
ratio = s[0] ** 2 / np.sum(s ** 2)
library = PCA(n_components=1).fit(X_pca)
print("shape:", components.shape, coordinates.shape, reconstructed.shape)
print("tỉ lệ:", round(float(ratio), 4))
print("MSE tái tạo:", round(float(np.mean((reconstructed - X_pca) ** 2)), 6))
print("khớp tái tạo:", np.allclose(reconstructed, library.inverse_transform(library.transform(X_pca))))

# Bước 2
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X, y = load_digits(return_X_y=True)          # 1797 ảnh 8×8 = 64 chiều
for name, data in [("thô", X), ("chuẩn hóa", StandardScaler().fit_transform(X))]:
    pca = PCA().fit(data)
    k = np.searchsorted(np.cumsum(pca.explained_variance_ratio_), 0.95) + 1
    print(f"{name}: cần {k} trên 64 thành phần để giữ 95% phương sai")
