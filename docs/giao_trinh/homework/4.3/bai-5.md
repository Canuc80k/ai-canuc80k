# Freeze và eval

"Đóng băng backbone" thường được viết là tắt `requires_grad` cho các tham số của nó. Nhưng BatchNorm còn có running statistics, thứ không phải tham số và không cần gradient để thay đổi. Bài này cho thấy điều đó bằng số.

Backbone gồm một lớp tuyến tính không bias $h=xW$ (theo quy ước hàng, $W$ cỡ $d\times d$) rồi `BatchNorm1d(d, affine=False)` với `momentum`, `eps` cho sẵn, running mean ban đầu bằng $0$ và running var ban đầu bằng $1$. Head là $\hat y=z\cdot v+c$ với $z$ là đầu ra BatchNorm. Backbone bị đóng băng: $W$ không bao giờ đổi. Head học bằng SGD với `lr`, loss MSE trung bình trong batch, mỗi batch một bước.

So hai cách huấn luyện:

- `freeze_train`: backbone vẫn ở chế độ train. BatchNorm chuẩn hóa bằng trung bình và phương sai của chính batch (phương sai chia $n$), và cập nhật running mean, running var (phương sai batch chia $n-1$): $\text{running}\leftarrow(1-\text{momentum})\cdot\text{running}+\text{momentum}\cdot\text{batch}$.
- `freeze_eval`: backbone ở chế độ eval suốt quá trình học. BatchNorm chuẩn hóa bằng running mean, running var, và không cập nhật chúng.

Sau khi học, chuyển cả mô hình sang eval và dự đoán cho các hàng trong `queries`.

## Dữ liệu vào

Một đối tượng JSON gồm `W`, `v`, `c`, `lr`, `momentum`, `eps`, `batches` (mỗi batch ít nhất hai hàng), `targets` (nhãn của từng batch) và `queries`.

## Kết quả

Một đối tượng JSON gồm `freeze_train` và `freeze_eval`, mỗi trường là `{"running_mean": [...], "running_var": [...], "v": [...], "c": ..., "predictions": [...]}`.

## Giới hạn

- $d\le3$, không quá $5$ batch, mỗi batch không quá $6$ hàng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "W": [[1.0, 0.0], [0.0, 2.0]],
  "v": [0.5, -0.5],
  "c": 0.0,
  "lr": 0.1,
  "momentum": 0.5,
  "eps": 1e-05,
  "batches": [[[3.0, 1.0], [5.0, 2.0]], [[4.0, 0.0], [6.0, 1.0]]],
  "targets": [[1.0, 2.0], [1.5, 2.5]],
  "queries": [[4.0, 1.0], [0.0, 0.0]]
}
```

```output
{
  "freeze_train": {
    "running_mean": [3.5, 1.25],
    "running_var": [1.75, 1.75],
    "v": [0.6599995999999999, -0.3400003999999999],
    "c": 0.6400000000000001,
    "predictions": [0.6966941310039111, -0.7849205557840171]
  },
  "freeze_eval": {
    "running_mean": [0.0, 0.0],
    "running_var": [1.0, 1.0],
    "v": [-4.219921900874243, -1.0999830002014983],
    "c": -0.8799895000817496,
    "predictions": [-19.95954770642918, -0.8799895000817496]
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
