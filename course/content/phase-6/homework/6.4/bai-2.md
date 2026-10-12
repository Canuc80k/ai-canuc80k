# Dịch nhãn

Huấn luyện mô hình ngôn ngữ nhân quả: ở vị trí $t$, mô hình chỉ được nhìn các token $0..t$ và phải đoán token $t+1$. Bài này dựng đúng đầu vào, nhãn và mask, rồi tính loss từ logits cho sẵn.

Token: $0$ là `PAD`, $1$ là `BOS`, $2$ là `EOS`. `ids` có shape $B\times L$.

1. Đầu vào là `ids[:, :-1]`, nhãn là `ids[:, 1:]` với mọi `PAD` trong nhãn đổi thành $-100$.
2. `allowed[b][i][j]` là `true` khi $j\le i$ **và** cả token đầu vào ở vị trí $i$ lẫn ở vị trí $j$ đều không phải `PAD`. Hàng của một vị trí `PAD` toàn `false`.
3. `logits` có shape $B\times(L-1)\times V$, ứng với từng vị trí đầu vào. Loss là cross-entropy trung bình trên mọi nhãn khác $-100$ (kể cả `EOS`). Perplexity là $e^{\text{loss}}$. Không có nhãn hợp lệ nào thì cả hai là `null`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `ids` và `logits`.

## Kết quả

Một đối tượng JSON gồm `inputs`, `targets`, `allowed`, `n_tokens` (số nhãn hợp lệ), `mean_nll` và `perplexity`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "ids": [[1, 3, 4, 2, 0, 0], [1, 6, 2, 0, 0, 0]],
  "logits": [
    [
      [1.212, 1.333, -0.138, 0.738, 0.643, -0.359, -0.889],
      [-1.008, -1.255, -0.929, -0.203, -0.489, -0.502, -0.798],
      [0.383, -0.087, -2.455, 0.726, 0.307, 0.466, 0.801],
      [-1.119, 0.55, -0.856, 0.8, -1.138, -0.459, 0.235],
      [0.172, 0.011, 1.948, 0.635, 0.293, -1.352, -0.334]
    ],
    [
      [-0.523, -0.168, 0.05, 0.375, 0.926, 0.443, 0.89],
      [-0.169, 0.467, -0.012, 0.477, 0.162, -1.394, 0.08],
      [0.605, -1.044, 1.271, -0.325, -0.076, 0.474, 1.192],
      [-0.009, -0.01, 0.022, 0.503, -0.854, 0.725, -0.712],
      [-1.107, -0.842, -0.246, 0.162, 0.863, -0.163, 0.779]
    ]
  ]
}
```

```output
{
  "inputs": [[1, 3, 4, 2, 0], [1, 6, 2, 0, 0]],
  "targets": [[3, 4, 2, -100, -100], [6, 2, -100, -100, -100]],
  "allowed": [
    [
      [true, false, false, false, false],
      [true, true, false, false, false],
      [true, true, true, false, false],
      [true, true, true, true, false],
      [false, false, false, false, false]
    ],
    [
      [true, false, false, false, false],
      [true, true, false, false, false],
      [true, true, true, false, false],
      [false, false, false, false, false],
      [false, false, false, false, false]
    ]
  ],
  "n_tokens": 5,
  "mean_nll": 2.3613123734775656,
  "perplexity": 10.604859860738994
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
