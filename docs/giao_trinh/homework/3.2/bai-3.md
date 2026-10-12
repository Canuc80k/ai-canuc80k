# Học XOR

Hai công tắc, đèn sáng khi đúng một công tắc bật: đó là XOR, bài toán mà một đường thẳng không tách được. Dữ liệu ở đây là bốn đám điểm có nhiễu quanh bốn góc, nhãn $1$ khi hai tọa độ trái dấu.

Hãy học mạng `Linear(2, 8)`, `ReLU`, `Linear(8, 2)` với `float64`, `torch.manual_seed(42)` trước khi tạo mạng, `Adam(lr=0.03)`, `CrossEntropyLoss` trên logits, $300$ bước, mỗi bước dùng toàn bộ train và xóa gradient trước khi backward. Sau đó dự đoán nhãn cho `test.csv`.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x0`, `x1`, `label`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy trên test từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
