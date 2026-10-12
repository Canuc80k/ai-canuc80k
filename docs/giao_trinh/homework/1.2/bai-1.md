# Chọn k

Mỗi mẫu là một cặp $(x, y)$ với $x$ từ $0$ đến $1$. Nhãn $y$ đi theo một đường cong trơn, có thêm chút nhiễu. Hãy học đường cong từ train bằng `KNeighborsRegressor` rồi dự đoán cho test.

Trước khi nộp, hãy thử vài giá trị $k$ và ghi MAE trên cả train lẫn validation. Thử ít nhất $k=1$, $k$ bằng số mẫu train, và vài giá trị ở giữa. Với $k=1$, mô hình chép nguyên nhãn train, kể cả nhiễu, nên MAE train bằng $0$ nhưng validation thì không. Với $k$ bằng số mẫu train, mô hình đoán mọi điểm như nhau. Chọn $k$ bằng validation.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` ($100$ hàng) và `valid.csv` ($50$ hàng) với hai cột `x`, `label`, và `test.csv` ($50$ hàng) chỉ có `x`.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}` gồm $50$ dự đoán theo thứ tự hàng của `test.csv`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi MAE trên test không quá $0.25$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
