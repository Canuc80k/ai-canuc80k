# Xác suất OOB

Rừng có $B$ cây, mỗi cây cho một xác suất thuộc lớp $1$ cho từng mẫu. Muốn chấm rừng mà không cần tập validation riêng, ta dùng dự đoán out-of-bag: với mỗi mẫu, chỉ hỏi những cây **không** thấy mẫu ấy lúc học.

Với mẫu $i$, xác suất OOB là trung bình xác suất của các cây mà lượt rút không chứa $i$. Nếu cây nào cũng đã thấy mẫu $i$ thì mẫu ấy không có dự đoán OOB, ghi `null`. Đoán lớp $1$ khi xác suất OOB lớn hơn $0.5$, bằng $0.5$ thì đoán $0$. Accuracy chỉ tính trên các mẫu có dự đoán OOB.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `bootstraps` ($B$ lượt rút), `probabilities` (ma trận $B\times n$) và `y`.

## Kết quả

Một đối tượng JSON gồm `oob_probability` ($n$ số hoặc `null`), `covered_rows` (số mẫu có dự đoán OOB) và `accuracy` (hoặc `null` nếu không mẫu nào có).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "bootstraps": [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]],
  "probabilities": [
    [
      0.9607894593180786, 0.3042122142727822, 0.232001321522604,
      0.09676390385536393, 0.47177652449417806, 0.454315452798425
    ],
    [
      0.5472892977559604, 0.4072119960196261, 0.09553633146043738,
      0.05343787024910074, 0.35520969436549865, 0.0068236141782715976
    ],
    [
      0.6773164067593842, 0.7929674255533641, 0.19384991808608665,
      0.5327526662492355, 0.8176393380744472, 0.9208923339678362
    ]
  ],
  "y": [1, 1, 1, 1, 1, 1]
}
```

```output
{
  "oob_probability": [null, null, null, null, null, null],
  "covered_rows": 0,
  "accuracy": null
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
