# Phát hiện sự kiện

Phát hiện sự kiện âm thanh: mô hình cho mỗi khung thời gian một xác suất "đang có sự kiện" (ví dụ tiếng còi). Đổi chuỗi xác suất ấy thành danh sách các sự kiện (bắt đầu, kết thúc) cần hậu xử lý; đặt một ngưỡng đơn giản thường cho ra các sự kiện vụn vặt. Bài này so hai cách.

Khung $t$ ứng với thời điểm $t\cdot h$ giây ($h$ là `hop`). Một sự kiện là đoạn khung $[a,b)$, viết thành $[a h,\ b h]$ giây.

1. **Ngưỡng trễ** (`high`, `low`): khi chưa có sự kiện, khung có xác suất $\ge$ `high` mở sự kiện; khi đang có sự kiện, khung đầu tiên có xác suất $<$ `low` đóng nó (khung ấy không thuộc sự kiện). Hết chuỗi mà sự kiện còn mở thì đóng ở cuối.
2. **Gộp:** hai sự kiện liền nhau có khoảng hở (đầu sau trừ cuối trước) không quá `merge_gap` thì gộp làm một.
3. **Bỏ sự kiện ngắn:** sau khi gộp, bỏ sự kiện dài dưới `min_duration`.
4. **Cách đơn giản** để so: chỉ bước 1 với `high` $=$ `low` $=0.5$, không gộp, không bỏ.

**Chấm theo sự kiện:** duyệt các sự kiện thật trong `reference` theo thứ tự; mỗi sự kiện thật ghép với sự kiện dự đoán **đầu tiên** chưa được ghép mà đầu lệch không quá `collar` và cuối lệch không quá `collar`. Mỗi cặp ghép là một TP; dự đoán thừa là FP, sự kiện thật không ghép được là FN; $F_1=\dfrac{2TP}{2TP+FP+FN}$ (bằng $0$ nếu $TP=0$).

## Dữ liệu vào

Một đối tượng JSON gồm `probs`, `hop`, `high`, `low`, `merge_gap`, `min_duration`, `reference` và `collar`.

## Kết quả

Một đối tượng JSON gồm `naive_events`, `events`, `naive_score` và `score` (mỗi điểm là `{"tp", "fp", "fn", "f1"}`).

## Giới hạn

- Không quá $40$ khung. `hop` là $0.125$, $0.25$ hoặc $0.5$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "probs": [
    0.1, 0.2, 0.7, 0.8, 0.45, 0.75, 0.9, 0.3, 0.1, 0.55, 0.2, 0.1, 0.6,
    0.85, 0.9, 0.8, 0.4, 0.1
  ],
  "hop": 0.25,
  "high": 0.7,
  "low": 0.4,
  "merge_gap": 0.25,
  "min_duration": 0.5,
  "reference": [[0.5, 1.75], [3.0, 4.0]],
  "collar": 0.25
}
```

```output
{
  "naive_events": [[0.5, 1.0], [1.25, 1.75], [2.25, 2.5], [3.0, 4.0]],
  "events": [[0.5, 1.75], [3.25, 4.25]],
  "naive_score": {"tp": 1, "fp": 3, "fn": 1, "f1": 0.3333333333333333},
  "score": {"tp": 2, "fp": 0, "fn": 0, "f1": 1.0}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
