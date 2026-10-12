# MAPE

MAPE đo sai số theo phần trăm của giá trị thật. Nghe rất dễ hiểu, cho đến khi giá trị thật bằng $0$ hoặc rất gần $0$.

scikit-learn tính MAPE như sau, với $\varepsilon=2^{-52}$ để mẫu số không bao giờ bằng $0$:

$$
\text{ratio}=\frac1n\sum_i\frac{|\hat y_i-y_i|}{\max(|y_i|,\varepsilon)}.
$$

Hàm `mean_absolute_percentage_error` trả về đúng `ratio` này, không nhân $100$. Hãy tính `ratio`, `percent` $=100\cdot\text{ratio}$, và đếm số giá trị thật bằng đúng $0$.

Mỗi tệp có một vài giá trị thật bằng $0$ hoặc gần $0$, như một hạt bụi trên cân. Nhìn xem MAPE thành bao nhiêu, và tự hỏi con số ấy còn nói lên điều gì không.

## Dữ liệu vào

Mỗi thư mục test có `weighing.csv` với hai cột `truth`, `prediction`.

## Kết quả

Một đối tượng JSON gồm `ratio`, `percent`, `zero_targets`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số tương đối khoảng $10^{-8}$, kể cả khi rất lớn.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
