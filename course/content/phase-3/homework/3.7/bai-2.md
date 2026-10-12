# Đếm bộ nhớ

Trước khi đưa mô hình lên GPU, nên ước lượng xem nó cần bao nhiêu bộ nhớ. Bài này đếm phần cố định theo tham số và phần attention score theo độ dài chuỗi.

Dựng mạng `Linear(d, h)`, `ReLU`, `Linear(h, c)` kiểu `float32` và đếm số tham số $P$. Hãy báo:

- `parameters`: $P$.
- `actual_parameter_bytes`: số byte trọng số đo thật từ các tham số (`numel() * element_size()`).
- `gradient_bytes_estimate`: $4P$, gradient FP32.
- `adam_moment_bytes_estimate`: $8P$, hai moment của Adam.
- `attention_scores_bytes_estimate`: $4\cdot B\cdot\text{heads}\cdot L^2$, kích thước một tensor attention score FP32 shape `(B, heads, L, L)` nếu tạo trọn.

Đây là ước lượng: chưa tính activation, vùng nhớ tạm và phần dư của bộ cấp phát.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `d`, `h`, `c`, `B`, `heads` và `L`.

## Kết quả

Một đối tượng JSON gồm năm trường ở trên.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"d": 3, "h": 5, "c": 2, "B": 2, "heads": 4, "L": 128}
```

```output
{
  "parameters": 32,
  "actual_parameter_bytes": 128,
  "gradient_bytes_estimate": 128,
  "adam_moment_bytes_estimate": 256,
  "attention_scores_bytes_estimate": 524288
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
