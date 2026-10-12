# Gán anchor

Faster R-CNN đặt sẵn rất nhiều box mẫu (anchor) trên ảnh. Để huấn luyện, mỗi anchor cần một nhãn: là vật, là nền, hay bỏ qua. Bài này gán nhãn ấy.

Tính IoU của mọi anchor với mọi box thật. Với mỗi anchor, gọi IoU lớn nhất của nó là $m$:

1. $m\ge$ `positive`: nhãn $1$ (vật).
2. $m<$ `negative`: nhãn $0$ (nền).
3. Còn lại: nhãn $-1$ (bỏ qua, không tính vào loss).

Nhưng có box thật không anchor nào phủ tới ngưỡng `positive`, và nó sẽ không được học. Nên thêm bước 4: với mỗi box thật, tìm IoU lớn nhất của nó với các anchor; mọi anchor đạt đúng IoU ấy được đổi thành nhãn $1$.

Anchor nhãn $1$ được ghép với box thật có IoU lớn nhất với nó. Anchor nhãn $0$ hoặc $-1$ ghép với $-1$. Box thật đánh số từ $0$.

Box viết dạng $[x_1,y_1,x_2,y_2]$ theo tọa độ liên tục: bề rộng là $x_2-x_1$.

## Dữ liệu vào

Một đối tượng JSON gồm `anchors`, `gt`, `positive` và `negative`.

## Kết quả

Một đối tượng JSON gồm `iou` (ma trận anchor $\times$ box thật), `labels`, `matched_gt`, `positives` (số anchor nhãn $1$) và `negatives` (số anchor nhãn $0$).

## Giới hạn

- Không quá $12$ anchor và $3$ box thật.
- Mỗi box thật chồng lên ít nhất một anchor. Không anchor nào có hai IoU dương bằng nhau, và không IoU nào đúng bằng một ngưỡng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "anchors": [
    [0, 0, 4, 4],
    [2, 0, 6, 4],
    [4, 0, 8, 4],
    [0, 4, 4, 8],
    [2, 4, 6, 8],
    [4, 4, 8, 8]
  ],
  "gt": [[1, 0, 5, 4], [5, 5, 8, 8]],
  "positive": 0.7,
  "negative": 0.3
}
```

```output
{
  "iou": [
    [0.6, 0.0],
    [0.6, 0.0],
    [0.14285714285714285, 0.0],
    [0.0, 0.0],
    [0.0, 0.13636363636363635],
    [0.0, 0.5625]
  ],
  "labels": [1, 1, 0, 0, 0, 1],
  "matched_gt": [0, 0, -1, -1, -1, 1],
  "positives": 3,
  "negatives": 3
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
