# K-means++

K-Means dễ kẹt ở nghiệm xấu nếu các tâm ban đầu nằm sát nhau. Khởi tạo k-means++ chọn tâm sao cho chúng thường nằm xa nhau:

1. Tâm đầu tiên là điểm có số thứ tự `first`.
2. Mỗi lần chọn tâm tiếp theo, tính $D(x)^2$ là bình phương khoảng cách từ mỗi điểm $x$ tới tâm gần nhất đã chọn. Điểm $x$ được chọn với xác suất $\dfrac{D(x)^2}{\sum_y D(y)^2}$.

Để kết quả xác định, đề cho sẵn các số ngẫu nhiên $u$ trong `draws`, mỗi lần chọn dùng một số. Với số $u$, đi qua các điểm theo thứ tự, cộng dồn $D(x)^2$, và chọn điểm đầu tiên làm tổng cộng dồn **lớn hơn** $u\cdot\sum_y D(y)^2$.

Có đủ $k$ tâm thì chạy Lloyd: gán mỗi điểm về tâm gần nhất (cách đều thì về tâm có số thứ tự nhỏ hơn), rồi lặp lại hai việc:

- Dời mỗi tâm về trung bình các điểm của nó. Tâm không có điểm nào thì giữ nguyên.
- Gán lại. Nếu cách gán không đổi thì dừng.

Dừng cả khi đã dời tâm `max_iter` lần. Cuối cùng gán lại theo các tâm sau cùng và tính inertia.

## Dữ liệu vào

Một đối tượng JSON gồm `X` (các điểm hai chiều, tọa độ nguyên, không trùng nhau), `k`, `first`, `draws` ($k-1$ số) và `max_iter`.

## Kết quả

Một đối tượng JSON gồm:

- `seeds`: số thứ tự các điểm được chọn làm tâm ban đầu.
- `probabilities`: với mỗi lần chọn tâm thứ hai trở đi, xác suất được chọn của từng điểm.
- `centers`, `assignment`, `inertia`: các tâm, cách gán và inertia sau cùng.
- `iterations`: số lần đã dời tâm.

## Giới hạn

- $2\le k\le n\le20$ và $1\le$ `max_iter` $\le10$.
- Không có điểm nào cách đều hai tâm, và không tổng cộng dồn nào sát đúng $u\cdot\sum_y D(y)^2$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[0, 0], [1, 2], [2, 3], [3, 1], [4, 1]],
  "k": 3,
  "first": 0,
  "draws": [0.3, 0.9],
  "max_iter": 10
}
```

```output
{
  "seeds": [0, 2, 4],
  "probabilities": [
    [
      0.0, 0.1111111111111111, 0.28888888888888886, 0.2222222222222222,
      0.37777777777777777
    ],
    [
      0.0, 0.13333333333333333, 0.0, 0.3333333333333333,
      0.5333333333333333
    ]
  ],
  "centers": [[0.0, 0.0], [1.5, 2.5], [3.5, 1.0]],
  "assignment": [0, 1, 1, 2, 2],
  "iterations": 1,
  "inertia": 1.5
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
