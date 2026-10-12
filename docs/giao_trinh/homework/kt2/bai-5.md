# Ba cách viết loss

Phân loại nhiều nhãn: mỗi mẫu có thể mang nhiều nhãn cùng lúc, nhãn là ma trận $0$/$1$ cùng cỡ với logits. Có ba cách viết loss hay gặp, với $z$ là logits, $t$ là nhãn:

```python
# Cách A
p = torch.sigmoid(z)
loss_a = (-t * torch.log(p) - (1 - t) * torch.log(1 - p)).mean()

# Cách B
loss_b = F.binary_cross_entropy_with_logits(z, t, reduction="mean")

# Cách C
q = torch.softmax(z, dim=1)
loss_c = (-t * torch.log(q)).sum(dim=1).mean()
```

Hãy chạy đúng ba đoạn code này với tensor kiểu `float64`. Giá trị nào là vô cùng hay `nan` thì ghi `null`. Thêm `a_matches_b`: cách A cho một số hữu hạn và lệch cách B không quá $10^{-9}\cdot\max(1,|B|)$.

Trước khi chạy, hãy đoán: cách nào đúng cho bài nhiều nhãn, và cách nào sẽ hỏng khi có một logit bằng $1000$?

## Dữ liệu vào

Mỗi tệp `input.json` gồm `logits` và `targets`.

## Kết quả

Một đối tượng JSON gồm `option_a`, `option_b`, `option_c` (số hoặc `null`) và `a_matches_b`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [[2.0, -1.0, 0.5], [1.5, -0.5, 3.0]],
  "targets": [[1, 0, 1], [1, 0, 0]]
}
```

```output
{
  "option_a": 0.7730573827463177,
  "option_b": 0.7730573827463173,
  "option_c": 1.8542123212729567,
  "a_matches_b": true
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 7](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=11).
:::
