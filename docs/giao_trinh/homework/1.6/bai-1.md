# RMSE

Một robot cân hàng rồi đoán khối lượng. Tệp `weighing.csv` ghi khối lượng thật `truth` và số robot đoán `prediction`. Hãy tính bốn thước đo của bài học: MAE, MSE, RMSE và $R^2$.

RMSE là căn của MSE, tức căn của trung bình bình phương sai số. Cẩn thận đừng lấy trung bình của các căn, vì như thế lại ra MAE.

$R^2$ so mô hình với cách đoán mọi mẫu bằng trung bình của chính các khối lượng thật trong tệp:

$$
R^2=1-\frac{\sum_i(y_i-\hat y_i)^2}{\sum_i(y_i-\bar y)^2}.
$$

$R^2$ có thể âm, khi mô hình còn tệ hơn cách đoán trung bình. Nếu mọi khối lượng thật bằng nhau thì mẫu số bằng $0$, $R^2$ không xác định và ta trả `null`.

Mỗi tệp có một món hàng bị đoán lệch rất xa. Hãy so MAE với RMSE để thấy thước đo nào nhạy hơn với nó.

## Dữ liệu vào

Mỗi thư mục test có `weighing.csv` với hai cột `truth`, `prediction`.

## Kết quả

Một đối tượng JSON gồm `mae`, `mse`, `rmse`, `r2`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
