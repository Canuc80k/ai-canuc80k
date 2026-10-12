# Tích lũy gradient

GPU không đủ bộ nhớ cho batch lớn, ta tích lũy gradient của vài batch nhỏ rồi mới cập nhật một lần. Một đoạn code hay gặp:

```python
optimizer.zero_grad()
for epoch in range(epochs):
    for i, (xb, yb) in enumerate(loader):
        loss = criterion(model(xb), yb)
        if divide:
            loss = loss / accumulation_steps
        loss.backward()
        if (i + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
```

Hãy mô phỏng đúng đoạn code này. Mô hình là $\hat y=w\cdot x$ (không có bias), `criterion` là MSE trung bình trong batch, `optimizer` là SGD với `learning_rate`. `loader` cắt dữ liệu theo thứ tự gốc thành các batch `batch_size` mẫu, batch cuối có thể nhỏ hơn, mọi epoch giống nhau. Để ý `zero_grad()` chỉ được gọi lúc đầu và ngay sau mỗi `step()`.

Hãy báo:

- `steps`, `trajectory`: số lần `step()` và $w$ sau mỗi lần.
- `leftover_batches`: số batch đã `backward()` nhưng gradient còn nằm trong `.grad` khi kết thúc, chưa được dùng.
- `first_grad`: gradient trong `.grad` ngay trước lần `step()` đầu tiên.
- `big_batch_grad`: gradient MSE tại $w$ ban đầu nếu gộp `accumulation_steps` batch đầu tiên thành một batch lớn.

## Dữ liệu vào

Một đối tượng JSON gồm `X`, `y`, `w`, `learning_rate`, `batch_size`, `accumulation_steps`, `epochs` và `divide`.

## Kết quả

Một đối tượng JSON gồm `steps`, `trajectory`, `leftover_batches`, `first_grad` và `big_batch_grad`.

## Giới hạn

- $n\le20$, $d\le3$, không quá $3$ epoch. Epoch đầu luôn có ít nhất một lần `step()`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [1.0, 0.5],
    [2.0, -1.0],
    [0.5, 1.5],
    [-1.0, 2.0],
    [1.5, 0.0],
    [0.0, -2.0],
    [2.5, 1.0],
    [-0.5, -0.5],
    [1.0, 1.0],
    [3.0, 0.5]
  ],
  "y": [1.0, 3.0, -1.0, -3.0, 1.5, 2.0, 1.5, 0.0, 0.0, 2.5],
  "w": [0.0, 0.0],
  "learning_rate": 0.1,
  "batch_size": 2,
  "accumulation_steps": 4,
  "epochs": 2,
  "divide": true
}
```

```output
{
  "steps": 2,
  "trajectory": [[0.3875, -0.3125], [0.73984375, -0.50859375]],
  "leftover_batches": 1,
  "first_grad": [-3.875, 3.125],
  "big_batch_grad": [-3.875, 3.125]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 11](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=16).
:::
