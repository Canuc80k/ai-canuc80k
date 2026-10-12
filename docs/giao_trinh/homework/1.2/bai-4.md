# kNN một chiều

kNN hồi quy dự đoán tại điểm $q$ bằng trung bình nhãn của $k$ điểm train gần $q$ nhất. Dữ liệu ở đây chỉ có một feature, nên khoảng cách là $|x-q|$. Khi hai điểm cách $q$ bằng nhau, coi điểm có $x$ nhỏ hơn là gần hơn.

Với mỗi $k$ trong `ks`, hãy dự đoán tại mọi điểm trong `queries`, và tính MSE trên chính tập train. Khi dự đoán tại một điểm train, bản thân điểm ấy cũng là hàng xóm, ở khoảng cách $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `train` (các cặp `[x, y]`, các $x$ khác nhau), `queries` và `ks`.

## Kết quả

Một đối tượng JSON gồm `predictions` (với mỗi $k$, một list dự đoán cho các truy vấn) và `train_mse` (với mỗi $k$, một số).

## Giới hạn

- Có từ $1$ đến $200$ điểm train với $|x|\le1000$, $|y|\le100$, đều là số nguyên.
- Có từ $1$ đến $60$ truy vấn nguyên với $|q|\le1100$.
- Có từ $1$ đến $5$ giá trị $k$, mỗi giá trị không vượt quá số điểm train.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "train": [[1, 3], [2, 1], [4, 4], [5, 2], [7, 6]],
  "queries": [3, 6, 0],
  "ks": [1, 2, 3, 5]
}
```

```output
{
  "predictions": [
    [1.0, 2.0, 3.0],
    [2.5, 4.0, 2.0],
    [2.6666666666666665, 4.0, 2.6666666666666665],
    [3.2, 3.2, 3.2]
  ],
  "train_mse": [0.0, 1.6, 2.7333333333333334, 2.96]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
