# Giáo trình: nguồn, website và công cụ

Mọi lệnh dưới đây chạy trong thư mục `course/`, dùng `python -B -X utf8`.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `content/` | **Nguồn để sửa.** `phase-N/<id>.md` (bài học), `phase-N/slides/<id>.md` (slide), `phase-N/fig/*.svg` (hình), `phase-N/fig/*.anim.*` (hình động), `phase-N/_intro.md` (mở chương), `phase-N/homework/<id>/` (bài tập mới, khi có). Cú pháp: `content/README.md`; bài tập: `content/HOMEWORK.md`; mục Trắc nghiệm: `quizzes/<bộ>.py` (light, medium, high, extra, max, ultra), bảng nối câu với mục lý thuyết cần ôn `quizzes/learn.json` |
| `output/` | Website đã dựng (`START_HERE.html`, `ui/`, `giao_trinh/`). Không sửa tay trừ `ui/` |
| `tools/` | Dựng từng bài, kiểm code, kiểm nguồn, QA trình duyệt, xuất PDF, công cụ trắc nghiệm, tra đề |
| `exam-sources/` | Văn bản trích từ đề NOAI 2025–2026, USAAIO 2026, đề luyện CMU/MIT; bản đồ câu theo bài ở `BANK.md` |
| `figures-recipe/` | Script dựng lại các hình SVG; `figures-recipe/anim/` dựng 68 hình động (xem README ở đó) |
| `code-examples/` | Nguồn và công cụ của tab Code mẫu (xem README ở đó) |
| `build/` | `serve.py` (preview), `integrate.py` (bộ dựng toàn bộ đời đầu, chỉ để `tools/` import), các script authoring lần đầu |
| `receipts/` | Receipt dựng ban đầu theo chương (`phase-N/REVIEW.md`) và receipt từng bài của lượt chỉnh chu (`lessons/`) |
| `archive/` | ZIP raw đã kiểm CRC/SHA: trang cũ trước khi viết lại, bản trước và recipe của các lượt rà quiz/xưng hô |
| `AUTHORING_BRIEF.md`, `curriculum.json` | Chuẩn soạn bài; danh sách bài theo chương |

## Sửa một bài

1. Chép `content/phase-N/<id>.md` và `content/phase-N/slides/<id>.md` vào thư mục việc trong `04. Workspace/` trước khi sửa.
2. Sửa nguồn. Với chuỗi thay thế chính xác, dùng `tools/edlib.py`; ví dụ ở `../reports/20261004-lesson-polish/edits/`.
3. Nếu sửa code trong bài: `python -B -X utf8 tools/check_code.py content/phase-N/<id>.md --write`, rồi chạy lại không có `--write`.
4. Bật preview (`build/serve.py --port 56872`), rồi chạy:

   ```bash
   bash tools/finish_lesson.sh <id>
   ```

   Lệnh này lần lượt chạy code → kiểm nguồn → dựng riêng bài đó vào `output/` → kiểm mọi trang khác không đổi (77/77) → Chromium sáng/tối/mobile và mọi slide → ảnh ghép slide trong `04. Workspace/AI-course-qa/<id>/`. Sửa nhiều bài cùng lúc thì chạy `tools/rebuild_lesson.py <id>` cho tất cả trước, rồi mới chạy `finish_lesson.sh` từng bài.
5. Xuất PDF: `cd tools/qa && node make_pdfs.cjs <id…>`, rồi chạy lại `tools/rebuild_lesson.py <id>` (gắn nút tải) và `tools/check_all_lessons.py`.

Phần mở chương: `tools/rebuild_intro.py <N>`. Bài có `recipes/` (3.7, 4.1, 4.4, 4.5, 5.2, 5.3, 5.5–5.8, 6.2, 6.3, 6.5, 6.6, 7.2, 7.3, kt2) chưa dựng riêng được: `rebuild_lesson.py` sẽ từ chối cho đến khi được bổ sung nhánh đóng gói recipe như `integrate.py`.

## Hình động

Từ 11/10/2026 mỗi bài có ít nhất một hình động: chuỗi khung ảnh thật hoặc dữ liệu thật qua từng bước của kỹ thuật trong bài. Nguồn bài viết `![Chú thích](fig/<tên>.anim.webp)` trên một dòng riêng (slide: `../fig/<tên>.anim.webp`, thường trên slide `<!-- figure -->`). Tệp do `figures-recipe/anim/build_anim.py` dựng: `<tên>.anim.webp` (sprite các khung), có thể `<tên>.anim.dark.webp` (bản nền tối) và `<tên>.anim.json` (kích thước, nhãn từng khung, thời lượng, khung chính để in). `tools/render_theory.py` nhúng mô tả JSON vào HTML; `output/ui/anim.js` phát: tự chạy lặp khi cuộn tới, bấm hình hoặc nút để dừng, kéo thanh để xem từng khung, nhãn khung là chữ HTML đổi màu theo nền; bản in (PDF) hiện các khung chính cạnh nhau; notebook nhận một ảnh PNG ghép các khung chính. Caption trong bài và slide lấy từ manifest của recipe, đồng bộ bằng `python -B -X utf8 ../reports/20261011-animations/edits/anim_edit.py sync`.

