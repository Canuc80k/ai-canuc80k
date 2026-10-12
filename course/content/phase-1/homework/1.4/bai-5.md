# Chọn feature

Ta có $n$ mẫu, mỗi mẫu $p$ feature nguyên và nhãn $0$ hoặc $1$. Ta muốn chọn ra $m$ feature tốt nhất rồi đánh giá bằng K-fold. Có hai cách làm:

- **Chọn ngoài**: chọn $m$ feature một lần trên toàn bộ dữ liệu, rồi mới chạy K-fold trên các feature đã chọn.
- **Chọn trong**: ở mỗi fold, chọn $m$ feature chỉ từ các hàng train của fold ấy, rồi học và chấm.

Hãy tính điểm CV của cả hai cách và xem chúng chênh nhau thế nào.

Cách chọn feature như sau. Trên một tập hàng, điểm của feature $j$ là $s_j=\left|\bar x_j^{(1)}-\bar x_j^{(0)}\right|$, với $\bar x_j^{(c)}$ là trung bình feature $j$ trên các hàng nhãn $c$. Lấy $m$ feature có điểm cao nhất, hòa thì ưu tiên chỉ số nhỏ.

Mô hình là **tâm gần nhất**. Trên các hàng train, tâm của mỗi lớp là trung bình các feature đã chọn trên các hàng của lớp ấy. Một hàng được đoán thuộc lớp có tâm gần nó hơn theo khoảng cách Euclid, cách đều thì đoán $0$.

K-fold chia các hàng thành $K$ phần liền nhau, bằng nhau, theo thứ tự cho sẵn. Điểm CV là trung bình accuracy của $K$ fold.

## Dữ liệu vào

Một đối tượng JSON gồm `X` (ma trận $n\times p$), `y`, `select` là $m$ và `folds` là $K$.

## Kết quả

Một đối tượng JSON gồm `selected_all` (các feature mà cách chọn ngoài chọn, xếp tăng dần), `cv_acc_outside` và `cv_acc_inside`.

## Giới hạn

- $K$ là $4$ hoặc $5$, $n\le80$ và chia hết cho $K$, $p\le60$, $1\le m<p$.
- Mọi feature là số nguyên từ $0$ đến $9$, mỗi tập train có đủ hai lớp.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [4, 5, 7, 9, 9, 7, 2, 3, 1, 2],
    [2, 5, 0, 9, 3, 7, 2, 5, 7, 7],
    [1, 4, 1, 4, 8, 7, 9, 4, 7, 8],
    [9, 0, 1, 0, 1, 3, 0, 4, 5, 3],
    [1, 1, 2, 3, 9, 3, 6, 3, 9, 7],
    [8, 4, 5, 1, 2, 4, 1, 9, 8, 5],
    [4, 6, 7, 2, 2, 1, 3, 7, 9, 5],
    [6, 4, 1, 0, 3, 9, 1, 9, 2, 2],
    [0, 8, 1, 6, 1, 9, 8, 2, 6, 6],
    [8, 3, 7, 4, 3, 2, 1, 1, 8, 9],
    [2, 9, 3, 0, 9, 1, 4, 8, 4, 1],
    [1, 7, 8, 8, 0, 3, 7, 6, 5, 8],
    [0, 8, 0, 8, 1, 6, 2, 7, 3, 3],
    [9, 6, 7, 8, 0, 0, 9, 0, 2, 0],
    [4, 2, 4, 2, 9, 0, 1, 6, 4, 5],
    [2, 9, 8, 3, 4, 2, 2, 7, 0, 4],
    [9, 3, 7, 4, 7, 4, 2, 4, 0, 9],
    [9, 3, 5, 2, 6, 0, 6, 3, 4, 7],
    [6, 8, 0, 4, 5, 3, 0, 1, 8, 6],
    [2, 2, 4, 8, 7, 6, 4, 5, 5, 6],
    [6, 7, 6, 9, 8, 5, 9, 5, 6, 5],
    [9, 4, 2, 2, 0, 6, 3, 0, 3, 0],
    [6, 3, 5, 4, 1, 3, 9, 7, 7, 8],
    [3, 9, 2, 1, 0, 8, 6, 9, 7, 1],
    [9, 2, 5, 8, 0, 2, 5, 2, 2, 5],
    [1, 1, 9, 8, 4, 6, 2, 1, 0, 3],
    [4, 1, 6, 6, 8, 2, 0, 0, 3, 4],
    [2, 9, 9, 4, 2, 1, 5, 7, 8, 2],
    [2, 5, 1, 2, 8, 6, 2, 5, 6, 9],
    [2, 6, 9, 1, 3, 5, 2, 5, 4, 2],
    [2, 8, 6, 6, 3, 0, 6, 1, 1, 1],
    [3, 3, 5, 0, 9, 2, 8, 5, 2, 7],
    [3, 4, 2, 7, 8, 2, 8, 0, 8, 7],
    [0, 0, 6, 0, 8, 7, 8, 1, 7, 3],
    [8, 6, 5, 3, 9, 9, 9, 9, 3, 4],
    [6, 8, 5, 5, 1, 3, 5, 6, 5, 5]
  ],
  "y": [
    0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1
  ],
  "select": 5,
  "folds": 4
}
```

```output
{
  "selected_all": [1, 2, 4, 5, 6],
  "cv_acc_outside": 0.6111111111111112,
  "cv_acc_inside": 0.5
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 4](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=5).
:::
