# Chọn alpha

Mức phạt `alpha` của Ridge là siêu tham số, nên ta chọn nó bằng cross-validation trên tập phát triển, như bài 1.7.

Dùng `GridSearchCV` với pipeline `StandardScaler()` rồi `Ridge(solver="cholesky")`, thử `alpha` lần lượt là $0.1$, $1$, $10$. Các fold cho sẵn trong cột `fold` của `dev.csv`, dùng `PredefinedSplit(dev["fold"])`. Chấm bằng `scoring="neg_mean_squared_error"` và `refit=True`. Hòa điểm thì `alpha` đứng trước thắng. Sau cùng dự đoán cho `test.csv`.

Thư viện trả về MSE mang dấu âm, để "lớn hơn là tốt hơn". Khi báo cáo, đổi dấu lại.

## Dữ liệu vào

Mỗi thư mục test có `dev.csv` (cột `x0`, `x1`, `label`, `fold`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON gồm `cv_mse` (MSE trung bình qua ba fold cho từng `alpha`, theo thứ tự trên), `best_alpha`, `predictions` và `fit_count`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
