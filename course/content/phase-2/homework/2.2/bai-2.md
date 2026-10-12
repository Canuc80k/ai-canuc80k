# Lasso

Khi ma trận dữ liệu là ma trận đơn vị, Lasso có lời giải rất gọn. Ta tìm $w$ cực tiểu

$$
\frac12\lVert z-w\rVert^2+\lambda\lVert w\rVert_1 .
$$

Mỗi trọng số được tính riêng: dịch $z_j$ về phía $0$ một khoảng $\lambda$, và nếu vượt qua $0$ thì dừng ở đúng $0$. Đây là phép soft-thresholding trong mục Lasso của bài học.

Hãy tính $w$ và đếm số trọng số bằng đúng $0$. Có thể kiểm bằng `Lasso` của scikit-learn với `X = np.eye(d)`, `y = z`, `fit_intercept=False`. `Lasso` chia phần sai số cho số mẫu, nên phải truyền `alpha=lambda/d` thì mới đúng bài toán trên.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `z` ($d$ số) và `lambda`.

## Kết quả

Một đối tượng JSON gồm `weights` và `zero_count`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"z": [0, 1.0, -1.0, 0.5, -0.5, 2.0, -3.0], "lambda": 1.0}
```

```output
{"weights": [0.0, 0.0, -0.0, 0.0, -0.0, 1.0, -2.0], "zero_count": 5}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
