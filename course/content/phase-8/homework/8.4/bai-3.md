# Ghép đúng hàng cột

Gộp dự đoán của hai model tưởng đơn giản, cho tới khi hai bảng dự đoán không cùng thứ tự hàng (ID) hay không cùng thứ tự cột (lớp). Cộng theo vị trí lúc ấy là cộng nhầm mẫu, nhầm lớp, mà code vẫn chạy.

Mỗi model cho `ids` (thứ tự hàng của nó), `classes` (thứ tự cột của nó) và `probs`. Thứ tự chuẩn là `ids` và `classes` ở ngoài cùng.

1. Với mỗi model, đổi cột theo **tên lớp** và đổi hàng theo **mã** về thứ tự chuẩn.
2. Lấy trung bình xác suất của các model.
3. Dự đoán là tên lớp có xác suất lớn nhất.

Mã là chuỗi: `"002"` và `"2"` là hai mẫu khác nhau.

## Dữ liệu vào

Một đối tượng JSON gồm `ids`, `classes` và `models` (mỗi model là `{"ids", "classes", "probs"}`).

## Kết quả

Một đối tượng JSON gồm `ids`, `probs` (theo thứ tự chuẩn) và `pred`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "ids": ["002", "x", "2"],
  "classes": ["owl", "cat", "fox"],
  "models": [
    {
      "ids": ["2", "002", "x"],
      "classes": ["fox", "owl", "cat"],
      "probs": [[0.034, 0.276, 0.69], [0.45, 0.2, 0.35], [0.333, 0.2, 0.467]]
    },
    {
      "ids": ["2", "002", "x"],
      "classes": ["cat", "owl", "fox"],
      "probs": [
        [0.073, 0.488, 0.439],
        [0.467, 0.5, 0.033],
        [0.372, 0.302, 0.326]
      ]
    }
  ]
}
```

```output
{
  "ids": ["002", "x", "2"],
  "probs": [
    [0.35, 0.4085, 0.2415],
    [0.251, 0.4195, 0.3295],
    [0.382, 0.38149999999999995, 0.2365]
  ],
  "pred": ["cat", "cat", "owl"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
