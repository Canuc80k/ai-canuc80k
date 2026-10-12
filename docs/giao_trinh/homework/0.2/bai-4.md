# Hiệu chỉnh ảnh

Một camera lưu ảnh bằng số nguyên từ $0$ đến $255$. Mỗi kênh màu có một độ tối nền `dark` và một hệ số khuếch đại `gain` riêng. Vài pixel bị đánh dấu là hỏng. Ta cần hiệu chỉnh ảnh, rồi thống kê các pixel còn tốt.

`frames` có shape $(N, H, W, C)$, lần lượt là ảnh, hàng, cột, kênh. `valid` có shape $(N, H, W)$, cho biết pixel nào còn tốt. `dark` và `gain` có $C$ phần tử.

Với giá trị $x$ ở kênh $j$:

$$
r=(x-\mathrm{dark}_j)\cdot\mathrm{gain}_j,\qquad
z=\frac{\min(255,\max(0,r))}{255}.
$$

Nhớ đổi sang số thực trước khi trừ. Trên kiểu `uint8`, phép trừ bị quay vòng, $0 - 100$ thành $156$.

Ảnh hiệu chỉnh gồm $z$ của **mọi** pixel. Mặt nạ `valid` chỉ dùng cho phần thống kê. Với từng ảnh, hãy tính:

- Số pixel tốt, đếm theo pixel chứ không nhân số kênh.
- Trung bình $z$ của các pixel tốt, riêng từng kênh.
- Số pixel tốt có $r<0$ và số pixel tốt có $r>255$, riêng từng kênh, xét trên $r$ trước khi cắt.

Ảnh không còn pixel tốt nào thì trung bình mỗi kênh là `null` và các số đếm là $0$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `frames`, `valid`, `dark`, `gain`.

## Kết quả

Một đối tượng JSON gồm:

- `corrected`: ảnh đã hiệu chỉnh, shape $(N, H, W, C)$.
- `frames`: $N$ đối tượng, mỗi đối tượng gồm `valid_pixels`, `mean`, `below_range`, `above_range`. Ba trường sau mỗi trường có $C$ giá trị.

## Giới hạn

- $1\le N\le4$, $1\le H,W\le12$, $C$ bằng $1$ hoặc $3$.
- Pixel và `dark` là số nguyên từ $0$ đến $255$, `gain` từ $0.5$ đến $4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "frames": [[[[0], [255]]]],
  "valid": [[[true, true]]],
  "dark": [100],
  "gain": [2]
}
```

```output
{
  "corrected": [[[[0.0], [1.0]]]],
  "frames": [
    {
      "valid_pixels": 2,
      "mean": [0.5],
      "below_range": [1],
      "above_range": [1]
    }
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
