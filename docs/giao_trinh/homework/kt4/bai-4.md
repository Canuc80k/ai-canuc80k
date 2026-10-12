# Thay, xóa, chèn

WER chỉ cho một con số. Muốn biết hệ nhận dạng hay sai kiểu gì, phải tách lỗi thành ba loại: **thay** một từ bằng từ khác (S), **xóa** mất một từ (D), **chèn** thêm một từ (I). Nhiều cách gióng hàng có thể cùng số lỗi, nên cần một quy tắc truy vết cố định.

Các câu đã viết không dấu, chữ thường; tách từ theo khoảng trắng. Bản chuẩn có $n$ từ $r_1..r_n$, bản nhận dạng có $m$ từ $h_1..h_m$.

1. **Bảng khoảng cách:** $d[i][0]=i$, $d[0][j]=j$, và
$$d[i][j]=\min\big(d[i-1][j-1]+[r_i\ne h_j],\ d[i-1][j]+1,\ d[i][j-1]+1\big).$$
2. **Truy vết** từ $(n,m)$ về $(0,0)$. Ở mỗi ô, thử theo thứ tự ưu tiên:
   - đi chéo nếu $i,j>0$ và $d[i][j]=d[i-1][j-1]+[r_i\ne h_j]$: ghi `C` (khớp) hoặc `S` (thay);
   - đi lên nếu $i>0$ và $d[i][j]=d[i-1][j]+1$: ghi `D`;
   - còn lại đi sang trái: ghi `I`.
3. `ops` là chuỗi các ký hiệu theo thứ tự từ đầu câu.

Gộp trên cả tập: WER là tổng số lỗi chia tổng số từ của bản chuẩn; tỉ lệ thay, xóa, chèn cũng chia cho tổng ấy.

## Dữ liệu vào

Một đối tượng JSON gồm `pairs`: mỗi cặp là `{"reference", "hypothesis"}`. Mọi bản chuẩn đều khác rỗng.

## Kết quả

Một đối tượng JSON gồm `pairs` (với mỗi cặp là `{"distance", "ops", "substitutions", "deletions", "insertions"}`), `wer` và `rates` (`{"substitution", "deletion", "insertion"}`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "pairs": [
    {"reference": "hom nay toi di hoc", "hypothesis": "hom nay toi hoc"},
    {"reference": "ban an com", "hypothesis": "ban an com o nha"},
    {"reference": "xe buyt den", "hypothesis": "xe bus den"},
    {"reference": "a b", "hypothesis": "b a"}
  ]
}
```

```output
{
  "pairs": [
    {
      "distance": 1,
      "ops": "CCCDC",
      "substitutions": 0,
      "deletions": 1,
      "insertions": 0
    },
    {
      "distance": 2,
      "ops": "CCCII",
      "substitutions": 0,
      "deletions": 0,
      "insertions": 2
    },
    {
      "distance": 1,
      "ops": "CSC",
      "substitutions": 1,
      "deletions": 0,
      "insertions": 0
    },
    {
      "distance": 2,
      "ops": "SS",
      "substitutions": 2,
      "deletions": 0,
      "insertions": 0
    }
  ],
  "wer": 0.46153846153846156,
  "rates": {
    "substitution": 0.23076923076923078,
    "deletion": 0.07692307692307693,
    "insertion": 0.15384615384615385
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
