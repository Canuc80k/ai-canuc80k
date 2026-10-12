# Q-learning

Q-learning không cần biết mô hình môi trường: nó học từ từng bộ trải nghiệm $(s, a, r, s')$, tức ở trạng thái $s$ làm $a$, nhận $r$ và tới $s'$. Bài này chạy đúng chuỗi cập nhật ấy.

Mọi $Q(s,a)$ ban đầu bằng $0$. Với mỗi bộ trải nghiệm theo thứ tự:
$$Q(s,a)\leftarrow(1-\alpha)\,Q(s,a)+\alpha\Big(r+\gamma\max_{a'}Q(s',a')\Big),$$
trong đó nếu $s'$ là trạng thái kết thúc (trong `terminal`) thì phần $\max_{a'}Q(s',a')$ coi là $0$. Mỗi bước dùng giá trị $Q$ **hiện tại** (đã gồm các cập nhật trước).

Báo giá trị mới sau từng cập nhật, bảng $Q$ cuối cùng, và hành động tham lam ở mỗi trạng thái không kết thúc (bằng nhau thì hành động đứng trước trong `actions`).

## Dữ liệu vào

Một đối tượng JSON gồm `states`, `actions`, `gamma`, `alpha`, `terminal` và `experience` (mỗi bộ là $[s, a, r, s']$).

## Kết quả

Một đối tượng JSON gồm `updates` (mỗi cập nhật là `{"state", "action", "value"}`), `Q` (từ trạng thái tới từ hành động tới giá trị) và `greedy`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "states": ["A", "B", "C", "D"],
  "actions": ["Move", "Stay"],
  "gamma": 0.9,
  "alpha": 1.0,
  "terminal": [],
  "experience": [
    ["A", "Move", 0, "B"],
    ["B", "Move", 0, "C"],
    ["C", "Move", 1, "A"],
    ["A", "Move", 0, "B"],
    ["B", "Move", 0, "C"],
    ["A", "Move", 0, "B"],
    ["B", "Move", 0, "D"]
  ]
}
```

```output
{
  "updates": [
    {"state": "A", "action": "Move", "value": 0.0},
    {"state": "B", "action": "Move", "value": 0.0},
    {"state": "C", "action": "Move", "value": 1.0},
    {"state": "A", "action": "Move", "value": 0.0},
    {"state": "B", "action": "Move", "value": 0.9},
    {"state": "A", "action": "Move", "value": 0.81},
    {"state": "B", "action": "Move", "value": 0.0}
  ],
  "Q": {
    "A": {"Move": 0.81, "Stay": 0.0},
    "B": {"Move": 0.0, "Stay": 0.0},
    "C": {"Move": 1.0, "Stay": 0.0},
    "D": {"Move": 0.0, "Stay": 0.0}
  },
  "greedy": {"A": "Move", "B": "Move", "C": "Move", "D": "Move"}
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
