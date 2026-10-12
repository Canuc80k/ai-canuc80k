# Vòng lặp SGD

Bài này tự viết lại một vòng huấn luyện mini-batch mà không dùng PyTorch: mô hình tuyến tính $\hat y=w\cdot x+b$, loss MSE, cập nhật bằng SGD.

Mỗi epoch dùng một thứ tự mẫu cho sẵn trong `orders` (đã xáo trước). Cắt thứ tự ấy thành các batch liên tiếp, mỗi batch `batch_size` mẫu; batch cuối có thể ít hơn, và bị bỏ nếu `drop_last` bật. Với mỗi batch, theo đúng thứ tự:

1. Tính loss của batch: trung bình $(\hat y-y)^2$ trên các mẫu trong batch, với $w$, $b$ hiện tại.
2. Tính gradient của loss ấy theo $w$ và $b$.
3. Cập nhật $w\leftarrow w-\eta\,\nabla_w$, $b\leftarrow b-\eta\,\nabla_b$ với $\eta$ là `learning_rate`.

Loss của một epoch là trung bình theo mẫu của các loss batch đã tính ở bước 1, tức tổng (loss batch nhân số mẫu) chia cho số mẫu đã dùng. Epoch không có batch nào thì loss ghi `null`.

## Dữ liệu vào

Một đối tượng JSON gồm `X` ($n$ hàng, mỗi hàng $d$ số), `y`, `w` ($d$ số), `b`, `learning_rate`, `batch_size`, `drop_last` và `orders` (mỗi epoch một hoán vị của $0,\dots,n-1$).

## Kết quả

Một đối tượng JSON gồm `epoch_losses`, `weights` (sau mỗi epoch, list $w$ nối thêm $b$ ở cuối) và `steps` (tổng số bước cập nhật).

## Giới hạn

- $n\le15$, $d\le3$, không quá $4$ epoch.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[1.0], [2.0], [3.0], [4.0], [5.0]],
  "y": [2.0, 4.0, 6.0, 8.0, 10.0],
  "w": [0.0],
  "b": 0.0,
  "learning_rate": 0.02,
  "batch_size": 2,
  "drop_last": false,
  "orders": [[0, 1, 2, 3, 4], [4, 2, 0, 3, 1]]
}
```

```output
{
  "epoch_losses": [23.157240448000003, 0.07618415892473632],
  "weights": [[1.92656, 0.535872], [1.8539522908160002, 0.505398878208]],
  "steps": 6
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
