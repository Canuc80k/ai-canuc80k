# Thang đo

Một cột đo bằng mét, cột kia đo bằng milimét. Với kNN, cột có số lớn sẽ gần như một mình quyết định khoảng cách. Bài này so kNN trước và sau khi chuẩn hóa trên cùng dữ liệu.

Hãy học hai mô hình trên `train.csv` rồi dự đoán cho `test.csv`. Mô hình thứ nhất là `KNeighborsClassifier(n_neighbors=5, algorithm="brute")` trên số liệu gốc. Mô hình thứ hai là pipeline `StandardScaler()` rồi cùng bộ kNN ấy. Thước đo của scaler học trên train.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x0`, `x1`, `label`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON gồm `raw_predictions` và `scaled_predictions`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
