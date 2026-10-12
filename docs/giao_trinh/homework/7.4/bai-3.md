# Cầu nối tuyến tính

Hai bộ mã hóa cho hai modality sinh ra vector ở hai không gian khác nhau (ở đây $3$ chiều và $4$ chiều). Muốn tìm kiếm chéo, cần một cầu nối. Bài này học một ánh xạ tuyến tính từ các cặp đã ghép sẵn, rồi dùng nó để tìm cặp cho các mẫu mới.

1. Tìm ma trận $W$ ($3\times4$) cực tiểu $\lVert XW-Y\rVert^2$ trên các cặp train (`train_source` là $X$, `train_target` là $Y$), không có bias. Chỉ dùng dữ liệu train.
2. Chiếu các truy vấn: $P=QW$ với $Q$ là `query_source`.
3. Chuẩn hóa từng hàng của $P$ và của `candidates` về độ dài $1$ (chia cho $\max(\lVert v\rVert,10^{-12})$).
4. Với mỗi truy vấn, chọn ứng viên có cosine lớn nhất (bằng nhau thì chỉ số nhỏ hơn).

## Dữ liệu vào

Mỗi tệp `input.json` gồm `train_source` ($n\times3$), `train_target` ($n\times4$), `query_source` ($8\times3$) và `candidates` ($8\times4$, đã xáo thứ tự).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`: chỉ số ứng viên ($0..7$) cho mỗi truy vấn.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi tỉ lệ ghép đúng từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
