# Grid search

Ba cấu hình kNN với $k=1, 3, 5$ thi trên cùng một đường đua: cùng các fold, cùng thước đo F1. Bài này làm đúng mục Chạy grid và đọc bảng log của bài học.

Dùng `GridSearchCV` với pipeline `StandardScaler()` rồi `KNeighborsClassifier`, `scoring="f1"` và `refit=True`. Các fold cho sẵn trong cột `fold` của `dev.csv`, dùng `PredefinedSplit(dev["fold"])`. Feature là `x0`, `x1`. Hòa điểm CV thì cấu hình đứng trước thắng, `GridSearchCV` làm sẵn việc này. Sau cùng, dự đoán cho `test.csv` bằng mô hình đã fit lại.

Cột `mean_test_score` trong `cv_results_` là điểm trên các fold validation, không phải điểm trên `test.csv`.

## Dữ liệu vào

Mỗi thư mục test có `dev.csv` (cột `x0`, `x1`, `label`, `fold`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON gồm:

- `scores`: với mỗi $k$ theo thứ tự $1, 3, 5$, đối tượng `{"k": ..., "fold_f1": [ba số], "mean_cv_f1": ...}`.
- `best_k`, `best_cv_f1`.
- `predictions`: nhãn cho từng hàng của `test.csv`.
- `fit_count`: tổng số lần fit, tính cả lần fit lại.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
