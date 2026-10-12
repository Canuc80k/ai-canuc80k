# Hậu nghiệm diffusion

Bài này làm toán của diffusion trên dữ liệu một chiều, từ quá trình thêm noise tới loss mà mô hình học.

Quá trình thuận: $x_t=\sqrt{\alpha_t}\,x_{t-1}+\sqrt{1-\alpha_t}\,\epsilon_t$ với các $\epsilon_t\sim\mathcal N(0,1)$ độc lập. Đặt $\bar\alpha_t=\alpha_1\alpha_2\cdots\alpha_t$ và $\bar\alpha_0=1$.

1. Gộp các bước lại, $x_t\mid x_0\sim\mathcal N\big(\sqrt{\bar\alpha_t}\,x_0,\ 1-\bar\alpha_t\big)$. Viết $x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\bar\epsilon$; từ $x_0$ và $x_t$ suy ra $\bar\epsilon$.
2. Biết cả $x_t$ và $x_0$, phân phối của bước trước là Gaussian: $x_{t-1}\mid x_t,x_0\sim\mathcal N(\tilde\mu,\tilde\beta)$ với
$$\tilde\beta=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}(1-\alpha_t),\qquad \tilde\mu=\frac{1}{\sqrt{\alpha_t}}\left(x_t-\frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}}\,\bar\epsilon\right).$$
3. Mô hình không biết $x_0$, nên đoán noise $\epsilon_\theta$ (cho sẵn là `eps_model`) và dùng cùng công thức với $\bar\epsilon$ thay bằng $\epsilon_\theta$ để có trung bình $\mu_\theta$. Phương sai của mô hình lấy bằng $\tilde\beta$.
4. KL giữa hai Gaussian cùng phương sai: $D_{\mathrm{KL}}\big(\mathcal N(\tilde\mu,\tilde\beta)\,\|\,\mathcal N(\mu_\theta,\tilde\beta)\big)=\dfrac{(\tilde\mu-\mu_\theta)^2}{2\tilde\beta}$.

Với mỗi truy vấn $(t, x_0, x_t, \epsilon_\theta)$, hãy tính các đại lượng trên.

## Dữ liệu vào

Một đối tượng JSON gồm `alphas` ($[\alpha_1,\dots,\alpha_T]$) và `queries`: mỗi truy vấn là `{"t", "x0", "xt", "eps_model"}`.

## Kết quả

Một đối tượng JSON gồm `queries`: với mỗi truy vấn là `{"alpha_bar", "forward_mean", "forward_var", "eps_bar", "posterior_mean", "posterior_var", "model_mean", "kl"}`, theo thứ tự các bước 1–4.

## Giới hạn

- $T\le12$, không quá $5$ truy vấn, $2\le t\le T$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "alphas": [0.9, 0.8, 0.7, 0.6],
  "queries": [
    {"t": 2, "x0": 1.0, "xt": 0.5, "eps_model": 0.0},
    {"t": 4, "x0": 1.0, "xt": 0.5, "eps_model": 0.0},
    {"t": 4, "x0": -2.0, "xt": 0.3, "eps_model": 1.5}
  ]
}
```

```output
{
  "queries": [
    {
      "alpha_bar": 0.7200000000000001,
      "forward_mean": 0.8485281374238571,
      "forward_var": 0.2799999999999999,
      "eps_bar": -0.6586562689514786,
      "posterior_mean": 0.8373500684289235,
      "posterior_var": 0.07142857142857141,
      "model_mean": 0.5590169943749475,
      "kl": 0.542285100786353
    },
    {
      "alpha_bar": 0.3024,
      "forward_mean": 0.5499090833947008,
      "forward_var": 0.6976,
      "eps_bar": -0.05975528993342364,
      "posterior_mean": 0.6824423789573817,
      "posterior_var": 0.28440366972477066,
      "model_mean": 0.6454972243679028,
      "kl": 0.0023996603998840405
    },
    {
      "alpha_bar": 0.3024,
      "forward_mean": -1.0998181667894016,
      "forward_var": 0.6976,
      "eps_bar": 1.6759782933512184,
      "posterior_mean": -0.648915818225961,
      "posterior_var": 0.28440366972477066,
      "model_mean": -0.5401129781845669,
      "kl": 0.02081206971156413
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 2, Ngày 2, Bài 3](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-2-day-2-problems.pdf#page=2).
:::
