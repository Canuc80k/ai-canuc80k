<!-- title -->
# Kiểm tra khóa 1

Từ đọc dữ liệu đến đầu ra đáng tin

Phase 2 · Ôn khóa Học máy

---
<!-- split -->
## Ba dấu mốc khác nhau

Notebook chạy hết.

File dự đoán đúng hợp đồng.

Điểm validation đáng tin.

|||

Một dấu mốc chưa chứng minh hai dấu mốc còn lại.

Buổi này đi lại cả quy trình bằng một ví dụ chạy được.

---
<!-- section 1 -->
# Đề và giao thức

---
<!-- center -->
## Mẫu mới là mới ở đâu?

Người mới → split theo người.

Lần đo tương lai → split theo thời gian.

Mẫu độc lập cùng phân phối → random split có thể phù hợp.

Không chọn split theo tên cột. Hỏi trước: validation mới khác train ở người, thời điểm, hay chỉ ở hàng độc lập?

---
<!-- figure -->
## Ba cách chia

![Ba cách chia cùng một bảng học sinh × lần đo: random theo hàng để mỗi người nằm cả hai phía; group giữ người mới cho validation; theo thời gian giữ lần đo sau mốc cắt.](../fig/2-kt1-splits.svg)

---
<!-- quiz -->
::: quiz
Mỗi học sinh có 5 hàng, và ta cần đánh giá trên học sinh chưa từng thấy. Chia thế nào là phù hợp nhất?
- [ ] Ngẫu nhiên từng hàng
- [x] Theo nhóm, mỗi học sinh là một nhóm
- [ ] Sắp theo target rồi chia
- [ ] Theo thời gian của lần đo
Muốn đánh giá trên người mới thì mỗi học sinh phải nằm trọn một phía.
:::

---
<!-- quiz -->
::: quiz
Mỗi học sinh có nhiều lần đo theo thời gian. Mục tiêu là dự đoán lần đo kế tiếp của chính những học sinh đã có trong dữ liệu. Chia dữ liệu thế nào cho đúng mục tiêu?
- [x] Theo thời gian, validation là các lần đo sau mốc cắt
- [ ] Theo nhóm học sinh, lấy người mới làm validation
- [ ] Ngẫu nhiên từng hàng, theo tỉ lệ 80/20
- [ ] Sắp theo target rồi cắt phần cuối
Học sinh không mới, lần đo mới, nên validation là các lần đo sau mốc cắt.
:::

---
<!-- section 2 -->
# Baseline và so sánh

---
<!-- center -->
## Metric quyết định baseline

MAE → median baseline.

MSE → mean baseline.

So mọi mô hình trên cùng fold và cùng metric.

Baseline là một phương án hợp lệ để so sánh và có thể dùng làm bài nộp đầu tiên. Nó giúp phát hiện metric hoặc target bị đọc sai.

---
<!-- split -->
## Những số đã đo

Dữ liệu tự sinh, các hàng độc lập; 3-fold trên phần train.

Median MAE từng fold: 1.362, 1.345, 1.220.

Ridge: 0.352, 0.345, 0.252.

|||

Ridge thắng ở cả ba fold của thí nghiệm này.

Bằng chứng này thuộc giao thức đã chọn, chưa phải cho mọi dữ liệu tương lai.

Test để riêng, chưa dùng chọn cấu hình.

Trung bình MAE: median $=(1.362+1.345+1.220)/3=1.309$; Ridge $=(0.352+0.345+0.252)/3=0.316$.

---
<!-- figure -->
## MAE từng fold

![MAE của median baseline và Ridge trên đúng ba fold: Ridge thấp hơn ở mọi fold, không chỉ ở trung bình.](../fig/2-kt1-folds.svg)

---

<!-- figure -->
## Baseline và Ridge trên từng fold

![Ba fold của buổi kiểm tra: baseline trung vị đoán một hằng số cho mọi mẫu, Ridge đoán gần đường chéo; cả hai được chấm trên đúng cùng những mẫu.](../fig/2-kt1-folds.anim.webp)

---
<!-- quiz -->
::: quiz
MAE của baseline median cao hơn Ridge trên cả ba fold. Ta kết luận được gì?
- [x] Theo cách đánh giá này, Ridge tốt hơn
- [ ] Ridge chắc chắn thắng trên mọi dữ liệu tương lai
- [ ] Có thể xóa baseline khỏi nhật ký thí nghiệm
- [ ] Nên chia lại dữ liệu để Ridge thắng nhiều hơn
Ridge thắng trên cả ba fold, nên với cách đánh giá này nó tốt hơn thật. Đó vẫn chưa phải lời hứa cho mọi dữ liệu tương lai.
:::

---
<!-- center -->
## Dấu của metric trong sklearn

`neg_mean_absolute_error = −0.4`

MAE để báo = **0.4**.

Quy ước scoring của scikit-learn: score lớn hơn là tốt hơn.

