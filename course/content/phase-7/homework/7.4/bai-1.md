# Ghép theo ID và giờ

Trước khi ghép âm thanh với hình ảnh, phải chắc hai bên đang nói về cùng một mẫu và cùng một khoảng thời gian. Ghép chỉ theo thời gian là sai khi hai mẫu khác nhau trùng giờ; ghép chỉ theo mã thì lấy cả những cửa sổ nằm ngoài đoạn cần.

Mỗi mẫu trong `samples` có `id`, `start`, `end` (giây, cùng một đồng hồ). Mỗi cửa sổ trong `windows` có `id`, `start`, `end` và vector `features` ($D$ số).

Với mỗi mẫu, theo thứ tự trong `samples`:

1. Chỉ xét các cửa sổ có **cùng mã** (so như chuỗi: `"002"` khác `"2"`).
2. Trọng số của cửa sổ là độ dài phần giao: $\max\big(0,\min(\text{end})-\max(\text{start})\big)$. Hai đoạn chỉ chạm nhau ở mút có giao bằng $0$.
3. `overlap_weight` là tổng trọng số; `features` là trung bình có trọng số của các vector, hoặc `null` nếu tổng bằng $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `dimension`, `samples` và `windows`.

## Kết quả

Một đối tượng JSON gồm `ids`, `overlap_weight` và `features`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "dimension": 2,
  "samples": [
    {"id": "002", "start": 0, "end": 1},
    {"id": "2", "start": 0, "end": 1},
    {"id": "x", "start": 2, "end": 3}
  ],
  "windows": [
    {"id": "002", "start": 0.5, "end": 2, "features": [5, 7]},
    {"id": "x", "start": 3, "end": 4, "features": [9, 9]},
    {"id": "2", "start": 0, "end": 1, "features": [100, 200]},
    {"id": "002", "start": -0.5, "end": 0.5, "features": [1, 3]}
  ]
}
```

```output
{
  "ids": ["002", "2", "x"],
  "overlap_weight": [1.0, 1, 0],
  "features": [[3.0, 5.0], [100.0, 200.0], null]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
