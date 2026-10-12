# AdamW

AdamW giữ hai trung bình trượt cho từng tọa độ: $m$ của gradient và $v$ của bình phương gradient. Với `torch.optim.AdamW(lr, weight_decay, betas=(0.8, 0.95), eps=1e-8)`, ở bước $t$:

1. $w\leftarrow w(1-\eta\lambda)$: weight decay tách riêng khỏi gradient.
2. $m\leftarrow0.8m+0.2g$, $v\leftarrow0.95v+0.05g^2$.
3. $w\leftarrow w-\eta\,\dfrac{m/(1-0.8^t)}{\sqrt{v/(1-0.95^t)}+10^{-8}}$.

$m$ và $v$ lưu trong optimizer là bản **chưa** hiệu chỉnh; phép chia cho $1-\beta^t$ chỉ dùng khi cập nhật.

Gradient của từng bước được cho sẵn. Hãy chạy AdamW và ghi lại trọng số sau mỗi bước.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `initial`, `gradients`, `lr` và `weight_decay`.

## Kết quả

Một đối tượng JSON gồm `trajectory`, `exp_avg` ($m$ sau bước cuối) và `exp_avg_sq` ($v$ sau bước cuối).

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
    [0.08664480696284696, 1.3083105847073189],
    [0.11471847152241534, 1.2903124575187135],
    [0.1419848496993894, 1.269371676613403],
    [0.16586700904590604, 1.2585639266293858],
    [0.19029387304075543, 1.2521148791547607],
    [0.21226741300052615, 1.2483207492749195]
  ],
  "exp_avg": [-0.753137494954842, 0.05166883955193404],
  "exp_avg_sq": [0.5144498125427832, 0.08121337313687434]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
