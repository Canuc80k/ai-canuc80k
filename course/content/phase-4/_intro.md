# Model pretrained

Huấn luyện một model đọc ảnh hay đọc chữ từ đầu cần rất nhiều dữ liệu và thời gian. Thường ta không làm vậy, mà lấy một model người khác đã học sẵn trên dữ liệu rất lớn (model pretrained) rồi dùng lại. Chương này học các cách dùng lại ấy, từ không học thêm gì tới học thêm một phần nhỏ.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 4.1 | Sử dụng model pretrained | Nạp đúng model, tiền xử lý và bảng nhãn; tính bộ nhớ cần để chạy. |
| 4.2 | Feature extraction | Lấy embedding từ model có sẵn rồi học một bộ phân loại nhỏ phía trên. |
| 4.3 | Fine-tuning | Học tiếp một phần hay toàn bộ model trên dữ liệu của bài. |
| 4.4 | LoRA | Học thêm một phần nhỏ chèn vào model, tiết kiệm bộ nhớ hơn fine-tuning. |
| 4.5 | Zero-shot | Dự đoán khi chưa có nhãn, bằng tên lớp hoặc prompt. |

Bài 4.2–4.4 đi dần từ ít đến nhiều tham số được học: chỉ học một head, mở thêm vài lớp, rồi học một phần nhỏ chèn vào các lớp. Học càng nhiều thì càng thích nghi tốt nhưng càng tốn và càng dễ overfit. Bài 4.5 không học thêm gì.

Code trong bài chạy offline trên CPU với các model nhỏ dựng ngay trong bài, để từng bước kiểm được bằng số. Phần [script của chương](recipes/README.md) làm các bước ấy với model thật.
