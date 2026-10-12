# Cây bốn góc

Mặt phẳng chia làm bốn góc, mỗi góc một nhãn, nhãn $0$ hoặc $1$. Một cây quyết định chỉ cần hai tầng chia là tách được bốn góc ấy.

Hãy học `DecisionTreeClassifier(max_depth=2, random_state=42)` trên `train.csv`, rồi dự đoán cho `test.csv`. Sau khi học, in cây bằng `sklearn.tree.export_text` và đọc xem cây chọn những ngưỡng nào.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `x0`, `x1`, `label`) và `test.csv` (cột `x0`, `x1`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy trên test từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
