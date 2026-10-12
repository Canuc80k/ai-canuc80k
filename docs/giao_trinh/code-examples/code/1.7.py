# -*- coding: utf-8 -*-
# Code mẫu — Hyperparameter tuning

# Ví dụ 1: Đếm ngân sách, và loại trước những cấu hình không chạy được
import numpy as np
from sklearn.model_selection import ParameterGrid
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression

grid = {"n_neighbors": [1, 3, 5], "weights": ["uniform", "distance"]}
configs = list(ParameterGrid(grid))
print("Số cấu hình:", len(configs))
print("Số fit với 3 fold và refit:", 3 * len(configs) + 1)

X_train = np.array([[0.0], [1.0], [2.0], [3.0]])
y_train = np.array([1.0, 3.0, 5.0, 7.0])
linear = LinearRegression().fit(X_train, y_train)
print("Hệ số được fit học:", np.round(linear.coef_, 2).tolist())
bad_k = 5
try:
    if bad_k > len(X_train):
        raise ValueError(f"k={bad_k} vượt {len(X_train)} mẫu train")
    KNeighborsRegressor(n_neighbors=bad_k).fit(X_train, y_train).predict([[1.5]])
except ValueError as error:
    print("Kiểm trước khi chạy:", error)


# Ví dụ 2: Grid search, với cả Pipeline chạy lại trong mỗi fold
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score, confusion_matrix

X, y = load_iris(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=30, stratify=y, random_state=71,
)
folds = list(StratifiedKFold(n_splits=3, shuffle=True, random_state=71).split(X_dev, y_dev))
pipeline = Pipeline([
    ("scale", StandardScaler()),
    ("knn", KNeighborsClassifier()),
])
parameters = {"knn__n_neighbors": [1, 5, 15], "knn__weights": ["uniform", "distance"]}
assert max(parameters["knn__n_neighbors"]) <= min(len(train_ids) for train_ids, _ in folds)
search = GridSearchCV(
    pipeline, parameters, scoring="f1_macro", cv=folds,
    return_train_score=True, refit=True, error_score="raise", n_jobs=1,
)
search.fit(X_dev, y_dev)
log = search.cv_results_
for params, train, valid in zip(log["params"], log["mean_train_score"], log["mean_test_score"]):
    print(f"k={params['knn__n_neighbors']:2d}, {params['knn__weights']:8s}: train F1={train:.3f}, CV F1={valid:.3f}")
print("Cấu hình chốt bằng CV:", search.best_params_)

prediction = search.best_estimator_.predict(X_test)
print(f"Test macro-F1={f1_score(y_test, prediction, average='macro'):.3f}")
print(confusion_matrix(y_test, prediction, labels=[0, 1, 2]))
print("Scaler refit dùng số mẫu:", int(search.best_estimator_.named_steps["scale"].n_samples_seen_))


# Ví dụ 3: Random search thử ít hơn trên cùng vùng
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score

X, y = load_iris(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=30, stratify=y, random_state=72,
)
folds = list(StratifiedKFold(n_splits=3, shuffle=True, random_state=72).split(X_dev, y_dev))
pipeline = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier())])
region = {"knn__n_neighbors": [1, 5, 15], "knn__weights": ["uniform", "distance"]}
grid = GridSearchCV(pipeline, region, scoring="f1_macro", cv=folds, n_jobs=1, error_score="raise")
random = RandomizedSearchCV(
    pipeline, region, n_iter=3, scoring="f1_macro", cv=folds,
    random_state=72, n_jobs=1, error_score="raise",
)
for name, search in [("grid", grid), ("random", random)]:
    search.fit(X_dev, y_dev)
    candidates = len(search.cv_results_["params"])
    print(f"{name}: ứng viên={candidates}, fit={3*candidates+1}, best CV F1={search.best_score_:.3f}")
    print("  Chọn:", search.best_params_)
chosen_name, chosen = ("grid", grid) if grid.best_score_ >= random.best_score_ else ("random", random)
print("Chốt trước test:", chosen_name)
prediction = chosen.best_estimator_.predict(X_test)
print(f"Test macro-F1={f1_score(y_test, prediction, average='macro'):.3f}")

