# Model card

Một model pretrained không chỉ là tệp trọng số. Nó còn đi kèm cách tiền xử lý đầu vào và danh sách tên lớp, ghi trong model card. Dùng sai tiền xử lý, model vẫn chạy và vẫn cho ra nhãn, chỉ là nhãn sai.

Mỗi ảnh là một lưới $H\times W$ điểm, mỗi điểm ba số từ $0$ đến $255$ theo thứ tự R, G, B như trong tệp ảnh. Model card cho:

- `channel_order`: thứ tự kênh model mong đợi, `RGB` hoặc `BGR`. Với `BGR`, kênh $0$ là B, kênh $2$ là R.
- `scale`: chia mọi giá trị cho số này.
- `mean`, `std`: với kênh $c$ (theo thứ tự model mong đợi), lấy $(x/\text{scale}-\text{mean}_c)/\text{std}_c$.
- `labels`: tên lớp theo thứ tự đầu ra.

Sau khi tiền xử lý, trải ảnh thành vector theo thứ tự kênh, rồi hàng, rồi cột (tức tensor `(C, H, W)` trải phẳng). Head tuyến tính cho logits $z=Wx+b$, nhãn là tên của lớp có logit lớn nhất.

Hãy tính, với từng ảnh: vector đầu vào sau tiền xử lý, logits, nhãn. Thêm nhãn mà ta sẽ nhận nếu **bỏ qua model card**: giữ thứ tự RGB và đưa thẳng giá trị $0$ tới $255$ vào head.

## Dữ liệu vào

Một đối tượng JSON gồm `card`, `images`, `head_weight` ($K$ hàng, mỗi hàng $3HW$ số) và `head_bias`.

## Kết quả

Một đối tượng JSON gồm `inputs`, `logits`, `labels` và `naive_labels`, mỗi trường một phần tử cho mỗi ảnh.

## Giới hạn

- Không quá $5$ ảnh, mỗi ảnh không quá $3\times3$ điểm. Không có hai logit nào sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "card": {
    "scale": 255.0,
    "mean": [0.5, 0.5, 0.5],
    "std": [0.25, 0.25, 0.25],
    "channel_order": "BGR",
    "labels": ["cat", "dog"]
  },
  "images": [[[[255, 0, 0]]], [[[0, 0, 255]]], [[[128, 64, 32]]]],
  "head_weight": [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
  "head_bias": [0.0, 0.1]
}
```

```output
{
  "inputs": [
    [-2.0, -2.0, 2.0],
    [2.0, -2.0, -2.0],
    [-1.4980392156862745, -0.996078431372549, 0.007843137254901933]
  ],
  "logits": [[-2.0, 2.1], [2.0, -1.9], [-1.4980392156862745, 0.10784313725490194]],
  "labels": ["dog", "cat", "dog"],
  "naive_labels": ["cat", "dog", "cat"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
