# EM và F1

Chấm một hệ hỏi đáp trích xuất như bộ SQuAD: so câu trả lời của mô hình với một hoặc vài đáp án đúng, theo hai thước đo.

**Chuẩn hóa** một chuỗi, theo thứ tự: đổi chữ thường; bỏ mọi dấu câu (các ký tự trong `string.punctuation` của Python); bỏ các mạo từ `a`, `an`, `the` khi chúng đứng thành từ riêng; gộp khoảng trắng (tách theo khoảng trắng rồi nối lại bằng một dấu cách).

- **Exact Match (EM):** $1$ nếu câu trả lời sau chuẩn hóa trùng hẳn một đáp án sau chuẩn hóa, ngược lại $0$.
- **F1:** tách hai chuỗi đã chuẩn hóa thành từ. Số từ chung đếm theo bội (một từ xuất hiện $2$ lần ở cả hai thì tính $2$). Precision là số từ chung chia số từ của câu trả lời, recall là số từ chung chia số từ của đáp án, F1 là trung bình điều hòa. Nếu một trong hai chuỗi rỗng, F1 bằng $1$ khi cả hai cùng rỗng và $0$ nếu không. Không có từ chung thì F1 bằng $0$.
- Mỗi câu hỏi lấy **max** EM và **max** F1 trên các đáp án. Điểm chung là trung bình trên các câu hỏi.

## Dữ liệu vào

Một đối tượng JSON gồm `questions`: mỗi câu hỏi là `{"prediction", "answers"}`.

## Kết quả

Một đối tượng JSON gồm `per_question` (với mỗi câu hỏi là `{"normalized_prediction", "exact_match", "f1"}`), `exact_match` và `f1`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "questions": [
    {
      "prediction": "the Eiffel Tower",
      "answers": ["Eiffel Tower", "the Eiffel tower in Paris"]
    },
    {"prediction": "in 1889.", "answers": ["1889"]},
    {"prediction": "Paris, France", "answers": ["Paris"]},
    {
      "prediction": "a red red car",
      "answers": ["red car", "the blue car"]
    },
    {"prediction": "the", "answers": ["an"]}
  ]
}
```

```output
{
  "per_question": [
    {
      "normalized_prediction": "eiffel tower",
      "exact_match": 1.0,
      "f1": 1.0
    },
    {
      "normalized_prediction": "in 1889",
      "exact_match": 0.0,
      "f1": 0.6666666666666666
    },
    {
      "normalized_prediction": "paris france",
      "exact_match": 0.0,
      "f1": 0.6666666666666666
    },
    {
      "normalized_prediction": "red red car",
      "exact_match": 0.0,
      "f1": 0.8
    },
    {"normalized_prediction": "", "exact_match": 1.0, "f1": 1.0}
  ],
  "exact_match": 0.4,
  "f1": 0.8266666666666665
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
