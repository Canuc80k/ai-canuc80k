# Học máy cổ điển

Trước khi có mạng neural, người ta đã giải rất nhiều bài toán thật bằng những mô hình gọn gàng: một đường thẳng, một cây câu hỏi, vài trăm cây cộng lại. Đến giờ chúng vẫn là thứ chạy nhanh nhất, dễ hiểu nhất, và với dữ liệu dạng bảng thì thường vẫn thắng.

::: goal Mục tiêu của chương
- Cài và đọc các mô hình kinh điển: hồi quy tuyến tính, regularization, logistic và softmax, kNN, cây, rừng, boosting, SVM, PCA và phân cụm.
- Chẩn đoán bias hay variance, rồi chọn đúng núm điều chỉnh của từng họ mô hình.
- Tính tay một ví dụ nhỏ cho mỗi mô hình trước khi gọi thư viện, và đối chiếu hai kết quả.
- Tạo đặc trưng đúng thời điểm, kiểm từng nhóm đặc trưng trên cùng fold.
:::

Chương này đi qua bốn họ mô hình:

| Họ | Bài | Ý tưởng một câu |
|---|---|---|
| Tuyến tính | 2.1–2.3, 2.8 | Cộng các đặc trưng với trọng số rồi quyết định. |
| Dựa trên láng giềng | 2.4 | Giống ai thì đoán như người đó. |
| Dựa trên cây | 2.5–2.7 | Hỏi liên tiếp các câu có/không, rồi gộp nhiều cây. |
| Không giám sát | 2.9–2.10 | Không có nhãn: tìm hướng quan trọng hoặc tìm nhóm. |

Bài 2.11 nói về thứ quyết định kết quả nhiều hơn cả việc chọn mô hình: đặc trưng (features), và thời điểm mỗi đặc trưng thật sự có sẵn. Buổi kiểm tra khóa 1 khép chương bằng một bài dữ liệu bảng đi trọn từ đọc đề, chọn split, baseline đến file nộp.

Xuyên suốt chương là một câu hỏi: mô hình sai vì quá đơn giản (**bias** cao) hay vì quá nhạy với dữ liệu huấn luyện (**variance** cao)? Regularization, chọn $k$ trong kNN, độ sâu của cây, số cây trong rừng, $C$ trong SVM đều là những cái núm để vặn sự cân bằng đó. Hiểu điều này rồi thì gặp mô hình mới cũng biết nên chỉnh gì trước.

Chương này dùng lại quy trình của chương 1: chia dữ liệu có lý do, baseline trước, so mô hình trên cùng fold, đưa tiền xử lý vào Pipeline. Mỗi mô hình được tính tay trên một ví dụ nhỏ trước khi gọi thư viện, để con số in ra từ máy luôn có thứ để đối chiếu. Câu cuối bài ưu tiên đề thật từ NOAI, USA-NA-AIO và đề luyện của các khóa học máy đại học, có ghi nguồn dưới mỗi câu.
