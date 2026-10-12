# Nhiều đặc trưng

Một bộ dữ liệu y tế có vài chục bệnh nhân, mỗi người đo cả trăm chỉ số. Mô hình tuyến tính học trên đó đạt accuracy train gần tuyệt đối, còn validation thì kém hẳn. Bài này tái hiện tình huống ấy để xem số đặc trưng và mức điều chuẩn ảnh hưởng thế nào.

Nhãn $y$ là $0$ hoặc $1$. Đặt $t=2y-1$ để nhãn thành $-1$ hoặc $1$. Với $p$ cột đầu của `X_train`, ghép thành ma trận $A$, học vector trọng số bằng ridge, không có hệ số chặn:

$$
w=(A^\top A+\alpha I)^{-1}A^\top t .
$$

Một hàng $x$ (lấy $p$ cột đầu) được đoán nhãn $1$ nếu $x\cdot w>0$, ngược lại đoán $0$.

Hãy làm với mọi cặp $\alpha$ trong `alphas` và $p$ trong `feature_counts`: tính accuracy trên train và trên validation. Cuối cùng, chọn cặp có accuracy validation cao nhất. Hòa thì chọn $p$ nhỏ hơn, còn hòa nữa thì chọn $\alpha$ lớn hơn.

Làm xong, hãy nhìn hàng ứng với $\alpha$ nhỏ nhất: accuracy train và validation thay đổi ra sao khi $p$ vượt số mẫu train?

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X_train`, `y_train`, `X_val`, `y_val`, `feature_counts` (tăng dần) và `alphas`.

## Kết quả

Một đối tượng JSON gồm:

- `train_accuracy`, `val_accuracy`: mỗi trường là ma trận, hàng theo thứ tự `alphas`, cột theo thứ tự `feature_counts`.
- `best`: `{"alpha": ..., "features": ...}`.

## Giới hạn

- Train có từ $20$ đến $40$ hàng, validation có $60$ hàng, không quá $100$ cột. Không điểm số $x\cdot w$ nào sát $0$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 269](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=96).
:::
