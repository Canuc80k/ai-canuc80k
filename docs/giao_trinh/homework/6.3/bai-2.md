# Entity từ mảnh

Nhận dạng thực thể (NER) gắn nhãn cho từng **từ**, nhưng BERT làm việc trên từng **mảnh** (subword): một từ có thể thành nhiều mảnh. Bài này nối hai cấp ấy và chấm theo thực thể.

Nhãn theo kiểu BIO: `B-X` mở một thực thể loại `X`, `I-X` nối tiếp nó, `O` là ngoài thực thể. `word_ids[t]` cho biết mảnh $t$ thuộc từ nào (`null` với `[CLS]`, `[SEP]`).

1. **Gán nhãn cho mảnh.** Chỉ mảnh **đầu tiên** của mỗi từ mang nhãn của từ (dạng chỉ số trong `label_names`); mọi mảnh khác và các token đặc biệt có nhãn $-100$.
2. **Đọc dự đoán.** Nhãn dự đoán của một từ là nhãn mà mô hình dự đoán ở mảnh đầu tiên của từ ấy.
3. **Tách thực thể** từ dãy nhãn của các từ: một thực thể là đoạn bắt đầu bằng `B-X` hoặc `I-X`, nối tiếp bằng các `I-X` cùng loại. Một `I-X` không nối được (đứng sau `O` hay sau loại khác) được coi như mở thực thể mới. Thực thể ghi là $[X, \text{đầu}, \text{cuối})$ theo chỉ số từ, cuối không tính.
4. **F1 theo thực thể**: một thực thể dự đoán đúng khi trùng cả loại lẫn hai đầu với một thực thể thật. $F_1=\dfrac{2\,TP}{(\text{số thực thể thật})+(\text{số thực thể dự đoán})}$, bằng $0$ nếu mẫu số bằng $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `word_ids`, `word_tags` (nhãn thật của từng từ), `label_names` và `token_predictions` (chỉ số nhãn dự đoán cho từng mảnh).

## Kết quả

Một đối tượng JSON gồm `aligned_labels`, `predicted_word_tags`, `true_entities`, `predicted_entities` và `entity_f1`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "word_ids": [null, 0, 0, 1, 2, 3, 3, 4, 5, null],
  "word_tags": ["B-LOC", "I-LOC", "O", "B-ORG", "I-ORG", "O"],
  "label_names": ["O", "B-LOC", "I-LOC", "B-ORG", "I-ORG"],
  "token_predictions": [0, 1, 4, 2, 0, 3, 1, 4, 0, 2]
}
```

```output
{
  "aligned_labels": [-100, 1, -100, 2, 0, 3, -100, 4, 0, -100],
  "predicted_word_tags": ["B-LOC", "I-LOC", "O", "B-ORG", "I-ORG", "O"],
  "true_entities": [["LOC", 0, 2], ["ORG", 3, 5]],
  "predicted_entities": [["LOC", 0, 2], ["ORG", 3, 5]],
  "entity_f1": 1.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
