# Sửa notebook

Một bạn ghi điểm các lần chạy thử model vào notebook `broken.ipynb` (có trong bộ kit). Lúc làm, bạn ấy chạy các ô lộn xộn nên mọi thứ vẫn có vẻ ổn. Đến khi bấm **Restart & Run All**, notebook báo lỗi ngay.

Notebook có bốn ô:

```py
max = 10
best = max(scores)
scores = ["9", "10", "2"]
print(best)
```

Có ba chỗ sai. `scores` được dùng trước khi gán. Tên `max` bị lấy làm tên biến, nên hàm `max` của Python bị che mất. Còn điểm thì đang là chuỗi, mà so chuỗi thì `"9"` lại lớn hơn `"10"`.

Hãy sửa notebook cho chạy được từ đầu đến cuối. Sau đó viết hàm `solve` nhận danh sách điểm dạng chuỗi và trả về điểm lớn nhất **theo giá trị số**.

## Dữ liệu vào

Một đối tượng JSON có trường `scores`, là danh sách chuỗi số thập phân, ví dụ `"9"`, `"-74.5"`.

## Kết quả

Điểm lớn nhất, dưới dạng một số.

## Giới hạn

- Có từ $1$ đến $100$ điểm, mỗi điểm trong đoạn $[-1000, 1000]$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"scores": ["9", "10", "2"]}
```

```output
10.0
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
