# Log-prob ứng viên

Mô hình ngôn ngữ nhân quả cho logits ở mỗi vị trí, dùng để đoán token **kế tiếp**. Muốn chấm một đoạn hoàn thành, ta đọc log-xác suất của từng token đoạn ấy từ logits của vị trí ngay trước nó.

Cho một chuỗi token `token_ids` dài $L$, bảng logits cỡ $L\times V$ (hàng $j$ là logits sau khi đọc token $j$), và vị trí bắt đầu chấm $s\ge1$. Các token $0,\dots,s-1$ là prompt, không chấm. Với mỗi $j=s,\dots,L-1$:

$$
\log p(t_j)=\operatorname{log\_softmax}(\text{logits}[j-1])[t_j].
$$

Hãy tính các log-xác suất ấy, tổng, trung bình, và perplexity $\exp(-\text{trung bình})$. Dùng log tự nhiên và tính log-softmax ổn định số; logits có thể tới $\pm1000$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `token_ids`, `logits` và `score_start`.

## Kết quả

Một đối tượng JSON gồm `token_logprobs` ($L-s$ số), `sum_logprob`, `mean_logprob` và `perplexity`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "token_ids": [0, 2, 2, 2, 4, 1, 5],
  "logits": [
    [1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0],
    [
      -0.6337686196406811, 0.41698389345600334, 0.15564999925861198,
      0.3416136308163888, 0.6625462545375214, 1.468558694843503
    ],
    [
      -0.28108900326501357, 0.23261570141539603, 0.421846846665839,
      0.5788572928473035, -0.8991387151673746, -0.12926922416924944
    ],
    [
      -0.01807321410720569, -0.8379489683585436, 1.1682664313233302,
      0.13049036240705364, 1.2496604665351856, -0.5245428679109003
    ],
    [
      -1.4902944145503667, 0.776732944876131, 1.3387938515449835,
      -0.11086292836052984, 1.4847163512955959, 1.0199942311863623
    ],
    [
      -1.9996905736461963, -0.5143027451928587, 0.6061987263696238,
      0.29862413433214136, 0.37543679604299374, 0.9732608361677255
    ],
    [
      -1.5269305075175554, -0.19027588625747638, -0.2319686033691774,
      -0.5988907545266229, 1.0463100862982988, -0.6380953771512903
    ]
  ],
  "score_start": 2
}
```

```output
{
  "token_logprobs": [
    -2.2336902703842654, -1.466931732034817, -1.0379600960164388,
    -1.8832507956970157, -1.1082951639300629
  ],
  "sum_logprob": -7.7301280580626,
  "mean_logprob": -1.54602561161252,
  "perplexity": 4.692782131594854
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
