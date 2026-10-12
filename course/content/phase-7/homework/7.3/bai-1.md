# Đường CTC

Mô hình nhận dạng tiếng nói kiểu CTC cho mỗi khung một phân phối trên các ký hiệu, kể cả một ký hiệu "trống" (blank, mã $0$). Một đường đi gán mỗi khung một ký hiệu; gộp các ký hiệu **liền nhau giống nhau** rồi bỏ blank ta được văn bản. Nhiều đường cho cùng một văn bản, và xác suất của văn bản là **tổng** xác suất của mọi đường ấy.

1. Softmax từng khung của `logits` ($T\times V$).
2. **Greedy:** mỗi khung lấy ký hiệu xác suất lớn nhất (bằng nhau thì mã nhỏ hơn) được `greedy_path`; gộp các ký hiệu liền nhau giống nhau **trước**, rồi bỏ blank, được `greedy_collapsed`.
3. **Xác suất của `target`:** tổng xác suất (tích xác suất từng khung) của mọi đường gộp ra đúng `target`. `negative_log_likelihood` là $-\log$ của nó, hoặc `null` nếu xác suất bằng $0$.

Muốn ra hai ký tự giống nhau liền nhau (như `[1, 1]`), giữa chúng phải có một blank.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `logits` ($T\le5$, $V=3$), `blank_id` và `target` (có thể rỗng).

## Kết quả

Một đối tượng JSON gồm `greedy_path`, `greedy_collapsed`, `target_probability` và `negative_log_likelihood`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [[-2.0, 3.0, -2.0], [3.0, -2.0, -2.0], [-2.0, 3.0, -2.0]],
  "blank_id": 0,
  "target": []
}
```

```output
{
  "greedy_path": [1, 0, 1],
  "greedy_collapsed": [1, 1],
  "target_probability": 4.361289453297783e-05,
  "negative_log_likelihood": 10.040157705164347
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
