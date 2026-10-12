# ROUGE

BLEU sinh ra để chấm bản dịch; với tóm tắt văn bản, người ta hay dùng ROUGE, thiên về độ phủ: bản tóm tắt chứa được bao nhiêu phần của bản mẫu. Bài này tính ba loại ROUGE cho vài bản tóm tắt của cùng một câu mẫu.

**Tách từ:** đổi chữ thường, lấy các dãy liên tiếp chữ cái `a`–`z` và chữ số (biểu thức chính quy `[a-z0-9]+`).

Với bản tóm tắt $c$ và bản mẫu $r$, mỗi loại cho precision $P=\dfrac{\text{khớp}}{|c|}$, recall $R=\dfrac{\text{khớp}}{|r|}$ và $F=\dfrac{2PR}{P+R}$ (bằng $0$ nếu $P+R=0$; precision hoặc recall bằng $0$ nếu mẫu số bằng $0$):

- **ROUGE-1:** đếm unigram; khớp là số unigram chung, đếm theo bội (mỗi lần xuất hiện ở bản mẫu chỉ khớp được một lần). $|c|$, $|r|$ là số unigram.
- **ROUGE-2:** như trên với bigram (hai từ liền nhau).
- **ROUGE-L:** khớp là độ dài dãy con chung dài nhất (LCS, không cần liền nhau) giữa hai dãy từ; $|c|$, $|r|$ là số từ.

## Dữ liệu vào

Một đối tượng JSON gồm `reference` và `candidates` (từ tên tới văn bản).

## Kết quả

Một đối tượng JSON: với mỗi tên là `{"rouge1", "rouge2", "rougeL"}`, mỗi loại là `{"precision", "recall", "f"}`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "reference": "The cat sat on the mat because it was tired.",
  "candidates": {
    "copy": "The cat sat on the mat.",
    "paraphrase": "A tired kitten rested on the rug.",
    "shuffled": "Mat the on sat cat the."
  }
}
```

```output
{
  "copy": {
    "rouge1": {"precision": 1.0, "recall": 0.6, "f": 0.7499999999999999},
    "rouge2": {
      "precision": 1.0,
      "recall": 0.5555555555555556,
      "f": 0.7142857142857143
    },
    "rougeL": {"precision": 1.0, "recall": 0.6, "f": 0.7499999999999999}
  },
  "paraphrase": {
    "rouge1": {
      "precision": 0.42857142857142855,
      "recall": 0.3,
      "f": 0.3529411764705882
    },
    "rouge2": {
      "precision": 0.16666666666666666,
      "recall": 0.1111111111111111,
      "f": 0.13333333333333333
    },
    "rougeL": {
      "precision": 0.2857142857142857,
      "recall": 0.2,
      "f": 0.23529411764705882
    }
  },
  "shuffled": {
    "rouge1": {"precision": 1.0, "recall": 0.6, "f": 0.7499999999999999},
    "rouge2": {"precision": 0.0, "recall": 0.0, "f": 0.0},
    "rougeL": {"precision": 0.5, "recall": 0.3, "f": 0.37499999999999994}
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
