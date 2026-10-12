# Mã vị trí

Attention không tự biết thứ tự của các token. Transformer gốc cộng thêm vào mỗi vị trí $p$ một vector mã vị trí gồm các cặp sin và cos ở nhiều tần số:

$$
\text{PE}[p,2i]=\sin\!\left(\frac{p}{10000^{2i/D}}\right),\qquad \text{PE}[p,2i+1]=\cos\!\left(\frac{p}{10000^{2i/D}}\right),
$$

với $D$ là độ rộng (chẵn) và $i=0,1,\dots,D/2-1$.

Hãy tính mã vị trí cho $L$ vị trí liên tiếp bắt đầu từ `offset`, tức các vị trí $p=\text{offset},\text{offset}+1,\dots,\text{offset}+L-1$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `length` ($L$), `width` ($D$) và `offset`.

## Kết quả

Một đối tượng JSON `{"positions": [...]}`, $L$ hàng, mỗi hàng $D$ số.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"length": 3, "width": 4, "offset": 0}
```

```output
{
  "positions": [
    [0.0, 1.0, 0.0, 1.0],
    [
      0.8414709848078965, 0.5403023058681398, 0.009999833334166664,
      0.9999500004166653
    ],
    [
      0.9092974268256817, -0.4161468365471424, 0.01999866669333308,
      0.9998000066665778
    ]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
