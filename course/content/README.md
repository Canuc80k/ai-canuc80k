# Mẫu soạn lý thuyết

Chương Học máy cổ điển (`phase-2/`) là mẫu cho các chương khác. Tài liệu nội bộ, không đưa lên website.

## Tệp

- `phase-N/_intro.md`: mở chương. Hiện ở trang Phase, trên danh sách bài.
- `phase-N/<id>.md`: một bài, `id` trùng `curriculum.json` (ví dụ `2.4.md`). Có tệp này thì tab Bài học dùng nó thay cho bài cũ.
- `phase-N/fig/*.svg`: hình vector, tái tạo bằng `figures.py` từ recipe được lưu.
- `phase-N/slides/<id>.md`: slide của bài (xem mục Slide). Có tệp này thì tab Slide dùng bộ slide mới, kèm bản PDF.

## Khung một bài

Bài 2.1 là mẫu đầy đủ. Một bài là một buổi giảng, đọc từ trên xuống là giảng được:

1. `# Tên bài` (chỉ để đọc nguồn; website dùng tên trong `curriculum.json`).
2. Đoạn mở: một tình huống thật gần với học sinh, dẫn tới câu hỏi bài sẽ trả lời.
3. `::: goal` 3–4 việc học sinh làm được sau bài, viết bằng động từ (viết, kiểm tra, đoán trước, đối chiếu).
4. Các mục giảng `##` theo đúng thứ tự dạy. Mỗi mục: vì sao cần → hình ảnh trực giác → công thức → code chạy được → đọc kết quả. Cuối mục quan trọng đặt một `::: quiz`.
5. Với mô hình tự cài được: có bảng shape, code NumPy ngắn, kiểm gradient (nếu có đạo hàm), đối chiếu thư viện. Đây là một phần của bài, không phải trục chính; phần dùng thư viện đúng quy trình và đọc kết quả cũng quan trọng như vậy.
6. Thí nghiệm có số liệu thật thay cho lời khẳng định (learning rate, chuẩn hóa, overfit...). Lý thuyết dự đoán trước, code xác nhận sau.
7. `## Ví dụ tính tay`, một mục ứng dụng gần với học sinh, rồi `## Khi đi thi`, `## Tóm tắt`, `## Kiểm tra cuối bài`, `## Đọc thêm`. Từ 14/10/2026 không có mục Bẫy, hộp `::: trap`, ô Nhắc lại hay mục Tìm hiểu kỹ; không nhồi khái niệm chỉ để phủ syllabus. Bài ưu tiên đơn giản, thực dụng; dạy lại kiến thức cũ khi cần là tốt.
8. `## Kiểm tra cuối bài`: mặc định 10 câu `::: quiz Câu 1` ... `::: quiz Câu 10`, bao quát cả bài, có câu tính toán nhỏ và câu đọc kết quả. Website tự chấm và hiện điểm.
9. `## Đọc thêm`: tài liệu công khai, có link khi miễn phí, mỗi mục một câu nói đọc để làm gì. Không ghi tài liệu nội bộ.

Không phải bài nào cũng cần đủ mọi mục; bài khái niệm (ví dụ phân cụm) có thể ít code hơn, nhưng vẫn giữ nhịp giảng và câu hỏi nhanh.

## Khối đặc biệt

```
::: goal Mục tiêu sau bài học       (tiêu đề tùy chọn; mặc định "Mục tiêu")
- ...
:::

::: trap Đừng nghịch đảo ma trận     (nền nhấn; cũng có tip, note)
Nội dung Markdown, có công thức và code.
:::

::: quiz                             (tiêu đề mặc định "Hỏi nhanh")
Câu hỏi, có thể có $công thức$ và `code`.
- [ ] Lựa chọn sai
- [x] Lựa chọn đúng (đúng một)
- [ ] Lựa chọn sai
Giải thích ngắn, hiện ra sau khi bấm chọn.
:::
```

Câu hỏi nhanh để hỏi bài, không để đánh đố: một ý, 3–4 lựa chọn, mỗi lựa chọn sai là một hiểu lầm có thật. Lời giải thích chỉ ra vì sao lựa chọn sai dễ bị chọn.

## Code và kết quả

- Mọi khối ```` ```python ```` trong một bài chạy nối tiếp như notebook, dùng chung biến.
- Ngay sau khối nào có in ra thì đặt khối ```` ```output ````. Không gõ tay: chạy `python tools/check_code.py content/phase-N/x.md --write` để ghi kết quả thật, và chạy lại không có `--write` để kiểm.
- Số liệu nhắc trong lời giảng phải khớp với khối output.
- Mỗi bài có code được xuất thành notebook (`tools/make_notebooks.py`), tải ở mục lục bên phải của bài.

## Văn phong

Giọng học thuật nhưng có người dạy đứng sau: chặt chẽ, rõ ràng, đoán trước chỗ học sinh vấp. Bài 2.1 là giọng mẫu.

