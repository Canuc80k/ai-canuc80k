# Python, dữ liệu và toán

Chương mở đầu bằng một công việc kiểm được từ đầu đến cuối: đọc bảng, biến đổi dữ liệu, nhìn vài kết quả và ghi lại một file đúng định dạng. Tư duy thuật toán từ lập trình thi đấu vẫn là nền tảng; khi chuyển sang AI, cần thêm thói quen theo dõi kiểu dữ liệu, ý nghĩa từng trục và các phép ghép bảng. Một thuật toán đúng vẫn có thể trả kết quả sai nếu dự đoán của học sinh này bị đặt vào ID của học sinh khác.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 0.1 | Python | Viết hàm, hiểu tên và đối tượng, đọc lỗi, ghi file và chạy notebook lại từ đầu. |
| 0.2 | NumPy | Tính trên mảng; dự đoán shape, dùng axis và broadcasting, kiểm vùng nhớ và bộ nhớ trung gian. |
| 0.3 | pandas, Matplotlib | Đọc CSV, xử lý thiếu, gộp và ghép theo khóa, vẽ theo câu hỏi, kiểm file dự đoán đã ghi. |
| 0.4 | Hàm số, mũ và log | Đổi điểm số của model thành xác suất bằng sigmoid, softmax; hiểu vì sao loss có log. |
| 0.5 | Vector và ma trận | Tích vô hướng, khoảng cách, cosine; nhân ma trận và đoán shape của `X @ w`. |
| 0.6 | Đạo hàm và gradient | Độ dốc, quy tắc chuỗi, gradient descent và kiểm gradient bằng sai phân. |
| 0.7 | Xác suất và thống kê | Xác suất có điều kiện, Bayes, phương sai, phân phối chuẩn, sai số chuẩn của accuracy. |

Ba bài đầu là công cụ. Tình huống bảng điểm nối chúng với nhau: bài Python cho thấy một list dùng chung và một ô notebook chưa chạy lại có thể làm kết quả lệch; bài NumPy tính trên bảng nhỏ đủ để đối chiếu từng ô bằng tay; bài pandas mở rộng thành dữ liệu giả lập với ô trống, bảng lớp riêng và thứ tự ID bị đảo, rồi tạo được 100 dự đoán hữu hạn trong đúng khung CSV.

Bốn bài sau là phần toán mà mọi chương về sau đều dùng, viết cho người mới học hết THCS: lũy thừa, phân số và đọc đồ thị là đủ để bắt đầu. Mỗi công thức đi kèm một phép tính tay và một đoạn NumPy in ra số để đối chiếu. Ai đã học log, đạo hàm hay xác suất ở trường vẫn nên làm câu hỏi trong bài, vì cách dùng trong học máy khác cách dùng trong sách giáo khoa: log để cộng thay vì nhân, đạo hàm để biết đổi tham số theo hướng nào, xác suất để biết một con số đo được dao động bao nhiêu.

Mỗi bài có code chạy nối tiếp, hình minh họa, câu hỏi xen kẽ và mười câu cuối bài. Trước mỗi đoạn code, hãy đoán một giá trị hoặc một shape; chạy xong, đọc đúng dòng output để đối chiếu. Dữ liệu trong cả chương đều tự sinh với seed cố định, nên mọi con số đều kiểm lại được; riêng các phép đo tốc độ nên chạy lại trên máy của mình.

Thói quen của chương là biết **shape**, **dtype**, **ý nghĩa trục hoặc khóa** trước khi tính; kiểm một ví dụ nhỏ bằng tay trước khi tin một công thức; và đọc lại tệp thật sau khi ghi. Sau Chương 0, ta có đủ công cụ và đủ toán để đi từ file đề đến file nộp. Chương 1 hỏi tiếp câu quan trọng hơn: đoán điều gì, chia dữ liệu thế nào và chấm mô hình bằng đại lượng nào để kết quả có ý nghĩa.
