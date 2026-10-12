# Ghép theo id

Mô hình đã dự đoán xong, kết quả nằm trong `predictions.csv`. Nhưng file nộp phải theo đúng thứ tự `id` của `sample.csv`, và thứ tự ấy khác. Chỉ cần ghép sai một hàng là điểm tụt dù mô hình tốt.

Hãy ghép dự đoán vào từng `id` của `sample.csv` theo đúng `id`, không theo vị trí hàng. Trước khi ghép, nên kiểm hai tệp có cùng tập id và không id nào lặp.

`id` là chuỗi, có thể là `"002"` và `"2"`, có dấu phẩy, dấu ngoặc kép hoặc chữ có dấu.

## Dữ liệu vào

Mỗi thư mục test có `predictions.csv` (cột `id`, `target`) và `sample.csv` (cột `id`).

## Kết quả

Một đối tượng JSON `{"rows": [...]}`, mỗi phần tử là `{"id": ..., "target": ...}`, theo thứ tự của `sample.csv`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
predictions.csv:
id,target
002,0.855931
2,0.539403
"A,1",0.812882
"""quoted""",1.62821
đồ chơi,0.302967

sample.csv:
id
2
002
"""quoted"""
đồ chơi
"A,1"
```

```output
{
  "rows": [
    {"id": "2", "target": 0.539403},
    {"id": "002", "target": 0.855931},
    {"id": "\"quoted\"", "target": 1.62821},
    {"id": "đồ chơi", "target": 0.302967},
    {"id": "A,1", "target": 0.812882}
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
