# Gradient descent

Robot học chỉnh tay lái bằng gradient descent. Mô hình có hai trọng số và một hệ số tự do, loss là MSE:

$$
J(w,b)=\frac1n\sum_{i=1}^{n}\left(X_iw+b-y_i\right)^2.
$$

Bắt đầu từ $w=(0,0)$, $b=0$, chạy đúng `steps` bước với tốc độ học `learning_rate`. Ở mỗi bước:

1. Tính sai số $r_i = X_iw+b-y_i$ và ghi lại loss **trước** khi cập nhật.
2. Tính gradient $\frac{\partial J}{\partial w}=\frac2n X^\top r$ và $\frac{\partial J}{\partial b}=\frac2n\sum_i r_i$, cả hai đều từ tham số cũ.
3. Cập nhật đồng thời $w$ và $b$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (ma trận $n\times2$), `y`, `learning_rate`, `steps`.

## Kết quả

Một đối tượng JSON gồm `loss_history` (`steps` giá trị loss), `weights` (hai trọng số sau bước cuối) và `bias`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
