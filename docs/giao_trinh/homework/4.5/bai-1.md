# Chấm kiểu CLIP

CLIP đưa ảnh và câu mô tả về cùng một không gian vector. Phân loại zero-shot là chọn câu mô tả có hướng gần ảnh nhất, không cần học thêm gì.

Cho các vector ảnh và các vector văn bản (mỗi lớp một vector), đã ở cùng không gian. Hãy:

1. Chuẩn hóa mọi vector về độ dài $1$.
2. Tính logit $z_{ik}=\text{scale}\cdot u_i\cdot v_k$, tức cosine nhân hệ số `scale`.
3. Softmax theo từng ảnh trên các lớp, và lấy lớp có logit lớn nhất (hòa thì chỉ số nhỏ).

## Dữ liệu vào

Mỗi tệp `input.json` gồm `image_vectors`, `text_vectors` (các vector khác $0$) và `scale`.

## Kết quả

Một đối tượng JSON gồm `probabilities` (mỗi ảnh một list xác suất) và `predictions`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "image_vectors": [
    [-0.657457478775608, 0.9150450272361619, -0.7486213113576718],
    [1.032906162072017, 0.008169067637476629, -0.46746977754893176],
    [-1.0838909566537156, 1.2880704605327433, 0.12389214560047149],
    [1.226172991487737, -0.6337686196406811, 0.41698389345600334],
    [0.15564999925861198, 0.3416136308163888, 0.6625462545375214]
  ],
  "text_vectors": [
    [1.468558694843503, -0.28108900326501357, 0.23261570141539603],
    [0.421846846665839, 0.5788572928473035, -0.8991387151673746],
    [-0.12926922416924944, -0.01807321410720569, -0.8379489683585436],
    [1.1682664313233302, 0.13049036240705364, 1.2496604665351856]
  ],
  "scale": 5.0
}
```

```output
{
  "probabilities": [
    [
      0.0008160100509339121, 0.48501032341569034, 0.5133584255871557,
      0.0008152409462200004
    ],
    [
      0.6258763408735525, 0.28264754390509633, 0.039802094467860996,
      0.051674020753490146
    ],
    [
      0.008121244473634116, 0.5548591568277923, 0.3680296954611679,
      0.06898990323740561
    ],
    [
      0.7233591523951757, 0.003156794687697346, 0.0008161409584078024,
      0.2726679119587192
    ],
    [
      0.05764619160076294, 0.0024901188062501642,
      0.00018423179289368428, 0.9396794578000931
    ]
  ],
  "predictions": [2, 0, 1, 0, 3]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
