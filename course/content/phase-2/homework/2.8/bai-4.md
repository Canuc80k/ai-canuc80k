# Perceptron RBF

Perceptron thường giữ một vector trọng số $w$. Khi dùng kernel, ta không giữ $w$ nữa mà giữ số lần mỗi điểm train từng bị đoán sai, gọi là $\alpha_i$. Điểm số của một điểm $x$ là

$$
s(x)=\sum_j \alpha_j\,y_j\,K(x_j,x),
$$

với kernel RBF $K(a,b)=e^{-\gamma\lVert a-b\rVert^2}$ và nhãn $y_j\in\{-1,1\}$.

Ban đầu mọi $\alpha_i$ bằng $0$. Mỗi epoch, đi qua các điểm train theo đúng thứ tự cho sẵn. Với điểm $i$, tính $s(x_i)$ bằng các $\alpha$ hiện tại. Nếu $y_i\,s(x_i)\le0$ thì điểm ấy bị đoán sai, tăng $\alpha_i$ thêm $1$ ngay rồi mới sang điểm kế tiếp.

Sau đủ số epoch, tính điểm số cho các điểm trong `X_test` và đoán nhãn $1$ nếu điểm số dương, ngược lại đoán $-1$.

## Dữ liệu vào

Một đối tượng JSON gồm `X`, `y`, `gamma`, `epochs` và `X_test`. Mỗi điểm có hai tọa độ.

## Kết quả

Một đối tượng JSON gồm:

- `alphas`: các $\alpha_i$ sau khi học.
- `mistakes`: số điểm bị đoán sai trong từng epoch.
- `test_scores`: điểm số của các điểm test.
- `predictions`: nhãn đoán cho các điểm test.

## Giới hạn

- Từ $2$ đến $25$ điểm train, không quá $8$ điểm test, không quá $6$ epoch.
- Trừ lúc mọi $\alpha$ còn bằng $0$, không điểm số nào sát $0$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[0, 0], [1, 1], [0, 1], [1, 0]],
  "y": [-1, -1, 1, 1],
  "gamma": 1,
  "epochs": 3,
  "X_test": [[0.2, 0.9], [0.9, 0.8]]
}
```

```output
{
  "alphas": [1, 1, 1, 1],
  "mistakes": [3, 1, 0],
  "test_scores": [0.23633900388476894, -0.23633900388476894],
  "predictions": [1, -1]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
