# k-NN đánh giá

Học tự giám sát xong, làm sao biết encoder có tốt không mà chưa phải huấn luyện thêm gì? Một cách rẻ: giữ nguyên encoder, lấy embedding của ảnh train có nhãn, rồi phân loại ảnh test bằng $k$ láng giềng gần nhất. Bài này so một encoder chưa học (`random_init`) với một encoder đã học (`ssl_trained`) theo cách ấy.

Với mỗi encoder và mỗi $k$ trong `ks`:

1. Chuẩn hóa mọi embedding về độ dài $1$ (chia cho $\max(\lVert v\rVert,10^{-12})$). Độ giống là tích vô hướng, tức cosine.
2. Với mỗi ảnh test, lấy $k$ ảnh train giống nhất (bằng nhau thì ảnh train đứng trước được chọn trước).
3. Mỗi láng giềng bỏ cho nhãn của nó một phiếu nặng $e^{s/T}$, với $s$ là độ giống và $T$ là `temperature`. Nhãn có tổng phiếu lớn nhất là dự đoán.

$T$ nhỏ làm láng giềng giống nhất áp đảo; $T$ lớn làm mọi láng giềng gần như ngang phiếu.

## Dữ liệu vào

Một đối tượng JSON gồm `train_labels`, `test_labels` (nhãn là số nguyên từ $0$), `ks`, `temperature` và `encoders`: từ tên encoder tới `{"train", "test"}`, hai bảng embedding.

## Kết quả

Một đối tượng JSON: với mỗi tên encoder là `{"accuracy", "predictions"}`, trong đó `accuracy` là độ chính xác trên test theo từng $k$ (cùng thứ tự với `ks`), `predictions` là dự đoán với $k$ đầu tiên trong `ks`.

## Giới hạn

- Không quá $16$ ảnh train và $8$ ảnh test. Không có hai độ giống, hay hai tổng phiếu dẫn đầu, sát nhau dưới $10^{-6}$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "train_labels": [1, 1, 0, 0, 0, 0, 1, 0, 1],
  "test_labels": [0, 0, 1, 1, 0, 1],
  "encoders": {
    "random_init": {
      "train": [
        [2.29, -4.57, 4.09, -3.85],
        [3.97, 1.46, 1.84, -5.91],
        [3.41, -5.62, -0.82, 2.2],
        [4.41, -4.57, 2.2, -1.49],
        [8.19, -4.24, 0.41, 3.32],
        [6.28, -2.42, 3.81, 1.14],
        [9.45, -3.68, 5.49, 1.14],
        [4.91, -5.41, 0.72, 2.27],
        [-0.34, -2.97, 2.97, -5.19]
      ],
      "test": [
        [9.17, -1.19, -0.96, 4.53],
        [2.47, -4.55, -3.15, 2.43],
        [2.71, 1.53, 5.51, -7.85],
        [5.44, -2.4, 3.9, -2.74],
        [6.98, -7.9, 1.14, 1.13],
        [5.38, 1.77, 1.65, -2.38]
      ]
    },
    "ssl_trained": {
      "train": [
        [0.08, 0.39, 0.84, 2.28],
        [-0.3, 0.9, -0.18, 2.15],
        [1.62, -0.28, 1.23, 0.99],
        [2.03, -0.34, 1.22, 0.68],
        [1.87, -1.38, 1.58, 1.04],
        [1.69, -0.1, 1.64, 1.14],
        [0.79, -0.06, 0.43, 1.95],
        [1.66, 0.18, 1.5, 0.52],
        [0.61, 1.19, 0.47, 2.23]
      ],
      "test": [
        [1.45, -0.41, 1.4, 1.56],
        [2.2, 0.08, 1.87, 0.77],
        [0.26, 0.34, 0.47, 2.04],
        [0.07, 0.66, 0.28, 1.93],
        [2.44, -0.28, 1.78, 0.76],
        [-0.09, 0.15, 0.19, 2.59]
      ]
    }
  },
  "ks": [3, 7],
  "temperature": 0.5
}
```

```output
{
  "random_init": {
    "accuracy": [0.8333333333333334, 0.8333333333333334],
    "predictions": [0, 0, 1, 0, 0, 1]
  },
  "ssl_trained": {"accuracy": [1.0, 1.0], "predictions": [0, 0, 1, 1, 0, 1]}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
