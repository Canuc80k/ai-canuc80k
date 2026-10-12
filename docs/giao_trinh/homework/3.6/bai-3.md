# Early stopping

Early stopping theo dõi loss trên validation sau mỗi epoch và dừng khi lâu không thấy tiến bộ. Quy tắc trong bài:

- Ban đầu, giá trị tốt nhất là vô cùng.
- Epoch có loss $L$ được tính là **tiến bộ** nếu $L+\text{min\_delta}$ nhỏ hơn giá trị tốt nhất (bằng nhau thì không tính). Khi ấy cập nhật giá trị tốt nhất, nhớ epoch này, và đặt bộ đếm về $0$.
- Ngược lại, tăng bộ đếm thêm $1$. Bộ đếm chạm `patience` thì dừng ngay ở epoch ấy, không đọc các epoch sau.

So sánh theo đúng giá trị thập phân của các số trong dữ liệu.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `validation_losses`, `patience` và `min_delta`.

## Kết quả

Một đối tượng JSON gồm `best_epoch` (đánh từ $1$), `best_loss`, `stop_epoch` (epoch dừng, hoặc `null` nếu chạy hết mà chưa dừng) và `epochs_processed`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "validation_losses": [0.5, 0.46, 0.455, 0.45, 0.453, 0.452, 0.451, 0.5, 0.7],
  "patience": 2,
  "min_delta": 0.004
}
```

```output
{
  "best_epoch": 4,
  "best_loss": 0.45,
  "stop_epoch": 6,
  "epochs_processed": 6
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
