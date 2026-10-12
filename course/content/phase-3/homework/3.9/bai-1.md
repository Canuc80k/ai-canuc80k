# Mask attention

Attention cho mỗi query một trung bình có trọng số của các value. Mask quyết định query được nhìn những key nào: không nhìn PAD, và với mô hình sinh văn bản thì không nhìn tương lai.

Query $i$ được nhìn key $j$ khi key $j$ hợp lệ (`valid_keys[j]` đúng) và, nếu `causal` bật, $j\le i$. Trên các key được nhìn:

$$
\text{out}_i=\sum_j\operatorname{softmax}_j\!\left(\frac{q_i\cdot k_j}{\sqrt d}\right)v_j,\qquad d=2.
$$

Dùng `F.scaled_dot_product_attention` được, nhưng cẩn thận: ở hàm này, giá trị `True` trong mask boolean nghĩa là **được nhìn**, ngược với `src_mask` của `nn.Transformer`. Mỗi query luôn có ít nhất một key được nhìn.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `Q`, `K` (mỗi hàng hai số), `V` (mỗi hàng ba số), `valid_keys` và `causal`.

## Kết quả

Một đối tượng JSON `{"attended": [...]}`, mỗi query một vector ba số.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "Q": [[-0.461, 1.108], [-1.224, 1.406], [0.269, 0.308], [0.847, 2.397]],
  "K": [[0.139, 1.767], [1.353, -0.054], [-0.111, 1.754], [-0.321, -1.905]],
  "V": [
    [-0.189, 0.889, -1.256],
    [1.628, 1.154, 0.85],
    [-0.722, 1.193, -0.001],
    [0.672, 2.275, 0.032]
  ],
  "valid_keys": [true, false, true, true],
  "causal": false
}
```

```output
{
  "attended": [
    [-0.43023030911622717, 1.0839852773005516, -0.5866231239418623],
    [-0.46279672963705826, 1.0772234103071219, -0.554691571119089],
    [-0.25344039559888104, 1.2529185070081528, -0.5264283889022013],
    [-0.4317671160699338, 1.0289955325295896, -0.6816760035759621]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
