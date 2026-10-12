# Chia theo nhóm

Cùng một bộ phân loại, cùng một dữ liệu, hai cách chia validation có thể cho hai con số rất khác nhau. Bài này đo khoảng cách ấy, và so với một "mô hình" chỉ nhớ nguồn của mẫu.

Mỗi hàng có `id`, `source`, vector đặc trưng `x` và nhãn `label` ($0$ hoặc $1$). Có hai cách chia, mỗi cách cho danh sách mã validation; mọi hàng còn lại là train.

- `random_split`: chọn ngẫu nhiên từng hàng.
- `group_split`: chọn nguyên cả vài nguồn.

Với mỗi cách chia:

1. **1-NN:** mỗi hàng validation lấy nhãn của hàng train gần nhất theo khoảng cách Euclid (bằng nhau thì mã nhỏ hơn). Báo độ chính xác.
2. **Baseline theo nguồn:** mỗi hàng validation đoán nhãn xuất hiện nhiều nhất trong các hàng train **cùng nguồn** (bằng nhau thì nhãn nhỏ hơn); nếu train không có nguồn ấy, đoán nhãn xuất hiện nhiều nhất trong cả train. Báo độ chính xác.

Báo thêm `gap`: độ chính xác 1-NN của cách chia ngẫu nhiên trừ của cách chia theo nhóm.

## Dữ liệu vào

Một đối tượng JSON gồm `rows`, `random_split` và `group_split`.

## Kết quả

Một đối tượng JSON gồm `random_split`, `group_split` (mỗi cái là `{"nn_accuracy", "source_baseline"}`) và `gap`.

## Giới hạn

- Không quá $30$ hàng. Không hàng validation nào có hai hàng train cách đều nhau ở vị trí gần nhất.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "rows": [
    {"id": "r00", "source": "doc0", "x": [1.43, -1.81], "label": 1},
    {"id": "r01", "source": "doc0", "x": [1.56, -1.49], "label": 0},
    {"id": "r02", "source": "doc0", "x": [1.89, -2.36], "label": 1},
    {"id": "r03", "source": "doc1", "x": [-0.45, -2.71], "label": 0},
    {"id": "r04", "source": "doc1", "x": [0.63, -3.17], "label": 0},
    {"id": "r05", "source": "doc1", "x": [0.77, -2.68], "label": 0},
    {"id": "r06", "source": "doc2", "x": [-2.95, -2.76], "label": 0},
    {"id": "r07", "source": "doc2", "x": [-4.02, -2.35], "label": 0},
    {"id": "r08", "source": "doc2", "x": [-2.18, -2.25], "label": 1},
    {"id": "r09", "source": "doc2", "x": [-3.28, -1.78], "label": 0},
    {"id": "r10", "source": "doc2", "x": [-3.67, -2.05], "label": 0},
    {"id": "r11", "source": "doc3", "x": [-0.84, 0.3], "label": 1},
    {"id": "r12", "source": "doc3", "x": [-2.26, 0.44], "label": 0},
    {"id": "r13", "source": "doc3", "x": [-0.62, 0.27], "label": 1},
    {"id": "r14", "source": "doc3", "x": [-1.85, 0.56], "label": 0}
  ],
  "random_split": ["r03", "r11", "r14"],
  "group_split": ["r00", "r01", "r02"]
}
```

```output
{
  "random_split": {"nn_accuracy": 1.0, "source_baseline": 0.6666666666666666},
  "group_split": {
    "nn_accuracy": 0.3333333333333333,
    "source_baseline": 0.3333333333333333
  },
  "gap": 0.6666666666666667
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
