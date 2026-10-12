# StepLR

`StepLR(step_size, gamma)` nhân learning rate với `gamma` sau mỗi `step_size` lần gọi `scheduler.step()`. Thứ tự đúng trong vòng lặp là `optimizer.step()` rồi mới `scheduler.step()`.

Có một trọng số vô hướng bắt đầu bằng $1$, mỗi bước gradient luôn bằng $1$, optimizer là `SGD(lr=base_lr)`. Chạy $T$ bước. Ở mỗi bước, ghi learning rate **trước** khi `optimizer.step()`, rồi gọi `optimizer.step()` và `scheduler.step()`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `base_lr`, `gamma`, `step_size` và `T`.

## Kết quả

Một đối tượng JSON gồm `rates` ($T$ số) và `final_weight`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"base_lr": 0.1, "gamma": 0.5, "step_size": 3, "T": 9}
```

```output
{
  "rates": [0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025],
  "final_weight": 0.475
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
