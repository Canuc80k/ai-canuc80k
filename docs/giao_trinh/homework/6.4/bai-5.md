# Beam search

Sinh văn bản tham lam (mỗi bước lấy token có xác suất cao nhất) không chắc cho câu có xác suất cao nhất. Beam search giữ vài ứng viên cùng lúc để bớt "tham ăn". Bài này so ba cách trên một mô hình bigram nhỏ cho sẵn.

`probs[i][j]` là xác suất token $j$ đứng sau token $i$ (mọi giá trị dương). Câu bắt đầu sau `bos`, và kết thúc khi sinh ra `eos`. Không bao giờ sinh `bos`. Log-xác suất của một dãy là tổng $\log$ các xác suất chuyển, tính từ `bos`. Điểm của một dãy dài $n$ token là
$$\text{score}=\frac{\text{log-xác suất}}{n^{\alpha}},$$
với $\alpha$ là `length_penalty` ($\alpha=0$ là không chuẩn hóa độ dài).

1. **Greedy.** Mỗi bước lấy token có xác suất chuyển lớn nhất (bằng nhau thì số nhỏ hơn). Dừng khi vừa sinh `eos` hoặc đã có `max_len` token.
2. **Beam search** với độ rộng $B$. Bắt đầu với một ứng viên rỗng. Lặp tối đa `max_len` bước: mở rộng mọi ứng viên đang sống bằng mọi token; xếp các dãy mới theo log-xác suất giảm dần (bằng nhau thì dãy nhỏ hơn theo thứ tự từ điển); giữ $B$ dãy đầu. Dãy nào kết thúc bằng `eos` chuyển sang danh sách đã xong, còn lại tiếp tục sống. Hết ứng viên sống thì dừng. Kết quả là dãy có điểm lớn nhất trong danh sách đã xong; nếu danh sách ấy rỗng thì chọn trong các dãy còn sống. Bằng điểm thì dãy nhỏ hơn.
3. **Vét cạn.** Trong mọi dãy dài từ $1$ tới `max_len` token, kết thúc bằng `eos` và không có `eos` ở giữa, chọn dãy có điểm lớn nhất (bằng điểm thì dãy nhỏ hơn).

## Dữ liệu vào

Một đối tượng JSON gồm `probs`, `bos`, `eos`, `max_len`, `beam_widths` và `length_penalty`.

## Kết quả

Một đối tượng JSON gồm:

- `greedy`: `{"tokens", "logprob"}`.
- `beam`: với mỗi độ rộng (khóa là chuỗi, như `"2"`) là `{"tokens", "logprob", "score"}`.
- `exhaustive`: `{"tokens", "logprob", "score"}`.

`tokens` không gồm `bos`.

## Giới hạn

- Không quá $5$ token, `max_len` $\le5$. Những so sánh quyết định kết quả không có hai giá trị sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "probs": [
    [0.0001, 0.5, 0.45, 0.0499],
    [0.0001, 0.34, 0.36, 0.2999],
    [0.0001, 0.02, 0.0299, 0.95],
    [0.25, 0.25, 0.25, 0.25]
  ],
  "bos": 0,
  "eos": 3,
  "max_len": 3,
  "beam_widths": [1, 2],
  "length_penalty": 0.0
}
```

```output
{
  "greedy": {"tokens": [1, 2, 3], "logprob": -1.7660917224794774},
  "beam": {
    "1": {
      "tokens": [1, 2, 3],
      "logprob": -1.7660917224794774,
      "score": -1.7660917224794774
    },
    "2": {
      "tokens": [2, 3],
      "logprob": -0.8498009906053222,
      "score": -0.8498009906053222
    }
  },
  "exhaustive": {
    "tokens": [2, 3],
    "logprob": -0.8498009906053222,
    "score": -0.8498009906053222
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
