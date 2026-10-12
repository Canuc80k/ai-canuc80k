# Xếp hạng

Trong một đề thi, mỗi đội nộp dự đoán cho nhiều nhóm dữ liệu, mỗi nhóm vài tham số. Ban tổ chức chấm như sau.

Trước hết, tính RMSE của mỗi bài nộp trên **toàn bộ** tham số của mọi nhóm:

$$
\text{RMSE}=\sqrt{\frac1N\sum_{i=1}^{N}(\hat p_i-p_i)^2},
$$

với $N$ là tổng số tham số. Ban tổ chức cũng có một lời giải baseline, RMSE của nó là $X_{\text{base}}$. Gọi $X_{\text{best}}$ là RMSE nhỏ nhất trong các bài nộp. Một bài có RMSE $X$ được điểm

$$
\text{Score}=\frac{X_{\text{base}}-X}{X_{\text{base}}-X_{\text{best}}}\cdot100\%,
$$

còn nếu $X>X_{\text{base}}$ thì được $0$. Bài tốt nhất được trọn $100\%$.

Hãy tính bảng điểm.

## Dữ liệu vào

Một đối tượng JSON gồm:

- `truth`: tham số thật, mỗi nhóm một list.
- `baseline`: dự đoán của baseline, cùng hình dạng.
- `submissions`: ánh xạ tên đội tới dự đoán của đội, cùng hình dạng.

## Kết quả

Một đối tượng JSON gồm `baseline_rmse`, `rmse` (ánh xạ tên đội tới RMSE) và `score` (ánh xạ tên đội tới điểm phần trăm).

## Giới hạn

- Có từ $1$ đến $30$ nhóm, mỗi nhóm không quá $11$ tham số, từ $1$ đến $7$ đội.
- Mọi số có trị tuyệt đối không quá $100$. Luôn có ít nhất một đội tốt hơn baseline.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "truth": [[2, 4], [6, 8]],
  "baseline": [[5, 5], [5, 5]],
  "submissions": {
    "an": [[2, 4], [6, 9]],
    "binh": [[3, 5], [7, 9]],
    "chi": [[0, 0], [0, 0]]
  }
}
```

```output
{
  "baseline_rmse": 2.23606797749979,
  "rmse": {"an": 0.5, "binh": 1.0, "chi": 5.477225575051661},
  "score": {"an": 99.99999999999999, "binh": 71.19928444737063, "chi": 0.0}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 2, Ngày 2, Bài 5](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-2-day-2-problems.pdf#page=13).
:::
