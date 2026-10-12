# Đường tắt và ReLU

Kết nối tắt cộng thẳng đầu vào vào đầu ra của nhánh, nên gradient luôn có một lối đi về. Nhưng nếu sau phép cộng còn một ReLU, lối đi ấy vẫn có thể bị chặn.

Bài này dùng một nhánh tính trên từng điểm ảnh (như conv $1\times1$ với một kênh), với các số $w_1$, $b_1$, $w_2$, $b_2$:

$$
y=\operatorname{ReLU}\!\left(x+w_2\operatorname{ReLU}(w_1x+b_1)+b_2\right).
$$

Áp cho mọi ô của ảnh $X$. Loss là tổng mọi ô của $y$. Hãy tính $y$ và gradient của loss theo từng ô của $X$. Không có ô nào làm đầu vào của ReLU đúng bằng $0$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X`, `w1`, `b1`, `w2` và `b2`.

## Kết quả

Một đối tượng JSON gồm `output` và `gradient`, cùng cỡ với `X`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [0.188, -0.415, -1.353],
    [-0.985, -0.028, 1.021],
    [-0.177, -0.385, 0.732]
  ],
  "w1": 0.7,
  "b1": 0.2,
  "w2": -0.3,
  "b2": 0.1
}
```

```output
{
  "output": [
    [0.18852000000000002, 0, 0],
    [0, 0.017880000000000007, 0.84659],
    [0, 0, 0.61828]
  ],
  "gradient": [[0.79, 0, 0], [0, 0.79, 0.79], [0, 0, 0.79]]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
