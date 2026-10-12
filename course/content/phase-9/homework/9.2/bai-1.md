# BFS trên lưới

Robot đi trên một lưới, mỗi bước sang một ô kề cạnh (lên, xuống, trái, phải), không đi vào ô chắn `#` và không ra ngoài lưới. Mọi bước tốn như nhau, nên BFS cho đường ngắn nhất.

Lưới có đúng một ô `S` (xuất phát) và một ô `G` (đích); `.` là ô trống. Báo số bước ít nhất từ `S` tới `G` ($-1$ nếu không tới được) và số ô tới được từ `S` (kể cả `S`).

## Dữ liệu vào

Một đối tượng JSON gồm `grid` (list các chuỗi cùng độ dài).

## Kết quả

Một đối tượng JSON gồm `steps` và `reachable`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"grid": ["S..#....", ".#.#.##.", ".#...#..", ".####.#.", "......#G"]}
```

```output
{"steps": 15, "reachable": 27}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
