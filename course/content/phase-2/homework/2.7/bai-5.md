# Boosting L1

Gradient boosting hồi quy thường dùng loss bình phương (L2). Khi dữ liệu có vài điểm ngoại lai rất xa, loss trị tuyệt đối (L1) thường bền hơn. Bài này chạy hai phiên bản cạnh nhau để so.

Dữ liệu có một feature $x$. Mỗi vòng dùng một cây một phép chia với ngưỡng cho sẵn trong `thresholds`: điểm có $x\le t$ vào lá trái, còn lại vào lá phải. Hai phiên bản chỉ khác nhau ở hai chỗ:

| | Dự đoán ban đầu | Giá trị của mỗi lá |
|---|---|---|
| L2 | trung bình của $y$ | trung bình của $y-F$ trong lá |
| L1 | median của $y$ | median của $y-F$ trong lá |

Mỗi vòng, $F$ của mọi điểm trong lá được cộng thêm $\nu$ nhân giá trị của lá, với $\nu$ là tốc độ học. Median của một số chẵn phần tử là trung bình hai phần tử giữa. Lá không có điểm nào thì bỏ qua.

Sau hết các vòng, báo dự đoán, MSE và MAE trên train của mỗi phiên bản.

## Dữ liệu vào

Một đối tượng JSON gồm `x`, `y`, `thresholds` và `learning_rate`.

## Kết quả

Một đối tượng JSON gồm `l2` và `l1`, mỗi trường là `{"predictions": ..., "mse": ..., "mae": ...}`.

## Giới hạn

- Từ $3$ đến $30$ điểm, không quá $6$ vòng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [1, 2, 3, 4, 5, 6],
  "y": [1, 2, 2, 3, 3, 40],
  "thresholds": [3.5, 3.5, 5.5],
  "learning_rate": 0.5
}
```

```output
{
  "l2": {
    "predictions": [0.7375, 0.7375, 0.7375, 10.9875, 10.9875, 26.8125],
    "mse": 50.79453125,
    "mae": 5.325
  },
  "l1": {
    "predictions": [2.0625, 2.0625, 2.0625, 2.8125, 2.8125, 21.4375],
    "mse": 57.62890625,
    "mae": 3.3541666666666665
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 3](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=4).
:::