## Công cụ

| Lệnh | Việc |
|---|---|
| `tools/rebuild_lesson.py <id> [--check]` | Dựng một bài (lý thuyết, slide, notebook, code, bài tập, nút PDF); `--check` chỉ so |
| `tools/check_all_lessons.py` | Render lại mọi bài và so với website; báo bài nào khác |
| `tools/audit_sources.py <id>` | Đủ 10 câu cuối bài, đúng một đáp án, đường dẫn hình, cú pháp code; ghi `receipts/lessons/` |
| `tools/check_code.py <md> [--write]` | Chạy code của bài và so khối output |
| `tools/qa/qa_lesson.cjs`, `tools/qa/make_pdfs.cjs` | QA Chromium; PDF bài học (A4) và slide (16:9) vào `output/giao_trinh/pdf/` (`AI_BASE=http://127.0.0.1:<cổng>` nếu preview chạy cổng khác) |
| `tools/qa/shot_anim.cjs [--base=…] <id…>` | Hình động: chụp từng hình ở nền sáng, nền tối, bản in (khung chính) và trang slide chứa nó vào `04. Workspace/AI-anim-20261011/shots/<id>/`; in lỗi console, slide tràn |
| `tools/quiz_dump.py <md>` | In từng câu trắc nghiệm, độ dài từng phương án, đánh dấu đáp án đúng dài nhất |
| `tools/quiz_stats.py phase-N/<id>.md …` | Đếm vị trí đáp án A/B/C/D và số câu đáp án đúng dài nhất |
| `tools/quiz_move.py phase-N/<id>.md '<chuỗi trong đáp án đúng>' <A-D> …` | Dời đáp án đúng, giữ thứ tự phương án sai |
| `tools/exam_find.py "từ khóa"` / `--page noai2026prelim 59` | Tra đề trong `exam-sources/` |
| `tools/build_contests.py [--check]` | Dựng mục Các cuộc thi từ `content/contests/` (`contests.json` + một tệp `.md` mỗi kỳ thi) thành `output/ui/contests.js`; kiểm link tới bài học |
| `tools/build_quizzes.py [--check]` | Dựng mục Trắc nghiệm (sáu bộ) từ `content/quizzes/` thành `output/ui/quiz-bank.js`: kiểm số câu từng chủ đề, đúng 4 phương án, vị trí đáp án đều, dòng nguồn, mọi câu đã nối mục ôn (`learn.json`); `--check` chỉ so |
| `tools/quiz_learn.py outline / find / cands / ingest / check / carry / audit / spots / section / mark` | Nối mỗi câu Trắc nghiệm với bài, mục `##` và câu văn cần đọc (dòng “Ôn lại” dưới lời giải, mở tab mới và tô câu). Câu cần đọc: `spots <bộ> --todo` hoặc `section <bài> "<mục>"` để xem câu, tệp chọn `MÃ.k: 2.1, 3.1-2`, rồi `mark <tệp>`. Sửa chữ một câu thì `carry --yes` chép nối cũ sang; câu mới thì `cands <bộ> --todo`, gán dòng `MÃ: 2.3§8, 2.5§3` (hoặc `MÃ: -` khi khóa học chưa dạy), rồi `ingest`; đổi tên mục `##` thì sửa tên trong `learn.json` (`check` chỉ chỗ) |
| `tools/qa/shot_learn.cjs [--base=…] [--all] [bộ:vị trí …]` | Kiểm dòng “Ôn lại” trên Chromium (sáng, tối, điện thoại): hiện sau khi trả lời, link mở tab mới đúng bài, cuộn tới đúng mục và tô đủ câu cần đọc, trang xem lại bài kiểm tra; `--all` mở cả 1734 link |

Chromium cho QA/PDF: `%LOCALAPPDATA%/ms-playwright/chromium-1200`, qua `playwright-core` trong `tools/qa/node_modules` (thiếu thì `npm install` trong `tools/qa`).

## Không làm

- Không chạy `build/integrate.py`: bước kiểm hash UI sẽ dừng vì `output/ui/app.js`, `portal.css`, `slides.css` đã được sửa có chủ đích (nút PDF, chân nguồn quiz, giao diện bài tập, bản in). Bản UI trước khi sửa ở `../reports/20261004-lesson-polish/` (mục Website).
- Không dùng `build/audit_sources.py` cho từng bài: nó ghi đè receipt cũ. Dùng `tools/audit_sources.py`.
- `build/final_verify.py`, `tools/preview_chapter.py` và các script `build/phase2_*` là hồ sơ của lần dựng đầu, trỏ tới thư mục phiên đã xóa; đọc để tham khảo, không chạy lại.
