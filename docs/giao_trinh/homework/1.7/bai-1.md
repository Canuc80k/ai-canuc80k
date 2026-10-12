# Đếm tổ hợp

Trước khi bấm chạy grid search, nên đếm xem mình sắp bắt máy làm bao nhiêu việc.

`grids` là một danh sách các grid nhỏ. Mỗi grid là một từ điển, ánh xạ tên tham số tới các giá trị cần thử. Trong một grid, mọi tổ hợp đều được thử. Giữa các grid khác nhau thì không ghép chéo, chỉ nối danh sách lại với nhau. Một grid rỗng `{}` cho đúng một cấu hình, tức dùng mọi giá trị mặc định.

Hãy liệt kê các cấu hình theo đúng thứ tự `ParameterGrid` của scikit-learn cho ra, rồi đếm số lần fit. Mỗi cấu hình được fit một lần trên mỗi fold. Nếu `refit` là `true`, cộng thêm một lần fit lại cấu hình thắng trên toàn bộ dữ liệu.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `grids`, `cv_folds` và `refit`.

## Kết quả

Một đối tượng JSON gồm `candidates` (danh sách cấu hình), `cv_fits` và `total_fits`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "grids": [
    {"k": [1], "weights": ["uniform", "distance"]},
    {"model": ["constant"], "strategy": ["zero", "mean"]},
    {}
  ],
  "cv_folds": 2,
  "refit": false
}
```

```output
{
  "candidates": [
    {"k": 1, "weights": "uniform"},
    {"k": 1, "weights": "distance"},
    {"model": "constant", "strategy": "zero"},
    {"model": "constant", "strategy": "mean"},
    {}
  ],
  "cv_fits": 10,
  "total_fits": 10
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
