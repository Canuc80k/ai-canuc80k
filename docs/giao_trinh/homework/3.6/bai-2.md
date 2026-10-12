# BatchNorm

BatchNorm có hai chế độ. Khi học, nó chuẩn hóa bằng trung bình và phương sai của chính batch, đồng thời cập nhật hai trung bình trượt `running_mean`, `running_var`. Khi suy luận, nó dùng hai trung bình trượt ấy.

Hãy dùng `nn.BatchNorm1d(2, affine=False, momentum=..., eps=...)` kiểu `float64`, ban đầu `running_mean` bằng $0$ và `running_var` bằng $1$:

1. Ở chế độ `train`, cho lần lượt các batch trong `batches` đi qua. Giữ lại đầu ra của batch cuối.
2. Chuyển sang `eval` và chuẩn hóa các hàng trong `queries`.

Hai chỗ dễ nhầm: khi chuẩn hóa batch, phương sai chia cho $n$; khi cập nhật `running_var`, phương sai của batch chia cho $n-1$. Và `momentum` là trọng số của batch mới: $\text{running}\leftarrow(1-\text{momentum})\cdot\text{running}+\text{momentum}\cdot\text{batch}$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `batches` (mỗi batch có ít nhất hai hàng, mỗi hàng hai số), `queries`, `momentum` và `eps`.

## Kết quả

Một đối tượng JSON gồm `train_last`, `running_mean`, `running_var` và `eval`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "batches": [
    [
      [0.05664480707558154, 2.0],
      [-2.661117367790814, 2.0],
      [-1.4633738908484955, 2.0]
    ],
    [
      [-1.305060783353052, 2.0],
      [-0.4881346870352931, 2.0],
      [-1.1359817377211683, 2.0],
      [-0.4049118790486861, 2.0],
      [-0.15463568765564858, 2.0]
    ]
  ],
  "queries": [
    [5.498165305010019, 4.451695071376041],
    [2.472347042177026, 5.853728930066792],
    [7.186244762267934, 7.9664678226756305]
  ],
  "momentum": 0.1,
  "eps": 1e-05
}
```

```output
{
  "train_last": [
    [-1.3678913482140818, 0.0],
    [0.4721169095078679, 0.0],
    [-0.9870651736400213, 0.0],
    [0.6595642864693722, 0.0],
    [1.2232753258768632, 0.0]
  ],
  "running_mean": [-0.19180988904318882, 0.38],
  "running_var": [1.0016076463704835, 0.81],
  "eval": [
    [5.685378586206146, 4.524077708542852],
    [2.662004710122898, 6.081883491032732],
    [7.372094339930203, 8.42935665895661]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
