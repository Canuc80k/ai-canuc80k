# Describe

Mở một bảng dữ liệu mới, việc đầu tiên thường là gọi `describe()`. Bài này tự tính lại bảng ấy cho một cột số, bằng Python thuần, để hiểu từng con số pandas in ra.

Cột số cho dưới dạng list `values`, trong đó `null` là ô thiếu và được bỏ qua. Gọi các số còn lại, sau khi sắp tăng dần, là $v_0\le v_1\le\dots\le v_{n-1}$. Hãy tính:

- `count`: số giá trị có mặt, tức $n$.
- `mean`: trung bình $\bar v$.
- `std`: độ lệch chuẩn, **chia cho $n-1$** như pandas. Khi $n=1$, `std` là `null`.
- `min`, `max`.
- `25%`, `50%`, `75%`: phân vị theo cách của pandas. Với phân vị $p$, đặt $t=p(n-1)$ và $k=\lfloor t\rfloor$, phân vị bằng $v_k+(t-k)(v_{k+1}-v_k)$. Phân vị $50\%$ chính là median.
- `z`: điểm chuẩn hóa của số `x` cho trong đề, $z=(x-\bar v)/s$ với $s$ là `std`. Nếu `std` là `null` hoặc bằng $0$ thì `z` là `null`.
- `mean_minus_median`: mean trừ median. Hiệu dương thường cho thấy phân bố có đuôi dài bên phải, khi vài giá trị rất lớn kéo mean lên còn median gần như đứng yên.

Công thức độ lệch chuẩn:

$$
s=\sqrt{\frac{1}{n-1}\sum_{i=0}^{n-1}(v_i-\bar v)^2}.
$$

Bài nộp chỉ dùng thư viện chuẩn. Trên máy, có thể so với `pd.Series(values, dtype=float).describe()`.

## Dữ liệu vào

Một đối tượng JSON gồm `values` và `x`.

## Kết quả

Một đối tượng JSON gồm mười trường `count`, `mean`, `std`, `min`, `25%`, `50%`, `75%`, `max`, `z`, `mean_minus_median`.

## Giới hạn

- `values` có từ $1$ đến $1000$ phần tử, ít nhất một phần tử có mặt. Mọi số có trị tuyệt đối không quá $10^6$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"values": [3, 1, null, 4, 1, 5, 9, 2, 6], "x": 9}
```

```output
{
  "count": 8,
  "mean": 3.875,
  "std": 2.748376143938713,
  "min": 1.0,
  "25%": 1.75,
  "50%": 3.5,
  "75%": 5.25,
  "max": 9.0,
  "z": 1.8647374782752024,
  "mean_minus_median": 0.375
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, các câu 57–69](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=23).
:::
