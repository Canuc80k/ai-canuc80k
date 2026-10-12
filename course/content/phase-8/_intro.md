# Luyện thi: biến hiểu biết thành một bài làm kiểm chứng được

Đến đây ta đã có công cụ cho dữ liệu bảng, ảnh, văn bản và âm thanh. Trong phòng thi, phần khó thường không nằm ở chỗ biết một model, mà ở những quyết định nối tiếp nhau: còn 40 phút thì làm việc gì, điểm validation cao có đáng tin không, gộp thêm một model có thật sự giúp, và bản nào được nộp. Chương này biến các quyết định ấy thành những bước có lý do và có bằng chứng.

::: goal Mục tiêu của chương
- Đọc hợp đồng của bài, có baseline nộp được trước khi cải thiện, và chia thời gian theo ích lợi kỳ vọng cùng rủi ro.
- Kiểm dữ liệu trước khi huấn luyện, gồm mẫu trùng, nhóm, rò rỉ và lệch phân phối, để validation đo đúng câu hỏi lúc sử dụng.
- Giải bài mở bằng cách ghép biểu diễn của model với thuật toán tìm kiếm, kèm baseline, ablation và báo cáo trung thực.
- Gộp model khi sai số thật sự bù cho nhau; chọn trọng số trên một tập và đánh giá trên tập khác.
- Chạy bài làm từ môi trường trống, kiểm file nộp, và chữa buổi thi thử bằng nhật ký.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 8.1 — Chiến lược thi | Khoảng thời gian tiếp theo nên dành cho việc nào, và bằng chứng nào khiến ta đổi kế hoạch? |
| 8.2 — Phân tích dữ liệu trước huấn luyện | Validation đang chứa ví dụ mới, hay chỉ chứa bản khác của dữ liệu model đã thấy? |
| 8.3 — Bài toán mở | Model cho biểu diễn; thuật toán dùng biểu diễn ấy để tìm lời giải thế nào? |
| 8.4 — Ensemble | Khi nào gộp nhiều model tốt hơn chọn model tốt nhất? |
| 8.5 — Thi thử | Bài làm có chạy lại được từ môi trường trống không, và lỗi hôm nay dẫn tới việc luyện nào? |

Ba bài đầu đi theo cùng một buổi luyện ba việc mở đầu ở 8.1: bài văn bản có validation đẹp bất thường được mổ xẻ ở 8.2, còn việc tìm vật bí mật bằng phản hồi thành bài mở của 8.3. Bài 8.4 gộp model, và 8.5 đưa cả bài làm, kể cả bản ensemble, qua một lần chạy từ đầu. Dữ liệu trong bài nhỏ, tự sinh và chạy offline trên CPU, nên mọi con số đều kiểm được bằng tay; câu cuối bài ưu tiên đề thật của NOAI và USA-NA-AIO, có ghi nguồn.

Quy định thi luôn gắn với năm, vòng và statement của từng bài. Thời gian, GPU, Internet, pretrained và dạng nộp của IOAI 2025 hay USA-NA-AIO 2026 không tự thành quy định của kỳ thi sau. Vì vậy chương không dạy một bộ luật cố định, mà dạy đọc đúng hợp đồng của đề, giữ validation độc lập, tái tạo được kết quả và dùng đúng tài nguyên được phép.

Học xong chương, mỗi học sinh nên tự viết được một danh sách kiểm cho buổi thi của mình: mốc đóng thí nghiệm, các phép kiểm file nộp và mẫu nhật ký, rút ra từ chính những buổi thi thử.
