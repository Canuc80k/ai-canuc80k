# Lịch learning rate

Learning rate thường không giữ nguyên suốt quá trình học. Bài này tính learning rate theo vài lịch hay gặp. Gọi $T$ là tổng số bước, bước được đánh số $t=0,1,\dots,T-1$, $\eta_{\max}$ là `peak_lr` và $\eta_{\min}$ là `min_lr`.

| Lịch | Learning rate ở bước $t$ |
|---|---|
| `constant` | $\eta_{\max}$ |
| `cosine` | $\eta_{\min}+(\eta_{\max}-\eta_{\min})\cdot\dfrac{1+\cos(\pi t/T)}{2}$ |
| `step` | $\eta_{\max}\cdot\gamma^{k}$, với $k$ là số mốc trong `milestones` không lớn hơn $t$ |

Lịch có tiền tố `warmup_` khởi động tuyến tính trong $W$ bước đầu: với $t<W$, learning rate là $\eta_{\max}\cdot t/W$. Từ bước $W$ trở đi, dùng lịch phía sau tiền tố với bước $t-W$ thay cho $t$ và $T-W$ thay cho $T$. Riêng `warmup_step` vẫn so các mốc với $t-W$.

Với mỗi lịch được hỏi, hãy cho biết learning rate tại các bước trong `queries`, và learning rate trung bình trên cả $T$ bước. Trung bình ấy cho biết tổng quãng đường mà các bước cập nhật được phép đi. Để dễ so các lịch, mọi con số ghi dưới dạng **tỉ lệ so với $\eta_{\max}$**, tức learning rate chia cho `peak_lr`.

## Dữ liệu vào

Một đối tượng JSON gồm `total_steps`, `peak_lr`, `min_lr`, `warmup`, `milestones`, `gamma`, `schedules` (tên các lịch) và `queries`.

## Kết quả

Một đối tượng JSON, mỗi lịch trong `schedules` là một trường `{"factors": [...], "average": ...}`, cả hai đã chia cho `peak_lr`.

## Giới hạn

- $T\le100\,000$, $1\le W<T$, mọi bước trong `queries` từ $0$ tới $T-1$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "total_steps": 100000,
  "peak_lr": 0.0003,
  "min_lr": 3e-05,
  "warmup": 5000,
  "milestones": [60000, 80000],
  "gamma": 0.1,
  "schedules": ["constant", "cosine", "step", "warmup_cosine"],
  "queries": [0, 2500, 20000, 50000, 60000, 80000, 99999]
}
```

```output
{
  "constant": {"factors": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], "average": 1.0},
  "cosine": {
    "factors": [
      1.0, 0.9986128001799076, 0.9140576474687263, 0.55,
      0.41094235253127365, 0.18594235253127367, 0.10000000022206611
    ],
    "average": 0.5500045
  },
  "step": {
    "factors": [
      1.0, 1.0, 1.0, 1.0, 0.1, 0.010000000000000002,
      0.010000000000000002
    ],
    "average": 0.6219999999999999
  },
  "warmup_cosine": {
    "factors": [
      0.0, 0.5, 0.94576318804292, 0.5871607054625495,
      0.43953153078664037, 0.19488677077162292, 0.10000000024605664
    ],
    "average": 0.5474994999999999
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 84](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=34).
:::
