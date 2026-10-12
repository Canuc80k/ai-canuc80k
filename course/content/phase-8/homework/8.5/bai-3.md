# Mốc thời gian

Buổi thi thử có một kế hoạch gồm các mốc, mỗi mốc có hạn (phút thứ mấy phải xong). Sau buổi thi, đối chiếu nhật ký với kế hoạch để thấy mình bắt đầu trễ từ đâu.

Với mỗi mốc theo thứ tự trong `plan`:

- Không có trong nhật ký: `missing`, `late_by` là `null`.
- Xong không muộn hơn hạn: `on_time`, `late_by` là $0$.
- Xong muộn hơn hạn: `late`, `late_by` là số phút muộn.

Báo thêm mốc **đầu tiên** (theo kế hoạch) không đúng hạn, hoặc `null` nếu mọi mốc đều đúng hạn. Mỗi mốc xuất hiện trong nhật ký không quá một lần.

## Dữ liệu vào

Một đối tượng JSON gồm `plan` (mỗi mốc là `{"milestone", "deadline"}`) và `log` (mỗi dòng là `{"milestone", "minute"}`, không theo thứ tự).

## Kết quả

Một đối tượng JSON gồm `milestones` (mỗi mốc là `{"milestone", "status", "late_by"}`) và `first_problem`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "plan": [
    {"milestone": "doc_de", "deadline": 20},
    {"milestone": "baseline_A", "deadline": 30},
    {"milestone": "nop_A", "deadline": 60},
    {"milestone": "baseline_B", "deadline": 70},
    {"milestone": "nop_B", "deadline": 100}
  ],
  "log": [
    {"milestone": "nop_A", "minute": 50},
    {"milestone": "doc_de", "minute": 45},
    {"milestone": "baseline_B", "minute": 70},
    {"milestone": "baseline_A", "minute": 30}
  ]
}
```

```output
{
  "milestones": [
    {"milestone": "doc_de", "status": "late", "late_by": 25},
    {"milestone": "baseline_A", "status": "on_time", "late_by": 0},
    {"milestone": "nop_A", "status": "on_time", "late_by": 0},
    {"milestone": "baseline_B", "status": "on_time", "late_by": 0},
    {"milestone": "nop_B", "status": "missing", "late_by": null}
  ],
  "first_problem": "doc_de"
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
