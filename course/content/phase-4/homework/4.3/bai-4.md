# Cắt backbone

Muốn phân loại ảnh vào vài lớp mới, ta có thể lấy một ResNet đã học, cắt bỏ phần sau một block nào đó, giữ nguyên (đóng băng) phần trước làm backbone, rồi gắn một head mới: average pooling toàn cục và `Linear(C, num_classes)`, với $C$ là số kênh tại chỗ cắt.

Kiến trúc ResNet giống bài D của buổi 4.1: thân đầu (conv $7\times7$ stride $2$, BatchNorm, ReLU, max pooling stride $2$), rồi bốn tầng bottleneck với số block trong `layers`, độ rộng $64\cdot2^{s-1}$ ở tầng $s$, đầu ra $4\times$ độ rộng, stride $2$ ở block đầu của tầng $2$ trở đi, nhánh tắt ở block đầu mỗi tầng. Conv không có bias; mỗi BatchNorm có $2C$ tham số.

Backbone giữ thân đầu, mọi tầng trước tầng $s$, và các block $0,1,\dots,i$ của tầng $s$, với `cut` = `[s, i]`. Mọi tham số của backbone bị đóng băng; chỉ head được học. Hãy tính:

- `feature_shape`: shape `[kênh, cao, rộng]` của đầu ra backbone với ảnh `image_size` × `image_size`.
- `frozen_params`: số tham số của backbone.
- `trainable_params`: số tham số của head.
- `trainable_fraction`: tỉ lệ tham số học được trên tổng.

## Dữ liệu vào

Một đối tượng JSON gồm `layers`, `cut`, `num_classes` và `image_size`.

## Kết quả

Một đối tượng JSON gồm `feature_shape`, `frozen_params`, `trainable_params` và `trainable_fraction`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "layers": [3, 4, 6, 3],
  "cut": [3, 4],
  "num_classes": 5,
  "image_size": 224
}
```

```output
{
  "feature_shape": [1024, 14, 14],
  "frozen_params": 7426112,
  "trainable_params": 5125,
  "trainable_fraction": 0.0006896563788774332
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 8.4](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=21).
:::
