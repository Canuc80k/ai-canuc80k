# Chẩn đoán

Bộ dữ liệu breast cancer có $569$ khối u, mỗi khối u $30$ số đo lấy từ ảnh tế bào như bán kính, chu vi, diện tích. Nhãn `target` là $0$ nếu khối u ác tính, $1$ nếu lành tính. Hãy đoán nhãn cho các khối u trong test.

Luật giống đề thi gốc. Mô hình học có giám sát duy nhất được dùng là kNN, nhưng tiền xử lý thì tùy ý.

Gợi ý: các số đo có thang rất khác nhau. Diện tích lên tới hàng nghìn, còn độ nhẵn chỉ khoảng $0.1$. kNN dựa vào khoảng cách, nên cột lớn sẽ lấn át cột nhỏ. Hãy so kNN có và không có `StandardScaler` trong một `Pipeline`, bằng cross-validation trên train.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` ($398$ hàng, $30$ cột số đo và cột `target`) và `test.csv` ($171$ hàng, chưa có `target`). Mỗi test chia bộ dữ liệu theo một cách khác.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, mỗi hàng của `test.csv` một số $0$ hoặc $1$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy trên test từ $0.92$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, Bài 9](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=22).
:::
