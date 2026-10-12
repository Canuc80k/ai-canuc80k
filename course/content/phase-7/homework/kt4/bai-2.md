# Thời tiết hay đi lại

Phân loại câu tiếng Việt ngắn theo chủ đề: thời tiết (nhãn $0$) hay đi lại (nhãn $1$).

1. `TfidfVectorizer` với `preprocessor` chuẩn hóa NFC rồi đổi chữ thường, `tokenizer=str.split`, `token_pattern=None`, `ngram_range=(1, 1)`, `smooth_idf=True`, `norm="l2"`.
2. `MultinomialNB(alpha=1, fit_prior=True)`.
3. Fit trên train **một lần**, dự đoán test theo đúng thứ tự hàng. Cột `id` chỉ là mã, không đưa vào đặc trưng.

## Dữ liệu vào

Mỗi thư mục test có `input.json`, `train.csv` (cột `id`, `text`, `label`) và `test.csv` (cột `id`, `text`).

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.9$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
