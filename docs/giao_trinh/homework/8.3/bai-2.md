# Lọc ứng viên

Mỗi câu trả lời loại bớt những vật không thể là vật bí mật. Người chơi chỉ có embedding public, nên dùng nó để kiểm: vật $c$ còn phù hợp với câu trả lời "gần $a$ hơn $b$" khi $c$ (theo embedding public) gần $a$ hơn $b$.

Bắt đầu với mọi vật trong danh mục. Với mỗi câu trong lịch sử $(a, b, \text{ans})$ theo thứ tự, chỉ giữ các vật $c$ thỏa: nếu ans là `"a"` thì $d(c,a)<d(c,b)$; nếu ans là `"b"` thì $d(c,a)>d(c,b)$ ($d$ là bình phương khoảng cách Euclid).

Báo các vật còn lại (theo thứ tự chuỗi) và số vật còn lại sau từng câu.

## Dữ liệu vào

Một đối tượng JSON gồm `public` (từ tên vật tới vector) và `history` (list các bộ $[a, b, \text{ans}]$).

## Kết quả

Một đối tượng JSON gồm `candidates` và `sizes`.

## Giới hạn

- Không quá $12$ vật. Không vật nào cách đều hai vật khác.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "public": {
    "apple": [6, -6],
    "book": [-8, -4],
    "chair": [3, 9],
    "desk": [-1, -6],
    "egg": [-4, 1],
    "fan": [-5, 3],
    "glass": [7, 6],
    "hat": [-4, -8],
    "ink": [4, -4],
    "lamp": [4, -7]
  },
  "history": [
    ["chair", "apple", "a"],
    ["fan", "desk", "a"],
    ["glass", "lamp", "a"]
  ]
}
```

```output
{"candidates": ["chair", "fan", "glass"], "sizes": [4, 4, 3]}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
