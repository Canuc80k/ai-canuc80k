# Giữ EOS

Một tokenizer mức từ đơn giản cho Transformer: dựng từ điển theo tần suất, rồi mã hóa mỗi câu thành dãy số có độ dài cố định. Chỗ dễ sai là khi câu quá dài.

**Dựng từ điển.** Bốn token đặc biệt có mã cố định: `<PAD>`$=0$, `<UNK>`$=1$, `<BOS>`$=2$, `<EOS>`$=3$. Đổi các câu trong `train` về chữ thường, tách theo khoảng trắng, đếm số lần mỗi từ xuất hiện. Lấy `vocab_size` $-4$ từ xuất hiện nhiều nhất (bằng nhau thì từ gặp trước trong `train` đứng trước), đánh mã tiếp từ $4$.

**Mã hóa** mỗi câu trong `texts` thành đúng `max_len` số:

1. Chữ thường, tách theo khoảng trắng, đổi mỗi từ thành mã của nó (không có thì `<UNK>`).
2. Nếu dãy dài hơn `max_len` $-2$, cắt bớt **phần cuối của các từ**, để còn chỗ cho `<BOS>` ở đầu và `<EOS>` ở cuối. Câu bị cắt vẫn phải kết thúc bằng `<EOS>`.
3. Thêm `<BOS>` và `<EOS>`, rồi đệm `<PAD>` ở cuối cho đủ `max_len`.
4. Attention mask là $1$ ở các vị trí không phải đệm, $0$ ở các vị trí đệm.

## Dữ liệu vào

Một đối tượng JSON gồm `train`, `vocab_size`, `max_len` và `texts`.

## Kết quả

Một đối tượng JSON gồm `vocab` (các token theo thứ tự mã, kể cả bốn token đặc biệt) và `encoded`: với mỗi câu là `{"ids", "attention_mask", "truncated", "unk"}`, trong đó `truncated` cho biết câu có bị cắt không, `unk` là số mã `<UNK>` trong `ids`.

## Giới hạn

- $4\le$ `max_len` $\le12$, không quá $10$ câu train và $5$ câu cần mã hóa.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "train": [
    "Hello world", "how are you", "hello my friend", "are you there",
    "hello you"
  ],
  "vocab_size": 9,
  "max_len": 8,
  "texts": [
    "Hello world how are you today my friend", "hello friend",
    "you are my world", "how are you hello"
  ]
}
```

```output
{
  "vocab": [
    "<PAD>", "<UNK>", "<BOS>", "<EOS>", "hello", "you", "are", "world",
    "how"
  ],
  "encoded": [
    {
      "ids": [2, 4, 7, 8, 6, 5, 1, 3],
      "attention_mask": [1, 1, 1, 1, 1, 1, 1, 1],
      "truncated": true,
      "unk": 1
    },
    {
      "ids": [2, 4, 1, 3, 0, 0, 0, 0],
      "attention_mask": [1, 1, 1, 1, 0, 0, 0, 0],
      "truncated": false,
      "unk": 1
    },
    {
      "ids": [2, 5, 6, 1, 7, 3, 0, 0],
      "attention_mask": [1, 1, 1, 1, 1, 1, 0, 0],
      "truncated": false,
      "unk": 1
    },
    {
      "ids": [2, 8, 6, 5, 4, 3, 0, 0],
      "attention_mask": [1, 1, 1, 1, 1, 1, 0, 0],
      "truncated": false,
      "unk": 0
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 19](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=30).
:::
