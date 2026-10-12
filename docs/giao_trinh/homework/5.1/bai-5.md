# im2col

Thư viện thường tính tích chập bằng một phép nhân ma trận lớn: trải mọi cửa sổ của ảnh thành các cột (im2col), rồi nhân với ma trận trọng số. Bài này làm đúng việc ấy.

Ảnh `X` có $C$ kênh, cỡ $H\times W$. Trọng số có $O$ kernel, mỗi kernel cỡ $C\times k\times k$. Với stride $s$ và padding $p$ (ô ngoài ảnh bằng $0$), đầu ra cỡ $H_o\times W_o$.

1. Dựng ma trận `cols` có $C k^2$ hàng và $H_o W_o$ cột. Hàng $c\,k^2+u\,k+v$, cột $i\,W_o+j$ là ô $X_{c,\ i s+u-p,\ j s+v-p}$.
2. Trải mỗi kernel thành một hàng $C k^2$ số theo cùng thứ tự $(c,u,v)$. Nhân ma trận trọng số ($O\times Ck^2$) với `cols`, cộng bias, rồi xếp lại thành $O\times H_o\times W_o$.
3. `blowup`: số phần tử của `cols` chia số phần tử của ảnh.

## Dữ liệu vào

Một đối tượng JSON gồm `X`, `weight`, `bias`, `stride` và `padding`.

## Kết quả

Một đối tượng JSON gồm `cols_shape`, `cols`, `output` và `blowup`.

## Giới hạn

- $C\le2$, $H,W\le6$, $k\le3$, $O\le3$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]],
  "weight": [[[[1.0, 0.0], [0.0, -1.0]]]],
  "bias": [0.5],
  "stride": 1,
  "padding": 0
}
```

```output
{
  "cols_shape": [4, 4],
  "cols": [
    [1.0, 2.0, 4.0, 5.0],
    [2.0, 3.0, 5.0, 6.0],
    [4.0, 5.0, 7.0, 8.0],
    [5.0, 6.0, 8.0, 9.0]
  ],
  "output": [[[-3.5, -3.5], [-3.5, -3.5]]],
  "blowup": 1.7777777777777777
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
