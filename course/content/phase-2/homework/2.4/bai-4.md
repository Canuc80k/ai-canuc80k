# Từ gần nghĩa

Mỗi từ được biểu diễn bằng một vector, gọi là embedding. Hai từ gần nghĩa thì vector của chúng cùng hướng. Ta đo độ giống của hai từ bằng cosine của hai vector, tức tích vô hướng sau khi đưa mỗi vector về độ dài $1$.

Hãy tính:

- Với mỗi từ, từ **khác** giống nó nhất.
- Cặp hai từ giống nhau nhất trong cả danh sách, và độ giống của cặp ấy.
- Độ giống của mỗi từ với chính nó. Kết quả này cho biết gì?

## Dữ liệu vào

Một đối tượng JSON gồm `tokens` (danh sách từ, khác nhau đôi một) và `vectors` (vector của từng từ, cùng thứ tự).

## Kết quả

Một đối tượng JSON gồm:

- `nearest`: ánh xạ mỗi từ tới từ khác giống nó nhất.
- `best_pair`: hai từ của cặp giống nhau nhất, xếp theo thứ tự chữ cái.
- `best_similarity`: cosine của cặp ấy.
- `diagonal`: độ giống của từng từ với chính nó, theo thứ tự `tokens`.

## Giới hạn

- Từ $3$ đến $25$ từ, vector có từ $2$ đến $8$ số nguyên nhỏ, không vector nào bằng $0$.
- Không có hai cặp từ nào có cùng độ giống.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "tokens": ["meo", "ho", "cho", "soi", "tao"],
  "vectors": [[3, 1, 0], [4, 1, 1], [1, 3, 0], [1, 4, 2], [0, 1, 5]]
}
```

```output
{
  "nearest": {"meo": "ho", "ho": "meo", "cho": "soi", "soi": "cho", "tao": "soi"},
  "best_pair": ["ho", "meo"],
  "best_similarity": 0.9689627902499088,
  "diagonal": [1.0, 1.0, 1.0, 1.0, 1.0]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 5.9](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=13).
:::
