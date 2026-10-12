# Momentum

Momentum nhớ hướng đi trước, như viên bi lăn có quán tính. Với `torch.optim.SGD(momentum=mu)` (không dampening, không Nesterov), mỗi bước:

$$
v\leftarrow\mu v+g,\qquad w\leftarrow w-\eta v,
$$

với $v$ ban đầu bằng $0$.

Bài này không có hàm loss: gradient của từng bước được cho sẵn. Hãy gán chúng vào `.grad` rồi gọi `optimizer.step()`, ghi lại trọng số sau mỗi bước.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `initial` (trọng số ban đầu, hai số), `gradients` (mỗi bước hai số), `lr` và `momentum`.

## Kết quả

Một đối tượng JSON gồm `trajectory` (trọng số sau mỗi bước) và `momentum_buffer` ($v$ sau bước cuối).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "initial": [0.05664480707558154, 1.3383105844670897],
  "gradients": [
    [-2.661117367790814, 1.2488079457592625],
    [-1.4633738908484955, -0.056744283289588186],
    [-1.305060783353052, 0.5782487847576361],
    [-0.4881346870352931, -0.33159200937462463],
    [-1.1359817377211683, -0.14429726438224788],
    [-0.4049118790486861, -0.0960294117616615]
  ],
  "lr": 0.03,
  "momentum": 0.8,
  "weight_decay": 0.0
}
```

```output
{
  "trajectory": [
    [0.13647832810930596, 1.3008463460943118],
    [0.24424636166174038, 1.272577283894777],
    [0.3696126120042795, 1.2326145705924203],
    [0.4845496528893696, 1.2105921602317735],
    [0.6105787377290767, 1.1973031498747235],
    [0.723549361972303, 1.1895528239419335]
  ],
  "momentum_buffer": [-3.76568747477421, 0.25834419775967005]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
