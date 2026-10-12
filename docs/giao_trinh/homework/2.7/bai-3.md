# Dừng sớm

Boosting thêm càng nhiều cây thì lỗi train càng giảm, nhưng tới một lúc lỗi validation lại tăng. Ta dừng ở số cây cho lỗi validation nhỏ nhất.

Học `GradientBoostingRegressor(n_estimators=50, max_depth=2, learning_rate=0.1, random_state=42)` trên `train.csv`. Dùng `staged_predict` để có dự đoán sau từng số cây, tính MSE trên `valid.csv` cho cả $50$ mốc, chọn mốc có MSE nhỏ nhất (hòa thì lấy mốc sớm hơn), rồi dự đoán `test.csv` bằng đúng mốc ấy.

In mốc đã chọn và MSE validation ra màn hình để xem lại trong notebook.

## Dữ liệu vào

Mỗi thư mục test có `train.csv`, `valid.csv` (cột `x`, `label`) và `test.csv` (cột `x`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi MAE trên test không quá $0.25$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
