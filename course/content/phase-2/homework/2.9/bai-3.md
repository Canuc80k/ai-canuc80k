# Chữ số nén

Mỗi ảnh chữ số viết tay là $8\times8=64$ điểm ảnh, độ sáng từ $0$ đến $16$. Ta thử nén mỗi ảnh còn $16$ số bằng PCA rồi dựng lại, xem chữ còn đọc được không.

Hãy học `PCA(n_components=16, svd_solver="full")` trên `train.csv`, rồi nén và dựng lại các ảnh của `test.csv`. Không cần cắt giá trị về khoảng $0$ đến $16$.

Bộ kit có `render.py` vẽ sáu ảnh trước và sau khi nén. Giữ $95\%$ phương sai có nghĩa là ảnh còn rõ $95\%$ không?

## Dữ liệu vào

Mỗi thư mục test có `train.csv` và `test.csv`, mỗi hàng một ảnh, cột `p0` đến `p63`.

## Kết quả

Một đối tượng JSON gồm `reconstructed` (các ảnh test sau khi dựng lại, mỗi ảnh $64$ số) và `variance_ratio` ($16$ số).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
