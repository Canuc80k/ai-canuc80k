# Detach và clone

`detach()` cắt đường gradient nhưng vẫn dùng chung vùng nhớ với tensor gốc. `detach().clone()` mới tạo một bản sao độc lập. Bài này kiểm cả hai điều ấy.

Cho tensor `x` cần gradient và tốc độ học `learning_rate`.

1. Tính gradient của $\sum x^3$ theo `x`, gọi là `attached_grad`.
2. Xóa gradient, rồi tính gradient của $\sum (\text{x.detach()})^2\cdot x$ theo `x`, gọi là `detached_grad`. Giá trị forward như cũ, nhưng một phần đường đi đã bị cắt.
3. Tạo `alias = x.detach()` và `snapshot = x.detach().clone()`.
4. Trong khối `torch.no_grad()`, cập nhật tại chỗ `x -= learning_rate * attached_grad`.

Báo lại `alias` và `snapshot` sau bước cập nhật.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `x` và `learning_rate`.

## Kết quả

Một đối tượng JSON gồm `attached_grad`, `detached_grad`, `alias_after_update` (giá trị của `alias`) và `clone_before` (giá trị của `snapshot`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [
    -0.025661605931689643, -0.2698080588775131, -1.7578144276508583,
    0.6392774740149706, -0.5579296520252873, 0.626881764410742
  ],
  "learning_rate": 0.01
}
```

```output
{
  "attached_grad": [
    0.001975554056979987, 0.2183891659057547, 9.269734686172542,
    1.2260270663488841, 0.9338564898271746, 1.178942239652175
  ],
  "detached_grad": [
    0.000658518018993329, 0.07279638863525156, 3.0899115620575146,
    0.4086756887829614, 0.3112854966090582, 0.39298074655072496
  ],
  "alias_after_update": [
    -0.025681361472259443, -0.2719919505365706, -1.8505117745125836,
    0.6270172033514817, -0.5672682169235591, 0.6150923420142203
  ],
  "clone_before": [
    -0.025661605931689643, -0.2698080588775131, -1.7578144276508583,
    0.6392774740149706, -0.5579296520252873, 0.626881764410742
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
