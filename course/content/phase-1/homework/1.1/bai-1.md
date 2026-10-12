# Pha màu

Xưởng pha màu trộn ba loại bột. Cột `sun` và `moon` là tỉ lệ của hai loại bột đầu trong hỗn hợp, còn cột `label` là độ đỏ của màu sau khi trộn. Hãy học từ các mẻ cũ để đoán độ đỏ của các mẻ mới.

Làm theo đúng quy trình của bài học. Học mô hình trên `train.csv`, chẳng hạn `LinearRegression`, với feature là các cột ghi trong `feature_columns` của `input.json`. Đo MAE trên `valid.csv` và so với cách đoán mọi mẻ bằng trung bình `label` của train. Mô hình tốt thì phải hơn hẳn cách đoán ấy. Cuối cùng dự đoán cho `test.csv`, giữ đúng thứ tự hàng.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` ($80$ hàng) và `valid.csv` ($20$ hàng) với các cột `id`, `sun`, `moon`, `label`, và `test.csv` ($20$ hàng) chưa có `label`.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}` gồm $20$ dự đoán theo thứ tự hàng của `test.csv`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi MAE trên test không quá $1.5$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
