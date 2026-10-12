# Lợi ích và rủi ro

Kế hoạch trên giấy giả sử mọi bước đều thành công. Thực tế, một bước có thể hỏng (mô hình không hội tụ, hết thời gian, lỗi định dạng), và khi một bước hỏng thì các bước sau của cùng việc ấy cũng không làm được. Bài này so vài kế hoạch theo điểm kỳ vọng **và** theo rủi ro không có bài nộp hợp lệ nào.

Mỗi kế hoạch gồm vài việc độc lập; mỗi việc là chuỗi bước, bước có `success` (xác suất thành công) và `gain` (điểm được thêm nếu thành công). Bước $j$ của một việc chỉ được làm khi mọi bước trước của việc ấy đã thành công; các bước thành công hay hỏng độc lập với nhau.

1. Điểm kỳ vọng của một việc $=\sum_j\big(\prod_{i\le j}\text{success}_i\big)\cdot\text{gain}_j$; của kế hoạch là tổng các việc.
2. Kế hoạch có bài nộp hợp lệ khi bước đầu của ít nhất một việc thành công. Xác suất không có bài hợp lệ là $\prod_{\text{việc}}(1-\text{success}_{\text{bước đầu}})$.
3. Báo kế hoạch có điểm kỳ vọng cao nhất, và kế hoạch được chọn: điểm kỳ vọng cao nhất trong các kế hoạch có xác suất không hợp lệ không vượt `max_risk` (`null` nếu không có). Bằng điểm thì tên nhỏ hơn.

## Dữ liệu vào

Một đối tượng JSON gồm `max_risk` và `plans` (mỗi kế hoạch là `{"name", "tasks"}`, mỗi việc là `{"steps"}`).

## Kết quả

Một đối tượng JSON gồm `plans` (mỗi kế hoạch là `{"name", "expected_points", "p_no_valid"}`), `best_expected` và `chosen`.

## Giới hạn

- Không quá $4$ kế hoạch, mỗi kế hoạch không quá $8$ bước. Không xác suất nào sát đúng `max_risk`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "max_risk": 0.1,
  "plans": [
    {
      "name": "safe",
      "tasks": [
        {
          "steps": [{"success": 0.95, "gain": 20}, {"success": 0.8, "gain": 10}]
        },
        {"steps": [{"success": 0.9, "gain": 15}]}
      ]
    },
    {
      "name": "bold",
      "tasks": [
        {
          "steps": [{"success": 0.6, "gain": 60}, {"success": 0.7, "gain": 40}]
        }
      ]
    },
    {
      "name": "one_more_seed",
      "tasks": [
        {
          "steps": [
            {"success": 0.95, "gain": 20},
            {"success": 0.8, "gain": 10},
            {"success": 0.5, "gain": 3}
          ]
        }
      ]
    }
  ]
}
```

```output
{
  "plans": [
    {"name": "safe", "expected_points": 40.1, "p_no_valid": 0.005},
    {"name": "bold", "expected_points": 52.8, "p_no_valid": 0.4},
    {
      "name": "one_more_seed",
      "expected_points": 27.74,
      "p_no_valid": 0.05
    }
  ],
  "best_expected": "bold",
  "chosen": "safe"
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
