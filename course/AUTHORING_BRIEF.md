# Bản sao giáo trình — chuẩn bài 2.1

## Phạm vi và quyền ghi

Trang cũ đã được sao chép nguyên vẹn vào `output/` và lưu vào `archive/TRANG_CU_TRUOC_KHI_CHINH.zip`, kiểm CRC và SHA-256 từng tệp. Không ghi link trang cũ. Không sửa bất kỳ tệp nào ngoài workspace này. Không upload, submit, rejudge, gọi Auto/AI LQDOJ; không sửa bài tập về nhà. CSS, app.js, font, khung trang giữ nguyên bytes. Chỉ tích hợp nội dung mới bằng dữ liệu và tài liệu bài học.

Đọc `curriculum.json`, `content/README.md`, toàn bộ `content/phase-2/2.1.md`, `content/phase-2/slides/2.1.md` trước khi viết. Tham chiếu hình mẫu trong `content/phase-2/fig/`, generator `content/figures.py`, PDF mẫu đã copy trong `output/giao_trinh/slides/2.1.pdf`. Nguồn cũ/canonical ở workspace khác chỉ đọc; không chạy builder cũ.

## Chuẩn nội dung

Đối tượng là học sinh THCS/THPT biết thuật toán thi đấu nhưng mới học AI. Mỗi bài có tình huống gần gũi và câu hỏi xuyên suốt; nối các đoạn để người học đọc từ trên xuống. Sau mục tiêu, triển khai vì sao → hình trực giác → ký hiệu/công thức → code chạy được → đọc kết quả → quay lại tình huống. Từng phép toán/kích thước/đơn vị được giải thích khi xuất hiện; nâng cao có vị trí và cầu nối, không đổ lý thuyết khó ngay đầu.

Dùng văn trung tính rõ ràng, câu vô chủ hoặc “ta” trong lập luận; không gọi trực tiếp người đọc là “các em”, “em”, “các bạn” hay “bạn”, không xưng “thầy”, “tôi”, “mình”. Giữ nguyên từ xưng hô khi chúng là dữ liệu, lời trích dẫn hoặc nhân vật trong ví dụ. Không kể chuyện cảm xúc, không lời quảng cáo, không cụm từ giả tạo. Tên thuật toán/model bằng tiếng Anh theo curriculum. Diễn giải học thuật bằng lời văn tự soạn từ sách, bài báo và documentation chính thức; browse nguồn sơ cấp khi nghiên cứu, dẫn link kèm mục đích đọc. Không sao chép chương sách có bản quyền. Không tuyên bố quy định thi/GPU/Internet mới nhất nếu chưa có nguồn chính thức; kỹ năng thi nói rõ điều kiện môi trường và đọc thông báo cuộc thi.

Không dùng nội dung giáo trình cũ sơ sài thay cho bài soạn. Bài thường nên có khoảng 1.400–3.000 từ tùy độ khó (2.1 dài hơn vì là bài nền tảng), hình phục vụ đúng bước học, ví dụ tính/đọc bằng tay, 3–6 câu kiểm tra xen kẽ, code theo từng bước có chú thích, cách dùng thư viện khi phù hợp, lỗi dễ gặp, kỹ năng thi, tóm tắt, đọc thêm. Độ dài và số hình phục vụ nội dung, không kéo dài để đạt số lượng. Bài chiến lược/thi thử cần quy trình/đọc kết quả cụ thể thay cho ép đạo hàm vô nghĩa.

## Trắc nghiệm

Mỗi bài thường bắt buộc `## Kiểm tra cuối bài`, đúng 10 khối `::: quiz Câu 1` đến `Câu 10`, mỗi khối 3–4 lựa chọn, đúng một `[x]`, giải thích ngắn. Có câu hiểu bản chất, tính tay, shape/đọc code, đọc kết quả thực nghiệm, lỗi/điều kiện áp dụng. Phân bố vị trí đáp án, phương án nhiễu là nhầm lẫn thực tế. Khối hỏi nhanh xen kẽ đặt đúng sau bước học cần kiểm. Không đổi BTVN.

