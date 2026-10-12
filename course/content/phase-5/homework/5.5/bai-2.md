# NMS theo lớp

Một detector thường bắn ra nhiều box gần trùng nhau quanh cùng một vật. NMS (non-maximum suppression) giữ box điểm cao nhất và bỏ những box chồng lên nó quá nhiều. Nhưng một con chó và một con mèo đứng sát nhau là hai vật khác nhau, nên NMS chỉ được so các box **cùng lớp**.

Với mỗi lớp, làm riêng:

1. Xếp các box của lớp theo điểm giảm dần.
2. Lần lượt xét từng box: giữ nó nếu IoU của nó với mọi box cùng lớp đã giữ đều **không vượt quá** `threshold`; ngược lại bỏ. IoU bằng đúng ngưỡng thì vẫn giữ.

Gộp các box được giữ của mọi lớp, xếp theo điểm giảm dần, rồi báo mã của chúng.

Box viết dạng $[x_1,y_1,x_2,y_2]$ theo tọa độ liên tục, như bài A. Các điểm đôi một khác nhau. Mã là chuỗi: `"002"` và `"2"` là hai mã khác nhau.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `boxes`, `scores`, `labels` (số nguyên), `ids` (chuỗi) và `threshold`.

## Kết quả

Một đối tượng JSON gồm `kept_ids`: mã của các box được giữ, theo điểm giảm dần.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "boxes": [[0, 0, 3, 2], [1, 0, 4, 2], [0.01, 0, 3.01, 2], [8, 0, 10, 2]],
  "scores": [0.99, 0.9, 0.8, 0.7],
  "labels": [0, 0, 1, 0],
  "ids": ["002", "2", "dup", "far"],
  "threshold": 0.5
}
```

```output
{"kept_ids": ["002", "2", "dup", "far"]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
