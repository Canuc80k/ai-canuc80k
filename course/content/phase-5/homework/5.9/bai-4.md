# Integrated gradients

Gradient tại đúng một điểm chỉ cho biết mô hình nhạy thế nào quanh điểm ấy. Khi mô hình đã bão hòa, gradient gần $0$ dù đặc trưng rất quan trọng. Integrated gradients sửa điều này: cộng gradient dọc đường thẳng từ một đầu vào gốc $x'$ (baseline) tới $x$.

Mô hình: $f(x)=\sum_j v_j\tanh\big(\sum_i W_{ji}x_i+b_j\big)+c$ với $W$ là `W1`, $b$ là `b1`, $v$ là `w2`, $c$ là `b2`.

Với số bước $m$, dùng tổng Riemann điểm giữa:
$$\mathrm{IG}_i=(x_i-x'_i)\cdot\frac1m\sum_{k=1}^{m}\frac{\partial f}{\partial x_i}\Big(x'+\tfrac{k-1/2}{m}(x-x')\Big).$$

Khi $m$ đủ lớn, tổng các $\mathrm{IG}_i$ xấp xỉ $f(x)-f(x')$. Đây là tính đầy đủ (completeness) của phương pháp, và độ lệch cho biết $m$ đã đủ chưa.

Với mỗi $m$ trong `steps`, hãy báo các $\mathrm{IG}_i$, tổng của chúng và độ lệch $\big|\sum_i\mathrm{IG}_i-(f(x)-f(x'))\big|$. Thêm $f(x)$, $f(x')$, và gradient nhân đầu vào $x_i\cdot\partial f/\partial x_i(x)$ để so sánh.

## Dữ liệu vào

Một đối tượng JSON gồm `W1`, `b1`, `w2`, `b2`, `x`, `baseline` và `steps`.

## Kết quả

Một đối tượng JSON gồm `f_x`, `f_baseline`, `gradient_x_input` và `runs`: với mỗi $m$, theo thứ tự trong `steps`, là `{"attributions", "sum", "gap"}`.

## Giới hạn

- Không quá $5$ đầu vào, $6$ nơ-ron ẩn, $m\le100$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "W1": [[2.0, 0.0], [0.0, 1.0]],
  "b1": [0.0, 0.0],
  "w2": [1.0, 1.0],
  "b2": 0.0,
  "x": [2.0, 0.5],
  "baseline": [0.0, 0.0],
  "steps": [1, 4, 32]
}
```

```output
{
  "f_x": 1.4614464569990768,
  "f_baseline": 0.0,
  "gradient_x_input": [0.005363802732103462, 0.3932238664829637],
  "runs": [
    {
      "attributions": [0.2826032994126577, 0.470007424403189],
      "sum": 0.7526107238158467,
      "gap": 0.7088357331832301
    },
    {
      "attributions": [0.9973874832932239, 0.4625915517633054],
      "sum": 1.4599790350565294,
      "gap": 0.0014674219425474533
    },
    {
      "attributions": [0.9993310414347314, 0.4621245515687447],
      "sum": 1.461455593003476,
      "gap": 9.136004399223907e-06
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
