# Gradient max pool

Max pooling chỉ cho gradient đi qua ô lớn nhất của mỗi cửa sổ. Khi các cửa sổ chồng lên nhau, một ô có thể thắng ở nhiều cửa sổ, và gradient của nó được **cộng** từ tất cả.

Cho ảnh `X` cỡ $H\times W$, các giá trị khác nhau đôi một. Áp `MaxPool2d(kernel_size=2, stride=1)`, nên các cửa sổ $2\times2$ chồng lên nhau. Loss là tổng mọi ô đầu ra. Hãy tính đầu ra pooling và gradient của loss theo từng ô của `X`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X`.

## Kết quả

Một đối tượng JSON gồm `pooled` (cỡ $(H-1)\times(W-1)$) và `gradient` (cỡ $H\times W$).

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "X": [
    [2.0, 16.0, 1.0, 8.0, 18.0],
    [4.0, 17.0, 12.0, 0.0, 19.0],
    [11.0, 14.0, 6.0, 10.0, 7.0],
    [3.0, 13.0, 15.0, 5.0, 9.0]
  ]
}
```

```output
{
  "pooled": [
    [17.0, 17.0, 12.0, 19.0],
    [17.0, 17.0, 12.0, 19.0],
    [14.0, 15.0, 15.0, 10.0]
  ],
  "gradient": [[0, 0, 0, 0, 0], [0, 4, 2, 0, 2], [0, 1, 0, 1, 0], [0, 0, 2, 0, 0]]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
