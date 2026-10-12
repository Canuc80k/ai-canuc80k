# Bảng hỗn hợp

Bảng robot giờ có đủ cả số, chữ và ô trống. `height`, `energy` là số, còn `color` là màu áo. Hãy dựng bộ tiền xử lý như mục Ghép ColumnTransformer với Pipeline của bài học, học trên train rồi biến đổi test.

Nhánh số, đặt tên `"num"`, điền ô trống bằng median rồi chuẩn hóa, tức `SimpleImputer(strategy="median", keep_empty_features=True)` nối với `StandardScaler()`. Nhánh chữ, đặt tên `"cat"`, điền ô trống bằng màu hay gặp nhất rồi one-hot, tức `SimpleImputer(strategy="most_frequent")` nối với `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`. Nhánh số đứng trước.

Ở test có thể xuất hiện một màu chưa từng gặp, chẳng hạn áo cam. Nhờ `handle_unknown="ignore"`, hàng ấy có mọi cột one-hot bằng $0$ và bảng vẫn giữ đúng các cột đã học. Một cột số cũng có thể trống hoàn toàn ở train, khi đó `keep_empty_features=True` giữ cột lại và điền $0$.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` và `test.csv` với ba cột `height`, `energy`, `color`.

## Kết quả

Một đối tượng JSON gồm `feature_names` (kết quả của `get_feature_names_out()`) và `features` (các hàng của test sau biến đổi).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
