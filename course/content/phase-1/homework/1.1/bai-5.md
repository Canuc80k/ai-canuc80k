# Đặt ghế

Trở lại chuyện đặt ghế của câu lạc bộ trong bài học. Phòng được thuê theo số ghế, mỗi ghế tốn $\alpha$ đồng, dù có người ngồi hay không. Mỗi người đến mà hết ghế phải ra về, câu lạc bộ mất $\beta$ đồng. Thiếu ghế đắt hơn thừa ghế, tức $\alpha<\beta$.

Thuê $g$ ghế cho một buổi có $a$ người đến thì tốn

$$
L(g,a)=\alpha g+\beta\max(0,\,a-g).
$$

Câu lạc bộ biết số người đến của $n$ buổi trước, $a_1, \dots, a_n$. Hãy chọn một số ghế nguyên $g\ge0$ dùng cho mọi buổi, sao cho chi phí trung bình trên các buổi ấy nhỏ nhất:

$$
\bar L(g)=\frac1n\sum_{i=1}^{n}L(g,a_i).
$$

Nếu nhiều $g$ cùng cho chi phí nhỏ nhất, chọn $g$ nhỏ nhất.

## Dữ liệu vào

Một đối tượng JSON gồm `attendance` (số người đến của các buổi trước), `seat_cost` là $\alpha$ và `turn_away_cost` là $\beta$.

## Kết quả

Một đối tượng JSON gồm `seats` là số ghế $g$ và `average_cost` là $\bar L(g)$.

## Giới hạn

- Từ $1$ đến $1000$ buổi, mỗi buổi từ $0$ đến $1000$ người.
- $\alpha$, $\beta$ là số nguyên, $1\le\alpha<\beta\le100$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. `average_cost` được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "attendance": [20, 22, 25, 30, 48],
  "seat_cost": 1,
  "turn_away_cost": 4
}
```

```output
{"seats": 30, "average_cost": 44.4}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
