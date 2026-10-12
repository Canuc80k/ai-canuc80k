# BCE nhiều nhãn

Một ảnh có thể đồng thời mang nhiều nhãn, như "có người" và "có xe". Khi ấy mỗi nhãn là một bài phân loại nhị phân riêng, dùng sigmoid cho từng logit chứ không softmax qua các nhãn.

Cho logits shape `(B, 3)`, nhãn $0$/$1$ cùng shape, và `pos_weight` cho ba nhãn. Hãy tính `BCEWithLogitsLoss(pos_weight=..., reduction="mean")` và gradient của loss theo từng logit.

Với logit $x$, nhãn $y$ và trọng số $w$ của nhãn ấy, mỗi ô đóng góp $-\big[w\,y\ln\sigma(x)+(1-y)\ln(1-\sigma(x))\big]$. Trung bình chia cho **tổng số ô** $B\times3$, không chia cho tổng trọng số. Logits có thể bằng $\pm1000$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `logits`, `targets` và `pos_weight`.

## Kết quả

Một đối tượng JSON gồm `loss` và `gradient` (shape `(B, 3)`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [
    [-1000.0, 0.0, 1000.0],
    [1.9178324220449117, -1.673788956075862, 1.880645293232226],
    [-2.4927361270988655, 1.7557553130078078, -1.7132635197555115],
    [0.289592770611119, 4.734997017000433, -2.032724506762987]
  ],
  "targets": [[0, 1, 1], [1, 0, 0], [0, 0, 0], [1, 0, 1]],
  "pos_weight": [1.0, 2.0, 3.0]
}
```

```output
{
  "loss": 1.4706759917484824,
  "gradient": [
    [0.0, -0.08333333333333333, 0.0],
    [-0.010675289537288116, 0.013159972183050225, 0.07230710238223727],
    [0.006364081331641669, 0.0710564371422359, 0.012728408435745334],
    [-0.03567529720725133, 0.0826078321105531, -0.2210475883768066]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
