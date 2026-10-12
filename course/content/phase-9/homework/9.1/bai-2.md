# Một bước Bellman

Phương trình Bellman tính việc xa bằng việc gần: giá trị của một hành động là phần thưởng ngay cộng giá trị (chiết khấu) của trạng thái tới.

Cho mô hình môi trường `P`: `P[s][a]` là danh sách các khả năng $[p, s', r]$ (xác suất, trạng thái tới, phần thưởng) khi làm $a$ ở $s$; ước lượng giá trị hiện tại `V`; hệ số $\gamma$; tập trạng thái kết thúc `terminal` (giá trị luôn coi là $0$).

Với mỗi trạng thái $s$ trong `P` (theo thứ tự chuỗi) và mỗi hành động $a$:
$$Q(s,a)=\sum p\cdot\big(r+\gamma\,V(s')\big),$$
với $V(s')=0$ nếu $s'$ là trạng thái kết thúc. Hành động tham lam là hành động có $Q$ lớn nhất (bằng nhau thì tên nhỏ hơn), và giá trị mới của $s$ là $Q$ ấy.

## Dữ liệu vào

Một đối tượng JSON gồm `P`, `V`, `gamma` và `terminal`.

## Kết quả

Một đối tượng JSON gồm `states`: từ trạng thái tới `{"Q", "greedy", "new_V"}`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "P": {
    "s0": {
      "right": [[0.5, "goal", 0], [0.5, "s0", 0]],
      "stay": [[1.0, "s1", -1]]
    },
    "s1": {
      "left": [[1.0, "goal", 1]],
      "right": [[0.8, "s0", 1], [0.2, "goal", 1]]
    }
  },
  "V": {"s0": 7, "s1": -5, "goal": -2},
  "gamma": 0.5,
  "terminal": ["goal"]
}
```

```output
{
  "states": {
    "s0": {
      "Q": {"right": 1.75, "stay": -3.5},
      "greedy": "right",
      "new_V": 1.75
    },
    "s1": {"Q": {"left": 1.0, "right": 3.8}, "greedy": "right", "new_V": 3.8}
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
