# Tiền xử lý

Một bảng dữ liệu có cột số và cột phân loại, có ô bị thiếu (`null`) và có giá trị ngoại lai rất xa. Trước khi học mô hình, ta xử lý theo đúng thứ tự sau. Mọi con số dùng để xử lý đều tính trên **train**, rồi áp nguyên cho cả train lẫn test.

Với mỗi cột số:

1. Điền ô thiếu bằng median của các giá trị có mặt trong train.
2. Chặn ngoại lai bằng IQR. Tính tứ phân vị $Q_1$, $Q_3$ của cột train sau khi điền. Giá trị nhỏ hơn $Q_1-1.5(Q_3-Q_1)$ được nâng lên bằng mức ấy, giá trị lớn hơn $Q_3+1.5(Q_3-Q_1)$ được hạ xuống bằng mức ấy.
3. Chuẩn hóa: trừ trung bình rồi chia độ lệch chuẩn của cột train sau khi chặn. Độ lệch chuẩn dùng mẫu số $n$. Nếu độ lệch chuẩn bằng $0$ thì chia cho $1$.

Tứ phân vị tính theo cách mặc định của NumPy: sắp $n$ giá trị tăng dần $v_0\le\dots\le v_{n-1}$, đặt $t=(n-1)q$ và $i=\lfloor t\rfloor$. Tứ phân vị là $v_i+(t-i)(v_{i+1}-v_i)$, hoặc $v_i$ nếu $t$ nguyên.

Với mỗi cột phân loại:

1. Điền ô thiếu bằng giá trị xuất hiện nhiều nhất trong train. Hòa thì lấy giá trị nhỏ nhất theo thứ tự chuỗi.
2. One-hot: mỗi giá trị có mặt trong train (không tính ô thiếu) thành một cột, xếp theo thứ tự chuỗi, tên cột là `tên=giá trị`. Giá trị ở test mà train không có thì mọi cột của nó bằng $0$.

Các cột kết quả gồm các cột số theo thứ tự trong `numeric`, rồi tới các cột one-hot theo thứ tự trong `categorical`.

## Dữ liệu vào

Một đối tượng JSON gồm `numeric`, `categorical` (tên các cột), `train` và `test` (mỗi hàng là một đối tượng từ tên cột tới giá trị hoặc `null`).

## Kết quả

Một đối tượng JSON gồm:

- `fill`: giá trị dùng để điền thiếu của từng cột.
- `bounds`: với mỗi cột số, `[mức dưới, mức trên]` dùng để chặn.
- `columns`: tên các cột kết quả.
- `test`: các hàng test sau khi xử lý.

## Giới hạn

- Train có từ $3$ đến $25$ hàng, test có từ $1$ đến $8$ hàng. Mỗi cột có ít nhất một giá trị không thiếu trong train.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "numeric": ["income", "age"],
  "categorical": ["job"],
  "train": [
    {"income": 20.0, "age": 25.0, "job": "teacher"},
    {"income": 35.0, "age": null, "job": "nurse"},
    {"income": null, "age": 40.0, "job": "teacher"},
    {"income": 30.0, "age": 33.0, "job": null},
    {"income": 500.0, "age": 50.0, "job": "driver"},
    {"income": 25.0, "age": 29.0, "job": "nurse"}
  ],
  "test": [
    {"income": 1000.0, "age": null, "job": "pilot"},
    {"income": null, "age": 61.0, "job": null}
  ]
}
```

```output
{
  "fill": {"income": 30.0, "age": 33.0, "job": "nurse"},
  "bounds": {"income": [15.0, 45.0], "age": [17.625, 50.625]},
  "columns": ["income", "age", "job=driver", "job=nurse", "job=teacher"],
  "test": [
    [1.8019963960108123, -0.24680702093691811, 0.0, 0.0, 0.0],
    [-0.10599978800063585, 1.9281798510696726, 0.0, 1.0, 0.0]
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 304](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=117).
:::
