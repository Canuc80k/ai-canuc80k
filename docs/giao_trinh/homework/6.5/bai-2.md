# Cross-attention

Trong mô hình encoder-decoder, mỗi vị trí của decoder nhìn sang **toàn bộ** câu nguồn đã mã hóa (cross-attention). Không có mask nhân quả giữa hai câu, nhưng các token đệm của câu nguồn phải bị chặn.

Với mỗi mẫu $b$: query $Q$ ($T\times d$) từ decoder, key $K$ ($S\times d$) và value $V$ ($S\times d_v$) từ encoder, `source_keep` ($S$ giá trị, `true` là token thật). $T$ và $S$ có thể khác nhau.

1. Điểm $s_{tj}=\dfrac{q_t\cdot k_j}{\sqrt d}$, chỉ trên các $j$ có `source_keep` là `true`.
2. Softmax theo $j$ trên các vị trí ấy, rồi đầu ra là tổng có trọng số của các $v_j$.
3. Nếu câu nguồn không có token thật nào, đầu ra của mọi vị trí là vector $0$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `Q`, `K`, `V` và `source_keep` (theo batch).

## Kết quả

Một đối tượng JSON gồm `attended` (shape $B\times T\times d_v$).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "Q": [
    [
      [1.6059824676376062, -0.4235745848936438],
      [0.797385312407288, 0.8808917847775957],
      [1.416217330237268, 0.051735607666017154]
    ],
    [
      [-1.8800316170539542, 0.9879048596104733],
      [0.360056003560088, -0.6800503749685238],
      [1.775857158205082, 0.008523683803885362]
    ]
  ],
  "K": [
    [
      [-0.8318325276973463, -0.06582565094778552],
      [0.023768481374670445, -0.35410752186769784],
      [-137.931578675288, -4.470827175818233],
      [-137.65576200159288, -13.214536595104063]
    ],
    [
      [-0.3252216023388079, 0.1074675250900078],
      [-0.1420661779187534, -1.3706566867808399],
      [-101.84451654236865, -22.946161515129727],
      [-78.07394556166825, 72.54357088078191]
    ]
  ],
  "V": [
    [
      [-1.3902072063005728, 0.8999383453538466, 0.7904492447873388],
      [-0.838164502658711, 0.7932508447198757, 0.70383846310903],
      [85.32519369893804, 23.01845409140968, 5.341431927148149],
      [-64.08413853678067, -7.930626003015762, 85.39101450234097]
    ],
    [
      [0.21381822526912936, -1.0186270969411058, 1.2142698080737786],
      [-0.8278103185012196, 0.35986826705343694, 0.27680811759190044],
      [-82.05735440128876, -44.38497387850281, 28.00657640014026],
      [101.1613690450017, 18.472046829654754, 89.38459689691392]
    ]
  ],
  "source_keep": [[true, true, false, false], [false, false, false, false]]
}
```

```output
{
  "attended": [
    [
      [-0.9804250522764927, 0.820744048374973, 0.7261579273879663],
      [-1.0727054979503712, 0.8385781217924563, 0.7406359405574374],
      [-1.0038968228021128, 0.8252801911702902, 0.7298404475611098]
    ],
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
