# Hai lần softmax

Một lỗi hay gặp: mô hình đã kết thúc bằng softmax, rồi đầu ra ấy lại được đưa vào `CrossEntropyLoss`, hàm vốn tự áp softmax thêm lần nữa. Loss vẫn giảm, nhưng dừng ở một cái sàn cao bất thường.

Cho logits và nhãn của một batch. Hãy tính:

- `correct_loss`: `CrossEntropyLoss` trung bình trên logits.
- `wrong_loss`: `CrossEntropyLoss` trung bình khi đưa vào xác suất softmax của logits, như thể chúng là logits.
- `wrong_best_possible_floor`: giá trị của `wrong_loss` khi xác suất softmax đã hoàn hảo, tức bằng $1$ ở lớp đúng và $0$ ở các lớp khác. Với $C$ lớp, giá trị ấy là $\ln(e+C-1)-1$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `logits` (mỗi hàng $C$ số) và `labels`.

## Kết quả

Một đối tượng JSON gồm `correct_loss`, `wrong_loss` và `wrong_best_possible_floor`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [
    [1.3171059985649483, 50.0],
    [0.8968118662316843, 50.0],
    [1.322858784410326, 50.0],
    [50.0, 0.627823756515188],
    [-0.8061661641315654, 50.0]
  ],
  "labels": [1, 1, 1, 0, 1]
}
```

```output
{
  "correct_loss": 0.0,
  "wrong_loss": 0.3132616875182228,
  "wrong_best_possible_floor": 0.3132616875182226
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
