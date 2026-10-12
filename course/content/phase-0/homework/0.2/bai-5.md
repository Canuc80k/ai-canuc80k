# Khoảng cách

Hai tập điểm $A$ và $B$ có $n$ và $m$ điểm trong không gian $d$ chiều. Hãy tính **bình phương khoảng cách** giữa mọi cặp điểm, rồi tìm cho mỗi điểm của $A$ điểm gần nhất trong $B$. Đây là bước chính của thuật toán láng giềng gần nhất ở bài 2.4.

$$
D_{ij}=\sum_{k}(A_{ik}-B_{jk})^2.
$$

Ở đây ta giữ bình phương, không lấy căn. Nếu nhiều điểm trong $B$ cùng gần nhất thì lấy điểm có chỉ số nhỏ nhất, `argmin` của NumPy làm sẵn việc này.

Cách tính không vòng lặp là `diff = A[:, None, :] - B[None, :, :]`, một mảng shape $(n, m, d)$. Mảng trung gian này có thể rất lớn, nên hãy tính luôn nó chiếm bao nhiêu byte khi dùng `float64`, mỗi phần tử $8$ byte.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `A` (ma trận $n\times d$) và `B` (ma trận $m\times d$).

## Kết quả

Một đối tượng JSON gồm `distance_squared` (ma trận $n\times m$), `nearest` ($n$ chỉ số) và `intermediate_bytes` (số byte của `diff`).

## Giới hạn

- $1\le n\le120$, $1\le m\le100$, $1\le d\le16$, tọa độ là số nguyên trong $[-100, 100]$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"A": [[0, 0], [3, 4]], "B": [[0, 4], [3, 0]]}
```

```output
{
  "distance_squared": [[16.0, 9.0], [9.0, 16.0]],
  "nearest": [1, 0],
  "intermediate_bytes": 64
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
