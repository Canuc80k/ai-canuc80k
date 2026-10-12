# Pipeline CV

Chuẩn hóa cũng là một phần của mô hình, nên trong cross-validation, mỗi fold phải học lại cả chiếc thước. Bài này làm đúng như vậy và ghi lại năm chiếc thước đã học.

Với mỗi fold $j$ từ $0$ đến $4$ trong cột `fold`, học một `Pipeline` gồm `StandardScaler()` rồi `KNeighborsClassifier(n_neighbors=1)` trên các hàng không thuộc fold $j$, với hai feature `x0`, `x1`. Dự đoán các hàng của fold $j$, ghi về đúng vị trí. Ghi lại `mean_` và `scale_` của scaler trong pipeline vừa học.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` với các cột `x0`, `x1`, `label`, `fold`.

## Kết quả

Một đối tượng JSON gồm `predictions` (dự đoán out-of-fold theo thứ tự hàng), `fold_means` và `fold_scales` (năm cặp số, theo fold $0$ đến $4$).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
