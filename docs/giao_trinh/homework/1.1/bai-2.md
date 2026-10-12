# Iris

Bộ dữ liệu Iris ghi bốn số đo của mỗi bông hoa, tính bằng cm, gồm chiều dài và chiều rộng của đài hoa và của cánh hoa. Mỗi bông thuộc một trong ba loài, mã hóa thành $0$ (setosa), $1$ (versicolor) và $2$ (virginica). Mã $0, 1, 2$ chỉ là tên lớp, nên đây là bài classification.

Hãy học từ `train.csv`, kiểm trên `valid.csv`, rồi đoán loài của các hoa trong `test.csv`. Chưa cần hiểu thuật toán bên trong. `KNeighborsClassifier(n_neighbors=5)` của scikit-learn dùng như một hộp đen là đủ, chỉ cần `fit` và `predict`. Thước đo là accuracy, tức tỉ lệ hoa đoán đúng loài.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` và `valid.csv` gồm `id`, bốn feature `f0` đến `f3` và `label`, cùng `test.csv` chưa có `label`. Mỗi test chia $150$ bông hoa theo một cách khác.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, mỗi hàng của `test.csv` một số $0$, $1$ hoặc $2$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy trên test từ $0.8$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
