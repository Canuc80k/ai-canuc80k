# Sigmoid

Cho các logit $z_i$ và nhãn $y_i\in\{0,1\}$. Hãy tính xác suất $p_i=\sigma(z_i)=\frac{1}{1+e^{-z_i}}$, binary cross-entropy trung bình

$$
L=\frac1n\sum_i\Big[-y_i\ln p_i-(1-y_i)\ln(1-p_i)\Big],
$$

và gradient của $L$ theo từng logit, $\frac{\partial L}{\partial z_i}=\frac{p_i-y_i}{n}$.

Một số logit lớn tới $\pm1000$. Tính thẳng theo công thức thì $e^{1000}$ tràn số, còn $\ln 0$ ra vô cùng. Hãy viết loss trực tiếp theo logit, như mục Sigmoid ổn định của bài học:

$$
-y\ln p-(1-y)\ln(1-p)=\max(z,0)-yz+\ln\!\left(1+e^{-|z|}\right).
$$

## Dữ liệu vào

Mỗi tệp `input.json` gồm `logits` và `y`.

## Kết quả

Một đối tượng JSON gồm `probabilities`, `loss` và `gradient`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [
    -1000.0, 1000.0, 0.0, -1.0, 1.0, -0.2568641432313081,
    -0.4608150955572951, 1.7755447707971468, 0.9563451020729434,
    -0.04847904283059711, -1.0988288739250234, -0.2774860384352499
  ],
  "y": [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
}
```

```output
{
  "probabilities": [
    0.0, 1.0, 0.5, 0.2689414213699951, 0.7310585786300049,
    0.4361347268953331, 0.3867924783592652, 0.855145863098891,
    0.7223894372469798, 0.4878826124075225, 0.24995939246323587,
    0.43107021468254947
  ],
  "loss": 84.21001883347866,
  "gradient": [
    0.0, 0.08333333333333333, -0.041666666666666664,
    -0.06092154821916707, 0.06092154821916707, -0.04698877275872224,
    0.032232706529938766, 0.07126215525824091, 0.06019911977058165,
    -0.04267644896603979, -0.06250338396139701, 0.03592251789021245
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
