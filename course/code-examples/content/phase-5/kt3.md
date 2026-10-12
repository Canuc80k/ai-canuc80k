# Code mẫu — Kiểm tra thị giác máy tính

Buổi ôn này nối các bước của một bài thị giác máy tính thành một quy trình chạy được trọn vẹn: ảnh, tiền xử lý, baseline, metric, và file kết quả theo ID. Một quy trình nhỏ mà đủ bước như vậy là nơi tốt để bắt lỗi thực tế, trước khi thay baseline bằng CNN hay model pretrained.

## Ví dụ 1: Phân loại hướng nét, chọn ngưỡng, xuất kết quả theo ID

Mỗi ảnh xám 8×8 chứa một nét đứng, nhãn 0, hoặc một nét ngang, nhãn 1. Pixel lưu theo thang 0 tới 255. Ta dùng hai feature: độ thay đổi trung bình giữa các hàng kề nhau, và giữa các cột kề nhau. Đây là một baseline hình học, chưa phải CNN. Train và validation được sinh độc lập, và validation có ảnh tối hơn.

Trước hết, thử feature trên hai ảnh 4×4 không nhiễu để thấy nó đo được gì.

```python
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
```
```output
Ảnh đứng/ngang (0/1):
[[0 1 1 0]
 [0 1 1 0]
 [0 1 1 0]
 [0 1 1 0]]
[[0 0 0 0]
 [1 1 1 1]
 [1 1 1 1]
 [0 0 0 0]]
Feature đứng/ngang: [[0.0, 0.6667], [0.6667, 0.0]]
Train/valid: (60, 8, 8) (12, 8, 8)
Giá trị sau chuẩn hóa: 0.0 0.937
```

Nét đứng không đổi gì khi đi từ hàng này sang hàng kia, nên feature thứ nhất bằng 0. Nhưng đi theo cột thì gặp hai lần đổi màu, nên feature thứ hai bằng 2/3. Nét ngang thì ngược lại. Hai feature tách hai lớp rất rõ.

Hàm `features` tự chia cho 255, và lúc suy luận cũng gọi đúng hàm này. Nhờ vậy train và suy luận không thể dùng hai thang pixel khác nhau. Ảnh validation có độ sáng thấp hơn train, để thử model trong một điều kiện hơi khác lúc học.

```python
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
```
```output
Threshold/F1: [(0.4, 1.0), (0.5, 1.0), (0.6, 1.0)]
Ngưỡng chọn: 0.5
Valid accuracy/F1: 1.0 1.0
Confusion [đứng, ngang]: [[6, 0], [0, 6]]
```

Cả ba ngưỡng đều cho F1 bằng 1. Luật phá hòa đã đặt trước chọn ngưỡng gần 0.5 nhất, tức chính 0.5. Confusion matrix cho thấy sáu ảnh đứng và sáu ảnh ngang đều đúng hết. Validation đã được dùng để chọn ngưỡng, nên đây chưa phải điểm test độc lập, càng không phải điểm của một cuộc thi.

Bước cuối là đóng gói và xuất kết quả. Ta lưu hệ số, cách tiền xử lý, tên lớp, thứ tự feature và ngưỡng vào một chuỗi JSON. Sau đó nạp lại và tự tính dự đoán từ JSON, không dùng tới object model cũ. Bảng dự đoán được cố tình đảo ngược thứ tự, rồi ghép lại theo ID trước khi ghi CSV.

```python
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
```
```output
Nạp lại cho cùng xác suất: True
Bốn dòng CSV đầu:
image_id,label
valid-00,0
valid-01,1
valid-02,0
valid-03,1
```

Tính lại từ JSON cho đúng các xác suất như model gốc. JSON lưu cả những thứ không phải con số, như thứ tự feature và ý nghĩa của từng lớp, để người dùng sau không phải đoán.

Dù bảng dự đoán đã bị đảo ngược, `valid-00` vẫn nhận đúng nhãn của ảnh 0, nhờ ghép theo ID. Tham số `validate="one_to_one"` bắt lỗi nếu ID bị trùng ở một phía. File CSV được đọc lại bằng pandas để kiểm kiểu dữ liệu và từng cặp ID với nhãn.

## Ví dụ 2: Bắt ID trùng hoặc thiếu trước khi xuất

File mẫu của đề yêu cầu ba ảnh a, b, c. Ta kiểm ba trường hợp: dự đoán đủ nhưng sai thứ tự, có ID bị trùng, và thiếu ảnh c. Có đủ ba dòng chưa có nghĩa là có đủ ba ảnh.

```python
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
```
```output
Đúng ID, sắp lại: [0, 1, 1]
Trùng -> ID prediction trùng
Thiếu -> ID prediction thiếu hoặc thừa
```

Trường hợp đúng được sắp lại theo thứ tự a, b, c của file mẫu, cho `[0, 1, 1]`. Hai trường hợp lỗi bị chặn ngay, kèm thông báo nói rõ lỗi gì, trước khi kịp ghép. Hàm này giả định mỗi ảnh có đúng một nhãn. Với bài detection, một ảnh có thể có nhiều box, nên ID được phép lặp, và phải viết lại phần kiểm cho hợp với định dạng của đề.
