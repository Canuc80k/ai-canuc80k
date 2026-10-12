# Đặc trưng đa thức

`PolynomialFeatures` biến $d$ đặc trưng $x_0,\dots,x_{d-1}$ thành mọi đơn thức của chúng có bậc không quá $p$. Chẳng hạn với $d=2$, $p=2$, ta được $1,\ x_0,\ x_1,\ x_0^2,\ x_0x_1,\ x_1^2$. Số đặc trưng tăng rất nhanh theo $d$ và $p$, nên trước khi dùng cần biết sẽ có bao nhiêu cột.

Có hai tùy chọn:

- `interaction_only`: nếu đúng, chỉ giữ các đơn thức mà mỗi biến có số mũ không quá $1$, như $x_0x_1$, bỏ $x_0^2$.
- `include_bias`: nếu đúng, giữ đơn thức bậc $0$, tức cột hằng số $1$.

Thứ tự các đơn thức giống scikit-learn: bậc tăng dần. Trong cùng một bậc, viết mỗi đơn thức thành dãy chỉ số biến không giảm, như $x_0x_0x_1$ thành $(0,0,1)$, rồi xếp các dãy theo thứ tự từ điển.

Tên của một đơn thức gồm các biến theo chỉ số tăng dần, cách nhau một dấu cách. Biến có số mũ lớn hơn $1$ thì thêm `^` và số mũ. Ví dụ `x0^2 x1`. Đơn thức bậc $0$ có tên `1`.

Cho một hàng dữ liệu $x$, hãy liệt kê tên và giá trị các đặc trưng của nó. Sau đó, với cùng $p$ và hai tùy chọn, hãy cho biết với mỗi số đặc trưng $d$ trong `count_queries` thì có bao nhiêu cột.

## Dữ liệu vào

Một đối tượng JSON gồm `x` (các số nguyên), `degree`, `interaction_only`, `include_bias` và `count_queries`.

## Kết quả

Một đối tượng JSON gồm `names`, `values` (cùng thứ tự) và `counts`.

## Giới hạn

- $1\le d\le5$, $1\le p\le4$, mỗi $\lvert x_i\rvert\le5$.
- Mỗi số trong `count_queries` từ $1$ đến $1000$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "x": [2, 3],
  "degree": 2,
  "interaction_only": false,
  "include_bias": true,
  "count_queries": [2, 10, 100]
}
```

```output
{
  "names": ["1", "x0", "x1", "x0^2", "x0 x1", "x1^2"],
  "values": [1, 2, 3, 4, 6, 9],
  "counts": [6, 66, 5151]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
