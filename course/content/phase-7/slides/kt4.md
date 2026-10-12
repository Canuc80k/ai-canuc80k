<!-- title -->
# Kiểm tra khóa 3

Hai bài, hai lĩnh vực, sáu giờ: đi đến file nộp

Phase 7 · Ôn khóa Ảnh, chữ và âm thanh

---
<!-- split -->
## Kết thúc cả hai bài

Bài A có model nhưng B chưa có file nộp.

Hoặc notebook có điểm nhưng ID, schema sai.

|||

::: note Mục tiêu luyện
Hai bài thuộc hai lĩnh vực, sáu giờ, hai pipeline chấm được.
:::

Thời gian, phần cứng, luật chấm: đọc từ đề.

---
## Mục tiêu buổi ôn

- Ghi input, output, metric cho từng bài.
- Ước điểm theo luật chấm để chia ngân sách.
- Đọc lỗi theo từng ID trước khi đổi model.
- Chạy lại suy luận và kiểm file cuối.

---
<!-- section 1 -->
# Đọc nhiệm vụ trước model

---
<!-- split -->
## Head theo đáp án

Ảnh: class, box hay mask?

Chữ: class câu, nhãn token hay sinh chữ?

|||

Âm thanh: class clip, transcript hay khoảng thời gian?

Đa phương thức: retrieval, class hay đáp án tự do?

Tên encoder chưa nói định dạng nộp.

---
<!-- quiz -->
::: quiz
Đề detection yêu cầu box, class và score cho từng vật. Notebook đang ghi một class cho cả ảnh, với accuracy validation 0.90. Việc đầu tiên cần làm là gì?
- [x] Đổi head và file nộp sang dạng box, class, score
- [ ] Train thêm epoch cho accuracy của ảnh cao hơn
- [ ] Ghi một box phủ cả ảnh, kèm class đã đoán
- [ ] Giữ model, chỉ đổi tên cột cho khớp sample
Accuracy 0.90 đo một nhiệm vụ khác. Scorer detection ghép từng box với vật thật theo IoU, nên cần head ra box và file đúng schema.
:::

---
<!-- quiz -->
::: quiz
Đề âm thanh: mỗi clip dài 10 giây, cần nộp các khoảng (bắt đầu, kết thúc) có tiếng chó sủa, chấm theo độ trùng thời gian với khoảng thật. Baseline phân loại cả clip “có hay không có chó sủa” đạt accuracy 0.95. Còn thiếu gì?
- [ ] Không thiếu gì, clip có chó sủa thì nộp khoảng 0–10 giây
- [x] Dự đoán theo từng frame, rồi gộp các frame thành khoảng
- [ ] Đẩy accuracy theo clip lên trên 0.99 rồi mới nộp
- [ ] Dùng nhiều mel band hơn để thấy rõ tiếng sủa
Đề hỏi *lúc nào*, nên cần điểm từng frame, threshold, rồi gộp các frame dương liền nhau thành khoảng.
:::

---
<!-- section 2 -->
# Thời gian và điểm

---
<!-- center -->
## Có hai đường về đích

$$20+60+60+80+80+40+20=360\ \text{phút}$$

Đọc đề, baseline A, baseline B, cải tiến A, cải tiến B, suy luận, kiểm file.

Hai baseline trước, phần chốt giữ nguyên, phần cải tiến co giãn.

---
<!-- figure -->
## Lịch mẫu 360 phút

![Lịch mẫu 360 phút: đọc hai đề, dựng hai baseline, mỗi bài một khoảng cải tiến, rồi 60 phút cuối khóa model, suy luận và kiểm file. Khi trễ, chỉ phần cải tiến co lại.](../fig/7-kt4-schedule.svg)

