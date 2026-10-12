# Một bước ngược

Sinh ảnh bằng diffusion là đi ngược: từ $x_t$ về $x_{t-1}$, mỗi bước bớt một chút noise. Bài này làm đúng một bước ấy, có classifier-free guidance.

Mô hình cho hai dự đoán noise: không điều kiện $\varepsilon_u$ và có điều kiện $\varepsilon_c$. Với lịch `betas`, đặt $\alpha_s=1-\beta_s$, $\bar\alpha_t=\alpha_1\cdots\alpha_t$ và $\bar\alpha_0=1$.

1. Noise sau guidance: $\hat\varepsilon=\varepsilon_u+w(\varepsilon_c-\varepsilon_u)$ với $w$ là `guidance`.
2. Trung bình: $\mu=\dfrac{1}{\sqrt{\alpha_t}}\left(x_t-\dfrac{\beta_t}{\sqrt{1-\bar\alpha_t}}\hat\varepsilon\right)$.
3. Phương sai: $\sigma^2=\beta_t\cdot\dfrac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}$. Ở bước $t=1$ phương sai bằng $0$.
4. $x_{t-1}=\mu+\sigma z$ với $z$ cho sẵn.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `xt`, `epsilon_uncond`, `epsilon_cond`, `z` (cùng độ dài), `betas`, `t` (từ $1$) và `guidance`.

## Kết quả

Một đối tượng JSON gồm `guided_epsilon`, `mean`, `variance` và `xprev`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "xt": [
    1.289783100746931, -0.765081991960241, 1.4560578817097856,
    -0.8821181980482352, -0.4104847159477657
  ],
  "epsilon_uncond": [
    -1.4851507532066648, -0.5892784016791289, -0.2716929192408032,
    -0.010106959976554775, -0.47104944812554067
  ],
  "epsilon_cond": [
    -0.3558338500967358, 1.2623480500983235, -1.3931907823379561,
    -0.5073753688097151, -0.20623172431934741
  ],
  "z": [
    1.2782926762375186, 0.8102370279700551, -0.20118003061009954,
    0.00568157068009179, -0.7472016740350412
  ],
  "betas": [0.01, 0.02, 0.03, 0.04],
  "t": 1,
  "guidance": 0.0
}
```

```output
{
  "guided_epsilon": [
    -1.4851507532066648, -0.5892784016791289, -0.2716929192408032,
    -0.010106959976554775, -0.47104944812554067
  ],
  "mean": [
    1.4455440565662874, -0.7097116259535834, 1.4906993981220764,
    -0.8855463588694164, -0.3652104112911256
  ],
  "variance": 0.0,
  "xprev": [
    1.4455440565662874, -0.7097116259535834, 1.4906993981220764,
    -0.8855463588694164, -0.3652104112911256
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
