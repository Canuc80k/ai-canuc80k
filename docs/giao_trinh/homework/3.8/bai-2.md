# Masked mean

Muốn biểu diễn cả câu bằng một vector, cách đơn giản là lấy trung bình embedding của các token. Nhưng nếu tính cả PAD thì câu ngắn bị kéo về phía embedding của PAD. Phải lấy trung bình chỉ trên các token thật.

Cho bảng embedding `table` ($V$ hàng, mỗi hàng ba số), các câu đã chèn PAD bên phải (`tokens`) và độ dài thật của từng câu (`lengths`). PAD có ID $0$, và hàng $0$ của bảng **cố tình khác $0$**. Với mỗi câu, lấy embedding của `lengths` token đầu rồi tính trung bình. Câu có độ dài $0$ ghi `null`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `table`, `tokens` và `lengths`.

## Kết quả

Một đối tượng JSON `{"pooled": [...]}`, mỗi câu một vector ba số hoặc `null`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "table": [
    [9.0, 8.0, 7.0],
    [0.5, -1.0, 0.0],
    [1.0, 1.0, 1.0],
    [-2.0, 0.0, 2.0],
    [0.0, 3.0, 0.0],
    [1.5, -0.5, 1.0]
  ],
  "tokens": [[1, 3, 0, 0], [4, 5, 2, 1], [0, 0, 0, 0]],
  "lengths": [2, 4, 0]
}
```

```output
{"pooled": [[-0.75, -0.5, 1.0], [0.75, 0.625, 0.5], null]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
