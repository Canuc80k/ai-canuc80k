# -*- coding: utf-8 -*-
# Kiểm tra thị giác máy tính — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

probabilities = np.array([0.9, 0.7, 0.6, 0.55, 0.45, 0.2, 0.1, 0.05])
labels = np.array([1, 1, 0, 1, 0, 0, 0, 0], dtype=bool)

def binary_metrics(prediction, target):
    tp = np.sum(prediction & target)
    fp = np.sum(prediction & ~target)
    fn = np.sum(~prediction & target)
    accuracy = np.mean(prediction == target)
    denominator = 2 * tp + fp + fn
    f1 = 0.0 if denominator == 0 else 2 * tp / denominator
    return float(accuracy), float(f1)

for threshold in [0.5, 0.65, 0.8]:
    accuracy, f1 = binary_metrics(probabilities >= threshold, labels)
    print(threshold, "accuracy/F1:", round(accuracy, 4), round(f1, 4))

# Bước 2
import pandas as pd

sample = pd.DataFrame({"image_id": ["a", "b", "c"]})
predictions = pd.DataFrame({"image_id": ["c", "a", "b"],
                            "label": [1, 0, 1]})
assert predictions["image_id"].is_unique
assert set(predictions["image_id"]) == set(sample["image_id"])
submission = sample.merge(predictions, on="image_id", how="left", validate="one_to_one")
assert submission["label"].notna().all()
print(submission.to_string(index=False))
