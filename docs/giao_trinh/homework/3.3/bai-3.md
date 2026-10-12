# Huber loss

MSE phạt nặng các sai số lớn, nên một điểm ngoại lai có thể kéo cả mô hình. Huber loss giữ dạng bình phương khi sai số nhỏ và chuyển sang tuyến tính khi sai số lớn. Với sai số $r$ và ngưỡng $\delta$:

$$
\ell(r)=\begin{cases}\frac12r^2 & \text{nếu } |r|\le\delta,\\ \delta\left(|r|-\frac12\delta\right) & \text{nếu } |r|>\delta.\end{cases}
$$

Hãy tính trung bình $\ell$ trên mọi phần tử, với $r$ là dự đoán trừ nhãn, và gradient của loss trung bình ấy theo từng dự đoán.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `prediction`, `target` (cùng độ dài) và `delta`.

## Kết quả

Một đối tượng JSON gồm `loss` và `gradient`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "prediction": [-10.0, -1.0, -0.1, 0.0, 0.1, 1.0, 10.0],
  "target": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
  "delta": 1.0
}
```

```output
{
  "loss": 2.858571428571429,
  "gradient": [
    -0.14285714285714285, -0.14285714285714285, -0.014285714285714287,
    0.0, 0.014285714285714287, 0.14285714285714285,
    0.14285714285714285
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
