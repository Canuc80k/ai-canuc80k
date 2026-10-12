# Phương sai rừng

Bagging giảm phương sai. Nhưng giảm được bao nhiêu còn tùy các cây giống nhau đến đâu. Nếu mỗi cây có phương sai $\sigma^2$ và mỗi cặp cây có hệ số tương quan $\rho$, thì trung bình của $B$ cây có phương sai

$$
\rho\,\sigma^2+\frac{1-\rho}{B}\,\sigma^2 .
$$

Khi $B$ rất lớn, phần thứ hai biến mất, chỉ còn $\rho\sigma^2$. Thêm cây không bao giờ đẩy phương sai xuống thấp hơn mức ấy.

Random forest giảm $\rho$ bằng cách cho mỗi lần chia chỉ xét một phần feature. Đổi lại, từng cây yếu hơn nên $\sigma^2$ tăng. Cho vài cấu hình, mỗi cấu hình có $\rho$ và $\sigma^2$ riêng. Với mỗi số cây $B$ trong danh sách, hãy tính phương sai của từng cấu hình và cho biết cấu hình nào tốt nhất. Hòa thì chọn cấu hình đứng trước.

## Dữ liệu vào

Một đối tượng JSON gồm `options` (mỗi cấu hình có `name`, `rho`, `sigma2`) và `trees` (các giá trị $B$, tăng dần).

## Kết quả

Một đối tượng JSON gồm:

- `variance`: với mỗi cấu hình, list phương sai theo thứ tự `trees`.
- `limit`: với mỗi cấu hình, phương sai khi $B$ rất lớn.
- `best`: với mỗi $B$, tên cấu hình tốt nhất.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "options": [
    {"name": "moi_feature", "rho": 0.6, "sigma2": 1.0},
    {"name": "mot_nua_feature", "rho": 0.3, "sigma2": 1.2},
    {"name": "mot_feature", "rho": 0.1, "sigma2": 2.0}
  ],
  "trees": [1, 5, 50, 500]
}
```

```output
{
  "variance": [
    [1.0, 0.68, 0.608, 0.6008],
    [1.2, 0.528, 0.3768, 0.36168],
    [2.0, 0.56, 0.236, 0.2036]
  ],
  "limit": [0.6, 0.36, 0.2],
  "best": ["moi_feature", "mot_nua_feature", "mot_feature", "mot_feature"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 165](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=61).
:::
