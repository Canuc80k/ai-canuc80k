# Chiếu đặc trưng

Một batch gồm $B$ chuỗi, mỗi chuỗi có $L$ vị trí, mỗi vị trí là một vector $d$ đặc trưng. Ta xếp chúng thành tensor `X` có shape `(B, L, d)`. Một lớp tuyến tính với ma trận `W` shape `(d, h)` và bias `b` shape `(h,)` biến mỗi vị trí thành vector $h$ chiều.

Hãy tính:

- `projected = X @ W + b`, shape `(B, L, h)`. Phép nhân chỉ gộp chiều đặc trưng cuối cùng, hai chiều batch và vị trí giữ nguyên.
- `pooled`: trung bình của `projected` theo chiều vị trí, shape `(B, h)`.

Kể cả khi $B=1$ hoặc $L=1$, giữ nguyên số chiều của kết quả.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X`, `W` và `b`.

## Kết quả

Một đối tượng JSON gồm `projected` và `pooled`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[[-0.025661605931689643, -0.2698080588775131]]],
  "W": [
    [-1.7578144276508583, 0.6392774740149706, -0.5579296520252873],
    [0.626881764410742, -0.8309120423662885, 0.5852517710026026]
  ],
  "b": [-0.5710878399185039, 0.09653092353703967, 1.5783323390001442]
}
```

```output
{
  "projected": [[[-0.6951172507764617, 0.30431280216665973, 1.4347440655791828]]],
  "pooled": [[-0.6951172507764617, 0.30431280216665973, 1.4347440655791828]]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
