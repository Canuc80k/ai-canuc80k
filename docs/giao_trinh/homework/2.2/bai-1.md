# Ridge

Hai cánh tay máy cùng nâng một vật. Hai feature `x0`, `x1` gần như đi đôi với nhau, nên hồi quy tuyến tính thường cho hai trọng số rất lớn và ngược dấu. Ridge phạt tổng bình phương trọng số, buộc hai tay chia lực hợp lý hơn.

Chuẩn hóa feature bằng `StandardScaler` học trên train, rồi học `Ridge(alpha=..., solver="cholesky")` với `alpha` cho trong `input.json`. Ridge của scikit-learn cực tiểu

$$
\sum_i\left(y_i-\hat y_i\right)^2+\alpha\sum_j w_j^2,
$$

và không phạt hệ số tự do. Cuối cùng dự đoán cho `test.csv`.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x0`, `x1`, `label`), `test.csv` (cột `x0`, `x1`) và `input.json` có `alpha`.

## Kết quả

Một đối tượng JSON gồm `weights` (hai trọng số trên feature đã chuẩn hóa), `bias` và `predictions`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
