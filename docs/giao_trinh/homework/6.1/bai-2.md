# WordPiece

WordPiece (tokenizer của BERT) tách một từ bằng cách tham lam: lấy đoạn đầu dài nhất có trong từ điển, rồi lặp lại với phần còn lại. Các mảnh không đứng đầu từ được viết thêm tiền tố `##`.

Với mỗi từ:

1. Chuẩn hóa Unicode NFC rồi đổi về chữ thường.
2. Từ vị trí đầu, tìm đoạn dài nhất bắt đầu ở đó mà có trong `vocab` (ở vị trí đầu từ thì so nguyên đoạn, ở vị trí khác thì so `##` + đoạn). Thêm mảnh ấy rồi đi tiếp từ cuối đoạn.
3. Nếu có lúc không tìm được mảnh nào, **cả từ** thành `["[UNK]"]`, bỏ cả những mảnh đã tách được trước đó.
4. Từ rỗng cho list rỗng.

## Dữ liệu vào

Một đối tượng JSON gồm `vocab` (list các mảnh, có `[UNK]`) và `words`.

## Kết quả

Một đối tượng JSON gồm `tokens`: list các mảnh của mỗi từ.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "vocab": [
    "[UNK]", "con", "m", "##èo", "café", "đ", "##ẹp", "đẹp", "##đẹp",
    "a", "aa", "##a", "##aa", "học", "##sinh"
  ],
  "words": [
    "MÈO", "café", "đẹpđẹp", "aaaaa", "họcsinh", "họcsinhx", "con",
    "xy", ""
  ]
}
```

```output
{
  "tokens": [
    ["m", "##èo"],
    ["café"],
    ["đẹp", "##đẹp"],
    ["aa", "##aa", "##a"],
    ["học", "##sinh"],
    ["[UNK]"],
    ["con"],
    ["[UNK]"],
    []
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
