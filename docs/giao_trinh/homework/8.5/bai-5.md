# Chữa buổi thi

Chữa một buổi thi thử không dừng ở bảng điểm. Nhật ký các việc đã làm cho biết thời gian đi đâu, việc nào phí, và bao giờ mỗi bài mới có bài nộp hợp lệ đầu tiên.

Mỗi việc trong nhật ký có `task`, `start`, `end` (phút), `kind` (`knowledge`: lỗi kiến thức; `experiment`: thử nghiệm; `process`: quy trình như đọc file, định dạng, nộp), `useful` (việc ấy có góp vào kết quả không) và có thể có `submission` (`valid` hoặc `invalid`). Các việc không chồng lên nhau.

1. `minutes_by_kind`: tổng thời gian theo loại việc. `wasted_by_kind`: tổng thời gian các việc **không** hữu ích, theo loại. Cả hai xếp khóa theo thứ tự chuỗi, chỉ gồm các loại có mặt.
2. `first_valid`: với mỗi bài trong `tasks`, thời điểm kết thúc của việc sớm nhất có bài nộp hợp lệ, hoặc `null`.
3. `idle_minutes`: số phút trong $[0,\text{duration})$ không thuộc việc nào.
4. `main_loss`: loại việc phí nhiều thời gian nhất (bằng nhau thì tên nhỏ hơn), hoặc `null` nếu không có việc phí.

## Dữ liệu vào

Một đối tượng JSON gồm `tasks`, `duration` và `events` (không theo thứ tự thời gian).

## Kết quả

Một đối tượng JSON gồm `minutes_by_kind`, `wasted_by_kind`, `first_valid`, `idle_minutes` và `main_loss`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "tasks": ["A", "B"],
  "duration": 120,
  "events": [
    {
      "task": "A",
      "start": 0,
      "end": 15,
      "kind": "knowledge",
      "useful": true
    },
    {
      "task": "A",
      "start": 15,
      "end": 45,
      "kind": "experiment",
      "useful": true,
      "submission": "valid"
    },
    {
      "task": "B",
      "start": 50,
      "end": 80,
      "kind": "process",
      "useful": false,
      "submission": "invalid"
    },
    {
      "task": "B",
      "start": 80,
      "end": 95,
      "kind": "process",
      "useful": true,
      "submission": "valid"
    },
    {
      "task": "A",
      "start": 95,
      "end": 115,
      "kind": "experiment",
      "useful": false
    }
  ]
}
```

```output
{
  "minutes_by_kind": {"experiment": 50, "knowledge": 15, "process": 45},
  "wasted_by_kind": {"experiment": 20, "process": 30},
  "first_valid": {"A": 45, "B": 95},
  "idle_minutes": 10,
  "main_loss": "process"
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
