# Mạng neural: từ mảng số tới một chương trình học được

Ở chương Học máy cổ điển, feature do người chọn, còn model học cách cân chúng. Mạng neural học luôn cả feature qua nhiều lớp nối tiếp, và gradient phải đi ngược qua toàn bộ chuỗi phép tính ấy. Những gì chương 1–2 đã dựng vẫn giữ nguyên: split đúng mục tiêu, baseline trước, so mọi cấu hình trên cùng validation. Chương này đi từ một tensor vài số tới một encoder block, với ví dụ đủ nhỏ để tính tay rồi kiểm bằng code.

::: goal Mục tiêu của chương
- Theo dõi shape, dtype, device và đường đi của gradient từ dữ liệu tới loss.
- Viết training loop có validation, checkpoint và suy luận lại từ tệp đã lưu.
- Chẩn đoán vì sao mạng không học: khởi tạo, activation, loss, optimizer, regularization hay bộ nhớ.
- Xử lý chuỗi có PAD và mask, hiểu RNN và attention, dùng lỗi tái tạo đúng mục đích.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 3.1 — Tensor và autograd | Mỗi chiều là gì, và gradient đi đâu? |
| 3.2 — MLP và backpropagation | Lỗi ở đầu ra chỉnh lớp đầu tiên thế nào? |
| 3.3 — Activation và loss | Đầu ra mang ý nghĩa gì, và vì sao tín hiệu tắt dần qua nhiều lớp? |
| 3.4 — Training loop | Đóng notebook rồi, model còn suy luận đúng không? |
| 3.5 — Optimizer | Gradient biến thành bước cập nhật ra sao, và learning rate đổi theo thời gian thế nào? |
| 3.6 — Regularization | Model học cấu trúc hay học thuộc nhiễu? |
| 3.7 — Huấn luyện trên GPU | Đúng, hữu hạn, vừa bộ nhớ và kịp giờ chưa? |
| 3.8 — Embedding và dữ liệu chuỗi | Thêm PAD có làm đổi câu không, và RNN đọc chuỗi ra sao? |
| 3.9 — Attention và Transformer | Mỗi token lấy thông tin từ đâu? |
| 3.10 — Autoencoder | Nén giữ lại gì, và lỗi tái tạo báo điều gì? |

Nhiều ý quen từ lập trình thi đấu có mặt ở đây dưới tên khác. Mảng nhiều chiều thành tensor; thứ tự topo trên DAG thành forward và backward. Lời giải brute force để đối chiếu thành sai phân để kiểm gradient. Giới hạn thời gian và bộ nhớ thành batch size, activation và VRAM. Prefix sum với đếm phần tử hợp lệ thành masked pooling, và xét mọi cặp token là một thuật toán $O(L^2)$. Điều CP không có là khoảng cách giữa train và dữ liệu mới: loss train thấp chưa nói gì về validation.

Xuyên suốt chương là một câu hỏi khi mạng không học: lỗi nằm ở dữ liệu, ở cài đặt hay ở cấu hình? Ba phép kiểm lặp lại nhiều lần: sai phân đối chiếu backward, học thuộc một batch nhỏ trước khi train thật, và so với baseline trên cùng validation. Mạng lớn hơn là một giả thuyết cần kiểm, không phải bước nâng cấp mặc định.

Code trong mỗi bài chạy nối tiếp như notebook, offline trên CPU với dữ liệu tự sinh. Đọc tình huống và đoán output trước khi chạy; khi đoán sai, thay một số nhỏ rồi kiểm lại, như đổi key thứ hai trong attention hay thêm một PAD vào masked pooling. Bài 3.7 kèm recipe đo trên GPU thật để lấy số của chính máy được cấp. Câu cuối bài ưu tiên đề thật từ NOAI, USA-NA-AIO và đề luyện của CMU, MIT, có ghi nguồn dưới mỗi câu.

Sau chương, có thể tự dựng một baseline neural nhỏ, debug một batch, chọn checkpoint bằng validation và suy luận lại từ tệp. Chương 4 dùng model pretrained trên nền ấy: nạp được một model lớn chưa có nghĩa là đã dùng đúng tiền xử lý, mask hay ngân sách.
