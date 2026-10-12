# -*- coding: utf-8 -*-
# Code mẫu — Classification metrics

# Ví dụ 1: Một hệ thống cảnh báo đang bỏ sót ai?
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

y = np.array([0, 1, 0, 1, 0, 0, 1, 0])
score = np.array([0.1, 0.9, 0.7, 0.6, 0.4, 0.2, 0.3, 0.8])
prediction = score >= 0.5
cm = confusion_matrix(y, prediction, labels=[0, 1])
tn, fp, fn, tp = cm.ravel()          # Hàng là nhãn thật, cột là nhãn dự đoán.
assert (tn, fp, fn, tp) == (3, 2, 1, 2)
print(cm)
print(f"Precision={precision_score(y, prediction):.3f}, recall={recall_score(y, prediction):.3f}, F1={f1_score(y, prediction):.3f}")

rare_y = np.array([1, 1] + [0] * 18)
always_zero = np.zeros(len(rare_y), dtype=int)
print(f"Luôn đoán 0: accuracy={accuracy_score(rare_y, always_zero):.2f}, recall={recall_score(rare_y, always_zero):.2f}")


# Ví dụ 2: Chọn ngưỡng trên validation, rồi giữ nguyên khi chấm test
import numpy as np
from sklearn.metrics import f1_score, confusion_matrix

y_valid = np.array([0, 1, 0, 1, 0, 0, 1, 0])
p_valid = np.array([0.1, 0.9, 0.7, 0.6, 0.4, 0.2, 0.3, 0.8])
thresholds = [0.3, 0.5, 0.7]
scores = []
for threshold in thresholds:
    prediction = p_valid >= threshold    # Score bằng đúng ngưỡng cũng được tính là dương.
    score = f1_score(y_valid, prediction, zero_division=0)
    scores.append(score)
    print(f"t={threshold:.1f}: cảnh báo={int(prediction.sum())}, valid F1={score:.3f}")
chosen = thresholds[int(np.argmax(scores))]
print("Ngưỡng chốt bằng validation:", chosen)

y_test = np.array([1, 0, 1, 0, 0, 1])
p_test = np.array([0.8, 0.2, 0.4, 0.35, 0.1, 0.25])
test_prediction = p_test >= chosen
print(f"Test F1={f1_score(y_test, test_prediction):.3f}")
print(confusion_matrix(y_test, test_prediction, labels=[0, 1]))


# Ví dụ 3: Xếp đúng thứ tự khác với tự tin đúng mức
import numpy as np
from sklearn.metrics import roc_auc_score, log_loss

y = np.array([1, 0, 1, 0])
p = np.array([0.8, 0.8, 0.4, 0.2])
positive = p[y == 1]
negative = p[y == 0]
points = (positive[:, None] > negative[None, :]).astype(float)
points += 0.5 * (positive[:, None] == negative[None, :])
print("Điểm bốn cặp:", points.ravel().tolist())
print(f"AUC tính tay={points.mean():.3f}, thư viện={roc_auc_score(y, p):.3f}")
for name, probability in [("gốc", p), ("bình phương", p ** 2)]:
    print(f"{name}: AUC={roc_auc_score(y, probability):.3f}, log loss={log_loss(y, probability):.3f}")


# Ví dụ 4: Đọc lỗi của một classifier ba lớp
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score

iris = load_iris()
X_train, X_valid, y_train, y_valid = train_test_split(
    iris.data, iris.target, test_size=30, stratify=iris.target, random_state=51,
)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300))
model.fit(X_train, y_train)
prediction = model.predict(X_valid)
classifier = model.named_steps["logisticregression"]
probability = model.predict_proba(X_valid)
assert np.allclose(probability.sum(axis=1), 1)
assert classifier.classes_.tolist() == [0, 1, 2]
print("Thứ tự lớp:", iris.target_names[classifier.classes_].tolist())
print(confusion_matrix(y_valid, prediction, labels=classifier.classes_))
print("F1 từng lớp:", np.round(f1_score(y_valid, prediction, average=None), 3).tolist())
print(f"Macro-F1={f1_score(y_valid, prediction, average='macro'):.3f}")

