# Silhouette

Silhouette đo một điểm nằm gọn trong cụm của nó đến đâu. Với điểm $i$:

- $a(i)$ là khoảng cách trung bình tới các điểm khác cùng cụm.
- $b(i)$ là khoảng cách trung bình tới các điểm của một cụm khác, lấy cụm cho giá trị nhỏ nhất.
- $s(i)=\dfrac{b(i)-a(i)}{\max\big(a(i),b(i)\big)}$.

Khoảng cách là khoảng cách Euclid, không bình phương. Điểm nằm một mình một cụm có $s=0$. Nếu mẫu số bằng $0$ thì $s=0$.

Silhouette chỉ có nghĩa khi số cụm từ $2$ đến $n-1$. Ngoài khoảng ấy, ghi cả hai kết quả là `null`. Nhãn cụm chỉ là tên gọi, số nào cũng được.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (các điểm hai chiều) và `labels`.

## Kết quả

Một đối tượng JSON gồm `per_sample` (silhouette của từng điểm) và `mean` (trung bình của chúng).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[0, 0], [1, 0], [4, 0], [5, 0], [20, 0]],
  "labels": [3, 3, 7, 7, 9]
}
```

```output
{
  "per_sample": [
    0.7777777777777778, 0.7142857142857143, 0.7142857142857143,
    0.7777777777777778, 0.0
  ],
  "mean": 0.5968253968253968
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
