# Tóm tắt nhóm

Trong một đề thi, dữ liệu chia thành nhiều nhóm, mỗi nhóm là một tập điểm $(x, y)$, và ta phải dự đoán vài tham số cho từng nhóm. Bước đầu tiên của mọi lời giải là tóm tắt mỗi nhóm thành một dòng. Bài này làm bước ấy.

`points.csv` chứa điểm của mọi nhóm, các dòng đan xen nhau. `groups.csv` liệt kê các nhóm cần nộp, theo đúng thứ tự cần nộp. Có nhóm trong `points.csv` không cần nộp, cũng có nhóm cần nộp mà không có điểm nào.

Với mỗi nhóm trong `groups.csv`, ghi một dòng gồm mã nhóm, số điểm `n`, trung bình và độ lệch chuẩn của $y$ (`y_mean`, `y_std`, chia cho $n-1$ như pandas), cùng giá trị nhỏ nhất và lớn nhất của $x$ (`x_min`, `x_max`). Nhóm không có điểm thì $n=0$ và bốn ô còn lại để trống. Nhóm chỉ có một điểm thì `y_std` để trống. Khi ghi CSV, pandas tự để trống các ô `NaN`.

Hàm `solve` trả về nội dung CSV dưới dạng một chuỗi.

## Dữ liệu vào

Mỗi thư mục test có `points.csv` (cột `group_id`, `x`, `y`) và `groups.csv` (cột `group_id`).

## Kết quả

Nội dung CSV với dòng đầu `group_id,n,y_mean,y_std,x_min,x_max`.

## Giới hạn

- `points.csv` có không quá $300$ dòng, `groups.csv` không quá $30$ dòng.
- Mã nhóm là số nguyên từ $1$ đến $1999$, $0\le x\le10$ và $|y|\le100$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Mã nhóm, thứ tự và các ô trống phải đúng, các số được chấm với sai số khoảng $10^{-6}$.

## Ví dụ

```input
points.csv:
group_id,x,y
2,0.0,1.0
1,1.0,3.0
2,1.0,3.0
1,2.0,5.0
2,2.0,5.0
3,4.0,10.0
1,3.0,7.0
9,0.0,0.0

groups.csv:
group_id
2
1
3
5
```

```output
group_id,n,y_mean,y_std,x_min,x_max
2,3,3.0,2.0,0.0,2.0
1,3,5.0,2.0,1.0,3.0
3,1,10.0,,4.0,4.0
5,0,,,,
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.csv`, `02.csv`, …, `20.csv`. Nộp tệp ZIP ấy, chọn **Output**.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 2, Ngày 2, Bài 5](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-2-day-2-problems.pdf#page=11).
:::