- **Xưng hô:** dùng văn phong trung tính, câu vô chủ hoặc "ta" trong lập luận. Không gọi trực tiếp người đọc là "các em", "em", "các bạn" hay "bạn"; không xưng "thầy", "tôi", "mình" hoặc kể chuyện bản thân. Giữ nguyên từ xưng hô khi chúng là dữ liệu, lời trích dẫn hoặc nhân vật trong ví dụ.
- **Đứng ở chỗ người dạy:** trước mỗi công thức hay đoạn code, nói vì sao cần nó. Sau mỗi kết quả, chỉ ra con số nào cần nhìn và nó nói lên điều gì.
- **Đứng ở chỗ người học:** đoán trước chỗ vấp và giải thích ngay tại đó: ký hiệu lạ, khái niệm chưa học (trị riêng, gradient, `nan`), kết quả trông bất thường (test cao hơn train). Kiến thức vượt cấp thì cho một cách hiểu trực giác dùng được, phần chặt chẽ để dành.
- **Hình ảnh trước, công thức sau:** cái bát, đi xuống núi trong sương mù, thung lũng dài hẹp, cái bóng chiếu xuống mặt sàn.
- **Không sến, không phô cảm xúc:** không "thầy khuyên thật", "chỗ thầy thích nhất", "lỗi thầy sợ nhất", "đừng mừng vội", "đơn giản đến bất ngờ". Không câu khẩu hiệu. Hài hước tối đa một hai chỗ, đặt trong tình huống, không bình luận thêm.
- **Câu rõ chủ ngữ, dài ngắn đan xen.** Tránh gạch đầu dòng khi một đoạn văn nói được; tránh văn liệt kê kiểu "X: ...; Y: ...".
- **Không đề cao một phần nào quá mức.** Tự cài bằng NumPy, kiểm gradient hay đối chiếu thư viện chỉ là một phần; trọng tâm là hiểu mô hình, dùng đúng và đọc được kết quả.
- **Tên thuật toán, mô hình, kỹ thuật viết bằng tiếng Anh**: linear regression, decision tree, clustering, gradient descent; lần đầu có thể kèm tiếng Việt trong ngoặc. Tên bài trong `curriculum.json` theo cùng quy tắc.
- Khái niệm chung: tiếng Việt trước, tiếng Anh trong ngoặc ở lần đầu (phần dư (residual), số điều kiện (condition number)).
- Mô tả bài trong `curriculum.json`: một câu ngắn (dưới khoảng 50 ký tự) bằng lời thường, nói bài học làm gì. Không liệt kê thuật ngữ, không giải thích dài.
- Mỗi con số trong bài phải có nguồn: tính tay, code đã chạy, hoặc trích dẫn.
- Không ghi chú cho người soạn trong văn bản. Ghi chú nội bộ để ở `curriculum.json` (`outcome`, `syllabus`).

## Slide

Mỗi slide cách nhau bởi dòng `---`. Dòng đầu chọn bố cục: `<!-- title -->` (bìa), `<!-- section 2 -->` (mở phần), `<!-- split -->` (hai cột, ngăn bởi `|||`), `<!-- figure -->` (một hình lớn), `<!-- center -->` (công thức lớn), `<!-- quiz -->` (câu hỏi bấm hiện đáp án). Không ghi là slide thường với tiêu đề `##`. Hình viết `../fig/x.svg`.

Một slide một ý, chữ ít hơn bài học: câu ngắn, gạch đầu dòng được phép. Code trên slide là đoạn trích; khối output chép đúng kết quả thật của bài. Bộ dựng tự thu nhỏ chữ khi slide quá dài; nếu bị thu nhỏ thì nên tách slide.

## Toán

- `$...$` trong dòng, `$$...$$` riêng dòng. Macro có sẵn: `\R`, `\E`, `\argmin`, `\argmax`.
- Vector in đậm `\mathbf{x}`, ma trận in hoa `X`, chuyển vị `^\top`, chuẩn `\lVert\cdot\rVert`.
- Công thức riêng dòng kết thúc bằng dấu câu của câu chứa nó.
- Công thức dài tự thu nhỏ trên điện thoại (tối đa còn 66%). Hai công thức độc lập và dài thì tách hai dòng `$$`.

## Hình

- Bám hình Linear regression của web cũ: hình gọn, nền trong suốt, đường nét nhẹ, ít nhãn. Dùng Lora như bài viết; chữ và trục đổi theo nền sáng/tối. Không thêm note, đoạn giải thích hay checklist vào hình.
- Mỗi hình phải làm rõ một bước tính, quan hệ hình học, luồng dữ liệu hoặc kết quả thực nghiệm trong đoạn đang học. Không ép số lượng hình; bỏ hình chỉ lặp lại văn bản. Đặt hình sát ví dụ tương ứng và trước câu hỏi kiểm tra bước đó.
- Bảng màu: `CLAY` (nhấn), `BLUE`, `SAND`, `GREEN` khi cần; thêm nhãn hoặc kiểu nét để không phụ thuộc riêng màu. Nhãn trực tiếp hoặc legend ngắn ở vùng trống, không đè lên dữ liệu. Kiểm render ở kích thước thật trên trang, cả nền sáng và tối.
- Biểu đồ số dùng Matplotlib với dữ liệu có nguồn; sơ đồ, ma trận và token dùng SVG có recipe hình học. `figures.py` gọi recipe tại `figures-recipe/build.py` (xem README ở đó); dữ liệu thực nghiệm nằm cùng recipe.
- Chèn bằng `![Chú thích ngắn chỉ ra điều cần quan sát.](fig/N-k-ten.svg)` trên một dòng riêng.
- Hình động: `![Chú thích một dòng.](fig/N-k-ten.anim.webp)` trên một dòng riêng; tệp do `figures-recipe/anim/build_anim.py` dựng (sprite WebP + mô tả JSON), không vẽ tay. Mỗi khung có nhãn ngắn hiện dưới hình; caption nói điều cần quan sát qua cả chuỗi.

## Dựng

```
python content/figures.py                            # sinh hình
python tools/check_code.py content/phase-2/2.1.md    # chạy code trong bài, so với khối output
python tools/render_theory.py content theory.json    # Markdown + KaTeX -> theory.json
python tools/make_notebooks.py content notebooks     # notebook cho từng bài
python tools/render_slides.py content slides_out --pdf=<thư mục ui của website>   # slide HTML + PDF
```

Sau đó dựng website như thường lệ (`build_ui.py` đọc `theory.json`). `render_theory.py` dừng nếu công thức sai cú pháp.
