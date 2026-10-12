# pass@k

Chấm một mô hình sinh code: với mỗi bài, cho mô hình sinh $n$ lời giải và chạy test, được $c$ lời giải đúng. pass@$k$ là xác suất trong $k$ lời giải (nộp $k$ lần) có ít nhất một lời giải đúng.

**Ước lượng không chệch.** Chọn ngẫu nhiên $k$ trong $n$ lời giải đã sinh, không lặp:
$$\text{pass@}k=1-\frac{\binom{n-c}{k}}{\binom{n}{k}},$$
bằng $1$ nếu $n-c<k$. Số tổ hợp rất lớn, nên tính bằng tích
$$\frac{\binom{n-c}{k}}{\binom{n}{k}}=\prod_{i=n-c+1}^{n}\left(1-\frac{k}{i}\right).$$

**Cách ngây thơ.** Coi $\hat p=c/n$ là xác suất đúng của một lần nộp, rồi tính $1-(1-\hat p)^k$.

Với mỗi $k$ trong `ks`, báo pass@$k$ không chệch của từng bài, trung bình trên các bài, trung bình của cách ngây thơ, và độ chênh (ngây thơ trừ không chệch).

## Dữ liệu vào

Một đối tượng JSON gồm `problems` (mỗi bài là `{"n", "c"}`) và `ks` (mọi $k\le n$).

## Kết quả

Một đối tượng JSON gồm `results`: với mỗi $k$ là `{"k", "per_problem", "pass_at_k", "naive", "gap"}`.

## Giới hạn

- $n\le200$, không quá $6$ bài.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "problems": [
    {"n": 10, "c": 3},
    {"n": 10, "c": 0},
    {"n": 10, "c": 10},
    {"n": 10, "c": 1}
  ],
  "ks": [1, 5, 10]
}
```

```output
{
  "results": [
    {
      "k": 1,
      "per_problem": [0.3, 0.0, 1.0, 0.1],
      "pass_at_k": 0.35,
      "naive": 0.35,
      "gap": 0.0
    },
    {
      "k": 5,
      "per_problem": [0.9166666666666666, 0.0, 1.0, 0.5],
      "pass_at_k": 0.6041666666666666,
      "naive": 0.56036,
      "gap": -0.04380666666666667
    },
    {
      "k": 10,
      "per_problem": [1.0, 0.0, 1.0, 1.0],
      "pass_at_k": 0.75,
      "naive": 0.65576850875,
      "gap": -0.09423149125
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
