# IOAI

## Tổng quan

IOAI (International Olympiad in Artificial Intelligence, Olympic Trí tuệ nhân tạo quốc tế) là kỳ thi AI quốc tế cho học sinh phổ thông, tổ chức lần đầu năm 2024. Mỗi nước gửi một đội tối đa 4 thí sinh, chọn qua kỳ thi quốc gia. Thí sinh phải dưới 20 tuổi tính đến ngày 01/07 của năm thi và đang học phổ thông.

Khác với olympiad Tin học, đề IOAI không có đáp án đúng tuyệt đối. Mỗi bài cho dữ liệu thật, một baseline và một metric; thí sinh viết notebook để model cho điểm càng cao càng tốt trong thời gian và tài nguyên giới hạn.

Đừng nhầm IOAI với [IAIO](#/contests/iaio): đó là một kỳ thi quốc tế khác, có vòng lý thuyết viết.

## Thể thức

Theo thể lệ IOAI 2026:

- **Vòng ở nhà**: 3 bài phát khoảng một tháng trước kỳ thi, làm trên Kaggle. Vòng này để học, **không tính** vào kết quả. Mỗi bài thi chính thức liên quan tới ít nhất một bài ở nhà về chủ đề hay phương pháp.
- **Hai ngày thi cá nhân**, mỗi ngày 6 giờ, mỗi ngày 3 bài mới. Huy chương chỉ xét hai ngày này.
- **Team Challenge**: thi đồng đội, đề đổi mỗi năm (2025 là lập trình robot hình người). Có cúp cho ba đội đầu, không có huy chương cá nhân.
- **GAITE**: bản dành cho các đội mới tham gia, cùng đề nhưng có gợi ý và bảng điểm riêng.

Môi trường thi năm 2026:

- JupyterLab trên web, mỗi thí sinh một phần GPU (khoảng 18 GB bộ nhớ), Python 3.13.
- Có sẵn PyTorch, transformers, peft, scikit-learn, XGBoost, LightGBM, CatBoost; **không có TensorFlow**, không cài thêm gói.
- Internet chỉ mở tới trang tài liệu (python.org, pytorch.org, scikit-learn.org, tài liệu Hugging Face…). Không tải model từ ngoài; chỉ dùng model ban tổ chức để sẵn.
- Có một LLM tích hợp (Gemma 3, tối đa 1000 token mỗi lượt) để hỏi; cấm LLM và copilot bên ngoài.
- Mỗi lần chạy notebook tối đa 20 phút nếu đề không ghi khác; mỗi bài tối đa 60 lượt nộp.

Năm 2025 thi trên nền tảng Bohrium, LLM tích hợp là GPT-4o-mini. Môi trường đổi theo năm, nên đọc thể lệ của đúng năm thi.

## Chấm điểm

Mỗi bài có ba tập: train có nhãn, validation và test. Trong lúc thi, bảng điểm A chấm trên validation, cho thấy điểm của mình và điểm cao nhất (ẩn danh). Bảng điểm B chấm trên test sau khi thi, dùng để xếp hạng chính thức.

Điểm thô được chuẩn hóa về thang 0–100:

$$\text{điểm} = \frac{\text{điểm nộp} - \text{baseline}}{\text{Max} - \text{baseline}} \cdot 100,$$

với Max là số lớn hơn giữa 90% điểm lời giải của Ban khoa học và điểm thô cao nhất của thí sinh. Nộp kém hơn baseline thì không có điểm. Huy chương chia theo tỉ lệ: vàng cho khoảng 1/12 thí sinh, vàng và bạc cộng lại khoảng 1/4, cả ba loại khoảng 1/2.

Hai hệ quả khi đi thi: chọn bài nộp theo validation nhưng nhớ rằng test mới quyết định (bài [1.3](#/lesson/1.3) và [8.1](#/lesson/8.1)); và vượt baseline sớm ở mọi bài đáng giá hơn dồn hết thời gian vào một bài.

## Các kỳ đã tổ chức

| Kỳ | Nơi | Thời gian | Đề và lời giải |
|---|---|---|---|
| 2024 | Burgas, Bulgaria | tháng 8/2024 | [Trang đề 2024](https://ioai-official.org/2024-tasks/): 3 bài ở nhà và 3 bài tại chỗ (ML, NLP, CV), 2 bài sinh ảnh, sinh video |
| 2025 | Bắc Kinh, Trung Quốc | tháng 8/2025 | [GitHub IOAI-2025](https://github.com/IOAI-official/IOAI-2025), giấy phép CC-BY-4.0, có notebook lời giải |
| 2026 | Astana, Kazakhstan | 2–8/08/2026 | [GitHub IOAI-2026](https://github.com/IOAI-official/IOAI-2026), CC-BY-4.0, có baseline và bộ chấm |
| 2027 | Singapore | 4–10/07/2027 | Chưa có |

**Đề 2025.** Ở nhà: Chameleon, Radar, Weather. Thi cá nhân: Radar, Chicken Counting, Concepts, Restroom Icon Matching, Antique Painting Authentication, Pixel Efficiency. GAITE thêm Synthetic Speech Detector và Word Segmentation.

**Đề 2026.** Ở nhà: Operation Night Watch, Robot Delivery Academy, The Analytical Language of John Wilkins. Ngày 1: Find the Order, Robot Chasing, Potato. Ngày 2: Double Agent Dilemma, Ghost of the Machine, IOAI Field. Mỗi bài chạy trên một GPU khoảng 16 GB, không có Internet.

## Luyện ở khóa học

- **Thực hành** có bản dựng lại nhiều bài IOAI thật, chấm trên LQDOJ: Tranh cổ (Antique Painting, mức [Medium](#/practice/m)); Biển nhà vệ sinh, Tách từ ghép tiếng Đức, Giọng thật hay giọng máy (mức [High](#/practice/h)); Radar, Bóng ma trong cỗ máy (mức [Extra](#/practice/e)); Rượt đuổi robot, Sắp lại cuộc trò chuyện (mức [Max](#/practice/x)).
- **Kiến thức**: ML trên bảng ở chương 1–2, PyTorch ở chương 3, model pretrained và fine-tune ở chương 4, ảnh, chữ, âm thanh ở chương 5–7.
- **Chiến lược phòng thi**: chương 8, đặc biệt [8.1](#/lesson/8.1) (chiến lược thi), [8.2](#/lesson/8.2) (phân tích dữ liệu trước khi huấn luyện) và [8.5](#/lesson/8.5) (thi thử).
- Mỗi bài học có nút **Chạy trên Kaggle** ở những bài đã có notebook chạy thật, gần với môi trường thi.

## Nguồn

- [Trang chủ IOAI](https://ioai-official.org/), [IOAI 2027 Singapore](https://ioai-official.org/singapore-2027/)
- [Thể lệ và phụ lục kỹ thuật IOAI 2026 (PDF)](https://ioai-official.org/wp-content/uploads/2026/06/IOAI2026-Contest-Rules-and-Tehnical-Appendix.pdf)
- [Thể lệ IOAI 2025 (PDF)](https://ioai-official.org/wp-content/uploads/2025/08/Contest-Rules-for-IOAI-2025-version-2.3-1.pdf), [Quy chế IOAI (PDF)](https://ioai-official.org/wp-content/uploads/2025/08/IOAI-regulations.pdf)
- [Giáo trình IOAI 2026](https://ioai-official.org/republic-of-kazakhstan/syllabus-2026/)
- [IOAI-2024](https://github.com/IOAI-official/IOAI-2024), [IOAI-2025](https://github.com/IOAI-official/IOAI-2025), [IOAI-2026](https://github.com/IOAI-official/IOAI-2026) trên GitHub
