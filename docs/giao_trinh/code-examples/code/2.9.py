# -*- coding: utf-8 -*-
# Code mẫu — Dimensionality reduction

# Ví dụ 1: Nén hai phép đo thành một tọa độ
import numpy as np
from sklearn.decomposition import PCA

X = np.array([[1., 1.], [2., 2.], [3., 2.], [4., 3.]])
mean = X.mean(axis=0)
centered = X - mean
_, singular_values, Vt = np.linalg.svd(centered, full_matrices=False)
direction = Vt[0].copy()
if direction[0] < 0:  # Lật dấu cho dễ đối chiếu. Hướng ngược dấu vẫn là cùng một trục.
    direction *= -1
coordinates = centered @ direction[:, None]
reconstructed = coordinates @ direction[None, :] + mean
variance_ratio = singular_values[0]**2 / np.sum(singular_values**2)
library = PCA(n_components=1, svd_solver="full").fit(X)
print("mean / hướng:", mean.round(3).tolist(), direction.round(3).tolist())
print("shape tọa độ / tái tạo:", coordinates.shape, reconstructed.shape)
print("tọa độ:", coordinates.ravel().round(3).tolist())
print("tái tạo:", reconstructed.round(3).tolist())
print("variance giữ / MSE tái tạo:", round(float(variance_ratio), 4),
      round(float(np.mean((X - reconstructed)**2)), 4))
print("khớp thư viện:", np.allclose(
    reconstructed, library.inverse_transform(library.transform(X))
))
assert np.allclose(reconstructed, library.inverse_transform(library.transform(X)))


# Ví dụ 2: Giữ gần hết phương sai mà vẫn mất sạch thông tin về nhãn
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

X_train = np.array([[large, small] for large in [-12., -4., 4., 12.]
                   for small in [-0.1, 0.1]])
y_train = (X_train[:, 1] > 0).astype(int)
X_valid = np.array([[large, small] for large in [-10., -2., 2., 10.]
                   for small in [-0.1, 0.1]])
y_valid = (X_valid[:, 1] > 0).astype(int)
for dimensions in [1, 2]:
    model = make_pipeline(PCA(n_components=dimensions, svd_solver="full"),
                          LogisticRegression(C=1000., max_iter=500))
    model.fit(X_train, y_train)
    pca = model[0]
    print("k =", dimensions,
          "variance giữ:", round(float(pca.explained_variance_ratio_.sum()), 6),
          "validation accuracy:", round(float(model.score(X_valid, y_valid)), 3))
    print("nhãn đoán:", model.predict(X_valid).tolist())
assert np.isclose(X_train[:, 0].var(), 80.)
assert np.isclose(X_train[:, 1].var(), 0.01)


# Ví dụ 3: Chọn số chiều cho ảnh chữ số bằng Pipeline
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline

data = load_digits()
selected = np.random.default_rng(29).permutation(len(data.target))[:700]
X, y = data.data[selected] / 16., data.target[selected]
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=2
)
pipeline = Pipeline([
    ("pca", PCA(svd_solver="full")),
    ("classifier", LogisticRegression(max_iter=500)),
])
folds = StratifiedKFold(3, shuffle=True, random_state=3)
search = GridSearchCV(pipeline, {"pca__n_components": [8, 16, 32]},
                      cv=folds, scoring="accuracy", n_jobs=1)
search.fit(X_dev, y_dev)
print("CV accuracy cho 8,16,32 chiều:",
      search.cv_results_["mean_test_score"].round(3).tolist())
print("số chiều chọn:", search.best_params_["pca__n_components"])

chosen = search.best_estimator_
pca = chosen["pca"]
compressed = pca.transform(X_test)
restored = pca.inverse_transform(compressed)
pred = chosen.predict(X_test)
print("shape trước / sau:", X_test.shape, compressed.shape)
print("variance giữ trên train:", round(float(pca.explained_variance_ratio_.sum()), 3))
print("test accuracy:", round(accuracy_score(y_test, pred), 3))
print("4 nhãn thật / đoán:", y_test[:4].tolist(), pred[:4].tolist())
print("MSE tái tạo test:", round(float(np.mean((X_test - restored)**2)), 5))
assert pca.n_samples_ == len(X_dev)
assert compressed.shape[1] == search.best_params_["pca__n_components"]

