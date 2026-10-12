# Rừng bốn góc

Cùng bài toán bốn góc của buổi 2.5, giờ dùng cả một rừng cây. Hãy học `RandomForestClassifier(n_estimators=40, max_depth=4, max_features=2, n_jobs=1, random_state=42)` trên `train.csv`, rồi dự đoán cho `test.csv`.

So thêm với một cây đơn lẻ cùng độ sâu. Rừng có ổn định hơn khi đổi `random_state` không?

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x0`, `x1`, `label`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy trên test từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
