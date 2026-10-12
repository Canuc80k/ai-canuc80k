# Kiểm SHA-256

Trước khi nạp một tệp trọng số tải về, phải chắc nó đúng là tệp mình mong đợi. `torch.load` có thể chạy mã trong tệp, nên một tệp bị sửa hay bị thay không được phép nạp.

Mỗi test có một tệp `candidate.pt` và mã SHA-256 mong đợi. Hãy tính SHA-256 trên **các byte của tệp**, so với mã mong đợi, và báo kích thước tệp. Một nửa số test có tệp đã bị sửa đúng một byte. Không gọi `torch.load` khi mã không khớp.

Khớp mã chỉ chứng tỏ tệp giống hệt bản đã ghi nhận, không chứng tỏ tệp ấy an toàn hay tốt.

## Dữ liệu vào

Mỗi thư mục test có `candidate.pt` và `input.json` chứa `expected_sha256`.

## Kết quả

Một đối tượng JSON gồm `matches` (`true` hoặc `false`) và `bytes` (số byte của tệp).

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "expected_sha256": "aca5591b9429317876c78fd4cc874708eb8a7487b22dfbc855707948fd167a02"
}
```

```output
{"matches": true, "bytes": 20667}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
