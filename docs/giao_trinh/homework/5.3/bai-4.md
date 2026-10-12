# Box qua pipeline

Một pipeline augmentation hay gặp: thu ảnh để cạnh ngắn bằng $S$, cắt một ô vuông $C\times C$ ở giữa, rồi có thể lật ngang. Với ảnh có bounding box, cần biết box đi đâu, và vật nằm sát mép còn thấy được bao nhiêu sau khi cắt.

Mọi tọa độ là tọa độ liên tục, không làm tròn. Ảnh gốc cỡ $W\times H$.

1. **Resize**: nhân mọi tọa độ với $s=S/\min(W,H)$. Ảnh mới cỡ $Ws\times Hs$.
2. **CenterCrop**: ô cắt bắt đầu ở $o_x=(Ws-C)/2$, $o_y=(Hs-C)/2$. Tọa độ mới là tọa độ sau Resize trừ $o_x$ (theo $x$) và $o_y$ (theo $y$), rồi box bị cắt cho nằm trong $[0,C]$.
3. **Lật ngang** (nếu `flip` bật): $x\mapsto C-x$, đổi vai hai cạnh trái phải.

Với mỗi box, phần còn thấy (`visible`) là diện tích sau khi cắt chia diện tích ngay trước khi cắt (sau Resize). Box nằm hẳn ngoài ô cắt thì ghi `null` và phần còn thấy bằng $0$. Box được giữ (`kept`) khi phần còn thấy từ `min_visible` trở lên.

## Dữ liệu vào

Một đối tượng JSON gồm `width`, `height`, `resize` ($S$), `crop` ($C$), `flip`, `min_visible` và `boxes` (mỗi box là $[x_1,y_1,x_2,y_2]$ trên ảnh gốc).

## Kết quả

Một đối tượng JSON gồm `scale`, `offset` ($[o_x,o_y]$), `boxes` (mỗi box là `{"box": [...] | null, "visible": ..., "kept": ...}`) và `lost` (số box không được giữ).

## Giới hạn

- Không quá $6$ box. Không box nào có phần còn thấy sát đúng `min_visible`, và không box nào chỉ vừa chạm mép ô cắt.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "width": 400,
  "height": 300,
  "resize": 256,
  "crop": 224,
  "flip": true,
  "min_visible": 0.5,
  "boxes": [
    [150, 100, 250, 200],
    [0, 120, 40, 180],
    [360, 10, 400, 60],
    [10, 0, 120, 30]
  ]
}
```

```output
{
  "scale": 0.8533333333333334,
  "offset": [58.666666666666664, 16.0],
  "boxes": [
    {
      "box": [
        69.33333333333333, 69.33333333333333, 154.66666666666666,
        154.66666666666666
      ],
      "visible": 1.0,
      "kept": true
    },
    {"box": null, "visible": 0.0, "kept": false},
    {"box": null, "visible": 0.0, "kept": false},
    {
      "box": [180.26666666666668, 0.0, 224.0, 9.6],
      "visible": 0.1747159090909091,
      "kept": false
    }
  ],
  "lost": 3
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 12](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=17).
:::
