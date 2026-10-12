# Chọn số chiều

Muốn biết cần giữ bao nhiêu thành phần chính, ta nhìn vào các giá trị kỳ dị $s_1\ge s_2\ge\dots$ của dữ liệu đã trừ trung bình. Phương sai mà thành phần thứ $i$ giữ tỉ lệ với $s_i^2$, không phải $s_i$.

Cho các giá trị kỳ dị và một ngưỡng, hãy tìm số $k$ nhỏ nhất sao cho $k$ thành phần đầu giữ được ít nhất ngần ấy phần phương sai:

$$
\frac{s_1^2+\dots+s_k^2}{s_1^2+s_2^2+\dots}\ge\text{threshold}.
$$

Nếu mọi giá trị kỳ dị đều bằng $0$ thì dữ liệu không có phương sai. Khi ấy ghi $k=0$ và tỉ lệ là `null`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `singular_values` (giảm dần, không âm) và `threshold` (trong khoảng $(0,1]$).

## Kết quả

Một đối tượng JSON gồm `k` và `retained` (tỉ lệ phương sai mà $k$ thành phần ấy giữ được).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"singular_values": [6, 3, 1], "threshold": 0.9}
```

```output
{"k": 2, "retained": 0.9782608695652174}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
