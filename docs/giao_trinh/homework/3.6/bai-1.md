# Dropout

Dropout khi học tắt ngẫu nhiên một số activation, mỗi activation bị tắt với xác suất $p$. Bản "inverted" của PyTorch chia các activation còn lại cho $1-p$, để kỳ vọng giữ nguyên và lúc suy luận không phải sửa gì.

Bài này cho sẵn mặt nạ: $m_i=1$ là giữ, $m_i=0$ là tắt. Với vector activation $h$, hãy tính:

- `train`: đầu ra khi học, $m_ih_i/(1-p)$.
- `eval`: đầu ra khi suy luận, tức $h$ nguyên vẹn.
- `expected_variance`: phương sai của đầu ra khi học tại từng vị trí, nếu mặt nạ được rút ngẫu nhiên: $h_i^2\,p/(1-p)$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `h`, `mask` (cùng độ dài, các số $0$/$1$) và `p`.

## Kết quả

Một đối tượng JSON gồm `train`, `eval` và `expected_variance`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "h": [
    0.05664480707558154, 1.3383105844670897, -2.661117367790814,
    1.2488079457592625, -1.4633738908484955, -0.056744283289588186,
    -1.305060783353052, 0.5782487847576361
  ],
  "mask": [0, 0, 1, 0, 1, 1, 0, 0],
  "p": 0.2
}
```

```output
{
  "train": [
    0.0, 0.0, -3.3263967097385176, 0.0, -1.8292173635606193,
    -0.07093035411198523, -0.0, 0.0
  ],
  "eval": [
    0.05664480707558154, 1.3383105844670897, -2.661117367790814,
    1.2488079457592625, -1.4633738908484955, -0.056744283289588186,
    -1.305060783353052, 0.5782487847576361
  ],
  "expected_variance": [
    0.0008021585421574631, 0.44776880512416084, 1.7703864112894778,
    0.38988032134786726, 0.5353657861042661, 0.0008049784215122594,
    0.4257959120615205, 0.08359291426842073
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
