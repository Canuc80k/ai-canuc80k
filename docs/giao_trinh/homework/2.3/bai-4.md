# Quy ước C

`LogisticRegression(C=...)` của scikit-learn không dùng $\lambda$ như sách vở mà dùng $C$. Theo tài liệu thư viện, với phạt L2, nó cực tiểu

$$
J(w,b)=C\sum_{i=1}^{n}\Big[\ln\!\left(1+e^{z_i}\right)-y_iz_i\Big]+\frac12\lVert w\rVert^2,\qquad z_i=w^\top x_i+b .
$$

Hai điểm cần để ý. Hệ số tự do $b$ không bị phạt. Và $C$ đứng trước phần loss chứ không đứng trước phần phạt, nên $C$ càng lớn thì phạt càng nhẹ.

Hãy tính $J$, $\frac{\partial J}{\partial w}$ và $\frac{\partial J}{\partial b}$ tại $(w, b)$ cho sẵn.

Sách vở hay viết loss dạng trung bình cộng phạt $\frac\lambda2\lVert w\rVert^2$. Chia $J$ cho $Cn$ thì được đúng dạng ấy, với $\lambda=\frac1{Cn}$. Hãy tính thêm $\lambda$ và gradient của dạng trung bình, tức hai gradient trên chia cho $Cn$.

## Dữ liệu vào

Một đối tượng JSON gồm `X` (ma trận $n\times d$), `y`, `w`, `b` và `C`.

## Kết quả

Một đối tượng JSON gồm `loss`, `grad_w`, `grad_b`, `lambda`, `mean_grad_w`, `mean_grad_b`.

## Giới hạn

- $n\le40$, $d\le5$, $C>0$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[1, 0], [0, 1], [1, 1]],
  "y": [1, 0, 1],
  "w": [0.5, -1],
  "b": 0.2,
  "C": 2
}
```

```output
{
  "loss": 3.882283918603526,
  "grad_w": [-1.3125094892869855, -1.5288339958785429],
  "grad_b": -1.1924584515422105,
  "lambda": 0.16666666666666666,
  "mean_grad_w": [-0.21875158154783092, -0.2548056659797571],
  "mean_grad_b": -0.19874307525703508
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
