# Soạn bài tập về nhà

Tài liệu nội bộ, không đưa lên website. Bài mẫu đầy đủ ở `content/_homework-template/`.

## Đặt tệp ở đâu

Mỗi bài học có một thư mục riêng: `content/phase-N/homework/<id>/`, ví dụ `content/phase-2/homework/2.2/`. Trong đó mỗi bài tập là một nhóm tệp cùng tên gốc `bai-K`, đánh số liên tục từ 1:

| Tệp | Bắt buộc | Trên website |
|---|---|---|
| `bai-1.md` | có | Đề bài; nút tải "Đề bài" |
| `bai-1.py` | không | Khối "Code khởi đầu" có nút sao chép; nút tải "Code khởi đầu" |
| `bai-1.in`, `bai-1.out` | không | Nút tải "Input mẫu", "Output mẫu" |
| `bai-1.ipynb`, `bai-1.csv`, `bai-1.zip`, tệp khác | không | Nút tải "Notebook", "Dữ liệu" hoặc "Tệp kèm" |

Tệp có tên bắt đầu bằng `_` bị bỏ qua, dùng cho bản nháp. Khi thư mục của một bài học có ít nhất một `bai-K.md`, tab Bài tập của bài đó hiện bộ bài mới và ẩn bài tập cũ; xóa hết `bai-*.md` thì bài tập cũ hiện lại.

## Viết đề

Dòng đầu là `# Tên bài` (hiện trên thẻ chọn bài và tiêu đề). Phần còn lại là Markdown như bài học: công thức `$...$`, `$$...$$`, code, bảng, hình `![Chú thích](fig/ten.svg)` (đặt hình trong `homework/<id>/fig/`), khối `::: tip`, `::: note`, `::: trap`. Nên dùng các mục:

- `## Input`, `## Output`: định dạng và giới hạn.
- `## Ví dụ`: một khối ```` ```input ```` đặt ngay trước một khối ```` ```output ```` sẽ hiện thành hai cột "Input mẫu / Output mẫu". Có thể lặp nhiều cặp.
- `## Tự kiểm tra`: danh sách gạch đầu dòng ngay sau tiêu đề này hiện thành checklist.

Tiêu đề `##` trong đề hiện nhỏ, gọn; không cần `## Đề bài` cho đoạn mở đầu.

## Dựng

```
python -B -X utf8 tools/rebuild_lesson.py 2.2
```

Lệnh dựng lại riêng bài 2.2 (bài học, slide, notebook và bài tập) và chép các tệp bài tập vào `output/giao_trinh/homework/2.2/`. Chạy từ thư mục `course/`. Nếu sai định dạng (thiếu `# Tên bài`, đánh số nhảy cóc), lệnh dừng và báo tệp lỗi.
