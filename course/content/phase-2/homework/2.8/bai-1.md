# Lề và khoảng cách

Một bộ phân loại tuyến tính cho mỗi điểm $x$ một điểm số $s=w\cdot x+b$. Dấu của $s$ cho biết điểm nằm bên nào của đường biên, còn độ lớn chưa phải khoảng cách thật. Muốn ra khoảng cách hình học, phải chia cho độ dài của $w$:

$$
d=\frac{|w\cdot x+b|}{\lVert w\rVert}.
$$

SVM dùng nhãn $y\in\{-1,1\}$ và hinge loss $\max(0,\,1-y\,s)$. Điểm nằm đúng phía và cách biên đủ xa thì loss bằng $0$. Hai đường $s=1$ và $s=-1$ cách nhau một khoảng $\frac{2}{\lVert w\rVert}$, gọi là bề rộng lề.

Hãy tính điểm số, khoảng cách tới biên và hinge loss của từng điểm, cùng bề rộng lề.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (mỗi hàng một điểm), `w`, `b` và `y` (nhãn $-1$ hoặc $1$).

## Kết quả

Một đối tượng JSON gồm `scores`, `distances`, `hinge` (mỗi trường một list theo thứ tự điểm) và `width`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [-2.0293021486634464, 0.018851207453313517],
    [0.7696875714199833, -0.007219495096140607],
    [-0.8833190069705763, 0.9206604133795265],
    [0.42166265837930256, 0.2518202207969097],
    [-1.205839480798117, 1.0915953995829177],
    [0.22657041090575394, 0.2491333225312491],
    [1.0104316642080668, 0.9448556850613351],
    [0.1742191007047443, 1.5011554491020194]
  ],
  "w": [3.0, 4.0],
  "b": -0.0,
  "y": [-1, 1, -1, 1, 1, 1, 1, 1]
}
```

```output
{
  "scores": [
    -6.012501616177085, 2.2801847338753873, 1.0326846326063772,
    2.272268858325546, 0.74886315593732, 1.6762445228422582,
    6.810717732869541, 6.52727909852231
  ],
  "distances": [
    1.202500323235417, 0.45603694677507745, 0.20653692652127545,
    0.45445377166510925, 0.149772631187464, 0.33524890456845163,
    1.3621435465739082, 1.3054558197044621
  ],
  "hinge": [0, 0, 2.032684632606377, 0, 0.25113684406268, 0, 0, 0],
  "width": 0.4
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
