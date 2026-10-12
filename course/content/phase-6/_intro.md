# Xử lý ngôn ngữ

Một câu là chuỗi ký tự, còn model chỉ học được trên số. Mọi bài trong chương đều bắt đầu bằng cùng một việc: biến câu thành token rồi thành vector, sao cho thông tin cần cho nhiệm vụ còn lại. Từ đó, chương đi qua sáu nhiệm vụ nối nhau: phân loại, tìm câu cùng ý, đọc token trong ngữ cảnh, đoán token tiếp theo, đọc nguồn rồi viết đích, và điều khiển một LLM theo hợp đồng đầu ra.

::: goal Mục tiêu của chương
- Chọn baseline hợp với classification, retrieval hay generation, và đặt nó cạnh mọi model lớn hơn.
- Kiểm tokenizer, shape, attention mask, loss mask và nhãn subword trước khi train.
- Phân biệt điểm train, validation độc lập, loss khi teacher forcing và chất lượng khi tự sinh.
- Tạo đầu ra đúng schema, đối chiếu nội dung với nguồn và dự toán ngân sách inference.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 6.1 — Tokenization và text classification | Thông tin nào còn lại khi câu thành vector đếm từ? |
| 6.2 — Sentence embedding | Gần nhau trong không gian vector có đúng là cùng ý? |
| 6.3 — BERT | Mỗi token được nhìn những token nào, và nhãn nằm ở vị trí nào? |
| 6.4 — Language model | Đoán từng token tiếp theo dẫn tới cả một chuỗi ra sao? |
| 6.5 — Encoder–decoder | Đọc nguồn rồi viết đích khi chưa có đáp án thế nào? |
| 6.6 — Large language model | Output có qua được schema, nội dung đúng và ngân sách không? |

Chương dùng lại embedding, mask, attention và training loop của chương 3, cùng model pretrained của chương 4. Điều mới là vị trí trong chuỗi: cùng một tensor shape `(B, L)` có thể ẩn PAD ở cuối, token đặc biệt ở đầu, hay nhãn bị dịch một bước, và mỗi chỗ cần một mask riêng. Không gian vector gom được những câu khác chữ cùng ý, nhưng không tự hiểu phủ định hay đúng sự thật; các thí nghiệm trong bài cho thấy rõ những chỗ ấy.

Code trong bài chạy offline trên CPU với model nhỏ học ngay trong bài; recipe của chương đưa cùng quy trình sang checkpoint công bố (MiniLM, DistilBERT, FLAN-T5, Qwen) khi có asset cục bộ. Thói quen giữ suốt chương: bắt đầu bằng ví dụ nhỏ có đáp án tính tay, chạy notebook theo thứ tự, đọc câu sai trước khi tăng model. Câu cuối bài ưu tiên đề thật từ NOAI, USA-NA-AIO và đề luyện của CMU, MIT, có ghi nguồn dưới mỗi câu.
