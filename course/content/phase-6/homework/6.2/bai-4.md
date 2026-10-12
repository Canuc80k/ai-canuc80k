# In-batch negatives

Sentence embedding thường được học bằng các cặp câu (câu hỏi, câu trả lời đúng). Không cần nhãn "sai": trong cùng một batch, câu trả lời của các cặp khác tự động là negative. Có thể thêm cho mỗi cặp một **hard negative**, một câu trông giống nhưng sai, để bài toán khó hơn. Đây là loss MultipleNegativesRanking của thư viện sentence-transformers.

Có $B$ câu neo $a_i$ và $B$ câu đúng $p_i$; có thể có thêm $B$ hard negative $n_i$. Đặt các ứng viên $c$ là $p_1,\dots,p_B$, rồi tới $n_1,\dots,n_B$ nếu có.

1. Chuẩn hóa mọi vector về độ dài $1$. Điểm $S_{ij}=s\cdot a_i\cdot c_j$ với $s$ là `scale`.
2. Loss của câu neo $i$: cross-entropy trên hàng $S_{i\cdot}$ với đáp án là cột $i$ (chính $p_i$).
3. `loss` là trung bình trên các câu neo; `accuracy` là tỉ lệ câu neo mà $p_i$ có điểm cao nhất trong hàng; `chance_loss` là $\log(\text{số ứng viên})$.

## Dữ liệu vào

Một đối tượng JSON gồm `anchors`, `positives`, `scale`, và có thể có `hard_negatives`.

## Kết quả

Một đối tượng JSON gồm `scores`, `per_anchor_loss`, `loss`, `accuracy` và `chance_loss`.

## Giới hạn

- $B\le5$, mỗi vector không quá $5$ số, không vector nào bằng $0$. Với mỗi câu neo, hai điểm cao nhất cách nhau rõ.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "anchors": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
  "positives": [[0.9, 0.1, 0], [0.1, 0.9, 0.1], [0, 0.2, 1]],
  "hard_negatives": [[0.8, 0.3, 0], [0.2, 0.8, 0.3], [0.3, 0, 0.9]],
  "scale": 20
}
```

```output
{
  "scores": [
    [
      19.87767469347238, 2.195285199793807, 0.0, 18.726583551380887,
      4.558423058385518, 6.324555320336759
    ],
    [
      2.208630521496931, 19.75756679814426, 3.9223227027636804,
      7.022468831767833, 18.233692233542072, 0.0
    ],
    [
      0.0, 2.195285199793807, 19.6116135138184, 0.0, 6.837634587578276,
      18.973665961010276
    ]
  ],
  "per_anchor_loss": [0.2748194583338321, 0.197102789385229, 0.4242074625412317],
  "loss": 0.29870990342009757,
  "accuracy": 1.0,
  "chance_loss": 1.791759469228055
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
