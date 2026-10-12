# Chọn ngưỡng

Mô hình phân loại nhị phân cho xác suất; đổi thành nhãn cần một ngưỡng. Ngưỡng $0.5$ không phải lúc nào cũng tốt, nhất là khi lớp dương hiếm. Ngưỡng phải được chọn trên validation, rồi mới báo kết quả trên test. Bài này làm đúng việc ấy, và đo xem nếu "nhìn trộm" test để chọn ngưỡng thì con số báo cáo đẹp lên bao nhiêu.

Dự đoán là $1$ khi xác suất **từ ngưỡng trở lên**. F1 là $\dfrac{2\,TP}{2\,TP+FP+FN}$, và bằng $0$ nếu không có TP nào.

1. Trong các ngưỡng `thresholds`, chọn ngưỡng cho F1 lớn nhất trên validation; hòa thì ngưỡng nhỏ hơn.
2. Báo F1 trên test với ngưỡng mặc định $0.5$ và với ngưỡng vừa chọn.
3. Làm lại bước 1 nhưng chọn trên chính test (cách làm sai), báo ngưỡng ấy, F1 của nó, và độ chênh so với F1 ở bước 2.

## Dữ liệu vào

Một đối tượng JSON gồm `valid_probs`, `valid_labels`, `test_probs`, `test_labels` và `thresholds`.

## Kết quả

Một đối tượng JSON gồm `valid_threshold`, `valid_f1`, `test_f1_default`, `test_f1_tuned`, `peek_threshold`, `test_f1_peek` và `optimism` (bằng `test_f1_peek` trừ `test_f1_tuned`).

## Giới hạn

- Không quá $40$ mẫu mỗi tập.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "valid_probs": [
    0.44, 0.84, 0.54, 0.25, 0.92, 0.08, 0.37, 0.68, 0.54, 0.26, 0.21,
    0.47, 0.35, 0.43, 0.6, 0.75, 0.46, 0.24, 0.41, 0.16, 0.33, 0.92
  ],
  "valid_labels": [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
  "test_probs": [
    0.62, 0.96, 0.51, 0.63, 0.66, 0.65, 0.73, 0.44, 0.33, 0.25, 0.43,
    0.41, 0.59, 0.6, 0.3, 0.34, 0.35, 0.6, 0.8, 0.41, 0.42, 0.16, 0.2,
    0.64, 0.67, 0.48, 0.43, 0.56, 0.7, 0.4, 0.66, 0.22, 0.61, 0.58,
    0.73, 0.59, 0.5
  ],
  "test_labels": [
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0
  ],
  "thresholds": [
    0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
    0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95
  ]
}
```

```output
{
  "valid_threshold": 0.55,
  "valid_f1": 1.0,
  "test_f1_default": 0.5517241379310345,
  "test_f1_tuned": 0.5925925925925926,
  "peek_threshold": 0.65,
  "test_f1_peek": 0.7058823529411765,
  "optimism": 0.11328976034858396
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
