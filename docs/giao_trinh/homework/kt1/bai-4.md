# Nhãn bị tráo

Một mô hình phân loại $k$ lớp có loss train giảm đều, nhưng accuracy trên validation chỉ ngang đoán bừa. Một nghi phạm hay gặp: nhãn validation được mã hóa theo cách khác train. Chẳng hạn train đánh số các lớp theo thứ tự chữ cái, còn validation đánh số theo thứ tự xuất hiện. Mô hình vẫn đúng, chỉ có tên lớp bị tráo.

Để kiểm nghi phạm ấy, hãy:

1. Lập ma trận nhầm lẫn $C$ cỡ $k\times k$: $C_{a,p}$ là số mẫu có nhãn validation $a$ mà mô hình đoán $p$.
2. Tính accuracy thô, tức tỉ lệ mẫu có $p=a$.
3. Tìm cách ghép mỗi nhãn validation $a$ với đúng một nhãn của mô hình `mapping[a]`, hai nhãn khác nhau ghép với hai nhãn khác nhau, sao cho số mẫu khớp $\sum_a C_{a,\,\text{mapping}[a]}$ lớn nhất. Nếu nhiều cách cùng tốt nhất, chọn cách có danh sách `mapping` nhỏ nhất theo thứ tự từ điển.
4. Tính accuracy sau khi ghép lại.

Nếu accuracy sau khi ghép cao hẳn accuracy thô, gần như chắc chắn nhãn đã bị tráo.

## Dữ liệu vào

Một đối tượng JSON gồm `k`, `predicted` (nhãn mô hình đoán) và `actual` (nhãn validation), các nhãn từ $0$ đến $k-1$.

## Kết quả

Một đối tượng JSON gồm `confusion`, `raw_accuracy`, `mapping` và `remapped_accuracy`.

## Giới hạn

- $2\le k\le8$, có từ $1$ đến $200$ mẫu.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "k": 3,
  "predicted": [0, 0, 1, 1, 2, 2, 2, 0, 1, 2],
  "actual": [2, 2, 0, 0, 1, 1, 1, 2, 1, 0]
}
```

```output
{
  "confusion": [[0, 2, 1], [0, 1, 3], [3, 0, 0]],
  "raw_accuracy": 0.1,
  "mapping": [1, 2, 0],
  "remapped_accuracy": 0.8
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 284](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=107).
:::
