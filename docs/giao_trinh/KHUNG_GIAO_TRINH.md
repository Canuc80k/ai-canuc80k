# Khung giáo trình AI Canuc80k

- **Đối tượng:** Học sinh THCS/THPT đã biết lập trình thi đấu, chưa học AI.
- **Mục tiêu:** VOAI → IOAI; APOAI, IAIO.
- **Máy học:** GPU T4 trên Colab hoặc Kaggle.
- **Quy mô:** 63 bài, 4 khóa.

## Khóa 1 — Học máy

### Phase 0 — Python và dữ liệu

| Bài | Tên bài | Nội dung |
|---|---|---|
| 0.1 | Python | Python cho người đã quen C++. |
| 0.2 | NumPy | Tính trên cả mảng thay cho vòng lặp. |
| 0.3 | Pandas và Matplotlib | Đọc, xử lý và vẽ dữ liệu bảng. |

### Phase 1 — Nền tảng học máy

| Bài | Tên bài | Nội dung |
|---|---|---|
| 1.1 | Bài toán học máy | Đọc đề và nộp mô hình đầu tiên. |
| 1.2 | Generalization | Vì sao mô hình tốt trên train mà tệ trên test. |
| 1.3 | Data split và cross-validation | Chia dữ liệu để điểm validation đáng tin. |
| 1.4 | Pipeline và data leakage | Gói tiền xử lý và chặn rò rỉ dữ liệu. |
| 1.5 | Classification metrics | Đo mô hình phân loại cho đúng. |
| 1.6 | Regression và ranking metrics | Đo mô hình hồi quy và xếp hạng. |
| 1.7 | Hyperparameter tuning | Thử tham số có hệ thống. |

### Phase 2 — Học máy cổ điển

| Bài | Tên bài | Nội dung |
|---|---|---|
| 2.1 | Linear regression | Định giá căn hộ bằng một đường thẳng. |
| 2.2 | Regularization | Phạt hệ số lớn để mô hình bớt học thuộc. |
| 2.3 | Logistic regression và softmax | Dự đoán xác suất để phân loại. |
| 2.4 | k-Nearest Neighbors | Đoán theo những điểm gần nhất. |
| 2.5 | Decision tree | Dự đoán bằng chuỗi câu hỏi có/không. |
| 2.6 | Random forest | Gộp nhiều cây để dự đoán ổn định. |
| 2.7 | Gradient boosting | Mỗi cây mới sửa lỗi của các cây trước. |
| 2.8 | SVM | Tìm đường phân chia có lề rộng nhất. |
| 2.9 | Dimensionality reduction | Nén dữ liệu xuống ít chiều. |
| 2.10 | Clustering | Chia nhóm dữ liệu khi không có nhãn. |
| 2.11 | Feature engineering | Biến dữ liệu thô thành đặc trưng tốt. |

## Khóa 2 — Học sâu

### Phase 3 — Mạng neural

| Bài | Tên bài | Nội dung |
|---|---|---|
| 3.1 | Tensor và autograd | Làm quen PyTorch và GPU. |
| 3.2 | MLP và backpropagation | Tự xây mạng neural và lan truyền ngược. |
| 3.3 | Activation và loss | Chọn hàm kích hoạt và hàm loss cho đúng. |
| 3.4 | Training loop | Viết vòng huấn luyện hoàn chỉnh. |
| 3.5 | Optimizer | Chọn optimizer và learning rate. |
| 3.6 | Regularization cho mạng neural | Chống overfit cho mạng neural. |
| 3.7 | Huấn luyện trên GPU | Gỡ lỗi và tăng tốc trên GPU. |
| 3.8 | Embedding và dữ liệu chuỗi | Đưa câu dài ngắn khác nhau vào mạng. |
| 3.9 | Attention và Transformer | Hiểu và tự cài attention. |
| 3.10 | Autoencoder | Nén rồi tái tạo dữ liệu, tìm mẫu bất thường. |

### Phase 4 — Model pretrained

| Bài | Tên bài | Nội dung |
|---|---|---|
| 4.1 | Sử dụng model pretrained | Nạp và chạy model có sẵn. |
| 4.2 | Feature extraction | Biến ảnh, chữ, âm thanh thành vector. |
| 4.3 | Fine-tuning | Huấn luyện tiếp model có sẵn. |
| 4.4 | LoRA | Fine-tune model lớn trên GPU nhỏ. |
| 4.5 | Zero-shot | Giải bài khi không có dữ liệu huấn luyện. |

## Khóa 3 — Ảnh, chữ và âm thanh

### Phase 5 — Thị giác máy tính

| Bài | Tên bài | Nội dung |
|---|---|---|
| 5.1 | Convolution và pooling | Phép tích chập trên ảnh. |
| 5.2 | CNN và ResNet | Phân loại ảnh bằng CNN. |
| 5.3 | Augmentation và transfer learning | Tăng dữ liệu ảnh và dùng model có sẵn. |
| 5.4 | Vision Transformer | Đưa ảnh vào Transformer. |
| 5.5 | Object detection | Tìm và khoanh vùng vật thể. |
| 5.6 | Image segmentation | Gán nhãn cho từng điểm ảnh. |
| 5.7 | Self-supervised và CLIP | Tìm ảnh bằng câu chữ. |
| 5.8 | GAN và diffusion | Sinh ảnh mới. |
| 5.9 | Phân tích hành vi model | Tìm chỗ model nhìn sai. |

### Phase 6 — Xử lý ngôn ngữ

| Bài | Tên bài | Nội dung |
|---|---|---|
| 6.1 | Tokenization và text classification | Cắt câu thành token và phân loại văn bản. |
| 6.2 | Sentence embedding | Tìm câu gần nghĩa bằng vector. |
| 6.3 | BERT | Fine-tune BERT cho câu và từng từ. |
| 6.4 | Language model | Mô hình đoán từ tiếp theo. |
| 6.5 | Encoder–decoder | Đọc một chuỗi, viết ra chuỗi khác. |
| 6.6 | Large language model | Chạy và điều khiển LLM trên T4. |

### Phase 7 — Âm thanh và đa phương thức

| Bài | Tên bài | Nội dung |
|---|---|---|
| 7.1 | Dữ liệu âm thanh | Biến âm thanh thành số và ảnh phổ. |
| 7.2 | Audio classification | Phân loại âm thanh. |
| 7.3 | Speech recognition | Chuyển giọng nói thành chữ. |
| 7.4 | Multimodal | Kết hợp ảnh, chữ và âm thanh. |

## Khóa 4 — Luyện thi

### Phase 8 — Luyện thi

| Bài | Tên bài | Nội dung |
|---|---|---|
| 8.1 | Chiến lược thi | Chia thời gian và lượt nộp trong phòng thi. |
| 8.2 | Phân tích dữ liệu trước huấn luyện | Soi dữ liệu trước khi huấn luyện. |
| 8.3 | Bài toán mở | Kết hợp thuật toán với model cho bài mở. |
| 8.4 | Ensemble | Gộp nhiều model để điểm ổn định. |
| 8.5 | Thi thử | Thi thử đúng điều kiện thật. |

### Phase 9 — Mở rộng

| Bài | Tên bài | Nội dung |
|---|---|---|
| 9.1 | Reinforcement learning | Học hành động qua phần thưởng. |
| 9.2 | Tìm kiếm và suy luận | Tìm đường, chơi cờ và suy luận logic. |
| 9.3 | Bài tập lý thuyết | Bài lý thuyết cho vòng thi viết. |

