# Recall và MRR

Đánh giá một hệ tìm kiếm bằng vector: mỗi truy vấn có thể có nhiều tài liệu đúng, và có truy vấn không có tài liệu đúng nào.

1. Độ giống là cosine; nếu một trong hai vector bằng $0$ thì cosine bằng $0$.
2. Với mỗi truy vấn, xếp tài liệu theo cosine giảm dần; bằng nhau thì theo mã tài liệu (so như chuỗi). Lấy $k$ tài liệu đầu.
3. Recall@$k$: tỉ lệ truy vấn có ít nhất một tài liệu đúng trong $k$ kết quả đầu.
4. MRR@$k$: trung bình của $1/\text{hạng}$ của tài liệu đúng **đầu tiên** trong $k$ kết quả đầu, hoặc $0$ nếu không có. Truy vấn không có tài liệu đúng nào vẫn được tính, với giá trị $0$.

Mã tài liệu là chuỗi: `"002"` và `"2"` là hai mã khác nhau, và `"002"` đứng trước `"2"`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `doc_ids`, `D` (vector tài liệu), `Q` (vector truy vấn), `gold` (list mã tài liệu đúng của mỗi truy vấn) và `k`.

## Kết quả

Một đối tượng JSON gồm `top_ids`, `recall_at_k` và `mrr_at_k`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "doc_ids": ["002", "2", "a", "b", "c"],
  "D": [[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0]],
  "Q": [[1, 0, 0], [0, 1, 0], [0, 0, 0], [-1, 0, 0]],
  "gold": [["2", "b"], ["a"], [], ["c"]],
  "k": 3
}
```

```output
{
  "top_ids": [
    ["002", "2", "a"],
    ["a", "002", "2"],
    ["002", "2", "a"],
    ["c", "a", "b"]
  ],
  "recall_at_k": 0.75,
  "mrr_at_k": 0.625
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
