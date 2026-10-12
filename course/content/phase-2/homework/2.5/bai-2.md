# Đi theo cây

Cho một cây quyết định đã dựng sẵn, lưu thành danh sách nút. Nút lá có dạng `{"label": c}`. Nút chia có dạng `{"feature": j, "threshold": t, "left": a, "right": b}`, trong đó `a`, `b` là chỉ số của hai nút con. Gốc là nút số $0$.

Mỗi truy vấn đi từ gốc xuống. Ở nút chia, nếu $x_j\le t$ thì sang con trái, ngược lại sang con phải. Tới lá thì đoán nhãn của lá ấy.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `nodes` và `queries`.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, mỗi truy vấn một nhãn.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "nodes": [
    {"feature": 1, "threshold": -2, "left": 1, "right": 2},
    {"label": 0},
    {"feature": 0, "threshold": 1, "left": 3, "right": 4},
    {"label": 1},
    {"label": 2}
  ],
  "queries": [[0, -2], [0, -1.9], [2, -1.9], [-1, -3], [1, 0]]
}
```

```output
{"predictions": [0, 1, 2, 0, 1]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
