# Ba lớp

Ba hành tinh, mỗi điểm dữ liệu có hai tọa độ `x0`, `x1` và nhãn hành tinh $0$, $1$ hoặc $2$. Hãy tự huấn luyện softmax regression bằng gradient descent.

Bắt đầu từ $W=0$ (cỡ $2\times3$) và $b=0$ ($3$ số). Lặp đúng $250$ lần với tốc độ học $0.2$:

1. $P=\operatorname{softmax}(XW+b)$ theo từng hàng.
2. $G=(P-Y)/n$, với $Y$ là one-hot của nhãn.
3. $W \leftarrow W-0.2\,(X^\top G+0.01\,W)$ và $b \leftarrow b-0.2\sum_i G_i$.

Số hạng $0.01\,W$ đến từ phạt $0.005\lVert W\rVert^2$. Hệ số tự do không bị phạt. Sau cùng dự đoán cho test bằng lớp có xác suất lớn nhất, hòa thì lấy lớp nhỏ hơn.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x0`, `x1`, `label`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON gồm `predictions`, `probabilities` (của test), `weights` ($2\times3$) và `bias`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
