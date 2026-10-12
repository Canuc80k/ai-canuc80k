# Phá đối xứng

Vì sao không khởi tạo mọi trọng số bằng nhau? Bài này để con số tự trả lời.

Mạng có $d$ đầu vào, $h$ nơ-ron ẩn sigmoid và một đầu ra tuyến tính:

$$
\hat y=\sum_{j=1}^{h}v_j\,\sigma\!\left(\sum_{i=1}^{d}x_iW_{ij}+c_j\right)+b,\qquad \sigma(z)=\frac{1}{1+e^{-z}}.
$$

Loss là MSE trên cả tập: $L=\frac1n\sum_k(\hat y_k-y_k)^2$. Chạy gradient descent đúng `steps` bước. Mỗi bước tính gradient của mọi tham số tại giá trị hiện tại, rồi cập nhật cùng lúc: tham số trừ đi `learning_rate` nhân gradient.

Hãy báo:

- `losses`: loss trước mỗi bước, và thêm loss sau bước cuối ($\text{steps}+1$ số).
- `W`, `c`, `v`, `b`: tham số sau cùng.
- `identical`: các cặp nơ-ron ẩn $[j,k]$ với $j<k$ (đánh số từ $0$) mà sau cùng có cột $W$, $c_j$, $v_j$ trùng nhau, sai khác mỗi số không quá $10^{-9}$.

## Dữ liệu vào

Một đối tượng JSON gồm `X` ($n$ hàng, mỗi hàng $d$ số), `y`, `W` (shape $d\times h$), `c`, `v`, `b`, `learning_rate` và `steps`.

## Kết quả

Một đối tượng JSON gồm `losses`, `W`, `c`, `v`, `b` và `identical`.

## Giới hạn

- $n\le12$, $d\le3$, $h\le4$, không quá $30$ bước. Các nơ-ron khởi tạo khác nhau thì sau cùng vẫn khác nhau rõ rệt.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [[-1.0], [0.0], [1.0], [2.0]],
  "y": [0.0, 1.0, 0.0, 1.0],
  "W": [[0.5, 0.5, -0.3]],
  "c": [0.1, 0.1, 0.2],
  "v": [0.4, 0.4, -0.2],
  "b": 0.0,
  "learning_rate": 0.5,
  "steps": 5
}
```

```output
{
  "losses": [
    0.23071106890771959, 0.22864202536268052, 0.226999351867374,
    0.22524869155413668, 0.22386386007247627, 0.22238601837370414
  ],
  "W": [[0.5378604717500081, 0.5378604717500081, -0.32585236926928524]],
  "c": [0.10252459271818079, 0.10252459271818079, 0.189305831857958],
  "v": [0.5185568302480216, 0.5185568302480216, -0.1777600008499858],
  "b": 0.11269061385065599,
  "identical": [[0, 1]]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
