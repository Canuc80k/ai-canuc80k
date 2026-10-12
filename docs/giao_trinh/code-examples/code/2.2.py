# -*- coding: utf-8 -*-
# Code mẫu — Regularization

# Ví dụ 1: Hệ số nhỏ bị co lại, hay bị bỏ hẳn?
import numpy as np

z = np.array([3., 0.5, -1.2])  # Bằng X.T @ y, khi X.T @ X là ma trận đơn vị.
for strength in [0.5, 1., 2.]:
    ridge_w = z / (1 + strength)
    lasso_w = np.sign(z) * np.maximum(np.abs(z) - strength, 0)
    print("lambda =", strength,
          "Ridge:", ridge_w.round(3).tolist(),
          "Lasso:", lasso_w.round(3).tolist())
assert np.allclose(np.sign(z) * np.maximum(np.abs(z) - 1, 0), [2., 0., -0.2])


# Ví dụ 2: Chỉ đổi km thành mét cũng làm đổi mức phạt
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X_km = np.array([[0.], [1.], [2.], [3.]])
y = np.array([0., 2., 4., 6.])
query_km = np.array([[1.5], [4.]])
scaled_predictions = []
for unit, factor in [("km", 1.), ("m", 1000.)]:
    X = X_km * factor
    raw = Ridge(alpha=5.).fit(X, y)
    pipeline = make_pipeline(StandardScaler(), Ridge(alpha=5.)).fit(X, y)
    prediction = pipeline.predict(query_km * factor)
    scaled_predictions.append(prediction)
    print(unit, "hệ số thô quy về mỗi km:", round(float(raw.coef_[0] * factor), 4))
    print(unit, "dự đoán có scaler:", prediction.round(4).tolist())
print("hai pipeline khớp:", np.allclose(*scaled_predictions))
assert np.allclose(*scaled_predictions)


# Ví dụ 3: Chọn Ridge hay Lasso khi bảng có nhiều cột nhiễu
import numpy as np
from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(22)
X = rng.normal(size=(120, 10))
y = 2 * X[:, 0] - X[:, 1] + rng.normal(0, 0.6, len(X))
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.25, random_state=3
)
folds = list(KFold(3, shuffle=True, random_state=5).split(X_dev))
searches = {}
for name, estimator, alphas in [
    ("Ridge", Ridge(), [0.1, 1., 10., 100.]),
    ("Lasso", Lasso(max_iter=10000), [0.01, 0.03, 0.1, 0.3]),
]:
    pipe = Pipeline([("scale", StandardScaler()), ("model", estimator)])
    # Scaler được fit lại trong từng fold. Không chuẩn hóa X_dev trước khi đưa vào GridSearchCV.
    search = GridSearchCV(pipe, {"model__alpha": alphas}, cv=folds,
                          scoring="neg_mean_squared_error", n_jobs=1)
    search.fit(X_dev, y_dev)
    searches[name] = search
    weights = search.best_estimator_["model"].coef_
    print(name, "alpha:", search.best_params_["model__alpha"],
          "CV MSE:", round(float(-search.best_score_), 4),
          "hệ số khác 0:", int(np.count_nonzero(weights)))
    print("hệ số:", weights.round(3).tolist())

chosen_name = max(searches, key=lambda name: searches[name].best_score_)
chosen = searches[chosen_name].best_estimator_
pred = chosen.predict(X_test)
baseline = np.full(len(y_test), y_dev.mean())
print("chọn bằng CV:", chosen_name)
print("test MSE baseline / mô hình:",
      round(mean_squared_error(y_test, baseline), 4),
      round(mean_squared_error(y_test, pred), 4))
print("train MSE:", round(mean_squared_error(y_dev, chosen.predict(X_dev)), 4))
print("4 cặp thật / dự đoán:", np.column_stack([y_test, pred])[:4].round(3).tolist())
assert chosen["scale"].n_samples_seen_ == len(X_dev)
assert pred.shape == y_test.shape and np.isfinite(pred).all()

