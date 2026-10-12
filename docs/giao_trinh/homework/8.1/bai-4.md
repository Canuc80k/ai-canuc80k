# Chia thời gian

Còn `minutes` phút cho vài bài. Mỗi bài có một chuỗi bước phải làm **theo thứ tự** (ví dụ: dựng pipeline, rồi huấn luyện, rồi tinh chỉnh); làm xong bước thứ $k$ thì kết quả của bài đạt `metric` của bước ấy. Điểm của một bài tính theo công thức chuẩn hóa của USA-NA-AIO:

- càng cao càng tốt: $r=\max\!\big(0,\frac{X-X_b}{X^*-X_b}\big)$; càng thấp càng tốt: $r=\max\!\big(0,\frac{X_b-X}{X_b-X^*}\big)$;
- điểm bài $=r\cdot$`points`; chưa làm bước nào thì $0$ điểm.

Một kế hoạch chọn cho mỗi bài số bước $k_i$ làm được (luôn là các bước đầu), với tổng thời gian không quá `minutes`.

1. **Kế hoạch tối ưu:** tổng điểm lớn nhất; bằng nhau thì ít phút hơn; vẫn bằng nhau thì vector $(k_1,k_2,\dots)$ nhỏ hơn theo thứ tự từ điển.
2. **Kế hoạch tham lam:** bắt đầu từ $k_i=0$; mỗi lượt, xét các bài còn bước tiếp theo và còn đủ thời gian cho bước ấy, chọn bước có (điểm tăng thêm)/(số phút) lớn nhất (bằng nhau thì bài đứng trước); dừng khi không còn bước nào hoặc mức tăng lớn nhất không dương.

Báo số bước, tổng điểm và số phút của cả hai kế hoạch.

## Dữ liệu vào

Một đối tượng JSON gồm `minutes` và `problems`: mỗi bài là `{"name", "points", "higher_is_better", "baseline", "best", "steps"}`, mỗi bước là `{"minutes", "metric"}`.

## Kết quả

Một đối tượng JSON gồm `optimal` và `greedy`, mỗi cái là `{"steps", "points", "minutes"}`.

## Giới hạn

- Không quá $3$ bài, mỗi bài không quá $3$ bước.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "minutes": 120,
  "problems": [
    {
      "name": "text",
      "points": 40,
      "higher_is_better": true,
      "baseline": 0.5,
      "best": 0.9,
      "steps": [
        {"minutes": 30, "metric": 0.7},
        {"minutes": 40, "metric": 0.8},
        {"minutes": 40, "metric": 0.85}
      ]
    },
    {
      "name": "image",
      "points": 50,
      "higher_is_better": true,
      "baseline": 0.4,
      "best": 0.95,
      "steps": [{"minutes": 50, "metric": 0.45}, {"minutes": 40, "metric": 0.9}]
    },
    {
      "name": "search",
      "points": 30,
      "higher_is_better": false,
      "baseline": 20.0,
      "best": 5.0,
      "steps": [{"minutes": 20, "metric": 12.0}, {"minutes": 30, "metric": 8.0}]
    }
  ]
}
```

```output
{
  "optimal": {"steps": [1, 2, 0], "points": 65.45454545454545, "minutes": 120},
  "greedy": {"steps": [2, 0, 2], "points": 54.0, "minutes": 120}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 2, Ngày 2, Bài 4–5](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-2-day-2-problems.pdf#page=9).
:::
