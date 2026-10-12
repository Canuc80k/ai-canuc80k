# -*- coding: utf-8 -*-
# Phân tích hành vi model — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
from sklearn.linear_model import LogisticRegression

vertical = np.zeros((8, 8))
vertical[2:6, 3:5] = 1
horizontal = np.zeros((8, 8))
horizontal[3:5, 2:6] = 1
orientation_filter = (horizontal - vertical) / 4

def make_images(count, seed, reverse_corner=False):
    rng = np.random.default_rng(seed)
    labels = np.arange(count) % 2
    images = np.zeros((count, 8, 8))
    for index, label in enumerate(labels):
        images[index] = vertical if label == 0 else horizontal
        marker = 1 - label if reverse_corner else label
        images[index, :2, :2] = marker
    images += rng.normal(0, 0.02, images.shape)
    return np.clip(images, 0, 1), labels

def features(images):
    corner = images[:, :2, :2].mean(axis=(1, 2))
    shape = (images * orientation_filter).sum(axis=(1, 2))
    return corner[:, None], shape[:, None]

train_images, train_labels = make_images(80, 1)
normal_images, labels = make_images(40, 2)
changed_images, changed_labels = make_images(40, 2, reverse_corner=True)
train_corner, train_shape = features(train_images)
model_a = LogisticRegression().fit(train_corner, train_labels)
model_b = LogisticRegression().fit(train_shape, train_labels)
print("same labels after intervention:", np.array_equal(labels, changed_labels))
print("shape features preserved:",
      np.allclose(features(normal_images)[1], features(changed_images)[1]))

# Bước 2
def predict_both(images):
    corner, shape = features(images)
    return model_a.predict(corner), model_b.predict(shape)

for name, images in [("normal", normal_images), ("changed corner", changed_images)]:
    pred_a, pred_b = predict_both(images)
    print(name, "A/B accuracy:",
          round(np.mean(pred_a == labels), 3),
          round(np.mean(pred_b == labels), 3))

pred_a, pred_b = predict_both(changed_images)
print("A correct, B wrong:", int(np.sum((pred_a == labels) & (pred_b != labels))))
print("B correct, A wrong:", int(np.sum((pred_b == labels) & (pred_a != labels))))

# Bước 3
example = normal_images[1].copy()
without_corner = example.copy()
without_corner[:2, :2] = 0
without_shape = example.copy()
without_shape[2:6, 2:6] = 0
batch = np.stack([example, without_corner, without_shape])
corner, shape = features(batch)
score_a = model_a.predict_proba(corner)[:, 1]
score_b = model_b.predict_proba(shape)[:, 1]
print("rows: original, cover corner, cover shape")
print("A probability of class 1:", score_a.round(4).tolist())
print("B probability of class 1:", score_b.round(4).tolist())

# Bước 4
import torch

shape_filter = torch.tensor(orientation_filter)
readers = {
    "A": (model_a, lambda pixels: pixels[:2, :2].mean()),
    "B": (model_b, lambda pixels: (pixels * shape_filter).sum()),
}

def saliency(name, image, use_probability=False):
    model, read_feature = readers[name]
    pixels = torch.tensor(image, requires_grad=True)
    score = (float(model.coef_[0, 0]) * read_feature(pixels)
             + float(model.intercept_[0]))
    if use_probability:
        score = torch.sigmoid(score)
    score.backward()
    return pixels.grad.abs().numpy()

corner = np.zeros((8, 8), dtype=bool)
corner[:2, :2] = True
for name in ["A", "B"]:
    horizontal_map = saliency(name, normal_images[1])
    vertical_map = saliency(name, normal_images[0])
    print(name, "corner:", round(horizontal_map[corner].sum() / horizontal_map.sum(), 3),
          "| max:", round(horizontal_map.max(), 4),
          "| same on vertical:", np.allclose(horizontal_map, vertical_map))
print("B max grad of probability:", round(saliency("B", normal_images[1], True).max(), 4))

# Bước 5
def shift_strokes(images, rows):
    shifted = images.copy()
    shifted[:, 2:, 2:] = np.roll(images[:, 2:, 2:], rows, axis=1)
    return shifted

conditions = {
    "normal": normal_images,
    "changed corner": changed_images,
    "shift 1 row": shift_strokes(normal_images, 1),
    "shift 2 rows": shift_strokes(normal_images, 2),
}
print("condition        A      B")
for name, images in conditions.items():
    pred_a, pred_b = predict_both(images)
    print(f"{name:15s} {np.mean(pred_a == labels):.3f}  {np.mean(pred_b == labels):.3f}")
