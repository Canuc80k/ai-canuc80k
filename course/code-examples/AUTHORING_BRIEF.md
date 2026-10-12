# Code mẫu AI Canuc80k — phạm vi và chuẩn bàn giao

Yêu cầu ngày 03/10/2026: hoàn thiện code mẫu/code ví dụ của từng bài thành một mục riêng để dùng giảng dạy trả phí. Không chỉnh lại bài lý thuyết. Mẫu phải giúp người mới hiểu quá trình, có ngữ cảnh ngắn, chú thích có ích, output thật và có thể mở rộng nhẹ ở ví dụ cuối. Không viết lời giảng máy móc hoặc chú giải những dòng hiển nhiên.

## Quyền ghi

- Chỉ tạo/sửa nguồn mới trong workspace này, `content/phase-N/<id>.md`, hình mới trong `content/phase-N/fig/`, và receipt riêng ở `reviews/phase-N.json`.
- Bài lý thuyết hiện hành chỉ đọc: `../AI-course-opus-standard-20261002/content/phase-N/<id>.md`. Curriculum chỉ đọc: `../AI-course-opus-standard-20261002/curriculum.json`.
- Không sửa quiz, slide, hình cũ, bài tập, dataset, UI hay output đang phục vụ. Root phụ trách UI/tích hợp đúng phạm vi tab Code.
- Đọc README/AGENTS/Guide của project; không quét Recycle Bin, .git, .opencode, node_modules. Không thao tác LQDOJ, Auto/AI, upload, submit hoặc rejudge.

## Một bài code mẫu

- `# Code mẫu — <tên bài>` và 1–2 câu nối với vấn đề/cơ chế của bài lý thuyết.
- `## Ví dụ 1: <bài toán cụ thể>`, rồi Ví dụ 2, 3... theo mạch học. Thường 2–4 ví dụ có mục đích khác nhau; không thêm cho đủ số. Bài ôn cần một quy trình tổng hợp và một phép kiểm/lỗi thực tế.
- Mỗi ví dụ nêu dữ liệu/đơn vị và câu hỏi trong vài câu. Khi hữu ích, có thể chia code thành vài khối theo các bước có ý nghĩa; giữa khối có lời giải thích ngắn. Một ví dụ phải chạy độc lập từ đầu, và cả bài chạy nối tiếp cũng phải đúng.
- Dùng dữ liệu nhỏ có thể đối chiếu bằng tay trước, rồi mới mô phỏng/thử quy trình thư viện. Ít nhất một ví dụ của mỗi bài cho thấy vì sao kết quả đổi khi đổi một điều kiện, hoặc phát hiện một lỗi quan trọng. Không dùng cùng khung câu/khung ví dụ máy móc cho mọi bài.
- Chú thích giải thích lựa chọn, shape, trục, nguồn rò rỉ, bước gradient hoặc điều kiện áp dụng khi cần. Không chú thích kiểu `# import thư viện`, `# in kết quả` hay diễn giải mọi phép cộng.
- Sau mỗi khối có in ra, đặt `output` chạy thật ngay sau fence. Sau output, chỉ ra 1–3 con số/dòng/ô cần nhìn và liên hệ cơ chế của bài. Không bịa số hiệu năng, accuracy, dữ liệu hay output.
- Ví dụ cuối có thể nâng cao vừa sức: thay tham số có chủ đích, thêm kiểm chứng/edge case, đo một điều kiện tổng quát, ghép vào pipeline gọn. Không đưa một khối trăm dòng thiếu cầu nối.
- Không gọi trực tiếp người đọc là “các em”, “em”, “bạn”, “mình”. Giọng trung tính, con người, súc tích. Giữ từ xưng hô nếu nó là dữ liệu token/lời trích/nhân vật trong ví dụ.
- Không thêm quiz, giáo trình dài, khẩu hiệu hoặc ghi chú nội bộ vào trang của người học.

## Code và kiểm thực thi

- Python 3.13; NumPy 2.2.6, pandas 2.3.2, scikit-learn 1.7.2, PyTorch 2.9.1 CPU và Matplotlib đang có. Chỉ dùng thư viện thực sự có trong môi trường.
- Demo CPU offline, không tải dataset/model, không cài phần mềm, không dùng GPU. Seed cố định; output gọn và ổn định, round số thập phân/shape khi cần. Không in thời gian đo máy làm một output cố định.
- Với torch: giới hạn threads, seed, kích thước dữ liệu/mạng và số epoch. Chương GPU dùng ví dụ CPU chạy được và thể hiện đúng điều kiện thiết bị; không gán số đo CPU thành GPU.
- Bài pretrained/CLIP/BERT/LLM... phân biệt rõ mô hình nhỏ minh họa cơ chế với một model pretrained thật. Ưu tiên code CPU thực sự hoàn chỉnh cho cơ chế/quy trình; không để “TODO tải model” thành ví dụ chính. Không giả nhận đã chạy asset/model thật.
- Các khối `python` trong một ví dụ chia sẻ namespace, nhưng ví dụ kế tiếp phải có imports/data/setup cần thiết để chạy riêng. Cả bài cũng chạy nối tiếp được. Không phụ thuộc biến/asset từ bài khác.
- Hình mới chỉ khi nó giúp đọc code/output, do code sinh thật. Nếu lưu hình, tạo tên có ID bài trong `fig/` của phase được giao; SVG không có Date metadata, có hashsalt cố định. Không sửa hình cũ. Dùng Markdown `![caption ngắn](fig/<id>-<tên>.svg)`.
- Controller `tools/run_examples.py` trong workspace sẽ chạy code và ghi/kiểm output; chờ nó có trước khi chạy training. Mọi chạy thử dùng controller có gate tối đa 2 tiến trình, không tự chạy nhiều training song song.
- Nếu chưa chắc API/giả thiết, đọc primary docs hoặc nguồn trong bài hiện hành. Có thể browse tài liệu chính thức; ghi mục cụ thể đã đối chiếu trong receipt, không kéo dài trang học bằng nguồn nội bộ.

## Receipt

Một JSON mỗi phase: IDs đã đọc, các ví dụ và mục đích học, phép kiểm độc lập/tính tay/edge case, nguồn API đã đối chiếu, trạng thái controller, giới hạn thực tế. Không tuyên bố xong nếu code/output chưa chạy thật. Không chỉ check cú pháp; đọc lại toàn bộ lời dẫn, code và kết quả.

Root sẽ đọc chéo, kiểm tất cả bài, dựng trang/code/notebook tải về và kiểm browser thật trước khi bàn giao.
