# Chọn mẫu số

Detector báo "bắt được 90% bài lỗi". Một bài bị cảnh báo thì có lỗi với xác suất bao nhiêu? Hai câu hỏi nghe giống nhau, nhưng mẫu số khác nhau.

Chọn ngẫu nhiên đều một bài trong tập kiểm. Gọi $B$ là biến cố "bài có lỗi", $F$ là "bài bị cảnh báo". Bảng bốn ô cho số bài: `tp` (lỗi, bị cảnh báo), `fn` (lỗi, không bị cảnh báo), `fp` (sạch, bị cảnh báo), `tn` (sạch, không bị cảnh báo). Hãy tính:

| Khóa | Xác suất |
|---|---|
| `p_bug` | $P(B)$ |
| `p_alarm` | $P(F)$ |
| `p_bug_and_alarm` | $P(B\cap F)$ |
| `p_alarm_given_bug` | $P(F\mid B)$ |
| `p_alarm_given_clean` | $P(F\mid\neg B)$ |
| `p_bug_given_alarm` | $P(B\mid F)$ |
| `p_bug_given_quiet` | $P(B\mid\neg F)$ |

## Dữ liệu vào

Một đối tượng JSON gồm `tp`, `fn`, `fp` và `tn`.

## Kết quả

Một đối tượng JSON gồm bảy khóa trong bảng.

## Giới hạn

- Các mẫu số luôn dương: có bài lỗi, có bài sạch, có bài bị cảnh báo và có bài không bị cảnh báo.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"tp": 18, "fn": 2, "fp": 98, "tn": 882}
```

```output
{
  "p_bug": 0.02,
  "p_alarm": 0.116,
  "p_bug_and_alarm": 0.018000000000000002,
  "p_alarm_given_bug": 0.9,
  "p_alarm_given_clean": 0.1,
  "p_bug_given_alarm": 0.15517241379310345,
  "p_bug_given_quiet": 0.0022624434389140265
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
