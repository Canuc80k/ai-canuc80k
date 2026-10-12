# Nested CV

Điểm CV tốt nhất của grid search thường lạc quan, vì cấu hình thắng được chọn chính nhờ điểm ấy. Muốn chấm cả việc chọn cấu hình, ta dùng nested CV. Vòng ngoài giữ một phần dữ liệu ra khỏi mọi quyết định, còn vòng trong lo chọn cấu hình.

Tệp `rows.csv` có cột `outer_fold` từ $0$ đến $2$ và `inner_fold` là $0$ hoặc $1$. Với mỗi fold ngoài $j$:

1. Phần train ngoài là các hàng không thuộc fold $j$.
2. Trên phần ấy, chạy `GridSearchCV` như bài B, với $k=1, 3, 5$, F1, và fold trong lấy từ cột `inner_fold`.
3. Cấu hình thắng được fit lại trên toàn bộ phần train ngoài, rồi dự đoán các hàng của fold $j$.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` với các cột `x0`, `x1`, `label`, `outer_fold`, `inner_fold`.

## Kết quả

Một đối tượng JSON gồm:

- `selected_k`: $k$ được chọn ở mỗi fold ngoài, theo thứ tự fold $0, 1, 2$.
- `outer_f1`: F1 trên mỗi fold ngoài, và `mean_outer_f1` là trung bình của chúng.
- `predictions`: dự đoán cho mọi hàng, theo thứ tự của `rows.csv`.
- `fit_count`: tổng số lần fit.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
