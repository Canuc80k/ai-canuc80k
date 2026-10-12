# Shape và tham số

Trước khi đếm tham số, hãy đếm shape. Một tensor ảnh có shape `(N, C, H, W)`: số mẫu, số channel, chiều cao, chiều rộng. Cho shape đầu vào và một dãy lớp, báo shape sau từng lớp, số tham số của từng lớp và tổng.

| Lớp | Đổi shape | Tham số |
|---|---|---|
| `conv` (`out`, `k`, `p`, `s`, `d`, `bias`) | $C\to$ `out`; $H\to\lfloor(H+2p-d(k-1)-1)/s\rfloor+1$, $W$ tương tự | $\text{out}\cdot(C k^2+[\text{bias}])$ |
| `bn` | không đổi | $2C$ |
| `pool` (`k`, `s`) | $H\to\lfloor(H-k)/s\rfloor+1$, $W$ tương tự | $0$ |
| `flatten` | `(N, C, H, W)` $\to$ `(N, C·H·W)` | $0$ |
| `linear` (`out`, `bias`) | `(N, F)` $\to$ `(N, out)` | $\text{out}\cdot(F+[\text{bias}])$ |

Ở đây $[\text{bias}]$ là $1$ nếu `bias` là `true`, ngược lại là $0$. Kernel là hình vuông $k\times k$.

## Dữ liệu vào

Một đối tượng JSON gồm `input` (list bốn số `[N, C, H, W]`) và `layers` (list các lớp, mỗi lớp có `type` và đủ các trường như bảng).

## Kết quả

Một đối tượng JSON gồm `shapes` (shape sau từng lớp), `params` (số tham số từng lớp) và `total`.

## Giới hạn

- Không quá $8$ lớp; mọi kích thước ở mọi bước đều dương; `linear` chỉ đứng sau `flatten`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "input": [4, 3, 8, 8],
  "layers": [
    {
      "type": "conv",
      "out": 2,
      "k": 3,
      "p": 1,
      "s": 2,
      "d": 1,
      "bias": true
    },
    {"type": "bn"},
    {"type": "pool", "k": 2, "s": 2},
    {"type": "flatten"},
    {"type": "linear", "out": 3, "bias": true}
  ]
}
```

```output
{
  "shapes": [[4, 2, 4, 4], [4, 2, 4, 4], [4, 2, 2, 2], [4, 8], [4, 3]],
  "params": [56, 4, 0, 0, 27],
  "total": 87
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
