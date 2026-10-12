# Chi phí ViT

ViT xem ảnh như một chuỗi patch. Patch nhỏ hơn thì nhìn chi tiết hơn, nhưng chuỗi dài hơn, và attention đắt theo bình phương độ dài chuỗi. Bài này tính các con số ấy cho vài kích thước patch.

Ảnh cỡ $H\times W$ có $C$ kênh; mô hình có độ rộng $d$, `heads` đầu attention và $L$ lớp. Với patch cỡ $p$:

- Số patch $n=\lfloor H/p\rfloor\cdot\lfloor W/p\rfloor$; số token $N=n+1$ (thêm CLS).
- Lớp nhúng patch là conv kernel $p$, stride $p$, từ $C$ lên $d$ kênh, có bias: $C p^2 d+d$ tham số.
- Bảng mã vị trí: $N\cdot d$ tham số.
- Số ô của các ma trận attention trên mọi lớp, mọi đầu: $L\cdot\text{heads}\cdot N^2$.
- Phép nhân-cộng (MAC) của phần attention mỗi lớp: $4Nd^2$ (bốn phép chiếu Q, K, V, đầu ra) cộng $2N^2d$ (tính điểm số và trộn value). Nhân với $L$.
- MAC của MLP mỗi lớp (hai lớp tuyến tính $d\to4d\to d$): $8Nd^2$. Nhân với $L$.
- `attention_share`: MAC attention chia tổng MAC attention và MLP.

## Dữ liệu vào

Một đối tượng JSON gồm `height`, `width`, `channels`, `d_model`, `heads`, `layers` và `patch_sizes`.

## Kết quả

Một đối tượng JSON: với mỗi kích thước patch (khóa là chuỗi, như `"16"`) là `{"patches", "tokens", "embedding_params", "position_params", "attention_score_entries", "attention_macs", "mlp_macs", "attention_share"}`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "height": 224,
  "width": 224,
  "channels": 3,
  "d_model": 768,
  "heads": 12,
  "layers": 12,
  "patch_sizes": [32, 16, 8]
}
```

```output
{
  "32": {
    "patches": 49,
    "tokens": 50,
    "embedding_params": 2360064,
    "position_params": 38400,
    "attention_score_entries": 360000,
    "attention_macs": 1461657600,
    "mlp_macs": 2831155200,
    "attention_share": 0.34048948046371835
  },
  "16": {
    "patches": 196,
    "tokens": 197,
    "embedding_params": 590592,
    "position_params": 151296,
    "attention_score_entries": 5588496,
    "attention_macs": 6292703232,
    "mlp_macs": 11154751488,
    "attention_share": 0.3606659729448491
  },
  "8": {
    "patches": 784,
    "tokens": 785,
    "embedding_params": 148224,
    "position_params": 602880,
    "attention_score_entries": 88736400,
    "attention_macs": 33582827520,
    "mlp_macs": 44449136640,
    "attention_share": 0.43037270535879846
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 260](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=93).
:::
