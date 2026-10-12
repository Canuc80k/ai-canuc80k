# IoU

IoU (intersection over union) đo hai box chồng lên nhau bao nhiêu: diện tích phần chung chia diện tích phần hợp. Đây là phép đo nền của mọi bài detection.

Box viết dạng $[x_1,y_1,x_2,y_2]$ theo tọa độ liên tục, với $x_1<x_2$ và $y_1<y_2$. Bề rộng là $x_2-x_1$, không cộng thêm $1$ như cách đếm điểm ảnh cũ. Hai box chỉ chạm nhau ở cạnh thì phần chung bằng $0$.

Cho hai danh sách box `a` ($N$ box) và `b` ($M$ box), hãy tính IoU của mọi cặp.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `a` và `b`.

## Kết quả

Một đối tượng JSON gồm `iou`, ma trận $N\times M$: phần tử hàng $i$ cột $j$ là IoU của `a[i]` và `b[j]`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "a": [[0, 0, 3, 2], [1, 0, 4, 2]],
  "b": [[0, 0, 3, 2], [3, 0, 6, 2], [8, 0, 10, 2]]
}
```

```output
{"iou": [[1.0, 0.0, 0.0], [0.5, 0.2, 0.0]]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
