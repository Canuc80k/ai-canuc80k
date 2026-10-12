# Gộp BatchNorm

Khi suy luận, BatchNorm chỉ còn là một phép biến đổi tuyến tính cố định theo từng kênh, dùng running mean và running var đã lưu. Vì vậy có thể gộp nó vào conv đứng trước, bỏ hẳn một lớp mà kết quả không đổi.

Conv có trọng số $W$ (shape `(O, C, k, k)`) và bias $b$, stride $1$, không padding. BatchNorm ở chế độ eval với tham số $\gamma$, $\beta$, running mean $\mu$, running var $\sigma^2$ và `eps` cho mỗi kênh ra $o$:

$$
\text{BN}(y_o)=\gamma_o\,\frac{y_o-\mu_o}{\sqrt{\sigma_o^2+\text{eps}}}+\beta_o .
$$

Hãy tìm trọng số $W'$ và bias $b'$ của một conv duy nhất cho đúng $\text{BN}(\text{conv}(X))$, rồi chạy conv đã gộp trên ảnh $X$. Thêm `max_abs_diff`: độ lệch tuyệt đối lớn nhất giữa đầu ra của conv đã gộp và của conv rồi BatchNorm.

## Dữ liệu vào

Một đối tượng JSON gồm `X` (shape `(C, H, W)`), `weight`, `bias`, `gamma`, `beta`, `mean`, `var` và `eps`.

## Kết quả

Một đối tượng JSON gồm `fused_weight`, `fused_bias`, `output` (shape `(O, H-k+1, W-k+1)`) và `max_abs_diff`.

## Giới hạn

- $C\le2$, $O\le3$, $k\le3$, ảnh không quá $5\times5$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[[1.0, 2.0, 0.0], [0.0, 1.0, 3.0], [2.0, 0.0, 1.0]]],
  "weight": [[[[1.0, 0.0], [0.0, 1.0]]]],
  "bias": [0.5],
  "gamma": [2.0],
  "beta": [-1.0],
  "mean": [2.0],
  "var": [3.99999],
  "eps": 1e-05
}
```

```output
{
  "fused_weight": [[[[1.0, 0.0], [0.0, 1.0]]]],
  "fused_bias": [-2.5],
  "output": [[[-0.5, 2.5], [-2.5, -0.5]]],
  "max_abs_diff": 0.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
