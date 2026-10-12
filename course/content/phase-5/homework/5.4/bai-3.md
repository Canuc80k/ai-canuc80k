# Đảo patch

Self-attention không biết thứ tự: đảo các token thì đầu ra đảo theo, và trung bình của đầu ra không đổi. Chỉ khi cộng mã vị trí cố định theo **chỗ đứng**, việc đảo nội dung mới làm kết quả thay đổi.

Có bốn token, mỗi token ba số. Self-attention dùng $Q=K=V$ bằng chính các token, chia điểm số cho $\sqrt3$, không mask. Hãy tính trung bình (theo token) của đầu ra attention trong bốn trường hợp:

- `plain_mean`: token $X$.
- `shuffled_plain_mean`: các hàng của $X$ đảo theo `permutation`, tức hàng $i$ mới là hàng `permutation[i]` cũ.
- `position_mean`: $X$ cộng bảng mã vị trí `positions`.
- `shuffled_position_mean`: $X$ đã đảo, cộng `positions` **không đảo**.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X`, `positions` và `permutation`.

## Kết quả

Một đối tượng JSON gồm bốn trường trên, mỗi trường ba số.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [-0.386, -0.017, -1.111],
    [-1.124, 2.215, 0.752],
    [-1.219, -0.774, -0.884],
    [1.255, -0.103, -0.187]
  ],
  "positions": [
    [0.149, -0.371, -0.862],
    [1.167, -0.325, 0.917],
    [-0.246, 1.473, 2.1],
    [-1.248, -1.574, 1.344]
  ],
  "permutation": [3, 0, 2, 1]
}
```

```output
{
  "plain_mean": [-0.5169297032082556, 0.4485999412836785, -0.28456053138491944],
  "shuffled_plain_mean": [-0.5169297032082556, 0.4485999412836785, -0.28456053138491944],
  "position_mean": [-0.3451426960482463, 0.23893750543756825, 0.5613646122367377],
  "shuffled_position_mean": [-0.6273058396944269, 0.1500771601272695, 0.6814645795968843]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
