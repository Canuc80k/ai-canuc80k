# Linear probe

Model nhỏ chỉ được học trên các chữ số $0$ tới $5$. Biểu diễn mà encoder của nó tạo ra có giúp phân biệt hai chữ số **chưa từng thấy**, $6$ và $9$, không? Linear probe trả lời câu hỏi ấy: giữ nguyên encoder, chỉ học một bộ phân loại tuyến tính trên đầu ra của nó.

1. Với mỗi hàng của `train.csv` và `test.csv`, tính $h=\operatorname{ReLU}(W_e\,x/16+b_e)$ bằng encoder trong `assets/pretrained.pt`, không học lại encoder.
2. Học `LogisticRegression(C=1, max_iter=1000)` trên các $h$ của train với nhãn $0$ (chữ số $6$) hoặc $1$ (chữ số $9$).
3. Dự đoán cho test.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `p0` tới `p63` và `label`) và `test.csv` (cột `p0` tới `p63`). Model nằm ở `assets/` trong bộ kit.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.8$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
