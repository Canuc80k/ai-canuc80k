# Thế giới mở

Phân loại zero-shot kiểu CLIP luôn chọn một trong các lớp được đưa vào, kể cả khi ảnh chẳng thuộc lớp nào. Muốn trả lời "không biết", một cách thường dùng là đặt ngưỡng: nếu xác suất lớn nhất dưới ngưỡng thì từ chối. Bài này kiểm cách ấy có hiệu quả không.

1. Chuẩn hóa mọi vector ảnh và vector lớp về độ dài $1$. Logit là `scale` nhân cosine; softmax theo từng ảnh trên các lớp.
2. Lớp dự đoán là lớp có xác suất lớn nhất (hòa thì chỉ số nhỏ).
3. Nhãn thật là chỉ số lớp, hoặc $-1$ nếu ảnh không thuộc lớp nào.
4. `closed_accuracy`: tỉ lệ ảnh có lớp dự đoán đúng bằng nhãn, khi không bao giờ từ chối.
5. Với mỗi ngưỡng $\tau$ trong `thresholds`: ảnh có xác suất lớn nhất từ $\tau$ trở lên giữ lớp dự đoán, còn lại thành $-1$. Tính tỉ lệ khớp nhãn.
6. `best_threshold`: ngưỡng cho tỉ lệ cao nhất (hòa thì ngưỡng đứng trước).

## Dữ liệu vào

Một đối tượng JSON gồm `image_vectors`, `text_vectors`, `scale`, `labels` và `thresholds` (tăng dần).

## Kết quả

Một đối tượng JSON gồm `probabilities`, `max_probability`, `closed_accuracy`, `threshold_accuracy` và `best_threshold`.

## Giới hạn

- Không quá $12$ ảnh và $4$ lớp. Không xác suất lớn nhất nào sát một ngưỡng, không có hai lớp hòa nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "image_vectors": [[1.0, 0.1], [0.1, 1.0], [0.7, 0.6], [-1.0, 0.2]],
  "text_vectors": [[1.0, 0.0], [0.0, 1.0]],
  "scale": 10.0,
  "labels": [0, 1, -1, -1],
  "thresholds": [0.0, 0.6, 0.9, 0.99]
}
```

```output
{
  "probabilities": [
    [0.99987096975845, 0.0001290302415500569],
    [0.0001290302415500569, 0.99987096975845],
    [0.7473733758181897, 0.25262662418181026],
    [7.756527082594747e-06, 0.9999922434729175]
  ],
  "max_probability": [
    0.99987096975845, 0.99987096975845, 0.7473733758181897,
    0.9999922434729175
  ],
  "closed_accuracy": 0.5,
  "threshold_accuracy": [0.5, 0.5, 0.75, 0.75],
  "best_threshold": 0.9
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
