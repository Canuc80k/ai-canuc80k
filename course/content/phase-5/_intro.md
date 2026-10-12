# Thị giác máy tính

Một camera ở thư viện chụp được giá sách. Từ cùng một ảnh có thể hỏi bốn câu khác nhau: ảnh thuộc khu nào, có bao nhiêu quyển sách, điểm ảnh nào thuộc sách, và ảnh nào trong kho hợp với câu “giá sách cạnh cửa sổ”. Đầu vào giống nhau, nhưng nhãn, đầu ra và cách chấm khác nhau. Chương này bắt đầu từ phép toán trên một ô vuông nhỏ, rồi nối dần tới những hệ thống trả lời được cả bốn câu ấy.

::: goal Mục tiêu của chương
- Tính shape, số tham số và receptive field của mạng convolution; đọc vì sao residual giúp mạng sâu học được.
- Chọn augmentation giữ nhãn và cách dùng lại model pretrained cho ảnh mới.
- Phân biệt classification, detection, segmentation và tìm kiếm ảnh–chữ theo hợp đồng đầu ra và metric.
- Kiểm model đang dựa vào nội dung hay vào đường tắt bằng thí nghiệm có đối chứng.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 5.1 — Convolution và pooling | Một kernel nhỏ nhìn ảnh ra sao, và thấy được bao xa? |
| 5.2 — CNN và ResNet | Vì sao mạng sâu có đường tắt học được còn mạng thẳng thì không? |
| 5.3 — Augmentation và transfer learning | Biến đổi nào giữ nhãn, và lợi ích của nó đo ở đâu? |
| 5.4 — Vision Transformer | Ảnh thành chuỗi patch thì mất gì, được gì? |
| 5.5 — Object detection | Đếm và định vị nhiều vật trong một ảnh thế nào? |
| 5.6 — Image segmentation | Gán nhãn cho từng điểm ảnh và chấm nó ra sao? |
| 5.7 — Self-supervised và CLIP | Học biểu diễn khi có ít nhãn, và ghép ảnh với chữ thế nào? |
| 5.8 — GAN và diffusion | Sinh ảnh mới từ nhiễu bằng cách nào? |
| 5.9 — Phân tích hành vi model | Model đang nhìn nội dung hay nhìn một dấu vết tình cờ? |

Chương dùng lại tensor, training loop, cross-entropy và model pretrained của chương 3 và 4. Code trong bài chạy trên CPU bằng ảnh nhỏ tự tạo hoặc chữ số của scikit-learn, không cần tải dữ liệu; các thí nghiệm nhỏ ấy làm lộ đúng cơ chế đang học, như phần dư của residual hay bất biến khi dời ảnh. Recipe của chương đưa cùng các bước sang checkpoint và ảnh thật khi có asset cục bộ. Câu cuối bài ưu tiên đề thật từ NOAI, USA-NA-AIO và đề luyện của CMU, MIT, có ghi nguồn dưới mỗi câu.

Xuyên suốt chương là một quy trình: đọc hợp đồng đầu ra, dựng baseline, đo validation, đọc lỗi, thử một thay đổi có lý do, rồi kiểm lại bài nộp. Một mạng mạnh chỉ có ích khi cả đường ấy đúng. Buổi kiểm tra thị giác máy tính khép chương bằng một bài đi trọn quy trình này.
