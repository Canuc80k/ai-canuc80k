# RNN đóng gói

Một RNN đọc câu đã chèn PAD sẽ đọc luôn cả PAD, và trạng thái cuối không còn là trạng thái sau từ thật cuối cùng. `pack_padded_sequence` báo cho RNN độ dài thật của từng câu.

Dựng `nn.RNN(input_size=2, hidden_size=3, num_layers=1, nonlinearity="tanh", batch_first=True)` kiểu `float64` và chép trọng số `W_ih`, `W_hh`, `b_ih`, `b_hh` vào. Trạng thái ban đầu bằng $0$.

Chèn PAD cho các chuỗi bằng `pad_sequence`, đóng gói bằng `pack_padded_sequence(..., enforce_sorted=False)` với độ dài nằm trên CPU, rồi chạy RNN. Trả trạng thái ẩn cuối $h_n$ của từng chuỗi, theo **đúng thứ tự ban đầu** của các chuỗi.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `sequences` (mỗi chuỗi có ít nhất một bước, mỗi bước hai số), `W_ih` ($3\times2$), `W_hh` ($3\times3$), `b_ih`, `b_hh`.

## Kết quả

Một đối tượng JSON `{"last_valid": [...]}`, mỗi chuỗi một vector ba số.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "sequences": [
    [[-0.661, 1.458], [1.028, -1.21]],
    [
      [-0.645, -1.087],
      [-0.97, -0.081],
      [-0.726, -1.807],
      [1.75, -0.355],
      [-0.536, 1.998]
    ],
    [[-0.154, 0.094]]
  ],
  "W_ih": [[-0.5, -0.253], [0.024, 0.184], [0.227, -0.297]],
  "W_hh": [
    [0.303, -0.234, 0.315],
    [-0.148, 0.014, 0.127],
    [-0.109, -0.002, 0.256]
  ],
  "b_ih": [-0.077, -0.039, 0.114],
  "b_hh": [0.184, -0.027, 0.119]
}
```

```output
{
  "last_valid": [
    [-0.22527740207171584, -0.304304653520827, 0.6241410512898957],
    [0.06283303632461633, 0.3730180431190915, -0.290318889896223],
    [0.15886101002669678, -0.052352093340720975, 0.16850152768472787]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
