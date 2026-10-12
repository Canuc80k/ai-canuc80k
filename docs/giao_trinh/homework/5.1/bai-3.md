# Shape và vùng nhìn

Trước khi dựng một CNN, nên lần theo shape qua từng lớp, cùng hai đại lượng: receptive field $r$ (mỗi ô đầu ra nhìn được bao nhiêu ô của ảnh gốc theo mỗi chiều) và jump $j$ (hai ô liền nhau ở đầu ra cách nhau bao nhiêu ô trên ảnh gốc). Bắt đầu với $r=j=1$; qua một lớp kernel $k$, stride $s$, dilation $d$:

$$
r\leftarrow r+(k-1)\,d\,j,\qquad j\leftarrow j\cdot s.
$$

Mỗi lớp là `conv` (`Conv2d` có bias, ra `out_channels` kênh) hoặc `pool` (`MaxPool2d`, giữ số kênh, bỏ qua `out_channels`). Kích thước không gian sau mỗi lớp là $\left\lfloor\frac{h+2p-d(k-1)-1}{s}\right\rfloor+1$.

Hãy báo shape `[1, C, H, W]` sau từng lớp, $r$ và $j$ sau từng lớp, và tổng số tham số của các lớp conv.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `height`, `width`, `channels` và `layers` (mỗi lớp có `kind`, `kernel`, `stride`, `padding`, `dilation`, `out_channels`).

## Kết quả

Một đối tượng JSON gồm `shapes`, `receptive_field`, `jump` và `parameters`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "height": 13,
  "width": 15,
  "channels": 2,
  "layers": [
    {
      "kind": "conv",
      "kernel": 3,
      "stride": 1,
      "padding": 1,
      "dilation": 1,
      "out_channels": 4
    },
    {
      "kind": "pool",
      "kernel": 2,
      "stride": 2,
      "padding": 0,
      "dilation": 1,
      "out_channels": 4
    },
    {
      "kind": "conv",
      "kernel": 3,
      "stride": 1,
      "padding": 1,
      "dilation": 1,
      "out_channels": 3
    }
  ]
}
```

```output
{
  "shapes": [[1, 4, 13, 15], [1, 4, 6, 7], [1, 3, 6, 7]],
  "receptive_field": [3, 4, 8],
  "jump": [1, 2, 2],
  "parameters": 187
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
