# Hạng thấp

Có $N$ từ, mỗi từ được biểu diễn bằng một vector $m$ chiều, xếp thành ma trận $W$ cỡ $N\times m$. Độ giống giữa hai từ là tích vô hướng của hai vector, nên cả bảng độ giống là $S=WW^\top$, cỡ $N\times N$.

Muốn tiết kiệm bộ nhớ, ta chỉ giữ $r$ cột: thay $W$ bằng một ma trận $W_r$ cỡ $N\times r$ rồi dùng $S_r=W_rW_r^\top$. Sai số được đo bằng

$$
\frac{\lVert S-S_r\rVert_F^2}{\lVert S\rVert_F^2},
$$

trong đó $\lVert A\rVert_F^2$ là tổng bình phương mọi phần tử của $A$.

Cách chọn $W_r$ tốt nhất đi qua phân tích SVD $W=U\Sigma V^\top$, với các giá trị kỳ dị $\sigma_1\ge\sigma_2\ge\dots\ge\sigma_m$: lấy $W_r$ là $r$ cột đầu của $U$, cột thứ $i$ nhân với $\sigma_i$.

Hãy tính:

- Các giá trị kỳ dị của $W$.
- Sai số nhỏ nhất ứng với mỗi $r$ từ $1$ đến $m$.
- Số $r$ nhỏ nhất có sai số không quá `threshold`.
- Ma trận $S_r$ với $r$ cho trong dữ liệu.

Trước khi viết code, hãy tự tìm công thức của sai số theo các $\sigma_i$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `W`, `r` và `threshold`.

## Kết quả

Một đối tượng JSON gồm `singular_values` ($m$ số, giảm dần), `errors` ($m$ số, ứng với $r=1,\dots,m$), `smallest_r` và `S_r`.

## Giới hạn

- $3\le N\le10$ và $2\le m\le\min(N,6)$. Các giá trị kỳ dị khác nhau đủ xa để $S_r$ xác định duy nhất.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"W": [[3, 1], [3, -1], [0, 2]], "r": 1, "threshold": 0.2}
```

```output
{
  "singular_values": [4.242640687119285, 2.449489742783178],
  "errors": [0.09999999999999998, 1.2482466888343529e-32],
  "smallest_r": 1,
  "S_r": [
    [8.999999999999995, 9.0, 0.0],
    [9.000000000000002, 9.000000000000007, 0.0],
    [0.0, 0.0, 0.0]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 5.14](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=14).
:::
