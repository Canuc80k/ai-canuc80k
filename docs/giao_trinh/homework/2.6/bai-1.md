# Bootstrap

Mỗi cây trong rừng học trên một lượt rút bootstrap: rút ngẫu nhiên $n$ lần **có hoàn lại** từ $n$ mẫu. Có mẫu được rút nhiều lần, có mẫu không được rút lần nào. Những mẫu không được rút gọi là out-of-bag (OOB) của cây ấy.

Cho kết quả một lượt rút, hãy đếm mỗi mẫu được rút bao nhiêu lần, và liệt kê các mẫu OOB.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `n` và `draws` (các chỉ số đã rút, từ $0$ đến $n-1$, có thể lặp).

## Kết quả

Một đối tượng JSON gồm `multiplicities` ($n$ số đếm) và `oob` (chỉ số các mẫu không được rút, tăng dần).

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"n": 3, "draws": [0, 2, 1]}
```

```output
{"multiplicities": [1, 1, 1], "oob": []}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
