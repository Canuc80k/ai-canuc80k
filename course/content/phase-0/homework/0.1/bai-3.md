# Robot vòng

Một con robot chạy trên đường vòng có `size` ô, đánh số từ $0$ đến $\text{size}-1$, ô cuối nối liền ô $0$. Robot xuất phát ở ô `start` rồi đi lần lượt từng bước trong `steps`. Bước dương đi theo chiều số ô tăng, bước âm đi ngược lại. Có bước rất dài, robot đi hết vòng này sang vòng khác.

Hãy ghi lại hành trình, gồm vị trí ban đầu và vị trí sau mỗi bước.

Gợi ý: với số chia dương, phép `%` của Python luôn cho kết quả từ $0$ đến số chia trừ $1$, kể cả khi số bị chia âm.

## Dữ liệu vào

Một đối tượng JSON gồm `size`, `start` và danh sách `steps`.

## Kết quả

Danh sách vị trí, bắt đầu bằng `start`, rồi lần lượt vị trí sau từng bước.

## Giới hạn

- $1\le\text{size}\le20$ và $0\le\text{start}<\text{size}$.
- Có không quá $100$ bước, mỗi bước dài không quá $10^6$ ô.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"size": 8, "start": 6, "steps": [3, -10, 1]}
```

```output
[6, 1, 7, 0]
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
