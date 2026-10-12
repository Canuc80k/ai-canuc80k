# Đếm từ

Trước khi đưa văn bản vào model, người ta hay đếm xem mỗi từ xuất hiện bao nhiêu lần. Bài này làm đúng việc ấy.

Tách văn bản thành từ bằng `text.split()`, nên dấu cách, tab hay xuống dòng đều là chỗ ngắt. Mỗi từ đưa về chữ thường bằng `lower()`, để `Mèo`, `mèo` và `MÈO` được tính là một. Rồi đếm.

Từ nào xuất hiện nhiều hơn đứng trước. Hai từ cùng số lần thì xếp theo thứ tự chuỗi của Python.

## Dữ liệu vào

Một đối tượng JSON có trường `text`, là đoạn văn bản, có thể có chữ có dấu.

## Kết quả

Danh sách các cặp `[từ, số_lần]`. Văn bản không có từ nào thì trả về `[]`.

## Giới hạn

- Văn bản dài không quá $5000$ ký tự.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"text": "Mèo chó mèo Gà mèo chó"}
```

```output
[["mèo", 3], ["chó", 2], ["gà", 1]]
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
