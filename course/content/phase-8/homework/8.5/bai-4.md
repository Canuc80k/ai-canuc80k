# Đọc lại tệp

Dự đoán trong bộ nhớ đúng, nhưng tệp ghi ra có thể không còn đúng: thêm một cột chỉ số, làm tròn xác suất quá tay, xáo thứ tự hàng, hay một nhãn bị ghi nhầm. Cách chắc nhất là **đọc lại** tệp vừa ghi và so với dự đoán trong bộ nhớ.

`memory` là danh sách dự đoán trong bộ nhớ (mỗi dòng `{"id", "label", "prob"}`); `csv` là nội dung tệp đã ghi, mong đợi có đúng ba cột `id`, `label`, `prob`.

1. `extra_columns`: các tên cột trong dòng tiêu đề không thuộc ba cột trên, theo thứ tự xuất hiện (cột không tên ghi là chuỗi rỗng).
2. `same_id_order`: dãy mã trong tệp có đúng bằng dãy mã trong bộ nhớ không.
3. Với mỗi dòng của tệp có mã trong bộ nhớ: nhãn (đọc như chuỗi) khác nhãn trong bộ nhớ thì ghi mã vào `label_mismatch`; tính độ lệch tuyệt đối của xác suất, `max_prob_diff` là lớn nhất (`null` nếu có ô xác suất không đọc được).
4. `ok` khi không có cột thừa, đúng thứ tự, không lệch nhãn và `max_prob_diff` không vượt `tolerance`.

## Dữ liệu vào

Một đối tượng JSON gồm `memory`, `csv` và `tolerance`.

## Kết quả

Một đối tượng JSON gồm `extra_columns`, `same_id_order`, `label_mismatch`, `max_prob_diff` và `ok`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "memory": [
    {"id": "002", "label": 1, "prob": 0.912345},
    {"id": "2", "label": 0, "prob": 0.2},
    {"id": "a7", "label": 1, "prob": 0.5004}
  ],
  "tolerance": 0.001,
  "csv": ",id,label,prob\n0,002,1,0.91\n1,2,0,0.20\n2,a7,1,0.50\n"
}
```

```output
{
  "extra_columns": [""],
  "same_id_order": true,
  "label_mismatch": [],
  "max_prob_diff": 0.0023449999999999305,
  "ok": false
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
