# Hai learning rate

Khi mở cả encoder để học, người ta thường cho encoder bước nhỏ hơn head, vì encoder đã học tốt rồi. PyTorch làm việc ấy bằng nhóm tham số: mỗi nhóm có learning rate riêng.

Mô hình thu gọn còn hai số: encoder $w$ và head $a$, dự đoán $\hat y=a\,w\,x$, loss $(\hat y-y)^2$ với $y$ là `target`. Hãy tạo `SGD` với hai nhóm tham số, nhóm encoder có learning rate `encoder_lr` và nhóm head có `head_lr`, rồi làm đúng một bước. Cả hai gradient được tính từ giá trị cũ, trước khi cập nhật.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `x`, `w`, `a`, `target`, `encoder_lr` và `head_lr`.

## Kết quả

Một đối tượng JSON gồm `encoder` ($w$ mới), `head` ($a$ mới), `grad_encoder` và `grad_head`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": 1.0,
  "w": 2.0,
  "a": 1.0,
  "target": 3.0,
  "encoder_lr": 0.01,
  "head_lr": 0.1
}
```

```output
{"encoder": 2.02, "head": 1.4, "grad_encoder": -2.0, "grad_head": -4.0}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
