# Bảng nhầm lẫn

Chiếc còi săn quái vật cho mỗi lần quét một điểm `score` từ $0$ đến $1$, và kêu khi `score` lớn hơn hoặc bằng ngưỡng `threshold` trong `input.json`. Nhãn `y_true` bằng $1$ nếu thật sự có quái vật. Hãy lập bảng nhầm lẫn rồi tính accuracy, precision, recall và F1 của lớp $1$.

Bảng nhầm lẫn viết như scikit-learn với `labels=[0, 1]`, hàng là nhãn thật, cột là nhãn đoán:

$$
\begin{pmatrix}\text{TN} & \text{FP}\\ \text{FN} & \text{TP}\end{pmatrix}
$$

Khi một mẫu số bằng $0$, chẳng hạn còi không kêu lần nào nên không tính được precision, ta lấy giá trị $0$, giống `zero_division=0`.

## Dữ liệu vào

Mỗi thư mục test có `detections.csv` với hai cột `y_true`, `score`, và `input.json` có `threshold`.

## Kết quả

Một đối tượng JSON gồm `cm`, `accuracy`, `precision`, `recall`, `f1`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
