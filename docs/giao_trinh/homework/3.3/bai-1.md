# Đạo hàm activation

Một activation không chỉ quyết định giá trị đầu ra mà còn quyết định gradient đi qua được bao nhiêu. Bài này cho thấy ở đâu cổng mở, ở đâu dốc gần như phẳng.

Cho một list số `x` và tên activation: `relu`, `tanh` hoặc `sigmoid`. Hãy tính giá trị activation tại từng phần tử, và đạo hàm của tổng các giá trị ấy theo từng phần tử.

Đạo hàm của ReLU tại $0$ lấy bằng $0$, theo quy ước của PyTorch. Dữ liệu có thể có $\pm1000$: sigmoid phải được tính sao cho không tràn số.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `x` và `activation`.

## Kết quả

Một đối tượng JSON gồm `values` và `gradient`, cùng độ dài với `x`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [-1000.0, -3.0, -0.2, 0.0, 0.2, 3.0, 1000.0],
  "activation": "sigmoid"
}
```

```output
{
  "values": [
    0.0, 0.04742587317756679, 0.4501660026875221, 0.5,
    0.549833997312478, 0.9525741268224334, 1.0
  ],
  "gradient": [
    0.0, 0.045176659730912144, 0.24751657271185998, 0.25,
    0.24751657271185995, 0.045176659730912, 0.0
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
