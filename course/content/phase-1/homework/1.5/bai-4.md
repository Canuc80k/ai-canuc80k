# Lớp hiếm

Khi lớp $1$ rất hiếm, một bộ phân loại chỉ biết đoán $0$ vẫn có accuracy rất cao, dù chẳng tìm ra mẫu dương nào. Bài này đo nhiều thước đo cùng lúc để thấy điều đó bằng số.

Cho nhãn thật `y` và dự đoán của vài mô hình. Với mỗi mô hình, tính accuracy, rồi precision, recall và F1 của lớp $1$. Tính thêm `macro_f1`, là trung bình cộng của F1 lớp $1$ và F1 lớp $0$. F1 lớp $0$ tính giống F1 lớp $1$, chỉ là coi $0$ là lớp dương. Mẫu số bằng $0$ thì lấy $0$.

Cuối cùng cho biết mô hình có accuracy cao nhất và mô hình có macro F1 cao nhất. Hòa thì chọn mô hình đứng trước trong `models`.

## Dữ liệu vào

Một đối tượng JSON gồm `y` và `models`, một đối tượng ánh xạ tên mô hình tới list dự đoán.

## Kết quả

Một đối tượng JSON gồm:

- `report`: với mỗi mô hình, đối tượng `{"accuracy", "precision", "recall", "f1", "macro_f1"}`.
- `best_accuracy`, `best_macro_f1`: tên mô hình.

## Giới hạn

- `y` có từ $1$ đến $1000$ phần tử, có từ $1$ đến $5$ mô hình.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "y": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
  "models": {
    "luon_0": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "luon_1": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "mo_hinh": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0]
  }
}
```

```output
{
  "report": {
    "luon_0": {
      "accuracy": 0.8,
      "precision": 0.0,
      "recall": 0.0,
      "f1": 0.0,
      "macro_f1": 0.4444444444444444
    },
    "luon_1": {
      "accuracy": 0.2,
      "precision": 0.2,
      "recall": 1.0,
      "f1": 0.3333333333333333,
      "macro_f1": 0.16666666666666666
    },
    "mo_hinh": {
      "accuracy": 0.8,
      "precision": 0.5,
      "recall": 0.75,
      "f1": 0.6,
      "macro_f1": 0.7333333333333333
    }
  },
  "best_accuracy": "luon_0",
  "best_macro_f1": "mo_hinh"
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 1.4](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=2).
:::
