# Lật chữ số

Lật ngang là augmentation hay dùng nhất cho ảnh, vì một con mèo lật ngang vẫn là con mèo. Nhưng với chữ số thì sao? Bài này kiểm trên chữ số viết tay thật của bộ dữ liệu UCI.

Mỗi ảnh là $8\times8$ điểm, trải thành $64$ cột `p0` tới `p63` theo từng hàng.

1. Tính tâm của mỗi lớp trên train: trung bình các ảnh của lớp ấy.
2. Phân loại một ảnh bằng tâm gần nhất theo khoảng cách Euclid (hòa thì lớp nhỏ hơn).
3. Phân loại các ảnh test như thường, rồi phân loại bản lật ngang của chúng: cột $c$ của mỗi hàng chuyển sang cột $7-c$. Nhãn đúng vẫn là nhãn gốc.

Hãy báo accuracy trên test trước và sau khi lật, và với mỗi lớp có trong test, tỉ lệ ảnh của lớp ấy đổi dự đoán sau khi lật. Thêm lớp có tỉ lệ đổi cao nhất (hòa thì lớp nhỏ hơn).

## Dữ liệu vào

Mỗi thư mục test có `train.csv` và `test.csv` (cột `p0` tới `p63` và `label`).

## Kết quả

Một đối tượng JSON gồm `accuracy`, `flipped_accuracy`, `change_rate` (từ nhãn, viết dạng chuỗi, tới tỉ lệ) và `most_changed_class`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
