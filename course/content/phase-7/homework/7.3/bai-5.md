# WER và CER

Tiếng Việt có dấu, và mô hình nhận dạng hay sai đúng ở dấu: nghe "tôi" ra "toi". Với WER, mỗi lỗi như vậy là sai cả một từ. Bài này đo cùng một bộ kết quả theo ba cách để thấy mỗi cách nói lên điều gì.

**Chuẩn hóa** mỗi câu: Unicode NFC, chữ thường, mọi ký tự dấu câu (loại Unicode bắt đầu bằng `P`) thay bằng dấu cách, rồi gộp khoảng trắng (tách theo khoảng trắng và nối lại bằng một dấu cách).

1. **WER:** khoảng cách chỉnh sửa (chèn, xóa, thay, mỗi phép $1$) giữa hai dãy **từ**.
2. **CER:** khoảng cách chỉnh sửa giữa hai dãy **ký tự** của câu đã chuẩn hóa (kể cả dấu cách).
3. **CER không dấu:** bỏ dấu cả hai câu đã chuẩn hóa (chuẩn hóa NFD, bỏ các ký tự loại `Mn`, đổi `đ` thành `d`), rồi tính như CER.

Gộp trên cả tập: WER $=\dfrac{\sum\text{lỗi từ}}{\sum\text{số từ của bản chuẩn}}$; CER và CER không dấu cùng chia cho $\sum$ số ký tự của bản chuẩn đã chuẩn hóa (có dấu).

## Dữ liệu vào

Một đối tượng JSON gồm `pairs`: mỗi cặp là `{"reference", "hypothesis"}`. Mọi bản chuẩn đều khác rỗng.

## Kết quả

Một đối tượng JSON gồm `per_pair` (với mỗi cặp là `{"word_errors", "char_errors", "plain_char_errors"}`), `wer`, `cer` và `plain_cer`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "pairs": [
    {
      "reference": "Tôi đọc sách ở thư viện.",
      "hypothesis": "toi doc sach o thu vien"
    },
    {
      "reference": "Hôm nay trời đẹp",
      "hypothesis": "hôm nay trời đẹp quá"
    },
    {"reference": "xin chào", "hypothesis": "xin trào"}
  ]
}
```

```output
{
  "per_pair": [
    {"word_errors": 6, "char_errors": 7, "plain_char_errors": 0},
    {"word_errors": 1, "char_errors": 4, "plain_char_errors": 4},
    {"word_errors": 1, "char_errors": 2, "plain_char_errors": 2}
  ],
  "wer": 0.6666666666666666,
  "cer": 0.2765957446808511,
  "plain_cer": 0.1276595744680851
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
