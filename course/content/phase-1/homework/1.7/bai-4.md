# Soi test

Hai đội cùng có một bảng dữ liệu và cùng thử $p$ cấu hình. Mỗi cấu hình là một mô hình chỉ nhìn một feature $j$. Cuối cùng đội nào cũng báo một con số accuracy.

- **Đội A** học trên $70\%$ hàng đầu, rồi thử lần lượt từng cấu hình và chấm trên $30\%$ còn lại. Đội báo accuracy cao nhất trong các lần thử.
- **Đội B** học trên $60\%$ hàng đầu, chọn cấu hình bằng $20\%$ kế tiếp làm validation, rồi mở $20\%$ cuối làm test đúng một lần. Đội báo accuracy trên test ấy.

Ta có thêm một tập hoàn toàn mới, `fresh_X` và `fresh_y`, chưa đội nào nhìn thấy. Đem mô hình mỗi đội đã chọn chấm trên tập này để biết con số nào nói thật.

Mô hình cho feature $j$ là **tâm gần nhất**. Trên phần train, tính trung bình feature $j$ của các hàng nhãn $0$ và của các hàng nhãn $1$. Một hàng được đoán nhãn $1$ khi giá trị feature $j$ của nó gần tâm lớp $1$ hơn hẳn, còn lại đoán $0$. Khi chọn cấu hình, hòa thì lấy $j$ nhỏ nhất.

Các phần chia lấy theo đúng thứ tự hàng: với $n$ hàng, đội A học trên $\lfloor 7n/10\rfloor$ hàng đầu, còn đội B học trên $\lfloor 6n/10\rfloor$ hàng đầu và lấy validation đến hàng thứ $\lfloor 8n/10\rfloor$.

## Dữ liệu vào

Một đối tượng JSON gồm `X`, `y` (bảng dữ liệu) và `fresh_X`, `fresh_y` (tập mới, $400$ hàng).

## Kết quả

Một đối tượng JSON gồm `a_feature`, `a_reported`, `a_fresh`, `b_feature`, `b_reported`, `b_fresh`. Hai trường `_fresh` là accuracy trên tập mới.

## Giới hạn

- $n\le100$, có không quá $50$ feature, mỗi giá trị là số nguyên từ $0$ đến $100$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 303](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=116).
:::
