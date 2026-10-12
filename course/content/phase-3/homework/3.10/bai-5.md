# Autoencoder và PCA

Một autoencoder tuyến tính nén mỗi điểm hai chiều $x$ thành một số $z=e\cdot x$ rồi mở ra $\hat x=z\,w$, không có bias. Có thể học $e$ và $w$ bằng gradient descent, nhưng với mô hình tuyến tính thì đáp án tốt nhất đã biết trước: chiếu lên hướng chính đầu tiên, như PCA.

Dữ liệu không trừ trung bình. Gọi $v$ là vector đơn vị theo hướng riêng của ma trận $X^\top X$ ứng với trị riêng lớn nhất, chọn dấu sao cho thành phần đầu dương (nếu thành phần đầu bằng $0$ thì thành phần sau dương). Lấy $e=w=v$.

Hãy tính:

- `direction`: $v$.
- `pca_mse`: MSE tái tạo với $e=w=v$, tức trung bình $(\hat x-x)^2$ trên mọi ô của bảng $n\times2$.
- `candidate_mse`: MSE tái tạo của từng cặp $(e,w)$ trong `candidates`.
- `best_candidate`: chỉ số (đánh từ $0$) của cặp có MSE nhỏ nhất.
- `gaps`: với từng cặp, MSE của nó trừ `pca_mse`.

## Dữ liệu vào

Một đối tượng JSON gồm `X` (mỗi hàng hai số) và `candidates`, mỗi cặp là `{"encoder": [..], "decoder": [..]}`.

## Kết quả

Một đối tượng JSON gồm `direction`, `pca_mse`, `candidate_mse`, `best_candidate` và `gaps`.

## Giới hạn

- $2\le n\le20$, không quá $4$ cặp. Hai trị riêng của $X^\top X$ khác nhau rõ rệt, và không có hai cặp nào có MSE sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "X": [
    [2.0, 1.0],
    [-2.0, -1.0],
    [1.0, 0.4],
    [-1.0, -0.6],
    [0.0, 0.2],
    [3.0, 1.6]
  ],
  "candidates": [
    {"encoder": [1.0, 0.0], "decoder": [1.0, 0.5]},
    {"encoder": [0.4, 0.2], "decoder": [2.0, 1.0]},
    {"encoder": [0.894, 0.447], "decoder": [0.894, 0.447]}
  ]
}
```

```output
{
  "direction": [0.8882355872281191, 0.4593882253405264],
  "pca_mse": 0.004293305264280303,
  "candidate_mse": [0.005833333333333335, 0.004666666666666668, 0.004668495580800001],
  "best_candidate": 1,
  "gaps": [0.001540028069053032, 0.0003733614023863647, 0.0003751903165196977]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
