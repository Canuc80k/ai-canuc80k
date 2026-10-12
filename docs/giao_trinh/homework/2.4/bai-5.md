# 1-NN thành cây

Dữ liệu chỉ có một feature $x$, mỗi điểm mang nhãn `+` hoặc `-`. Bộ phân loại 1-NN đoán nhãn của điểm train gần nhất. Khi hai điểm train cách đều, điểm bên trái được coi là gần hơn.

Có thể dựng một cây quyết định đoán y hệt bộ 1-NN này với mọi đầu vào. Các ngưỡng chia của cây nằm ở trung điểm giữa hai điểm train liền nhau mang nhãn khác nhau. Mỗi ngưỡng tách trục số thành các đoạn, và mỗi đoạn mang một nhãn.

Hãy tìm:

- `thresholds`: các ngưỡng của cây, tăng dần.
- `leaf_labels`: nhãn của từng đoạn, từ trái sang phải. Số đoạn bằng số ngưỡng cộng $1$.
- `predictions`: nhãn mà bộ 1-NN đoán cho từng truy vấn.

Một truy vấn đúng bằng ngưỡng thì cách đều hai điểm train hai bên, nên thuộc đoạn bên trái.

## Dữ liệu vào

Một đối tượng JSON gồm `x`, `y` (nhãn từng điểm, theo thứ tự bất kỳ) và `queries`.

## Kết quả

Một đối tượng JSON gồm `thresholds`, `leaf_labels`, `predictions`.

## Giới hạn

- Từ $1$ đến $30$ điểm train, các $x$ là số nguyên khác nhau trong $[-50, 50]$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [1, 2, 4, 6, 7, 9],
  "y": ["-", "-", "+", "+", "-", "+"],
  "queries": [0, 3, 3.5, 5, 6.5, 8, 10]
}
```

```output
{
  "thresholds": [3.0, 6.5, 8.0],
  "leaf_labels": ["-", "+", "-", "+"],
  "predictions": ["-", "-", "+", "+", "+", "-", "+"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
