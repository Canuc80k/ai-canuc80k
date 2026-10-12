# Bigram

Mô hình ngôn ngữ đơn giản nhất: đoán token tiếp theo chỉ từ token ngay trước. Bài này đếm bigram trên các câu train, làm trơn, đo perplexity trên câu test rồi sinh tiếp một câu.

Token là số nguyên $0..V-1$: $0$ là `BOS` (đầu câu), $1$ là `EOS` (cuối câu), $2$ là `PAD`. Mỗi câu bắt đầu bằng $0$ và kết thúc bằng $1$.

1. **Đếm.** $C_{ij}$ là số lần token $j$ đứng ngay sau token $i$ trong các câu train.
2. **Làm trơn** với hệ số $\alpha$: $P(j\mid i)=\dfrac{C_{ij}+\alpha}{\sum_k C_{ik}+\alpha V}$, trên cả $V$ token.
3. **Perplexity.** Với mọi cặp token liền nhau trong các câu test (kể cả cặp kết thúc bằng `EOS`), lấy $-\log P(\text{sau}\mid\text{trước})$. `mean_nll` là trung bình trên mọi cặp của mọi câu; perplexity là $e^{\text{mean\_nll}}$.
4. **Sinh câu.** Bắt đầu từ token cuối của `prompt`. Mỗi bước chọn token có xác suất lớn nhất (không chọn `BOS` và `PAD`; bằng nhau thì số nhỏ hơn), thêm vào kết quả. Dừng khi vừa thêm `EOS` hoặc đã thêm `max_new_tokens` token.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `V`, `alpha`, `train`, `test`, `prompt` và `max_new_tokens`.

## Kết quả

Một đối tượng JSON gồm `counts`, `probabilities` (hai ma trận $V\times V$), `mean_nll`, `perplexity` và `generated` (các token mới sinh).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "V": 7,
  "alpha": 0.5,
  "train": [[0, 3, 4, 1], [0, 3, 5, 1], [0, 4, 3, 1], [0, 6, 1]],
  "test": [[0, 3, 4, 1], [0, 5, 6, 3, 1]],
  "prompt": [0, 3],
  "max_new_tokens": 4
}
```

```output
{
  "counts": [
    [0, 0, 0, 2, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0]
  ],
  "probabilities": [
    [
      0.06666666666666667, 0.06666666666666667, 0.06666666666666667,
      0.3333333333333333, 0.2, 0.06666666666666667, 0.2
    ],
    [
      0.14285714285714285, 0.14285714285714285, 0.14285714285714285,
      0.14285714285714285, 0.14285714285714285, 0.14285714285714285,
      0.14285714285714285
    ],
    [
      0.14285714285714285, 0.14285714285714285, 0.14285714285714285,
      0.14285714285714285, 0.14285714285714285, 0.14285714285714285,
      0.14285714285714285
    ],
    [
      0.07692307692307693, 0.23076923076923078, 0.07692307692307693,
      0.07692307692307693, 0.23076923076923078, 0.23076923076923078,
      0.07692307692307693
    ],
    [
      0.09090909090909091, 0.2727272727272727, 0.09090909090909091,
      0.2727272727272727, 0.09090909090909091, 0.09090909090909091,
      0.09090909090909091
    ],
    [
      0.1111111111111111, 0.3333333333333333, 0.1111111111111111,
      0.1111111111111111, 0.1111111111111111, 0.1111111111111111,
      0.1111111111111111
    ],
    [
      0.1111111111111111, 0.3333333333333333, 0.1111111111111111,
      0.1111111111111111, 0.1111111111111111, 0.1111111111111111,
      0.1111111111111111
    ]
  ],
  "mean_nll": 1.776152680879982,
  "perplexity": 5.907086198850627,
  "generated": [1]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
