# Linear attention

Softmax attention trên $T$ token phải tính mọi cặp query–key, tốn thời gian cỡ $T^2$. Linear attention thay $\exp(q\cdot k/\sqrt d)$ bằng tích $\phi(q)\cdot\phi(k)$ của một feature map, rồi đổi thứ tự nhân để chỉ còn tỉ lệ với $T$.

Với $Q$, $K$ cỡ $T\times d$ và $V$ cỡ $T\times d_v$, hãy tính:

1. `softmax_output`: softmax attention thông thường, hàng $i$ là $\sum_j\operatorname{softmax}_j\!\left(q_i\cdot k_j/\sqrt d\right)v_j$.
2. Feature map $\phi(x)=1+\operatorname{ELU}(x)$ áp cho từng thành phần, với $\operatorname{ELU}(x)=x$ khi $x\ge0$ và $e^x-1$ khi $x<0$. Nhờ vậy $\phi(x)>0$.
3. `kv`: ma trận $\sum_j\phi(k_j)\,v_j^\top$, cỡ $d\times d_v$.
4. `z`: vector $\sum_j\phi(k_j)$, cỡ $d$.
5. `linear_output`: hàng $i$ là $\dfrac{\phi(q_i)^\top\,\text{kv}}{\phi(q_i)\cdot z}$.

Bước 3 và 4 chỉ làm một lần cho mọi query, nên tổng chi phí tỉ lệ với $T$ chứ không với $T^2$.

## Dữ liệu vào

Một đối tượng JSON gồm `Q`, `K` và `V`.

## Kết quả

Một đối tượng JSON gồm `softmax_output`, `kv`, `z` và `linear_output`.

## Giới hạn

- $T\le8$, $d\le4$, $d_v\le4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "Q": [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]],
  "K": [[1.0, 0.0], [0.0, 1.0], [-2.0, 0.5]],
  "V": [[1.0, 0.0], [0.0, 1.0], [2.0, 2.0]]
}
```

```output
{
  "softmax_output": [
    [0.768624380277045, 0.45433451307101336],
    [0.8643386753676013, 1.0952598222316001],
    [1.6182117134137801, 1.6182117134137801]
  ],
  "kv": [[2.2706705664732256, 1.2706705664732254], [4.0, 5.0]],
  "z": [3.135335283236613, 4.5],
  "linear_output": [
    [0.7930185108004142, 0.7001737808619846],
    [0.846344194598465, 0.9287481806985747],
    [0.8212698373888688, 0.8212698373888688]
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 2, Ngày 1, Bài 1](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-2-day-1-problems.pdf#page=3).
:::
