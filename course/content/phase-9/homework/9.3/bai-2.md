# Log-loss

Hai model cùng accuracy chưa chắc tốt như nhau. Log-loss phạt nặng một dự đoán tự tin mà sai, điều accuracy không thấy.

Có $n$ mẫu với nhãn $y_i\in\{0,1\}$ và vài model, mỗi model xuất xác suất $p_i$ của lớp 1 cho từng mẫu ($0<p_i<1$). Với mỗi model, tính log-loss

$$L=-\frac1n\sum_{i}\big[y_i\log p_i+(1-y_i)\log(1-p_i)\big]$$

(log tự nhiên) và accuracy khi đoán lớp 1 lúc $p_i\ge0.5$.

So với một dự đoán hằng: nếu mọi mẫu đều nhận cùng một xác suất $c$, log-loss nhỏ nhất đạt tại $c=q$, tỉ lệ nhãn 1 trong dữ liệu. Báo $q$, log-loss của dự đoán hằng ấy (quy ước $0\log0=0$), thứ tự các model theo log-loss tăng dần (bằng nhau thì tên nhỏ trước), và các model có log-loss lớn hơn dự đoán hằng.

## Dữ liệu vào

Một đối tượng JSON gồm `y` và `models` (tên model ánh xạ tới list xác suất).

## Kết quả

Một đối tượng JSON gồm `models` (mỗi tên một `{"log_loss", "accuracy"}`), `ranking`, `best_constant`, `best_constant_loss` và `worse_than_constant` (sắp theo tên).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "y": [1, 1, 1, 0, 0],
  "models": {
    "than_trong": [0.7, 0.7, 0.4, 0.3, 0.3],
    "tu_tin": [0.99, 0.99, 0.99, 0.01, 0.99]
  }
}
```

```output
{
  "models": {
    "than_trong": {"log_loss": 0.468598101525817, "accuracy": 0.8},
    "tu_tin": {"log_loss": 0.9290743058804193, "accuracy": 0.8}
  },
  "ranking": ["than_trong", "tu_tin"],
  "best_constant": 0.6,
  "best_constant_loss": 0.6730116670092564,
  "worse_than_constant": ["tu_tin"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
