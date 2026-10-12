# Nucleus

Khi sinh văn bản, mô hình cho logits của token tiếp theo; ta lọc bớt rồi mới lấy mẫu. Bài này làm một bước lọc gồm temperature, top-$k$ và nucleus (top-$p$), rồi lấy mẫu bằng một số ngẫu nhiên $u$ cho sẵn.

1. Chia logits cho `temperature`.
2. Xếp token theo logit giảm dần (bằng nhau thì số nhỏ hơn). Nếu $k>0$ chỉ giữ $k$ token đầu; $k=0$ giữ hết.
3. Softmax trên các token đã giữ.
4. **Nucleus:** giữ đoạn đầu ngắn nhất của danh sách mà tổng xác suất từ $p$ trở lên. Token làm tổng vượt ngưỡng **cũng được giữ**. Luôn giữ ít nhất một token.
5. Chuẩn hóa lại xác suất của các token còn lại cho tổng bằng $1$.
6. Lấy mẫu: cộng dồn xác suất theo đúng thứ tự trên, chọn token đầu tiên có tổng cộng dồn **lớn hơn** $u$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `logits`, `temperature`, `k`, `p` và `u`.

## Kết quả

Một đối tượng JSON gồm `retained_ids`, `probabilities` (cùng thứ tự) và `sampled_id`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [0, 0, 0, 0, 0, 0, 0],
  "temperature": 0.5,
  "k": 0,
  "p": 0,
  "u": 0.5
}
```

```output
{"retained_ids": [0], "probabilities": [1.0], "sampled_id": 0}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
