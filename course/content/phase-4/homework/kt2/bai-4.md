# Gradient tắt dần

Khi huấn luyện một mạng sâu, chuẩn gradient ở lớp đầu chỉ cỡ $0.0003$ trong khi ở lớp cuối cỡ $0.85$. Các lớp đầu gần như không học. Bài này tái hiện hiện tượng ấy, và xem kết nối tắt (residual) thay đổi điều gì.

Mạng có $L$ lớp, mỗi lớp một ma trận $W_l$ cỡ $d\times d$, activation $f$ là `sigmoid` hoặc `tanh`. Với đầu vào $h_0=x$:

- Mạng thường: $h_l=f(W_lh_{l-1})$.
- Mạng có kết nối tắt: $h_l=h_{l-1}+f(W_lh_{l-1})$.

Loss là $\tfrac12\lVert h_L-y\rVert^2$. Với mỗi mạng, hãy tính chuẩn Frobenius của gradient theo từng $W_l$, rồi báo **log cơ số $10$** của các chuẩn ấy (để thấy rõ cả những số rất nhỏ). Thêm `drop`: log của lớp cuối trừ log của lớp đầu, tức gradient lớp đầu nhỏ hơn lớp cuối bao nhiêu bậc.

## Dữ liệu vào

Một đối tượng JSON gồm `weights` (list $L$ ma trận), `activation`, `x` và `y`.

## Kết quả

Một đối tượng JSON gồm `log10_plain`, `log10_residual` ($L$ số mỗi trường, theo thứ tự lớp $1$ tới $L$), `drop_plain` và `drop_residual`.

## Giới hạn

- $d\le4$, $L\le12$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "weights": [
    [
      [-0.088, -1.09, 0.869],
      [-0.291, -1.129, -0.202],
      [0.793, 1.701, 2.209]
    ],
    [
      [-0.397, -1.477, -0.981],
      [-0.456, -1.58, -2.374],
      [0.049, -0.99, 0.885]
    ],
    [
      [-0.612, 0.665, -0.287],
      [-0.966, -0.714, -1.267],
      [1.488, 1.276, -0.275]
    ],
    [
      [-0.39, -0.117, -0.057],
      [-1.18, -0.642, 0.294],
      [0.993, 0.499, 2.392]
    ],
    [
      [0.56, -0.47, 0.296],
      [0.411, 0.764, 0.087],
      [-0.985, -1.279, -0.433]
    ],
    [
      [1.096, 1.155, -0.063],
      [0.513, 0.849, 0.378],
      [0.931, 2.267, 1.369]
    ],
    [
      [-0.971, -0.767, 0.756],
      [0.063, 1.902, 0.086],
      [-1.554, 0.058, 1.063]
    ],
    [
      [1.295, -0.884, -1.308],
      [-0.443, -0.766, 1.407],
      [-0.433, -1.122, 0.596]
    ],
    [
      [0.566, 0.242, 1.362],
      [0.644, -0.055, -0.78],
      [-0.16, 0.159, 1.136]
    ],
    [
      [-1.45, -1.861, -0.346],
      [-0.1, 2.696, -0.949],
      [1.763, -1.293, -0.602]
    ]
  ],
  "activation": "sigmoid",
  "x": [0.305, -1.982, 1.327],
  "y": [1.327, 0.379, -1.239]
}
```

```output
{
  "log10_plain": [
    -5.441353934737578, -5.14853800258819, -4.91978440973616,
    -3.8312944041382706, -2.816616975105043, -2.34487728435424,
    -1.7215445029139582, -1.2473739180749805, -0.8465529097611183,
    -0.32752984719686773
  ],
  "log10_residual": [
    0.7414452520223159, 0.5399852919193822, 0.9560457124539293,
    0.16346744300952348, 0.3908912295802142, -0.3331349396176123,
    1.2182766006768126, 1.0952501642369232, 0.3694849965969781,
    1.2205893297993107
  ],
  "drop_plain": 5.113824087540711,
  "drop_residual": 0.47914407777699475
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 8](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=12).
:::
