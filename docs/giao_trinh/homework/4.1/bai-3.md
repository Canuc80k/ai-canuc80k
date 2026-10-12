# Ảnh chữ số

Lần này đầu vào là ảnh PNG thật: các chữ số viết tay $8\times8$ của bộ dữ liệu UCI, ảnh xám với độ sáng từ $0$ đến $240$. Dùng lại model của bài B.

Model đã học trên điểm ảnh từ $0$ tới $16$ chia cho $16$, tức thang $[0,1]$. Ảnh PNG ở đây có thang $0$ tới $240$, nên phải chia cho $240$ để đưa về đúng thang ấy, **không** chia cho `feature_divisor`. Đọc từng ảnh theo thứ tự trong `image_names`, trải thành $64$ số theo từng hàng, chia cho $240$, chạy model và lấy lớp có logit lớn nhất.

## Dữ liệu vào

Mỗi thư mục test có `images/` và `input.json` chứa `image_names`. Model nằm ở `assets/` trong bộ kit.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự của `image_names`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.85$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
