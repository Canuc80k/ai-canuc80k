# Nền tảng học máy

Chương này học cách làm một bài học máy từ đầu đến cuối và cách biết model tốt đến đâu: chia dữ liệu, chọn thước đo, chọn model mà không tự đánh lừa mình. Chưa có model phức tạp; chương 2 mới học các model.

| Bài | Nội dung | Dùng để |
|---|---|---|
| 1.1 | Bài toán học máy | Xác định mẫu, đặc trưng, nhãn; dựng baseline; chia train, validation, test. |
| 1.2 | Generalization | Phân biệt học thuộc với học được quy luật; đọc learning curve. |
| 1.3 | Data split và cross-validation | Chia dữ liệu theo nhóm, theo thời gian; chấm bằng cross-validation. |
| 1.4 | Pipeline và data leakage | Xử lý dữ liệu đúng chỗ để điểm validation không bị đẹp giả. |
| 1.5 | Classification metrics | Precision, recall, F1, ROC-AUC; chọn ngưỡng. |
| 1.6 | Regression và ranking metrics | MAE, RMSE, $R^2$, MAP@k; metric khác loss thế nào. |
| 1.7 | Hyperparameter tuning | Grid search, random search; chấm test một lần sau khi chọn xong. |

Ví dụ xuyên chương là một câu lạc bộ: đoán số người đến mỗi buổi sinh hoạt, báo trước buổi cần thêm người hỗ trợ, gợi ý bài luyện cho từng thành viên. Dữ liệu đều tự sinh với seed cố định, nên chạy trên máy nào cũng ra cùng số, và vì biết quy luật thật nên thấy được model học đúng đến đâu.

Chương này dùng Python, NumPy, pandas và phần toán của chương 0.
