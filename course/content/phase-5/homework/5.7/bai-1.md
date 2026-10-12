# InfoNCE

CLIP học bằng cách ghép cặp: ảnh thứ $i$ đi với câu mô tả thứ $i$, và mọi câu khác trong batch là negative. Bài này tính loss ấy trên các vector cho sẵn.

Có hai bảng vector `a` và `b`, mỗi bảng $N$ hàng; hàng $i$ của `a` ghép với hàng $i$ của `b`.

1. Chuẩn hóa từng hàng về độ dài $1$: chia cho $\max(\lVert v\rVert, 10^{-12})$. Hàng toàn $0$ vẫn là hàng toàn $0$.
2. Ma trận điểm $S_{ij}=\dfrac{a_i\cdot b_j}{\tau}$ với $\tau$ là `temperature`.
3. Loss theo hàng: cross-entropy của mỗi hàng $S_{i\cdot}$ với đáp án là cột $i$, lấy trung bình. Loss theo cột: tương tự với mỗi cột $S_{\cdot j}$ và đáp án là hàng $j$.
4. Loss cuối là trung bình cộng hai loss trên.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `a`, `b` và `temperature`.

## Kết quả

Một đối tượng JSON gồm `similarity` (ma trận $S$) và `loss`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "a": [
    [0.0, 0.0, 0.0],
    [-0.8821181980482352, -0.4104847159477657, -1.4851507532066648],
    [-0.5892784016791289, -0.2716929192408032, -0.010106959976554775],
    [-0.47104944812554067, -0.3558338500967358, 1.2623480500983235]
  ],
  "b": [
    [-1.3931907823379561, -0.5073753688097151, -0.20623172431934741],
    [1.2782926762375186, 0.8102370279700551, -0.20118003061009954],
    [0.00568157068009179, -0.7472016740350412, 1.0909480568870638],
    [0.05599854939433933, 0.16638281980102984, -1.661624957471365]
  ],
  "temperature": 0.15
}
```

```output
{
  "similarity": [
    [0.0, 0.0, 0.0, 0.0],
    [
      4.373256044832961, -2.8563477634979457, -3.7440975319483,
      5.281190897443332
    ],
    [
      6.594004250208258, -6.535767955192501, 1.4654452649119574,
      -0.37755057074175935
    ],
    [
      1.842213936715466, -3.5858468618972834, 5.934524810726903,
      -6.2505396157507995
    ]
  ],
  "loss": 6.60862311560953
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
