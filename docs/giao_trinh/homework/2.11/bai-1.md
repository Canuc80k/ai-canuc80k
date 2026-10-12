# Độ trễ

Muốn dự đoán doanh số của một cửa hàng ở một thời điểm, ta chỉ được dùng những gì đã biết trước thời điểm ấy. Hai đặc trưng hay dùng:

- `lag1`: doanh số của chính cửa hàng ấy ở lần ngay trước.
- `mean_previous2`: trung bình doanh số của hai lần ngay trước, không tính lần hiện tại.

Bảng dữ liệu bị xáo trộn thứ tự. Hãy sắp các hàng theo cửa hàng rồi theo thời gian, tính hai đặc trưng, và trả kết quả theo **đúng thứ tự hàng ban đầu**. Lần đầu tiên của một cửa hàng không có `lag1`. Hai lần đầu tiên không có `mean_previous2`. Khi ấy ghi `null`.

Mã cửa hàng là chuỗi: `"002"` và `"2"` là hai cửa hàng khác nhau.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` với các cột `id`, `shop`, `time` (số nguyên, không lặp trong một cửa hàng) và `sales`.

## Kết quả

Một đối tượng JSON `{"rows": [...]}`, mỗi phần tử là `{"id": ..., "lag1": ..., "mean_previous2": ...}`, theo thứ tự hàng trong `rows.csv`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
rows.csv:
id,shop,time,sales
000,002,2,14.0
001,2,1,11.0
002,002,1,11.0
003,A,1,11.0
004,002,3,19.0
005,2,3,19.0
006,2,2,14.0
007,A,2,14.0
008,A,3,19.0
```

```output
{
  "rows": [
    {"id": "000", "lag1": 11.0, "mean_previous2": null},
    {"id": "001", "lag1": null, "mean_previous2": null},
    {"id": "002", "lag1": null, "mean_previous2": null},
    {"id": "003", "lag1": null, "mean_previous2": null},
    {"id": "004", "lag1": 14.0, "mean_previous2": 12.5},
    {"id": "005", "lag1": 14.0, "mean_previous2": 12.5},
    {"id": "006", "lag1": 11.0, "mean_previous2": null},
    {"id": "007", "lag1": 11.0, "mean_previous2": null},
    {"id": "008", "lag1": 14.0, "mean_previous2": 12.5}
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
