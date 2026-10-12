# Ma trận

Cho $x=(x_0, x_1, x_2, x_3)^\top$ là một vector cột trong $\mathbb{R}^4$. Phép biến đổi $f$ đưa $x$ thành một vector trong $\mathbb{R}^3$:

$$
f(x)=\begin{pmatrix} x_2-x_3 \\ x_3 \\ x_0+2x_1 \end{pmatrix}.
$$

Hãy tìm ma trận $A$ cỡ $3\times4$ sao cho $Ax=f(x)$ với mọi $x$.

Gợi ý: cột thứ $j$ của $A$ chính là $f(e_j)$, với $e_j$ là vector có số $1$ ở vị trí $j$, các vị trí khác bằng $0$. Có thể tính tay, hoặc viết code thử bốn vector ấy.

## Dữ liệu vào

Một đối tượng JSON có trường `mapping` ghi lại công thức của $f$. Bài chỉ có một test.

## Kết quả

Một đối tượng JSON có trường `A`, là ma trận $3\times4$ dạng list ba hàng.

## Chấm điểm

Một test, 100 điểm.

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Đề thi [USA-NA-AIO 2026, Vòng 1, câu 3.1](https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=7).
:::
