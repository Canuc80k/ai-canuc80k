# Hai người chơi

Ghép các mảnh ở bài A, B, C thành một người chơi hoàn chỉnh, rồi so với một người chơi đơn giản hơn trên nhiều ván. Ở bài này câu trả lời luôn đúng theo embedding public (judge dùng chính embedding ấy).

**Người chơi minimax.** Bắt đầu với tập ứng viên là cả danh mục. Chừng nào còn hơn một ứng viên và chưa hết `budget` câu hỏi: chọn cặp như bài C, hỏi, lọc như bài B. Cuối cùng đoán ứng viên nhỏ nhất (theo thứ tự chuỗi) còn lại.

**Người chơi đấu loại.** Xếp danh mục theo thứ tự chuỗi; "nhà vô địch" là vật đầu tiên. Lần lượt với mỗi vật tiếp theo, nếu còn ngân sách thì hỏi (nhà vô địch, vật ấy); trả lời `"b"` thì vật ấy thành nhà vô địch mới. Hết danh mục hoặc hết ngân sách thì đoán nhà vô địch.

Với mỗi người chơi và mỗi vật bí mật trong `secrets`, báo vật đoán, số câu đã hỏi và có đoán đúng không; rồi tỉ lệ thắng và số câu hỏi trung bình (tính cả ván thua).

## Dữ liệu vào

Một đối tượng JSON gồm `public`, `budget` và `secrets`.

## Kết quả

Một đối tượng JSON gồm `minimax` và `tournament`, mỗi cái là `{"games", "win_rate", "mean_queries"}`; mỗi ván là `{"secret", "guess", "queries", "win"}`.

## Giới hạn

- Không quá $12$ vật. Không vật nào cách đều hai vật khác.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "public": {
    "apple": [0, 8],
    "chair": [-3, -7],
    "egg": [-7, 6],
    "fan": [8, 8],
    "hat": [0, -2],
    "ink": [7, -8],
    "jar": [-6, -5]
  },
  "budget": 8,
  "secrets": ["fan", "ink", "egg", "jar"]
}
```

```output
{
  "minimax": {
    "games": [
      {"secret": "fan", "guess": "fan", "queries": 3, "win": true},
      {"secret": "ink", "guess": "ink", "queries": 3, "win": true},
      {"secret": "egg", "guess": "egg", "queries": 2, "win": true},
      {"secret": "jar", "guess": "jar", "queries": 3, "win": true}
    ],
    "win_rate": 1.0,
    "mean_queries": 2.75
  },
  "tournament": {
    "games": [
      {"secret": "fan", "guess": "fan", "queries": 6, "win": true},
      {"secret": "ink", "guess": "ink", "queries": 6, "win": true},
      {"secret": "egg", "guess": "egg", "queries": 6, "win": true},
      {"secret": "jar", "guess": "jar", "queries": 6, "win": true}
    ],
    "win_rate": 1.0,
    "mean_queries": 6.0
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
