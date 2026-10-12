# -*- coding: utf-8 -*-
# Code mẫu — k-Nearest Neighbors

# Ví dụ 1: Ba hồ sơ gần nhất bỏ phiếu ra sao?
import numpy as np

X = np.array([[1., 1.], [2., 1.], [4., 3.], [5., 4.], [3., 2.]])
y = np.array([0, 0, 1, 1, 1])
query = np.array([2., 2.])
distance2 = np.sum((X - query) ** 2, axis=1)
order = np.argsort(distance2, kind="stable")
neighbors = order[:3]
votes = np.bincount(y[neighbors], minlength=2)
print("d²:", distance2.tolist())
print("3 láng giềng:", neighbors.tolist(), "nhãn:", y[neighbors].tolist())
print("phiếu / dự đoán:", votes.tolist(), int(votes.argmax()))
print("k=1:", int(y[order[0]]), "hai điểm cùng gần nhất:", order[:2].tolist())
assert neighbors.tolist() == [1, 4, 0]

distance = np.array([1., 2.])
targets = np.array([0., 6.])
print("đều:", float(targets.mean()))
print("1/d:", round(float(np.average(targets, weights=1 / distance)), 3))
print("1/d²:", round(float(np.average(targets, weights=1 / distance**2)), 3))


# Ví dụ 2: Đổi giờ sang phút làm đổi luôn hàng xóm gần nhất
import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([[7., 5.], [8., 6.]])
query = np.array([[8., 5.2]])
scaled_distances = []
for unit, factor in [("giờ", 1.), ("phút", 60.)]:
    factors = np.array([1., factor])
    raw_distance = np.linalg.norm(X * factors - query * factors, axis=1)
    scaler = StandardScaler().fit(X * factors)
    Z = scaler.transform(X * factors)
    z_query = scaler.transform(query * factors)
    distance = np.linalg.norm(Z - z_query, axis=1)
    scaled_distances.append(distance)
    print(unit, "khoảng cách thô:", raw_distance.round(3).tolist(),
          "gần nhất:", int(raw_distance.argmin()))
    print(unit, "khoảng cách chuẩn hóa:", distance.round(3).tolist())
print("sau chuẩn hóa không đổi:", np.allclose(*scaled_distances))
assert np.allclose(*scaled_distances)


# Ví dụ 3: Chọn k cho dữ liệu rượu, trên cùng các fold
import numpy as np
from sklearn.datasets import load_wine
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=10
)
folds = list(StratifiedKFold(3, shuffle=True, random_state=6).split(X_dev, y_dev))
searches = {}
for name, scaler in [("thô", "passthrough"), ("chuẩn hóa", StandardScaler())]:
    pipeline = Pipeline([("scale", scaler), ("knn", KNeighborsClassifier())])
    search = GridSearchCV(pipeline, {"knn__n_neighbors": [1, 3, 5, 9]},
                          cv=folds, scoring="accuracy", n_jobs=1)
    search.fit(X_dev, y_dev)
    searches[name] = search
    print(name, "CV theo k=1,3,5,9:", search.cv_results_["mean_test_score"].round(3).tolist())
    print("k chọn:", search.best_params_["knn__n_neighbors"])

name = max(searches, key=lambda key: searches[key].best_score_)
chosen = searches[name].best_estimator_
pred = chosen.predict(X_test)
prob = chosen.predict_proba(X_test)
print("chọn bằng CV:", name)
print("test accuracy:", round(accuracy_score(y_test, pred), 3))
print("confusion matrix, hàng=thật, cột=đoán:")
print(confusion_matrix(y_test, pred, labels=[0, 1, 2]))
print("3 hàng xác suất:", prob[:3].round(3).tolist())
assert np.allclose(prob.sum(axis=1), 1.)
assert pred.shape == y_test.shape

