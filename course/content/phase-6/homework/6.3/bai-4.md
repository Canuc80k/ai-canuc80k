# Mã hóa cặp câu

Khi fine-tune BERT cho bài toán cặp câu (câu hỏi và đoạn văn, hai câu có cùng nghĩa không), hai câu được ghép thành một dãy:
$$[\text{CLS}]\ A\ [\text{SEP}]\ B\ [\text{SEP}].$$
Dãy phải có đúng `max_length` token, nên câu dài phải bị cắt và câu ngắn phải được đệm. Bài này làm đúng việc của tokenizer khi gọi với `padding="max_length", truncation=True`.

1. Đổi mỗi câu về chữ thường, tách theo khoảng trắng, đổi mỗi từ thành mã trong `vocab` (không có thì mã của `[UNK]`).
2. **Cắt kiểu longest_first.** Ba token đặc biệt chiếm $3$ chỗ. Chừng nào tổng độ dài $|A|+|B|+3$ còn vượt `max_length`, bỏ token cuối của câu **dài hơn**; hai câu dài bằng nhau thì bỏ ở câu $B$.
3. Ghép dãy như trên. `token_type_ids` bằng $0$ cho `[CLS]`, câu $A$ và `[SEP]` đầu; bằng $1$ cho câu $B$ và `[SEP]` cuối.
4. Đệm `[PAD]` ở cuối cho đủ `max_length`. Ở vị trí đệm, `token_type_ids` bằng $0$ và `attention_mask` bằng $0$; các vị trí khác có `attention_mask` bằng $1$.

Báo thêm số token đã bỏ và độ dài còn lại của hai câu.

## Dữ liệu vào

Một đối tượng JSON gồm `vocab` (từ từ tới mã, có `[PAD]`, `[UNK]`, `[CLS]`, `[SEP]`), `max_length` và `pairs` (list các cặp $[A, B]$).

## Kết quả

Một đối tượng JSON gồm `encoded`: với mỗi cặp là `{"input_ids", "token_type_ids", "attention_mask", "removed", "kept"}`, với `kept` là $[|A|, |B|]$ sau khi cắt.

## Giới hạn

- $5\le$ `max_length` $\le16$, không quá $5$ cặp.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "vocab": {
    "[PAD]": 0,
    "[UNK]": 1,
    "[CLS]": 2,
    "[SEP]": 3,
    "where": 4,
    "is": 5,
    "the": 6,
    "cat": 7,
    "sat": 8,
    "on": 9,
    "mat": 10
  },
  "max_length": 10,
  "pairs": [
    ["Where is the cat", "The cat sat on the mat today"],
    ["the cat", "sat"],
    ["the cat sat on", "the mat"]
  ]
}
```

```output
{
  "encoded": [
    {
      "input_ids": [2, 4, 5, 6, 7, 3, 6, 7, 8, 3],
      "token_type_ids": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
      "attention_mask": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      "removed": 4,
      "kept": [4, 3]
    },
    {
      "input_ids": [2, 6, 7, 3, 8, 3, 0, 0, 0, 0],
      "token_type_ids": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
      "attention_mask": [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
      "removed": 0,
      "kept": [2, 1]
    },
    {
      "input_ids": [2, 6, 7, 8, 9, 3, 6, 10, 3, 0],
      "token_type_ids": [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
      "attention_mask": [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
      "removed": 0,
      "kept": [4, 2]
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 21](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=34).
:::