---
<!-- quiz -->
::: quiz
Theo lịch mẫu, baseline A xong ở phút 80. Thực tế A xong ở phút 140, và đội vẫn giữ 60 phút cuối cho suy luận và kiểm file. Còn bao nhiêu phút cho baseline B và cải tiến, và nên làm gì trước?
- [ ] 220 phút, nên cải tiến A trước khi đụng tới B
- [ ] 220 phút, nên dựng baseline B trước
- [ ] 160 phút, nên cải tiến A trước vì A đã chạy
- [x] 160 phút, nên dựng baseline B trước
Còn $360 - 140 - 60 = 160$ phút. Dựng baseline B trước để có đường về đích thứ hai, rồi mới cải tiến.
:::

---
## Điểm chuẩn hóa

$$S=\max\left(0,\ \dfrac{X-X_{\mathrm{base}}}{X_{\mathrm{best}}-X_{\mathrm{base}}}\right)$$

```output
A, macro-F1 0.70 -> 50.0
A, macro-F1 0.74 -> 60.0
B, WER 0.30      -> 40.0
B, WER 0.45      -> 0.0
```

Cải tiến A thêm 10; baseline B đạt WER 0.30 thêm 40.

---
<!-- figure -->
## Kém baseline của đề thì được 0

![Điểm chuẩn hóa của hai bài trong ví dụ: kém baseline của đề (vạch đứt) thì được 0. Bài A tính theo macro-F1, bài B theo WER nên trục đảo chiều; các chấm là bốn trường hợp trong code.](../fig/7-kt4-score.svg)

---
<!-- quiz -->
::: quiz
Vẫn luật chấm như trong ví dụ, với bài B có baseline WER 0.40 và bài tốt nhất 0.15. Baseline B nhanh nhất ước đạt WER 0.38. Bài B được bao nhiêu điểm?
- [x] 8
- [ ] 92
- [ ] 38
- [ ] 0
$(0.38 - 0.40)/(0.15 - 0.40) = 0.08$, tức 8 điểm.
:::

---
<!-- section 3 -->
# Kiểm output và scorer

---
<!-- split -->
## ID trước điểm

Dictionary có prediction theo ID.

Xuất theo manifest `img-a, img-b, img-c`, không theo batch.

|||

```output
[2 0 1]
accuracy minh hoa = 0.667
```

Nhãn đặt tay: khâu xuất file phải đúng với mọi model.

---
<!-- figure -->
## Cùng dictionary, hai thứ tự hàng

![Cùng dictionary dự đoán theo ID của bài: ghi theo insertion order thì mỗi hàng nộp mang dự đoán của ID khác (đúng 0/3); sắp theo manifest thì đúng 2/3 như code.](../fig/7-kt4-ids.svg)

---
<!-- quiz -->
::: quiz
Mỗi file test dài 30 giây được cắt thành ba đoạn 10 giây cho khớp độ dài lúc train. Vì vậy bảng dự đoán có ba hàng cho mỗi ID, mỗi hàng là xác suất của ba lớp. Sample submission có một hàng mỗi ID. Ghi file nộp thế nào?
- [ ] Giữ cả ba hàng, vì scorer tự lấy trung bình theo ID
- [ ] Gọi `drop_duplicates("id")`, giữ nhãn của đoạn đầu
- [x] Gộp xác suất theo ID, lấy argmax, rồi ghép theo sample
- [ ] Bỏ phép cắt, đưa nguyên clip 30 giây vào model
Sample có một hàng mỗi ID, và scorer không hứa gộp giúp. Gộp xác suất các đoạn theo ID, lấy argmax, rồi assert mỗi ID một hàng.
:::

---
<!-- figure -->
## Ba đoạn, một hàng

![Một file 30 giây cắt thành ba đoạn 10 giây (xác suất đặt tay): trung bình xác suất ba đoạn theo ID rồi argmax, để file nộp có đúng một hàng cho ID ấy.](../fig/7-kt4-segments.svg)

---
<!-- split -->
## WER khác đúng cả câu

Một token thiếu trong tổng sáu token.

Một trong hai câu đúng hoàn toàn.

|||

```output
[(1, 3), (0, 3)]
corpus WER = 0.167
cau dung hoan toan = 1/2
```

Chuẩn hóa chữ là một phần của scorer.

