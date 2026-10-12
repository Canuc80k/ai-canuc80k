# Phát hiện bất thường

Một autoencoder đã học trên dữ liệu bình thường. Ta có lỗi tái tạo của ba nhóm dữ liệu:

- `normal_errors`: các mẫu bình thường, không có nhãn bất thường nào. Ngưỡng được lấy từ đây.
- `valid_errors` cùng `valid_labels`: một tập validation có nhãn ($1$ là bất thường), dùng để chọn mức phân vị.
- `test_errors` cùng `test_labels`: tập test, chỉ dùng để báo kết quả cuối.

Với mỗi mức $q$ trong `quantiles`:

1. Ngưỡng là phân vị mức $q$ của `normal_errors`, theo cách mặc định của NumPy: sắp tăng $v_0\le\dots\le v_{n-1}$, đặt $t=(n-1)q$, $i=\lfloor t\rfloor$, ngưỡng là $v_i+(t-i)(v_{i+1}-v_i)$ (hoặc $v_i$ nếu $t$ nguyên).
2. Mẫu có lỗi lớn hơn ngưỡng bị báo là bất thường; bằng ngưỡng thì không.
3. Trên validation, đếm TP, FP, FN và tính precision $=\frac{TP}{TP+FP}$, recall $=\frac{TP}{TP+FN}$, F1 $=\frac{2TP}{2TP+FP+FN}$. Mẫu số bằng $0$ thì giá trị ấy bằng $0$.

Chọn mức $q$ có F1 trên validation cao nhất; hòa thì lấy mức đứng trước trong `quantiles`. Cuối cùng, dùng ngưỡng của mức đã chọn để tính precision, recall, F1 trên test.

## Dữ liệu vào

Một đối tượng JSON gồm `normal_errors`, `valid_errors`, `valid_labels`, `test_errors`, `test_labels` và `quantiles`.

## Kết quả

Một đối tượng JSON gồm:

- `validation`: với mỗi mức, `{"q": ..., "threshold": ..., "precision": ..., "recall": ..., "f1": ...}`.
- `chosen_q`: mức đã chọn.
- `test`: `{"precision": ..., "recall": ..., "f1": ...}` trên test.

## Giới hạn

- Mỗi tập không quá $40$ mẫu. Không lỗi nào sát đúng một ngưỡng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "normal_errors": [0.1, 0.12, 0.08, 0.15, 0.11, 0.09, 0.13, 0.3, 0.1, 0.12],
  "valid_errors": [0.09, 0.14, 0.4, 0.11, 0.25, 0.6, 0.13, 0.2],
  "valid_labels": [0, 0, 1, 0, 1, 1, 0, 0],
  "test_errors": [0.12, 0.35, 0.18, 0.07, 0.55, 0.16, 0.22, 0.1],
  "test_labels": [0, 1, 0, 0, 1, 1, 0, 0],
  "quantiles": [0.5, 0.8, 0.9, 0.95, 1.0]
}
```

```output
{
  "validation": [
    {
      "q": 0.5,
      "threshold": 0.11499999999999999,
      "precision": 0.5,
      "recall": 1.0,
      "f1": 0.6666666666666666
    },
    {
      "q": 0.8,
      "threshold": 0.134,
      "precision": 0.6,
      "recall": 1.0,
      "f1": 0.75
    },
    {
      "q": 0.9,
      "threshold": 0.16499999999999995,
      "precision": 0.75,
      "recall": 1.0,
      "f1": 0.8571428571428571
    },
    {
      "q": 0.95,
      "threshold": 0.23249999999999982,
      "precision": 1.0,
      "recall": 1.0,
      "f1": 1.0
    },
    {
      "q": 1.0,
      "threshold": 0.3,
      "precision": 1.0,
      "recall": 0.6666666666666666,
      "f1": 0.8
    }
  ],
  "chosen_q": 0.95,
  "test": {"precision": 1.0, "recall": 0.6666666666666666, "f1": 0.8}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 170](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=63).
:::
