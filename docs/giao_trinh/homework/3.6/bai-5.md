# BatchNorm tự viết

Một bạn tự viết BatchNorm như sau (đã bỏ $\gamma$, $\beta$ cho gọn):

```python
class BatchNorm1d(nn.Module):
    def forward(self, x):
        if self.training:
            mean = x.mean(dim=0)
            var = x.var(dim=0, unbiased=False)
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * mean
            self.running_var = (1 - self.momentum) * self.running_var + self.momentum * var
            return (x - mean) / torch.sqrt(var + self.eps)
        return (x - self.running_mean) / torch.sqrt(self.running_var + self.eps)
```

Ban đầu `running_mean` bằng $0$ và `running_var` bằng $1$. Khi học, kết quả giống hệt `nn.BatchNorm1d`; khi suy luận thì lại khác. Lý do: `nn.BatchNorm1d` cập nhật `running_var` bằng phương sai batch chia cho $n-1$, còn đoạn code trên chia cho $n$.

Hãy chạy cả hai phiên bản, `custom` là đoạn code trên và `torch` là cách của `nn.BatchNorm1d`, với cùng `momentum` và `eps`:

1. Cho lần lượt các batch trong `batches` đi qua ở chế độ học.
2. Chuyển sang chế độ suy luận, chuẩn hóa các hàng trong `queries`.

## Dữ liệu vào

Một đối tượng JSON gồm `batches` (mỗi batch có ít nhất hai hàng, mọi hàng cùng số cột), `queries`, `momentum` và `eps`.

## Kết quả

Một đối tượng JSON gồm `custom` và `torch`, mỗi trường là `{"running_mean": [...], "running_var": [...], "eval": [...]}`, cùng `max_eval_gap` là độ lệch tuyệt đối lớn nhất giữa hai bảng `eval`.

## Giới hạn

- Không quá $6$ batch, mỗi batch không quá $16$ hàng, không quá $3$ cột.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "batches": [
    [[1.0, 10.0], [3.0, 14.0]],
    [[2.0, 9.0], [4.0, 13.0]],
    [[0.0, 11.0], [2.0, 15.0]]
  ],
  "queries": [[2.0, 12.0], [5.0, 8.0]],
  "momentum": 0.3,
  "eps": 1e-05
}
```

```output
{
  "custom": {
    "running_mean": [1.2239999999999998, 7.973999999999998],
    "running_var": [1.0, 2.9709999999999996],
    "eval": [
      [0.7759961200291, 2.3357250247861696],
      [3.775981120141599, 0.015084165584809755]
    ]
  },
  "torch": {
    "running_mean": [1.2239999999999998, 7.973999999999998],
    "running_var": [1.6569999999999996, 5.598999999999999],
    "eval": [
      [0.6028359681696035, 1.7014459170819287],
      [2.933387391505699, 0.01098797661304829]
    ]
  },
  "max_eval_gap": 0.8425937286359
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 9](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=13).
:::
