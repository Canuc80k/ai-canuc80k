# Chuẩn hóa

Một bảng dữ liệu có $n$ hàng, $d$ cột. Mỗi hàng là một mẫu, mỗi cột là một đặc trưng. Các cột có thang đo rất khác nhau, nên trước khi đưa vào model, ta chuẩn hóa **từng cột** về trung bình $0$, độ lệch chuẩn $1$.

Với cột $j$, trung bình và độ lệch chuẩn tính như sau, chia cho $n$:

$$
\mu_j=\frac1n\sum_{i}X_{ij},\qquad
\sigma_j=\sqrt{\frac1n\sum_{i}(X_{ij}-\mu_j)^2}.
$$

Giá trị chuẩn hóa là $Z_{ij}=(X_{ij}-\mu_j)/\sigma_j$. Cột có mọi giá trị bằng nhau thì $\sigma_j=0$. Khi ấy ta chia cho $1$, cả cột thành số $0$.

`np.std` mặc định chia cho $n$, đúng công thức trên. Một số thư viện khác chia cho $n-1$, nên khi dùng cần để ý.

## Dữ liệu vào

Mỗi tệp `input.json` có trường `X`, ma trận $n\times d$.

## Kết quả

Một đối tượng JSON gồm `mean` ($d$ giá trị $\mu_j$), `std` ($d$ giá trị $\sigma_j$, kể cả khi bằng $0$) và `normalized` (ma trận $Z$).

## Giới hạn

- $1\le n\le128$, $1\le d\le12$, các phần tử là số nguyên trong $[-1000, 1000]$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"X": [[1, 10], [3, 10]]}
```

```output
{
  "mean": [2.0, 10.0],
  "std": [1.0, 0.0],
  "normalized": [[-1.0, 0.0], [1.0, 0.0]]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
