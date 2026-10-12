# Grad-CAM

Hai cách vẽ bản đồ "mô hình nhìn vào đâu": gradient theo từng điểm ảnh (saliency), và Grad-CAM trên feature map của lớp conv. Bài này tính cả hai trên một CNN tí hon có trọng số cho sẵn.

Mô hình, kiểu `float64`:

1. Ảnh $4\times4$, một kênh. Conv `weight` (shape $2\times1\times2\times2$) với `bias`, không padding, ra hai feature map $3\times3$; áp ReLU, gọi là $A_1, A_2$.
2. Trung bình toàn cục mỗi feature map, rồi $\text{logit}=\sum_k h_k\cdot\operatorname{mean}(A_k)$ với $h$ là `head` (không bias).

Hãy báo:

- `saliency`: đạo hàm của logit theo từng điểm ảnh ($4\times4$, giữ dấu).
- `gradcam`: với mỗi kênh $k$, $\alpha_k$ là trung bình của $\partial\text{logit}/\partial A_k$ trên $3\times3$ vị trí; bản đồ là $\operatorname{ReLU}\big(\sum_k\alpha_kA_k\big)$, kích thước $3\times3$, không chuẩn hóa, không phóng to.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `image`, `weight`, `bias` và `head`.

## Kết quả

Một đối tượng JSON gồm `logit`, `saliency` và `gradcam`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "image": [
    [
      1.289783100746931, -0.765081991960241, 1.4560578817097856,
      -0.8821181980482352
    ],
    [
      -0.4104847159477657, -1.4851507532066648, -0.5892784016791289,
      -0.2716929192408032
    ],
    [
      -0.010106959976554775, -0.47104944812554067, -0.3558338500967358,
      1.2623480500983235
    ],
    [
      -1.3931907823379561, -0.5073753688097151, -0.20623172431934741,
      1.2782926762375186
    ]
  ],
  "weight": [
    [
      [
        [0.8102370279700551, -0.20118003061009954],
        [0.00568157068009179, -0.7472016740350412]
      ]
    ],
    [
      [
        [1.0909480568870638, 0.05599854939433933],
        [0.16638281980102984, -1.661624957471365]
      ]
    ]
  ],
  "bias": [0.2, -0.1],
  "head": [0.7, -0.4]
}
```

```output
{
  "logit": 0.15601238365470635,
  "saliency": [
    [
      0.01453185520269034, -0.01813616013164504, 0.01453185520269034,
      -0.01813616013164504
    ],
    [
      0.00757896315331838, -0.0024018477800875743,
      -0.006952892049371965, 0.015734312351557464
    ],
    [
      0.00757896315331838, 0.06061658772869449, -0.01564733571411885,
      0.0
    ],
    [
      -0.006952892049371965, 0.01617621229334238, -0.05811568575828098,
      0.0
    ]
  ],
  "gradcam": [
    [0.032104820860757666, 0, 0.05697974705744377],
    [0.0336284608765472, 0, 0],
    [0.030099657923646304, 0.003199696936311372, 0]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
