# AUC

Hai robot A và B cùng đưa ra xác suất có quái vật cho mỗi lần quét, ở cột `p_a` và `p_b`. Xác suất của B là bình phương xác suất của A. Thứ tự các mẫu vẫn y như cũ, chỉ có mức tự tin thay đổi.

Với mỗi robot, hãy tính hai thước đo.

**ROC-AUC.** Xét mọi cặp gồm một mẫu dương và một mẫu âm. Cặp được $1$ điểm nếu mẫu dương có xác suất cao hơn, $0.5$ nếu bằng nhau, $0$ nếu thấp hơn. AUC là trung bình điểm các cặp. Dữ liệu chỉ có một lớp thì không có cặp nào, AUC là `null`.

**Log loss.** Trung bình của $-\left[y\ln p+(1-y)\ln(1-p)\right]$ trên mọi mẫu. Trước khi tính, kẹp $p$ vào đoạn $[\varepsilon, 1-\varepsilon]$ với $\varepsilon=2^{-52}$ để tránh $\ln 0$.

Tính xong, so hai robot. Thước đo nào đổi, thước đo nào giữ nguyên, và vì sao?

## Dữ liệu vào

Mỗi thư mục test có `scores.csv` với các cột `y_true`, `p_a`, `p_b`.

## Kết quả

Một đối tượng JSON gồm hai trường `A` và `B`, mỗi trường là `{"auc": ..., "log_loss": ...}`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
