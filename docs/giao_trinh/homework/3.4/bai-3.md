# Checkpoint

Một vòng huấn luyện trọn vẹn: học, chọn checkpoint theo validation, lưu, rồi nạp lại ở một tiến trình mới để dự đoán, như khi notebook đã đóng.

1. Chuẩn hóa hai cột `x0`, `x1` bằng trung bình và độ lệch chuẩn của train (mẫu số $n$; cột nào độ lệch chuẩn bằng $0$ thì chia cho $1$). Valid và test dùng đúng các con số ấy.
2. Mô hình `Linear(2, 1)` kiểu `float64`, trọng số và bias khởi tạo bằng $0$. `SGD` với `learning_rate` cho trong `input.json`, loss MSE.
3. Học $25$ epoch, mỗi epoch đi qua `DataLoader(batch_size=4, shuffle=False)`. Cuối mỗi epoch, ở chế độ `eval` và trong `no_grad`, tính MSE trên valid.
4. Giữ bản sao trạng thái của epoch có MSE valid nhỏ nhất (hòa thì lấy epoch sớm hơn).
5. Lưu trạng thái ấy cùng các con số chuẩn hóa, nạp lại bằng `torch.load(..., weights_only=True)` ở một tiến trình Python mới, rồi dự đoán test.

## Dữ liệu vào

Mỗi thư mục test có `train.csv`, `valid.csv` (cột `x0`, `x1`, `label`), `test.csv` (cột `x0`, `x1`) và `input.json` chứa `learning_rate`.

## Kết quả

Một đối tượng JSON gồm `best_epoch` (đánh từ $1$), `validation_mse` ($25$ số), `predictions` (theo thứ tự hàng của test) và `optimizer_steps`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
