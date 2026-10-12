# Ngân sách

Máy có `budget_minutes` phút để tìm siêu tham số. Mỗi lần fit mô hình mất `fit_minutes` phút, dù dữ liệu nhiều hay ít. Mỗi cấu hình được chấm bằng `cv_runs` lần chia train và validation, tức `cv_runs` lần fit. Nếu `refit` là `true`, còn phải dành thêm một lần fit để học lại cấu hình thắng trên toàn bộ dữ liệu.

Hãy tính ba điều.

**Grid search.** Một số siêu tham số đã chốt số giá trị cần thử, ghi trong `fixed_counts`. Còn một siêu tham số tự do. Với grid gồm mọi tổ hợp, có thể thử nhiều nhất bao nhiêu giá trị của tham số tự do mà không vượt ngân sách? Gọi số ấy là `free_values`, và `grid_fits` là tổng số lần fit khi đó, kể cả lần fit lại nếu có.

**Random search.** Nếu không chia theo grid mà bốc ngẫu nhiên từng cấu hình, ngân sách đủ cho bao nhiêu cấu hình? Gọi là `random_trials`.

**Xác suất trúng.** Giả sử một tỉ lệ `top_fraction` các cấu hình được xem là "tốt", và mỗi lần bốc độc lập với nhau. Xác suất để ít nhất một trong `random_trials` lần bốc rơi vào nhóm tốt là bao nhiêu? Gọi là `hit_probability`.

## Dữ liệu vào

Một đối tượng JSON gồm `budget_minutes`, `fit_minutes`, `cv_runs`, `fixed_counts`, `refit`, `top_fraction`. Các số phút là số nguyên.

## Kết quả

Một đối tượng JSON gồm `free_values`, `grid_fits`, `random_trials`, `hit_probability`.

## Giới hạn

- Ngân sách không quá $10^5$ phút và luôn đủ cho ít nhất một cấu hình cộng một lần fit lại. Có thể grid không thử nổi giá trị nào của tham số tự do.
- `fixed_counts` có không quá $3$ phần tử, mỗi phần tử từ $2$ đến $10$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "budget_minutes": 6000,
  "fit_minutes": 60,
  "cv_runs": 4,
  "fixed_counts": [8],
  "refit": false,
  "top_fraction": 0.05
}
```

```output
{
  "free_values": 3,
  "grid_fits": 96,
  "random_trials": 25,
  "hit_probability": 0.7226104268781659
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
