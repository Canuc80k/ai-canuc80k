# Nối skip

Một bạn viết U-Net, chạy với ảnh $256\times256$ thì ổn, nhưng đổi sang ảnh $100\times100$ thì báo lỗi `Sizes of tensors must match` ở phép nối skip. Bài này lần theo shape để tìm chỗ hỏng.

U-Net có $D$ lần giảm độ phân giải, số kênh ở các mức là `channels` $=[c_0,c_1,\dots,c_D]$. Ảnh vào cỡ $H\times W$.

- **Encoder.** Mức $0$ có feature map $c_0\times H\times W$ (các conv đều có padding, giữ nguyên cỡ). Từ mức $k$ xuống mức $k+1$ dùng `MaxPool2d(2)`: cỡ chia đôi, **làm tròn xuống**. Feature map ở mức $k$ có $c_k$ kênh và được giữ làm skip.
- **Decoder**, đi từ mức $D-1$ về mức $0$. Ở mức $k$:
  1. `ConvTranspose2d(c_{k+1}, u_k, 2, stride=2)`: nhân đôi cỡ, ra $u_k$ kênh, với `up_channels` $=[u_0,\dots,u_{D-1}]$.
  2. Nối với skip mức $k$ theo chiều kênh. Hai tensor phải cùng cỡ, nếu không thì báo lỗi.
  3. `Conv2d(u_k + c_k, c_k, 3, padding=1)`.
- Cuối cùng `Conv2d(c_0, classes, 1)`.

Hãy tính:

- `cat_channels`: số kênh sau phép nối ở mỗi mức $k=0,\dots,D-1$.
- `decoder_params`: tổng số tham số (kể cả bias) của các lớp `ConvTranspose2d`, các `Conv2d` sau phép nối và lớp `Conv2d` cuối.
- Với mỗi cỡ ảnh trong `sizes`:
  - `skip_shapes`: shape $[c_k, H_k, W_k]$ của feature map ở mỗi mức $k=0,\dots,D$.
  - `fail_level`: mức mà decoder báo lỗi khi nối, hoặc $-1$ nếu chạy trọn vẹn.
  - `pad_to`: cỡ nhỏ nhất, không nhỏ hơn ảnh, mà đệm ảnh lên cỡ ấy thì U-Net chạy được, viết $[H', W']$.

## Dữ liệu vào

Một đối tượng JSON gồm `channels`, `up_channels`, `classes` và `sizes` (list các cặp $[H, W]$).

## Kết quả

Một đối tượng JSON gồm `cat_channels`, `decoder_params` và `sizes`: list cùng thứ tự với dữ liệu vào, mỗi phần tử là `{"skip_shapes", "fail_level", "pad_to"}`.

## Giới hạn

- $1\le D\le4$, không quá $5$ cỡ ảnh mỗi test, $2^D\le H, W\le640$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "channels": [64, 128, 256, 512],
  "up_channels": [64, 128, 256],
  "classes": 2,
  "sizes": [[256, 256], [100, 100], [572, 572], [96, 98]]
}
```

```output
{
  "cat_channels": [128, 256, 512],
  "decoder_params": 2237442,
  "sizes": [
    {
      "skip_shapes": [[64, 256, 256], [128, 128, 128], [256, 64, 64], [512, 32, 32]],
      "fail_level": -1,
      "pad_to": [256, 256]
    },
    {
      "skip_shapes": [[64, 100, 100], [128, 50, 50], [256, 25, 25], [512, 12, 12]],
      "fail_level": 2,
      "pad_to": [104, 104]
    },
    {
      "skip_shapes": [[64, 572, 572], [128, 286, 286], [256, 143, 143], [512, 71, 71]],
      "fail_level": 2,
      "pad_to": [576, 576]
    },
    {
      "skip_shapes": [[64, 96, 98], [128, 48, 49], [256, 24, 24], [512, 12, 12]],
      "fail_level": 1,
      "pad_to": [96, 104]
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 13](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=18).
:::
