# Làm sạch

Dữ liệu thật hiếm khi sạch. Có ô trống, có ô ghi bậy, có mã bị nhập hai lần. Cho danh sách bản ghi, mỗi bản ghi có mã `id` và giá trị `value` dạng chuỗi. Hãy làm sạch bảng.

Một giá trị dùng được khi nó khác `null`, đọc được bằng `float(value)`, là số hữu hạn và nằm trong đoạn $[-10^4, 10^4]$. `float` đọc được cả `"NaN"` hay `"inf"`, nhưng đó không phải số hữu hạn; hàm `math.isfinite` kiểm được việc này.

Mã giữ nguyên là chuỗi, `"001"` vẫn là `"001"`. Khi một mã có nhiều bản ghi dùng được, giữ bản **sau cùng**. Bản ghi hỏng không thay được bản tốt đứng trước nó.

Bảng sạch xếp theo `id` tăng dần, theo thứ tự chuỗi của Python.

## Dữ liệu vào

Một đối tượng JSON có trường `records`, là danh sách `{"id": ..., "value": ...}`. `value` là chuỗi hoặc `null`.

## Kết quả

Một đối tượng JSON gồm ba trường:

- `rows`: bảng sạch, mỗi dòng `{"id": ..., "value": ...}` với `value` là số.
- `rejected`: chỉ số các bản ghi bị loại vì giá trị không dùng được.
- `superseded`: chỉ số các bản ghi dùng được nhưng bị một bản cùng mã đến sau thay thế.

Chỉ số đánh từ $0$, xếp tăng dần.

## Giới hạn

- Có không quá $2000$ bản ghi. Mã và chuỗi giá trị dài không quá $64$ ký tự.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "records": [
    {"id": "001", "value": " 7.5 "},
    {"id": "B", "value": null},
    {"id": "001", "value": "8"},
    {"id": "001", "value": "NaN"},
    {"id": "A", "value": "-2"}
  ]
}
```

```output
{
  "rows": [{"id": "001", "value": 8.0}, {"id": "A", "value": -2.0}],
  "rejected": [1, 3],
  "superseded": [0]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
