# Âm thanh và đa phương thức

Ba giây ghi âm ở 16 kHz là 48 000 số, trong khi câu nói trong đó chỉ là vài token. Chương này học cách biến dãy số dài ấy thành thứ model đọc được, rồi giải ba loại bài: phân loại âm thanh, chép lời nói, và kết hợp nhiều nguồn như ảnh, chữ, âm thanh.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 7.1 | Dữ liệu âm thanh | Đọc waveform, sample rate; biến âm thanh thành spectrogram, log-mel. |
| 7.2 | Audio classification | Phân loại một đoạn âm thanh; chia dữ liệu theo người nói. |
| 7.3 | Speech recognition | Chép lời nói thành chữ (CTC, Whisper); chấm bằng WER. |
| 7.4 | Multimodal | Ghép ảnh, chữ, âm thanh; xử lý khi thiếu một nguồn. |

Chương dùng lại CNN của chương 5, attention của chương 3 và 6. Code trong bài chạy trên CPU với tín hiệu tự sinh, nên mỗi con số đều kiểm được bằng tay. Phần [script của chương](recipes/README.md) làm các bước ấy với bản ghi và model thật (HuBERT, wav2vec2, Whisper).
