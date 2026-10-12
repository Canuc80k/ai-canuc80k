# Ba cách gộp

Có vài model phân loại nhị phân, mỗi model cho xác suất lớp $1$ của từng mẫu. Ba cách gộp quen thuộc có thể cho kết quả khác nhau trên cùng dữ liệu.

Với mỗi mẫu:

1. **Hard voting:** mỗi model bỏ một phiếu cho lớp $1$ nếu xác suất từ $0.5$ trở lên; đoán lớp $1$ khi số phiếu lớp $1$ chiếm quá nửa số model.
2. **Soft voting:** trung bình các xác suất; đoán lớp $1$ khi trung bình từ $0.5$ trở lên.
3. **Trung bình logit:** trung bình các $\log\frac{p}{1-p}$; đoán lớp $1$ khi trung bình từ $0$ trở lên.

Báo dự đoán và độ chính xác (so với `labels`) của mỗi cách.

## Dữ liệu vào

Một đối tượng JSON gồm `probs` ($M$ hàng, mỗi hàng là xác suất của một model trên $N$ mẫu; $M$ lẻ, xác suất trong $(0,1)$) và `labels`.

## Kết quả

Một đối tượng JSON gồm `hard`, `soft`, `logit` và `accuracy` (`{"hard", "soft", "logit"}`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "probs": [
    [0.9, 0.6, 0.4, 0.55],
    [0.4, 0.45, 0.45, 0.55],
    [0.45, 0.48, 0.99, 0.02]
  ],
  "labels": [1, 0, 1, 0]
}
```

```output
{
  "hard": [0, 0, 0, 1],
  "soft": [1, 1, 1, 0],
  "logit": [1, 1, 1, 0],
  "accuracy": {"hard": 0.25, "soft": 0.75, "logit": 0.75}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
