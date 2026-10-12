# Span corruption

T5 được huấn luyện trước bằng cách che các **đoạn** liên tiếp của câu. Mỗi đoạn bị che được thay bằng một token đặc biệt (sentinel) trong đầu vào, và mô hình phải sinh lại đúng các đoạn ấy, mỗi đoạn mở đầu bằng sentinel của nó.

Có câu `tokens` và `noise_mask` (cùng độ dài; `true` là bị che). Các sentinel là `<extra_id_0>`, `<extra_id_1>`, … đánh số theo thứ tự xuất hiện của các đoạn.

1. **Đầu vào:** đi dọc câu; mỗi đoạn liên tiếp bị che được thay bằng **một** sentinel; token không bị che giữ nguyên. Cuối cùng thêm `</s>`.
2. **Đích:** với mỗi đoạn bị che, theo thứ tự: sentinel của đoạn, rồi các token của đoạn. Sau đoạn cuối thêm một sentinel nữa (số tiếp theo), rồi `</s>`. Câu không có đoạn nào bị che thì đích là `<extra_id_0>` và `</s>`.
3. **Decoder input:** `<pad>` rồi đích bỏ token cuối.
4. Báo thêm số đoạn, tỉ lệ token bị che, độ dài đầu vào và đích, và câu khôi phục: thay mỗi sentinel trong đầu vào bằng đoạn tương ứng lấy từ đích, bỏ `</s>`.

## Dữ liệu vào

Một đối tượng JSON gồm `tokens` và `noise_mask`.

## Kết quả

Một đối tượng JSON gồm `input`, `target`, `decoder_input`, `num_spans`, `noise_density`, `input_length`, `target_length` và `reconstructed`.

## Giới hạn

- Câu có từ $4$ tới $16$ token, không token nào bắt đầu bằng `<`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "tokens": [
    "Thank", "you", "for", "inviting", "me", "to", "your", "party",
    "last", "week", "."
  ],
  "noise_mask": [
    false, false, true, true, false, false, false, false, true, false,
    false
  ]
}
```

```output
{
  "input": [
    "Thank", "you", "<extra_id_0>", "me", "to", "your", "party",
    "<extra_id_1>", "week", ".", "</s>"
  ],
  "target": [
    "<extra_id_0>", "for", "inviting", "<extra_id_1>", "last",
    "<extra_id_2>", "</s>"
  ],
  "decoder_input": [
    "<pad>", "<extra_id_0>", "for", "inviting", "<extra_id_1>", "last",
    "<extra_id_2>"
  ],
  "num_spans": 2,
  "noise_density": 0.2727272727272727,
  "input_length": 11,
  "target_length": 7,
  "reconstructed": [
    "Thank", "you", "for", "inviting", "me", "to", "your", "party",
    "last", "week", "."
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
