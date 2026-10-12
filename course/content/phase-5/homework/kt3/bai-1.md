# Ảnh trong suốt

Ảnh PNG có thể có kênh thứ tư là độ trong suốt (alpha). Bỏ thẳng kênh ấy để được ảnh RGB là sai: điểm hoàn toàn trong suốt vẫn mang một màu "ẩn" không ai nhìn thấy. Đúng ra phải đặt ảnh lên một nền rồi trộn màu.

Mỗi điểm có $(R,G,B,a)$ với các số nguyên $0..255$; nền có màu $(R_b,G_b,B_b)$. Với từng kênh màu:
$$\text{kết quả}=\frac{a\cdot\text{màu}+(255-a)\cdot\text{nền}}{255},$$
làm tròn tới số nguyên gần nhất. $a=0$ cho đúng màu nền, $a=255$ cho đúng màu của điểm.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `rgba` (ảnh $2\times3$, mỗi điểm bốn số) và `background` (ba số).

## Kết quả

Một đối tượng JSON gồm `rgb`: ảnh $2\times3$, mỗi điểm ba số nguyên.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "rgba": [
    [[28, 217, 251, 0], [146, 111, 241, 128], [52, 185, 1, 255]],
    [[29, 49, 16, 255], [141, 255, 59, 1], [51, 205, 193, 254]]
  ],
  "background": [255, 250, 240]
}
```

```output
{
  "rgb": [
    [[255, 250, 240], [200, 180, 241], [52, 185, 1]],
    [[29, 49, 16], [255, 250, 239], [52, 205, 193]]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
