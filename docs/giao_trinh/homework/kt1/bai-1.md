# Baseline

Trước khi thử mô hình lớn, hãy có một baseline: dự đoán cùng một hằng số cho mọi hàng. Với sai số tuyệt đối, hằng số tốt nhất là median của nhãn train. Mọi mô hình sau này phải thắng được con số ấy mới đáng dùng.

Hãy tính median của nhãn trong `train.csv` (số phần tử chẵn thì lấy trung bình hai phần tử giữa), rồi ghi dự đoán ấy cho mọi `id` trong `sample.csv`, **đúng thứ tự của `sample.csv`**.

`id` là chuỗi. `"002"` và `"2"` là hai id khác nhau, và id có thể chứa dấu phẩy, dấu ngoặc kép hay dấu cách. Đọc tệp bằng thư viện `csv` hoặc pandas với `dtype=str` để không làm hỏng chúng.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `id`, `label`) và `sample.csv` (cột `id`).

## Kết quả

Một đối tượng JSON `{"rows": [...]}`, mỗi phần tử là `{"id": ..., "target": ...}`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
sample.csv:
id
002
2
"A,1"
"""quoted"""

train.csv:
id,label
0,10
1,19
2,14
3,4
4,-2
```

```output
{
  "rows": [
    {"id": "002", "target": 10.0},
    {"id": "2", "target": 10.0},
    {"id": "A,1", "target": 10.0},
    {"id": "\"quoted\"", "target": 10.0}
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
