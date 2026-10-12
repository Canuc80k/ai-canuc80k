# Lõi và nhiễu

DBSCAN xếp mỗi điểm vào một trong ba loại. Gọi láng giềng của một điểm là các điểm cách nó không quá `eps`, tính cả chính nó.

- Điểm **lõi** có ít nhất `min_samples` láng giềng.
- Điểm **biên** không phải lõi, nhưng là láng giềng của ít nhất một điểm lõi.
- Còn lại là **nhiễu**.

Dữ liệu ở đây là một chiều. Hãy xếp loại từng điểm. Có thể tự đếm láng giềng, hoặc dùng `DBSCAN` của scikit-learn rồi đọc `core_sample_indices_` và `labels_`.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `X` (mỗi hàng một điểm có một tọa độ), `eps` và `min_samples`.

## Kết quả

Một đối tượng JSON `{"status": [...]}`, mỗi phần tử là `"core"`, `"border"` hoặc `"noise"`, theo thứ tự điểm.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "X": [[0.0], [0.1], [0.2], [0.35], [3.0]],
  "eps": 0.16,
  "min_samples": 1
}
```

```output
{"status": ["core", "core", "core", "core", "core"]}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
