# Tìm bằng TF-IDF

Trước khi dùng embedding, hãy có một baseline tìm kiếm bằng từ khóa: TF-IDF. Bài này dựng chỉ mục TF-IDF trên các tài liệu tiếng Việt ngắn rồi tìm cho vài truy vấn.

1. `TfidfVectorizer` với `preprocessor` chuẩn hóa NFC rồi đổi chữ thường, `tokenizer=str.split`, `token_pattern=None`, `ngram_range=(1, 1)`, `smooth_idf=True`, `sublinear_tf=False`, `norm="l2"`.
2. Fit **chỉ trên tài liệu**. Biến đổi truy vấn bằng từ vựng và IDF đã học; từ lạ trong truy vấn bị bỏ qua.
3. Điểm là tích vô hướng của hai vector đã chuẩn hóa. Xếp tài liệu theo điểm giảm dần, bằng nhau thì theo mã (so như chuỗi); lấy $k$ tài liệu đầu. Truy vấn không có từ nào trong từ vựng cho điểm $0$ với mọi tài liệu.

Báo thêm IDF của từng từ trong từ vựng, theo thứ tự từ vựng của scikit-learn.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `doc_ids`, `documents`, `queries` và `k`.

## Kết quả

Một đối tượng JSON gồm `top_ids` (mã $k$ tài liệu đầu cho mỗi truy vấn) và `idf` (list các cặp $[\text{từ}, \text{idf}]$).

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "doc_ids": ["c", "002", "d", "2", "b", "a"],
  "documents": [
    "nhạc đàn ca hát", "đường xe đèn giao thông", "đàn nhạc vui hát",
    "xe đèn đỏ đường", "nước biển sóng", "biển sóng thuyền bến"
  ],
  "queries": ["biển thuyền", "XE ĐÈN", "đàn ca", "ngoàivocab", "sóng sóng nước"],
  "k": 1
}
```

```output
{
  "top_ids": [["a"], ["2"], ["c"], ["002"], ["b"]],
  "idf": [
    ["biển", 1.8472978603872037],
    ["bến", 2.252762968495368],
    ["ca", 2.252762968495368],
    ["giao", 2.252762968495368],
    ["hát", 1.8472978603872037],
    ["nhạc", 1.8472978603872037],
    ["nước", 2.252762968495368],
    ["sóng", 1.8472978603872037],
    ["thuyền", 2.252762968495368],
    ["thông", 2.252762968495368],
    ["vui", 2.252762968495368],
    ["xe", 1.8472978603872037],
    ["đàn", 1.8472978603872037],
    ["đèn", 1.8472978603872037],
    ["đường", 1.8472978603872037],
    ["đỏ", 2.252762968495368]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
