# Thị giác máy tính

Từ một ảnh chụp giá sách có thể hỏi nhiều câu khác nhau: ảnh thuộc khu nào, có bao nhiêu quyển sách và nằm ở đâu, điểm ảnh nào thuộc sách, ảnh nào khớp với câu “giá sách cạnh cửa sổ”. Đầu vào giống nhau, nhưng đầu ra và cách chấm khác nhau. Chương này đi từ phép toán trên một ô vuông nhỏ tới các model trả lời được những câu ấy.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 5.1 | Convolution và pooling | Phép toán cơ bản của mạng xử lý ảnh; tính shape và số tham số. |
| 5.2 | CNN và ResNet | Xếp nhiều lớp convolution; kết nối tắt giúp mạng rất sâu học được. |
| 5.3 | Augmentation và transfer learning | Tăng dữ liệu bằng biến đổi giữ nhãn; dùng lại model đã học cho ảnh mới. |
| 5.4 | Vision Transformer | Cắt ảnh thành các mảnh rồi dùng Transformer như với chữ. |
| 5.5 | Object detection | Tìm và khoanh hộp từng vật trong ảnh. |
| 5.6 | Image segmentation | Gán nhãn cho từng điểm ảnh. |
| 5.7 | Self-supervised và CLIP | Học từ ảnh chưa có nhãn; tìm ảnh bằng câu chữ. |
| 5.8 | GAN và diffusion | Sinh ảnh mới từ nhiễu. |
| 5.9 | Phân tích hành vi model | Kiểm model đang nhìn đúng nội dung hay một dấu vết tình cờ. |

Chương dùng lại training loop của chương 3 và model pretrained của chương 4. Code trong bài chạy trên CPU với ảnh nhỏ tự tạo hoặc bộ chữ số của scikit-learn, không cần tải dữ liệu. Phần [script của chương](recipes/README.md) làm các bước ấy với model và ảnh thật.
