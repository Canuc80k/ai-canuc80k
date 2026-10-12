# Kiểm heuristic

A* chỉ bảo đảm tìm đường tối ưu khi heuristic giữ một lời hứa. Bài này kiểm hai lời hứa ấy cho một heuristic cho sẵn.

Đồ thị vô hướng có trọng số dương; `h[n]` là ước lượng khoảng cách từ $n$ tới `goal`.

1. Khoảng cách thật $d^*(n)$ từ mỗi đỉnh tới `goal` (chỉ các đỉnh tới được), theo thứ tự chuỗi.
2. **Admissible:** $h(n)\le d^*(n)$ ở mọi đỉnh tới được. Liệt kê các đỉnh vi phạm (theo thứ tự chuỗi).
3. **Consistent:** với mọi cạnh $(u,v,w)$, theo **cả hai chiều**: $h(u)\le w+h(v)$. Liệt kê các cặp $[u,v]$ vi phạm, theo thứ tự từ điển.

## Dữ liệu vào

Một đối tượng JSON gồm `edges`, `goal` và `h` (từ tên đỉnh tới số nguyên).

## Kết quả

Một đối tượng JSON gồm `true_dist`, `not_admissible_at`, `inconsistent_edges`, `admissible` và `consistent`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "edges": [["a", "b", 8], ["b", "d", 8], ["c", "b", 2]],
  "goal": "d",
  "h": {"a": 17, "b": 9, "c": 10, "d": 0}
}
```

```output
{
  "true_dist": {"a": 16, "b": 8, "c": 10, "d": 0},
  "not_admissible_at": ["a", "b"],
  "inconsistent_edges": [["b", "d"]],
  "admissible": false,
  "consistent": false
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
