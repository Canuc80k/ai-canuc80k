# Vòng Lloyd

K-Means lặp hai bước. Bước gán: mỗi điểm về tâm gần nhất. Bước cập nhật: mỗi tâm dời về trung bình các điểm của nó. Kết quả phụ thuộc nhiều vào các tâm ban đầu, nên bài này cho sẵn chúng.

Hãy chạy đúng `steps` vòng gán rồi cập nhật, theo các quy ước:

- Khoảng cách là khoảng cách Euclid. Điểm cách đều hai tâm thì về tâm có số thứ tự nhỏ hơn.
- Tâm không có điểm nào thì giữ nguyên chỗ cũ.

Sau vòng cuối, gán lại các điểm theo tâm cuối cùng và tính inertia, tức tổng bình phương khoảng cách từ mỗi điểm tới tâm của nó.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (các điểm hai chiều), `centers` (các tâm ban đầu) và `steps`.

## Kết quả

Một đối tượng JSON gồm `centers` (các tâm sau cùng), `assignment` (số thứ tự tâm của từng điểm) và `inertia`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[0, 0], [1, 0], [5, 0], [6, 0]],
  "centers": [[0, 0], [6, 0], [100, 100]],
  "steps": 1
}
```

```output
{
  "centers": [[0.5, 0.0], [5.5, 0.0], [100, 100]],
  "assignment": [0, 0, 1, 1],
  "inertia": 1.0
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
