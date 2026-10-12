# Value iteration

Khi biết đầy đủ mô hình (xác suất chuyển trạng thái, phần thưởng), ta có thể lập kế hoạch mà không cần thử: value iteration. Bài này tính giá trị tối ưu theo từng horizon (số bước còn lại), và giá trị vô hạn bước của một policy cố định.

Phần thưởng gắn với trạng thái: ở trạng thái $s$ nhận $R(s)$ rồi mới chuyển. `transitions[s][a]` là phân phối trạng thái tới khi làm $a$ ở $s$.

1. **Horizon.** $V_0(s)=0$; với $h=1..H$:
$$Q_h(s,a)=R(s)+\gamma\sum_{s'}P(s'\mid s,a)\,V_{h-1}(s'),\qquad V_h(s)=\max_a Q_h(s,a).$$
Báo $V_h$ và các hành động tối ưu ở mỗi trạng thái (mọi hành động đạt giá trị lớn nhất, sai lệch dưới $10^{-9}$, theo thứ tự trong `actions`).
2. **Policy cố định.** Với policy $\pi$ cho sẵn, giá trị vô hạn bước thỏa $V^\pi(s)=R(s)+\gamma\sum_{s'}P(s'\mid s,\pi(s))V^\pi(s')$. Giải hệ phương trình tuyến tính ấy.

## Dữ liệu vào

Một đối tượng JSON gồm `states`, `actions`, `gamma` ($<1$), `horizon`, `reward`, `transitions` và `policy`.

## Kết quả

Một đối tượng JSON gồm `horizons` (với mỗi $h$ là `{"h", "V", "best_actions"}`) và `policy_value`.

## Giới hạn

- Không quá $5$ trạng thái, $H\le4$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "states": ["S0", "S1", "S2", "S3"],
  "actions": ["A", "B"],
  "gamma": 0.8,
  "horizon": 3,
  "reward": {"S0": 0, "S1": 10, "S2": 2, "S3": 1},
  "transitions": {
    "S0": {"A": {"S1": 0.1, "S3": 0.9}, "B": {"S2": 1.0}},
    "S1": {"A": {"S3": 1.0}, "B": {"S3": 1.0}},
    "S2": {"A": {"S0": 1.0}, "B": {"S2": 0.5, "S3": 0.5}},
    "S3": {"A": {"S3": 1.0}, "B": {"S3": 1.0}}
  },
  "policy": {"S0": "B", "S1": "A", "S2": "A", "S3": "A"}
}
```

```output
{
  "horizons": [
    {
      "h": 1,
      "V": {"S0": 0.0, "S1": 10.0, "S2": 2.0, "S3": 1.0},
      "best_actions": {
        "S0": ["A", "B"],
        "S1": ["A", "B"],
        "S2": ["A", "B"],
        "S3": ["A", "B"]
      }
    },
    {
      "h": 2,
      "V": {"S0": 1.6, "S1": 10.8, "S2": 3.2, "S3": 1.8},
      "best_actions": {"S0": ["B"], "S1": ["A", "B"], "S2": ["B"], "S3": ["A", "B"]}
    },
    {
      "h": 3,
      "V": {"S0": 2.56, "S1": 11.44, "S2": 4.0, "S3": 2.44},
      "best_actions": {"S0": ["B"], "S1": ["A", "B"], "S2": ["B"], "S3": ["A", "B"]}
    }
  ],
  "policy_value": {
    "S0": 4.4444444444444455,
    "S1": 14.0,
    "S2": 5.555555555555557,
    "S3": 5.000000000000001
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
