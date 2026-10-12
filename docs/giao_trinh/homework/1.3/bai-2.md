# Chia nhóm

Có $20$ robot, mỗi robot ghi số đo trong $3$ ngày. Ta muốn biết mô hình đoán tốt đến đâu cho một **robot mới**. Vậy mọi bản ghi của cùng một robot phải nằm trong cùng một phần. Nếu ngày 1 của robot A ở train còn ngày 2 ở test, mô hình đã quen robot A trước khi được chấm.

Hãy xếp $12$ robot vào train, $4$ vào valid, $4$ vào test. Có nhiều cách chia đúng, cách nào cũng được.

Cách gọn nhất là lấy danh sách các robot, xáo trộn rồi tự chia. Dùng `GroupShuffleSplit` cũng được, nhưng lần gọi thứ hai chạy trên phần còn lại, nên phải đổi chỉ số trả về thành chỉ số gốc.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` gồm $60$ hàng với các cột `row_id`, `group` (tên robot), `day`, `reading`.

## Kết quả

Một đối tượng JSON `{"assignment": [...]}` gồm $60$ chuỗi `"train"`, `"valid"` hoặc `"test"`, theo thứ tự hàng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Hệ thống đếm số robot mỗi phần và kiểm không robot nào bị tách đôi.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
