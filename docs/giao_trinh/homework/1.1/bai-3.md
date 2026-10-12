# Chữ số

Mỗi ảnh là một chữ số viết tay, thu nhỏ thành lưới $8\times8$ ô, mỗi ô có độ đậm từ $0$ đến $16$. Lưới được trải thành một hàng $64$ số `f0`, …, `f63`, đọc lần lượt từng hàng của lưới. Nhãn là chữ số từ $0$ đến $9$.

Hãy học từ `train.csv`, kiểm trên `valid.csv`, rồi đoán chữ số cho các ảnh trong `test.csv`. `SVC(gamma=0.001)` của scikit-learn dùng như hộp đen là đủ, thuật toán này sẽ học ở bài 2.8.

Muốn xem một ảnh, lấy $64$ số của hàng ấy, `reshape(8, 8)` rồi vẽ bằng `plt.imshow`. Thử xem vài ảnh bị đoán sai trên validation, nhiều khi chính mắt người cũng phân vân.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` và `valid.csv` gồm `id`, $64$ feature và `label`, cùng `test.csv` chưa có `label`. Mỗi test chia $1797$ ảnh theo một cách khác.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, mỗi hàng của `test.csv` một chữ số.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy trên test từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
