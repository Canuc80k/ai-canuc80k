# Chấm bằng LM

Có thể dùng một mô hình ngôn ngữ để trả lời câu trắc nghiệm: chấm từng phương án bằng log-xác suất mà mô hình gán cho nó, rồi chọn phương án điểm cao nhất. Nhưng "điểm" có nhiều cách tính, và mỗi cách có thể chọn một đáp án khác.

Với mỗi phương án, đề cho `logprobs`: log-xác suất của từng token phương án khi đọc câu hỏi, và `neutral_logprobs`: log-xác suất của cùng các token ấy khi thay câu hỏi bằng một input trung tính (như "N/A"). Ba cách chấm:

- `sum`: tổng `logprobs`.
- `mean`: tổng `logprobs` chia số token.
- `calibrated`: tổng `logprobs` trừ tổng `neutral_logprobs`. Phương án được mô hình ưa thích sẵn, kể cả khi chưa đọc câu hỏi, bị trừ bớt.

Với mỗi câu hỏi, hãy tính điểm `sum`, `mean`, perplexity $\exp(-\text{mean})$ của từng phương án, và phương án được chọn theo từng cách (hòa thì chỉ số nhỏ). Cuối cùng, tính accuracy của từng cách trên mọi câu hỏi.

## Dữ liệu vào

Một đối tượng JSON gồm `questions`, mỗi câu là `{"candidates": [{"logprobs": [...], "neutral_logprobs": [...]}, ...], "answer": k}`.

## Kết quả

Một đối tượng JSON gồm:

- `questions`: mỗi câu là `{"sum": [...], "mean": [...], "perplexity": [...], "choice": {"sum": i, "mean": j, "calibrated": k}}`.
- `accuracy`: `{"sum": ..., "mean": ..., "calibrated": ...}`.

## Giới hạn

- Không quá $8$ câu hỏi, mỗi câu từ $2$ tới $4$ phương án. Không có hai điểm nào sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "questions": [
    {
      "candidates": [
        {
          "logprobs": [-0.5108256238, -0.2231435513],
          "neutral_logprobs": [-0.6931471806, -0.2231435513]
        },
        {
          "logprobs": [-0.9162907319, -0.0512932944, -0.0512932944],
          "neutral_logprobs": [-1.6094379124, -0.1053605157, -0.1053605157]
        }
      ],
      "answer": 1
    },
    {
      "candidates": [
        {
          "logprobs": [-1.2039728043],
          "neutral_logprobs": [-0.5108256238]
        },
        {
          "logprobs": [-1.3862943611],
          "neutral_logprobs": [-2.302585093]
        },
        {
          "logprobs": [-1.6094379124, -0.1053605157],
          "neutral_logprobs": [-1.2039728043, -0.1053605157]
        }
      ],
      "answer": 1
    }
  ]
}
```

```output
{
  "questions": [
    {
      "sum": [-0.7339691750999999, -1.0188773207],
      "mean": [-0.36698458754999996, -0.3396257735666666],
      "perplexity": [1.4433756729883536, 1.4044219204037263],
      "choice": {"sum": 0, "mean": 1, "calibrated": 1}
    },
    {
      "sum": [-1.2039728043, -1.3862943611, -1.7147984281],
      "mean": [-1.2039728043, -1.3862943611, -0.85739921405],
      "perplexity": [3.33333333324688, 3.999999999920438, 2.3570226039646727],
      "choice": {"sum": 0, "mean": 2, "calibrated": 1}
    }
  ],
  "accuracy": {"sum": 0.0, "mean": 0.5, "calibrated": 1.0}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
