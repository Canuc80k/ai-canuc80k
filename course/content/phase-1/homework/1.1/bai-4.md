# Hằng số

Baseline đơn giản nhất là đoán cùng một số $c$ cho mọi mẫu. Nhưng nên chọn $c$ bằng bao nhiêu? Câu trả lời tùy vào thước đo ta dùng để học.

Cho các nhãn train $y_1, \dots, y_n$. Hãy tìm hai hằng số:

- `c_square`: số $c$ làm tổng bình phương sai số $\sum_i (y_i-c)^2$ nhỏ nhất.
- `c_abs`: số $c$ làm tổng trị tuyệt đối sai số $\sum_i |y_i-c|$ nhỏ nhất. Nếu có nhiều số cùng đạt nhỏ nhất, lấy số nhỏ nhất trong chúng.

Rồi chấm cả hai trên tập validation bằng MAE, được `valid_mae_square` và `valid_mae_abs`.

Gợi ý: thử vẽ hai tổng trên như hàm số của $c$ với vài nhãn nhỏ, chẳng hạn $1, 2, 10$. Một tổng là parabol, tổng kia là đường gấp khúc.

## Dữ liệu vào

Một đối tượng JSON gồm hai list số nguyên `train` và `valid`.

## Kết quả

Một đối tượng JSON gồm `c_square`, `c_abs`, `valid_mae_square`, `valid_mae_abs`.

## Giới hạn

- Mỗi list có từ $1$ đến $1000$ phần tử, mỗi nhãn từ $0$ đến $10^4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"train": [20, 30, 40, 100], "valid": [25, 35]}
```

```output
{
  "c_square": 47.5,
  "c_abs": 30,
  "valid_mae_square": 17.5,
  "valid_mae_abs": 5.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
