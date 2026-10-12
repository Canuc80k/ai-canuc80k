# Thêm tương tác

Nhãn trong bài này phụ thuộc vào tích $x_0x_1$. Mô hình tuyến tính chỉ nhìn $x_0$ và $x_1$ riêng lẻ thì không bắt được điều ấy. Hãy đo xem thêm đặc trưng tương tác giúp được bao nhiêu.

So hai mô hình `make_pipeline(StandardScaler(), Ridge(alpha=0.1))`:

- Mô hình thô dùng hai cột $x_0$, $x_1$.
- Mô hình tương tác dùng thêm cột $x_0x_1$.

Đánh giá cả hai bằng MAE trên đúng ba fold cho sẵn trong cột `fold` (dùng `PredefinedSplit`). Mức cải thiện là MAE trung bình của mô hình thô trừ MAE trung bình của mô hình tương tác.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` với các cột `x0`, `x1`, `label`, `fold`.

## Kết quả

Một đối tượng JSON gồm `raw_mae`, `interaction_mae` (mỗi trường ba số, theo fold $0,1,2$) và `mean_improvement`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
