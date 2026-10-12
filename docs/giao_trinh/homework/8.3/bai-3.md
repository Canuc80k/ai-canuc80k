# Câu hỏi tốt nhất

Nên hỏi cặp nào tiếp theo? Một câu hỏi tốt chia tập ứng viên thành hai phần gần bằng nhau, để dù câu trả lời là gì, tập còn lại cũng nhỏ.

Với tập ứng viên $S$ và embedding public, xét mọi cặp $a<b$ (theo thứ tự chuỗi) với $a,b\in S$. Câu trả lời `"a"` giữ lại các $c\in S$ có $d(c,a)<d(c,b)$; câu trả lời `"b"` giữ phần còn lại. Chọn cặp làm **trường hợp xấu nhất** $\max(|S_a|,|S_b|)$ nhỏ nhất; bằng nhau thì cặp $(a,b)$ nhỏ hơn theo thứ tự từ điển.

## Dữ liệu vào

Một đối tượng JSON gồm `public` và `candidates`.

## Kết quả

Một đối tượng JSON gồm `pair`, `if_a`, `if_b` (kích thước tập còn lại ứng với mỗi câu trả lời) và `worst_case`.

## Giới hạn

- Không quá $12$ vật. Không vật nào cách đều hai vật khác.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "public": {
    "apple": [-8, 9],
    "book": [9, 5],
    "chair": [1, 0],
    "desk": [-9, -9],
    "egg": [-2, 9],
    "fan": [-6, -8],
    "glass": [9, -3],
    "hat": [3, -5],
    "ink": [-9, -8],
    "lamp": [7, -5]
  },
  "candidates": ["desk", "egg", "fan", "glass"]
}
```

```output
{"pair": ["desk", "egg"], "if_a": 2, "if_b": 2, "worst_case": 2}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
