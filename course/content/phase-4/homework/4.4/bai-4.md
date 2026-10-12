# Ngân sách LoRA

Trước khi fine-tune một Transformer bằng LoRA, nên tính xem mình tiết kiệm được bao nhiêu. Mỗi block của mô hình có sáu ma trận trọng số (không tính bias):

| Tên | Cỡ (đầu ra × đầu vào) |
|---|---|
| `q`, `k`, `v`, `o` | $d\times d$ |
| `ff1` | $d_{ff}\times d$ |
| `ff2` | $d\times d_{ff}$ |

Chèn LoRA hạng $r$ vào một ma trận $d_{out}\times d_{in}$ thêm $r(d_{in}+d_{out})$ số được học. LoRA được chèn vào các ma trận có tên trong `targets`, ở mọi block.

Ước lượng bộ nhớ theo buổi 3.7, FP32 và Adam: mỗi tham số được học tốn $16$ byte (trọng số, gradient, hai trạng thái Adam); mỗi tham số đóng băng chỉ tốn $4$ byte.

Hãy tính:

- `full_params`: số tham số của mọi ma trận ở mọi block, tức số tham số phải học nếu fine-tune toàn bộ.
- `lora_params`: số tham số adapter với hạng `rank`.
- `ratio`: `lora_params` chia `full_params`.
- `full_adam_bytes`: $16\cdot$`full_params`.
- `lora_adam_bytes`: $4\cdot$`full_params` $+\ 16\cdot$`lora_params`.
- `max_rank`: hạng lớn nhất sao cho số tham số adapter không vượt `budget` (có thể bằng $0$).
- `break_even_rank`: với mỗi ma trận trong `targets`, hạng nhỏ nhất mà adapter có ít nhất bằng số tham số của chính ma trận ấy.

## Dữ liệu vào

Một đối tượng JSON gồm `blocks`, `d_model` ($d$), `d_ff`, `targets`, `rank` và `budget`.

## Kết quả

Một đối tượng JSON gồm bảy trường ở trên; `break_even_rank` là một đối tượng từ tên ma trận tới số nguyên.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "blocks": 6,
  "d_model": 768,
  "d_ff": 3072,
  "targets": ["q", "v"],
  "rank": 4,
  "budget": 200000
}
```

```output
{
  "full_params": 42467328,
  "lora_params": 73728,
  "ratio": 0.001736111111111111,
  "full_adam_bytes": 679477248,
  "lora_adam_bytes": 171048960,
  "max_rank": 10,
  "break_even_rank": {"q": 384, "v": 384}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 246](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=88).
:::
