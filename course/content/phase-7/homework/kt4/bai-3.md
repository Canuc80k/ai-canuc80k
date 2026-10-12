# Chọn theo validation

Nhật ký thí nghiệm ghi lại các mô hình đã thử cho từng miền dữ liệu, kèm điểm validation, điểm test và chi phí huấn luyện. Hãy chọn mô hình **đúng quy trình**: theo validation, trong giới hạn chi phí; điểm test chỉ để báo cáo sau cùng, không dùng để chọn.

Với mỗi miền trong `domains`, theo thứ tự:

1. Chỉ xét các ứng viên của miền ấy có `fit_units` không quá `budget` của miền.
2. Chọn ứng viên có `valid_score` lớn nhất; bằng nhau thì `id` nhỏ hơn (so như chuỗi).
3. Không có ứng viên nào hợp lệ thì trả `id` là `null` và `fit_units` là $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `domains`, `budget` (từ miền tới số nguyên) và `candidates` (mỗi ứng viên là `{"domain", "id", "valid_score", "test_score", "fit_units"}`).

## Kết quả

Một đối tượng JSON gồm `selected`: với mỗi miền là `{"domain", "id", "fit_units"}`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "domains": ["audio", "text", "none"],
  "budget": {"audio": 3, "text": 1, "none": 0},
  "candidates": [
    {
      "domain": "audio",
      "id": "good",
      "valid_score": 0.85,
      "test_score": 0.3,
      "fit_units": 2
    },
    {
      "domain": "audio",
      "id": "testwinner",
      "valid_score": 0.7,
      "test_score": 0.99,
      "fit_units": 2
    },
    {
      "domain": "audio",
      "id": "expensive",
      "valid_score": 0.95,
      "test_score": 0.95,
      "fit_units": 4
    },
    {
      "domain": "text",
      "id": "z",
      "valid_score": 0.9,
      "test_score": 1,
      "fit_units": 1
    },
    {
      "domain": "text",
      "id": "a",
      "valid_score": 0.9,
      "test_score": 0.2,
      "fit_units": 1
    }
  ]
}
```

```output
{
  "selected": [
    {"domain": "audio", "id": "good", "fit_units": 2},
    {"domain": "text", "id": "a", "fit_units": 1},
    {"domain": "none", "id": null, "fit_units": 0}
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
