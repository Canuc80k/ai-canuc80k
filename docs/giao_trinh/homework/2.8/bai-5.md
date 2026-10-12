# Bốn loss

Một mô hình phân loại nhị phân cho ra logit $z$, rồi đưa qua sigmoid $p=\sigma(z)=\frac{1}{1+e^{-z}}$. Nhãn thật $y$ là $0$ hoặc $1$. Có bốn ứng viên cho hàm loss:

| Loss | Công thức |
|---|---|
| BCE | $-\big[y\ln p+(1-y)\ln(1-p)\big]$ |
| MSE | $(y-p)^2$ |
| Hinge | $\max(0,\,1-s\,z)$ với $s=2y-1$ |
| MAE | $\lvert y-p\rvert$ |

Hinge dùng thẳng logit $z$ và nhãn $s\in\{-1,1\}$, không qua sigmoid.

Điều quyết định mô hình học nhanh hay chậm là đạo hàm của loss theo $z$. Với từng mẫu, hãy tính giá trị loss và đạo hàm theo $z$ của cả bốn loss. Riêng hinge, khi $s\,z<1$ đạo hàm là $-s$, còn lại là $0$.

Làm xong, hãy nhìn vào những mẫu bị đoán sai mà rất tự tin. Loss nào vẫn cho đạo hàm đủ lớn để sửa chúng?

## Dữ liệu vào

Một đối tượng JSON gồm `z` (các logit) và `y` (các nhãn $0$ hoặc $1$).

## Kết quả

Một đối tượng JSON gồm bốn trường `bce`, `mse`, `hinge`, `mae`. Mỗi trường là `{"loss": [...], "grad": [...], "mean_loss": ...}`, trong đó `mean_loss` là trung bình loss trên các mẫu.

## Giới hạn

- Từ $1$ đến $30$ mẫu. Mỗi logit có $\lvert z\rvert\le10$ và $\lvert z\rvert\ne1$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"z": [3.0, -4.0, 0.5, -0.5], "y": [1, 1, 0, 1]}
```

```output
{
  "bce": {
    "loss": [
      0.04858735157374206, 4.0181499279178094, 0.9740769841801067,
      0.9740769841801067
    ],
    "grad": [
      -0.04742587317756678, -0.9820137900379085, 0.6224593312018546,
      -0.6224593312018546
    ],
    "mean_loss": 1.5037228119629413
  },
  "mse": {
    "loss": [
      0.002249213446654648, 0.9643510838246173, 0.3874556190002601,
      0.3874556190002601
    ],
    "grad": [
      -0.004285085069968654, -0.03469004214168025, 0.29256050705391523,
      -0.29256050705391523
    ],
    "mean_loss": 0.435377883817948
  },
  "hinge": {
    "loss": [0.0, 5.0, 1.5, 1.5],
    "grad": [0.0, -1.0, 1.0, -1.0],
    "mean_loss": 2.0
  },
  "mae": {
    "loss": [
      0.04742587317756678, 0.9820137900379085, 0.6224593312018546,
      0.6224593312018546
    ],
    "grad": [
      -0.04517665973091213, -0.017662706213291118, 0.2350037122015945,
      -0.2350037122015945
    ],
    "mean_loss": 0.5685895814047961
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 273](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=99).
:::
