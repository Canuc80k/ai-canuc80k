# Lát dữ liệu

Độ chính xác chung che mất chỗ mô hình sai. Chia dữ liệu thành từng lát (theo camera, theo điều kiện ánh sáng, …) sẽ thấy rõ hơn, nhưng lát nhỏ thì con số dao động mạnh. Bài này gắn cho mỗi lát một khoảng tin cậy để biết lát nào yếu thật, lát nào chỉ là ít mẫu.

Mỗi hàng có các cột phân lát và `correct` ($1$ nếu mô hình đoán đúng).

1. Độ chính xác chung $\bar p$ trên mọi hàng.
2. Với mỗi cột trong `slice_by`, mỗi giá trị (theo thứ tự chuỗi): số mẫu $n$, số đúng $k$, độ chính xác $\hat p=k/n$.
3. **Khoảng Wilson** với hệ số $z$: 
$$\frac{\hat p+\frac{z^2}{2n}\ \pm\ z\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}}{1+\frac{z^2}{n}}.$$
4. Kết luận: `weak` nếu cận trên nhỏ hơn $\bar p$; `strong` nếu cận dưới lớn hơn $\bar p$; còn lại `uncertain`.

## Dữ liệu vào

Một đối tượng JSON gồm `rows`, `slice_by` và `z`.

## Kết quả

Một đối tượng JSON gồm `overall` và `slices`: mỗi lát là `{"slice", "n", "accuracy", "low", "high", "verdict"}`, với `slice` viết dạng `cột=giá trị`.

## Giới hạn

- Không quá $120$ hàng. Không cận nào sát đúng $\bar p$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "rows": [
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_b", "light": "day", "correct": 0},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_b", "light": "night", "correct": 1},
    {"camera": "cam_b", "light": "night", "correct": 1},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_b", "light": "day", "correct": 0},
    {"camera": "cam_b", "light": "day", "correct": 1},
    {"camera": "cam_a", "light": "day", "correct": 0},
    {"camera": "cam_b", "light": "day", "correct": 0},
    {"camera": "cam_b", "light": "night", "correct": 0},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_a", "light": "night", "correct": 1},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_a", "light": "day", "correct": 1},
    {"camera": "cam_c", "light": "night", "correct": 1},
    {"camera": "cam_b", "light": "night", "correct": 0},
    {"camera": "cam_a", "light": "day", "correct": 1},
    {"camera": "cam_b", "light": "day", "correct": 1},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_c", "light": "day", "correct": 1},
    {"camera": "cam_b", "light": "night", "correct": 1}
  ],
  "slice_by": ["camera", "light"],
  "z": 1.645
}
```

```output
{
  "overall": 0.75,
  "slices": [
    {
      "slice": "camera=cam_a",
      "n": 4,
      "accuracy": 0.75,
      "low": 0.3561399055620657,
      "high": 0.9420993643482014,
      "verdict": "uncertain"
    },
    {
      "slice": "camera=cam_b",
      "n": 10,
      "accuracy": 0.5,
      "low": 0.26925566160142683,
      "high": 0.7307443383985732,
      "verdict": "weak"
    },
    {
      "slice": "camera=cam_c",
      "n": 10,
      "accuracy": 1.0,
      "low": 0.7870282011880192,
      "high": 1.0,
      "verdict": "strong"
    },
    {
      "slice": "light=day",
      "n": 17,
      "accuracy": 0.7647058823529411,
      "low": 0.567020532640186,
      "high": 0.8896925792126609,
      "verdict": "uncertain"
    },
    {
      "slice": "light=night",
      "n": 7,
      "accuracy": 0.7142857142857143,
      "low": 0.40864316565570713,
      "high": 0.9004432008022402,
      "verdict": "uncertain"
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
