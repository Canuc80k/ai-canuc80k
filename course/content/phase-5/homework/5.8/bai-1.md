# Một vòng GAN

Một vòng huấn luyện GAN có hai bước: cập nhật discriminator $D$ trước, rồi cập nhật generator $G$. Bài này chạy đúng một vòng trên hai mô hình một chiều để thấy gradient đi đâu trong từng bước.

- $G(z)=g_wz+g_b$, sinh dữ liệu giả từ noise $z$.
- $D(x)=d_wx+d_b$, cho **logit** "là thật".

Mọi tính toán dùng `float64`.

1. **Bước của $D$.** Dữ liệu giả là $G(z)$ đã `detach`. Loss là trung bình `BCEWithLogitsLoss` trên dữ liệu thật với nhãn $1$, cộng trung bình trên dữ liệu giả với nhãn $0$. Cập nhật $D$ bằng `SGD(lr=0.1)`. Ghi lại xem sau `backward` này, tham số của $G$ có gradient không.
2. **Bước của $G$.** Khóa tham số của $D$ (không cho học). Dùng $D$ **đã cập nhật**, loss là trung bình `BCEWithLogitsLoss` của $D(G(z))$ với nhãn $1$. Cập nhật $G$ bằng `SGD(lr=0.1)`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `real`, `z` (cùng độ dài), `G` ($[g_w,g_b]$) và `D` ($[d_w,d_b]$).

## Kết quả

Một đối tượng JSON gồm `G` và `D` (tham số sau khi cập nhật), `loss_D` (trước khi cập nhật $D$), `loss_G` (sau khi cập nhật $D$, trước khi cập nhật $G$) và `generator_grad_none_in_D` (`true` nếu mọi gradient của $G$ là `None` sau bước của $D$).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "real": [
    1.2579566201493861, 0.8469836016079518, 1.2912115763419572,
    0.823576360390353, 0.9179030568104468
  ],
  "z": [
    -1.4851507532066648, -0.5892784016791289, -0.2716929192408032,
    -0.010106959976554775, -0.47104944812554067
  ],
  "G": [0.6, 0.1],
  "D": [0.5, -0.2]
}
```

```output
{
  "G": [0.5807580616801113, 0.13209882601582906],
  "D": [0.5518948626904272, -0.19988518679263118],
  "loss_D": 1.0985535515340192,
  "loss_G": 0.8761239136840236,
  "generator_grad_none_in_D": true
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
