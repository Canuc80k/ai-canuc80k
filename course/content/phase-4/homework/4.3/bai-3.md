# Mở encoder

Lần này mở cả encoder để học tiếp trên nhiệm vụ mới: phân biệt chữ số $6$ và $9$, hai lớp encoder chưa từng thấy.

1. Encoder lấy từ `assets/pretrained.pt` ($h=\operatorname{ReLU}(W_e\,x/16+b_e)$), head mới `Linear(32, 2)` có trọng số và bias bằng $0$, tất cả kiểu `float64`.
2. `Adam` với hai nhóm tham số: encoder learning rate $0.001$, head learning rate $0.02$, không weight decay.
3. Học $200$ bước, mỗi bước dùng toàn bộ train, loss `CrossEntropyLoss` trung bình.
4. Dự đoán nhãn cho test.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `p0` tới `p63` và `label`) và `test.csv` (cột `p0` tới `p63`). Model nằm ở `assets/` trong bộ kit.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.85$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
