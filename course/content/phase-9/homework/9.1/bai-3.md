# Policy gradient

Policy gradient học thẳng xác suất chọn hành động. Bài này làm trên bài toán một bước: chọn một trong $K$ hành động, nhận phần thưởng, kết thúc.

Policy là softmax của tham số $\theta$: $\pi_k=e^{\theta_k}/\sum_j e^{\theta_j}$.

1. Có $n$ mẫu, mỗi mẫu là (hành động $a$, phần thưởng $r$). Baseline $b$ là trung bình phần thưởng của các mẫu nếu `baseline` là `true`, ngược lại $b=0$.
2. Ước lượng gradient (REINFORCE): $g_k=\frac1n\sum_{\text{mẫu}}(r-b)\big([k=a]-\pi_k\big)$. (Đây là đạo hàm của $\log\pi_a$ theo $\theta_k$, nhân $r-b$.)
3. Cập nhật một bước: $\theta\leftarrow\theta+\text{lr}\cdot g$.

## Dữ liệu vào

Một đối tượng JSON gồm `theta`, `samples` (mỗi mẫu là `{"action", "reward"}`), `baseline` và `lr`.

## Kết quả

Một đối tượng JSON gồm `policy`, `baseline`, `gradient` và `new_theta`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "theta": [0.0, 0.0, 0.0],
  "samples": [
    {"action": 0, "reward": 1},
    {"action": 1, "reward": 3},
    {"action": 0, "reward": 1}
  ],
  "baseline": true,
  "lr": 0.5
}
```

```output
{
  "policy": [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
  "baseline": 1.6666666666666667,
  "gradient": [-0.4444444444444445, 0.4444444444444444, 1.850371707708594e-17],
  "new_theta": [-0.22222222222222224, 0.2222222222222222, 9.25185853854297e-18]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
