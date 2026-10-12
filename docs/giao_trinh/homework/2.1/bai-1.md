# Dự đoán

Robot cân đồ chơi bằng một mô hình tuyến tính đã học sẵn. Mỗi món đồ chơi có $d$ feature, và khối lượng dự đoán là

$$
\hat y_i = \sum_{j} X_{ij}\,w_j + b.
$$

Cho bảng $X$, vector trọng số $w$ và hệ số tự do $b$, hãy tính dự đoán cho từng món. Với NumPy, chỉ cần một phép nhân ma trận với vector rồi cộng $b$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (ma trận $n\times d$), `w` ($d$ số) và `b`.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}` gồm $n$ dự đoán theo thứ tự hàng.

## Giới hạn

- $1\le n\le20$, $1\le d\le4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"X": [[3]], "w": [-0.4608150955572951], "b": 1.7755447707971468}
```

```output
{"predictions": [0.3930994841252615]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
