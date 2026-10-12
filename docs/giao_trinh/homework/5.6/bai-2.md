# RLE theo cột

Mask nhị phân thường được lưu gọn bằng RLE (run-length encoding): thay vì ghi từng điểm, ghi độ dài các đoạn liên tiếp cùng giá trị. Bộ COCO dùng cách ghi sau.

1. Trải mask $H\times W$ thành một dãy **theo cột**: hết cột $0$ từ trên xuống, rồi tới cột $1$, và cứ thế.
2. Ghi độ dài các đoạn xen kẽ, **luôn bắt đầu bằng đoạn nền** (số $0$). Nếu dãy mở đầu bằng $1$ thì số đầu tiên là $0$.

Ví dụ mask $2\times3$ gồm hai hàng $[0,1,0]$ và $[1,1,0]$: trải theo cột được $0,1,1,1,0,0$, nên RLE là $[1,3,2]$.

Sau đó giải mã ngược RLE vừa tìm để kiểm lại.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `mask`.

## Kết quả

Một đối tượng JSON gồm `counts` (RLE) và `decoded` (mask giải mã từ `counts`, cùng shape với `mask`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"mask": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}
```

```output
{
  "counts": [15],
  "decoded": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
