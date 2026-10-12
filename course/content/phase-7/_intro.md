# Âm thanh và đa phương thức

Một bản ghi âm ba giây ở 16 kHz là 48 000 số; câu nói trong đó chỉ là vài token. Chương này đi từ chênh lệch ấy tới ba bài toán: phân loại âm thanh, chép lời nói, và kết hợp nhiều nguồn như ảnh, chữ, âm thanh. Điều mới so với các chương trước là phải giữ đúng **thời gian, sample rate và quan hệ giữa các mẫu** từ lúc đọc file tới lúc chấm.

::: goal Mục tiêu của chương
- Đọc waveform đúng sample rate, tính spectrogram và log-mel, tránh aliasing khi đổi tần số lấy mẫu.
- Phân loại âm thanh với validation chia theo người nói hoặc phiên ghi, và gộp dự đoán nhiều cửa sổ.
- Hiểu CTC và encoder–decoder ASR, tính WER bằng dynamic programming theo đúng scorer.
- Kết hợp nhiều modality, đo đóng góp của từng nguồn bằng ablation và xử lý khi một nguồn bị thiếu.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 7.1 — Dữ liệu âm thanh | Một dãy số trở thành biểu diễn thời gian–tần số thế nào, và mất gì khi lấy mẫu thưa? |
| 7.2 — Audio classification | Model nghe cả đoạn hay chỉ một khoảnh khắc, và chia dữ liệu theo đơn vị nào? |
| 7.3 — Speech recognition | Học từ âm và chữ khác độ dài thế nào, và chấm transcript ra sao? |
| 7.4 — Multimodal | Nguồn nào thực sự giúp, và model làm gì khi thiếu một nguồn? |

Chương dùng lại CNN của chương 5, attention và sequence của chương 3 và 6. Code trong bài chạy offline trên CPU với tín hiệu tổng hợp có cấu trúc biết trước, nên mỗi phép biến đổi và mỗi con số đều kiểm được bằng tay: tần số giả sinh ra khi lấy mẫu thưa, bảng α của CTC, WER của một câu. Recipe của chương đưa cùng quy trình sang bản ghi thật với checkpoint HuBERT, wav2vec2 hay Whisper có sẵn trên máy, chấm trên validation theo người nói và ghi lại phiên bản. Câu cuối bài ưu tiên đề thật có ghi nguồn; kho đề về âm thanh còn ít nên phần lớn câu được soạn theo đúng tình huống thi.

Buổi kiểm tra khóa 3 khép chương: ôn cách làm hai bài thuộc hai lĩnh vực trong một buổi sáu giờ, từ đọc hợp đồng chấm điểm tới bài nộp hợp lệ.
