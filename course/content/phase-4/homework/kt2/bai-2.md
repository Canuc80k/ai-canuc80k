# Sổ optimizer

Tạo optimizer xong rồi mới thay head của mô hình: head mới có gradient, nhưng không nằm trong danh sách tham số của optimizer, nên không bao giờ được cập nhật. Bài này tái hiện lỗi ấy rồi sửa.

1. Tạo head cũ `Linear(3, 2)` kiểu `float64` và `SGD(lr)` trên các tham số của nó.
2. Thay bằng head mới `Linear(3, 2)` có trọng số `new_weight`, bias `new_bias`. Forward, `CrossEntropyLoss` trung bình, `backward()`, rồi `step()` của optimizer **cũ**. Ghi trọng số head mới lúc này (`broken_weight`).
3. Tạo `SGD(lr)` mới trên tham số của head mới, xóa gradient, forward, `backward()`, `step()`. Ghi trọng số (`fixed_weight`).

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (mỗi hàng ba số), `labels` ($0$/$1$), `new_weight` ($2\times3$), `new_bias` và `lr`.

## Kết quả

Một đối tượng JSON gồm `broken_weight`, `fixed_weight` và `new_head_in_old_optimizer` (head mới có nằm trong optimizer cũ không).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [0.6585529992824741, -1.5719341702476237, 0.44840593311584215],
    [0.8988109261445906, 0.661429392205163, -2.2213349559716717],
    [1.2185774057971854, 0.313911878257594, -0.4030830820657827],
    [0.11405053525151357, -0.4066786572011673, -0.8537186325490661],
    [0.8624216830837342, -0.48470883685413424, 1.2615807119912799],
    [-1.315296239593139, -1.2864055299315635, 0.12432291544351613],
    [0.6941075990551734, -1.3520390731244862, -0.18708238174585884],
    [0.45683832502704014, -0.19812036698273328, -0.33534465907744454]
  ],
  "labels": [1, 1, 1, 0, 0, 1, 0, 0],
  "new_weight": [
    [1.1680861678842493, -0.38338278595106956, 0.44308628946811696],
    [-1.8687566372091011, -1.5147939063345992, -1.6566533773971666]
  ],
  "new_bias": [-1.7949199341999134, -0.7703454980502085],
  "lr": 0.05
}
```

```output
{
  "broken_weight": [
    [1.1680861678842493, -0.38338278595106956, 0.44308628946811696],
    [-1.8687566372091011, -1.5147939063345992, -1.6566533773971666]
  ],
  "fixed_weight": [
    [1.1641592106419993, -0.3894639063080466, 0.4381950612056673],
    [-1.8648296799668511, -1.5087127859776222, -1.651762149134717]
  ],
  "new_head_in_old_optimizer": false
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
