# Xử lý ngôn ngữ

Model chỉ học được trên số, còn câu là chuỗi ký tự. Bài nào trong chương cũng bắt đầu bằng cùng một việc: tách câu thành token rồi biến thành vector, sao cho thông tin cần cho nhiệm vụ còn lại.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 6.1 | Tokenization và text classification | Tách câu thành token; phân loại văn bản bằng đếm từ, TF-IDF. |
| 6.2 | Sentence embedding | Biến cả câu thành một vector; tìm câu cùng ý. |
| 6.3 | BERT | Hiểu từng token theo ngữ cảnh hai phía; phân loại câu và gán nhãn từng từ. |
| 6.4 | Language model | Đoán token tiếp theo; sinh văn bản. |
| 6.5 | Encoder–decoder | Đọc một chuỗi rồi viết một chuỗi khác: dịch, tóm tắt. |
| 6.6 | Large language model | Dùng LLM qua prompt; kiểm đầu ra đúng định dạng và đúng nội dung. |

Chương dùng lại embedding, mask, attention của chương 3 và model pretrained của chương 4. Code trong bài chạy trên CPU với model nhỏ học ngay trong bài; phần [script của chương](recipes/README.md) làm các bước ấy với model thật (MiniLM, DistilBERT, FLAN-T5, Qwen).
