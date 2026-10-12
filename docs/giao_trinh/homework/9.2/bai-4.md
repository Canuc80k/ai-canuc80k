# Weighted A*

Weighted A* ưu tiên đỉnh theo $f(n)=g(n)+w\cdot h(n)$, trong đó $g$ là chi phí đã đi từ nguồn và $h$ là ước lượng phần còn lại. Với $w>1$, thuật toán tin $h$ hơn, lao về phía đích và thường mở ít đỉnh hơn; đổi lại, đường tìm được có thể dài hơn tối ưu. Khi $h$ đến từ một model, ước lượng còn có thể sai cả hai phía.

Đồ thị vô hướng, trọng số dương. Với mỗi $w$ trong `weights`, chạy A* như sau:

1. Heap ban đầu chỉ có nguồn, với $g=0$.
2. Lặp: lấy ra đỉnh có $f$ nhỏ nhất (bằng nhau thì tên nhỏ hơn); bỏ qua nếu đỉnh đã đóng. Đóng đỉnh ấy và ghi vào thứ tự mở. Nếu đó là đích thì dừng.
3. Xét các đỉnh kề chưa đóng theo thứ tự tên: nếu đi qua đỉnh vừa mở cho $g$ nhỏ hơn $g$ đang có (hoặc đỉnh chưa có $g$), cập nhật $g$, đỉnh trước, và đưa vào heap. Đỉnh đã đóng không bao giờ mở lại.

Báo chi phí tối ưu thật $C^*$ (chạy đúng cách trên với $w=0$, tức Dijkstra), và với mỗi $w$: thứ tự các đỉnh được mở, đường đi, chi phí, và chi phí có không vượt $w\cdot C^*$ không.

## Dữ liệu vào

Một đối tượng JSON gồm `edges`, `h`, `start`, `goal` và `weights`.

## Kết quả

Một đối tượng JSON gồm `optimal_cost` và `runs` (với mỗi $w$ là `{"weight", "expanded", "path", "cost", "within_bound"}`).

## Giới hạn

- Không quá $8$ đỉnh; đích tới được từ nguồn; $h$ là số nguyên không âm.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "edges": [
    ["S", "A", 2],
    ["S", "B", 4],
    ["A", "C", 5],
    ["B", "C", 1],
    ["C", "G", 3],
    ["A", "G", 9]
  ],
  "h": {"S": 6, "A": 5, "B": 3, "C": 3, "G": 0},
  "start": "S",
  "goal": "G",
  "weights": [1, 2]
}
```

```output
{
  "optimal_cost": 8,
  "runs": [
    {
      "weight": 1,
      "expanded": ["S", "A", "B", "C", "G"],
      "path": ["S", "B", "C", "G"],
      "cost": 8,
      "within_bound": true
    },
    {
      "weight": 2,
      "expanded": ["S", "B", "C", "G"],
      "path": ["S", "B", "C", "G"],
      "cost": 8,
      "within_bound": true
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
