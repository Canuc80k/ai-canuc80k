# Đồ thị tính toán

Autograd ghi lại phép tính thành một đồ thị, rồi đi ngược đồ thị để tính gradient. Bài này yêu cầu tự làm việc ấy trên một đồ thị nhỏ.

Đồ thị gồm các đỉnh đánh số từ $0$, cho theo thứ tự tính được: mỗi đỉnh chỉ dùng các đỉnh đứng trước nó. Mỗi đỉnh là một trong các loại:

| Loại | Giá trị |
|---|---|
| `input` | số `value` cho sẵn |
| `add`, `sub`, `mul` | $u+w$, $u-w$, $u\cdot w$ với $u$, $w$ là giá trị hai đỉnh trong `args` |
| `tanh`, `exp`, `relu` | $\tanh u$, $e^u$, $\max(0,u)$ với $u$ là giá trị đỉnh trong `args` |
| `pow` | $u^p$ với số mũ nguyên `p` |

Hai đỉnh trong `args` có thể trùng nhau, chẳng hạn `mul` với `args` là `[0, 0]` cho $u^2$.

Đầu ra của đồ thị là đỉnh cuối cùng. Hãy tính giá trị mọi đỉnh, và đạo hàm của đầu ra theo từng đỉnh. Một đỉnh được dùng ở nhiều chỗ thì gradient từ các chỗ ấy được **cộng** lại. Đạo hàm của `relu` tại $u\le0$ quy ước bằng $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `nodes`, danh sách các đỉnh. Mỗi đỉnh có `op`, và tùy loại có thêm `value`, `args`, `p`.

## Kết quả

Một đối tượng JSON gồm `values` (giá trị từng đỉnh) và `grads` (đạo hàm của đầu ra theo từng đỉnh). Đạo hàm theo chính đỉnh cuối bằng $1$.

## Giới hạn

- Không quá $30$ đỉnh. Mọi giá trị có trị tuyệt đối không quá $1000$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "nodes": [
    {"op": "input", "value": 2.0},
    {"op": "input", "value": -3.0},
    {"op": "input", "value": 1.5},
    {"op": "mul", "args": [0, 1]},
    {"op": "add", "args": [3, 0]},
    {"op": "mul", "args": [4, 2]},
    {"op": "pow", "args": [0], "p": 2},
    {"op": "add", "args": [5, 6]}
  ]
}
```

```output
{
  "values": [2.0, -3.0, 1.5, -6.0, -4.0, -6.0, 4.0, -2.0],
  "grads": [1.0, 3.0, -4.0, 1.5, 1.5, 1.0, 1.0, 1.0]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
