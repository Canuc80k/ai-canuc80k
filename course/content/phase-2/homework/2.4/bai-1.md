# Bỏ phiếu

Mỗi quả bóng mới được đoán thuộc đội nào dựa vào $k$ cầu thủ gần nó nhất. Khoảng cách là khoảng cách Euclid. Khi hai cầu thủ cách đều, người có chỉ số nhỏ hơn được coi là gần hơn.

Có hai cách bỏ phiếu, chọn theo trường `weighted`:

- **Đều nhau** (`false`): mỗi hàng xóm một phiếu, đội nhiều phiếu nhất thắng.
- **Theo khoảng cách** (`true`): mỗi hàng xóm có phiếu nặng $1/d$. Nếu có hàng xóm ở đúng vị trí quả bóng ($d=0$), chỉ những hàng xóm ấy được bỏ phiếu, mỗi người một phiếu.

Hòa phiếu thì đội có số nhỏ hơn thắng.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (vị trí cầu thủ), `y` (đội $0$, $1$ hoặc $2$), `queries` (vị trí các quả bóng), `k` và `weighted`.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, mỗi quả bóng một đội, theo thứ tự `queries`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "X": [[0, 0], [0, 0], [1, 0], [-1, 0], [3, 0], [0, 4]],
  "y": [2, 1, 0, 0, 2, 1],
  "queries": [[0, 0], [1, 1], [0.1, 0.3]],
  "k": 1,
  "weighted": false
}
```

```output
{"predictions": [2, 0, 2]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
