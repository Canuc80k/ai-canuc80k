# Thứ tự lớp

Một checkpoint lưu xác suất theo thứ tự lớp lúc huấn luyện (`checkpoint_classes`), còn bộ dữ liệu chấm bài đánh số lớp theo thứ tự khác (`dataset_classes`). Ghép cột theo vị trí là sai; phải ghép theo **tên lớp**.

1. Sắp lại các cột xác suất theo thứ tự của `dataset_classes`.
2. Dự đoán là chỉ số (trong `dataset_classes`) của cột lớn nhất sau khi sắp lại; hòa thì chỉ số nhỏ hơn.
3. Giữ nguyên mã ảnh và thứ tự các hàng. Không áp softmax thêm lần nào.

Mã ảnh là chuỗi: `"002"` và `"2"` là hai mã khác nhau.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `checkpoint_classes`, `dataset_classes`, `ids` và `probabilities` (theo thứ tự `checkpoint_classes`).

## Kết quả

Một đối tượng JSON gồm `rows`: mỗi hàng là `{"ID", "prediction", "probabilities"}`, với `probabilities` đã sắp lại.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "checkpoint_classes": ["bird", "cat", "dog"],
  "dataset_classes": ["dog", "bird", "cat"],
  "ids": ["002", "2", "last"],
  "probabilities": [[0.5, 0, 0.5], [0.1, 0.8, 0.1], [0.2, 0.1, 0.7]]
}
```

```output
{
  "rows": [
    {"ID": "002", "prediction": 0, "probabilities": [0.5, 0.5, 0]},
    {"ID": "2", "prediction": 2, "probabilities": [0.1, 0.1, 0.8]},
    {"ID": "last", "prediction": 0, "probabilities": [0.7, 0.2, 0.1]}
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
