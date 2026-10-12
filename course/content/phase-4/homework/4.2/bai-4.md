# Ma trận độ giống

Mỗi từ được biểu diễn bằng một vector $m$ chiều; xếp $N$ vector thành ma trận $W$ cỡ $N\times m$. Ma trận độ giống $S=WW^\top$ cỡ $N\times N$ có $S_{ij}$ là tích vô hướng của từ $i$ và từ $j$. Bài này hỏi: $S$ có khả nghịch không?

Các vector ở đây có tọa độ nguyên, nên mọi phép tính làm được chính xác, không cần số thực. Hãy tính:

- `S`: ma trận $WW^\top$.
- `rank_W`, `rank_S`: hạng của $W$ và của $S$.
- `invertible`: $S$ có khả nghịch không.
- `frobenius_sq`: bình phương chuẩn Frobenius của $S$, tức tổng bình phương mọi phần tử.

Trước khi viết code, hãy tự trả lời: khi số từ $N$ lớn hơn số chiều $m$, $S$ có thể khả nghịch không?

## Dữ liệu vào

Một đối tượng JSON gồm `W` (các hàng số nguyên).

## Kết quả

Một đối tượng JSON gồm `S`, `rank_W`, `rank_S`, `invertible` và `frobenius_sq`.

## Giới hạn

- $N\le7$, $m\le5$, mọi tọa độ có trị tuyệt đối không quá $6$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"W": [[1, 2], [2, 4], [0, 1]]}
```

```output
{
  "S": [[5, 10, 2], [10, 20, 4], [2, 4, 1]],
  "rank_W": 2,
  "rank_S": 2,
  "invertible": false,
  "frobenius_sq": 666
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 5.10](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=13).
:::
