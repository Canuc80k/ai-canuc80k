# Phép chiếu

Giả sử thành phần chính đầu tiên của dữ liệu cùng hướng với một vector nguyên $v$. Vector đơn vị theo hướng ấy là $\hat e=\frac{v}{\lVert v\rVert}$. Với một điểm $x$, ta cần ba thứ:

- Hình chiếu của $x$ lên $\hat e$, tức tích vô hướng $x\cdot\hat e$. Đây là tọa độ của $x$ sau khi nén còn một chiều.
- Phần dư $r=x-(x\cdot\hat e)\,\hat e$, tức phần của $x$ bị mất khi nén.
- Bình phương độ dài của phần dư, $\lVert r\rVert^2$.

Mọi số liệu đều nguyên, nên đáp số viết được ở dạng chính xác. Hãy viết chúng theo đúng các dạng sau:

1. $\hat e=\frac{1}{\sqrt a}\,(u_1,\dots,u_d)$, với $a$ nguyên dương, các $u_i$ nguyên, và ước chung lớn nhất của $a,u_1^2,\dots,u_d^2$ bằng $1$.
2. $x\cdot\hat e=\frac{b}{c}\sqrt f$, với $c$ nguyên dương, $b$ nguyên, $\gcd(b,c)=1$, và $f$ nguyên dương không chia hết cho số chính phương nào lớn hơn $1$. Nếu hình chiếu bằng $0$ thì ghi $b=0$, $c=1$, $f=1$.
3. $r=\frac{1}{a'}\,(r_1,\dots,r_d)$, với $a'$ nguyên dương, các $r_i$ nguyên, và ước chung lớn nhất của $a',r_1,\dots,r_d$ bằng $1$.
4. $\lVert r\rVert^2$ là phân số tối giản, mẫu dương.

## Dữ liệu vào

Một đối tượng JSON gồm `v` và `x`, hai vector nguyên cùng số chiều.

## Kết quả

Một đối tượng JSON gồm:

- `direction`: `{"a": a, "u": [u1, ..., ud]}`.
- `projection`: `{"num": b, "den": c, "root": f}`.
- `residual`: `{"den": a', "num": [r1, ..., rd]}`.
- `residual_sq`: `[tử, mẫu]`.

## Giới hạn

- Từ $2$ đến $5$ chiều. Mọi tọa độ có trị tuyệt đối không quá $20$, và $v$ khác vector $0$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"v": [1, -2, 3], "x": [-1, -4, 6]}
```

```output
{
  "direction": {"a": 14, "u": [1, -2, 3]},
  "projection": {"num": 25, "den": 14, "root": 14},
  "residual": {"den": 14, "num": [-39, -6, 9]},
  "residual_sq": [117, 14]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, Bài 2](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=4).
:::
