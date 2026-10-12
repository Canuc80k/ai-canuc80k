# Cache embedding

Tính embedding cho cả kho dữ liệu tốn thời gian, nên người ta lưu lại để dùng lần sau. Nhưng bản lưu chỉ còn dùng được khi nó được tạo ra **đúng cùng một cách**: cùng model, cùng tiền xử lý, cùng pooling, cùng chuẩn hóa, và các hàng theo đúng cùng danh sách ID. Chỉ cùng số chiều thì chưa đủ.

Mỗi bên là một từ điển với năm trường `model_sha`, `processor`, `pooling`, `normalization`, `ids`. Hãy so bản lưu (`cache`) với cấu hình hiện tại (`expected`) và liệt kê các trường khác nhau theo đúng thứ tự trên. `ids` là list chuỗi: `"002"` khác `"2"`, và cùng các ID nhưng khác thứ tự cũng là khác.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `expected` và `cache`.

## Kết quả

Một đối tượng JSON gồm `reusable` (`true` khi không có trường nào khác) và `mismatches`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "expected": {
    "model_sha": "learned-source-v1",
    "processor": "divide16",
    "pooling": "relu32",
    "normalization": "l2",
    "ids": ["002", "2", "03"]
  },
  "cache": {
    "model_sha": "learned-source-v1",
    "processor": "divide16",
    "pooling": "relu32",
    "normalization": "l2",
    "ids": ["2", "002", "03"]
  }
}
```

```output
{"reusable": false, "mismatches": ["ids"]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
