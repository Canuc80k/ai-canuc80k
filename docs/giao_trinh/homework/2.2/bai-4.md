# Điểm mốc

Ridge thường kéo trọng số về $0$. Nhưng nếu đã giải nhiều bài cùng loại và biết lời giải thường gần một vector $w_0$ nào đó, ta có thể kéo trọng số về $w_0$ thay vì về $0$. Mô hình không có hệ số tự do, và ta tìm $w$ cực tiểu

$$
J(w)=\sum_{i=1}^{n}\left(y_i-w^\top x_i\right)^2+\lambda\lVert w-w_0\rVert^2 .
$$

Với mỗi $\lambda$ trong danh sách, hãy tìm $w$ và tính MSE trên chính dữ liệu train.

Gợi ý: cho đạo hàm của $J$ theo $w$ bằng $0$ để được một hệ phương trình tuyến tính $d$ ẩn. Khi $\lambda=0$ ta được hồi quy tuyến tính thường. Khi $\lambda$ rất lớn, $w$ tiến về $w_0$.

## Dữ liệu vào

Một đối tượng JSON gồm `X` (ma trận $n\times d$), `y`, `w0` và `lambdas`.

## Kết quả

Một đối tượng JSON gồm `weights` (với mỗi $\lambda$, một list $d$ số) và `train_mse` (với mỗi $\lambda$, một số).

## Giới hạn

- $1\le d\le4$, $d<n\le30$, các số trong `X`, `y`, `w0` là số nguyên nhỏ.
- Các cột của `X` độc lập tuyến tính, nên hệ phương trình luôn có nghiệm duy nhất.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[1], [2], [3]],
  "y": [2, 4, 7],
  "w0": [1],
  "lambdas": [0, 14, 1000]
}
```

```output
{
  "weights": [[2.2142857142857144], [1.6071428571428572], [1.0167652859960552]],
  "train_mse": [0.11904761904761904, 1.8392857142857142, 6.811305107845845]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
