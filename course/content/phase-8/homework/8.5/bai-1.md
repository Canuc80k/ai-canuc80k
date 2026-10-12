# Kiểm tệp nộp

Mô hình tốt mà tệp nộp hỏng thì vẫn $0$ điểm. Trước mỗi lần nộp, hãy kiểm tệp CSV bằng chính máy: đọc lại tệp như bộ chấm đọc.

Tệp nộp có tiêu đề đúng bằng `columns` (cột mã rồi cột xác suất), mỗi mã cần nộp xuất hiện đúng một lần, và xác suất là số hữu hạn trong $[\text{min},\text{max}]$.

1. Đọc tệp bằng `csv` của Python. Nếu dòng đầu khác `columns`, chỉ báo lỗi `header`, các danh sách khác rỗng.
2. Với mỗi dòng dữ liệu: dòng có số ô khác số cột thì mã (ô đầu) ghi vào `bad_values`. Ngược lại, mã xuất hiện lần thứ hai trở đi ghi vào `duplicates` (mỗi mã một lần, theo thứ tự gặp); giá trị không đọc được thành số, không hữu hạn (`nan`, `inf`) hay ngoài miền thì mã ghi vào `bad_values` (theo thứ tự dòng).
3. `missing`: các mã trong `ids` không có trong tệp (theo thứ tự `ids`); `extra`: các mã có trong tệp mà không cần nộp (theo thứ tự chuỗi).
4. `errors` liệt kê, theo thứ tự `missing`, `extra`, `duplicates`, `bad_values`, những danh sách khác rỗng. Tệp hợp lệ khi không có lỗi nào.

Mã là chuỗi: `"002"` và `"2"` là hai mã khác nhau.

## Dữ liệu vào

Một đối tượng JSON gồm `columns`, `ids`, `min`, `max` và `csv` (nội dung tệp).

## Kết quả

Một đối tượng JSON gồm `valid`, `errors`, `missing`, `extra`, `duplicates` và `bad_values`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "columns": ["id", "prob"],
  "ids": ["002", "2", "a7", "b1"],
  "min": 0.0,
  "max": 1.0,
  "csv": "id,prob\n002,0.91\n2,1.2\na7,nan\na7,0.3\nzz,0.5\n"
}
```

```output
{
  "valid": false,
  "errors": ["missing", "extra", "duplicates", "bad_values"],
  "missing": ["b1"],
  "extra": ["zz"],
  "duplicates": ["a7"],
  "bad_values": ["2", "a7"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
