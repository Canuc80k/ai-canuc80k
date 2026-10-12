# Softmax ổn định

Softmax biến logits thành xác suất: $p_i=\dfrac{e^{z_i}}{\sum_j e^{z_j}}$. Cross-entropy với nhãn $y$ là $-\ln p_y$. Viết thẳng theo công thức thì $e^{1000}$ tràn số và kết quả thành `nan`. Bài này yêu cầu tính đúng cả khi logits rất lớn.

Với mỗi hàng logits và nhãn của nó, hãy tính:

- `probabilities`: xác suất softmax của từng lớp.
- `log_probabilities`: $\ln p_i$ của từng lớp. Kể cả khi $p_i$ nhỏ tới mức làm tròn về $0$, $\ln p_i$ vẫn là một số hữu hạn, chẳng hạn $-2000$.
- `losses`: cross-entropy $-\ln p_y$ của hàng ấy.

Thêm `mean_loss` là trung bình `losses`, và `log_C` là $\ln C$ với $C$ là số lớp. Một mô hình vừa khởi tạo cho logits gần bằng nhau thì loss ở batch đầu nằm gần $\ln C$; đó là mốc để kiểm nhanh.

## Dữ liệu vào

Một đối tượng JSON gồm `logits` (mỗi hàng $C$ số) và `labels` (nhãn của từng hàng, đánh từ $0$).

## Kết quả

Một đối tượng JSON gồm `probabilities`, `log_probabilities`, `losses`, `mean_loss` và `log_C`.

## Giới hạn

- $2\le C\le10$, không quá $8$ hàng, mỗi logit có trị tuyệt đối không quá $5000$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [
    [1000.0, 0.0, -1000.0],
    [2.0, 1.0, 0.1],
    [0.0, 0.0, 0.0],
    [-5.0, 800.0, 790.0]
  ],
  "labels": [2, 0, 1, 2]
}
```

```output
{
  "probabilities": [
    [1.0, 0.0, 0.0],
    [0.6590011388859679, 0.24243297070471392, 0.09856589040931817],
    [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
    [0.0, 0.9999546021312976, 4.5397868702434395e-05]
  ],
  "log_probabilities": [
    [0.0, -1000.0, -2000.0],
    [-0.4170300162778335, -1.4170300162778335, -2.3170300162778337],
    [-1.0986122886681098, -1.0986122886681098, -1.0986122886681098],
    [-805.0000453988993, -4.539889921686465e-05, -10.000045398899218]
  ],
  "losses": [2000.0, 0.4170300162778335, 1.0986122886681098, 10.000045398899218],
  "mean_loss": 502.87892192596127,
  "log_C": 1.0986122886681098
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
