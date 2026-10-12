# Cosine

Tìm các vector gần một vector truy vấn có thể đo bằng tích vô hướng hoặc bằng cosine. Hai cách cho kết quả rất khác nhau khi các vector có độ dài khác nhau: tích vô hướng ưu tiên vector **dài**, cosine chỉ nhìn **hướng**.

Cho vector truy vấn $q$ và một kho vector. Hãy tính:

- `norms`: độ dài của từng vector trong kho.
- `dot_top`: chỉ số $k$ vector có tích vô hướng với $q$ lớn nhất, xếp giảm dần.
- `cos_top`: chỉ số $k$ vector có cosine với $q$ lớn nhất, xếp giảm dần.
- `overlap`: số chỉ số có mặt trong cả hai danh sách.

Hòa thì chỉ số nhỏ đứng trước.

## Dữ liệu vào

Một đối tượng JSON gồm `query`, `database` (các vector khác $0$, cùng số chiều với `query`) và `k`.

## Kết quả

Một đối tượng JSON gồm `norms`, `dot_top`, `cos_top` và `overlap`.

## Giới hạn

- Không quá $12$ vector, mỗi vector không quá $5$ chiều. Không có hai điểm số nào sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "query": [1.0, 0.0],
  "database": [[0.9, 0.1], [5.0, 4.0], [0.0, 1.0], [3.0, -1.0], [0.5, 0.05]],
  "k": 2
}
```

```output
{
  "norms": [
    0.9055385138137417, 6.4031242374328485, 1.0, 3.1622776601683795,
    0.5024937810560445
  ],
  "dot_top": [1, 3],
  "cos_top": [4, 0],
  "overlap": 0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