---
<!-- quiz -->
::: quiz
Scorer local là hàm `token_errors` ở trên. Scorer của đề thì hạ chữ thường và bỏ dấu câu trước khi tách token. Reference là `em học ai`, transcript là `Em học AI.`. WER theo scorer local và theo scorer của đề lần lượt là bao nhiêu?
- [ ] 2/3 và 0
- [x] 1/3 và 0
- [ ] 1/3 và 1/3
- [ ] 0 và 0
Local đã hạ chữ thường nhưng vẫn giữ dấu chấm, nên đếm 1 lỗi trên 3 token. Scorer của đề bỏ dấu câu, nên WER bằng 0.
:::

---
<!-- figure -->
## Hai scorer, một transcript

![Transcript “Em học AI.” qua hai scorer: scorer local chỉ hạ chữ thường nên còn token “ai.” khác “ai” (WER 1/3); scorer của đề bỏ thêm dấu câu nên khớp hoàn toàn (WER 0).](../fig/7-kt4-normalize.svg)

---
<!-- section 4 -->
# Đọc lỗi theo ID

---
<!-- split -->
## Ba cấu hình, 25 mẫu

Fusion hơn ảnh 0.04: một mẫu, chưa đủ để kết luận.

Năm ID đổi kết quả: sửa 3, làm sai 2.

|||

```output
anh    accuracy = 0.80
chu    accuracy = 0.76
fusion accuracy = 0.84
fusion sua    : [3, 11, 17]
fusion lam sai: [8, 21]
ca ba cung sai: [5, 14]
```

---
<!-- figure -->
## Đọc từng mẫu

![Đúng/sai theo từng ID của ba cấu hình trên 25 mẫu validation (từ code bài), ô đặc là đúng: fusion sửa ba ID nhánh ảnh sai, làm sai thêm hai ID nhánh ảnh đúng; ID 5 và 14 cả ba cùng sai.](../fig/7-kt4-paired.svg)

---

<!-- figure -->
## Đọc lỗi theo ID

![Đúng/sai theo từng ID của ba cấu hình trên 25 mẫu validation của buổi kiểm tra, rồi khoanh các nhóm ID cần đọc: fusion sửa, fusion làm sai, cả ba cùng sai.](../fig/7-kt4-ids.anim.webp)

---
<!-- quiz -->
::: quiz
Với 25 dự đoán ở trên, xét mọi cách gộp chỉ chọn giữa dự đoán của nhánh ảnh và của nhánh chữ ở từng mẫu. Cách gộp tốt nhất có thể, tức luôn chọn đúng nhánh đúng, đạt accuracy bao nhiêu?
- [x] 0.92
- [ ] 0.84
- [ ] 0.96
- [ ] 1.00
Chỉ ID 5 và 14 có cả hai nhánh cùng sai, nên trần là $23/25 = 0.92$.
:::

---
<!-- section 5 -->
# Chốt và chạy lại

---
## Kiểm ở tiến trình mới

- Nạp checkpoint, processor, cấu hình đã lưu.
- Input đúng sample rate, shape, mask.
- Prediction đủ ID, không trùng, không thiếu, không NaN.
- Khóa cả cấu hình sinh.
- Ghi metric, runtime và giới hạn asset.

---
<!-- quiz -->
::: quiz
Chạy lại suy luận VLM ở một tiến trình mới, cùng checkpoint, prompt và ảnh, thì 14 trong 200 câu trả lời khác với lần chạy trong notebook. Cấu hình sinh đang là `do_sample=True, temperature=0.7`. Chốt file nộp thế nào?
- [ ] Chạy thêm vài lần, nộp lần có validation cao nhất
- [ ] Giữ sampling, vì file nào cũng hợp lệ, rồi nộp lần cuối
- [x] Sinh bằng greedy, chạy lại hai lần và so khớp từng ID
- [ ] Giảm `max_new_tokens` để câu trả lời ổn định hơn
Sampling cho mỗi lần chạy một file khác. Greedy cho kết quả xác định, và hai lần chạy khớp nhau là bằng chứng pipeline tái lập được.
:::

---
## Khi đi thi

