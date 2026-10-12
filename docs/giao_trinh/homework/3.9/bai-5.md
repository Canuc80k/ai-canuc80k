# Feature map

Muốn viết đúng $\exp\!\left(q\cdot k/\sqrt d\right)$ thành tích $\phi(q)\cdot\phi(k)$, feature map phải có vô hạn chiều, vì $e^x=\sum_{r\ge0}x^r/r!$. Cắt khai triển ở bậc hai, $e^x\approx1+x+\tfrac{x^2}{2}$, thì dựng được một feature map hữu hạn.

Với $x\in\mathbb R^d$, đặt $u=x/d^{1/4}$ để $u_q\cdot u_k=q\cdot k/\sqrt d$. Feature map gồm, theo đúng thứ tự:

- số $1$;
- $d$ thành phần $u_1,\dots,u_d$;
- $d^2$ thành phần $u_iu_j/\sqrt2$, với $i$ chạy ngoài và $j$ chạy trong, cả hai từ $1$ tới $d$.

Khi ấy $\phi(q)\cdot\phi(k)=1+s+\tfrac{s^2}{2}$ với $s=q\cdot k/\sqrt d$.

Hãy tính:

- `ell`: số chiều của feature map.
- `phi_q`: $\phi$ của từng query.
- `approx_output`: attention với trọng số tỉ lệ $\phi(q_i)\cdot\phi(k_j)$, chuẩn hóa để tổng trọng số của mỗi query bằng $1$.
- `exact_output`: softmax attention thật.
- `max_abs_error`: độ lệch tuyệt đối lớn nhất giữa hai bảng đầu ra.

## Dữ liệu vào

Một đối tượng JSON gồm `Q`, `K` ($T\times d$) và `V` ($T\times d_v$).

## Kết quả

Một đối tượng JSON gồm `ell`, `phi_q`, `approx_output`, `exact_output` và `max_abs_error`.

## Giới hạn

- $T\le6$, $d\le4$, $d_v\le3$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "Q": [[0.2, 0.1], [1.0, -0.5], [3.0, 3.0]],
  "K": [[0.1, 0.3], [-0.4, 0.2], [2.0, 2.5]],
  "V": [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
}
```

```output
{
  "ell": 7,
  "phi_q": [
    [
      1.0, 0.16817928305074292, 0.08408964152537146, 0.02, 0.01, 0.01,
      0.005
    ],
    [
      1.0, 0.8408964152537146, -0.4204482076268573, 0.5000000000000001,
      -0.25000000000000006, -0.25000000000000006, 0.12500000000000003
    ],
    [1.0, 2.5226892457611436, 2.5226892457611436, 4.5, 4.5, 4.5, 4.5]
  ],
  "approx_output": [
    [0.7307430288770644, 0.7089696260410803],
    [0.788068671554046, 0.7114438818983491],
    [0.9887130316530985, 0.9625563440265057]
  ],
  "exact_output": [
    [0.7321178216216426, 0.7104497095273141],
    [0.7914463413556287, 0.713312028996811],
    [0.9999532370521904, 0.9998330184408586]
  ],
  "max_abs_error": 0.037276674414352895
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 2, Ngày 1, câu 1.1.6](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-2-day-1-problems.pdf#page=4).
:::
