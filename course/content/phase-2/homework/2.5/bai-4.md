# Chọn split

Mỗi điểm có hai feature $x_0, x_1$ và nhãn $0$ hoặc $1$. Ta muốn chọn phép chia đầu tiên cho cây, có dạng $x_j<t$, trong danh sách ứng viên `splits`.

Có hai cách chấm một phép chia:

- **Mutual information**: entropy của nhãn trước khi chia, trừ entropy trung bình có trọng số của hai nhánh sau khi chia. Entropy tính theo bit. Càng lớn càng tốt.
- **Tỉ lệ lỗi**: mỗi nhánh đoán nhãn chiếm đa số của nó, rồi đếm số điểm bị đoán sai trên tổng số điểm. Càng nhỏ càng tốt.

Hãy tính entropy của nhãn trước khi chia, hai con số trên cho từng ứng viên, rồi chọn ứng viên tốt nhất theo mỗi cách. Hòa thì chọn ứng viên đứng trước.

## Dữ liệu vào

Một đối tượng JSON gồm `X`, `y` và `splits`, mỗi ứng viên là `[j, t]`.

## Kết quả

Một đối tượng JSON gồm:

- `entropy`: entropy của nhãn.
- `splits`: với mỗi ứng viên, `{"mutual_information": ..., "error_rate": ...}`.
- `best_by_mi`, `best_by_error`: chỉ số của ứng viên tốt nhất, đánh số từ $0$.

## Giới hạn

- Từ $2$ đến $40$ điểm, tọa độ nguyên từ $0$ đến $9$, các ngưỡng có dạng $k+0.5$.
- Không quá $8$ ứng viên.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[1, 1], [1, 2], [2, 1], [2, 3], [3, 2], [3, 3], [4, 1], [4, 3]],
  "y": [0, 0, 0, 1, 1, 1, 1, 0],
  "splits": [[0, 2], [0, 3], [1, 1.5], [1, 2.5]]
}
```

```output
{
  "entropy": 1.0,
  "splits": [
    {"mutual_information": 0.31127812445913283, "error_rate": 0.25},
    {"mutual_information": 0.18872187554086717, "error_rate": 0.25},
    {"mutual_information": 0.04879494069539847, "error_rate": 0.375},
    {"mutual_information": 0.04879494069539847, "error_rate": 0.375}
  ],
  "best_by_mi": 0,
  "best_by_error": 0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
