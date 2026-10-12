# Trung bình hạng

Khi metric chỉ xét thứ tự (như AUC), các model có thể cho điểm trên những thang rất khác nhau: một model cho xác suất, model kia cho điểm từ $0$ tới $100$. Cộng thẳng điểm thì model có thang lớn áp đảo. Trung bình **hạng** đưa mọi model về cùng một thang.

1. **Hạng** của từng model: điểm nhỏ nhất có hạng $1$; các điểm bằng nhau nhận trung bình các hạng mà chúng chiếm (như `scipy.stats.rankdata`, cách `average`).
2. Trung bình hạng của các model cho mỗi mẫu.
3. **AUC** của một dãy điểm: tỉ lệ các cặp (mẫu dương, mẫu âm) mà mẫu dương có điểm cao hơn; bằng điểm tính nửa cặp.

Báo hạng, trung bình hạng, AUC của từng model, của trung bình hạng và của trung bình điểm thô.

## Dữ liệu vào

Một đối tượng JSON gồm `scores` (mỗi hàng là điểm của một model) và `labels` (có cả $0$ và $1$).

## Kết quả

Một đối tượng JSON gồm `ranks`, `rank_average`, `auc_models`, `auc_rank_average` và `auc_score_average`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "scores": [[0.1, 0.4, 0.35, 0.8, 0.8], [12.0, 30.0, 50.0, 40.0, 41.0]],
  "labels": [0, 0, 1, 1, 1]
}
```

```output
{
  "ranks": [[1.0, 3.0, 2.0, 4.5, 4.5], [1.0, 2.0, 5.0, 3.0, 4.0]],
  "rank_average": [1.0, 2.5, 3.5, 3.75, 4.25],
  "auc_models": [0.8333333333333333, 1.0],
  "auc_rank_average": 1.0,
  "auc_score_average": 1.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
