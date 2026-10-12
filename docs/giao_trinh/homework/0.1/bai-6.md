# Tệp dự đoán

Bài thi AI nào cũng kết thúc bằng một tệp dự đoán. Model tốt đến đâu mà tệp sai định dạng, hay ghép nhầm mã với dự đoán, thì vẫn mất điểm.

Ta đã chạy vài thử nghiệm. Mỗi thử nghiệm có một lỗi validation và một bộ dự đoán cho mọi mẫu, nhưng các dự đoán nằm lộn xộn. Hãy chọn thử nghiệm có lỗi validation **nhỏ nhất**, rồi ghi tệp CSV gồm mã mẫu và dự đoán của thử nghiệm ấy, theo đúng thứ tự `sample_ids`. Nếu nhiều thử nghiệm cùng lỗi nhỏ nhất, lấy thử nghiệm có `run_id` nhỏ nhất theo thứ tự chuỗi.

Mã mẫu có thể chứa dấu phẩy, ví dụ `A,B`. Ghép tay bằng `",".join(...)` sẽ tách nhầm một mã thành hai ô. Module `csv` tự đặt ngoặc kép khi cần, hãy dùng `csv.writer`.

## Dữ liệu vào

Một đối tượng JSON gồm:

- `sample_ids`: danh sách mã mẫu, theo thứ tự cần ghi.
- `runs`: danh sách thử nghiệm, mỗi thử nghiệm có `run_id`, `validation_error` và `predictions`. `predictions` là danh sách `{"id": ..., "prediction": ...}`, mỗi mã đúng một lần.

## Kết quả

Nội dung tệp CSV, dòng đầu là `id,prediction`. Hàm `solve` trả về cả nội dung ấy dưới dạng một chuỗi, `starter.py` sẽ in ra.

## Giới hạn

- Có từ $1$ đến $500$ mẫu và từ $1$ đến $10$ thử nghiệm.
- Mã và `run_id` dài từ $1$ đến $64$ ký tự, không chứa ký tự xuống dòng.
- Lỗi validation từ $0$ đến $10^4$, dự đoán có trị tuyệt đối không quá $10^4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Dòng đầu, các mã và thứ tự phải đúng hoàn toàn. Dự đoán được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "sample_ids": ["001", "A,B"],
  "runs": [
    {
      "run_id": "r2",
      "validation_error": 2,
      "predictions": [{"id": "001", "prediction": 9}, {"id": "A,B", "prediction": 8}]
    },
    {
      "run_id": "r1",
      "validation_error": 1,
      "predictions": [{"id": "A,B", "prediction": 7}, {"id": "001", "prediction": 3}]
    }
  ]
}
```

```output
id,prediction
001,3
"A,B",7
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
