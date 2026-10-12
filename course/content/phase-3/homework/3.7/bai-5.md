# Loss scaling

Khi huấn luyện mixed precision, gradient được nhân với một hệ số `scale` trước khi ép sang float16. Chọn `scale` quá lớn thì tràn số; quá nhỏ thì gradient bé bị làm tròn về $0$. `GradScaler` của PyTorch tự điều chỉnh `scale` theo quy tắc sau, và bài này mô phỏng đúng quy tắc ấy.

Ở mỗi bước, có một list gradient (chưa nhân). Nhân từng gradient với `scale` hiện tại rồi xét:

- **Tràn số** nếu có giá trị nào có trị tuyệt đối từ $65520$ trở lên (khi ép sang float16 nó thành vô cùng). Khi ấy bỏ qua bước cập nhật, nhân `scale` với `backoff_factor`, và đặt bộ đếm bước tốt về $0$.
- Ngược lại, bước cập nhật diễn ra. Đếm số gradient **bị mất**, tức có trị tuyệt đối sau khi nhân không quá $2^{-25}$ (khi ép sang float16 nó thành $0$). Tăng bộ đếm bước tốt thêm $1$; nếu bộ đếm bằng `growth_interval` thì nhân `scale` với `growth_factor` và đặt bộ đếm về $0$.

Hãy ghi lại `scale` dùng ở mỗi bước, bước ấy có bị bỏ qua không, số gradient bị mất ở mỗi bước (bước bị bỏ qua ghi $0$), và `scale` sau bước cuối.

## Dữ liệu vào

Một đối tượng JSON gồm `init_scale`, `growth_factor`, `backoff_factor`, `growth_interval` và `steps` (mỗi bước một list gradient khác $0$).

## Kết quả

Một đối tượng JSON gồm `scales`, `skipped`, `lost` và `final_scale`.

## Giới hạn

- Không quá $30$ bước. Không giá trị nào sau khi nhân nằm sát hai ngưỡng $65520$ và $2^{-25}$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "init_scale": 131072.0,
  "growth_factor": 2.0,
  "backoff_factor": 0.5,
  "growth_interval": 2,
  "steps": [
    [0.6, 1e-06],
    [0.6, 1e-06],
    [0.4, 1e-12],
    [0.4, 1e-12],
    [0.6, 1e-13],
    [0.3, 1e-13],
    [0.3, 2e-13],
    [0.3, 2e-13]
  ]
}
```

```output
{
  "scales": [
    131072.0, 65536.0, 65536.0, 131072.0, 131072.0, 65536.0, 65536.0,
    131072.0
  ],
  "skipped": [true, false, false, false, true, false, false, false],
  "lost": [0, 0, 0, 0, 0, 1, 1, 1],
  "final_scale": 131072.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
