# -*- coding: utf-8 -*-
# Classification metrics — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score, f1_score,
)

y_valid = np.array([1, 0, 1, 0, 0, 1, 0, 0, 1, 0])
p_valid = np.array([0.95, 0.80, 0.70, 0.65, 0.60, 0.55, 0.40, 0.30, 0.20, 0.10])
prediction = (p_valid >= 0.5).astype(int)
cm = confusion_matrix(y_valid, prediction, labels=[0, 1])
tn, fp, fn, tp = cm.ravel()
print(cm)
print('TN, FP, FN, TP:', tn, fp, fn, tp)
print(f'Accuracy={accuracy_score(y_valid, prediction):.3f}')
print(f'Precision={precision_score(y_valid, prediction, zero_division=0):.3f}')
print(f'Recall={recall_score(y_valid, prediction, zero_division=0):.3f}')
print(f'F1={f1_score(y_valid, prediction, zero_division=0):.3f}')

# Bước 2
thresholds = np.array([0.3, 0.5, 0.7, 0.9])
valid_f1 = []
for threshold in thresholds:
    prediction = p_valid >= threshold
    score = f1_score(y_valid, prediction, zero_division=0)
    valid_f1.append(score)
    print(f't={threshold:.1f}: F1={score:.3f}')
chosen_threshold = float(thresholds[np.argmax(valid_f1)])
print('Chọn trên validation:', chosen_threshold)

# Bước 3
y_test = np.array([0, 1, 0, 0, 1, 0, 1, 0])
p_test = np.array([0.70, 0.80, 0.20, 0.40, 0.55, 0.10, 0.30, 0.65])
test_prediction = p_test >= chosen_threshold
print(f'Test F1 với ngưỡng đã chốt={f1_score(y_test, test_prediction, zero_division=0):.3f}')

# Bước 4
from sklearn.metrics import roc_auc_score, average_precision_score

positive_scores = p_valid[y_valid == 1]
negative_scores = p_valid[y_valid == 0]
pair_points = []
for positive in positive_scores:
    for negative in negative_scores:
        pair_points.append(float(positive > negative) + 0.5 * float(positive == negative))
print(f'AUC tính theo cặp={np.mean(pair_points):.3f}')
print(f'AUC thư viện={roc_auc_score(y_valid, p_valid):.3f}')
print(f'Average precision={average_precision_score(y_valid, p_valid):.3f}')

# Bước 5
from sklearn.metrics import log_loss

truth = np.array([1, 0])
confident_wrong = np.array([0.01, 0.99])
less_confident_wrong = np.array([0.4, 0.6])
print(f'Sai rất tự tin: log loss={log_loss(truth, confident_wrong):.3f}')
print(f'Sai ít tự tin: log loss={log_loss(truth, less_confident_wrong):.3f}')
