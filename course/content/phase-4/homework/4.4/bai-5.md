# LoRA và SVD

Giả sử ta biết thay đổi trọng số lý tưởng $\Delta$ cho một nhiệm vụ mới. LoRA hạng $r$ chỉ biểu diễn được các thay đổi dạng $BA$, có hạng không quá $r$. Vậy với mỗi $r$, adapter tốt nhất xấp xỉ $\Delta$ được tới đâu?

Đo sai số bằng chuẩn Frobenius $\lVert\Delta-BA\rVert_F$ (căn của tổng bình phương mọi phần tử). Gọi $\sigma_1\ge\sigma_2\ge\dots$ là các giá trị kỳ dị của $\Delta$. Hãy tính:

- `singular_values`: các $\sigma_i$, giảm dần, có $\min(d_{out},d_{in})$ số.
- `errors`: với mỗi $r$ trong `ranks`, sai số nhỏ nhất đạt được bởi một ma trận hạng không quá $r$.
- `relative_sq_errors`: sai số ấy bình phương, chia cho $\lVert\Delta\rVert_F^2$.
- `best_update`: ma trận hạng không quá `show_rank` gần $\Delta$ nhất.

Có thể dùng `np.linalg.svd`. Hãy tự tìm công thức của sai số theo các $\sigma_i$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `delta` (ma trận $d_{out}\times d_{in}$), `ranks` và `show_rank`.

## Kết quả

Một đối tượng JSON gồm `singular_values`, `errors`, `relative_sq_errors` và `best_update`.

## Giới hạn

- $d_{out},d_{in}\le6$. Ở hạng `show_rank`, hai giá trị kỳ dị liền kề khác nhau rõ rệt.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "delta": [[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.1], [0.0, 0.0, 0.0]],
  "ranks": [0, 1, 2, 3],
  "show_rank": 1
}
```

```output
{
  "singular_values": [2.0, 1.0, 0.1],
  "errors": [2.238302928559939, 1.004987562112089, 0.1, 0.0],
  "relative_sq_errors": [1.0, 0.20159680638722555, 0.0019960079840319364, 0.0],
  "best_update": [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
