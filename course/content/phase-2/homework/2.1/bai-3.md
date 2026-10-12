# Bậc hai

Nhiệt độ của chiếc lò nhỏ thay đổi theo một đường cong. Đường cong vẫn học được bằng hồi quy tuyến tính, chỉ cần thêm cột $x^2$: mô hình $\hat y = w_1x + w_2x^2 + b$ vẫn tuyến tính theo các trọng số.

Dựng pipeline `PolynomialFeatures(degree=2, include_bias=False)` rồi `LinearRegression()`, học trên `train.csv` và dự đoán cho `test.csv`. Đặt `include_bias=False` vì `LinearRegression` đã tự có hệ số tự do.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x`, `label`) và `test.csv` (cột `x`).

## Kết quả

Một đối tượng JSON gồm `predictions` (theo thứ tự hàng của test), `weights` (hai trọng số của $x$ và $x^2$) và `bias`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
