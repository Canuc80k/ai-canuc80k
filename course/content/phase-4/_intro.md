# Model pretrained

Câu lạc bộ tin học có ảnh hoạt động, bài viết và tài liệu thuật toán. Muốn tìm tài liệu gần với một câu hỏi, phân loại ảnh hay nhận ra chủ đề của bài mới, huấn luyện mọi bộ đọc ảnh và chữ từ đầu thường vượt quá dữ liệu và thời gian có sẵn. Một model đã học trên dữ liệu rất lớn mang sẵn những biểu diễn dùng lại được. Câu hỏi của chương là dùng lại phần nào, và làm sao biết kiến thức ấy hợp với bài mới.

::: goal Mục tiêu của chương
- Nạp một checkpoint với đúng trọng số, cấu hình, processor, bảng nhãn và phiên bản; chạy offline.
- Trích embedding rồi dùng linear probe, kNN và tìm kiếm tương đồng làm baseline.
- Chọn giữa giữ nguyên encoder, fine-tune có chọn lọc và LoRA theo dữ liệu và ngân sách.
- Dự đoán khi chưa có nhãn bằng tên lớp, prompt hoặc xác suất chuỗi, và biết khi nào cách ấy sai.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 4.1 — Sử dụng model pretrained | Checkpoint gồm những gì, và cần bao nhiêu bộ nhớ để chạy? |
| 4.2 — Feature extraction | Biểu diễn có sẵn đã đủ tách các lớp chưa? |
| 4.3 — Fine-tuning | Mở thêm phần nào để cập nhật, với bước bao lớn? |
| 4.4 — LoRA | Học phần thay đổi hạng thấp thay vì cả ma trận thì tiết kiệm và mất gì? |
| 4.5 — Zero-shot | Không có nhãn của bài mới thì dự đoán bằng gì? |

Bốn bài đầu đi dần từ ít đến nhiều tham số được cập nhật: không cập nhật gì, chỉ học một head, mở thêm vài block, rồi học một phần hạng thấp chèn vào các lớp. Mỗi bước thêm khả năng thích nghi và thêm chi phí, rủi ro overfit. Bài 4.5 đi theo hướng khác: không học thêm gì, chỉ đặt câu hỏi cho model bằng tên lớp hoặc prompt.

Chương dùng lại tensor, backpropagation, `train()`/`eval()` và training loop của chương 3. Code trong bài chạy offline trên CPU với các model nhỏ dựng ngay trong bài, để từng cơ chế (nạp, trích embedding, cập nhật, chèn LoRA, chấm zero-shot) hiện ra rõ và kiểm được bằng số. [Recipe của chương](recipes/README.md) đưa các bước ấy sang model công bố thật: kiểm môi trường, tải đúng revision khi được phép, lưu hash, nạp lại offline rồi mới thực nghiệm. Câu cuối bài ưu tiên đề thật từ NOAI, USA-NA-AIO và đề luyện của CMU, MIT, có ghi nguồn dưới mỗi câu.

Sau chương này, mỗi lựa chọn model phải trả lời được bốn câu: nó học trước từ đâu, nhận đầu vào thế nào, phần nào được cập nhật, và chất lượng đã được đo trên validation nào.