Khi báo MAE, đổi dấu `neg_mean_absolute_error` một lần và ghi rõ metric gốc.

---
<!-- section 3 -->
# Fit và kiểm đầu ra

---
## Kiểm trước khi nộp

```python
predictions = selected.predict(X_test)
assert predictions.shape == (len(X_test),)
assert np.isfinite(predictions).all()
```

```output
test MAE: 0.318
3 hàng đầu: [(1000, 8.359), (1001, 4.14), (1002, 6.358)]
```

Ví dụ này có nhãn nên tính được test MAE; đề không cho nhãn test thì không tự tính được con số này. Hai `assert` chỉ kiểm shape và số hữu hạn; ID, thứ tự hàng và schema cần kiểm riêng theo đúng đề.

---
<!-- quiz -->
::: quiz
Cross-validation đã chọn Ridge. Trước khi chấm test, bước tiếp theo đúng quy trình là gì?
- [ ] Giữ lại mô hình của fold có MAE thấp nhất
- [ ] Fit trên train cộng test cho nhiều dữ liệu
- [ ] Chọn lại `alpha` theo MAE trên test
- [x] Fit lại cấu hình đã chọn trên toàn bộ train
CV chọn cấu hình, không chọn bộ trọng số của một fold.
:::

---
<!-- quiz -->
::: quiz
Một đoạn code tạo ra `pred` có shape `(30, 1)` và `y` có shape `(30,)`. Dòng nào vừa kiểm cùng số mẫu, vừa tính đúng MAE theo từng cặp?
- [ ] `np.abs(pred - y).mean()`, vì hai mảng cùng độ dài
- [ ] `np.abs(pred - y.T).mean()`, vì `.T` biến `y` thành cột
- [ ] `abs(pred.mean() - y.mean())`, để tránh broadcasting
- [x] `np.abs(pred.ravel() - y).mean()`, sau khi kiểm độ dài
Kiểm shape trước khi tính metric. Một con số loss trông hợp lý vẫn có thể được tính sai.
:::

---
<!-- figure -->
## Đọc phần dư để hỏi đúng

![Phần dư tốt nằm đều quanh 0; uốn cong báo thiếu quan hệ phi tuyến, loe dần báo nhiễu không đều.](../fig/2-1-residual-plots.svg)

---
<!-- quiz -->
::: quiz
Một mô hình cây có MAE 0.30 trên train và 1.30 trên validation. Baseline median có MAE 1.31 trên validation. Hiểu kết quả này thế nào?
- [ ] Mô hình tốt, vì MAE trên train rất thấp
- [x] Ngang baseline, cần kiểm overfit và cách đánh giá
- [ ] Metric bị đảo dấu, nên phải đọc ngược lại
- [ ] Chỉ cần thêm cây để MAE validation giảm xuống
Trên dữ liệu chưa thấy, mô hình gần như không hơn một hằng số. Train và validation cách xa nhau gợi ý mô hình đang học thuộc.
:::

---
<!-- split -->
## Khi điểm tăng quá đẹp

Feature mới có chứa target?

Có dùng tương lai?

Có sẵn lúc dự đoán thật?

|||

Scaler/PCA/encoder fit ở đâu?

ID có đổi thứ tự?

Test đã bị dùng chọn lại cấu hình chưa?

Nếu dùng scaler, PCA, encoder hoặc thống kê nhóm, chúng phải được fit trong train của fold. Một điểm cao không thay thế việc truy ngược thời điểm feature có sẵn.

---
<!-- section 4 -->
# Luyện đề

---
<!-- quiz -->
::: quiz Luyện đề
Bài phân loại 10 lớp. Loss trên train giảm đều tới 0.01, nhưng accuracy trên validation đứng yên ở 10%, đúng bằng mức đoán ngẫu nhiên. Giả thuyết nào khớp nhất?
- [ ] Overfitting cực mạnh, do thiếu regularization
- [x] Nhãn của train và validation được mã hóa lệch nhau
- [ ] Learning rate quá nhỏ nên mô hình chưa học được gì
- [ ] Rò rỉ dữ liệu trong train làm điểm train bị ảo
Đứng đúng ở mức ngẫu nhiên nghĩa là thứ mô hình học được không liên quan tới nhãn validation.
Đề thi: [NOAI 2026 Singapore · Vòng sơ loại · Câu 284](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=107)
:::

---
<!-- center -->
## Chốt quy trình

Đọc đề → xác định thông tin có lúc dự đoán → split có lý do → baseline → cùng fold → model chọn → kiểm file.

Mỗi bước có bằng chứng riêng: split, điểm từng fold, output và schema.

---
<!-- center -->
## Sau buổi ôn

Làm 10 câu cuối bài.

Chạy notebook từ đầu và giải thích từng lựa chọn: split, baseline, metric, output.

Trước khi chạy dài, kiểm shape, số hữu hạn, ID và schema theo hợp đồng.
