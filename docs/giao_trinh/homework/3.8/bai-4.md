# Lan truyền ngược

RNN đọc chuỗi từng bước và mang theo một trạng thái ẩn. Bài này chạy một RNN nhỏ bằng tay, rồi lan truyền ngược qua thời gian để xem gradient yếu đi thế nào khi lùi về các bước đầu.

Với trạng thái ban đầu $h_0$ và các đầu vào $x_1,\dots,x_T$:

$$
h_t=\tanh\!\left(W_hh_{t-1}+W_xx_t+b\right),\qquad \hat y=v\cdot h_T,\qquad L=\tfrac12(\hat y-y)^2.
$$

Hãy tính:

- `hidden`: các trạng thái $h_1,\dots,h_T$.
- `loss`: $L$.
- `grad_W_x`, `grad_W_h`, `grad_b`, `grad_v`: đạo hàm của $L$ theo các tham số, cùng shape với tham số. Ma trận dùng chung ở mọi bước, nên gradient của nó là tổng phần đóng góp của các bước.
- `state_grad_norms`: với $t=0,1,\dots,T$, độ dài $\lVert\partial L/\partial h_t\rVert$ (chuẩn Euclid).

## Dữ liệu vào

Một đối tượng JSON gồm `W_x` ($H\times D$), `W_h` ($H\times H$), `b`, `v`, `h0` ($H$ số), `xs` ($T$ bước, mỗi bước $D$ số) và `y`.

## Kết quả

Một đối tượng JSON gồm `hidden`, `loss`, `grad_W_x`, `grad_W_h`, `grad_b`, `grad_v` và `state_grad_norms`.

## Giới hạn

- $H\le3$, $D\le2$, $T\le12$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "W_x": [[0.5], [-0.3]],
  "W_h": [[0.4, 0.1], [-0.2, 0.3]],
  "b": [0.0, 0.1],
  "v": [1.0, -1.0],
  "h0": [0.0, 0.0],
  "xs": [[1.0], [0.5], [-1.0], [2.0], [0.0], [1.0]],
  "y": 0.5
}
```

```output
{
  "hidden": [
    [0.46211715726000974, -0.19737532022490398],
    [0.3928023254371852, -0.19894710404309462],
    [-0.34765491188716574, 0.2559366867252093],
    [0.7096764444119902, -0.3396421956578316],
    [0.2448306357017102, -0.14284432130225422],
    [0.5253116858123725, -0.2838085489783002]
  ],
  "loss": 0.047777659778520325,
  "grad_W_x": [[0.281090762801378], [-0.29276351417876234]],
  "grad_W_h": [
    [0.14753038878660216, -0.07340195354451004],
    [-0.11026947068072619, 0.05971649561324862]
  ],
  "grad_b": [0.4121848433920447, -0.3454002691850093],
  "grad_v": [0.16238447165660472, -0.0877309652957723],
  "state_grad_norms": [
    0.0004127929469794151, 0.0015154937696386871, 0.004958099123745305,
    0.014361976684828592, 0.06752455953773466, 0.15930808372099992,
    0.43716202844492486
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
