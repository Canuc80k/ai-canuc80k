# Bàn cờ

Robot dọn nhà cần bản đồ sàn nhà lát gạch hai màu xen kẽ như bàn cờ. Sàn là một lưới `rows` hàng, `cols` cột. Ô ở hàng $r$, cột $c$ (đánh số từ $0$) có giá trị $(r+c) \bmod 2$, nên ô góc trên trái là $0$ và hai ô kề nhau luôn khác màu.

Hãy dựng lưới này bằng NumPy mà không dùng vòng lặp Python.

Gợi ý: `np.arange(rows)[:, None]` là một cột chỉ số hàng, shape $(\text{rows}, 1)$. Cộng nó với hàng chỉ số cột `np.arange(cols)`, broadcasting cho ngay cả lưới.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `rows` và `cols`.

## Kết quả

Lưới số nguyên `rows` × `cols`, dạng list các hàng. `.tolist()` đổi mảng NumPy thành list.

## Giới hạn

- $1\le\text{rows},\text{cols}\le30$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"rows": 3, "cols": 5}
```

```output
[[0, 1, 0, 1, 0], [1, 0, 1, 0, 1], [0, 1, 0, 1, 0]]
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
