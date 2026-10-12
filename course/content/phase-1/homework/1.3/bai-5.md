# Fold khối

Cùng một dữ liệu một feature $x$, ta thử hai cách chia K-fold rồi xem điểm CV khác nhau thế nào.

- **Cách 1**: mỗi hàng đã được gán ngẫu nhiên vào một fold, ghi trong list `fold`.
- **Cách 2**: sắp các hàng theo $x$ tăng dần rồi cắt thành $K$ khối liền nhau, bằng nhau.

Mô hình là đường thẳng $\hat y=wx+b$. Ở mỗi fold, học $w, b$ trên các hàng còn lại bằng công thức bình phương nhỏ nhất

$$
w=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sum_i(x_i-\bar x)^2},\qquad b=\bar y-w\bar x,
$$

rồi tính MSE trên các hàng của fold. Điểm CV là trung bình MSE của $K$ fold.

## Dữ liệu vào

Một đối tượng JSON gồm `data` (các cặp `[x, y]`, các $x$ khác nhau), `fold` cho cách 1, và `folds` là $K$.

## Kết quả

Một đối tượng JSON gồm `given_fold_mse` và `given_cv_mse` cho cách 1, `sorted_fold_mse` và `sorted_cv_mse` cho cách 2. Các list MSE theo thứ tự fold, hay khối, từ $0$ đến $K-1$.

## Giới hạn

- $2\le K\le5$, số hàng $n\le100$ và chia hết cho $K$. Ở cách 1, mỗi fold có $n/K$ hàng.
- $|x|\le50$, $|y|\le1000$, đều là số nguyên.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "data": [[0, 4], [1, 1], [2, 0], [3, 1], [4, 4], [5, 9]],
  "fold": [0, 1, 2, 0, 1, 2],
  "folds": 3
}
```

```output
{
  "given_fold_mse": [24.25, 1.0, 24.25],
  "given_cv_mse": 16.5,
  "sorted_fold_mse": [73.0, 16.0, 73.0],
  "sorted_cv_mse": 54.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