## Code và số liệu

Mọi khối ```python trong một bài chạy nối tiếp cùng namespace như notebook; nhỏ, tên biến dễ đọc, chia hàm theo ý nghĩa, không nhét nhiều thao tác vào một dòng. Nếu có print, đặt output đã chạy thật ngay sau khối code. Phần tính tay đối chiếu độc lập. CPU demo chạy offline nhanh bằng numpy/pandas/sklearn/torch có sẵn, seed cố định; không tải dataset/model trong code minh họa đã chạy. Nếu cần pretrained lớn, kèm recipe ở tệp riêng có kiểm môi trường và asset, nói rõ chưa chạy asset đó, demo CPU thật giải thích được cùng cơ chế. Không bịa số hiệu năng. Trước code nói mục đích, sau output nói nhìn dòng nào và suy ra gì.

Kiểm bằng `python -B -X utf8 tools/check_code.py content/phase-N/id.md --write`, rồi chạy lại không `--write`. Môi trường Windows CPU: torch có sẵn; peft/diffusers/torchaudio không mặc định. Không cài phần mềm toàn máy. Không để nhiều agent chạy training nặng cùng lúc. Notebook và tích hợp do root dựng sau khi hoàn tất source.

## Hình và slide

Giữ palette mẫu: INK/currentColor, CLAY #c2603e, BLUE #3b6ea8, SAND #b8892b; GREEN chỉ khi cần. Bám hình Linear regression của web cũ: SVG nền trong suốt, nét nhẹ, ít nhãn, Lora đồng bộ bài viết, chữ/trục adaptive currentColor. Mỗi hình giải quyết một câu hỏi học cụ thể bằng cơ chế, ví dụ tính hoặc dữ liệu thực; caption ngắn chỉ ra phải nhìn gì. Không ghi note/checklist trong hình, không ép số lượng hình. Biểu đồ số dùng Matplotlib; sơ đồ và ma trận có thể sinh trực tiếp bằng SVG hình học. Kiểm ảnh thật trong bài, tránh chữ đè hình/chữ, cả nền sáng và tối. Generator `content/phase-N/figures.py` gọi `figures-recipe/build.py`, SVG tại `content/phase-N/fig/`; báo cáo QA của lượt làm lại hình ở `../reports/20261003-figure-redesign/`.

Mỗi bài có deck Markdown `content/phase-N/slides/id.md` theo đúng mẫu 2.1, phân cách `---`, markers `<!-- title -->`, `<!-- section 1 -->`, `<!-- split -->` với `|||`, `<!-- center -->`, `<!-- figure -->`, `<!-- quiz -->`. Mỗi slide một ý, ít chữ, hình đủ lớn, code chỉ excerpt đã có trong note; deck khoảng 16–28 slide theo lượng nội dung, không ép mẫu slide hàng loạt y hệt. Có slide đặt vấn đề, hình trực giác, ví dụ tay, kết quả code, bẫy, hỏi nhanh, chốt ý. Dùng hình `../fig/name.svg`. Không đổi CSS. Root render HTML bằng renderer hiện có; không tạo PowerPoint với phong cách khác. Không dùng browser workaround cho file URL bị chặn; root đã xem hình từ PDF mẫu có sẵn bằng đọc tệp cục bộ.

## Hồ sơ nội bộ

Mỗi chương có `_intro.md`, các bài theo đúng ID curriculum, toàn bộ slide/hình. Tạo `receipts/phase-N/REVIEW.md` ghi nguồn đã nghiên cứu, lựa chọn sư phạm, tính tay/check code, phần asset chưa chạy, hướng dẫn tái tạo, điểm cần root kiểm. Với checkpoint của chương: ghi lại mục tiêu/ôn tập/dạy học và 10 câu ôn có giải thích, giữ bài thi/BTVN cũ nguyên vẹn. Không sửa registry chung; không coi công việc của agent khác là mình được quyền sửa. Root kiểm và tích hợp.
