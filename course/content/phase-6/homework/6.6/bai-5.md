# Self-consistency

Hỏi LLM một bài toán nhiều lần (lấy mẫu có ngẫu nhiên), các lời giải có thể ra đáp số khác nhau. Self-consistency lấy đáp số xuất hiện nhiều nhất. Bài này đo xem bỏ phiếu như vậy giúp được bao nhiêu.

1. **Trích đáp số** của mỗi lời giải: bỏ mọi dấu phẩy, rồi lấy **số cuối cùng** trong văn bản theo biểu thức chính quy `-?\d+(?:\.\d+)?`, đổi thành số thực. Không có số nào thì không có đáp số (`null`).
2. **Bỏ phiếu** trên một danh sách đáp số: bỏ qua `null`; đáp số có nhiều phiếu nhất thắng; bằng phiếu thì đáp số xuất hiện sớm nhất trong danh sách thắng. Không có phiếu nào thì kết quả là `null`.
3. Với mỗi $m$ trong `ms`, bỏ phiếu trên $m$ lời giải đầu của mỗi câu hỏi. Độ chính xác là tỉ lệ câu hỏi có kết quả bằng `gold` (sai khác dưới $10^{-9}$).

## Dữ liệu vào

Một đối tượng JSON gồm `questions` (mỗi câu là `{"gold", "samples"}`) và `ms` (mọi $m$ không quá số lời giải của mỗi câu).

## Kết quả

Một đối tượng JSON gồm `extracted` (đáp số trích được, theo câu hỏi và lời giải), `majority` (kết quả bỏ phiếu trên mọi lời giải của mỗi câu) và `by_m` (với mỗi $m$ là `{"m", "accuracy"}`).

## Giới hạn

- Không quá $6$ câu hỏi, mỗi câu không quá $9$ lời giải.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "questions": [
    {
      "gold": 18,
      "samples": [
        "Janet has 16 eggs, eats 3, bakes 4, so she sells 9 and earns 18 dollars.",
        "She sells 16 - 3 - 4 = 9 eggs at 2 each, the answer is 18.",
        "The answer is 14.", "9 * 2 = 18", "I think it is 16"
      ]
    },
    {
      "gold": 3,
      "samples": [
        "Two plus one is 3.", "The answer is 4.", "Answer: 4",
        "It equals 3", "I am not sure."
      ]
    },
    {
      "gold": 1250,
      "samples": [
        "The total is 1,250.", "So 1250 dollars.", "Total: 1,205",
        "He pays 1250.", "= 1250.0"
      ]
    }
  ],
  "ms": [1, 3, 5]
}
```

```output
{
  "extracted": [
    [18.0, 18.0, 14.0, 18.0, 16.0],
    [3.0, 4.0, 4.0, 3.0, null],
    [1250.0, 1250.0, 1205.0, 1250.0, 1250.0]
  ],
  "majority": [18.0, 3.0, 1250.0],
  "by_m": [
    {"m": 1, "accuracy": 1.0},
    {"m": 3, "accuracy": 0.6666666666666666},
    {"m": 5, "accuracy": 1.0}
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
