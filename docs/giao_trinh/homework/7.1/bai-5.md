# Trộn nhiễu

Một cách làm giàu dữ liệu âm thanh là trộn thêm tiếng ồn ở một mức SNR (tỉ số tín hiệu trên nhiễu) định trước. Làm sai, tiếng ồn có thể to hơn ý muốn, hoặc tín hiệu trộn vượt quá giới hạn của PCM 16 bit và bị cắt méo.

Tín hiệu sạch $s$ và nhiễu $n$ cùng độ dài, giá trị thực (theo thang của PCM đã chia $32768$). Công suất là trung bình bình phương: $P_s$, $P_n$.

Với mỗi mức SNR (dB) trong `snr_db`:

1. Hệ số nhân nhiễu $a=\sqrt{\dfrac{P_s}{P_n\cdot10^{\text{SNR}/10}}}$, để $10\log_{10}\dfrac{P_s}{P_{an}}$ đúng bằng SNR.
2. Tín hiệu trộn $m=s+a\,n$.
3. Báo SNR đạt được (tính lại từ $a\,n$), đỉnh $\max|m|$, và số mẫu bị cắt khi đổi về PCM 16 bit: nhân $32768$, làm tròn tới số nguyên gần nhất, đếm các giá trị lớn hơn $32767$ hoặc nhỏ hơn $-32768$.
4. `safe_gain`: hệ số nhân cả tín hiệu trộn để đỉnh không vượt $32767/32768$, tức $\min\!\big(1,\ \tfrac{32767/32768}{\max|m|}\big)$.

## Dữ liệu vào

Một đối tượng JSON gồm `clean`, `noise` (cùng độ dài, nhiễu không toàn $0$) và `snr_db`.

## Kết quả

Một đối tượng JSON gồm `clean_power`, `noise_power` và `mixes`: với mỗi mức SNR là `{"snr_db", "noise_scale", "achieved_snr_db", "mix", "peak", "clipped", "safe_gain"}`.

## Giới hạn

- Không quá $32$ mẫu. Không mẫu nào nằm sát ranh giới làm tròn hay ranh giới cắt.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "clean": [
    0.0, 0.3536, 0.5, 0.3536, 0.0, -0.3536, -0.5, -0.3536, -0.0,
    0.3536, 0.5, 0.3536, 0.0, -0.3536, -0.5, -0.3536
  ],
  "noise": [
    0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1,
    0.1, -0.1, 0.1, -0.1
  ],
  "snr_db": [20, 10, 0, -5]
}
```

```output
{
  "clean_power": 0.12501648,
  "noise_power": 0.010000000000000002,
  "mixes": [
    {
      "snr_db": 20,
      "noise_scale": 0.35357669606465864,
      "achieved_snr_db": 20.0,
      "mix": [
        0.035357669606465865, 0.31824233039353417, 0.5353576696064659,
        0.31824233039353417, 0.035357669606465865, -0.3889576696064659,
        -0.46464233039353414, -0.3889576696064659,
        0.035357669606465865, 0.31824233039353417, 0.5353576696064659,
        0.31824233039353417, 0.035357669606465865, -0.3889576696064659,
        -0.46464233039353414, -0.3889576696064659
      ],
      "peak": 0.5353576696064659,
      "clipped": 0,
      "safe_gain": 1.0
    },
    {
      "snr_db": 10,
      "noise_scale": 1.1181076871214148,
      "achieved_snr_db": 10.0,
      "mix": [
        0.11181076871214149, 0.24178923128785854, 0.6118107687121415,
        0.24178923128785854, 0.11181076871214149, -0.4654107687121415,
        -0.38818923128785854, -0.4654107687121415, 0.11181076871214149,
        0.24178923128785854, 0.6118107687121415, 0.24178923128785854,
        0.11181076871214149, -0.4654107687121415, -0.38818923128785854,
        -0.4654107687121415
      ],
      "peak": 0.6118107687121415,
      "clipped": 0,
      "safe_gain": 1.0
    },
    {
      "snr_db": 0,
      "noise_scale": 3.5357669606465865,
      "achieved_snr_db": -9.643274665532871e-16,
      "mix": [
        0.3535766960646587, 2.330393534133446e-05, 0.8535766960646587,
        2.330393534133446e-05, 0.3535766960646587, -0.7071766960646587,
        -0.1464233039353413, -0.7071766960646587, 0.3535766960646587,
        2.330393534133446e-05, 0.8535766960646587,
        2.330393534133446e-05, 0.3535766960646587, -0.7071766960646587,
        -0.1464233039353413, -0.7071766960646587
      ],
      "peak": 0.8535766960646587,
      "clipped": 0,
      "safe_gain": 1.0
    },
    {
      "snr_db": -5,
      "noise_scale": 6.287581584813727,
      "achieved_snr_db": -5.0,
      "mix": [
        0.6287581584813727, -0.2751581584813727, 1.1287581584813728,
        -0.2751581584813727, 0.6287581584813727, -0.9823581584813728,
        0.12875815848137273, -0.9823581584813728, 0.6287581584813727,
        -0.2751581584813727, 1.1287581584813728, -0.2751581584813727,
        0.6287581584813727, -0.9823581584813728, 0.12875815848137273,
        -0.9823581584813728
      ],
      "peak": 1.1287581584813728,
      "clipped": 2,
      "safe_gain": 0.8859023298376247
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
