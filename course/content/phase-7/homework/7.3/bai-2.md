# WER cả tập

WER (word error rate) đo bản nhận dạng sai bao nhiêu so với bản chuẩn. Trên cả tập, WER phải là **tổng số lỗi chia tổng số từ của bản chuẩn**, không phải trung bình WER từng câu: một câu ngắn sai một từ không được nặng ngang một câu dài.

1. **Chuẩn hóa** mỗi câu: Unicode NFC, chữ thường, mọi ký tự dấu câu (loại Unicode bắt đầu bằng `P`) thay bằng dấu cách, rồi tách theo khoảng trắng. Chữ có dấu tiếng Việt và chữ số giữ nguyên.
2. **Khoảng cách** giữa hai dãy từ là số phép chèn, xóa, thay tối thiểu (mỗi phép tốn $1$).
3. WER $=\dfrac{\sum\text{khoảng cách}}{\sum\text{số từ của bản chuẩn}}$, hoặc `null` nếu mẫu số bằng $0$. WER có thể lớn hơn $1$.

## Dữ liệu vào

Một đối tượng JSON gồm `pairs`: mỗi cặp là `{"reference", "hypothesis"}`.

## Kết quả

Một đối tượng JSON gồm `distances`, `reference_word_counts`, `total_errors`, `total_reference_words` và `wer`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "pairs": [
    {"reference": "", "hypothesis": ""},
    {"reference": "", "hypothesis": "đi đi"}
  ]
}
```

```output
{
  "distances": [0, 2],
  "reference_word_counts": [0, 0],
  "total_errors": 2,
  "total_reference_words": 0,
  "wer": null
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
