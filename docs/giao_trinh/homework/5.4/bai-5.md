# Attention rollout

Muốn biết ViT dựa vào patch nào để phân loại, nhìn attention của token CLS ở lớp cuối là chưa đủ: thông tin đã được trộn qua mọi lớp trước, và kết nối tắt cũng mang một phần thông tin đi thẳng. Attention rollout gộp attention của mọi lớp lại.

Token $0$ là CLS, token $1,\dots,n$ là các patch theo thứ tự hàng của lưới `grid`. Mỗi lớp có ma trận attention $A_l$ (đã lấy trung bình các đầu), mỗi hàng cộng lại bằng $1$.

1. Tính kết nối tắt: $\tilde A_l=\tfrac12A_l+\tfrac12I$, rồi chuẩn hóa mỗi hàng của $\tilde A_l$ để tổng bằng $1$.
2. Gộp từ lớp đầu tới lớp cuối: $R=\tilde A_L\cdots\tilde A_2\tilde A_1$.
3. Hàng $0$ của $R$, bỏ cột $0$, cho biết CLS dựa vào từng patch bao nhiêu. Xếp lại thành lưới.

Hãy báo $R$, bản đồ của CLS trên lưới, patch có giá trị lớn nhất theo rollout, và patch được CLS nhìn nhiều nhất ở lớp cuối theo $A_L$ thô (đánh số patch từ $0$; hòa thì số nhỏ).

## Dữ liệu vào

Một đối tượng JSON gồm `attentions` (list các ma trận, theo thứ tự lớp) và `grid` ($[h,w]$).

## Kết quả

Một đối tượng JSON gồm `rollout`, `cls_map`, `top_patch` và `top_patch_last_layer`.

## Giới hạn

- Không quá $6$ lớp và $10$ token. Không có hai patch hòa nhau ở vị trí lớn nhất.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "attentions": [
    [
      [0.1, 0.1, 0.1, 0.7, 0.0],
      [0.2, 0.2, 0.2, 0.2, 0.2],
      [0.2, 0.2, 0.2, 0.2, 0.2],
      [0.0, 0.0, 0.0, 1.0, 0.0],
      [0.2, 0.2, 0.2, 0.2, 0.2]
    ],
    [
      [0.1, 0.0, 0.5, 0.0, 0.4],
      [0.2, 0.2, 0.2, 0.2, 0.2],
      [0.25, 0.25, 0.0, 0.5, 0.0],
      [0.2, 0.2, 0.2, 0.2, 0.2],
      [0.0, 0.0, 0.0, 0.0, 1.0]
    ]
  ],
  "grid": [2, 2]
}
```

```output
{
  "rollout": [
    [
      0.3475000000000001, 0.07250000000000001, 0.19749999999999998,
      0.2375, 0.145
    ],
    [
      0.13500000000000004, 0.3850000000000001, 0.13500000000000004,
      0.21500000000000008, 0.13000000000000003
    ],
    [0.13125, 0.13125000000000003, 0.31875, 0.35625, 0.0625],
    [0.085, 0.085, 0.08499999999999999, 0.665, 0.08],
    [0.1, 0.1, 0.1, 0.1, 0.6]
  ],
  "cls_map": [[0.07250000000000001, 0.19749999999999998], [0.2375, 0.145]],
  "top_patch": 2,
  "top_patch_last_layer": 1
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
