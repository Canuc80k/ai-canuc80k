# Hybrid search

Tìm kiếm bằng từ khóa giỏi bắt đúng tên riêng, mã số; tìm kiếm bằng vector giỏi bắt đúng ý dù khác chữ. Hybrid search dùng cả hai, rồi gộp hai bảng xếp hạng bằng Reciprocal Rank Fusion (RRF). Bài này so ba cách xếp hạng.

Có $N$ tài liệu với mã `doc_ids`. Với mỗi truy vấn:

1. **Từ khóa.** Điểm cho sẵn trong `lexical_scores`. Xếp tài liệu theo điểm giảm dần.
2. **Vector.** Điểm là cosine giữa vector truy vấn và vector tài liệu (bằng $0$ nếu một vector bằng $0$). Xếp theo điểm giảm dần.
3. **Gộp.** Gọi $r_1(d)$, $r_2(d)$ là hạng (từ $1$) của tài liệu $d$ trong hai bảng trên. Điểm RRF là
$$\frac{1}{c+r_1(d)}+\frac{1}{c+r_2(d)},$$
với $c$ là `rrf_k`. Xếp theo điểm giảm dần.

Mọi phép xếp hạng: bằng điểm thì theo mã (so như chuỗi).

Với mỗi cách, báo $k$ mã đầu của mỗi truy vấn, Recall@$k$ (tỉ lệ truy vấn có ít nhất một tài liệu đúng trong $k$ kết quả đầu) và MRR@$k$ (trung bình $1/\text{hạng}$ của tài liệu đúng đầu tiên trong $k$ kết quả đầu, hoặc $0$).

## Dữ liệu vào

Một đối tượng JSON gồm `doc_ids`, `lexical_scores` (mỗi truy vấn một hàng $N$ số), `doc_vectors`, `query_vectors`, `gold`, `k` và `rrf_k`.

## Kết quả

Một đối tượng JSON gồm `lexical`, `dense` và `fused`, mỗi cái là `{"top_ids", "recall_at_k", "mrr_at_k"}`.

## Giới hạn

- Không quá $10$ tài liệu và $6$ truy vấn. Không có hai điểm khác nhau mà sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "doc_ids": ["d6", "d14", "d11", "d16", "d0", "2", "d2", "d9"],
  "lexical_scores": [
    [3.04, 0.133, 0.148, 2.434, 0.214, 0.003, 0.084, 0.228],
    [2.691, 0.237, 0.3, 0.152, 0.155, 0.075, 1.528, 0.248],
    [0.147, 0.047, 0.011, 0.239, 2.63, 0.271, 2.133, 0.182],
    [0.295, 0.021, 0.014, 2.745, 0.046, 0.017, 3.181, 0.13],
    [1.994, 0.13, 0.143, 0.08, 0.033, 0.218, 2.0, 1.635],
    [0.101, 0.237, 0.086, 1.479, 2.456, 0.071, 0.162, 0.111]
  ],
  "doc_vectors": [
    [-0.75, 0.88, 1.12],
    [-0.02, -0.92, -0.96],
    [0.06, -0.24, 0.29],
    [-1.1, 0.45, 0.6],
    [-0.25, -1.75, -0.5],
    [-0.49, -0.26, -0.04],
    [-0.28, -1.16, -1.88],
    [0.14, 0.65, -0.86]
  ],
  "query_vectors": [
    [-1.21, 0.2, 1.52],
    [-2.0, 0.83, 2.12],
    [-0.25, -1.1, -2.67],
    [-0.29, 0.72, 1.91],
    [-3.11, 0.26, 2.06],
    [-1.04, -0.58, 1.62]
  ],
  "gold": [["d16"], ["d6"], ["d2"], ["d16", "d6"], ["d6"], ["d16"]],
  "k": 1,
  "rrf_k": 60
}
```

```output
{
  "lexical": {
    "top_ids": [["d6"], ["d6"], ["d0"], ["d2"], ["d2"], ["d0"]],
    "recall_at_k": 0.16666666666666666,
    "mrr_at_k": 0.16666666666666666
  },
  "dense": {
    "top_ids": [["d16"], ["d16"], ["d2"], ["d6"], ["d16"], ["d11"]],
    "recall_at_k": 0.5,
    "mrr_at_k": 0.5
  },
  "fused": {
    "top_ids": [["d16"], ["d6"], ["d2"], ["d6"], ["d6"], ["d16"]],
    "recall_at_k": 1.0,
    "mrr_at_k": 1.0
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
