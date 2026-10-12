# Cắt tỉa

Cây mọc quá sâu thì học thuộc cả nhiễu. Một cách chữa là cắt tỉa bằng validation: thử thay từng nút chia bằng một lá, nếu lỗi trên validation không tăng thì giữ việc thay ấy.

Cây cho dưới dạng lồng nhau. Lá là `{"label": c}`. Nút chia là `{"feature": j, "threshold": t, "left": ..., "right": ...}`, điểm có $x_j<t$ đi sang trái. Các ngưỡng đều có dạng $k+0.5$ nên không điểm nào rơi đúng ngưỡng.

Cắt tỉa theo từng vòng:

1. Với mỗi nút chia, thử thay nó bằng một lá. Nhãn của lá là nhãn đa số của các điểm **train** đi tới nút ấy. Hòa, hoặc không có điểm train nào, thì nhãn là $0$.
2. Trong các nút mà việc thay không làm lỗi validation tăng lên, chọn nút cho lỗi validation nhỏ nhất. Hòa thì chọn nút gặp trước khi duyệt cây theo thứ tự gốc, cây con trái, cây con phải.
3. Thay nút ấy bằng lá thật sự, rồi sang vòng mới. Dừng khi không còn nút nào thay được.

## Dữ liệu vào

Một đối tượng JSON gồm `tree`, `train_X`, `train_y`, `valid_X`, `valid_y`.

## Kết quả

Một đối tượng JSON gồm `tree` (cây sau khi cắt tỉa, cùng dạng), `valid_errors_before`, `valid_errors_after` (số điểm validation bị đoán sai) và `pruned` (số lần thay).

## Giới hạn

- Cây sâu không quá $4$ tầng. Có không quá $60$ điểm train và $40$ điểm validation, tọa độ nguyên từ $0$ đến $9$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "tree": {
    "feature": 0,
    "threshold": 5.5,
    "left": {
      "feature": 1,
      "threshold": 3.5,
      "left": {"label": 0},
      "right": {"label": 1}
    },
    "right": {
      "feature": 1,
      "threshold": 7.5,
      "left": {"label": 1},
      "right": {"label": 0}
    }
  },
  "train_X": [[1, 1], [2, 5], [3, 2], [6, 2], [7, 4], [8, 8], [9, 1], [4, 6]],
  "train_y": [0, 1, 0, 1, 1, 0, 1, 1],
  "valid_X": [[2, 2], [3, 6], [6, 5], [7, 8], [9, 9], [1, 5]],
  "valid_y": [0, 1, 1, 1, 1, 0]
}
```

```output
{
  "tree": {
    "feature": 0,
    "threshold": 5.5,
    "left": {"label": 0},
    "right": {"label": 1}
  },
  "valid_errors_before": 3,
  "valid_errors_after": 1,
  "pruned": 2
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
