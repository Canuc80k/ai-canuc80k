# -*- coding: utf-8 -*-
# Code mẫu — SVM

# Ví dụ 1: Score, khoảng cách và hinge loss
import numpy as np

w = np.array([3., 4.])
b = -10.
points = np.array([[2., 1.], [3., 2.], [2., 1.1]])
y_signed = np.array([1., 1., 1.])
scores = points @ w + b
distances = np.abs(scores) / np.linalg.norm(w)
hinge = np.maximum(0., 1. - y_signed * scores)
print("score:", scores.round(3).tolist())
print("khoảng cách:", distances.round(3).tolist())
print("hinge:", hinge.round(3).tolist())
assert np.allclose(scores, [0., 7., 0.4])
assert np.allclose(distances, [0., 1.4, 0.08])
assert np.allclose(hinge, [1., 0., 0.6])

scores_check = np.array([0.4, -0.2])
y01 = np.array([1., 0.])
y_signed_check = np.array([1., -1.])
wrong = np.maximum(0., 1. - y01 * scores_check)
correct = np.maximum(0., 1. - y_signed_check * scores_check)
print("hinge dùng 0/1:", wrong.round(3).tolist())
print("hinge đổi sang -1/+1:", correct.round(3).tolist())
assert np.allclose(wrong, [0.6, 1.0])
assert np.allclose(correct, [0.6, 0.8])


# Ví dụ 2: Biên thẳng và biên cong nhờ kernel
import numpy as np
from sklearn.datasets import make_moons
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_moons(n_samples=180, noise=0.22, random_state=4)
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=2
)
for kernel in ["linear", "rbf"]:
    model = make_pipeline(
        StandardScaler(), SVC(kernel=kernel, C=1., gamma="scale")
    ).fit(X_train, y_train)
    svc = model[-1]
    score = model.decision_function(X_valid[:3])
    print(kernel, "valid:", round(accuracy_score(y_valid, model.predict(X_valid)), 3),
          "support:", int(svc.n_support_.sum()),
          "score 3 điểm:", np.round(score, 3).tolist())
    assert svc.n_support_.sum() > 0

x_kernel = np.array([1., 2.])
z_kernel = np.array([3., 4.])

def phi2(v):
    a, b = v
    return np.array([a * a, np.sqrt(2.) * a * b, b * b])

expanded = phi2(x_kernel) @ phi2(z_kernel)
kernel_value = (x_kernel @ z_kernel) ** 2
print("dot trong không gian mở rộng:", round(float(expanded), 3))
print("kernel (x · z)^2:", round(float(kernel_value), 3))
assert np.isclose(expanded, kernel_value)


# Ví dụ 3: Chuẩn hóa và dò gamma trên validation
import numpy as np
from sklearn.datasets import make_moons
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_moons(n_samples=240, noise=0.24, random_state=6)
X = X * np.array([1., 100.])
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=7
)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_dev, y_dev, test_size=0.25, stratify=y_dev, random_state=3
)

raw = SVC(kernel="rbf", C=2., gamma=1.).fit(X_train, y_train)
scaled = make_pipeline(
    StandardScaler(), SVC(kernel="rbf", C=2., gamma=1.)
).fit(X_train, y_train)
print("RBF thô valid:", round(accuracy_score(y_valid, raw.predict(X_valid)), 3))
print("RBF có scaler valid:", round(accuracy_score(y_valid, scaled.predict(X_valid)), 3))

gamma_rows = []
for gamma in [0.1, 1., 10.]:
    candidate = make_pipeline(
        StandardScaler(), SVC(kernel="rbf", C=2., gamma=gamma)
    ).fit(X_train, y_train)
    valid_accuracy = accuracy_score(y_valid, candidate.predict(X_valid))
    gamma_rows.append((gamma, float(valid_accuracy), int(candidate[-1].n_support_.sum())))
    print("gamma =", gamma, "valid:", round(float(valid_accuracy), 3),
          "support:", int(candidate[-1].n_support_.sum()))

best_gamma, _, _ = max(gamma_rows, key=lambda row: row[1])
chosen = make_pipeline(
    StandardScaler(), SVC(kernel="rbf", C=2., gamma=best_gamma)
).fit(X_dev, y_dev)
test_accuracy = accuracy_score(y_test, chosen.predict(X_test))
print("gamma chọn:", best_gamma, "test sau khi khóa:", round(float(test_accuracy), 3))
assert best_gamma in {0.1, 1.0, 10.0}

