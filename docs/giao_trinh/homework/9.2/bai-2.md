# Dijkstra

Hành lang trong thư viện dài ngắn khác nhau, nên đường ít bước nhất chưa chắc là đường ngắn nhất. Dijkstra tìm khoảng cách ngắn nhất từ một đỉnh tới mọi đỉnh trên đồ thị có trọng số dương.

Đồ thị vô hướng, mỗi cạnh $[u, v, w]$ có độ dài $w>0$. Tên đỉnh là chuỗi.

1. Khoảng cách ngắn nhất từ `source` tới mọi đỉnh tới được, theo thứ tự chuỗi của tên đỉnh.
2. Một đường ngắn nhất tới `target`: đi ngược từ `target`, mỗi bước chọn đỉnh trước $u$ có $d(u)+w(u,v)=d(v)$; nếu có nhiều đỉnh như vậy, chọn tên nhỏ nhất. Không tới được thì `null`.

## Dữ liệu vào

Một đối tượng JSON gồm `edges`, `source` và `target`.

## Kết quả

Một đối tượng JSON gồm `dist` và `path` (từ `source` tới `target`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "edges": [
    ["a", "b", 4],
    ["a", "c", 1],
    ["c", "b", 2],
    ["b", "d", 1],
    ["c", "d", 5],
    ["c", "e", 1],
    ["e", "d", 2]
  ],
  "source": "a",
  "target": "d"
}
```

```output
{
  "dist": {"a": 0, "b": 3, "c": 1, "d": 4, "e": 2},
  "path": ["a", "c", "b", "d"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
