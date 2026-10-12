# Baseline

Trước khi dựng model, nên nộp thử một **điểm mốc** (baseline) thật đơn giản. Ta đoán điểm của mỗi học sinh bằng điểm trung bình của lớp ấy trên train. Lớp chưa có trong train thì đoán bằng trung bình của cả train. Đây đúng là các bước ở mục Tạo file nộp của bài học.

Tệp nộp phải theo **đúng thứ tự mã trong `sample.csv`**, thứ tự này có thể khác `test.csv`. Mã có thể có số $0$ ở đầu như `0007`, nên đọc bằng `dtype={"id": str}`.

Hàm `solve` trả về nội dung CSV dưới dạng một chuỗi. `to_csv(index=False)` không kèm tên tệp sẽ trả về đúng chuỗi ấy.

## Dữ liệu vào

Mỗi thư mục test có ba tệp:

- `train.csv` gồm `id`, `class`, `score`.
- `test.csv` gồm `id`, `class`.
- `sample.csv` là tệp nộp mẫu, gồm `id` và cột `prediction` toàn số $0$.

## Kết quả

Nội dung CSV với dòng đầu `id,prediction`.

## Giới hạn

- Train có từ $1$ đến $200$ dòng, test có từ $1$ đến $120$ dòng, điểm từ $0$ đến $10$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Mã và thứ tự phải đúng hoàn toàn, dự đoán được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
train.csv:
id,class,score
001,A,6
002,A,8
003,B,5

test.csv:
id,class
0101,A
0102,C
0103,B

sample.csv:
id,prediction
0103,0
0101,0
0102,0
```

```output
id,prediction
0103,5.0
0101,7.0
0102,6.333333333333333
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.csv`, `02.csv`, …, `20.csv`. Nộp tệp ZIP ấy, chọn **Output**.
:::
