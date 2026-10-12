# CTC forward

Vét cạn mọi đường CTC chỉ làm được với vài khung. Với $30$ khung, phải dùng quy hoạch động: thuật toán forward. Bài này tính log-xác suất của một văn bản bằng forward, và tìm đường đi đơn lẻ tốt nhất bằng Viterbi.

Softmax từng khung của `logits` ($T\times V$) để có log-xác suất $\ell_t(k)$. Blank là `blank_id`.

1. **Chuỗi mở rộng:** chèn blank vào đầu, cuối và giữa mọi ký tự của `target`: với target $[c_1,\dots,c_L]$ được $z=[\text{b},c_1,\text{b},c_2,\dots,c_L,\text{b}]$, dài $2L+1$.
2. **Chuyển trạng thái:** ở khung $t$ đang ở vị trí $s$ của $z$, khung trước có thể ở $s$ hoặc $s-1$; thêm $s-2$ nếu $z_s$ không phải blank và $z_s\ne z_{s-2}$.
3. **Forward:** $\alpha_0(0)=\ell_0(z_0)$, $\alpha_0(1)=\ell_0(z_1)$, các vị trí khác $-\infty$. $\alpha_t(s)=\ell_t(z_s)+\log\sum_{s'}e^{\alpha_{t-1}(s')}$ trên các $s'$ được phép. Log-xác suất của target là $\log\big(e^{\alpha_{T-1}(2L)}+e^{\alpha_{T-1}(2L-1)}\big)$ (chỉ vị trí cuối nếu $L=0$).
4. **Viterbi:** như forward nhưng thay tổng bằng max, nhớ vị trí trước đó. Đường tốt nhất kết thúc ở vị trí cuối hoặc kề cuối, cái nào lớn hơn. `viterbi_path` là ký hiệu ($z_s$) ở mỗi khung, chưa gộp.
5. Nếu target không thể đạt được (quá ít khung), cả ba kết quả là `null`.

## Dữ liệu vào

Một đối tượng JSON gồm `logits`, `blank_id` và `target`.

## Kết quả

Một đối tượng JSON gồm `log_likelihood`, `viterbi_logprob` và `viterbi_path`.

## Giới hạn

- $T\le30$, $V\le6$. Đường Viterbi tốt nhất là duy nhất.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [
    [2.0, 1.0, 0.0],
    [0.5, 2.0, 0.0],
    [1.5, 0.5, 0.2],
    [0.0, 2.5, 0.3],
    [2.0, 0.0, 1.0]
  ],
  "blank_id": 0,
  "target": [1, 1]
}
```

```output
{
  "log_likelihood": -1.2589935438145874,
  "viterbi_logprob": -1.7928919934233047,
  "viterbi_path": [0, 1, 0, 1, 0]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
