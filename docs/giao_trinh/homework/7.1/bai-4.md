# Khung đặc trưng

Nhiều mô hình tiếng nói (như wav2vec 2.0) không dùng phổ mà đưa thẳng sóng âm qua một chồng conv 1D. Mỗi lớp thu ngắn chuỗi lại. Bài này tính chuỗi còn dài bao nhiêu sau mỗi lớp, và mỗi khung đầu ra "nghe" bao nhiêu mẫu âm thanh.

Mỗi lớp có `kernel` $k$, `stride` $s$, `padding` $p$ (đệm $p$ mẫu mỗi bên). Một chuỗi dài $a$ qua lớp ấy còn
$$b=\left\lfloor\frac{a+2p-k}{s}\right\rfloor+1$$
khung, nếu $a>0$ và $a+2p\ge k$; ngược lại còn $0$ khung (và mọi lớp sau cũng $0$).

Hãy tính:

- `total_stride`: tích các stride, tức số mẫu giữa hai khung đầu ra liền nhau.
- `receptive_field`: số mẫu đầu vào mà một khung đầu ra phụ thuộc vào. Đi từ lớp đầu: bắt đầu với $r=1$, $J=1$; qua mỗi lớp, $r\leftarrow r+(k-1)J$ rồi $J\leftarrow J\cdot s$.
- `frame_rate`: số khung đầu ra mỗi giây, $F_s/\text{total\_stride}$; và `receptive_field_ms`: vùng nhìn tính bằng mili giây.
- Với mỗi độ dài trong `input_samples`: số khung sau từng lớp.
- Với mỗi số trong `target_frames`: số mẫu nhỏ nhất để lớp cuối ra ít nhất chừng ấy khung.

## Dữ liệu vào

Một đối tượng JSON gồm `layers` (mỗi lớp là `{"kernel", "stride", "padding"}`), `sample_rate`, `input_samples` và `target_frames`.

## Kết quả

Một đối tượng JSON gồm `total_stride`, `receptive_field`, `frame_rate`, `receptive_field_ms`, `inputs` (với mỗi độ dài là `{"samples", "frames_per_layer"}`) và `min_samples`.

## Giới hạn

- Không quá $7$ lớp. Đáp số của `min_samples` không quá $40000$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "layers": [
    {"kernel": 10, "stride": 5, "padding": 0},
    {"kernel": 3, "stride": 2, "padding": 0},
    {"kernel": 3, "stride": 2, "padding": 0},
    {"kernel": 3, "stride": 2, "padding": 0},
    {"kernel": 3, "stride": 2, "padding": 0},
    {"kernel": 2, "stride": 2, "padding": 0},
    {"kernel": 2, "stride": 2, "padding": 0}
  ],
  "sample_rate": 16000,
  "input_samples": [16000, 8000, 400, 399],
  "target_frames": [1, 50, 100]
}
```

```output
{
  "total_stride": 320,
  "receptive_field": 400,
  "frame_rate": 50.0,
  "receptive_field_ms": 25.0,
  "inputs": [
    {
      "samples": 16000,
      "frames_per_layer": [3199, 1599, 799, 399, 199, 99, 49]
    },
    {
      "samples": 8000,
      "frames_per_layer": [1599, 799, 399, 199, 99, 49, 24]
    },
    {"samples": 400, "frames_per_layer": [79, 39, 19, 9, 4, 2, 1]},
    {"samples": 399, "frames_per_layer": [78, 38, 18, 8, 3, 1, 0]}
  ],
  "min_samples": [400, 16080, 32080]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
