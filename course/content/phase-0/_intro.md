# Python, dữ liệu và toán

Chương này chuẩn bị hai thứ dùng trong cả khóa học: công cụ lập trình (Python, NumPy, pandas) và phần toán nền (hàm mũ và log, vector và ma trận, đạo hàm, xác suất).

| Bài | Nội dung | Dùng để |
|---|---|---|
| 0.1 | Python | Viết hàm, hiểu tên và đối tượng, đọc lỗi, ghi file và chạy notebook lại từ đầu. |
| 0.2 | NumPy | Tính trên mảng; dự đoán shape, dùng axis và broadcasting, kiểm vùng nhớ và bộ nhớ trung gian. |
| 0.3 | pandas, Matplotlib | Đọc CSV, xử lý thiếu, gộp và ghép theo khóa, vẽ theo câu hỏi, kiểm file dự đoán đã ghi. |
| 0.4 | Hàm số, mũ và log | Đổi điểm số của model thành xác suất bằng sigmoid, softmax; hiểu vì sao loss có log. |
| 0.5 | Vector và ma trận | Tích vô hướng, khoảng cách, cosine; nhân ma trận và đoán shape của `X @ w`. |
| 0.6 | Đạo hàm và gradient | Độ dốc, quy tắc chuỗi, gradient descent và kiểm gradient bằng sai phân. |
| 0.7 | Xác suất và thống kê | Xác suất có điều kiện, Bayes, phương sai, phân phối chuẩn, sai số chuẩn của accuracy. |

Phần toán chỉ cần kiến thức THCS: lũy thừa, phân số và đọc đồ thị. Ai đã học log, đạo hàm hay xác suất ở trường vẫn nên đọc, vì học máy dùng chúng theo cách khác sách giáo khoa: log để đổi phép nhân thành phép cộng, đạo hàm để biết nên chỉnh tham số theo hướng nào, xác suất để biết một con số đo được dao động bao nhiêu.

Mỗi công thức có một phép tính tay và một đoạn code in ra số để đối chiếu. Dữ liệu trong chương đều tự sinh với seed cố định, nên chạy lại sẽ ra đúng các số trong bài; riêng số đo tốc độ thì tùy máy.
