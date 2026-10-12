# Mạng ngưỡng

Không cần huấn luyện, một mạng nơ-ron có thể được đặt trọng số bằng tay để làm một việc cụ thể. Ở đây mạng nhận một điểm trên mặt phẳng và cho biết điểm ấy có nằm trong một tam giác hay không.

Hàm ngưỡng là $\Theta(t)=1$ nếu $t\ge0$, ngược lại $\Theta(t)=0$. Mạng có ba nơ-ron ẩn, mỗi nơ-ron ứng với một cạnh của tam giác:

- Nơ-ron $j$ ứng với cạnh nối đỉnh $j$ và đỉnh $j+1$ (đỉnh $2$ nối về đỉnh $0$). Nó cho $1$ khi điểm nằm cùng phía với đỉnh còn lại so với đường thẳng chứa cạnh ấy, hoặc nằm trên đường thẳng ấy. Ngược lại nó cho $0$.
- Nơ-ron đầu ra tính $\Theta(h_0+h_1+h_2-3)$, tức chỉ bật khi cả ba nơ-ron ẩn cùng bật.

Điểm nằm trên cạnh được coi là ở trong tam giác. Ba đỉnh có thể cho theo chiều kim đồng hồ hoặc ngược chiều.

Hãy tính đầu ra của ba nơ-ron ẩn và của nơ-ron đầu ra cho từng điểm truy vấn.

## Dữ liệu vào

Một đối tượng JSON gồm `vertices` (ba đỉnh, tọa độ nguyên, không thẳng hàng) và `queries` (các điểm, tọa độ là số nguyên hoặc nửa nguyên).

## Kết quả

Một đối tượng JSON gồm `hidden` (mỗi điểm một list ba số $0$/$1$, theo thứ tự cạnh $01$, $12$, $20$) và `predictions` (mỗi điểm một số $0$/$1$).

## Giới hạn

- Không quá $30$ điểm truy vấn, mọi tọa độ có trị tuyệt đối không quá $10$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "vertices": [[0, 0], [3, 1], [1, 5]],
  "queries": [
    [1, 1],
    [2, 3],
    [0, 0],
    [1.5, 0.5],
    [2, 3.0],
    [3, 4],
    [-1, 0],
    [1, 4]
  ]
}
```

```output
{
  "hidden": [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
  ],
  "predictions": [1, 1, 1, 1, 1, 0, 0, 1]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 7.4](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=19).
:::
