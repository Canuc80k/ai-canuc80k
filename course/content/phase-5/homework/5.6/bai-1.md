# IoU và Dice

Chấm một mô hình phân vùng nhị phân trên vài ảnh. Mỗi ảnh có mask thật `truth` và mask dự đoán `prediction`, gồm các số $0$ (nền) và $1$ (vật).

- IoU của một ảnh: số điểm cùng là $1$ chia số điểm là $1$ ở ít nhất một mask. Nếu cả hai mask đều trống thì mô hình đã đúng hoàn toàn: IoU bằng $1$.
- `mean_foreground_iou`: trung bình IoU của các ảnh.
- Gộp điểm ảnh của mọi ảnh để đếm TP (thật $1$, đoán $1$), FP (thật $0$, đoán $1$), FN (thật $1$, đoán $0$). Dice gộp là $\dfrac{2\,TP}{2\,TP+FP+FN}$, và bằng $1$ nếu mẫu số bằng $0$.

Hai cách gộp này cho kết quả khác nhau: trung bình theo ảnh coi mọi ảnh ngang nhau, còn khi gộp điểm ảnh thì ảnh có vật lớn quyết định nhiều hơn.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `truth` và `prediction`, cùng shape $N\times H\times W$.

## Kết quả

Một đối tượng JSON gồm `per_image_iou`, `mean_foreground_iou`, `micro_dice`, `tp`, `fp` và `fn`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "truth": [
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    [[0, 1, 1, 0, 0], [1, 1, 0, 1, 1], [1, 1, 0, 0, 1], [0, 1, 1, 1, 0]],
    [[1, 1, 1, 1, 1], [0, 0, 0, 1, 0], [1, 0, 1, 0, 0], [1, 0, 0, 1, 1]]
  ],
  "prediction": [
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    [[0, 0, 0, 1, 1], [1, 0, 0, 0, 0], [1, 1, 0, 1, 0], [0, 0, 0, 1, 1]],
    [[0, 0, 1, 1, 1], [1, 1, 1, 0, 0], [1, 0, 0, 1, 1], [0, 0, 0, 0, 0]]
  ]
}
```

```output
{
  "per_image_iou": [1, 0.25, 0.25],
  "mean_foreground_iou": 0.5,
  "micro_dice": 0.4,
  "tp": 8,
  "fp": 9,
  "fn": 15
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
