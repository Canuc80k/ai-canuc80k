# Chi phí

Một mô hình phát hiện gian lận chấm cho mỗi giao dịch một điểm `score`, và giao dịch bị gắn cờ khi `score` lớn hơn hoặc bằng ngưỡng. Hai loại lỗi có giá rất khác nhau. Bỏ sót một giao dịch gian lận làm mất `cost_fn` đồng. Gắn cờ nhầm một giao dịch thật thì tốn `cost_fp` đồng để người kiểm tra lại.

Tổng chi phí ở một ngưỡng là $\text{cost\_fn}\cdot\text{FN}+\text{cost\_fp}\cdot\text{FP}$. Hãy tính tổng chi phí ở mỗi ngưỡng trong `thresholds`, chọn ngưỡng rẻ nhất (hòa thì lấy ngưỡng nhỏ nhất), rồi báo precision và recall của lớp gian lận ở ngưỡng ấy. Mẫu số bằng $0$ thì lấy $0$.

## Dữ liệu vào

Một đối tượng JSON gồm `y` ($1$ là gian lận), `score`, `thresholds` (tăng dần), `cost_fn` và `cost_fp`.

## Kết quả

Một đối tượng JSON gồm `costs` (một số cho mỗi ngưỡng), `best_threshold`, `precision`, `recall`.

## Giới hạn

- Từ $1$ đến $1000$ giao dịch, điểm từ $0$ đến $1$.
- Từ $1$ đến $10$ ngưỡng, hai chi phí là số nguyên từ $1$ đến $1000$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "y": [0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
  "score": [0.05, 0.1, 0.2, 0.3, 0.35, 0.5, 0.55, 0.6, 0.8, 0.9],
  "thresholds": [0.25, 0.5, 0.7],
  "cost_fn": 10,
  "cost_fp": 1
}
```

```output
{
  "costs": [4, 2, 10],
  "best_threshold": 0.5,
  "precision": 0.6,
  "recall": 1.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 275–276](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=101).
:::
