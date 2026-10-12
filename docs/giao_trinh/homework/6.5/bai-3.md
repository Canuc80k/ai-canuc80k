# BLEU

BLEU chấm bản dịch máy bằng cách đếm n-gram trùng với các bản dịch mẫu. Nếu không chặn, một câu lặp đi lặp lại một từ đúng sẽ được điểm cao; BLEU vì thế **cắt** số lần trùng.

Có các câu dịch `candidates` (list từ), mỗi câu có một hoặc vài bản mẫu `references`. Với $n=1..N$ (`max_order`):

1. **Đếm cắt.** Với mỗi câu dịch và mỗi n-gram của nó, số lần được tính là $\min(\text{số lần trong câu dịch},\ \max_{\text{bản mẫu}}\text{số lần trong bản mẫu})$. Cộng trên mọi câu: `clipped[n-1]`. Tổng số n-gram của các câu dịch: `totals[n-1]`.
2. **Precision** $p_n$ = `clipped` / `totals`, bằng $0$ nếu `totals` bằng $0$.
3. **Độ dài.** $C$ là tổng độ dài các câu dịch. Với mỗi câu dịch, chọn bản mẫu có độ dài gần nhất (bằng nhau thì bản ngắn hơn); $R$ là tổng các độ dài ấy.
4. **Brevity penalty:** $0$ nếu $C=0$; $1$ nếu $C\ge R$; ngược lại $e^{1-R/C}$.
5. $\text{BLEU}=\text{BP}\cdot\big(p_1p_2\cdots p_N\big)^{1/N}$, bằng $0$ nếu có $p_n$ nào bằng $0$. Không làm trơn.

## Dữ liệu vào

Một đối tượng JSON gồm `candidates`, `references` và `max_order`.

## Kết quả

Một đối tượng JSON gồm `clipped`, `totals`, `precisions`, `candidate_length`, `reference_length`, `brevity_penalty` và `bleu`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "candidates": [[], []],
  "references": [
    [["bóng", "sân"], ["đội", "bóng", "trên", "sân"]],
    [["đọc", "quyển", "sách"], ["đọc", "sách", "mới"]]
  ],
  "max_order": 2
}
```

```output
{
  "clipped": [0, 0],
  "totals": [0, 0],
  "precisions": [0, 0],
  "candidate_length": 0,
  "reference_length": 5,
  "brevity_penalty": 0,
  "bleu": 0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
