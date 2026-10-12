# Thêm cây

Một Random Forest tăng số cây từ $100$ lên $1000$: độ chính xác trên train nhích lên, còn trên validation đứng yên. Bài này tái hiện hiện tượng ấy trên các phiếu bầu cho sẵn của từng cây, và đo xem các cây sai giống nhau tới mức nào.

Có $M$ cây ($M$ lẻ). `train_votes[t][i]` là nhãn ($0$ hoặc $1$) cây $t$ đoán cho mẫu train $i$; tương tự `valid_votes`.

1. Với mỗi $k$ (lẻ) trong `ks`: dùng $k$ cây **đầu tiên**, đoán lớp $1$ khi quá nửa số phiếu là $1$. Báo độ chính xác trên train và trên validation.
2. `mean_single_valid`: độ chính xác trên validation của từng cây, lấy trung bình.
3. `mean_error_correlation`: với mỗi cây, dãy lỗi trên validation là $1$ nếu cây đoán sai mẫu ấy, $0$ nếu đúng. Tính hệ số tương quan Pearson giữa dãy lỗi của mọi cặp cây, bỏ các cặp có một dãy không đổi (luôn đúng hoặc luôn sai), rồi lấy trung bình.

## Dữ liệu vào

Một đối tượng JSON gồm `train_votes`, `train_labels`, `valid_votes`, `valid_labels` và `ks`.

## Kết quả

Một đối tượng JSON gồm `curve` (với mỗi $k$ là `{"k", "train", "valid"}`), `mean_single_valid` và `mean_error_correlation`.

## Giới hạn

- Không quá $15$ cây và $24$ mẫu mỗi tập. Có ít nhất hai cây có dãy lỗi thay đổi (không phải luôn đúng hay luôn sai).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "train_votes": [
    [
      0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
      1, 0
    ],
    [
      0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
      1, 0
    ],
    [
      0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1,
      1, 0
    ],
    [
      1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
      1, 0
    ],
    [
      0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1,
      1, 0
    ],
    [
      0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
      1, 0
    ],
    [
      0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
      1, 0
    ],
    [
      0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
      1, 0
    ],
    [
      0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
      1, 0
    ]
  ],
  "train_labels": [
    0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
    1, 0
  ],
  "valid_votes": [
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0]
  ],
  "valid_labels": [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
  "ks": [1, 3, 5, 7]
}
```

```output
{
  "curve": [
    {"k": 1, "train": 0.9583333333333334, "valid": 0.5833333333333334},
    {"k": 3, "train": 1.0, "valid": 0.9166666666666666},
    {"k": 5, "train": 0.9583333333333334, "valid": 0.8333333333333334},
    {"k": 7, "train": 0.9583333333333334, "valid": 0.8333333333333334}
  ],
  "mean_single_valid": 0.6759259259259259,
  "mean_error_correlation": 0.14143085159207097
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 2](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=3).
:::
