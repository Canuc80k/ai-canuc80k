# Python và dữ liệu

Chương mở đầu bằng một công việc kiểm được từ đầu đến cuối: đọc bảng, biến đổi dữ liệu, nhìn vài kết quả và ghi lại một file đúng định dạng. Tư duy thuật toán từ lập trình thi đấu vẫn là nền tảng; khi chuyển sang AI, cần thêm thói quen theo dõi kiểu dữ liệu, ý nghĩa từng trục và các phép ghép bảng. Một thuật toán đúng vẫn có thể trả kết quả sai nếu dự đoán của học sinh này bị đặt vào ID của học sinh khác.

| Bài | Công cụ | Dùng để |
|---|---|---|
| 0.1 | Python | Viết hàm, hiểu tên và đối tượng, đọc lỗi, ghi file và chạy notebook lại từ đầu. |
| 0.2 | NumPy | Tính trên mảng; dự đoán shape, dùng axis và broadcasting, kiểm vùng nhớ và bộ nhớ trung gian. |
| 0.3 | pandas, Matplotlib | Đọc CSV, xử lý thiếu, gộp và ghép theo khóa, vẽ theo câu hỏi, kiểm file dự đoán đã ghi. |

Tình huống bảng điểm nối ba bài với nhau. Bài Python cho thấy một list dùng chung và một ô notebook chưa chạy lại có thể làm kết quả lệch. Bài NumPy tính trên bảng nhỏ đủ để đối chiếu từng ô bằng tay. Bài pandas mở rộng thành dữ liệu giả lập với ô trống, bảng lớp riêng và thứ tự ID bị đảo; cuối buổi, ta tạo được 100 dự đoán hữu hạn trong đúng khung CSV. Dữ liệu trong cả chương đều tự sinh, nên mọi con số đều kiểm lại được.

Mỗi bài có code chạy nối tiếp, hình minh họa, câu hỏi xen kẽ và mười câu cuối bài. Trước mỗi đoạn code, hãy đoán một giá trị hoặc một shape; chạy xong, đọc đúng dòng output để đối chiếu. Ai đã quen Python có thể làm phần kiểm tra đầu vào của 0.1 để biết mục nào cần ôn; ba chỗ vẫn nên đọc kỹ là notebook, sao chép đối tượng và ghi CSV.

Thói quen của chương là biết **shape**, **dtype**, **ý nghĩa trục hoặc khóa** trước khi tính; kiểm một ví dụ nhỏ độc lập trước khi tối ưu; và đọc lại tệp thật sau khi ghi. Mọi đoạn code chạy offline trên CPU với seed cố định; riêng các phép đo tốc độ nên chạy lại trên máy của mình, vì thời gian phụ thuộc phần cứng.

Sau Chương 0, ta có đủ công cụ để đi từ file đề đến file nộp. Chương 1 hỏi tiếp câu quan trọng hơn: đoán điều gì, chia dữ liệu thế nào và chấm mô hình bằng đại lượng nào để kết quả có ý nghĩa.
