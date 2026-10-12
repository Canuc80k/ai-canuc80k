# Tách phần mới

Với mô hình chỉ có decoder, đầu ra của `generate` gồm **cả prompt** rồi mới tới phần mới sinh. Muốn lấy câu trả lời, phải dựng lại đúng prompt và cắt nó đi. Bài này làm với một khuôn chat đơn giản, trên các mã token.

1. **Dựng prompt.** Với mỗi tin nhắn theo thứ tự: mã của vai (`role_markers[role]`), rồi các mã của nội dung, rồi `end_turn`. Sau tin nhắn cuối, thêm `assistant_prefix` (báo cho mô hình đến lượt trợ lý nói).
2. **Kiểm tiền tố.** `full_output` phải bắt đầu đúng bằng prompt (và dài ít nhất bằng prompt).
3. Nếu đúng, phần mới là phần còn lại của `full_output`; nếu không, phần mới là `null`.

## Dữ liệu vào

Một đối tượng JSON gồm `messages` (mỗi tin nhắn là `{"role", "token_ids"}`), `role_markers`, `end_turn`, `assistant_prefix` và `full_output`.

## Kết quả

Một đối tượng JSON gồm `prompt_ids`, `prefix_matches` và `new_ids`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "messages": [
    {"role": "system", "token_ids": [10, 11]},
    {"role": "user", "token_ids": [20, 30]},
    {"role": "assistant", "token_ids": [40]},
    {"role": "user", "token_ids": [50]}
  ],
  "role_markers": {"system": 1, "user": 2, "assistant": 3},
  "end_turn": 4,
  "assistant_prefix": [3, 5],
  "full_output": [99, 10, 11, 4, 2, 20, 30, 4, 3, 40, 4, 2, 50, 4, 3, 5, 60, 61, 4]
}
```

```output
{
  "prompt_ids": [1, 10, 11, 4, 2, 20, 30, 4, 3, 40, 4, 2, 50, 4, 3, 5],
  "prefix_matches": false,
  "new_ids": null
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
