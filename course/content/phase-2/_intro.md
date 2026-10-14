# Học máy cổ điển

Trước khi có mạng neural, người ta đã giải rất nhiều bài toán thật bằng những model gọn: một đường thẳng, một cây câu hỏi, vài trăm cây cộng lại. Đến nay chúng vẫn chạy nhanh nhất, dễ hiểu nhất, và với dữ liệu dạng bảng thì thường vẫn thắng. Chương này học các model đó.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 2.1 | Linear regression | Đoán một số bằng tổng có trọng số; tìm trọng số bằng công thức và bằng gradient descent. |
| 2.2 | Regularization | Phạt trọng số lớn để model bớt học thuộc: Ridge, Lasso. |
| 2.3 | Logistic regression, softmax | Phân loại bằng xác suất; học bằng cross-entropy. |
| 2.4 | k-Nearest Neighbors | Đoán theo các mẫu giống nhất; vì sao phải chuẩn hóa. |
| 2.5 | Cây quyết định | Chuỗi câu hỏi if–else học từ dữ liệu. |
| 2.6 | Random forest | Gộp nhiều cây khác nhau cho dự đoán ổn định hơn. |
| 2.7 | Gradient boosting | Mỗi cây mới sửa phần sai của các cây trước; thường mạnh nhất với dữ liệu bảng. |
| 2.8 | SVM | Đường phân chia có lề rộng nhất; kernel cho đường cong. |
| 2.9 | Giảm chiều | PCA; vẽ dữ liệu nhiều chiều bằng t-SNE, UMAP. |
| 2.10 | Phân cụm | Chia nhóm khi không có nhãn: K-Means, DBSCAN. |
| 2.11 | Feature engineering | Tạo đặc trưng tốt, chỉ dùng thông tin có lúc dự đoán. |

Với mỗi model, bài đều trả lời cùng một câu: model sai vì quá đơn giản (bias cao, bài 1.2) hay vì quá nhạy với dữ liệu train (variance cao)? Mỗi model có một vài tham số để chỉnh cân bằng đó: mức phạt của regularization, $k$ của kNN, độ sâu của cây, số cây, $C$ của SVM.

Chương này dùng lại cách làm của chương 1: chia dữ liệu đúng, có baseline, so các model trên cùng fold, đưa tiền xử lý vào Pipeline. Mỗi model được tính tay trên một ví dụ nhỏ trước khi gọi thư viện, để có số đối chiếu.
