# AP một lớp

AP (average precision) chấm một detector trên một lớp. Bài này tính AP cho một ảnh, một lớp, theo cách ghép box quen thuộc.

Có các box thật `gt` và các box dự đoán `boxes` cùng điểm `scores` (đôi một khác nhau).

1. Xét các box dự đoán theo điểm giảm dần. Với mỗi box, tìm trong các box thật **chưa được ghép** box có IoU lớn nhất (hòa thì box thật số nhỏ). Nếu IoU ấy ít nhất $0.5$, ghép hai box và ghi TP (cờ $1$); ngược lại ghi FP (cờ $0$). Một box thật đã ghép thì không ghép lần nữa, nên box trùng lặp là FP.
2. Sau $k$ box đầu: precision là số TP chia $k$, recall là số TP chia số box thật.
3. Với mỗi mức recall $r=0,0.01,\dots,1$ ($101$ mức), lấy precision lớn nhất trong các vị trí có recall ít nhất $r$, hoặc $0$ nếu không có. AP101 là trung bình $101$ số ấy.

Box viết dạng $[x_1,y_1,x_2,y_2]$ theo tọa độ liên tục, như bài A.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `gt`, `boxes` và `scores`.

## Kết quả

Một đối tượng JSON gồm `tp_flags`, `precision`, `recall` (theo thứ tự điểm giảm dần) và `ap101`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "gt": [[0, 0, 3, 2], [8, 0, 10, 2]],
  "boxes": [[0, 0, 3, 2], [1, 0, 4, 2], [0.01, 0, 3.01, 2], [8, 0, 10, 2]],
  "scores": [0.9, 0.95, 0.8, 0.7]
}
```

```output
{
  "tp_flags": [1, 0, 0, 1],
  "precision": [1.0, 0.5, 0.3333333333333333, 0.5],
  "recall": [0.5, 0.5, 0.5, 1.0],
  "ap101": 0.7524752475247525
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
