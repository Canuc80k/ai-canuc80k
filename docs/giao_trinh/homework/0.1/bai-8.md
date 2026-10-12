# Đọc chéo

Cho một bảng vuông $M$ cỡ $N\times N$. Hãy đọc bảng theo các **đường chéo ngược**. Đường chéo thứ $d$ gồm các ô $(r, c)$ có $r+c=d$. Đọc lần lượt $d = 0, 1, \dots, 2N-2$, trong mỗi đường chéo thì đi từ hàng trên xuống hàng dưới.

Được một dãy $N^2$ số. Xếp dãy ấy vào một bảng mới $N\times N$, điền lần lượt từng hàng từ trái sang phải.

Ví dụ, bảng `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]` đọc ra dãy $1, 2, 4, 3, 5, 7, 6, 8, 9$, nên bảng mới là `[[1, 2, 4], [3, 5, 7], [6, 8, 9]]`.

Đầu vào có khi không phải bảng vuông hợp lệ. Bảng hợp lệ là một list khác rỗng gồm $N$ list con, mỗi list con có đúng $N$ phần tử, và mọi phần tử đều là số nguyên. `true`, `false` hay chuỗi `"2"` không được tính là số nguyên. Gặp đầu vào không hợp lệ thì trả về `[]`.

Hàm không được làm đổi bảng gốc.

## Dữ liệu vào

Một giá trị JSON $M$.

## Kết quả

Bảng mới, hoặc `[]`.

## Giới hạn

- $M$ có không quá $12$ phần tử, mỗi list con không quá $12$ phần tử, các số có trị tuyệt đối không quá $100$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

```output
[[1, 2, 4], [3, 5, 7], [6, 8, 9]]
```

```input
[[1, 2], [3]]
```

```output
[]
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
