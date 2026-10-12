# Từ điển

Trước khi đưa câu vào embedding, phải biến từ thành ID. Bài này dựng từ điển từ dữ liệu train, mã hóa các câu test, và kiểm một hạn chế của việc lấy trung bình embedding.

Mỗi câu là một chuỗi, các từ cách nhau bởi dấu cách.

1. Đếm số lần mỗi từ xuất hiện trong train. Chỉ giữ các từ xuất hiện ít nhất `min_freq` lần.
2. Từ điển bắt đầu bằng `<pad>` (ID $0$) và `<unk>` (ID $1$), tiếp theo là các từ được giữ, xếp theo số lần xuất hiện giảm dần; cùng số lần thì xếp theo thứ tự mã Unicode của chuỗi, như hàm `sorted` của Python.
3. Mã hóa từng câu test, từ không có trong từ điển thành `<unk>`. Chèn `<pad>` bên phải để mọi câu dài bằng câu dài nhất.
4. Tỉ lệ từ ngoài từ điển (`oov_rate`) là số token `<unk>` chia cho tổng số token của các câu test, chưa tính `<pad>`. Không có token nào thì ghi `null`.
5. Lấy trung bình embedding của các token là cách biểu diễn câu không quan tâm thứ tự. Liệt kê các cặp câu test $[i, j]$ với $i<j$, câu $i$ khác rỗng, có dãy ID **khác nhau** nhưng gồm đúng cùng các ID với cùng số lần. Mọi bảng embedding đều cho hai câu ấy cùng một vector trung bình.

## Dữ liệu vào

Một đối tượng JSON gồm `train`, `test` (các câu) và `min_freq`.

## Kết quả

Một đối tượng JSON gồm `vocab`, `padded`, `lengths`, `oov_rate` và `same_bag` (các cặp, theo thứ tự tăng của $i$ rồi $j$).

## Giới hạn

- Không quá $10$ câu train và $7$ câu test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "train": ["con meo duoi con chuot", "con cho duoi con meo", "chuot an pho mai"],
  "test": ["con cho duoi con meo", "con meo duoi con cho", "meo an banh", "cho"],
  "min_freq": 2
}
```

```output
{
  "vocab": ["<pad>", "<unk>", "con", "chuot", "duoi", "meo"],
  "padded": [[2, 1, 4, 2, 5], [2, 5, 4, 2, 1], [5, 1, 1, 0, 0], [1, 0, 0, 0, 0]],
  "lengths": [5, 5, 3, 1],
  "oov_rate": 0.35714285714285715,
  "same_bag": [[0, 1]]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
