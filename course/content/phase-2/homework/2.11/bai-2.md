# Target encoding

Target encoding thay mỗi danh mục bằng trung bình nhãn của danh mục ấy. Nếu tính trung bình bằng cả nhãn của chính hàng đang mã hóa thì mô hình được nhìn trước đáp án. Cách chữa là mã hóa chéo theo fold: hàng thuộc fold nào thì chỉ dùng các hàng của những fold còn lại.

Với một tập hàng dùng để tính, gọi `prior` là trung bình nhãn của cả tập. Danh mục $c$ có tổng nhãn $S_c$ và số hàng $n_c$ trong tập ấy được mã hóa thành

$$
\frac{S_c+m\cdot\text{prior}}{n_c+m},
$$

với $m$ là `smoothing`. Danh mục không xuất hiện trong tập thì nhận `prior`.

- Mỗi hàng của `rows.csv` dùng tập gồm các hàng thuộc fold khác.
- Mỗi hàng của `test.csv` dùng toàn bộ `rows.csv`.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` (cột `category`, `label`, `fold` từ $0$ đến $2$), `test.csv` (cột `category`) và `input.json` chứa `smoothing`. Danh mục là chuỗi, `"002"` khác `"2"`.

## Kết quả

Một đối tượng JSON gồm `oof` (giá trị mã hóa của từng hàng `rows.csv`) và `test_encoding` (của từng hàng `test.csv`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
input.json:
{"smoothing": 0.0}

rows.csv:
category,label,fold
A,0.0,0
B,1.0,1
002,2.0,2
2,3.0,0
singleton,4.0,1
A,5.0,2
B,6.0,0
002,0.0,1
2,1.0,2
singleton,2.0,0
A,3.0,1
B,4.0,2
002,5.0,0
2,6.0,1
singleton,0.0,2
A,1.0,0
B,2.0,1
002,3.0,2
2,4.0,0
singleton,5.0,1
A,6.0,2
B,0.0,0
002,1.0,1
2,2.0,2
singleton,3.0,0
A,4.0,1
B,5.0,2
002,6.0,0
2,0.0,1
rare,1.0,2

test.csv:
category
A
B
002
2
unseen
rare
```

```output
{
  "oof": [
    4.5, 3.75, 3.0, 2.25, 1.6666666666666667, 2.0, 3.0, 4.0, 3.25, 3.0,
    3.0, 2.25, 1.5, 2.5, 3.5, 4.5, 3.75, 3.0, 2.25, 1.6666666666666667,
    2.0, 3.0, 4.0, 3.25, 3.0, 3.0, 2.25, 1.5, 2.5, 2.8
  ],
  "test_encoding": [
    3.1666666666666665, 3.0, 2.8333333333333335, 2.6666666666666665,
    2.8333333333333335, 1.0
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
