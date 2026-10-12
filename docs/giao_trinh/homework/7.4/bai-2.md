# Thiếu một modality

Late fusion: mỗi modality (âm thanh, hình ảnh, …) tự cho một phân phối xác suất, rồi gộp bằng trung bình có trọng số. Khi một mẫu thiếu một modality, không được coi phần thiếu là vector $0$: phải chia lại trọng số trên các modality còn có.

Mỗi modality có `weight` $>0$ và `probabilities`: với mỗi mẫu là một phân phối ($C$ số) hoặc `null` nếu thiếu.

Với mỗi mẫu:

1. Chỉ lấy các modality có dữ liệu. Chia trọng số của chúng cho tổng trọng số **của chính các modality ấy**.
2. Phân phối gộp là trung bình có trọng số; dự đoán là lớp có xác suất lớn nhất (bằng nhau thì lớp số nhỏ hơn).
3. Nếu mọi modality đều thiếu, cả phân phối lẫn dự đoán là `null`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `ids` và `modalities`.

## Kết quả

Một đối tượng JSON gồm `ids`, `probabilities` và `predictions`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "ids": ["002", "2", "none", "audio"],
  "modalities": [
    {
      "weight": 0.7,
      "probabilities": [[0.8, 0.2], [0.2, 0.8], null, null]
    },
    {
      "weight": 0.3,
      "probabilities": [[0.1, 0.9], null, null, [0.75, 0.25]]
    }
  ]
}
```

```output
{
  "ids": ["002", "2", "none", "audio"],
  "probabilities": [
    [0.59, 0.41000000000000003],
    [0.19999999999999998, 0.7999999999999999],
    null,
    [0.75, 0.25]
  ],
  "predictions": [0, 1, null, 0]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
