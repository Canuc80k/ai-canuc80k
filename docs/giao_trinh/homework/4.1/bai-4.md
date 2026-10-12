# Đếm ResNet

ResNet-50 là một backbone pretrained rất hay dùng. Trước khi tải trọng số, nên biết nó có bao nhiêu tham số và mỗi tầng cho ra tensor shape gì. Bài này tính các con số ấy bằng tay, không dựng model, cho cả họ ResNet kiểu bottleneck với số block mỗi tầng tùy chọn.

Kiến trúc theo `torchvision`. Mọi conv **không có bias**; mỗi BatchNorm có $2C$ tham số với $C$ kênh. Conv $k\times k$ từ $c_{in}$ kênh sang $c_{out}$ kênh có $c_{in}c_{out}k^2$ tham số và cho kích thước không gian $\left\lfloor\frac{h+2p-k}{s}\right\rfloor+1$ với stride $s$, padding $p$.

1. **Thân đầu**: conv $7\times7$, $3\to64$ kênh, stride $2$, padding $3$; BatchNorm; ReLU; max pooling $3\times3$, stride $2$, padding $1$ (không có tham số).
2. **Bốn tầng**, tầng $s$ có `layers[s-1]` block và độ rộng $w=64\cdot2^{s-1}$. Mỗi block gồm conv $1\times1$ sang $w$ kênh; conv $3\times3$ $w\to w$, padding $1$; conv $1\times1$ $w\to4w$; mỗi conv có một BatchNorm theo sau. Block đầu của mỗi tầng có thêm nhánh tắt: conv $1\times1$ sang $4w$ kênh cùng một BatchNorm. Ở block đầu của tầng $2$, $3$, $4$, conv $3\times3$ và conv của nhánh tắt có stride $2$; mọi chỗ khác stride $1$.
3. **Đầu ra**: average pooling toàn cục, rồi `Linear(2048, num_classes)` có bias.

Ảnh đầu vào có $3$ kênh, kích thước `image_size` × `image_size`. Hãy tính:

- `parameters`: tổng số tham số học được.
- `stage_shapes`: shape `[kênh, cao, rộng]` của đầu ra mỗi tầng, không tính chiều batch.
- `block_conv_params`: tổng tham số của **các conv** (không tính BatchNorm) trong block `query_block` = `[s, i]`, tức block thứ $i$ (đánh từ $0$) của tầng $s$, kể cả conv nhánh tắt nếu có.

## Dữ liệu vào

Một đối tượng JSON gồm `layers` (bốn số), `num_classes`, `image_size` và `query_block`.

## Kết quả

Một đối tượng JSON gồm `parameters`, `stage_shapes` và `block_conv_params`.

## Giới hạn

- Mỗi tầng từ $1$ đến $6$ block, `image_size` từ $32$ đến $224$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "layers": [3, 4, 6, 3],
  "num_classes": 1000,
  "image_size": 224,
  "query_block": [3, 2]
}
```

```output
{
  "parameters": 25557032,
  "stage_shapes": [[256, 56, 56], [512, 28, 28], [1024, 14, 14], [2048, 7, 7]],
  "block_conv_params": 1114112
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 8.1–8.3](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=20).
:::
