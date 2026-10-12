# Bộ trả lời

Trong một bài thi mở, hệ thống giữ một vật bí mật trong danh mục. Mỗi câu hỏi nêu hai vật $a$, $b$, và hệ thống trả lời vật nào **gần vật bí mật hơn**. Trước khi viết người chơi, hãy viết lại chính bộ trả lời để hiểu đúng giao thức.

Mỗi vật có một vector (`judge`). Khoảng cách là bình phương khoảng cách Euclid.

Xử lý các câu hỏi theo thứ tự:

1. Nếu đã trả lời đủ `budget` câu hợp lệ: trả `"over_budget"`.
2. Nếu $a$ hoặc $b$ không có trong danh mục, hoặc $a=b$: trả `"invalid"` (không tính vào ngân sách).
3. Ngược lại: trả `"a"` nếu vật bí mật gần $a$ hơn, `"b"` nếu gần $b$ hơn, và tính một câu vào ngân sách.

## Dữ liệu vào

Một đối tượng JSON gồm `judge` (từ tên vật tới vector), `secret`, `queries` (list các cặp $[a, b]$) và `budget`.

## Kết quả

Một đối tượng JSON gồm `answers` và `queries_used`.

## Giới hạn

- Không quá $12$ vật. Không vật nào cách đều hai vật khác.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "judge": {
    "apple": [-1, -8],
    "chair": [-4, 4],
    "desk": [-9, -6],
    "fan": [-8, -3],
    "hat": [-8, 2],
    "ink": [-5, 7],
    "jar": [6, -6],
    "key": [7, 4]
  },
  "secret": "chair",
  "queries": [["fan", "jar"], ["desk", "apple"], ["jar", "fan"]],
  "budget": 3
}
```

```output
{"answers": ["a", "a", "b"], "queries_used": 3}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
