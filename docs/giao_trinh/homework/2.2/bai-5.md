# L1 và L2

Phạt L1 (Lasso) và phạt L2 (Ridge) cùng mức $\lambda$, mô hình nào giữ ít trọng số khác $0$ hơn? Ta trả lời bằng số trong trường hợp đơn giản nhất: ma trận dữ liệu là ma trận đơn vị, và $z$ là lời giải khi không phạt.

Với mỗi $\lambda$, hãy tìm hai vector trọng số:

- Ridge cực tiểu $\lVert z-w\rVert^2+\lambda\lVert w\rVert^2$.
- Lasso cực tiểu $\frac12\lVert z-w\rVert^2+\lambda\lVert w\rVert_1$.

Hai bài toán đều tách được theo từng tọa độ, nên chỉ cần giải bài toán một biến cho mỗi $w_j$. Đếm số trọng số khác $0$ của mỗi mô hình. Cuối cùng, với mỗi $j$, cho biết $\lambda$ nhỏ nhất làm trọng số Lasso thứ $j$ bằng $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `z` và `lambdas` (tăng dần, không âm).

## Kết quả

Một đối tượng JSON gồm `ridge`, `lasso` (với mỗi $\lambda$, một vector), `ridge_nonzero`, `lasso_nonzero` (với mỗi $\lambda$, một số) và `lasso_zero_at` (với mỗi $j$, một số).

## Giới hạn

- $z$ có từ $1$ đến $12$ phần tử, mọi số có nhiều nhất một chữ số sau dấu phẩy.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"z": [3, 0.5, -1.2], "lambdas": [0, 0.5, 1, 2, 4]}
```

```output
{
  "ridge": [
    [3.0, 0.5, -1.2],
    [2.0, 0.3333333333333333, -0.8],
    [1.5, 0.25, -0.6],
    [1.0, 0.16666666666666666, -0.4],
    [0.6, 0.1, -0.24]
  ],
  "lasso": [
    [3.0, 0.5, -1.2],
    [2.5, 0.0, -0.7],
    [2.0, 0.0, -0.2],
    [1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0]
  ],
  "ridge_nonzero": [3, 3, 3, 3, 3],
  "lasso_nonzero": [3, 2, 2, 1, 0],
  "lasso_zero_at": [3.0, 0.5, 1.2]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 1.2](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=1).
:::
