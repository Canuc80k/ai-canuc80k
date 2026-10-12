# Loss một epoch

Trong một epoch, mỗi batch cho một giá trị loss là trung bình trên các mẫu của batch ấy. Lấy trung bình cộng các giá trị này là sai khi batch cuối nhỏ hơn: mẫu trong batch nhỏ bị tính nặng hơn. Loss đúng của epoch là trung bình theo **mẫu**.

Cho dự đoán và nhãn đã có sẵn. Đi qua chúng bằng `DataLoader` với kích thước batch `bs`, không xáo. Với mỗi batch, tính MSE trung bình trong batch. Loss epoch là tổng của (loss batch nhân số mẫu của batch), chia cho tổng số mẫu.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `prediction`, `target` (cùng độ dài) và `bs`.

## Kết quả

Một đối tượng JSON gồm `batch_losses` và `epoch_loss`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "prediction": [
    0.05664480707558154, 1.3383105844670897, -2.661117367790814,
    1.2488079457592625, -1.4633738908484955, -0.056744283289588186,
    -1.305060783353052
  ],
  "target": [
    0.5782487847576361, -0.4881346870352931, -0.33159200937462463,
    -1.1359817377211683, -0.14429726438224788, -0.4049118790486861,
    -0.0960294117616615
  ],
  "bs": 4
}
```

```output
{
  "batch_losses": [3.680470817316481, 1.1076468929061354],
  "epoch_loss": 2.57783199256919
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
