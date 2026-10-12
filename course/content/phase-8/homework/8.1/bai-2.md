# Bài nộp còn hiệu lực

Trong kỳ thi, bài được chấm là bài nộp **hợp lệ gần nhất**. Một bài nộp hỏng định dạng không xóa được bài hợp lệ trước đó, nhưng cũng không tính điểm. Bài này cho biết: nếu kỳ thi dừng ở từng thời điểm, em được bao nhiêu điểm?

Mỗi lần nộp có `id`, `time` (phút), `valid` và `private` (điểm private, chỉ biết sau kỳ thi). Danh sách không theo thứ tự thời gian, và không có hai lần nộp cùng phút.

Với mỗi thời điểm $t$ trong `checkpoints`: bài được chấm là bài hợp lệ có `time` $\le t$ lớn nhất; báo `id` và điểm của nó, hoặc `null` và $0$ nếu chưa có bài hợp lệ nào. Báo thêm điểm private cao nhất trong mọi bài hợp lệ.

## Dữ liệu vào

Một đối tượng JSON gồm `submissions` và `checkpoints`.

## Kết quả

Một đối tượng JSON gồm `final` (với mỗi thời điểm là `{"time", "id", "score"}`) và `best_private_ever`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "submissions": [
    {"id": "baseline", "time": 20, "valid": true, "private": 0.61},
    {"id": "cnn-v1", "time": 95, "valid": true, "private": 0.78},
    {"id": "cnn-v2", "time": 160, "valid": false, "private": 0.84},
    {"id": "ensemble", "time": 175, "valid": true, "private": 0.8}
  ],
  "checkpoints": [10, 60, 170, 180]
}
```

```output
{
  "final": [
    {"time": 10, "id": null, "score": 0.0},
    {"time": 60, "id": "baseline", "score": 0.61},
    {"time": 170, "id": "cnn-v1", "score": 0.78},
    {"time": 180, "id": "ensemble", "score": 0.8}
  ],
  "best_private_ever": 0.8
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
