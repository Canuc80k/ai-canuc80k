# Naive Bayes đếm tay

Naive Bayes đa thức là baseline kinh điển cho phân loại văn bản, và đủ đơn giản để tính bằng tay. Bài này làm đúng các phép đếm ấy, không dùng thư viện.

Các câu đã viết không dấu, tách từ theo khoảng trắng. Nhãn là $0$ hoặc $1$.

1. Từ vựng: mọi từ xuất hiện trong train, xếp theo thứ tự chữ cái; $V$ là số từ.
2. Log-prior của lớp $c$: $\log\big(\text{số câu lớp }c\,/\,\text{số câu}\big)$.
3. Đếm $n_c(w)$ là số lần từ $w$ xuất hiện trong các câu lớp $c$, và $N_c=\sum_w n_c(w)$. Làm trơn Laplace với hệ số $\alpha$:
$$\log P(w\mid c)=\log\frac{n_c(w)+\alpha}{N_c+\alpha V}.$$
4. Điểm của một câu test cho lớp $c$: log-prior cộng $\log P(w\mid c)$ của mọi từ trong câu (từ lặp thì cộng nhiều lần). Từ không có trong từ vựng bị bỏ qua.
5. Xác suất hậu nghiệm: softmax của hai điểm. Dự đoán là lớp có điểm lớn hơn; bằng nhau thì lớp $0$.

Cuối cùng, xếp các từ theo $\log P(w\mid 1)-\log P(w\mid 0)$: `top_k` từ có giá trị lớn nhất là từ đặc trưng của lớp $1$, `top_k` từ có giá trị nhỏ nhất là từ đặc trưng của lớp $0$ (bằng nhau thì theo thứ tự chữ cái).

## Dữ liệu vào

Một đối tượng JSON gồm `train_texts`, `train_labels`, `alpha`, `top_k` và `test_texts`.

## Kết quả

Một đối tượng JSON gồm `vocab_size`, `log_prior`, `results` (với mỗi câu test là `{"scores", "probabilities", "prediction", "ignored"}`, trong đó `ignored` là số từ bị bỏ qua), `top_class1` và `top_class0`.

## Giới hạn

- Không quá $14$ câu train và $6$ câu test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "train_texts": [
    "sach doc thu vien", "doc sach truyen", "muon sach ve doc",
    "bong da san", "chay san bong", "doi bong thang"
  ],
  "train_labels": [0, 0, 0, 1, 1, 1],
  "alpha": 1.0,
  "top_k": 2,
  "test_texts": ["doc sach", "san bong doc", "thu vien moi", "banh mi"]
}
```

```output
{
  "vocab_size": 13,
  "log_prior": [-0.6931471805599452, -0.6931471805599452],
  "results": [
    {
      "scores": [-4.276666119016055, -6.8752320872765775],
      "probabilities": [0.9307692307692312, 0.06923076923076923],
      "prediction": 0,
      "ignored": 0
    },
    {
      "scores": [-8.841014310483892, -7.481367890846893],
      "probabilities": [0.2042977743668456, 0.7957022256331542],
      "prediction": 1,
      "ignored": 0
    },
    {
      "scores": [-5.662960480135946, -6.8752320872765775],
      "probabilities": [0.770700636942675, 0.2292993630573247],
      "prediction": 0,
      "ignored": 1
    },
    {
      "scores": [-0.6931471805599452, -0.6931471805599452],
      "probabilities": [0.5, 0.5],
      "prediction": 0,
      "ignored": 2
    }
  ],
  "top_class1": ["bong", "san"],
  "top_class0": ["doc", "sach"]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
