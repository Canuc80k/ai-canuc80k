# Microbatch

Batch không vừa bộ nhớ thì chia thành nhiều microbatch, mỗi microbatch `backward()` một lần và cộng dồn gradient, rồi mới cập nhật. Muốn gradient cộng dồn đúng bằng gradient của cả batch, loss của mỗi microbatch phải được nhân với tỉ lệ số mẫu của nó.

Mô hình là hồi quy logistic: logit $z=w\cdot x+b$, loss `BCEWithLogitsLoss` lấy trung bình, kiểu `float64`.

1. Tính gradient theo $(w_0,w_1,b)$ của loss trên cả batch.
2. Với tham số mới, xóa gradient **một lần**, rồi đi qua các microbatch liên tiếp có kích thước cho trong `chunk_sizes`. Với microbatch $n_k$ mẫu, gọi `backward()` trên $\text{loss}_k\cdot n_k/n$. Không gọi `step()` ở giữa.

Hai gradient phải trùng nhau, kể cả khi các microbatch không đều.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (mỗi hàng hai số), `y` (nhãn $0$/$1$), `w`, `b` và `chunk_sizes` (tổng bằng số hàng).

## Kết quả

Một đối tượng JSON gồm `full_gradient` và `accumulated_gradient`, mỗi trường là `[dw0, dw1, db]`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [1.5422810517218632, 1.119727597742594],
    [-0.2506378319437306, -0.23255424701382738],
    [-0.22832924300471708, 0.14137106959292967],
    [0.23485741329208693, -0.2766371964927191],
    [-0.3700277387766048, -0.2841472610562709],
    [0.04250158806403885, -3.0004241679098747],
    [1.6722596366120763, 0.37415017979365056],
    [0.7881280388429539, -1.5666617614455423],
    [1.1647928409848756, -0.25778052058031625],
    [0.13399430148241656, -0.1549172024797579]
  ],
  "y": [1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
  "w": [-1.421901762678799, -0.5727995883664803],
  "b": -0.7994179840763487,
  "chunk_sizes": [3, 3, 3, 1]
}
```

```output
{
  "full_gradient": [-0.20609733256918478, 0.12022941314733968, -0.20615260855536205],
  "accumulated_gradient": [-0.20609733256918478, 0.12022941314733968, -0.20615260855536202]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
