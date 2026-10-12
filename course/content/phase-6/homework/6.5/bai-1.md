# Decoder input

Huấn luyện mô hình encoder-decoder như T5 bằng teacher forcing: decoder nhận câu đích đã dịch phải một bước, và phải đoán từng token của câu đích. Ở T5, token bắt đầu của decoder chính là `PAD` (mã $0$), nên không thể dùng "khác $0$" để biết vị trí nào hợp lệ.

`labels` có shape $B\times T$; vị trí bị bỏ qua có giá trị $-100$.

1. **Decoder input:** $[0]$ rồi `labels[:, :-1]`, với mọi $-100$ đổi thành $0$.
2. **decoder_keep:** vị trí $0$ luôn `true`; vị trí $j>0$ là `true` khi `labels[j-1]` khác $-100$.
3. **Loss:** cross-entropy trung bình trên mọi nhãn khác $-100$ (kể cả `EOS`), với `logits` cho sẵn shape $B\times T\times V$. Không có nhãn hợp lệ thì loss là `null`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `labels` và `logits`.

## Kết quả

Một đối tượng JSON gồm `decoder_inputs`, `decoder_keep`, `n_tokens` (số nhãn hợp lệ) và `loss`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "labels": [[-100, -100, -100, -100, -100], [-100, -100, -100, -100, -100]],
  "logits": [
    [
      [0.327, -2.332, 0.565, -1.352, 1.17, 0.116, -0.322],
      [1.534, -0.71, -0.21, -0.262, 0.445, -0.454, -0.043],
      [-2.092, -0.674, 0.539, 2.263, 1.237, -0.063, 1.871],
      [-0.435, 0.11, 2.371, -1.538, 1.644, -3.481, -1.614],
      [-1.881, -2.333, -1.019, 0.189, -0.059, -0.865, -4.513]
    ],
    [
      [1.024, 0.158, -0.056, 1.01, 2.406, -2.011, 2.725],
      [-2.612, 2.921, 0.144, 0.211, -0.136, -0.372, 0.245],
      [-0.991, 1.064, -3.051, 4.012, -1.637, -1.367, -0.528],
      [0.613, -0.738, 1.747, -3.286, -0.643, -1.159, -0.694],
      [0.093, 0.957, 0.537, 0.444, 2.113, 2.186, 0.947]
    ]
  ]
}
```

```output
{
  "decoder_inputs": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
  "decoder_keep": [
    [true, false, false, false, false],
    [true, false, false, false, false]
  ],
  "n_tokens": 0,
  "loss": null
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
