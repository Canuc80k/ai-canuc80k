# Gộp token

Một sentence embedding thường được làm bằng cách gộp các vector token của câu. Nhưng không phải token nào cũng được tính: token đặc biệt (như `[CLS]`, `[SEP]`) và token đệm phải bị loại, dù vector của chúng rất lớn.

Với mỗi câu $b$, có các vector token $X_{b,t}$, trọng số $w_{b,t}\ge0$ và `content_mask` cho biết token nào là nội dung.

1. Trọng số hiệu dụng bằng $w_{b,t}$ nếu token là nội dung, bằng $0$ nếu không.
2. Nếu tổng trọng số hiệu dụng bằng $0$, câu không có embedding: trả `null` cho cả embedding và độ dài.
3. Ngược lại, vector gộp là $\sum_t w_{b,t}X_{b,t}\,/\,\sum_t w_{b,t}$ (chỉ tính trọng số hiệu dụng). Báo độ dài của nó **trước** khi chuẩn hóa. Nếu độ dài bằng $0$ thì embedding là chính vector $0$ ấy; ngược lại chia cho độ dài.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (shape $B\times L\times d$), `weights` và `content_mask` (shape $B\times L$).

## Kết quả

Một đối tượng JSON gồm `embeddings` và `norms` (mỗi câu một phần tử, có thể là `null`).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [
      [15.177466444623999, 129.06307697522675, -6.72860928612761],
      [-0.1267748335830371, 0.15100991795828228, 0.036727884583210385],
      [0.8021437385703065, 0.026854167519736252, 0.7097150894862867],
      [0.9344743848344612, -0.4325542545416357, -0.4753117119380259]
    ],
    [
      [57.784774601927836, -4.365950092543993, 225.68419161364451],
      [-1.9260428039059259, -0.6089000469259058, -0.03706794599769419],
      [-1.4086633831962332, 1.6638658473607888, 1.5344101341562277],
      [0.9174181571691442, -0.5758150548355324, 0.36626901816683016]
    ],
    [
      [-178.18636160154816, 136.4852724683157, -73.21318813901428],
      [1.3971155277998204, 1.0665161040287057, -0.024944937779107505],
      [-1.3971155277998204, -1.0665161040287057, 0.024944937779107505],
      [-1.3049312605716883, 1.221496031558595, -0.6506753050866266]
    ]
  ],
  "weights": [[2.0, 4.0, 4.0, 0.0], [2.0, 3.0, 4.0, 3.0], [1.0, 1.0, 1.0, 1.0]],
  "content_mask": [
    [false, true, true, false],
    [false, false, false, false],
    [false, true, true, false]
  ]
}
```

```output
{
  "embeddings": [
    [0.6606877206750057, 0.1739976720228651, 0.7302167800591064],
    null,
    [0.0, 0.0, 0.0]
  ],
  "norms": [0.5111105321416178, null, 0.0]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
