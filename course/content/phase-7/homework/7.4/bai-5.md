# Chọn trọng số

Có hai mô hình cho cùng một bài phân loại, một nghe âm thanh, một nhìn hình. Gộp xác suất của chúng thường tốt hơn từng mô hình riêng, nhưng trọng số gộp phải chọn trên validation, không phải trên test.

Với trọng số $w$: $p=w\,p_{\text{audio}}+(1-w)\,p_{\text{image}}$.

1. Với mỗi $w$ trong `weights`, tính log-loss trên validation: trung bình của $-\log p_{\text{đúng}}$ (với $p_{\text{đúng}}$ chặn dưới ở $10^{-15}$).
2. Chọn $w$ có log-loss validation nhỏ nhất (bằng nhau thì $w$ nhỏ hơn).
3. Trên test, báo độ chính xác (dự đoán là lớp xác suất lớn nhất) và log-loss của bốn cách: chỉ âm thanh, chỉ hình, gộp đều ($w=0.5$), gộp với $w$ đã chọn.

## Dữ liệu vào

Một đối tượng JSON gồm `valid`, `test` (mỗi tập là `{"labels", "audio", "image"}`, hai bảng xác suất cùng shape) và `weights`.

## Kết quả

Một đối tượng JSON gồm `validation_log_loss` (theo thứ tự `weights`), `best_weight` và `test`: `{"audio_only", "image_only", "equal_weight", "tuned"}`, mỗi cái là `{"accuracy", "log_loss"}`.

## Giới hạn

- Không quá $24$ mẫu mỗi tập. Không có hai lớp hòa nhau ở xác suất lớn nhất, và log-loss validation nhỏ nhất là duy nhất.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "valid": {
    "labels": [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    "audio": [
      [0.845, 0.155],
      [0.216, 0.784],
      [0.353, 0.647],
      [0.172, 0.828],
      [0.757, 0.243],
      [0.133, 0.867],
      [0.13, 0.87],
      [0.224, 0.776],
      [0.163, 0.837],
      [0.173, 0.827]
    ],
    "image": [
      [0.89, 0.11],
      [0.232, 0.768],
      [0.183, 0.817],
      [0.62, 0.38],
      [0.68, 0.32],
      [0.662, 0.338],
      [0.275, 0.725],
      [0.285, 0.715],
      [0.196, 0.804],
      [0.214, 0.786]
    ]
  },
  "test": {
    "labels": [
      0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1,
      0
    ],
    "audio": [
      [0.923, 0.077],
      [0.233, 0.767],
      [0.683, 0.317],
      [0.231, 0.769],
      [0.833, 0.167],
      [0.211, 0.789],
      [0.183, 0.817],
      [0.037, 0.963],
      [0.255, 0.745],
      [0.875, 0.125],
      [0.779, 0.221],
      [0.82, 0.18],
      [0.125, 0.875],
      [0.836, 0.164],
      [0.689, 0.311],
      [0.156, 0.844],
      [0.81, 0.19],
      [0.101, 0.899],
      [0.102, 0.898],
      [0.267, 0.733],
      [0.317, 0.683],
      [0.774, 0.226],
      [0.755, 0.245]
    ],
    "image": [
      [0.081, 0.919],
      [0.101, 0.899],
      [0.873, 0.127],
      [0.2, 0.8],
      [0.778, 0.222],
      [0.688, 0.312],
      [0.372, 0.628],
      [0.04, 0.96],
      [0.329, 0.671],
      [0.808, 0.192],
      [0.76, 0.24],
      [0.767, 0.233],
      [0.623, 0.377],
      [0.872, 0.128],
      [0.698, 0.302],
      [0.253, 0.747],
      [0.244, 0.756],
      [0.384, 0.616],
      [0.157, 0.843],
      [0.246, 0.754],
      [0.251, 0.749],
      [0.087, 0.913],
      [0.782, 0.218]
    ]
  },
  "weights": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
}
```

```output
{
  "validation_log_loss": [
    0.3464362633103063, 0.34113571092798745, 0.33782143509479556,
    0.33644094838471894, 0.33704386403226994, 0.3397914629348343,
    0.34499019131252606, 0.3531652172289254, 0.36521731748625486,
    0.3827865115553891, 0.40924608142234115
  ],
  "best_weight": 0.3,
  "test": {
    "audio_only": {"accuracy": 0.8695652173913043, "log_loss": 0.3927628273265374},
    "image_only": {"accuracy": 0.9130434782608695, "log_loss": 0.38559437091838233},
    "equal_weight": {"accuracy": 0.9130434782608695, "log_loss": 0.3304300130449199},
    "tuned": {"accuracy": 0.9565217391304348, "log_loss": 0.33342500976071776}
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
