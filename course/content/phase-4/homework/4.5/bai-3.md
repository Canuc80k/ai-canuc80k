# Ghép prompt

Một lớp có thể mô tả bằng nhiều câu ("a photo of a cat", "a drawing of a cat", …). Ghép nhiều câu mô tả giúp bớt phụ thuộc vào một cách diễn đạt. Quy tắc ghép được cố định trước:

1. Chuẩn hóa vector của từng câu về độ dài $1$.
2. Lấy trung bình các câu của cùng một lớp.
3. Chuẩn hóa vector trung bình ấy về độ dài $1$ lần nữa.

Rồi chấm ảnh bằng cosine với từng vector lớp và chọn lớp có cosine lớn nhất (hòa thì chỉ số nhỏ).

## Dữ liệu vào

Mỗi tệp `input.json` gồm `templates` (với mỗi lớp, một list vector câu mô tả) và `image` (một vector).

## Kết quả

Một đối tượng JSON gồm `class_vectors`, `scores` và `prediction`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "templates": [
    [
      [-0.657457478775608, 0.9150450272361619, -0.7486213113576718],
      [1.032906162072017, 0.008169067637476629, -0.46746977754893176]
    ],
    [
      [-1.0838909566537156, 1.2880704605327433, 0.12389214560047149],
      [1.226172991487737, -0.6337686196406811, 0.41698389345600334]
    ],
    [
      [0.15564999925861198, 0.3416136308163888, 0.6625462545375214],
      [1.468558694843503, -0.28108900326501357, 0.23261570141539603]
    ]
  ],
  "image": [0.421846846665839, 0.5788572928473035, -0.8991387151673746]
}
```

```output
{
  "class_vectors": [
    [0.3380591489441669, 0.543767870917548, -0.7681357395492949],
    [0.3939324189618273, 0.6119505565354054, 0.6858088404554807],
    [0.7434300233008997, 0.16631817629926704, 0.647804032626619]
  ],
  "scores": [0.9986750662353246, -0.08370711567266206, -0.15012531559695763],
  "prediction": 0
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
