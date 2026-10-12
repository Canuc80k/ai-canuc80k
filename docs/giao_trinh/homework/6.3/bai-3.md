# Chọn đoạn trả lời

QA trích xuất: mô hình cho mỗi token một điểm "bắt đầu" và một điểm "kết thúc", và câu trả lời là một đoạn của ngữ cảnh. Chọn đoạn sai cách thì có thể ra một đoạn nằm trong câu hỏi, hoặc đoạn có đầu sau cuối.

Token $0$ là `[CLS]`. `context_mask` cho biết token nào thuộc ngữ cảnh.

1. Một đoạn $[s, e]$ hợp lệ khi $s\le e$, độ dài $e-s+1$ không quá `max_answer_length`, và **mọi** token từ $s$ tới $e$ thuộc ngữ cảnh.
2. Điểm của đoạn là `start_logits[s]` + `end_logits[e]`. Chọn đoạn hợp lệ có điểm lớn nhất; bằng nhau thì $(s,e)$ nhỏ hơn theo thứ tự từ điển.
3. Điểm "không có câu trả lời" là `start_logits[0]` + `end_logits[0]`. Chỉ trả lời khi điểm đoạn tốt nhất lớn hơn điểm ấy cộng `null_margin`; bằng nhau thì không trả lời.
4. Nếu không có đoạn hợp lệ, hoặc không vượt ngưỡng, trả `{"span": null, "answer_tokens": [], "score": điểm không trả lời}`. Ngược lại trả `{"span": [s, e], "answer_tokens": các token từ s tới e, "score": điểm đoạn}`.

## Dữ liệu vào

Một đối tượng JSON gồm `tokens`, `start_logits`, `end_logits`, `context_mask`, `max_answer_length` và `null_margin`.

## Kết quả

Một đối tượng JSON gồm `span`, `answer_tokens` và `score`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "tokens": [
    "[CLS]", "ở", "đâu", "[SEP]", "nhà", "sách", "ven", "sông",
    "[SEP]", "[PAD]"
  ],
  "start_logits": [-3.0, 4.0, 100.0, 3.0, -2.0, 3.0, 4.0, -3.0, -3.0, 3.0],
  "end_logits": [-1.0, 100.0, 3.0, 0.0, 2.0, 4.0, 4.0, 3.0, -1.0, 0.0],
  "context_mask": [false, false, false, false, false, false, false, false, false, false],
  "max_answer_length": 1,
  "null_margin": 0.0
}
```

```output
{"span": null, "answer_tokens": [], "score": -4.0}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
