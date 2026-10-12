# Mẫu trùng

Hai câu "Hôm nay mưa!" và "hôm  nay mưa" là một mẫu, chỉ khác cách viết. Để lại cả hai thì validation có thể chứa bản sao của dữ liệu train. Tệ hơn, hai bản sao có thể mang hai nhãn khác nhau.

1. **Chuẩn hóa** văn bản: Unicode NFC, chữ thường, mọi ký tự dấu câu hoặc ký hiệu (loại Unicode bắt đầu bằng `P` hoặc `S`) thay bằng dấu cách, rồi gộp khoảng trắng.
2. Gom các hàng có cùng văn bản đã chuẩn hóa.
3. Báo số văn bản khác nhau; các nhóm có từ hai hàng trở lên (văn bản chuẩn hóa và các mã, xếp theo chuỗi), theo thứ tự chuỗi của văn bản; các nhóm có nhãn mâu thuẫn; số hàng bỏ đi nếu chỉ giữ một hàng mỗi nhóm.

## Dữ liệu vào

Một đối tượng JSON gồm `rows`: mỗi hàng là `{"id", "text", "label"}`.

## Kết quả

Một đối tượng JSON gồm `unique_texts`, `duplicate_groups` (mỗi nhóm là `{"text", "ids"}`), `conflicting_texts` và `rows_removed_by_dedup`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "rows": [
    {"id": "a", "text": "Hôm nay mưa!", "label": 0},
    {"id": "b", "text": "hôm  nay mưa", "label": 0},
    {"id": "c", "text": "Xe buýt đến muộn.", "label": 1},
    {"id": "d", "text": "xe buýt đến muộn", "label": 0},
    {"id": "e", "text": "trời đẹp", "label": 0}
  ]
}
```

```output
{
  "unique_texts": 3,
  "duplicate_groups": [
    {"text": "hôm nay mưa", "ids": ["a", "b"]},
    {"text": "xe buýt đến muộn", "ids": ["c", "d"]}
  ],
  "conflicting_texts": ["xe buýt đến muộn"],
  "rows_removed_by_dedup": 2
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
