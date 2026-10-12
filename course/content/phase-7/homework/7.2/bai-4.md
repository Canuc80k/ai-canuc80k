# mAP nhiều nhãn

Gắn nhãn âm thanh thường là bài toán **nhiều nhãn**: một clip có thể vừa có tiếng chó sủa vừa có tiếng xe. Bộ AudioSet chấm bằng mAP: average precision của từng lớp, rồi lấy trung bình. Bài này tính mAP và so với hai cách đo theo ngưỡng.

`labels[i][c]` là $1$ nếu clip $i$ có lớp $c$; `scores[i][c]` là điểm mô hình cho.

**AP của một lớp** (như `average_precision_score` của scikit-learn):

1. Xét các ngưỡng là các giá trị điểm khác nhau của lớp ấy, từ cao xuống thấp. Ở mỗi ngưỡng, mọi clip có điểm từ ngưỡng trở lên được đoán dương; các clip **bằng điểm nhau vào cùng lúc**.
2. Tại mỗi ngưỡng có precision $P$ và recall $R$. $\text{AP}=\sum(R_n-R_{n-1})P_n$, với $R_0=0$.
3. Lớp không có clip dương nào thì không có AP (`null`) và không tính vào mAP.

**Theo ngưỡng** `threshold` (đoán dương khi điểm từ ngưỡng trở lên): `subset_accuracy` là tỉ lệ clip đoán đúng **mọi** nhãn; `label_accuracy` là tỉ lệ ô (clip, lớp) đoán đúng.

## Dữ liệu vào

Một đối tượng JSON gồm `labels`, `scores` và `threshold`.

## Kết quả

Một đối tượng JSON gồm `per_class_ap`, `mAP`, `subset_accuracy` và `label_accuracy`.

## Giới hạn

- Không quá $10$ clip và $5$ lớp; có ít nhất một nhãn dương.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "labels": [[1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0]],
  "scores": [
    [0.9, 0.2, 0.1],
    [0.6, 0.6, 0.3],
    [0.6, 0.4, 0.2],
    [0.2, 0.7, 0.05],
    [0.3, 0.1, 0.1]
  ],
  "threshold": 0.5
}
```

```output
{
  "per_class_ap": [0.8055555555555556, 0.5833333333333333, null],
  "mAP": 0.6944444444444444,
  "subset_accuracy": 0.4,
  "label_accuracy": 0.7333333333333333
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
