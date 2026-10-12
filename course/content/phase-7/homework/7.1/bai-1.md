# Đọc tệp WAV

Đọc một tệp WAV và kiểm vài con số cơ bản trước khi đưa âm thanh vào mô hình. Một bẫy quen thuộc: hai kênh trái phải có thể rất to mà gộp thành mono lại gần như im lặng, khi hai kênh ngược pha nhau.

Tệp `clip.wav` là PCM 16 bit (số nguyên có dấu, little-endian), có $N$ khung, $C$ kênh, tần số lấy mẫu $F_s$.

- Đổi mỗi mẫu thành số thực bằng cách chia cho $32768$.
- `duration` là $N/F_s$ giây; `last_sample_time` là thời điểm của mẫu cuối, $(N-1)/F_s$.
- `mono` là trung bình các kênh tại từng khung.
- `channel_rms` là $\sqrt{\text{trung bình bình phương}}$ của từng kênh; `mono_rms` tương tự cho tín hiệu mono.

## Dữ liệu vào

Mỗi thư mục test có `input.json` (gồm `file`, tên tệp WAV) và tệp WAV ấy.

## Kết quả

Một đối tượng JSON gồm `frames`, `channels`, `sample_rate`, `duration`, `last_sample_time`, `mono`, `channel_rms` và `mono_rms`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"file": "clip.wav"}
```

```output
{
  "frames": 64,
  "channels": 2,
  "sample_rate": 2048,
  "duration": 0.03125,
  "last_sample_time": 0.03076171875,
  "mono": [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
  ],
  "channel_rms": [0.4242614408971766, 0.4242614408971766],
  "mono_rms": 0.0
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
