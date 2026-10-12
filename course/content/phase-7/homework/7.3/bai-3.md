# Ghép theo thời gian

Mô hình nhận dạng chỉ nghe được đoạn ngắn, nên âm thanh dài được cắt thành các khúc **chồng lên nhau**. Mỗi khúc cho các từ kèm thời điểm, tính từ đầu khúc. Ghép lại cần hai việc: đổi về thời điểm tuyệt đối, và quyết định khúc nào "sở hữu" từ nào ở vùng chồng nhau.

Mỗi khúc có `offset` (giây), `keep_interval` $[a,b)$ (giây, tuyệt đối) và các từ `{start, end, text}` (giây, tính từ đầu khúc). Các `keep_interval` không chồng nhau.

1. Cộng `offset` vào `start` và `end` của mỗi từ.
2. Giữ từ khi điểm giữa $(\text{start}+\text{end})/2$ (tuyệt đối) nằm trong $[a,b)$ của khúc chứa nó.
3. Xếp các từ giữ lại theo `start`, rồi `end`, rồi `text`.

Đừng bỏ từ chỉ vì trùng chữ: hai từ "đi" ở hai thời điểm khác nhau đều là thật.

## Dữ liệu vào

Một đối tượng JSON gồm `chunks` (không nhất thiết theo thứ tự thời gian).

## Kết quả

Một đối tượng JSON gồm `words`: list các `{"start", "end", "text"}` theo thời gian tuyệt đối.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "chunks": [
    {
      "offset": 0,
      "keep_interval": [0, 1],
      "words": [
        {"start": 0.2, "end": 0.4, "text": "đi"},
        {"start": 0.6, "end": 0.8, "text": "đi"},
        {"start": 0.9, "end": 1.1, "text": "nào"}
      ]
    },
    {
      "offset": 0.5,
      "keep_interval": [1, 2],
      "words": [
        {"start": 0.1, "end": 0.3, "text": "đi"},
        {"start": 0.4, "end": 0.6, "text": "nào"},
        {"start": 0.8, "end": 1, "text": "bạn"}
      ]
    }
  ]
}
```

```output
{
  "words": [
    {"start": 0.2, "end": 0.4, "text": "đi"},
    {"start": 0.6, "end": 0.8, "text": "đi"},
    {"start": 0.9, "end": 1.1, "text": "nào"},
    {"start": 1.3, "end": 1.5, "text": "bạn"}
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
