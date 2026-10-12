# Nền tảng học máy

Một chương trình có thể trả về đúng định dạng mà vẫn dự đoán rất sai. Chương này tập trung vào hai việc: kiểm chương trình làm đúng điều đề yêu cầu, và kiểm cách đo điểm có phản ánh tình huống sẽ gặp sau này hay không.

::: goal Mục tiêu của chương
- Đặt một bài toán thành đặc trưng, nhãn và hàm dự đoán, rồi dựng baseline trước mọi mô hình.
- Chia dữ liệu theo người, thời gian hay nhóm cho khớp với lúc sử dụng, và đưa tiền xử lý vào Pipeline để validation không bị rò rỉ.
- Chọn và tính tay metric cho phân loại, hồi quy và xếp hạng; biết mỗi con số đang thưởng và phạt điều gì.
- Thử tham số trên validation, chọn mô hình, rồi báo cáo một lần trên test độc lập.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 1.1 — Bài toán học máy | Dùng những buổi trước để đoán số người đến thế nào, và hơn cách đoán đơn giản nhất bao nhiêu? |
| 1.2 — Generalization | Vì sao nhớ đúng dữ liệu cũ chưa đủ để đoán tốt một buổi mới? |
| 1.3 — Data split và cross-validation | Chia dữ liệu thế nào để validation đo đúng tình huống gặp người mới, thời điểm mới? |
| 1.4 — Pipeline và data leakage | Tiền xử lý cả bảng trước khi chia làm điểm validation sai lệch thế nào? |
| 1.5 — Classification metrics | Khi lớp quan trọng rất hiếm, accuracy che giấu điều gì? |
| 1.6 — Regression và ranking metrics | Đoán lệch hai người khác gì với đẩy bài phù hợp xuống cuối danh sách? |
| 1.7 — Hyperparameter tuning | Thử nhiều tham số thế nào mà điểm báo cáo cuối vẫn đáng tin? |

Cả chương đi cùng một câu lạc bộ đang chuẩn bị các buổi sinh hoạt: ước lượng số người đến, phát hiện buổi cần hỗ trợ, rồi xếp bài luyện tập phù hợp. Dữ liệu trong code đều được tạo ngay trên máy với seed cố định, không cần tải bộ dữ liệu hay dùng GPU. Vì tự sinh, ta biết chính xác quy luật thật và nhìn được mô hình học đúng đến đâu.

Điểm nối với lập trình thi đấu là thói quen kiểm tra: đọc hợp đồng input/output, viết một phương án đơn giản trước, tính tay một ví dụ, rồi đối chiếu thư viện. Điểm mới là validation có nhiễu: một cải thiện nhỏ chưa chứng minh mô hình tốt hơn trong mọi tình huống.

Nền tảng cần có là Python, shape của NumPy và đọc bảng bằng pandas ở chương 0; chưa cần đạo hàm hay mạng neural, ký hiệu mới được giải thích ngay khi gặp. Học xong chương, mỗi con số validation in ra đều phải trả lời được ba câu: đo trên dữ liệu nào, chia theo đơn vị nào, và so với baseline nào.
