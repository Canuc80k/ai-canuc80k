# Độ rung

Năm robot học cùng một quy luật, nhưng mỗi robot có bộ train riêng. Hỏi cả năm tại cùng một điểm $x$ thì các câu trả lời lệch nhau bao nhiêu? Độ lệch ấy cho biết mô hình nhạy với dữ liệu train đến đâu.

Với mỗi $i$ từ $0$ đến $4$, học `KNeighborsRegressor(n_neighbors=k)` trên `train_i.csv` và dự đoán cho mọi điểm của `queries.csv`. Tại mỗi điểm có năm dự đoán. Hãy tính trung bình và phương sai của năm số ấy, phương sai chia cho $5$ như `np.var(..., ddof=0)`.

So các test có $k=1$ với các test có $k=7$ bằng `render.py`. Dải quanh đường trung bình rộng hơn ở đâu?

## Dữ liệu vào

Mỗi thư mục test có năm tệp `train_0.csv` đến `train_4.csv` với hai cột `x`, `label`, tệp `queries.csv` gồm $41$ điểm, và `input.json` có `k`.

## Kết quả

Một đối tượng JSON gồm `mean` và `variance`, mỗi trường $41$ số theo thứ tự của `queries.csv`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
