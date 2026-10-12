# Gradient MSE

Đây là một câu trong đề thi USA-NA-AIO. Viết hàm `my_fun_derivative(X, y, theta)` nhận mảng NumPy `X` shape $(N, d)$, `y` shape $(N,)$ và `theta` shape $(d,)$, rồi trả về gradient theo $\theta$ của

$$
\frac1N\sum_{n=0}^{N-1}\left(y_n-\theta^\top X_n\right)^2,
$$

dưới dạng mảng shape $(d,)$.

Đề gốc có luật chơi chặt. Trong hàm không được dùng vòng lặp, không được dùng `@`, `.T` hay bất cứ thứ gì trong `np.linalg`, và không thêm `import`. Hãy làm bằng phép nhân từng phần tử, broadcasting và `np.sum`, `np.mean` với `axis`.

Bộ kit có sẵn khung hàm. Hàm `solve` gọi `my_fun_derivative` và ghi kết quả ra tệp.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X`, `y`, `theta`.

## Kết quả

Một đối tượng JSON `{"gradient": [...]}` gồm $d$ số.

## Giới hạn

- $1\le N\le16$, $1\le d\le4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$. Giáo viên xem code để kiểm luật không vòng lặp.

## Ví dụ

```input
{
  "X": [[-0.2568641432313081]],
  "y": [-0.4608150955572951],
  "theta": [1.7755447707971468]
}
```

```output
{"gradient": [-0.0024357446702507773]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::

::: note Nguồn
Đề thi [USA-NA-AIO 2026, Vòng 1, câu 4.2](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=8).
:::
