# Điểm chuẩn hóa

Mỗi bài trong một kỳ thi đo bằng một thước đo riêng: bài này F1 (càng cao càng tốt), bài kia RMSE (càng thấp càng tốt). Để so hay cộng điểm giữa các bài, kỳ thi USA-NA-AIO quy mọi kết quả về một thang chung bằng điểm của baseline và điểm của bài làm tốt nhất.

Với mỗi bài, gọi $X$ là kết quả của em, $X_b$ của baseline, $X^*$ của bài làm tốt nhất:

- Thước đo càng cao càng tốt: $r=\dfrac{X-X_b}{X^*-X_b}$.
- Thước đo càng thấp càng tốt: $r=\dfrac{X_b-X}{X_b-X^*}$.
- Kém hơn baseline thì $r=0$ (không có điểm âm).

Điểm của bài là $r$ nhân số điểm tối đa của bài. Báo $r$, điểm từng bài và tổng điểm.

## Dữ liệu vào

Một đối tượng JSON gồm `problems`: mỗi bài là `{"score", "baseline", "best", "higher_is_better", "points"}`.

## Kết quả

Một đối tượng JSON gồm `problems` (mỗi bài là `{"ratio", "points"}`) và `total`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "problems": [
    {
      "score": 0.82,
      "baseline": 0.0,
      "best": 0.91,
      "higher_is_better": true,
      "points": 40
    },
    {
      "score": 1.9,
      "baseline": 2.5,
      "best": 1.2,
      "higher_is_better": false,
      "points": 50
    },
    {
      "score": 2.8,
      "baseline": 2.5,
      "best": 1.2,
      "higher_is_better": false,
      "points": 50
    },
    {
      "score": 0.91,
      "baseline": 0.0,
      "best": 0.91,
      "higher_is_better": true,
      "points": 40
    }
  ]
}
```

```output
{
  "problems": [
    {"ratio": 0.9010989010989011, "points": 36.043956043956044},
    {"ratio": 0.46153846153846156, "points": 23.076923076923077},
    {"ratio": 0.0, "points": 0.0},
    {"ratio": 1.0, "points": 40.0}
  ],
  "total": 99.12087912087912
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 2, Ngày 2, Bài 4](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-2-day-2-problems.pdf#page=9).
:::
