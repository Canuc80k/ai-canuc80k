# -*- coding: utf-8 -*-
# Kiểm tra khóa 3 — chạy các bước như notebook từ trên xuống.

# Bước 1
def normalized_score(x, baseline, best):
    return 100 * max(0.0, (x - baseline) / (best - baseline))

print(f"A, macro-F1 0.70 -> {normalized_score(0.70, 0.50, 0.90):.1f}")
print(f"A, macro-F1 0.74 -> {normalized_score(0.74, 0.50, 0.90):.1f}")
print(f"B, WER 0.30      -> {normalized_score(0.30, 0.40, 0.15):.1f}")
print(f"B, WER 0.45      -> {normalized_score(0.45, 0.40, 0.15):.1f}")

# Bước 2
import numpy as np

expected_ids = ["img-a", "img-b", "img-c"]
prediction_by_id = {"img-c": 1, "img-a": 2, "img-b": 0}
assert len(expected_ids) == len(set(expected_ids))
assert set(prediction_by_id) == set(expected_ids)
ordered_predictions = np.array([prediction_by_id[sample_id] for sample_id in expected_ids])
assert ordered_predictions.shape == (3,)
assert np.isin(ordered_predictions, [0, 1, 2]).all()
reference_labels = np.array([2, 1, 1])
print(ordered_predictions)
print(f"accuracy minh hoa = {np.mean(ordered_predictions == reference_labels):.3f}")

# Bước 3
def token_errors(reference, prediction):
    left, right = reference.lower().split(), prediction.lower().split()
    previous = list(range(len(right) + 1))
    for row, token in enumerate(left, start=1):
        current = [row]
        for column, predicted_token in enumerate(right, start=1):
            current.append(min(
                previous[column] + 1,
                current[column - 1] + 1,
                previous[column - 1] + (token != predicted_token),
            ))
        previous = current
    return previous[-1], len(left)

references = ["em học ai", "mai thi toán"]
transcripts = ["em học", "mai thi toán"]
counts = [token_errors(r, p) for r, p in zip(references, transcripts)]
total_errors = sum(error_count for error_count, _ in counts)
total_tokens = sum(length for _, length in counts)
print(counts)
print(f"corpus WER = {total_errors / total_tokens:.3f}")
print(f"cau dung hoan toan = {sum(r == p for r, p in zip(references, transcripts))}/2")

# Bước 4
import numpy as np

labels      = np.array([0, 1, 2, 1, 0, 2, 2, 0, 1, 1, 0, 2, 1, 0, 2, 1, 0, 2, 0, 1, 2, 0, 1, 2, 0])
image_pred  = np.array([0, 1, 2, 2, 0, 1, 2, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 2, 0, 1, 2, 0])
text_pred   = np.array([1, 1, 2, 1, 0, 1, 2, 0, 0, 1, 0, 2, 2, 0, 1, 1, 0, 2, 0, 1, 2, 1, 1, 2, 0])
fusion_pred = np.array([0, 1, 2, 1, 0, 1, 2, 0, 0, 1, 0, 2, 1, 0, 0, 1, 0, 2, 0, 1, 2, 1, 1, 2, 0])

image_ok, text_ok, fusion_ok = (pred == labels for pred in (image_pred, text_pred, fusion_pred))
for name, ok in [("anh", image_ok), ("chu", text_ok), ("fusion", fusion_ok)]:
    print(f"{name:6s} accuracy = {ok.mean():.2f}")
for name, mask in [("fusion sua", ~image_ok & fusion_ok),
                   ("fusion lam sai", image_ok & ~fusion_ok),
                   ("ca ba cung sai", ~image_ok & ~text_ok & ~fusion_ok)]:
    print(f"{name:14s}: {np.flatnonzero(mask).tolist()}")
