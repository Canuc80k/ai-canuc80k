# NT-Xent

SimCLR lấy $N$ ảnh, tạo hai view cho mỗi ảnh, được $2N$ view. Với mỗi view, positive là view còn lại của cùng ảnh; **mọi** $2N-2$ view khác đều là negative, kể cả các view cùng phía. Loss này có tên NT-Xent.

Đánh số view: $0,\dots,N-1$ là `view_a`, $N,\dots,2N-1$ là `view_b`. View $i$ và view $i+N$ là một cặp.

1. Chuẩn hóa mọi view về độ dài $1$ (chia cho $\max(\lVert v\rVert,10^{-12})$).
2. $S_{ij}=z_i\cdot z_j/\tau$ với mọi $i,j$ (kể cả $i=j$), $\tau$ là `temperature`.
3. Loss của view $i$: cross-entropy trên các $S_{ij}$ với $j\ne i$ (bỏ chính nó), đáp án là positive $p(i)$:
$$\ell_i=-\log\frac{e^{S_{i,p(i)}}}{\sum_{j\ne i}e^{S_{ij}}}.$$
4. `loss` là trung bình của $2N$ giá trị $\ell_i$.

Thêm vài con số để đọc loss:

- `positive_probability`: xác suất softmax mà view $i$ dành cho positive, tức $e^{-\ell_i}$.
- `pair_accuracy`: tỉ lệ view mà positive có điểm cao nhất trong các view khác.
- `chance_loss`: loss khi mọi điểm bằng nhau, $\log(2N-1)$.

## Dữ liệu vào

Một đối tượng JSON gồm `view_a`, `view_b` (mỗi cái $N$ vector) và `temperature`.

## Kết quả

Một đối tượng JSON gồm `similarity` ($2N\times2N$), `per_view_loss`, `loss`, `positive_probability`, `pair_accuracy` và `chance_loss`.

## Giới hạn

- $N\le5$, mỗi vector không quá $4$ số. Với mỗi view, điểm cao nhất và nhì (trong các view khác) cách nhau ít nhất $10^{-6}$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "view_a": [[1, 0], [0, 1], [-1, 0]],
  "view_b": [[0.9, 0.2], [0.3, 1], [-1, -0.4]],
  "temperature": 0.5
}
```

```output
{
  "similarity": [
    [
      2.0, 0.0, -2.0, 1.9523741203679055, 0.5746957711326908,
      -1.8569533817705184
    ],
    [
      0.0, 2.0, 0.0, 0.4338609156373124, 1.9156525704423026,
      -0.7427813527082073
    ],
    [
      -2.0, 0.0, 2.0, -1.9523741203679055, -0.5746957711326908,
      1.8569533817705184
    ],
    [
      1.9523741203679055, 0.4338609156373124, -1.9523741203679055, 2.0,
      0.9765739644497053, -1.9738657615513637
    ],
    [
      0.5746957711326908, 1.9156525704423026, -0.5746957711326908,
      0.9765739644497053, 1.9999999999999998, -1.245047131643077
    ],
    [
      -1.8569533817705184, -0.7427813527082073, 1.8569533817705184,
      -1.9738657615513637, -1.245047131643077, 1.9999999999999993
    ]
  ],
  "per_view_loss": [
    0.36149380358908045, 0.4648525623009326, 0.25257400108403716,
    0.4921268890679999, 0.5754105821020217, 0.15300119846717042
  ],
  "loss": 0.38324317276854036,
  "positive_probability": [
    0.6966349126983017, 0.6282277228117502, 0.7767987267644645,
    0.6113247904778716, 0.5624738796823482, 0.8581286933717105
  ],
  "pair_accuracy": 1.0,
  "chance_loss": 1.6094379124341003
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
