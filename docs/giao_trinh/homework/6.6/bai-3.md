# Bộ nhớ KV cache

Khi sinh văn bản, mô hình giữ lại key và value của mọi token đã qua (KV cache) để khỏi tính lại. Với nhiều đầu attention, cache này có thể còn lớn hơn cả trọng số. Grouped-query attention (GQA) cho nhiều đầu query dùng chung một đầu key/value, nên cache chỉ phụ thuộc số đầu **key/value**.

Với $L$ lớp, $H_{kv}$ đầu key/value, mỗi đầu $d$ chiều, batch $B$, mỗi số chiếm $s$ byte, cache cho $N$ token chiếm
$$2\cdot B\cdot L\cdot H_{kv}\cdot d\cdot N\cdot s\ \text{byte}$$
(số $2$ vì có cả key lẫn value).

Hãy tính:

- `prefill_kv_bytes`: cache cho các token của prompt.
- `full_kv_bytes`: cache cho prompt và toàn bộ token mới.
- `dense_weight_bytes`: số tham số nhân số byte mỗi tham số.
- `minimum_bytes`: tổng hai số trên (chưa tính bộ nhớ tạm khi tính toán).

## Dữ liệu vào

Một đối tượng JSON gồm `layers`, `query_heads`, `kv_heads`, `head_dim`, `batch`, `prompt_tokens`, `new_tokens`, `kv_dtype_bytes`, `parameter_count` và `weight_dtype_bytes`.

## Kết quả

Một đối tượng JSON gồm `prefill_kv_bytes`, `full_kv_bytes`, `dense_weight_bytes` và `minimum_bytes`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "layers": 12,
  "query_heads": 16,
  "kv_heads": 1,
  "head_dim": 64,
  "batch": 1,
  "prompt_tokens": 128,
  "new_tokens": 0,
  "kv_dtype_bytes": 2,
  "parameter_count": 100000000,
  "weight_dtype_bytes": 2
}
```

```output
{
  "prefill_kv_bytes": 393216,
  "full_kv_bytes": 393216,
  "dense_weight_bytes": 200000000,
  "minimum_bytes": 200393216
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
