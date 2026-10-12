# -*- coding: utf-8 -*-
# Bài tập lý thuyết — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

tp, fn, fp, tn = 18, 2, 98, 882
total = tp + fn + fp + tn
prior = (tp + fn) / total
sensitivity = tp / (tp + fn)
false_alarm_rate = fp / (fp + tn)
alarm_probability = sensitivity * prior + false_alarm_rate * (1 - prior)
posterior = sensitivity * prior / alarm_probability
print(f"P(lỗi)={prior:.4f}, P(cảnh báo)={alarm_probability:.4f}")
print(f"P(lỗi | cảnh báo)={posterior:.4f}")
assert np.isclose(posterior, tp / (tp + fp))

# Bước 2
def expected_log_loss(q, p):
    return -q * np.log(p) - (1 - q) * np.log(1 - p)

q = 0.02
print(f"E[Y]={q:.4f}, Var(Y)={q * (1 - q):.4f}")
print(f"y=1: loss tại p=0.8 là {-np.log(0.8):.4f}; tại p=0.2 là {-np.log(0.2):.4f}")
print(f"E[loss] tại p=0.02: {expected_log_loss(q, 0.02):.4f}")
print(f"E[loss] tại p=0.50: {expected_log_loss(q, 0.50):.4f}")
assert expected_log_loss(q, q) < expected_log_loss(q, 0.5)

# Bước 3
X = np.array([[1.0, 2.0], [3.0, 4.0]])
w_linear = np.array([2.0, -1.0])
b_linear = 1.0
prediction = X @ w_linear + b_linear
print("Shape:", X.shape, w_linear.shape, prediction.shape)
print("Dự đoán:", prediction)
assert np.allclose(prediction, [1.0, 3.0])

dependent = np.array([[1.0, 2.0], [2.0, 4.0]])
null_direction = np.array([2.0, -1.0])
print("Hướng không thay đổi dự đoán:", dependent @ null_direction)
print("Hạng ma trận:", np.linalg.matrix_rank(dependent))

# Bước 4
x = np.array([1.0, 2.0])
y = 1.0
theta = np.array([0.2, -0.1, 0.0])

def logistic_loss(parameters):
    z = x @ parameters[:2] + parameters[2]
    return float(np.logaddexp(0.0, z) - y * z)

def logistic_gradient(parameters):
    z = x @ parameters[:2] + parameters[2]
    p = 1.0 / (1.0 + np.exp(-z))
    return np.append((p - y) * x, p - y)

gradient = logistic_gradient(theta)
h = 1e-5
numerical = np.zeros_like(theta)
for j in range(len(theta)):
    shift = np.zeros_like(theta)
    shift[j] = h
    numerical[j] = (logistic_loss(theta + shift) - logistic_loss(theta - shift)) / (2 * h)
new_theta = theta - 0.1 * gradient
print("Gradient:", gradient)
print("Tham số mới:", new_theta)
print(f"Loss: {logistic_loss(theta):.4f} -> {logistic_loss(new_theta):.4f}")
print("Sai phân khớp:", np.allclose(gradient, numerical, atol=1e-8))
assert np.allclose(gradient, [-0.5, -1.0, -0.5])
assert logistic_loss(new_theta) < logistic_loss(theta)

# Bước 5
import torch

torch.manual_seed(0)
conv = torch.nn.Conv2d(3, 2, kernel_size=3, stride=2, padding=1)
images = torch.zeros(4, 3, 8, 8)
with torch.no_grad():
    conv_output = conv(images)
parameter_count = sum(parameter.numel() for parameter in conv.parameters())
print("Output shape:", tuple(conv_output.shape))
print("Số tham số:", parameter_count)
assert tuple(conv_output.shape) == (4, 2, 4, 4)
assert parameter_count == 56

# Bước 6
Q = np.eye(2)
K = np.eye(2)
values = np.array([[2.0, 0.0], [0.0, 4.0]])

def row_softmax(scores):
    shifted = scores - scores.max(axis=1, keepdims=True)
    exponentials = np.exp(shifted)
    return exponentials / exponentials.sum(axis=1, keepdims=True)

scores = Q @ K.T / np.sqrt(Q.shape[1])
weights = row_softmax(scores)
attention_output = weights @ values
print("Trọng số:\n", weights.round(4))
print("Output:\n", attention_output.round(4))
assert np.allclose(weights.sum(axis=1), 1.0)

masked_scores = scores.copy()
masked_scores[0, 1] = -np.inf       # query đầu không nhìn token tương lai
causal_weights = row_softmax(masked_scores)
print("Output đầu với causal mask:", (causal_weights @ values)[0])
assert np.allclose(causal_weights[0], [1.0, 0.0])

# Bước 7
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

labels = np.array([1] * (tp + fn) + [0] * (fp + tn))
predicted = np.array([1] * tp + [0] * fn + [1] * fp + [0] * tn)
accuracy = (tp + tn) / total
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * tp / (2 * tp + fp + fn)
library = np.array([
    accuracy_score(labels, predicted), precision_score(labels, predicted),
    recall_score(labels, predicted), f1_score(labels, predicted),
])
assert np.allclose(library, [accuracy, precision, recall, f1])
print(f"Accuracy={accuracy:.4f}, precision={precision:.4f}, recall={recall:.4f}, F1={f1:.4f}")
print(f"Baseline sạch: accuracy={(fp + tn) / total:.4f}, recall=0.0000")
print("Tính tay khớp thư viện:", True)
