# Kiểm JSON trả về

Ta yêu cầu một LLM trả lời bằng JSON dạng `{"label": ..., "confidence": ...}`. Câu trả lời có thể hỏng ở ba tầng: không đọc được JSON, đọc được nhưng sai khuôn, đúng khuôn nhưng sai nội dung. Bài này kiểm cả ba tầng, theo đúng thứ tự.

**Tầng 1, đọc JSON** (chặt hơn `json.loads` mặc định):

- Một object (ở bất kỳ tầng nào) có khóa xuất hiện hai lần: lỗi `DUPLICATE_KEY`.
- Có `NaN`, `Infinity` hoặc `-Infinity`: lỗi `NONFINITE`.
- Có chuỗi chứa ký tự surrogate lẻ (mã từ `U+D800` tới `U+DFFF`): lỗi `UNICODE`.
- Không phải JSON hợp lệ (kể cả có chữ thừa sau JSON): lỗi `SYNTAX`.
- Số thực được đọc chính xác (như `decimal.Decimal`), nên `1e309` vẫn đọc được.

**Tầng 2, khuôn:** giá trị là object có **đúng** hai khóa `label` và `confidence`; `label` là một trong `positive`, `negative`, `neutral`; `confidence` là số (không phải `true`/`false`) trong đoạn $[0,1]$. Sai thì lỗi `SCHEMA`.

**Tầng 3, nội dung:** `label` bằng `gold_label`. Sai thì `CONTENT`; đúng thì `OK`.

## Dữ liệu vào

Một đối tượng JSON gồm `raw_response` (chuỗi trả về của mô hình) và `gold_label`.

## Kết quả

Một đối tượng JSON gồm `parse_ok`, `schema_ok`, `content_ok` và `failure` (một trong `SYNTAX`, `DUPLICATE_KEY`, `NONFINITE`, `UNICODE`, `SCHEMA`, `CONTENT`, `OK`). Tầng nào hỏng thì các tầng sau đều là `false`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "raw_response": "{\"label\":\"positive\",\"confidence\":0.9}",
  "gold_label": "positive"
}
```

```output
{
  "parse_ok": true,
  "schema_ok": true,
  "content_ok": true,
  "failure": "OK"
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
