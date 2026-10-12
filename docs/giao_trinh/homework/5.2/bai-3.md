# CNN chữ số

Tự học một CNN nhỏ để phân biệt chữ số viết tay $0$ và $1$ trên ảnh $8\times8$.

1. Mỗi hàng gồm $64$ điểm ảnh từ $0$ tới $16$; chia cho $16$ một lần rồi xếp thành tensor `(N, 1, 8, 8)`.
2. Mạng kiểu `float64`: `Conv2d(1, 4, 3, padding=1)`, `ReLU`, `MaxPool2d(2)`, `Conv2d(4, 8, 3, padding=1)`, `ReLU`, `Flatten`, `Linear(128, 2)`. Gọi `torch.manual_seed(52)` trước khi tạo mạng.
3. `Adam(lr=0.01)`, $100$ bước, mỗi bước dùng toàn bộ train, loss `CrossEntropyLoss`.
4. Chuyển sang `eval` và dự đoán test.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `p0` tới `p63` và `label`) và `test.csv` (cột `p0` tới `p63`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
