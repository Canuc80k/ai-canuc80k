# Code mẫu

Nguồn tab **Code mẫu**: `content/phase-N/<id>.md` (67 bài, 212 ví dụ, 265 khối Python). Chuẩn soạn: `AUTHORING_BRIEF.md`.

## Sửa một bài Code mẫu

1. Sửa `content/phase-N/<id>.md`.
2. Chạy lại code và ghi output thật:

   ```bash
   python -B -X utf8 tools/run_examples.py content/phase-N/<id>.md --write
   ```

   Lệnh chạy mỗi ví dụ trong tiến trình riêng, chạy cả bài nối tiếp, rồi ghi receipt vào `verification/<id>.json`.
3. Dựng: `python -B -X utf8 build_examples.py` ghi vào `build/stage/` các tệp `giao_trinh/code-examples/{code,notebook,source}/…` và `ui/code-examples.js`. Lệnh từ chối bài nào chưa có receipt chạy qua hoặc code đã đổi sau receipt.
4. Chép các tệp trong `build/stage/` sang `../output/` (cùng đường dẫn tương đối), rồi xóa `build/`.

`build_examples.py` đã được bỏ bước stage `app.js` và `START_HERE.html` của bản UI cũ, để không ghi đè UI hiện hành. Kiểm ngày 05/10/2026: dựng lại ra 205 tệp khớp từng byte với `../output/`.
