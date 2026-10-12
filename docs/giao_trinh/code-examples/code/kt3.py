# -*- coding: utf-8 -*-
# Code mẫu — Kiểm tra thị giác máy tính

# Ví dụ 1: Phân loại hướng nét, chọn ngưỡng, xuất kết quả theo ID
import io
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

def features(images_uint8, pixel_scale=255.0):
    images = images_uint8.astype(np.float64) / pixel_scale
    # Giữ nguyên hai trục không gian. Chỉ chia thang pixel đúng một lần ở đây.
    change_rows = np.abs(np.diff(images, axis=1)).mean((1, 2))
    change_cols = np.abs(np.diff(images, axis=2)).mean((1, 2))
    return np.column_stack([change_rows, change_cols])

vertical = np.zeros((4, 4), dtype=np.uint8); vertical[:, 1:3] = 255
horizontal = np.zeros((4, 4), dtype=np.uint8); horizontal[1:3, :] = 255
print("Ảnh đứng/ngang (0/1):")
print(vertical // 255)
print(horizontal // 255)
print("Feature đứng/ngang:", features(np.stack([vertical, horizontal])).round(4).tolist())
assert np.allclose(features(np.stack([vertical, horizontal])), [[0, 2/3], [2/3, 0]])

def make_images(count, seed, min_brightness):
    rng = np.random.default_rng(seed)
    labels = np.arange(count) % 2
    images = np.zeros((count, 8, 8))
    for i, label in enumerate(labels):
        position = int(rng.integers(2, 5))
        brightness = rng.uniform(min_brightness, 0.9)
        if label == 0:
            images[i, 1:7, position:position + 2] = brightness
        else:
            images[i, position:position + 2, 1:7] = brightness
    images = np.clip(images + rng.normal(0.03, 0.02, images.shape), 0, 1)
    return np.rint(images * 255).astype(np.uint8), labels

train_x, train_y = make_images(60, 1, 0.5)
valid_x, valid_y = make_images(12, 2, 0.25)
print("Train/valid:", train_x.shape, valid_x.shape)
print("Giá trị sau chuẩn hóa:", round(float(valid_x.min() / 255), 3),
      round(float(valid_x.max() / 255), 3))

model = LogisticRegression(C=100, max_iter=300, random_state=0)
model.fit(features(train_x), train_y)
probability = model.predict_proba(features(valid_x))[:, 1]
thresholds = [0.4, 0.5, 0.6]
scores = [f1_score(valid_y, probability >= t, zero_division=0) for t in thresholds]
# Nếu hòa điểm, chọn ngưỡng gần 0.5 nhất. Luật này đặt ra trước khi xem kết quả.
best_index = max(range(len(thresholds)), key=lambda i: (scores[i], -abs(thresholds[i] - 0.5)))
threshold = thresholds[best_index]
prediction = (probability >= threshold).astype(int)
print("Threshold/F1:", [(t, round(float(s), 4)) for t, s in zip(thresholds, scores)])
print("Ngưỡng chọn:", threshold)
print("Valid accuracy/F1:", round(accuracy_score(valid_y, prediction), 4),
      round(f1_score(valid_y, prediction), 4))
print("Confusion [đứng, ngang]:", confusion_matrix(valid_y, prediction, labels=[0, 1]).tolist())
assert prediction.shape == valid_y.shape
assert f1_score(valid_y, prediction) > 0.8

checkpoint = json.dumps({
    "coef": model.coef_.tolist(), "intercept": model.intercept_.tolist(),
    "class_names": ["đứng", "ngang"], "pixel_scale": 255.0,
    "feature_order": ["change_rows", "change_cols"], "threshold": threshold,
}, ensure_ascii=False)
loaded = json.loads(checkpoint)
assert loaded["feature_order"] == ["change_rows", "change_cols"]
logits = features(valid_x, loaded["pixel_scale"]) @ np.asarray(loaded["coef"])[0] + loaded["intercept"][0]
reloaded_probability = 1 / (1 + np.exp(-logits))
reloaded_prediction = (reloaded_probability >= loaded["threshold"]).astype(int)
assert np.allclose(probability, reloaded_probability, atol=1e-12)
assert np.array_equal(prediction, reloaded_prediction)

ids = [f"valid-{i:02d}" for i in range(len(valid_x))]
sample = pd.DataFrame({"image_id": ids})
rows = pd.DataFrame({"image_id": ids, "label": reloaded_prediction}).iloc[::-1]
submission = sample.merge(rows, on="image_id", validate="one_to_one", how="left")
assert submission["label"].notna().all()
assert submission["image_id"].tolist() == ids
assert submission["label"].tolist() == prediction.tolist()
csv_text = submission.to_csv(index=False)
read_back = pd.read_csv(io.StringIO(csv_text))
assert read_back.equals(submission)
print("Nạp lại cho cùng xác suất:", np.allclose(probability, reloaded_probability, atol=1e-12))
print("Bốn dòng CSV đầu:")
print("\n".join(csv_text.splitlines()[:5]))


# Ví dụ 2: Bắt ID trùng hoặc thiếu trước khi xuất
import pandas as pd

def align_predictions(sample, rows):
    if not rows["image_id"].is_unique:
        raise ValueError("ID prediction trùng")
    if set(rows["image_id"]) != set(sample["image_id"]):
        raise ValueError("ID prediction thiếu hoặc thừa")
    result = sample.merge(rows, on="image_id", how="left", validate="one_to_one")
    if result["label"].isna().any() or not result["label"].isin([0, 1]).all():
        raise ValueError("Nhãn chưa đúng hợp đồng 0/1")
    return result

sample = pd.DataFrame({"image_id": ["a", "b", "c"]})
correct = pd.DataFrame({"image_id": ["c", "a", "b"], "label": [1, 0, 1]})
print("Đúng ID, sắp lại:", align_predictions(sample, correct)["label"].tolist())
bad_cases = {
    "Trùng": pd.DataFrame({"image_id": ["a", "b", "b"], "label": [0, 1, 1]}),
    "Thiếu": pd.DataFrame({"image_id": ["a", "b"], "label": [0, 1]}),
}
for name, rows in bad_cases.items():
    try:
        align_predictions(sample, rows)
    except ValueError as error:
        print(name, "->", error)
    else:
        raise AssertionError("Chưa bắt lỗi " + name)

