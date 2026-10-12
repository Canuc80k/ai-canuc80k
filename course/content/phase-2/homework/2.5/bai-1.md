# Độ lẫn lộn

Một hộp kẹo có nhiều loại, `counts` cho biết mỗi loại có bao nhiêu viên. Hộp càng lẫn lộn thì độ lẫn lộn (impurity) càng cao. Hãy tính hai thước đo quen thuộc của cây quyết định, với $p_k$ là tỉ lệ loại $k$:

$$
\text{Gini}=1-\sum_k p_k^2,\qquad
H=-\sum_k p_k\log_2 p_k .
$$

Entropy tính theo bit, tức logarit cơ số $2$. Loại có $0$ viên không góp gì, ta quy ước $0\log_2 0=0$.

## Dữ liệu vào

Mỗi tệp `input.json` có `counts`, các số nguyên không âm, tổng dương.

## Kết quả

Một đối tượng JSON gồm `gini` và `entropy_bits`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"counts": [2]}
```

```output
{"gini": 0.0, "entropy_bits": 0.0}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
