# Chọn ngưỡng

Ngưỡng của chiếc còi cũng là một lựa chọn, nên ta chọn nó trên validation rồi giữ nguyên khi dùng cho những hộp mới.

Với mỗi ngưỡng trong `candidates`, còi kêu khi `score` lớn hơn hoặc bằng ngưỡng. Tính F1 của lớp $1$ trên `valid.csv`, mẫu số bằng $0$ thì F1 bằng $0$. Chọn ngưỡng có F1 cao nhất, hòa thì lấy ngưỡng nhỏ nhất. Rồi dùng đúng ngưỡng ấy để gắn nhãn cho `test.csv`.

## Dữ liệu vào

Mỗi thư mục test có `valid.csv` (cột `y_true`, `score`), `test.csv` (chỉ có `score`) và `input.json` có `candidates` tăng dần.

## Kết quả

Một đối tượng JSON gồm `threshold`, `valid_f1` (F1 trên validation ở ngưỡng ấy) và `predictions` (nhãn cho từng hàng của test).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
