# Soft-thresholding

Các cột của ma trận dữ liệu trực chuẩn, $\mathbf{z}$ là vector hệ số least squares và $\lambda \ge 0$ là mức phạt, như mục Lasso của bài 2.2. Tính hệ số Ridge và Lasso tương ứng:

$$w_j^{\text{ridge}} = \frac{z_j}{1 + \lambda}, \qquad w_j^{\text{lasso}} = \operatorname{sign}(z_j)\,\max\!\left(\lvert z_j\rvert - \lambda,\ 0\right).$$

## Input

Một JSON object đọc từ stdin: `z` là list số thực có $1 \le n \le 1000$ phần tử, $\lvert z_j\rvert \le 10^6$; `lam` là số thực $\lambda$, $0 \le \lambda \le 10^6$.

## Output

Một JSON object gồm hai trường `ridge` và `lasso`, mỗi trường là list cùng độ dài với `z`. Chấp nhận sai số tuyệt đối hoặc tương đối không quá $10^{-6}$.

## Ví dụ

```input
{"z": [3, 0.5, -1.2], "lam": 1}
```

```output
{"ridge": [1.5, 0.25, -0.6], "lasso": [2.0, 0.0, -0.2]}
```

Ridge chia mỗi hệ số cho $1 + \lambda = 2$. Lasso trừ đúng 1 đơn vị độ lớn rồi cắt về 0, nên hệ số thứ hai biến mất còn hệ số thứ ba giữ dấu âm.

::: tip Gợi ý
Viết riêng hàm `soft(z, t)` như trong bài học, rồi áp dụng cho từng phần tử.
:::

## Tự kiểm tra

- Chạy đúng ví dụ mẫu.
- Thử `lam = 0`: cả Ridge và Lasso phải trả lại đúng `z`.
- Thử một $z_j$ âm có độ lớn nhỏ hơn `lam`: hệ số Lasso phải bằng 0, không đổi dấu.