- Đọc cả hai đề trước khi code.
- Hai baseline vượt baseline đề, rồi mới cải tiến.
- Scorer local khớp scorer của đề.
- Đọc lỗi theo ID trước khi đổi model.
- Khóa sớm, chạy lại ở tiến trình mới.
- Kiểm file cuối, giữ bản dự phòng.

---
<!-- section 6 -->
# Luyện đề

---
<!-- quiz -->
::: quiz Luyện đề 1
Một CNN 1D trên log-mel cho mỗi frame của clip một điểm $z_t$, và $z_t$ cao nghĩa là frame ấy có tiếng mưa. Theo nhãn của đề, clip dương nếu mưa chiếm ít nhất nửa thời lượng. Gộp $z_1, \dots, z_T$ thành một điểm của clip, rồi so với ngưỡng, bằng cách nào thì khớp với định nghĩa nhãn?
- [ ] Lấy max của các $z_t$
- [ ] Lấy min của các $z_t$
- [ ] Lấy trung bình của các $z_t$
- [x] Lấy trung vị của các $z_t$
“Ít nhất nửa thời lượng” là câu hỏi về số frame có mưa, nên trung vị vượt ngưỡng đúng khi ít nhất nửa số frame vượt ngưỡng.
Phỏng theo: [MIT 6.036 · Final, Spring 2022 · Q8(b)](https://introml.mit.edu/_static/fall22/final/review/6036_final_sp22.pdf#page=21)
:::

---
<!-- quiz -->
::: quiz Luyện đề 2
Mỗi mẫu là một video 10 giây. Nhánh ảnh lấy 25 khung hình mỗi giây, được 250 vector. Audio encoder trả 50 vector mỗi giây, được 500 vector. Để fusion theo từng bước, đội lấy 250 vector audio đầu cho khớp shape. Code chạy, hai nhánh cùng shape `(250, d)`, nhưng fusion trên validation chỉ ngang với nhánh ảnh. Nên làm gì trước?
- [ ] Kết luận audio không giúp gì và bỏ nhánh audio
- [x] Đổi chỉ số của mỗi cặp ra giây, rồi assert hai bên trùng mốc
- [ ] Thêm assert hai nhánh cùng shape trước bước fusion
- [ ] Train fusion thêm vài epoch để nó tự học cách căn
250 vector audio đầu chỉ dài 5 giây, còn 250 khung ảnh dài 10 giây. Shape khớp mà thời điểm lệch, nên phải assert theo giây.
Phỏng theo: [NOAI 2026 Singapore · Vòng sơ loại · Câu 266](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=95)
:::

---
<!-- quiz -->
::: quiz Luyện đề 3
Đề hỏi đáp về ảnh có 1500 bộ (ảnh, câu hỏi, đáp án) để train, một GPU T4, và được dùng hai checkpoint pretrained: một vision encoder, và một language model chỉ đọc chữ, chưa từng được nối với nhau. Nên train phần nào?
- [ ] Fine-tune toàn bộ language model, giữ vision encoder
- [ ] Train một VLM nhỏ từ đầu cho vừa bộ nhớ T4
- [x] Giữ nguyên hai model, chỉ học lớp nối ảnh vào language model
- [ ] Không train gì, mô tả ảnh bằng chữ rồi đưa vào prompt
Giữ nguyên vision encoder và language model, chỉ học lớp nối ảnh vào model chữ: ít tham số, vừa với 1500 mẫu và một T4.
Phỏng theo: [NOAI 2026 Singapore · Vòng sơ loại · Câu 263](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=94)
:::

---
<!-- center -->
## Chốt buổi luyện

Mỗi bài: baseline chấm được, validation, một so sánh giải thích được, output tái lập.

Chưa xong thì ghi khâu dừng và luyện đúng khâu đó trên bài nhỏ.

---
<!-- center -->
## Sau buổi ôn

Làm **10 câu kiểm tra cuối bài** trên trang bài học.

Chữa từng câu sai theo đúng mục của buổi ôn; chạy lại ví dụ kiểm ID và ví dụ WER.
