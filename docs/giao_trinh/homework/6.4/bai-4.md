# Attention nhân quả

Một đầu self-attention của mô hình ngôn ngữ nhân quả: token ở vị trí $i$ chỉ được nhìn các vị trí $j\le i$, và không ai được nhìn token đệm. Bài này tính attention ấy theo hai cách, có và không chia cho $\sqrt d$, để thấy vì sao phải chia.

Có $T$ vị trí, mỗi vị trí có vector query, key (cùng độ dài $d$) và value. `padding_mask[i]` là `true` nếu vị trí $i$ là token thật.

1. `allowed[i][j]` là `true` khi $j\le i$ và cả vị trí $i$ lẫn $j$ đều là token thật.
2. Với hệ số $c$: điểm $s_{ij}=c\cdot(q_i\cdot k_j)$ ở các ô được phép. Trọng số là softmax của các điểm trên hàng $i$, chỉ lấy các ô được phép; ô không được phép có trọng số $0$. Hàng không có ô nào được phép thì mọi trọng số bằng $0$ và đầu ra bằng vector $0$.
3. Đầu ra ở vị trí $i$ là $\sum_j w_{ij}v_j$.
4. Làm với $c=1/\sqrt d$ (`scaled`) và với $c=1$ (`unscaled`). Với mỗi cách, báo thêm trọng số lớn nhất của mỗi hàng.

## Dữ liệu vào

Một đối tượng JSON gồm `Q`, `K`, `V` (mỗi cái $T$ vector) và `padding_mask`.

## Kết quả

Một đối tượng JSON gồm `allowed`, `scaled` và `unscaled`; mỗi cách là `{"weights", "output", "max_weight"}`.

## Giới hạn

- $T\le6$, $d\le16$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "Q": [[1, 0, 1, 0], [2, 2, 0, 1], [3, 1, 2, 2], [0, 0, 0, 0]],
  "K": [[1, 1, 0, 0], [0, 2, 1, 1], [2, 0, 2, 1], [1, 1, 1, 1]],
  "V": [[1, 0], [0, 1], [1, 1], [5, 5]],
  "padding_mask": [true, true, true, false]
}
```

```output
{
  "allowed": [
    [true, false, false, false],
    [true, true, false, false],
    [true, true, true, false],
    [false, false, false, false]
  ],
  "scaled": {
    "weights": [
      [1.0, 0.0, 0.0, 0.0],
      [0.37754066879814546, 0.6224593312018546, 0.0, 0.0],
      [
        0.017147825545520388, 0.0466126225779739, 0.9362395518765058,
        0.0
      ],
      [0.0, 0.0, 0.0, 0.0]
    ],
    "output": [
      [1.0, 0.0],
      [0.37754066879814546, 0.6224593312018546],
      [0.9533873774220262, 0.9828521744544797],
      [0.0, 0.0]
    ],
    "max_weight": [1.0, 0.6224593312018546, 0.9362395518765058, 0.0]
  },
  "unscaled": {
    "weights": [
      [1.0, 0.0, 0.0, 0.0],
      [0.26894142136999516, 0.7310585786300049, 0.0, 0.0],
      [
        0.00033452121335145586, 0.002471796011736256,
        0.9971936827749123, 0.0
      ],
      [0.0, 0.0, 0.0, 0.0]
    ],
    "output": [
      [1.0, 0.0],
      [0.26894142136999516, 0.7310585786300049],
      [0.9975282039882637, 0.9996654787866486],
      [0.0, 0.0]
    ],
    "max_weight": [1.0, 0.7310585786300049, 0.9971936827749123, 0.0]
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 17–18](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=26).
:::
