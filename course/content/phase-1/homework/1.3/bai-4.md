# K-fold

Ta chọn $k$ cho kNN hồi quy một chiều của bài 1.2 bằng K-fold cross-validation.

Chia `data` thành $K$ phần liền nhau, bằng nhau, giữ đúng thứ tự cho sẵn, không xáo trộn. Với mỗi $k$ và mỗi phần, học trên các phần còn lại rồi tính MSE trên phần đang giữ. Điểm CV của $k$ là trung bình $K$ giá trị MSE ấy. Chọn `best_k` có điểm CV nhỏ nhất, hòa thì lấy $k$ nhỏ hơn.

kNN hồi quy làm như bài 1.2. Dự đoán là trung bình nhãn của $k$ điểm gần nhất theo khoảng cách $|x-q|$, và hai điểm cách đều thì điểm có $x$ nhỏ hơn được coi là gần hơn.

## Dữ liệu vào

Một đối tượng JSON gồm `data` (các cặp `[x, y]`, các $x$ khác nhau), `folds` là $K$, và `ks`.

## Kết quả

Một đối tượng JSON gồm `cv_mse` (một số cho mỗi $k$) và `best_k`.

## Giới hạn

- $2\le K\le10$, số hàng $n\le120$ và chia hết cho $K$.
- $0\le x\le1000$, $|y|\le100$, đều là số nguyên.
- Có từ $1$ đến $5$ giá trị $k$, mỗi giá trị không vượt quá số hàng train của một fold.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "data": [[1, 2], [6, 7], [3, 3], [8, 9], [2, 1], [7, 6]],
  "folds": 3,
  "ks": [1, 2]
}
```

```output
{"cv_mse": [2.8333333333333335, 2.5], "best_k": 2}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
