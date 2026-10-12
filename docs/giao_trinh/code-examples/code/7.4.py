# -*- coding: utf-8 -*-
# Code mẫu — Multimodal

# Ví dụ 1: Ghép theo ID, và căn lại thứ tự các lớp
import numpy as np

ids = ["notice-a", "notice-b", "notice-c"]
image_by_id = {
    "notice-a": [0.8, 0.2],
    "notice-b": [0.3, 0.7],
    "notice-c": [0.6, 0.4],
}
text_by_id = {
    "notice-c": [0.8, 0.2],
    "notice-a": [0.7, 0.3],
    "notice-b": [0.1, 0.9],
}
image_classes = ["xe", "chuong"]
text_classes = ["chuong", "xe"]
assert set(image_by_id) == set(text_by_id) == set(ids)
assert set(image_classes) == set(text_classes)

image_p = np.array([image_by_id[sample_id] for sample_id in ids])
text_p = np.array([text_by_id[sample_id] for sample_id in ids])
column_order = [text_classes.index(label) for label in image_classes]
aligned_text_p = text_p[:, column_order]
fused_p = 0.25 * image_p + 0.75 * aligned_text_p
assert np.allclose(fused_p.sum(axis=1), 1)

print("thu tu lop:", image_classes)
for sample_id, probability in zip(ids, fused_p):
    label = image_classes[probability.argmax()]
    print(sample_id, np.round(probability, 3), "->", label)


# Ví dụ 2: Một nguồn kém tin cậy, hoặc bị thiếu
import numpy as np

probabilities = np.array([
    [0.1, 0.9],
    [0.8, np.nan],
    [np.nan, 0.3],
    [np.nan, np.nan],
])
base_weights = np.array([0.7, 0.3])
reliability = np.array([
    [0.1, 1.0],
    [1.0, 1.0],
    [1.0, 1.0],
    [1.0, 1.0],
])
available = np.isfinite(probabilities)
weights = base_weights * reliability * available
denominator = weights.sum(axis=1)
usable = denominator > 0
fused = np.full(len(probabilities), np.nan)
safe_values = np.where(available, probabilities, 0.0)
fused[usable] = (safe_values * weights).sum(axis=1)[usable] / denominator[usable]

assert np.allclose(fused[:3], [0.277 / 0.37, 0.8, 0.3])
assert np.isnan(fused[3])
print(f"hang 1, trong so con lai: {weights[0].round(2)}")
for row, value in enumerate(fused, start=1):
    print(f"hang {row}: p1={value:.3f}" if np.isfinite(value)
          else f"hang {row}: REVIEW (khong con nguon)")


# Ví dụ 3: Train hai nhánh, rồi chọn cách ghép trên tập hiệu chỉnh
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss

rng = np.random.default_rng(74)
latent = rng.normal(size=600)
labels = (latent > 0).astype(int)
features_a = np.column_stack([latent + rng.normal(0, 0.8, 600), rng.normal(size=600)])
features_b = np.column_stack([latent + rng.normal(0, 0.8, 600), rng.normal(size=600)])
order = rng.permutation(600)
train, calibration, valid = order[:300], order[300:450], order[450:]
assert not set(train) & set(calibration) and not set(calibration) & set(valid)

models = []
for features in [features_a, features_b]:
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300))
    model.fit(features[train], labels[train])
    assert np.array_equal(model.classes_, [0, 1])
    models.append(model)

def sigmoid(logits):
    return 1 / (1 + np.exp(-logits))

def binary_log_loss(targets, positive_p):
    return log_loss(targets, np.column_stack([1 - positive_p, positive_p]), labels=[0, 1])

a_cal_logits = 3 * models[0].decision_function(features_a[calibration])
b_cal_p = models[1].predict_proba(features_b[calibration])[:, 1]
temperature_grid = [1.0, 2.0, 3.0, 4.0]
temperature_losses = [binary_log_loss(labels[calibration], sigmoid(a_cal_logits / t))
                      for t in temperature_grid]
temperature = temperature_grid[int(np.argmin(temperature_losses))]
a_cal_p = sigmoid(a_cal_logits / temperature)
weight_grid = [0.0, 0.25, 0.5, 0.75, 1.0]
fusion_losses = [binary_log_loss(labels[calibration], w * a_cal_p + (1 - w) * b_cal_p)
                 for w in weight_grid]
weight_a = weight_grid[int(np.argmin(fusion_losses))]

a_valid_logits = 3 * models[0].decision_function(features_a[valid])
raw_a_p = sigmoid(a_valid_logits)
a_valid_p = sigmoid(a_valid_logits / temperature)
b_valid_p = models[1].predict_proba(features_b[valid])[:, 1]
fusion_p = weight_a * a_valid_p + (1 - weight_a) * b_valid_p
assert np.isfinite(fusion_p).all() and np.all((fusion_p >= 0) & (fusion_p <= 1))
assert np.array_equal(raw_a_p >= 0.5, a_valid_p >= 0.5)

print(f"temperature A = {temperature:.1f}; trong so A = {weight_a:.2f}")
for name, probabilities in [("A qua tu tin", raw_a_p), ("A calibrated", a_valid_p),
                            ("B", b_valid_p), ("fusion", fusion_p)]:
    print(f"{name}: accuracy={accuracy_score(labels[valid], probabilities >= 0.5):.3f}, "
          f"log-loss={binary_log_loss(labels[valid], probabilities):.3f}")

