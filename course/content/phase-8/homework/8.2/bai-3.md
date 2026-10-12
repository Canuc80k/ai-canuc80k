# Rò rỉ theo nguồn

Nhiều ảnh chụp từ cùng một camera (hay nhiều câu của cùng một tài liệu) giống nhau ở những chi tiết không liên quan tới nhãn. Nếu cùng một nguồn có mặt ở cả train lẫn validation, mô hình có thể "nhận ra nguồn" thay vì học điều cần học, và validation đẹp giả.

Mỗi hàng có `id`, `source` và `split` (`train` hoặc `valid`).

1. Nguồn bị rò rỉ là nguồn có mặt ở cả hai phía; xếp theo thứ tự chuỗi.
2. Đếm số hàng validation thuộc nguồn bị rò rỉ, và tỉ lệ của chúng trong validation.
3. Liệt kê mã các hàng validation **không** bị rò rỉ, theo thứ tự trong dữ liệu.

## Dữ liệu vào

Một đối tượng JSON gồm `rows`.

## Kết quả

Một đối tượng JSON gồm `leaked_sources`, `leaked_valid_rows`, `leak_rate` và `clean_valid_ids`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "rows": [
    {"id": "r00", "source": "cam1", "split": "train"},
    {"id": "r01", "source": "cam1", "split": "valid"},
    {"id": "r02", "source": "cam2", "split": "train"},
    {"id": "r03", "source": "cam2", "split": "train"},
    {"id": "r04", "source": "cam3", "split": "valid"},
    {"id": "r05", "source": "cam3", "split": "valid"},
    {"id": "r06", "source": "cam2", "split": "valid"},
    {"id": "r07", "source": "cam4", "split": "train"}
  ]
}
```

```output
{
  "leaked_sources": ["cam1", "cam2"],
  "leaked_valid_rows": 2,
  "leak_rate": 0.5,
  "clean_valid_ids": ["r04", "r05"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
