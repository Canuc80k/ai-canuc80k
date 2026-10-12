# Learning curve

Thêm dữ liệu có giúp mô hình không? Learning curve trả lời câu hỏi này. Ta học lại mô hình với số mẫu train tăng dần, mỗi lần đo lỗi trên cả phần train vừa học lẫn validation.

Với mỗi `size` trong danh sách `sizes`, lấy `size` hàng đầu tiên của `train.csv`, học một mô hình mới `KNeighborsRegressor(n_neighbors=k)` trên chừng ấy hàng, rồi tính MAE trên chính các hàng ấy và trên toàn bộ `valid.csv`. Giá trị `k` và `sizes` cho trong `input.json`.

Trục ngang của learning curve là số mẫu train, không phải số vòng học. Vẽ hai đường bằng `render.py` trong bộ kit rồi tự hỏi xem thêm dữ liệu nữa có đáng không.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` ($96$ hàng) và `valid.csv` ($80$ hàng) với hai cột `x`, `label`, và `input.json` gồm `k`, `sizes`.

## Kết quả

Một đối tượng JSON gồm `sizes` (chép lại), `train_mae` và `valid_mae`, mỗi trường một số cho mỗi `size`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
