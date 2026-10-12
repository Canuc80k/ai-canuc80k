# AdaBoost

AdaBoost giữ một trọng số cho mỗi mẫu. Sau mỗi vòng, mẫu bị đoán sai được tăng trọng số, để cây tiếp theo chú ý tới nó hơn.

Có $n$ mẫu, ban đầu mỗi mẫu có trọng số $\frac1n$. Ở vòng $t$, ta biết cây yếu đoán sai những mẫu nào. Khi ấy:

1. Sai số có trọng số $\varepsilon_t$ là tổng trọng số của các mẫu bị đoán sai.
2. Hệ số của cây là $\alpha_t=\frac12\ln\frac{1-\varepsilon_t}{\varepsilon_t}$.
3. Mẫu sai nhân trọng số với $e^{\alpha_t}$, mẫu đúng nhân với $e^{-\alpha_t}$, rồi chia cho tổng để các trọng số cộng lại bằng $1$.

Nếu ở vòng nào $\varepsilon_t=0$ (cây không sai mẫu nào) hoặc $\varepsilon_t\ge\frac12$ (cây không hơn đoán bừa), dừng ngay, không tính vòng ấy và các vòng sau.

## Dữ liệu vào

Một đối tượng JSON gồm `n` và `mistakes`, danh sách các vòng, mỗi vòng là list chỉ số các mẫu bị đoán sai.

## Kết quả

Một đối tượng JSON gồm `errors`, `alphas` (mỗi vòng đã tính một số), `weights` (trọng số sau từng vòng) và `rounds` (số vòng đã tính).

## Giới hạn

- $2\le n\le30$, không quá $8$ vòng. Không vòng nào có sai số đúng bằng $\frac12$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{"n": 6, "mistakes": [[3, 5]]}
```

```output
{
  "errors": [0.3333333333333333],
  "alphas": [0.34657359027997264],
  "weights": [[0.125, 0.125, 0.125, 0.25, 0.125, 0.25]],
  "rounds": 1
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng chung kết, câu 6](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=9).
:::
