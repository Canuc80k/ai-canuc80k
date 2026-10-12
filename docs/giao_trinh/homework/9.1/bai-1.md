# Return

Robot đi một episode và nhận phần thưởng $r_0, r_1, \dots, r_{T-1}$. Một bước ở xa đích có giá trị bao nhiêu? Return của bước $t$ cộng mọi phần thưởng từ bước ấy về sau, phần thưởng càng xa càng bị chiết khấu:
$$G_t=r_t+\gamma r_{t+1}+\gamma^2 r_{t+2}+\cdots=r_t+\gamma G_{t+1},\qquad G_T=0.$$

Hãy tính $G_t$ cho mọi $t$.

## Dữ liệu vào

Một đối tượng JSON gồm `rewards` và `gamma`.

## Kết quả

Một đối tượng JSON gồm `returns` (dãy $G_0..G_{T-1}$) và `G0`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"rewards": [-1, -1, -1, 10], "gamma": 0.9}
```

```output
{"returns": [4.58, 6.2, 8.0, 10.0], "G0": 4.58}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
