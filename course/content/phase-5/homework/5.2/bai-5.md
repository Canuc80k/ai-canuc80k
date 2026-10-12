# Conv tách

MobileNet thay mỗi conv thường bằng một conv tách: depthwise $k\times k$ (mỗi kênh một kernel riêng) rồi pointwise $1\times1$ (trộn kênh). Bài này đo nó tiết kiệm bao nhiêu.

Mỗi lớp nhận $c$ kênh, ra $o$ kênh, kernel $k$, và giữ nguyên kích thước ảnh $h\times w$ (padding phù hợp, stride $1$). Không tính bias.

- Conv thường: $o\cdot c\cdot k^2$ tham số; mỗi ô đầu ra cần $c\,k^2$ phép nhân-cộng cho mỗi kênh ra.
- Conv tách: depthwise có $c\cdot k^2$ tham số, pointwise có $c\cdot o$ tham số.
- Số phép nhân-cộng (MAC) của mỗi phần bằng số tham số của nó nhân $h\cdot w$.

Với mỗi lớp, hãy tính tham số và MAC của hai cách, tỉ số MAC (tách chia thường), và giá trị $\frac1o+\frac1{k^2}$. Thêm tỉ số MAC và tỉ số tham số trên toàn bộ các lớp.

## Dữ liệu vào

Một đối tượng JSON gồm `layers`, mỗi lớp là `{"in": c, "out": o, "kernel": k, "height": h, "width": w}`.

## Kết quả

Một đối tượng JSON gồm `layers` (mỗi lớp là `{"standard_params", "separable_params", "standard_macs", "separable_macs", "ratio", "formula"}`), `total_ratio` và `total_param_ratio`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "layers": [
    {"in": 32, "out": 64, "kernel": 3, "height": 112, "width": 112},
    {"in": 512, "out": 512, "kernel": 3, "height": 14, "width": 14},
    {"in": 3, "out": 8, "kernel": 3, "height": 224, "width": 224}
  ]
}
```

```output
{
  "layers": [
    {
      "standard_params": 18432,
      "separable_params": 2336,
      "standard_macs": 231211008,
      "separable_macs": 29302784,
      "ratio": 0.1267361111111111,
      "formula": 0.1267361111111111
    },
    {
      "standard_params": 2359296,
      "separable_params": 266752,
      "standard_macs": 462422016,
      "separable_macs": 52283392,
      "ratio": 0.1130642361111111,
      "formula": 0.1130642361111111
    },
    {
      "standard_params": 216,
      "separable_params": 51,
      "standard_macs": 10838016,
      "separable_macs": 2558976,
      "ratio": 0.2361111111111111,
      "formula": 0.2361111111111111
    }
  ],
  "total_ratio": 0.11944444444444445,
  "total_param_ratio": 0.11318138694603405
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
