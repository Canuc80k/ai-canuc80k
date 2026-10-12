# mIoU và lớp vắng

mIoU (mean IoU) là trung bình IoU của các lớp. Nhưng nếu một lớp vắng mặt trong cả dự đoán lẫn nhãn của một ảnh, hợp của nó bằng $0$ và IoU không xác định. Có ba cách xử lý thường gặp, và chúng cho các con số khác nhau. Bài này tính cả ba.

Mỗi ảnh có mask dự đoán và mask nhãn, mỗi điểm là một lớp $0..C-1$. Với ảnh và lớp $c$: phần giao là số điểm cùng là $c$ ở cả hai mask, phần hợp là số điểm là $c$ ở ít nhất một mask; IoU là giao chia hợp.

Với mỗi ảnh, mIoU theo ba cách khi hợp bằng $0$:

- `skip`: bỏ lớp ấy, lấy trung bình trên các lớp còn lại.
- `absent_is_1`: coi IoU bằng $1$ (cả hai cùng đúng là không có).
- `absent_is_0`: coi IoU bằng $0$.

Thêm danh sách lớp vắng mặt của mỗi ảnh, trung bình của mỗi cách trên các ảnh, và cách gộp trên cả tập: cộng giao và hợp của mỗi lớp qua mọi ảnh rồi mới chia, sau đó lấy trung bình trên các lớp.

## Dữ liệu vào

Một đối tượng JSON gồm `num_classes`, `predictions` và `targets` (các mask cùng cỡ).

## Kết quả

Một đối tượng JSON gồm:

- `per_image`: với mỗi ảnh là `{"skip", "absent_is_1", "absent_is_0", "absent_classes"}`.
- `mean`: `{"skip", "absent_is_1", "absent_is_0"}`, trung bình trên các ảnh.
- `dataset_class_iou`: IoU gộp của từng lớp, và `dataset_miou`: trung bình của chúng.

## Giới hạn

- Không quá $4$ lớp và $4$ ảnh. Mỗi ảnh có ít nhất một lớp có mặt; trên cả tập, lớp nào cũng có mặt.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "num_classes": 3,
  "predictions": [
    [
      [0, 0, 0, 0, 0, 0],
      [0, 1, 1, 1, 0, 0],
      [0, 1, 1, 1, 0, 0],
      [0, 0, 0, 0, 0, 0]
    ],
    [
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]
    ]
  ],
  "targets": [
    [
      [0, 0, 0, 0, 0, 0],
      [0, 1, 1, 0, 0, 0],
      [0, 1, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]
    ],
    [
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 2, 0],
      [0, 0, 0, 0, 0, 0]
    ]
  ]
}
```

```output
{
  "per_image": [
    {
      "skip": 0.7833333333333333,
      "absent_is_1": 0.8555555555555555,
      "absent_is_0": 0.5222222222222223,
      "absent_classes": [2]
    },
    {
      "skip": 0.4791666666666667,
      "absent_is_1": 0.6527777777777778,
      "absent_is_0": 0.3194444444444445,
      "absent_classes": [1]
    }
  ],
  "mean": {
    "skip": 0.63125,
    "absent_is_1": 0.7541666666666667,
    "absent_is_0": 0.4208333333333334
  },
  "dataset_class_iou": [0.9318181818181818, 0.6666666666666666, 0.0],
  "dataset_miou": 0.5328282828282828
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 14](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=20).
:::
