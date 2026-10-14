# Mạng neural: từ mảng số tới một chương trình học được

Ở chương 2, đặc trưng do người tạo, còn model học cách cân chúng. Mạng neural học luôn cả đặc trưng, qua nhiều lớp nối tiếp nhau. Chương này đi từ một tensor vài số tới một khối Transformer, mỗi bước đều có ví dụ đủ nhỏ để tính tay rồi kiểm bằng code.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 3.1 | Tensor và autograd | Làm việc với mảng nhiều chiều trong PyTorch; để máy tự tính đạo hàm. |
| 3.2 | MLP và backpropagation | Hiểu mạng nhiều lớp và cách lỗi ở đầu ra chỉnh được lớp đầu tiên. |
| 3.3 | Activation và loss | Chọn hàm kích hoạt và hàm mất mát đúng với đầu ra. |
| 3.4 | Training loop | Viết vòng huấn luyện có validation, lưu và nạp lại model. |
| 3.5 | Optimizer | SGD, momentum, Adam; đổi learning rate theo thời gian. |
| 3.6 | Regularization | Chống học thuộc: dropout, weight decay, dừng sớm; BatchNorm. |
| 3.7 | Huấn luyện trên GPU | Tính bộ nhớ, xử lý hết bộ nhớ, mixed precision, ước lượng thời gian chạy. |
| 3.8 | Embedding và dữ liệu chuỗi | Biến chữ thành vector; xử lý câu dài ngắn khác nhau; RNN. |
| 3.9 | Attention và Transformer | Mỗi từ lấy thông tin từ các từ khác; nền của các model ngôn ngữ. |
| 3.10 | Autoencoder | Nén dữ liệu rồi dựng lại; dùng lỗi tái tạo để tìm điểm bất thường. |

Những gì chương 1–2 đã dựng vẫn giữ nguyên: chia dữ liệu đúng, có baseline, so mọi cấu hình trên cùng validation. Khi mạng không học, có ba phép kiểm dùng xuyên suốt chương: so gradient với sai phân, cho mạng học thuộc một batch nhỏ, và so với baseline.

Code trong mỗi bài chạy được trên CPU với dữ liệu tự sinh. Bài 3.7 có thêm phần đo trên GPU thật.
