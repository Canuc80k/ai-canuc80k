# Nhiều seed

Huấn luyện cùng một model với nhiều seed rồi lấy trung bình là cách ensemble rẻ nhất. Nó giảm được phần lỗi do seed (phương sai), nhưng không giảm được phần lỗi mà mọi seed cùng mắc (bias). Bài này tách hai phần ấy trên một bài hồi quy.

`preds[s][i]` là dự đoán của seed $s$ cho mẫu $i$ ($S$ seed, $N$ mẫu); `targets[i]` là giá trị đúng. Gọi $\bar f_i$ là trung bình dự đoán của mọi seed ở mẫu $i$.

- `bias2`: $\frac1N\sum_i(\bar f_i-y_i)^2$.
- `variance`: $\frac1{SN}\sum_{s,i}(f_{s,i}-\bar f_i)^2$.
- `mean_single_mse`: MSE của từng seed, lấy trung bình: $\frac1{SN}\sum_{s,i}(f_{s,i}-y_i)^2$.
- Với mỗi $k$ trong `ks`: MSE của trung bình $k$ seed **đầu tiên**.

## Dữ liệu vào

Một đối tượng JSON gồm `preds`, `targets` và `ks`.

## Kết quả

Một đối tượng JSON gồm `bias2`, `variance`, `mean_single_mse` và `curve` (với mỗi $k$ là `{"k", "mse"}`).

## Giới hạn

- Không quá $8$ seed và $12$ mẫu.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "preds": [
    [
      0.766, 1.472, -1.042, 1.409, -1.731, 0.908, -0.299, -1.636,
      -0.624, -1.087, 1.243, -0.213
    ],
    [
      1.303, 0.921, -1.056, 1.262, -1.276, 0.908, -0.268, -1.421,
      -0.649, -1.993, 0.884, -0.231
    ],
    [
      0.515, 1.468, -2.206, 0.873, -0.801, 1.385, -0.908, -1.328,
      -0.804, -1.646, 1.637, 0.257
    ],
    [
      0.112, 1.617, -1.327, 1.684, -0.85, 1.082, -0.495, -1.163,
      -0.447, -1.98, 1.609, -0.16
    ],
    [
      0.342, 1.42, -1.42, 0.915, -1.16, 1.357, -0.01, -1.535, -0.728,
      -1.852, 1.95, 0.006
    ],
    [
      0.866, 1.479, -0.753, 1.519, -1.337, 1.413, -0.244, -2.35,
      -0.709, -1.835, 1.952, 0.27
    ],
    [
      1.272, 1.424, -1.592, 1.213, -1.0, 1.384, -0.415, -1.594, -0.173,
      -2.416, 1.557, 0.406
    ],
    [
      1.681, 1.264, -2.085, 1.364, -1.27, 1.494, -0.301, -1.849,
      -0.569, -1.653, 2.112, 1.006
    ]
  ],
  "targets": [
    0.9, 1.57, -1.22, 0.9, -0.83, 1.5, 0.1, -1.22, -0.54, -1.72, 1.46,
    0.37
  ],
  "ks": [1, 2, 6, 8]
}
```

```output
{
  "bias2": 0.07180003645833337,
  "variance": 0.11192183854166665,
  "mean_single_mse": 0.183721875,
  "curve": [
    {"k": 1, "mse": 0.21729749999999995},
    {"k": 2, "mse": 0.16434941666666666},
    {"k": 6, "mse": 0.08258569444444447},
    {"k": 8, "mse": 0.07180003645833337}
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
