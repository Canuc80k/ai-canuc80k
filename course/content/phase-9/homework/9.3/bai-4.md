# Lan truyền ngược

Một mạng nhỏ có hai input $x_1, x_2$, sáu trọng số $w_A,\dots,w_F$ và không có bias:

$$z_1=w_Ax_1+w_Bx_2,\quad a_1=g(z_1),$$
$$z_2=w_Ca_1,\quad a_2=g(z_2),\qquad z_3=w_Da_1,\quad a_3=g(z_3),$$
$$z_4=w_Ea_2+w_Fa_3,\quad\hat y=g(z_4),$$

với $g(z)=1/(1+e^{-z})$ là sigmoid và loss $\ell=\frac12(\hat y-y)^2$. Nút $a_1$ đi vào cả hai nhánh $a_2$ và $a_3$.

Một bạn đã tự tính gradient và nộp các giá trị `claimed`. Hãy tính $\hat y$, $\ell$, gradient đúng $\partial\ell/\partial w_k$ cho cả sáu trọng số, và chỉ ra những trọng số mà `claimed` lệch khỏi gradient đúng quá $10^{-6}$.

## Dữ liệu vào

Một đối tượng JSON gồm `x` (hai số), `y` ($0$ hoặc $1$), `w` và `claimed` (mỗi cái ánh xạ `"A"`..`"F"` tới một số).

## Kết quả

Một đối tượng JSON gồm `y_hat`, `loss`, `grad` (ánh xạ `"A"`..`"F"`) và `wrong` (list tên trọng số, sắp theo thứ tự chữ cái).

## Giới hạn

- Trong mọi test, một giá trị `claimed` hoặc lệch không quá $10^{-7}$, hoặc lệch ít nhất $10^{-3}$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [1.0, 2.0],
  "y": 1,
  "w": {"A": 0.5, "B": -0.25, "C": 1.0, "D": -1.0, "E": 2.0, "F": 1.0},
  "claimed": {
    "A": -0.002667245,
    "B": -0.002667245,
    "C": -0.005334491,
    "D": -0.002667245,
    "E": -0.01412958,
    "F": -0.008570023
  }
}
```

```output
{
  "y_hat": 0.8351340224322011,
  "loss": 0.013590395279692979,
  "grad": {
    "A": -0.0013336227404521504,
    "B": -0.002667245480991037,
    "C": -0.005334490960073878,
    "D": -0.002667245480036939,
    "E": -0.014129579673297086,
    "F": -0.00857002327948539
  },
  "wrong": ["A"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
