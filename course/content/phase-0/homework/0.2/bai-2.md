# Padding

Trước khi cho ảnh đi qua một bộ lọc, người ta thường viền quanh ảnh một lớp số $0$, để bộ lọc đọc được cả các ô sát mép. Việc này gọi là padding, ta sẽ gặp lại ở bài convolution.

Cho ảnh `image` là một lưới số nguyên và độ dày viền `pad`. Hãy tạo ảnh mới có thêm `pad` hàng số $0$ ở trên và ở dưới, `pad` cột số $0$ ở bên trái và bên phải. Phần giữa là ảnh cũ, và ảnh cũ không bị đổi.

Gợi ý: tạo mảng toàn số $0$ đúng kích thước mới, rồi gán ảnh cũ vào giữa bằng lát cắt. Nhớ thử `pad = 0`, vì lát cắt `a[0:-0]` là rỗng.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `image` và `pad`.

## Kết quả

Lưới mới, cao hơn và rộng hơn ảnh cũ $2\cdot\text{pad}$ ô.

## Giới hạn

- Ảnh có từ $1$ đến $20$ hàng và cột, mỗi số trong đoạn $[-100, 100]$.
- $0\le\text{pad}\le4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"image": [[1, 2, 1], [2, 0, 2], [1, 2, 1]], "pad": 1}
```

```output
[
  [0, 0, 0, 0, 0],
  [0, 1, 2, 1, 0],
  [0, 2, 0, 2, 0],
  [0, 1, 2, 1, 0],
  [0, 0, 0, 0, 0]
]
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
