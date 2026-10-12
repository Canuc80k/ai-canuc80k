# -*- coding: utf-8 -*-
# Code mẫu — Logistic regression và softmax

# Ví dụ 1: Tăng trọng số để sửa một email bị đoán thấp
import numpy as np

def sigmoid(z):
    # Không tính thẳng exp(-z), vì khi z rất âm thì exp(-z) sẽ tràn số.
    return np.exp(-np.logaddexp(0., -np.asarray(z)))

x, target = 2., 1.
w, bias = 1., -1.
logit = w * x + bias
probability = float(sigmoid(logit))
loss = float(np.logaddexp(0., logit) - target * logit)
gradient_w = (probability - target) * x
new_w = w - 0.5 * gradient_w
new_logit = new_w * x + bias
print("logit / xác suất / loss:", round(logit, 4), round(probability, 4), round(loss, 4))
print("gradient w:", round(gradient_w, 4), "w mới:", round(new_w, 4))
print("xác suất / loss mới:", round(float(sigmoid(new_logit)), 4),
      round(float(np.logaddexp(0., new_logit) - target * new_logit), 4))
extreme = np.array([-1000., 0., 1000.])
print("sigmoid ở logits lớn:", sigmoid(extreme).round(3).tolist())
assert gradient_w < 0 and float(sigmoid(new_logit)) > probability


# Ví dụ 2: Cùng một xác suất, đổi ngưỡng chặn thư
import numpy as np
from sklearn.linear_model import LogisticRegression

X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1],
                    [1, 3], [2, 2], [3, 1], [3, 3], [4, 2], [4, 4]], dtype=float)
y_train = np.array([0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1])
X_valid = np.array([[0, 2], [1, 2], [2, 1], [2, 3], [3, 0], [4, 3]], dtype=float)
y_valid = np.array([0, 0, 1, 1, 0, 1])
model = LogisticRegression(C=1., max_iter=500).fit(X_train, y_train)
spam_column = int(np.flatnonzero(model.classes_ == 1)[0])
probabilities = model.predict_proba(X_valid)[:, spam_column]
print("classes_:", model.classes_.tolist())
print("(nhãn, P(spam)):", list(zip(y_valid.tolist(), probabilities.round(3).tolist())))
for threshold in [0.3, 0.5, 0.8]:
    blocked = probabilities >= threshold
    false_positive = int(np.sum(blocked & (y_valid == 0)))
    false_negative = int(np.sum(~blocked & (y_valid == 1)))
    print("ngưỡng", threshold, "chặn nhầm:", false_positive,
          "lọt spam:", false_negative, "chi phí:", 5 * false_positive + false_negative)


# Ví dụ 3: Ba chủ đề với logits rất lớn
import numpy as np

def log_softmax(logits):
    shifted = logits - logits.max(axis=1, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))

logits = np.array([[2., 1., 0.], [0., 1., 2.]])
labels = np.array([1, 2])  # Chỉ số của lớp đúng ở từng văn bản.
log_prob = log_softmax(logits)
prob = np.exp(log_prob)
print("xác suất:", prob.round(4).tolist())
print("tổng từng hàng:", prob.sum(axis=1).round(4).tolist())
print("cộng 1000 không đổi:", np.allclose(log_prob, log_softmax(logits + 1000)))
print("loss từng mẫu:", (-log_prob[np.arange(len(labels)), labels]).round(4).tolist())
one_hot = np.eye(3)[labels]
gradient = (prob - one_hot) / len(labels)  # Gradient của cross-entropy trung bình theo logits.
print("gradient logits:", gradient.round(4).tolist())
print("tổng gradient mỗi hàng:", gradient.sum(axis=1).round(6).tolist())
assert np.allclose(prob.sum(axis=1), 1.)
assert np.allclose(gradient.sum(axis=1), 0.)


# Ví dụ 4: Từ số đo bông hoa tới xác suất của ba loài
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.3, stratify=data.target, random_state=8
)
pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))
pipeline.fit(X_train, y_train)
classifier = pipeline[-1]
prob = pipeline.predict_proba(X_test)
chosen_labels = classifier.classes_[np.argmax(prob, axis=1)]
print("cột xác suất:", data.target_names[classifier.classes_].tolist())
print("3 hàng xác suất:", prob[:3].round(3).tolist())
print("3 nhãn thật / đoán:", y_test[:3].tolist(), chosen_labels[:3].tolist())
print("accuracy / log loss:", round(accuracy_score(y_test, chosen_labels), 3),
      round(log_loss(y_test, prob, labels=classifier.classes_), 3))
print("shape / tổng hàng hợp lệ:", prob.shape, np.allclose(prob.sum(axis=1), 1.))
assert np.array_equal(chosen_labels, pipeline.predict(X_test))

