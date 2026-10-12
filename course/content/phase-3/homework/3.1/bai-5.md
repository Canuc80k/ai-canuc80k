# Broadcasting

Broadcasting giúp viết `X @ W + b` gọn gàng, nhưng cũng có thể âm thầm đổi bài toán: trừ một tensor `(2, 1)` cho một tensor `(2,)` không báo lỗi mà cho ra `(2, 2)`. Bài này luyện suy shape trước khi chạy.

**Phép theo từng phần tử** (`add`, `sub`, `mul`): căn hai shape thẳng từ chiều cuối. Shape ngắn hơn được coi như có thêm các chiều $1$ ở đầu. Ở mỗi vị trí, hai kích thước phải bằng nhau hoặc một trong hai bằng $1$; kết quả lấy kích thước lớn hơn. Có vị trí không thỏa thì báo lỗi.

**Phép `matmul`**, theo quy ước của `torch.matmul`:

- Hai vector `(n,)` và `(n,)`: tích vô hướng, kết quả là số, shape `()`.
- `(..., n, m)` với vector `(m,)`: kết quả `(..., n)`.
- Vector `(m,)` với `(..., m, p)`: kết quả `(..., p)`.
- `(..., n, m)` với `(..., m, p)`: các chiều đứng trước hai chiều cuối được broadcast như phép theo từng phần tử, kết quả là shape broadcast ấy nối thêm `(n, p)`.

Kích thước không khớp thì báo lỗi.

Hãy cho biết shape kết quả của từng phép, hoặc `null` nếu báo lỗi. Ngoài ra, liệt kê các phép theo từng phần tử mà kết quả có **nhiều phần tử hơn cả hai đầu vào**. Đó là dấu hiệu broadcast có thể đang làm sai bài toán.

## Dữ liệu vào

Một đối tượng JSON gồm `ops`, mỗi phép là `{"op": ..., "a": [...], "b": [...]}` với `a`, `b` là shape hai đầu vào.

## Kết quả

Một đối tượng JSON gồm `shapes` (shape kết quả hoặc `null`, theo thứ tự phép; tích vô hướng ghi `[]`) và `suspicious` (chỉ số các phép đáng ngờ, tăng dần, đánh số từ $0$).

## Giới hạn

- Không quá $10$ phép. Mỗi shape có từ $1$ đến $4$ chiều, mỗi chiều từ $1$ đến $4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "ops": [
    {"op": "sub", "a": [2, 1], "b": [2]},
    {"op": "add", "a": [8, 3], "b": [3]},
    {"op": "matmul", "a": [8, 3], "b": [3, 5]},
    {"op": "mul", "a": [64, 10], "b": [64]},
    {"op": "matmul", "a": [3], "b": [3]},
    {"op": "matmul", "a": [2, 4, 3], "b": [3]}
  ]
}
```

```output
{
  "shapes": [[2, 2], [8, 3], [8, 5], null, [], [2, 4]],
  "suspicious": [0]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
