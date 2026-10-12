# Điền thiếu

Bảng khảo sát có cột giờ tự học mỗi tuần, nhưng nhiều học sinh bỏ trống. Ta điền chỗ trống như mục Ô trống của bài học. Mỗi ô nhận trung vị (median) giờ học của lớp mình, tính trên `train.csv`. Lớp chưa gặp trong train, hoặc lớp mà mọi ô đều trống, thì nhận median chung của cả train. Tệp `test.csv` chỉ được điền, không góp vào việc tính median.

Cụ thể, hãy tính:

- `global_median`: median của mọi ô giờ học có số trong train.
- Median của từng lớp trong train. Lớp toàn ô trống thì median là `null`.
- Giờ học của từng học sinh trong test sau khi điền. Ô có số thì giữ nguyên.

Mã học sinh có thể có số $0$ ở đầu như `0007`, nên đọc bằng `dtype={"id": str, "class": str}`.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` và `test.csv`, cùng ba cột `id`, `class`, `hours`. Ô `hours` trống là chưa biết.

## Kết quả

Một đối tượng JSON gồm:

- `global_median`: một số.
- `class_medians`: các đối tượng `{"class": ..., "median": ...}`, mỗi lớp trong train một đối tượng, xếp theo tên lớp.
- `filled`: các đối tượng `{"id": ..., "hours": ..., "was_missing": ...}`, theo thứ tự của test. `was_missing` cho biết ô ban đầu có trống không.

## Giới hạn

- Train có tối đa $250$ dòng và có ít nhất một ô có số. Test có từ $1$ đến $100$ dòng.
- Giờ học từ $0$ đến $40$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
train.csv:
id,class,hours
t1,A,1
t2,A,3
t3,A,
t4,B,4
t5,B,6
t6,B,8
t7,C,

test.csv:
id,class,hours
s1,A,
s2,B,5
s3,B,
s4,C,
s5,D,
```

```output
{
  "global_median": 4.0,
  "class_medians": [
    {"class": "A", "median": 2.0},
    {"class": "B", "median": 6.0},
    {"class": "C", "median": null}
  ],
  "filled": [
    {"id": "s1", "hours": 2.0, "was_missing": true},
    {"id": "s2", "hours": 5.0, "was_missing": false},
    {"id": "s3", "hours": 6.0, "was_missing": true},
    {"id": "s4", "hours": 4.0, "was_missing": true},
    {"id": "s5", "hours": 4.0, "was_missing": true}
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
