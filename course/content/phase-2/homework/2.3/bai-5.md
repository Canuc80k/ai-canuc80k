# Tách được

Khi hai lớp tách được hoàn toàn bằng một ngưỡng, logistic regression gặp chuyện lạ: loss cứ giảm mãi mà không bao giờ chạm đáy, và trọng số cứ lớn dần lên. Bài này cho ta thấy điều đó bằng số.

Dữ liệu có một feature $x$ và nhãn $y\in\{0,1\}$. Mô hình là $p=\sigma(wx+b)$, loss là binary cross-entropy trung bình cộng phạt $\frac\lambda2w^2$ (không phạt $b$). Bắt đầu từ $w=b=0$, chạy gradient descent đúng `steps` bước với tốc độ học $\eta$:

$$
w\leftarrow w-\eta\left(\frac1n\sum_i(p_i-y_i)x_i+\lambda w\right),\qquad
b\leftarrow b-\eta\,\frac1n\sum_i(p_i-y_i).
$$

Cả hai gradient tính từ tham số cũ. Ghi lại $w$ sau các bước có số thứ tự nằm trong `report_at`, rồi báo $w$, $b$ và loss (chưa cộng phạt) sau bước cuối.

So hai test đầu: cùng dữ liệu, một test không phạt, một test có phạt. Trọng số của test nào dừng lại?

## Dữ liệu vào

Một đối tượng JSON gồm `x`, `y`, `lam`, `eta`, `steps` và `report_at`.

## Kết quả

Một đối tượng JSON gồm `w`, `b`, `loss` và `w_history`.

## Giới hạn

- Từ $2$ đến $20$ điểm, $\text{steps}\le2000$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [-2, -1, 1, 2],
  "y": [0, 0, 1, 1],
  "lam": 0,
  "eta": 1,
  "steps": 1000,
  "report_at": [10, 100, 1000]
}
```

```output
{
  "w": 6.2311949021186255,
  "b": -4.440892098500626e-16,
  "loss": 0.000984518633509979,
  "w_history": [2.1029996275185914, 4.01803948294775, 6.2311949021186255]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
