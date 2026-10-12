# BPE có trọng số

BPE (byte pair encoding) học cách ghép các mảnh chữ hay đi cùng nhau thành một token. Bài này học BPE trên một danh sách từ có đếm số lần xuất hiện: một cặp nằm trong từ xuất hiện $7$ lần thì được tính $7$ lần.

1. Chuẩn hóa mỗi từ về dạng Unicode NFC (giữ nguyên chữ hoa, chữ thường). Tách thành từng ký tự rồi thêm token `</w>` ở cuối.
2. Lặp `steps` lần: đếm mọi cặp token kề nhau trên cả danh sách, mỗi lần xuất hiện cộng thêm số đếm của từ. Chọn cặp có tổng lớn nhất; hòa thì chọn cặp $(a,b)$ nhỏ nhất theo thứ tự so sánh chuỗi của Python (so $a$ trước, rồi $b$). Ghép cặp ấy thành token $a+b$ trong mọi từ, quét từ trái sang phải, không chồng lấn. Nếu không còn cặp nào thì dừng sớm.
3. Áp lần lượt các phép ghép đã học, đúng thứ tự, lên từng từ trong `test_words` (cũng chuẩn hóa NFC và thêm `</w>`).

Chữ "é" có thể được viết bằng một ký tự, hoặc bằng chữ "e" cộng dấu sắc rời. NFC đưa cả hai về một ký tự, nên `café` viết theo hai cách cho cùng kết quả.

## Dữ liệu vào

Một đối tượng JSON gồm `words` (list các `{"text", "count"}`), `steps` và `test_words`.

## Kết quả

Một đối tượng JSON gồm `merges` (list các cặp $[a, b]$ theo thứ tự học) và `tokens` (list token của mỗi từ trong `test_words`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "words": [
    {"text": "aaaa", "count": 2},
    {"text": "abab", "count": 7},
    {"text": "café", "count": 1}
  ],
  "steps": 1,
  "test_words": ["aaaaa", "ababab", "café", "MÈO", "lạ", ""]
}
```

```output
{
  "merges": [["a", "b"]],
  "tokens": [
    ["a", "a", "a", "a", "a", "</w>"],
    ["ab", "ab", "ab", "</w>"],
    ["c", "a", "f", "é", "</w>"],
    ["M", "È", "O", "</w>"],
    ["l", "ạ", "</w>"],
    ["</w>"]
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
