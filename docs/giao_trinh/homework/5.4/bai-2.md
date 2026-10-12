# Nội suy vị trí

Một ViT đã học với lưới patch cỡ $h\times w$ có bảng mã vị trí $1+hw$ hàng: hàng đầu cho token CLS, các hàng sau cho từng patch theo thứ tự hàng. Đổi kích thước ảnh thì lưới đổi, và bảng mã vị trí phải được nội suy theo lưới mới.

1. Tách hàng CLS ra, giữ nguyên.
2. Xếp các hàng còn lại thành lưới $h\times w$ (mỗi ô hai số), nội suy song tuyến tính (bilinear) sang lưới mới với `align_corners=True`, tức bốn góc của lưới cũ và lưới mới trùng nhau.
3. Ghép hàng CLS lên đầu, trải lưới mới theo thứ tự hàng.

Có thể dùng `torch.nn.functional.interpolate(..., mode="bilinear", align_corners=True)`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `table`, `old_grid` ($[h,w]$) và `new_grid`.

## Kết quả

Một đối tượng JSON `{"table": [...]}` với $1+h'w'$ hàng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "table": [
    [-0.733, -3.137],
    [-1.173, -0.826],
    [0.905, 1.578],
    [0.263, 0.05],
    [-1.796, 1.016],
    [-0.16, 2.589],
    [1.065, -1.0],
    [1.237, -0.624],
    [-0.713, 0.254]
  ],
  "old_grid": [4, 2],
  "new_grid": [3, 2]
}
```

```output
{
  "table": [
    [-0.733, -3.137],
    [-1.173, -0.826],
    [0.905, 1.578],
    [0.051500000000000004, 1.3195],
    [-0.36550000000000005, 0.008000000000000007],
    [1.237, -0.624],
    [-0.713, 0.254]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
