# -*- coding: utf-8 -*-
# Code mẫu — Bài tập lý thuyết

# Ví dụ 1: Bắt được 80% bài lỗi không có nghĩa 80% cảnh báo là đúng
import numpy as np
from sklearn.metrics import precision_score, recall_score

tp, fn, fp, tn = 8, 2, 18, 72
prior = (tp + fn) / (tp + fn + fp + tn)
sensitivity = tp / (tp + fn)
false_alarm = fp / (fp + tn)
alarm = prior * sensitivity + (1 - prior) * false_alarm
posterior = prior * sensitivity / alarm
labels = np.array([1] * 10 + [0] * 90)
predicted = np.array([1] * 8 + [0] * 2 + [1] * 18 + [0] * 72)
assert np.isclose(posterior, precision_score(labels, predicted))
assert np.isclose(sensitivity, recall_score(labels, predicted))
print("P(cảnh báo | lỗi):", f"{sensitivity:.4f}")
print("P(lỗi | cảnh báo):", f"{posterior:.4f}")
print("kiểm bằng đếm:", tp, "/", tp + fp)

# Chỉ đổi tỉ lệ bài lỗi. Khả năng bắt lỗi và tỉ lệ báo nhầm giữ nguyên.
new_prior = 0.5
new_posterior = new_prior * sensitivity / (
    new_prior * sensitivity + (1 - new_prior) * false_alarm)
print("nếu P(lỗi)=0.5, posterior:", f"{new_posterior:.4f}")


# Ví dụ 2: Nhãn giống nhau, mức tự tin khác nhau
import numpy as np
from sklearn.metrics import accuracy_score, log_loss

y = np.array([0, 1, 1, 0])
models = {"A": np.array([0.1, 0.9, 0.4, 0.6]),
          "B": np.array([0.01, 0.99, 0.01, 0.99])}
for name, p in models.items():
    per_row = -y * np.log(p) - (1 - y) * np.log1p(-p)
    library_loss = log_loss(y, np.column_stack([1 - p, p]), labels=[0, 1])
    assert np.isclose(per_row.mean(), library_loss)
    print(name, "loss từng mẫu:", per_row.round(4).tolist())
    print("accuracy:", f"{accuracy_score(y, p >= 0.5):.2f}",
          "mean loss (nats):", f"{library_loss:.4f}")
assert np.array_equal(models["A"] >= 0.5, models["B"] >= 0.5)

q = 0.25
expected = lambda p: -q * np.log(p) - (1 - q) * np.log1p(-p)
print("dự đoán cố định, loss kỳ vọng tại p=q / p=0.5:",
      f"{expected(q):.4f}", f"{expected(0.5):.4f}")
assert expected(q) < expected(0.5)


# Ví dụ 3: Gradient có cả hệ số trung bình lẫn regularization
import numpy as np
import torch

torch.set_num_threads(1)
torch.manual_seed(93)
X = np.array([[1.0, 2.0], [2.0, -1.0]])
y = np.array([1.0, 0.0])
theta = np.array([0.2, -0.1, 0.0])  # Hai trọng số, rồi tới bias.
penalty = 0.1

def loss(parameters):
    z = X @ parameters[:2] + parameters[2]
    return np.mean(np.logaddexp(0.0, z) - y * z) + penalty * np.sum(parameters[:2] ** 2)

z = X @ theta[:2] + theta[2]
p = 1 / (1 + np.exp(-z))
gradient = np.append(X.T @ (p - y) / len(y) + 2 * penalty * theta[:2],
                     np.mean(p - y))
epsilon = 1e-5
numerical = []
for column in range(len(theta)):
    shift = np.zeros_like(theta)
    shift[column] = epsilon
    numerical.append((loss(theta + shift) - loss(theta - shift)) / (2 * epsilon))

parameters = torch.tensor(theta, dtype=torch.float64, requires_grad=True)
features = torch.tensor(X, dtype=torch.float64)
labels = torch.tensor(y, dtype=torch.float64)
logits = features @ parameters[:2] + parameters[2]
torch_loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
torch_loss = torch_loss + penalty * parameters[:2].square().sum()
torch_loss.backward()
assert np.allclose(gradient, numerical, rtol=0, atol=1e-8)
assert np.allclose(gradient, parameters.grad.numpy(), rtol=0, atol=1e-12)
print("gradient (w0,w1,b):", gradient.round(6).tolist())
print("hai phép kiểm khớp:", True)
for learning_rate in [0.1, 20.0]:
    updated = theta - learning_rate * gradient
    print("lr:", learning_rate, "loss:", f"{loss(theta):.4f}", "->", f"{loss(updated):.4f}")
assert loss(theta - 0.1 * gradient) < loss(theta)
assert loss(theta - 20.0 * gradient) > loss(theta)
large_step = theta - 20.0 * gradient
large_logits = X @ large_step[:2] + large_step[2]
data_loss = np.mean(np.logaddexp(0.0, large_logits) - y * large_logits)
l2_loss = penalty * np.sum(large_step[:2] ** 2)
print("lr=20, data loss / L2:", f"{data_loss:.6f}", f"{l2_loss:.6f}")

