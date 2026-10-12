# Rừng tính tay

Ta tự dựng một rừng nhỏ trên dữ liệu một feature, rồi chấm nó bằng lỗi out-of-bag.

Mỗi cây là một **stump**, tức cây chỉ có một phép chia. Một stump có ngưỡng $t$ và chiều `sign`. Với `sign` bằng $1$, nó đoán $1$ khi $x>t$, còn lại đoán $0$. Với `sign` bằng $-1$ thì ngược lại.

Cây thứ $b$ học trên lượt rút `bootstraps[b]`, kể cả các mẫu được rút nhiều lần. Ứng viên ngưỡng là trung điểm của hai giá trị $x$ khác nhau liền nhau trong lượt rút. Chọn ngưỡng và chiều cho ít lỗi nhất trên lượt rút. Hòa thì ưu tiên ngưỡng nhỏ hơn, rồi tới chiều $1$. Nếu lượt rút chỉ có một giá trị $x$ thì không có ngưỡng nào, cây đoán hằng số là nhãn đa số của lượt rút (hòa thì $0$).

Sau đó, mỗi mẫu được các cây chưa thấy nó bỏ phiếu. Nhãn nhiều phiếu hơn thắng, hòa thì $0$. Mẫu không có cây nào bỏ phiếu thì không có dự đoán. Lỗi OOB là tỉ lệ đoán sai trên các mẫu có dự đoán.

## Dữ liệu vào

Một đối tượng JSON gồm `x` (số nguyên khác nhau), `y` và `bootstraps`.

## Kết quả

Một đối tượng JSON gồm:

- `stumps`: mỗi cây là `{"threshold": t, "sign": s}`, hoặc `{"constant": c}` nếu đoán hằng số.
- `oob_votes`: với mỗi mẫu, số phiếu cho nhãn $0$ và nhãn $1$.
- `oob_prediction`: nhãn OOB của mỗi mẫu, hoặc `null`.
- `oob_error`: lỗi OOB, hoặc `null` nếu không mẫu nào có dự đoán.

## Giới hạn

- Từ $3$ đến $30$ mẫu, không quá $16$ cây.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [1, 2, 3, 4, 5, 6],
  "y": [0, 0, 1, 0, 1, 1],
  "bootstraps": [[0, 1, 1, 3, 4, 5], [0, 2, 2, 3, 5, 5], [1, 2, 3, 3, 4, 4]]
}
```

```output
{
  "stumps": [
    {"threshold": 4.5, "sign": 1},
    {"threshold": 2.0, "sign": 1},
    {"threshold": 4.5, "sign": 1}
  ],
  "oob_votes": [[1, 0], [1, 0], [1, 0], [0, 0], [0, 1], [0, 1]],
  "oob_prediction": [0, 0, 0, null, 1, 1],
  "oob_error": 0.2
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
