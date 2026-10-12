# Float16

Số dương nhỏ nhất mà float16 biểu diễn được là $2^{-24}\approx6\cdot10^{-8}$; số nào không vượt một nửa mức ấy bị làm tròn về $0$, số lớn hơn một chút cũng chỉ còn rất ít chữ số đúng. Gradient rất nhỏ vì thế có thể mất hẳn khi huấn luyện mixed precision. Cách chữa là nhân gradient với một hệ số lớn trước khi ép kiểu, rồi chia lại sau.

Cho một list gradient khác $0$ (kiểu `float64`) và hệ số `scale` là lũy thừa của $2$. Hãy so hai cách:

- Ép thẳng: ép từng gradient sang `float16`, rồi đưa về `float64`.
- Phóng to: nhân với `scale` trong `float64`, ép sang `float16`, đưa về `float64`, rồi chia cho `scale`.

Với mỗi cách, tính sai số tương đối $|\tilde g-g|/|g|$ của từng phần tử. Đếm thêm số gradient thành $0$ khi ép thẳng.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `gradients` và `scale`.

## Kết quả

Một đối tượng JSON gồm `direct_half`, `restored`, `direct_relative_errors`, `restored_relative_errors` và `direct_zero_count`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"gradients": [1e-08, -2e-08, 5e-08, -8e-08, 1.2e-07], "scale": 65536.0}
```

```output
{
  "direct_half": [
    0.0, -0.0, 5.960464477539063e-08, -5.960464477539063e-08,
    1.1920928955078125e-07
  ],
  "restored": [
    9.997165761888027e-09, -1.9994331523776054e-08,
    5.00003807246685e-08, -7.997732609510422e-08,
    1.200241968035698e-07
  ],
  "direct_relative_errors": [
    1.0, 1.0, 0.19209289550781256, 0.2549419403076172,
    0.006589253743489495
  ],
  "restored_relative_errors": [
    0.0002834238111973018, 0.0002834238111973018,
    7.614493370101404e-06, 0.0002834238111973018,
    0.00020164002974837022
  ],
  "direct_zero_count": 2
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
