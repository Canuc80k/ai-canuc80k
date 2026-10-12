# -*- coding: utf-8 -*-
# Multimodal — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(74)
binary_signals = rng.integers(0, 2, size=(400, 2))
labels = np.logical_xor(binary_signals[:, 0], binary_signals[:, 1]).astype(int)
features = binary_signals + rng.normal(0, 0.04, binary_signals.shape)
train_indices, valid_indices = train_test_split(
    np.arange(400), test_size=0.25, random_state=7, stratify=labels
)
linear_fusion = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300))
nonlinear_fusion = make_pipeline(
    StandardScaler(),
    MLPClassifier(hidden_layer_sizes=(8,), activation="tanh", solver="lbfgs", max_iter=1000, random_state=7),
)
for name, model in [("linear", linear_fusion), ("MLP", nonlinear_fusion)]:
    model.fit(features[train_indices], labels[train_indices])
    predictions = model.predict(features[valid_indices])
    print(f"{name}: accuracy = {accuracy_score(labels[valid_indices], predictions):.3f}")
print(features.shape)

# Bước 2
toy_labels = np.array([1, 1, 1, 1, 0, 0, 0, 0])
image_probability = np.array([0.90, 0.80, 0.40, 0.30, 0.10, 0.20, 0.60, 0.70])
text_probability = np.array([0.40, 0.35, 0.85, 0.90, 0.55, 0.65, 0.25, 0.20])
fused_probability = (image_probability + text_probability) / 2
for name, probability in [
    ("image", image_probability),
    ("text", text_probability),
    ("fusion", fused_probability),
]:
    prediction = (probability >= 0.5).astype(int)
    print(f"{name}: accuracy = {accuracy_score(toy_labels, prediction):.3f}")
print(fused_probability.round(3))

# Bước 3
wrongly_paired_text = np.roll(
    text_probability, 4
)
wrong_fusion = (
    image_probability + wrongly_paired_text
) / 2
print(f"sai cap: accuracy = {accuracy_score(toy_labels, wrong_fusion >= 0.5):.3f}")

# Bước 4
branch_probabilities = np.column_stack([image_probability, text_probability])
available = np.ones((8, 2), dtype=bool)
available[3, 1] = False  # mẫu 4 mất chữ
available[6, 0] = False  # mẫu 7 mất ảnh
weights = available.astype(float)
weight_sum = weights.sum(axis=1)
assert np.all(weight_sum > 0)
missing_fusion = (branch_probabilities * weights).sum(axis=1) / weight_sum
print(missing_fusion[[3, 6]].round(2))
print(f"thieu nguon: accuracy = {accuracy_score(toy_labels, missing_fusion >= 0.5):.3f}")

# Bước 5
align_rng = np.random.default_rng(7)
n_pairs, dim = 60, 8
shared_content = align_rng.normal(size=(n_pairs, dim))
# Hai ma trận trực giao ngẫu nhiên: mỗi encoder một hệ trục
image_axes = np.linalg.qr(align_rng.normal(size=(dim, dim)))[0]
text_axes = np.linalg.qr(align_rng.normal(size=(dim, dim)))[0]
image_embeddings = shared_content @ image_axes + align_rng.normal(0, 0.3, (n_pairs, dim))
text_embeddings = shared_content @ text_axes + align_rng.normal(0, 0.3, (n_pairs, dim))
train_pairs, valid_pairs = np.arange(40), np.arange(40, 60)

def unit_rows(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)

def recall_at_1(images, texts):
    cosine = unit_rows(images) @ unit_rows(texts).T
    return np.mean(cosine.argmax(axis=1) == np.arange(len(images)))

def fit_map(images, texts):
    return np.linalg.lstsq(images, texts, rcond=None)[0]

projection = fit_map(image_embeddings[train_pairs], text_embeddings[train_pairs])
shuffled_pairs = align_rng.permutation(train_pairs)
wrong_projection = fit_map(image_embeddings[train_pairs], text_embeddings[shuffled_pairs])
valid_images, valid_texts = image_embeddings[valid_pairs], text_embeddings[valid_pairs]
pair_cosine = np.sum(unit_rows(valid_images) * unit_rows(valid_texts), axis=1).mean()
print(f"cosine cap dung, chua can chinh: {pair_cosine:.3f}")
print(f"recall@1 chua can chinh: {recall_at_1(valid_images, valid_texts):.2f}")
print(f"recall@1 sau khi hoc W: {recall_at_1(valid_images @ projection, valid_texts):.2f}")
print(f"recall@1 khi hoc W tu cap bi xao: {recall_at_1(valid_images @ wrong_projection, valid_texts):.2f}")

# Bước 6
import json

def parse_count(text):
    answer = json.loads(text)
    if not isinstance(answer, dict) or set(answer) != {"count"}:
        raise ValueError("can dung khoa count")
    count = answer["count"]
    if type(count) is not int or count < 0:
        raise ValueError("count phai la so nguyen khong am")
    return count

for response in ['{"count": 3}', '{"count": true}', '{"count": "3"}']:
    try:
        print(parse_count(response))
    except ValueError as error:
        print(str(error))
