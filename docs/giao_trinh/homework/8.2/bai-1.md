# Kiểm schema

Trước khi huấn luyện, đọc dữ liệu như một bảng và kiểm vài điều cơ bản: mã có duy nhất không, ô nào bị thiếu, có hàng nào chỉ là bản sao của hàng khác không.

Dữ liệu là danh sách hàng, mỗi hàng là một object với các cột trong `columns` (một cột là `id`).

1. `duplicate_ids`: các mã xuất hiện ở hơn một hàng, xếp theo thứ tự chuỗi. Mã là chuỗi: `"001"` và `"1"` là hai mã khác nhau.
2. `missing`: với mỗi cột, số hàng có ô ấy thiếu, tức giá trị là `null`, chuỗi rỗng, hoặc không có khóa ấy.
3. `duplicate_content_rows`: số hàng thừa khi gom các hàng giống hệt nhau ở **mọi cột trừ `id`** (một nhóm $k$ hàng giống nhau đóng góp $k-1$). Hai ô thiếu (`null`) được coi là giống nhau; `null` khác chuỗi rỗng.

## Dữ liệu vào

Một đối tượng JSON gồm `columns` và `rows`.

## Kết quả

Một đối tượng JSON gồm `n_rows`, `duplicate_ids`, `missing` (từ tên cột tới số ô thiếu) và `duplicate_content_rows`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "columns": ["id", "text", "label", "source"],
  "rows": [
    {"id": "001", "text": "hom nay mua", "label": "0", "source": "doc1"},
    {"id": "1", "text": "hom nay mua", "label": "0", "source": "doc1"},
    {"id": "002", "text": "xe tau ve", "label": "1", "source": "doc2"},
    {"id": "002", "text": "", "label": "1", "source": "doc3"},
    {"id": "003", "text": "nang dep", "label": null, "source": "doc4"}
  ]
}
```

```output
{
  "n_rows": 5,
  "duplicate_ids": ["002"],
  "missing": {"id": 0, "text": 1, "label": 1, "source": 0},
  "duplicate_content_rows": 1
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
