# Gradient cộng dồn

PyTorch không ghi đè `.grad` mà **cộng** gradient mới vào đó. Bài này cho ta tận mắt thấy điều ấy.

Cho tensor `x` cần gradient và vector hằng `a`. Đặt $J_1=\operatorname{mean}(x^3)$ và $J_2=\sum_i a_ix_i$. Làm theo đúng thứ tự:

1. Forward $J_1$, gọi `backward()`. Lưu bản sao của `x.grad`, gọi là `first`.
2. Forward $J_2$ mới, gọi `backward()` mà không xóa `.grad`. Lưu bản sao, gọi là `accumulated`.
3. Xóa gradient bằng `x.grad = None`, forward $J_1$ lần nữa rồi `backward()`. Lưu kết quả, gọi là `after_reset`.

Mỗi lần backward dùng một lần forward mới, không dùng `retain_graph`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `x` và `a`, cùng độ dài.

## Kết quả

Một đối tượng JSON gồm `first`, `accumulated` và `after_reset`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x": [
    -0.025661605931689643, -0.2698080588775131, -1.7578144276508583,
    0.6392774740149706, -0.5579296520252873, 0.626881764410742
  ],
  "a": [
    -0.8309120423662885, 0.5852517710026026, -0.5710878399185039,
    0.09653092353703967, 1.5783323390001442, -0.6775748355876624
  ]
}
```

```output
{
  "first": [
    0.0003292590094966645, 0.03639819431762578, 1.544955781028757,
    0.2043378443914807, 0.1556427483045291, 0.19649037327536248
  ],
  "accumulated": [
    -0.8305827833567918, 0.6216499653202284, 0.9738679411102532,
    0.30086876792852035, 1.7339750873046733, -0.48108446231229995
  ],
  "after_reset": [
    0.0003292590094966645, 0.03639819431762578, 1.544955781028757,
    0.2043378443914807, 0.1556427483045291, 0.19649037327536248
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
