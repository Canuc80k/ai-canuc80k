# Chia batch

`DataLoader` chia dữ liệu thành các batch. Khi số mẫu không chia hết cho kích thước batch, batch cuối nhỏ hơn, và `drop_last=True` bỏ hẳn batch ấy.

Dataset gồm các chỉ số $0,1,\dots,n-1$. Hãy tạo `DataLoader(batch_size=..., shuffle=False, drop_last=..., num_workers=0)` và cho biết:

- `batches`: các batch của một epoch, mỗi batch là list chỉ số.
- `steps`: tổng số bước cập nhật sau `epochs` epoch, mỗi batch một bước.
- `seen_per_epoch`: số mẫu thực sự được dùng trong một epoch.

Nếu $n$ nhỏ hơn kích thước batch mà `drop_last` bật thì không có batch nào.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `n`, `batch_size`, `drop_last` và `epochs`.

## Kết quả

Một đối tượng JSON gồm `batches`, `steps` và `seen_per_epoch`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"n": 1, "batch_size": 2, "drop_last": false, "epochs": 1}
```

```output
{"batches": [[0]], "steps": 1, "seen_per_epoch": 1}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
