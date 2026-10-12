# Public và private

Bảng xếp hạng public chỉ chấm trên một phần nhỏ của test. Điểm public vì thế là một phép đo có nhiễu: bài cao nhất trên public chưa chắc cao nhất trên phần còn lại (private).

Có nhãn thật `labels`, tập chỉ số public `public_indices` (phần còn lại là private) và dự đoán của vài bài nộp.

1. Với mỗi bài: độ chính xác trên public, trên private, và sai số chuẩn của độ chính xác public $\sqrt{p(1-p)/n}$, với $p$ là độ chính xác public và $n$ là số mẫu public.
2. Xếp hạng các bài theo public và theo private (cao trước; bằng nhau thì tên nhỏ hơn).

## Dữ liệu vào

Một đối tượng JSON gồm `labels`, `public_indices` và `predictions` (từ tên bài tới danh sách dự đoán).

## Kết quả

Một đối tượng JSON gồm `submissions` (mỗi bài là `{"name", "public", "private", "public_se"}`, theo thứ tự trong `predictions`), `public_ranking` và `private_ranking`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "labels": [
    1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1,
    1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1,
    1, 1, 1, 1, 0, 1, 0, 0, 1, 1
  ],
  "public_indices": [2, 23, 32, 44, 49],
  "predictions": {
    "tuned": [
      1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0,
      1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1,
      1, 1, 0, 1, 0, 1, 1, 0, 0, 1
    ],
    "ensemble": [
      1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0,
      1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1,
      1, 1, 0, 1, 1, 1, 0, 0, 1, 1
    ],
    "cnn_seed2": [
      1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1,
      1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
      0, 1, 1, 1, 0, 0, 0, 0, 1, 1
    ]
  }
}
```

```output
{
  "submissions": [
    {
      "name": "tuned",
      "public": 0.8,
      "private": 0.8775510204081632,
      "public_se": 0.17888543819998315
    },
    {
      "name": "ensemble",
      "public": 1.0,
      "private": 0.6938775510204082,
      "public_se": 0.0
    },
    {
      "name": "cnn_seed2",
      "public": 0.6,
      "private": 0.7551020408163265,
      "public_se": 0.21908902300206645
    }
  ],
  "public_ranking": ["ensemble", "tuned", "cnn_seed2"],
  "private_ranking": ["tuned", "cnn_seed2", "ensemble"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
