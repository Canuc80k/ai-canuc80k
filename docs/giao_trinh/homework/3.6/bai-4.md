# Weight decay

Weight decay kéo trọng số về $0$ một chút ở mỗi bước. Có hai cách cài nghe giống nhau:

- **Cộng vào gradient** (L2): dùng $g+\lambda w$ thay cho gradient $g$ của loss, rồi cho optimizer xử lý như thường.
- **Tách riêng**: trước bước cập nhật, nhân trọng số với $1-\eta\lambda$, còn optimizer chỉ thấy $g$.

Bài này cho thấy hai cách có trùng nhau hay không, tùy optimizer. Loss là $f(w)=\tfrac12\sum_i a_i(w_i-c_i)^2$, gradient $g_i=a_i(w_i-c_i)$. Chạy đúng `steps` bước từ `initial` với bốn cấu hình:

- `sgd_l2`: $w\leftarrow w-\eta(g+\lambda w)$.
- `sgd_decoupled`: $w\leftarrow w(1-\eta\lambda)-\eta g$.
- `adam_l2`: Adam với gradient $g+\lambda w$.
- `adamw`: nhân $w$ với $1-\eta\lambda$, rồi bước Adam với gradient $g$. Gradient $g$ tính tại $w$ **trước** khi nhân.

Adam dùng $\beta_1=0.9$, $\beta_2=0.999$, $\varepsilon=10^{-8}$: ở bước $t=1,2,\dots$, $m\leftarrow\beta_1m+(1-\beta_1)g$, $s\leftarrow\beta_2s+(1-\beta_2)g^2$, $w\leftarrow w-\eta\,\dfrac{m/(1-\beta_1^t)}{\sqrt{s/(1-\beta_2^t)}+\varepsilon}$, với $m$, $s$ ban đầu bằng $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `a`, `center` ($c$), `initial`, `lr` ($\eta$), `weight_decay` ($\lambda$) và `steps`.

## Kết quả

Một đối tượng JSON gồm bốn trường `sgd_l2`, `sgd_decoupled`, `adam_l2`, `adamw`. Mỗi trường là `{"weights": [...], "loss": ..., "norm": ...}`: trọng số sau cùng, $f$ tại đó (không tính phần weight decay), và độ dài $\lVert w\rVert$.

## Giới hạn

- Không quá $4$ trọng số và $200$ bước.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "a": [10.0, 0.1],
  "center": [1.0, 1.0],
  "initial": [0.0, 0.0],
  "lr": 0.01,
  "weight_decay": 0.5,
  "steps": 200
}
```

```output
{
  "sgd_l2": {
    "weights": [0.9523809521604477, 0.11664874649544177],
    "loss": 0.05035334043913156,
    "norm": 0.9594979979640389
  },
  "sgd_decoupled": {
    "weights": [0.9523809521604477, 0.1166487464954417],
    "loss": 0.050353340439131575,
    "norm": 0.9594979979640389
  },
  "adam_l2": {
    "weights": [0.9427362858401772, 0.16667081388698546],
    "loss": 0.051117541418278414,
    "norm": 0.9573561849392745
  },
  "adamw": {
    "weights": [0.7852804554763412, 0.785280403756612],
    "loss": 0.23282763925278369,
    "norm": 1.1105542338297925
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
