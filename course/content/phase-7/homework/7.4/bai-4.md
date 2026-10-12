# Token ảnh

Mô hình ngôn ngữ thị giác (VLM) đổi ảnh thành các token rồi đặt trước câu hỏi. Ảnh độ phân giải cao tốn rất nhiều token. Bài này tính số token ảnh theo cách của LLaVA-NeXT và kiểm xem ảnh có vừa ngữ cảnh không.

Bộ mã hóa ảnh nhận ảnh vuông cạnh `base_size` và chia thành patch cạnh `patch_size`, nên mỗi ô ảnh cho $(\text{base\_size}/\text{patch\_size})^2$ token.

1. **Chọn lưới.** Với ảnh rộng $w$, cao $h$, xét từng lưới $[g_x,g_y]$ trong `grids` (tức khung rộng $W=g_x\cdot$`base_size`, cao $H=g_y\cdot$`base_size`):
   - thu ảnh giữ tỉ lệ để vừa khung: hệ số $s=\min(W/w,\ H/h)$, kích thước $\lfloor ws\rfloor\times\lfloor hs\rfloor$;
   - độ phân giải hiệu dụng $=\min(\lfloor ws\rfloor\cdot\lfloor hs\rfloor,\ wh)$; phần thừa $=WH-$ độ phân giải hiệu dụng.
   
   Chọn lưới có độ phân giải hiệu dụng lớn nhất; bằng nhau thì phần thừa nhỏ nhất; vẫn bằng nhau thì lưới đứng trước trong danh sách.
2. **Đếm token.** Ảnh cho một ô toàn cảnh (ảnh thu về `base_size`) cộng $g_xg_y$ ô chi tiết: tổng $(1+g_xg_y)$ ô.
3. **Ngữ cảnh.** Tổng token là `text_tokens` cộng token của mọi ảnh. Báo tổng ấy có vượt `context_length` không, và nếu đưa ảnh vào lần lượt theo thứ tự (sau phần chữ) thì được bao nhiêu ảnh đầu tiên trước khi vượt.

## Dữ liệu vào

Một đối tượng JSON gồm `base_size`, `patch_size`, `grids`, `images` (các cặp $[w,h]$), `text_tokens` và `context_length`.

## Kết quả

Một đối tượng JSON gồm `tokens_per_tile`, `images` (với mỗi ảnh là `{"grid", "tiles", "image_tokens"}`), `total_tokens`, `fits` và `images_that_fit`.

## Giới hạn

- Không quá $4$ ảnh và $6$ lưới.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "base_size": 336,
  "patch_size": 14,
  "grids": [[1, 2], [2, 1], [2, 2], [1, 3], [3, 1]],
  "images": [[1000, 500], [400, 1200], [336, 336], [800, 800]],
  "text_tokens": 200,
  "context_length": 4096
}
```

```output
{
  "tokens_per_tile": 576,
  "images": [
    {"grid": [2, 1], "tiles": 2, "image_tokens": 1728},
    {"grid": [1, 3], "tiles": 3, "image_tokens": 2304},
    {"grid": [1, 2], "tiles": 2, "image_tokens": 1728},
    {"grid": [2, 2], "tiles": 4, "image_tokens": 2880}
  ],
  "total_tokens": 8840,
  "fits": false,
  "images_that_fit": 1
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
