# Gộp cửa sổ

Clip dài được cắt thành nhiều cửa sổ ngắn, mô hình cho mỗi cửa sổ một phân phối xác suất trên các lớp. Muốn một nhãn cho cả clip thì phải gộp lại. Bài này thử ba cách gộp.

Các cửa sổ cho trong `windows`, không theo thứ tự, mỗi cửa sổ có `clip_id` và `probabilities` ($C$ số). Với mỗi clip, **theo thứ tự trong `clip_ids`**:

- `means`: trung bình xác suất của các cửa sổ, theo từng lớp.
- `maxima`: giá trị lớn nhất theo từng lớp (không chuẩn hóa lại).
- `votes`: số cửa sổ có lớp ấy là lớp xác suất cao nhất (bằng nhau thì lớp số nhỏ hơn).
- `argmax_means`, `argmax_votes`: lớp thắng theo trung bình và theo số phiếu (bằng nhau thì lớp số nhỏ hơn).

Mã clip là chuỗi: `"002"` và `"2"` là hai clip khác nhau.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `clip_ids`, `num_classes` và `windows`.

## Kết quả

Một đối tượng JSON gồm `clip_ids`, `means`, `maxima`, `votes`, `argmax_means` và `argmax_votes`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "clip_ids": ["2", "b", "002"],
  "num_classes": 3,
  "windows": [
    {"clip_id": "b", "probabilities": [0.9, 0.08, 0.02]},
    {"clip_id": "2", "probabilities": [0.9, 0.08, 0.02]},
    {"clip_id": "002", "probabilities": [0.9, 0.08, 0.02]},
    {"clip_id": "002", "probabilities": [0.4, 0.59, 0.01]},
    {"clip_id": "002", "probabilities": [0.45, 0.54, 0.01]},
    {"clip_id": "b", "probabilities": [0.4, 0.59, 0.01]},
    {"clip_id": "2", "probabilities": [0.45, 0.54, 0.01]},
    {"clip_id": "2", "probabilities": [0.4, 0.59, 0.01]},
    {"clip_id": "b", "probabilities": [0.45, 0.54, 0.01]}
  ]
}
```

```output
{
  "clip_ids": ["2", "b", "002"],
  "means": [
    [0.5833333333333334, 0.4033333333333333, 0.013333333333333334],
    [0.5833333333333334, 0.4033333333333333, 0.013333333333333334],
    [0.5833333333333334, 0.4033333333333333, 0.013333333333333334]
  ],
  "maxima": [[0.9, 0.59, 0.02], [0.9, 0.59, 0.02], [0.9, 0.59, 0.02]],
  "votes": [[1, 2, 0], [1, 2, 0], [1, 2, 0]],
  "argmax_means": [0, 0, 0],
  "argmax_votes": [1, 1, 1]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
