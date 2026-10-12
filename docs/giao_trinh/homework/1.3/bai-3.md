# OOF

Dự đoán out-of-fold (OOF) của một mẫu đến từ mô hình **chưa học** mẫu ấy. Bài này tạo một bộ OOF theo các fold cho sẵn trong cột `fold`.

Với mỗi fold $j$ từ $0$ đến $4$, học `KNeighborsClassifier(n_neighbors=1)` trên các hàng không thuộc fold $j$, chỉ dùng feature `x`, rồi dự đoán các hàng của fold $j$ và ghi về đúng vị trí của chúng.

Nếu học một lần trên toàn bộ rồi đoán lại, mọi hàng sẽ được đoán đúng nhãn của chính nó, kể cả vài nhãn nhiễu có sẵn trong dữ liệu. OOF cho ta cái nhìn thật hơn. `cross_val_predict` với `cv=PredefinedSplit(rows["fold"])` làm đúng việc này, tự viết vòng lặp năm fold cũng được.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` gồm $100$ hàng với các cột `row_id`, `x`, `label`, `fold`.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}` gồm $100$ nhãn $0$ hoặc $1$, theo thứ tự hàng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
