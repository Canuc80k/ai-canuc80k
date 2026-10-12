# Parabol

Gradient descent tìm cực tiểu của $f(x)=ax^2$, với $a>0$. Bắt đầu từ $x_0$, mỗi bước đi ngược hướng đạo hàm:

$$
x_{t+1}=x_t-\eta\,f'(x_t)=x_t-2a\eta\,x_t.
$$

Cực tiểu nằm ở $x=0$, nhưng gradient descent có đến được đó hay không còn tùy bước học $\eta$. Hãy chạy đúng `steps` bước, ghi lại $x_t$, $f(x_t)$ và $f'(x_t)$ từ $t=0$, rồi cho biết dãy $x_t$ thuộc loại nào:

- `"converge"` nếu dãy tiến dần về $0$,
- `"oscillate"` nếu dãy nhảy qua lại giữa hai giá trị mãi không đổi,
- `"diverge"` nếu dãy ngày càng xa $0$.

Gợi ý: viết $x_{t+1}$ theo dạng một số nhân với $x_t$.

## Dữ liệu vào

Một đối tượng JSON gồm `a`, `x0`, `eta` và `steps`.

## Kết quả

Một đối tượng JSON gồm `x`, `f`, `grad` (mỗi trường `steps` cộng $1$ số) và `kind`.

## Giới hạn

- $x_0\ne0$, $1\le\text{steps}\le20$. Các số $a$, $\eta$ đều dương và là bội của $\frac1{16}$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số tương đối khoảng $10^{-8}$.

## Ví dụ

```input
{"a": 1, "x0": -1, "eta": 1.5, "steps": 2}
```

```output
{
  "x": [-1.0, 2.0, -4.0],
  "f": [1.0, 4.0, 16.0],
  "grad": [-2.0, 4.0, -8.0],
  "kind": "diverge"
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
