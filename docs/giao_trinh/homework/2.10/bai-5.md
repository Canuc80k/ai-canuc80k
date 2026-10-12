# Gộp cụm

Gộp cụm phân cấp bắt đầu với mỗi điểm là một cụm, rồi lặp lại việc gộp hai cụm gần nhau nhất cho tới khi chỉ còn một cụm. "Gần" giữa hai cụm $A$, $B$ được đo theo một trong ba kiểu linkage:

| Linkage | Khoảng cách giữa $A$ và $B$ |
|---|---|
| single | nhỏ nhất trong các $d(i,j)$ với $i\in A$, $j\in B$ |
| complete | lớn nhất trong các $d(i,j)$ ấy |
| average | trung bình của các $d(i,j)$ ấy |

Ta chỉ có bảng khoảng cách $d(i,j)$ giữa các điểm. Mỗi cụm được gọi bằng số thứ tự nhỏ nhất của các điểm trong nó. Viết mỗi cặp cụm bằng hai tên $(a,b)$ với $a<b$. Nếu nhiều cặp cùng gần nhất, chọn cặp có $a$ nhỏ nhất, còn hòa thì chọn cặp có $b$ nhỏ nhất.

Hãy chạy cả ba kiểu linkage. Với mỗi kiểu, ghi lại các lần gộp, và cách chia khi còn đúng $k$ cụm. Trong cách chia ấy, đánh số các cụm $0,1,2,\dots$ theo thứ tự tên cụm.

## Dữ liệu vào

Một đối tượng JSON gồm `D` (bảng khoảng cách $n\times n$, số nguyên, đối xứng, đường chéo bằng $0$) và `k`.

## Kết quả

Một đối tượng JSON gồm ba trường `single`, `complete`, `average`. Mỗi trường là `{"merges": [...], "labels": [...]}`:

- `merges`: $n-1$ lần gộp theo thứ tự, mỗi lần là `[a, b, d]` với $a<b$ là tên hai cụm và $d$ là khoảng cách giữa chúng.
- `labels`: số thứ tự cụm của từng điểm khi còn $k$ cụm.

## Giới hạn

- $2\le n\le12$ và $1\le k\le n$.
- Với average linkage, không có hai cặp cụm nào cùng gần nhất hoặc sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "D": [
    [0, 2, 3, 6, 8, 11],
    [2, 0, 1, 4, 6, 9],
    [3, 1, 0, 3, 5, 8],
    [6, 4, 3, 0, 2, 5],
    [8, 6, 5, 2, 0, 3],
    [11, 9, 8, 5, 3, 0]
  ],
  "k": 2
}
```

```output
{
  "single": {
    "merges": [[1, 2, 1], [0, 1, 2], [3, 4, 2], [0, 3, 3], [0, 5, 3]],
    "labels": [0, 0, 0, 0, 0, 1]
  },
  "complete": {
    "merges": [[1, 2, 1], [3, 4, 2], [0, 1, 3], [3, 5, 5], [0, 3, 11]],
    "labels": [0, 0, 0, 1, 1, 1]
  },
  "average": {
    "merges": [
      [1, 2, 1.0],
      [3, 4, 2.0],
      [0, 1, 2.5],
      [3, 5, 4.0],
      [0, 3, 6.666666666666667]
    ],
    "labels": [0, 0, 0, 1, 1, 1]
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
