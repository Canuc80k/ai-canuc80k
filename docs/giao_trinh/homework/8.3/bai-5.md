# Lọc mềm

Hệ thống thật không phải lúc nào cũng trả lời đúng: người chấm có thể nhầm, hay biểu diễn của judge hơi khác biểu diễn public. Lọc **cứng** (bỏ ngay mọi ứng viên trái với một câu trả lời) sẽ loại luôn vật bí mật khi gặp một câu trả lời sai. Lọc **mềm** chỉ đếm số lần trái, và chỉ loại khi số lần trái vượt ngưỡng.

Ở bài này, câu trả lời đúng theo embedding public, trừ các câu hỏi thứ $k$ (đếm từ $1$ trong mỗi ván) nằm trong `flip_at` của ván ấy: những câu đó bị lật (`"a"` thành `"b"` và ngược lại).

**Lọc cứng:** như người chơi minimax ở bài D (chọn cặp như bài C trên tập hiện tại, lọc như bài B), tối đa `budget` câu. Cuối cùng, nếu còn đúng một ứng viên thì đoán nó; nếu không thì đoán `null`.

**Lọc mềm:** mỗi vật có một bộ đếm số lần trái, ban đầu $0$. Mỗi lượt (tối đa `budget` lượt): tập hiện tại là các vật có số lần trái không vượt `tolerance`; nếu tập ấy còn không quá một vật thì dừng; ngược lại chọn cặp như bài C trên tập ấy, hỏi, và cộng $1$ vào bộ đếm của **mọi** vật trái với câu trả lời. Cuối cùng đoán vật có số lần trái ít nhất (bằng nhau thì tên nhỏ hơn).

Báo vật đoán của mỗi cách ở từng ván và tỉ lệ thắng của mỗi cách.

## Dữ liệu vào

Một đối tượng JSON gồm `public`, `budget`, `tolerance` và `games` (mỗi ván là `{"secret", "flip_at"}`).

## Kết quả

Một đối tượng JSON gồm `games` (mỗi ván là `{"secret", "hard_guess", "soft_guess"}`), `hard_win_rate` và `soft_win_rate`.

## Giới hạn

- Không quá $12$ vật. Không vật nào cách đều hai vật khác.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "public": {
    "apple": [4, 8],
    "book": [-6, -3],
    "desk": [-9, 7],
    "fan": [-5, 6],
    "glass": [-8, -5],
    "hat": [-2, 2],
    "ink": [-9, -7],
    "lamp": [-8, -8]
  },
  "budget": 13,
  "tolerance": 2,
  "games": [
    {"secret": "desk", "flip_at": [3]},
    {"secret": "fan", "flip_at": [3]},
    {"secret": "lamp", "flip_at": [3, 6]}
  ]
}
```

```output
{
  "games": [
    {"secret": "desk", "hard_guess": "fan", "soft_guess": "desk"},
    {"secret": "fan", "hard_guess": "desk", "soft_guess": "fan"},
    {"secret": "lamp", "hard_guess": "ink", "soft_guess": "lamp"}
  ],
  "hard_win_rate": 0.0,
  "soft_win_rate": 1.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
