# Recall@k

Tìm ảnh bằng embedding: với mỗi ảnh truy vấn, xếp các ảnh trong kho (gallery) theo độ giống, rồi xem trong vài kết quả đầu có ảnh nào cùng lớp không.

1. Độ giống là cosine. Nếu một trong hai vector toàn $0$ thì cosine bằng $0$.
2. Với mỗi truy vấn, xếp gallery theo cosine giảm dần; bằng nhau thì ảnh đứng trước trong gallery xếp trước.
3. Recall@$k$ là tỉ lệ truy vấn có **ít nhất một** ảnh cùng lớp trong $k$ kết quả đầu.

Mỗi truy vấn có ít nhất một ảnh cùng lớp trong gallery. Mã ảnh là chuỗi: `"002"` và `"2"` là hai mã khác nhau.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `query`, `gallery`, `query_labels`, `gallery_labels` và `gallery_ids`.

## Kết quả

Một đối tượng JSON gồm `top3_ids` (mã của ba kết quả đầu, cho mỗi truy vấn), `recall_at_1` và `recall_at_3`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "query": [[1, 0, 0], [0, 1, 0], [0, 0, 0]],
  "gallery": [[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, -1, 0]],
  "query_labels": ["a", "b", "a"],
  "gallery_labels": ["b", "a", "b", "a", "c"],
  "gallery_ids": ["002", "2", "x", "y", "z"]
}
```

```output
{
  "top3_ids": [["002", "2", "x"], ["x", "002", "2"], ["002", "2", "x"]],
  "recall_at_1": 0.3333333333333333,
  "recall_at_3": 1.0
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
