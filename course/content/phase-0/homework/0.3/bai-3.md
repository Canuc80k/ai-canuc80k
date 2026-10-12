# Merge

Hội thám hiểm có hai cuốn sổ. `players.csv` ghi mã và tên hội viên, `stats.csv` ghi sức mạnh theo mã. Hãy ghép sức mạnh vào danh sách hội viên, giống mục `merge` của bài học.

Mã là chuỗi: `002` và `2` là hai người khác nhau, nên đọc mã bằng `dtype={"id": str}`. Mỗi dòng của `players.csv` cho đúng một dòng kết quả, theo thứ tự cũ. Một mã có thể xuất hiện nhiều lần trong `players.csv`, nhưng trong `stats.csv` thì mỗi mã có nhiều nhất một dòng. Hội viên chưa có trong `stats.csv` thì sức mạnh là `null`.

`merge` với `how="left"` làm đúng việc này. Sau khi ghép, cột `power` có ô trống nên thành số thực, khi trả về hãy đổi lại thành số nguyên.

## Dữ liệu vào

Mỗi thư mục test có `players.csv` (cột `id`, `name`) và `stats.csv` (cột `id`, `power`). Tên có thể chứa dấu phẩy hay dấu ngoặc kép, pandas tự đọc đúng.

## Kết quả

Danh sách các đối tượng `{"id": ..., "name": ..., "power": ...}`, theo thứ tự của `players.csv`.

## Giới hạn

- `players.csv` có từ $4$ đến $23$ dòng, `stats.csv` có $5$ dòng, sức mạnh từ $0$ đến $100$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
players.csv:
id,name
002,"Rồng ""nhỏ"""
2,"Mèo, đỏ"
002,Rồng lớn
404,Chưa ghi điểm

stats.csv:
id,power
2,50
003,53
10,85
002,0
001,58
```

```output
[
  {"id": "002", "name": "Rồng \"nhỏ\"", "power": 0},
  {"id": "2", "name": "Mèo, đỏ", "power": 50},
  {"id": "002", "name": "Rồng lớn", "power": 0},
  {"id": "404", "name": "Chưa ghi điểm", "power": null}
]
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
