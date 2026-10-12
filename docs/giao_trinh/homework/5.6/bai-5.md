# Ghép tile

Ảnh hiển vi hay ảnh vệ tinh có thể lớn tới mức không vừa bộ nhớ GPU. Cách thường dùng là cắt ảnh thành từng mảnh (tile), dự đoán từng mảnh rồi ghép lại. Nhưng điểm ảnh sát mép mảnh thiếu ngữ cảnh ở một phía, nên kết quả ghép có thể khác kết quả chạy trên cả ảnh. Bài này đo sự khác biệt ấy.

**Mô hình.** Áp lần lượt các kernel $3\times3$ trong `kernels` lên ảnh một kênh. Mỗi lớp là tương quan chéo (như `Conv2d`, không lật kernel), đệm $0$ quanh viền để giữ nguyên cỡ, không bias:
$$Y[i][j]=\sum_{a=0}^{2}\sum_{b=0}^{2}K[a][b]\cdot X[i+a-1][j+b-1],$$
với $X$ ngoài ảnh coi là $0$. Sau mỗi lớp trừ lớp cuối, áp ReLU.

**Chia mảnh với lề $m$.** Theo mỗi chiều, chia các chỉ số $0,1,\dots,n-1$ thành các đoạn lõi dài `core` (đoạn cuối có thể ngắn hơn). Mỗi đoạn lõi $[s,e)$ được nới thêm $m$ mỗi bên thành $[\max(0,s-m),\ \min(n,e+m))$. Mỗi mảnh là tích của một đoạn nới theo hàng và một đoạn nới theo cột. Chạy mô hình **riêng trên từng mảnh** (đệm $0$ quanh viền của mảnh), rồi chỉ chép phần lõi vào kết quả ghép.

Với mỗi lề $m=0,1,\dots,$ `max_margin`, hãy báo:

- `max_error`: sai lệch tuyệt đối lớn nhất giữa kết quả ghép và kết quả chạy trên cả ảnh.
- `processed_pixels`: tổng số điểm ảnh của mọi mảnh, cho biết lề làm tăng khối lượng tính bao nhiêu.

Thêm `full` (kết quả chạy trên cả ảnh) và `smallest_exact_margin`: lề nhỏ nhất có sai lệch dưới $10^{-9}$, hoặc $-1$ nếu không có.

## Dữ liệu vào

Một đối tượng JSON gồm `image`, `kernels`, `core` và `max_margin`.

## Kết quả

Một đối tượng JSON gồm `full`, `max_error`, `processed_pixels` và `smallest_exact_margin`.

## Giới hạn

- Ảnh không quá $12\times12$, không quá $4$ kernel, $2\le$ `core` $\le5$, `max_margin` $\le5$.
- Với mọi lề, sai lệch hoặc dưới $10^{-9}$, hoặc trên $10^{-3}$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "image": [
    [0.0, 5.0, 3.0, 1.0, 6.0, 4.0, 2.0, 0.0],
    [3.0, 1.0, 6.0, 4.0, 2.0, 0.0, 5.0, 3.0],
    [6.0, 4.0, 2.0, 0.0, 5.0, 3.0, 1.0, 6.0],
    [2.0, 0.0, 5.0, 3.0, 1.0, 6.0, 4.0, 2.0],
    [5.0, 3.0, 1.0, 6.0, 4.0, 2.0, 0.0, 5.0],
    [1.0, 6.0, 4.0, 2.0, 0.0, 5.0, 3.0, 1.0],
    [4.0, 2.0, 0.0, 5.0, 3.0, 1.0, 6.0, 4.0],
    [0.0, 5.0, 3.0, 1.0, 6.0, 4.0, 2.0, 0.0]
  ],
  "kernels": [
    [[0, 0.25, 0], [0.25, 0, 0.25], [0, 0.25, 0]],
    [[0.1, 0.2, 0.1], [0.2, -0.4, 0.2], [0.1, 0.2, 0.1]]
  ],
  "core": 4,
  "max_margin": 3
}
```

```output
{
  "full": [
    [
      0.19999999999999996, 1.9250000000000003, 0.8250000000000001,
      0.7250000000000001, 1.675, 1.225, 0.675, 0.65
    ],
    [
      1.375, 0.8, 2.7000000000000006, 2.7, 1.4749999999999999, 1.65,
      2.775, 0.425
    ],
    [1.25, 2.75, 1.7750000000000001, 1.925, 3.475, 2.4, 1.1, 1.975],
    [
      0.8750000000000001, 1.7, 3.475, 2.4, 1.3250000000000002,
      2.8750000000000004, 2.8500000000000005, 0.19999999999999987
    ],
    [
      1.9000000000000001, 2.225, 1.3250000000000002,
      2.8750000000000004, 3.0250000000000004, 1.7750000000000001,
      1.6250000000000002, 2.275
    ],
    [
      0.12500000000000003, 2.575, 3.0250000000000004,
      1.7750000000000001, 1.925, 3.475, 1.9749999999999999, 0.5
    ],
    [
      2.025, 1.075, 1.5000000000000002, 3.0750000000000006, 2.2,
      1.1500000000000001, 2.1750000000000003, 1.25
    ],
    [
      -0.12499999999999999, 1.425, 1.5749999999999997,
      0.24999999999999994, 1.5499999999999998, 1.4500000000000002,
      0.875, 0.5
    ]
  ],
  "max_error": [2.0250000000000004, 0.6249999999999998, 0.0, 0.0],
  "processed_pixels": [64, 100, 144, 196],
  "smallest_exact_margin": 2
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
