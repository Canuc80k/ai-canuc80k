# Ngưỡng lỗi

Một autoencoder học trên dữ liệu bình thường sẽ tái tạo dữ liệu bình thường tốt, còn dữ liệu lạ thì kém hơn. Lỗi tái tạo lớn là dấu hiệu bất thường. Ngưỡng báo động được lấy từ dữ liệu **bình thường** trên validation, không dùng nhãn bất thường nào.

Lỗi của một hàng là trung bình bình phương sai khác giữa hàng thật và hàng tái tạo, trên ba cột.

1. Tính lỗi của từng hàng validation (toàn dữ liệu bình thường). Ngưỡng là phân vị mức $q$ của các lỗi ấy, theo cách mặc định của NumPy: sắp tăng $v_0\le\dots\le v_{n-1}$, đặt $t=(n-1)q$, $i=\lfloor t\rfloor$, ngưỡng là $v_i+(t-i)(v_{i+1}-v_i)$ (hoặc $v_i$ nếu $t$ nguyên).
2. Tính lỗi của từng hàng test. Hàng có lỗi lớn hơn ngưỡng là bất thường; bằng ngưỡng thì không.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `validation_true`, `validation_reconstructed`, `test_true`, `test_reconstructed` (mỗi hàng ba số) và `q`.

## Kết quả

Một đối tượng JSON gồm `threshold`, `test_errors` và `anomaly` (mỗi hàng test một số $0$/$1$).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "validation_true": [
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0]
  ],
  "validation_reconstructed": [
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0]
  ],
  "test_true": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
  "test_reconstructed": [[1.0, 1.0, 1.0], [2.0, 2.0, 2.0], [0.0, 0.0, 0.0]],
  "q": 0.95
}
```

```output
{"threshold": 1.0, "test_errors": [1.0, 4.0, 0.0], "anomaly": [0, 1, 0]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
