# Bộ nhận tông

Một bản nộp trọn vẹn cho bài phân loại âm thanh: học CNN trên log-mel, chọn checkpoint theo validation, lưu cùng bộ tiền xử lý, rồi nạp lại ở một tiến trình Python mới để dự đoán. Mỗi clip là một âm trầm (khoảng $96$ Hz, nhãn $0$) hoặc một âm cao (khoảng $320$ Hz, nhãn $1$).

1. **Đặc trưng** như bài C buổi 7.2: WAV một kênh, $1024$ Hz, $512$ mẫu (chia $32768$); $16$ khung dài $32$, cửa sổ Hann tuần hoàn, công suất $|\text{rFFT}|^2/(\sum w)^2$; $8$ bộ lọc mel HTK trên $0..512$ Hz; $10\log_{10}(\max(\cdot,10^{-8}))$.
2. **Chuẩn hóa** từng dải mel bằng trung bình và độ lệch chuẩn của **train** (tối thiểu $10^{-6}$).
3. **Nhãn bên trong mô hình** là $1-\text{nhãn}$ (lớp $0$ của mạng là âm cao). Khi dự đoán, đổi lại bằng bảng $[1, 0]$.
4. **Mạng** `float64`: `Conv2d(1, 4, 3, padding=1)`, `ReLU`, `Flatten`, `Linear(512, 2)`; `torch.manual_seed(seed)` trước khi tạo mạng; `Adam(lr=0.01)`, $60$ bước trên toàn bộ train.
5. Sau mỗi bước, ở chế độ `eval`, tính loss trên valid; giữ **bản sao** trạng thái có loss valid nhỏ nhất (hòa thì bước sớm hơn).
6. Lưu trạng thái ấy cùng trung bình, độ lệch chuẩn, bảng nhãn và cấu hình tiền xử lý. Ở một tiến trình Python mới, nạp bằng `torch.load(..., weights_only=True)`, đọc lại các tệp WAV của test và dự đoán.

## Dữ liệu vào

Mỗi thư mục test có `input.json` (gồm `seed`), `train.csv`, `valid.csv` (cột `id`, `path`, `label`, `session`), `test.csv` (cột `id`, `path`, `session`) và các tệp WAV.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`: nhãn ($0$ hoặc $1$) theo thứ tự hàng của `test.csv`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
