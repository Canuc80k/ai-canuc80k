# Khởi tạo

Xét một lớp $z=\sum_{c=1}^{n}w_c\,a_c$ với $n$ đầu vào (fan-in). Các trọng số độc lập, trung bình $0$, độ lệch chuẩn $\sigma_w$, và độc lập với đầu vào. Khi ấy

$$
\operatorname{Var}(z)=n\,\sigma_w^2\,\mathbb E[a^2].
$$

Đầu vào của mạng có trung bình $0$ và phương sai $\sigma^2$, nên ở lớp đầu $\mathbb E[a^2]=\sigma^2$. Ở các lớp sau, $a$ là đầu ra activation của lớp trước:

- Lớp trước `linear` thì $\mathbb E[a^2]$ bằng phương sai pre-activation của lớp trước.
- Lớp trước `relu` thì $\mathbb E[a^2]$ bằng **một nửa** phương sai ấy, vì nửa âm bị đặt về $0$.

Cho cấu hình từng lớp, hãy tính:

- `variances`: phương sai pre-activation $\operatorname{Var}(z)$ của từng lớp.
- `preserving_sigma`: với từng lớp, độ lệch chuẩn $\sigma_w$ làm $\operatorname{Var}(z)$ của lớp ấy đúng bằng phương sai đầu vào của nó. Ở lớp đầu, phương sai đầu vào là $\sigma^2$. Ở các lớp sau, đó là phương sai pre-activation của lớp trước.
- `first_bad`: số thứ tự (đánh từ $1$) của lớp đầu tiên có phương sai nhỏ hơn $10^{-6}\sigma^2$ hoặc lớn hơn $10^{6}\sigma^2$, hoặc `null` nếu không có.

## Dữ liệu vào

Một đối tượng JSON gồm `input_variance` ($\sigma^2$) và `layers`, mỗi lớp là `{"fan_in": n, "sigma_w": ..., "activation": "relu" | "linear"}`.

## Kết quả

Một đối tượng JSON gồm `variances`, `preserving_sigma` và `first_bad`.

## Giới hạn

- Không quá $12$ lớp, fan-in không quá $1000$. Không phương sai nào sát đúng hai ngưỡng $10^{\pm6}\sigma^2$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "input_variance": 1.0,
  "layers": [
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"},
    {"fan_in": 256, "sigma_w": 0.01, "activation": "relu"}
  ]
}
```

```output
{
  "variances": [
    0.0256, 0.00032768, 4.194304e-06, 5.36870912e-08, 6.8719476736e-10,
    8.796093022208e-12, 1.125899906842624e-13, 1.4411518807585588e-15,
    1.844674407370955e-17, 2.3611832414348224e-19
  ],
  "preserving_sigma": [
    0.0625, 0.08838834764831845, 0.08838834764831845,
    0.08838834764831845, 0.08838834764831845, 0.08838834764831845,
    0.08838834764831845, 0.08838834764831845, 0.08838834764831845,
    0.08838834764831845
  ],
  "first_bad": 4
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 7.2](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=18).
:::
