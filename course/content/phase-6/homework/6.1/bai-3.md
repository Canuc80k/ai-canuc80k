# Thư viện hay sân bóng

Phân loại câu tiếng Việt theo chủ đề: thư viện (nhãn $0$) hay thể thao (nhãn $1$). Dùng một pipeline quen thuộc của scikit-learn:

1. `TfidfVectorizer` với `preprocessor` chuẩn hóa NFC rồi đổi chữ thường, `tokenizer=str.split`, `token_pattern=None`, `ngram_range=(1, 2)`, `smooth_idf=True`, `sublinear_tf=False`, `norm="l2"`.
2. `MultinomialNB(alpha=1, fit_prior=True)`.
3. Fit trên train **một lần**, dự đoán test theo đúng thứ tự hàng.

Từ vựng và IDF chỉ được học từ train. Cột `id` chỉ là mã, không đưa vào đặc trưng. Một số câu được lưu ở dạng NFD (dấu rời), nên phải chuẩn hóa trước khi tách từ.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `id`, `text`, `label`) và `test.csv` (cột `id`, `text`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.8$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
