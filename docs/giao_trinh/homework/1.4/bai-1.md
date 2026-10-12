# Chuẩn hóa

Xưởng robot đo chiều cao `height` và năng lượng `energy` của mỗi robot. Hai cột có thang đo rất khác nhau, nên trước khi đưa vào mô hình ta chuẩn hóa từng cột về trung bình $0$, độ lệch chuẩn $1$.

Chiếc thước, tức trung bình và độ lệch chuẩn, chỉ được học trên train. Robot ở test được đo bằng đúng chiếc thước ấy, dù chúng có khác robot ở train. Nói theo code, gọi `fit` của `StandardScaler` trên `train.csv`, còn với `test.csv` thì chỉ gọi `transform`.

Cột có mọi giá trị bằng nhau thì thang đo là $1$, thư viện tự lo việc này.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` và `test.csv` với hai cột `height`, `energy`.

## Kết quả

Một đối tượng JSON gồm `mean` và `scale` (hai số mỗi trường, tức `scaler.mean_` và `scaler.scale_`) cùng `features` (các hàng của test sau khi biến đổi).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
