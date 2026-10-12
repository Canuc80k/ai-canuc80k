# Hai vòng tròn

Hai lớp nằm trên hai vòng tròn lồng nhau, lớp $0$ ở vòng trong, lớp $1$ ở vòng ngoài. Không đường thẳng nào tách được hai vòng, nhưng SVM với kernel RBF thì làm được.

Hãy học `make_pipeline(StandardScaler(), SVC(C=10, gamma=1, kernel="rbf"))` trên `train.csv`, rồi dự đoán cho `test.csv`. Thử thêm `kernel="linear"` để thấy nó thất bại ra sao.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x0`, `x1`, `label`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy trên test từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
