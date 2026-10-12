# Lỗi theo nhóm

Một mô hình phân loại ảnh đạt độ chính xác chung khá cao, nhưng ảnh đến từ hai camera khác nhau. Điểm chung có thể che một nhóm đang làm kém. Hãy tách kết quả theo camera.

Mỗi bản ghi gồm mã ảnh `ID`, nhóm `group`, nhãn thật `truth` và dự đoán `prediction` (đều là $0$ hoặc $1$).

Với mỗi nhóm, theo thứ tự từ điển của tên nhóm, báo:

- `count`: số bản ghi.
- `accuracy`: tỉ lệ dự đoán đúng.
- `macro_f1`: trung bình F1 của **cả hai** lớp $0$ và $1$. F1 của một lớp là $\dfrac{2\,TP}{2\,TP+FP+FN}$ khi coi lớp ấy là lớp dương, và bằng $0$ nếu mẫu số bằng $0$.

Thêm `error_ids`: mã các ảnh bị đoán sai, theo thứ tự trong dữ liệu. Mã là chuỗi: `"002"` và `"2"` là hai mã khác nhau.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `records`.

## Kết quả

Một đối tượng JSON gồm `groups` (list các `{"group", "count", "accuracy", "macro_f1"}`) và `error_ids`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "records": [
    {"ID": "002", "group": "cameraA", "truth": 1, "prediction": 1},
    {"ID": "2", "group": "cameraA", "truth": 0, "prediction": 0},
    {"ID": "image2", "group": "cameraA", "truth": 0, "prediction": 1},
    {"ID": "image3", "group": "cameraA", "truth": 1, "prediction": 0},
    {"ID": "image4", "group": "cameraA", "truth": 0, "prediction": 0},
    {"ID": "image5", "group": "cameraA", "truth": 0, "prediction": 0},
    {"ID": "image6", "group": "cameraA", "truth": 0, "prediction": 0},
    {"ID": "image7", "group": "cameraB", "truth": 1, "prediction": 0},
    {"ID": "image8", "group": "cameraB", "truth": 1, "prediction": 1},
    {"ID": "image9", "group": "cameraB", "truth": 1, "prediction": 0}
  ]
}
```

```output
{
  "groups": [
    {
      "group": "cameraA",
      "count": 7,
      "accuracy": 0.7142857142857143,
      "macro_f1": 0.65
    },
    {
      "group": "cameraB",
      "count": 3,
      "accuracy": 0.3333333333333333,
      "macro_f1": 0.25
    }
  ],
  "error_ids": ["image2", "image3", "image7", "image9"]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
