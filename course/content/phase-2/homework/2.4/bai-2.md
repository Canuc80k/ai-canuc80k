# Cosine

Hai món đồ chơi giống nhau khi vector đặc trưng của chúng cùng hướng, dù dài ngắn khác nhau. Độ giống ấy đo bằng cosine:

$$
\cos(u,v)=\frac{u\cdot v}{\lVert u\rVert\,\lVert v\rVert}.
$$

Nếu một trong hai vector bằng $0$ thì ta quy ước cosine bằng $0$.

Với mỗi vector trong `queries`, tìm $k$ vector trong `vectors` có cosine lớn nhất, xếp từ giống nhất. Hòa thì vector có chỉ số nhỏ hơn đứng trước. Đây là chuẩn hóa độ dài của từng vector, không phải chuẩn hóa từng cột như `StandardScaler`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `vectors` (ma trận $n\times d$), `queries` (ma trận $m\times d$) và `k`.

## Kết quả

Một đối tượng JSON `{"neighbors": [...]}`, với mỗi truy vấn một list $k$ chỉ số.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "vectors": [[1, 0], [2, 0], [0, 0], [-1, 0], [0, 1], [1, 1]],
  "queries": [[1, 0], [0, 0], [1, 2]],
  "k": 1
}
```

```output
{"neighbors": [[0], [0], [5]]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
