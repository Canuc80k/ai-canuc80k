# CNN nghe chuông

Mỗi clip dài nửa giây có một tiếng chuông, ở nửa đầu (nhãn $0$) hoặc nửa sau (nhãn $1$). Hãy học một CNN nhỏ trên log-mel để phân biệt hai loại.

1. **Đặc trưng.** Mỗi tệp WAV một kênh, $1024$ Hz, $512$ mẫu (chia $32768$). Cắt thành $16$ khung liền nhau dài $32$, nhân cửa sổ Hann tuần hoàn, công suất $|\text{rFFT}|^2/(\sum w)^2$. Tám bộ lọc mel HTK tam giác trên $0..512$ Hz (đỉnh $1$, không chuẩn hóa diện tích), rồi $10\log_{10}(\max(\cdot,10^{-8}))$. Được ma trận $8\times16$ (dải mel $\times$ khung).
2. **Chuẩn hóa** từng dải mel bằng trung bình và độ lệch chuẩn tính trên **train** (gộp mọi clip và mọi khung); độ lệch chuẩn tối thiểu $10^{-6}$.
3. **Mạng** `float64`: `Conv2d(1, 4, 3, padding=1)`, `ReLU`, `Flatten`, `Linear(512, 2)`. Gọi `torch.manual_seed(seed)` trước khi tạo mạng.
4. `Adam(lr=0.01)`, $60$ bước trên toàn bộ train, loss `CrossEntropyLoss`. Chuyển sang `eval` rồi dự đoán test.

Train và test đến từ các phiên ghi khác nhau.

## Dữ liệu vào

Mỗi thư mục test có `input.json` (gồm `seed`), `train.csv` (cột `id`, `path`, `label`, `session`), `test.csv` (cột `id`, `path`, `session`) và các tệp WAV.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của `test.csv`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
