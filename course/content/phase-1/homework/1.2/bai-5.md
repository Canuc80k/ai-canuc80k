# LOO

Mỗi học sinh cũ có điểm hai bài kiểm tra, và nhãn `+` nếu cuối kỳ đạt từ khá trở lên, `-` nếu không. Ta muốn dùng kNN phân loại để đoán nhãn ấy, và cần chọn $k$.

kNN phân loại đoán theo đa số trong $k$ hàng xóm gần nhất, khoảng cách Euclid. Khi hai hàng xóm cách đều, điểm đứng trước trong danh sách được coi là gần hơn. Mọi $k$ đều lẻ nên không có chuyện hòa phiếu.

Với mỗi $k$, hãy tính hai tỉ lệ lỗi. **Lỗi train** đoán từng điểm bằng kNN học trên toàn bộ dữ liệu, kể cả chính điểm ấy. **Lỗi leave-one-out** đoán từng điểm bằng kNN học trên mọi điểm trừ chính nó. Cuối cùng chọn `best_k` có lỗi leave-one-out nhỏ nhất, hòa thì lấy $k$ nhỏ hơn.

## Dữ liệu vào

Một đối tượng JSON gồm `points` (các điểm `[a, b, nhãn]`) và `ks` (các $k$, tăng dần).

## Kết quả

Một đối tượng JSON gồm `train_error`, `loo_error` (mỗi trường một số cho mỗi $k$) và `best_k`.

## Giới hạn

- Có từ $2$ đến $150$ điểm, không có hai điểm trùng nhau, tọa độ là số nguyên từ $0$ đến $100$.
- Mỗi $k$ là số lẻ, không vượt quá số điểm trừ $1$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "points": [
    [10, 60, "-"],
    [20, 55, "-"],
    [35, 30, "-"],
    [35, 85, "+"],
    [50, 20, "-"],
    [55, 10, "-"],
    [60, 55, "+"],
    [65, 55, "-"],
    [65, 75, "+"],
    [85, 60, "+"]
  ],
  "ks": [1, 3, 5]
}
```

```output
{
  "train_error": [0.0, 0.1, 0.1],
  "loo_error": [0.4, 0.2, 0.3],
  "best_k": 3
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
