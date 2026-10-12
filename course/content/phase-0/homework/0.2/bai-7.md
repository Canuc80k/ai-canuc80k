# Tích ngoài

Tích ngoài của $u\in\mathbb{R}^3$ và $v\in\mathbb{R}^4$ là ma trận $uv^\top$ cỡ $3\times4$, phần tử ở hàng $r$, cột $c$ bằng $u_r v_c$. Ma trận kiểu này có mọi hàng tỉ lệ với nhau.

Cho ma trận $A$ cỡ $3\times4$. Hãy viết $A$ thành tổng của một số tích ngoài:

$$
A=\sum_{i=1}^{I} u_i v_i^\top.
$$

Có rất nhiều cách viết, cách nào đúng cũng được, và không cần $I$ nhỏ nhất. Hệ thống cộng các tích ngoài của bài làm rồi so với $A$.

Gợi ý: với $e_0=(1,0,0)$ và một vector $v$ bất kỳ, tích ngoài $e_0v^\top$ trông như thế nào?

## Dữ liệu vào

Một đối tượng JSON có trường `A`, ma trận $3\times4$ gồm các số nguyên.

## Kết quả

Một đối tượng JSON gồm `u` (danh sách $I$ vector, mỗi vector $3$ số) và `v` (danh sách $I$ vector, mỗi vector $4$ số), với $1\le I\le12$ và mọi số có trị tuyệt đối không quá $10^6$.

## Giới hạn

- Các phần tử của $A$ nằm trong $[-9, 9]$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Tổng các tích ngoài được chấm với sai số khoảng $10^{-7}$ trên từng phần tử. Test 1 là ma trận của đề gốc. Ví dụ dưới đây chỉ là một trong nhiều đáp án đúng.

## Ví dụ

```input
{"A": [[0, 0, 1, -1], [0, 0, 0, 1], [1, 2, 0, 0]]}
```

```output
{
  "u": [[0, 0, 1], [0, 0, 2], [1, 0, 0], [-1, 1, 0]],
  "v": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [USA-NA-AIO 2026, Vòng 1, câu 3.2](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=7).
:::
