# Chồng 3x3

Một conv $7\times7$ và ba conv $3\times3$ chồng lên nhau nhìn cùng một vùng $7\times7$ của ảnh. Vì sao các CNN hiện đại chọn cách thứ hai? Bài này so bằng số.

Mỗi thiết kế là một dãy lớp `Conv2d` có bias. Lớp có kernel $k$, stride $s$, padding $p$, nhận $c$ kênh và ra $o$ kênh:

- Kích thước không gian mới: $\left\lfloor\frac{h+2p-k}{s}\right\rfloor+1$.
- Số tham số: $o\cdot c\cdot k^2+o$.
- Số phép nhân-cộng (MAC): mỗi ô đầu ra cần $c\cdot k^2$ phép, nhân với $o\cdot h_{out}\cdot w_{out}$ ô.
- Receptive field: bắt đầu $r=j=1$, qua mỗi lớp $r\leftarrow r+(k-1)j$ rồi $j\leftarrow j\cdot s$.

Với mỗi thiết kế, hãy báo shape `[C, H, W]` sau từng lớp, tổng tham số, tổng MAC và receptive field cuối. Thêm hai tỉ số: tham số và MAC của thiết kế thứ hai trong `compare` chia cho của thiết kế thứ nhất.

## Dữ liệu vào

Một đối tượng JSON gồm `channels`, `height`, `width` (của ảnh vào), `designs` (từ tên thiết kế tới list lớp, mỗi lớp có `kernel`, `stride`, `padding`, `out_channels`) và `compare` (hai tên).

## Kết quả

Một đối tượng JSON: mỗi thiết kế là một trường `{"shapes": [...], "parameters": ..., "macs": ..., "receptive_field": ...}`, cùng hai trường `param_ratio` và `mac_ratio`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "channels": 64,
  "height": 56,
  "width": 56,
  "compare": ["big", "stack"],
  "designs": {
    "big": [{"kernel": 7, "stride": 1, "padding": 3, "out_channels": 64}],
    "stack": [
      {"kernel": 3, "stride": 1, "padding": 1, "out_channels": 64},
      {"kernel": 3, "stride": 1, "padding": 1, "out_channels": 64},
      {"kernel": 3, "stride": 1, "padding": 1, "out_channels": 64}
    ]
  }
}
```

```output
{
  "big": {
    "shapes": [[64, 56, 56]],
    "parameters": 200768,
    "macs": 629407744,
    "receptive_field": 7
  },
  "stack": {
    "shapes": [[64, 56, 56], [64, 56, 56], [64, 56, 56]],
    "parameters": 110784,
    "macs": 346816512,
    "receptive_field": 7
  },
  "param_ratio": 0.5518010838380618,
  "mac_ratio": 0.5510204081632653
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 215](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=78).
:::
