# Từ đầu đến cuối

Bài này đi trọn một vòng: đánh giá bằng cross-validation, học lại trên toàn bộ train, dự đoán test, rồi ghép theo `sample.csv`.

Mỗi người (`group`) có nhiều hàng, và cả nhóm nằm trọn trong một fold cho sẵn ở cột `fold`. Nhờ vậy validation luôn là người mới.

1. Với mỗi fold $f$ từ $0$ đến $2$, học `make_pipeline(StandardScaler(), Ridge(alpha=0.1))` trên các hàng không thuộc fold $f$, dùng hai cột `x0`, `x1`. Tính MAE trên fold $f$.
2. Học lại mô hình ấy trên toàn bộ train, dự đoán cho `test.csv`.
3. Ghép dự đoán theo `id` và trả theo thứ tự của `sample.csv`.

Không dùng `id`, `group` hay `fold` làm đặc trưng. Tổng cộng có $4$ lần học mô hình.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `id`, `group`, `fold`, `x0`, `x1`, `label`), `test.csv` (cột `id`, `x0`, `x1`) và `sample.csv` (cột `id`).

## Kết quả

Một đối tượng JSON gồm `fold_mae` (ba số), `rows` (mỗi phần tử là `{"id": ..., "target": ...}`) và `fit_count` (bằng $4$).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
