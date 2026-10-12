# Mã băm tệp nộp

Chạy lại toàn bộ pipeline ở một môi trường trống, ta muốn biết tệp nộp tạo ra có **giống hệt** lần trước không. So hai tệp bằng mã băm SHA-256 nhanh và chắc hơn so bằng mắt. Nhưng hai tệp chỉ khác cách xuống dòng (`\r\n` trên Windows, `\n` trên Linux) cũng cho mã băm khác, nên trước khi băm cần chuẩn hóa.

Với mỗi tệp trong `files`:

1. Đổi mọi `\r\n` và `\r` thành `\n`; nếu tệp không kết thúc bằng `\n` thì thêm một `\n`.
2. Mã hóa UTF-8, tính SHA-256, viết dạng 64 chữ số hex thường.

Báo các mã băm, tệp nào giống tệp đầu tiên, và các nhóm tệp giống nhau (chỉ số tệp từ $0$, theo thứ tự xuất hiện đầu tiên của mỗi nhóm).

## Dữ liệu vào

Một đối tượng JSON gồm `files` (các chuỗi nội dung tệp).

## Kết quả

Một đối tượng JSON gồm `sha256`, `same_as_first` và `groups`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "files": [
    "id,label\n0,1\n1,0\n", "id,label\n0,1\n1,0",
    "id,label\n0,1\n1,1\n", "index,id,label\n0,1\n1,0\n",
    "id,label\n0,1\n1,0"
  ]
}
```

```output
{
  "sha256": [
    "1e11f41f95817abf00969b1766f273e6f9c19477847d6afafc333425a8f50146",
    "1e11f41f95817abf00969b1766f273e6f9c19477847d6afafc333425a8f50146",
    "827adda4c14faa43baac73c359844f4fd1a0482dc31070bf7733fa5546ba5c2f",
    "48ff4ff86b285afdb3c3b3c04c42de68cbcff67037538e325bc2f724023f9ab4",
    "1e11f41f95817abf00969b1766f273e6f9c19477847d6afafc333425a8f50146"
  ],
  "same_as_first": [true, true, false, false, true],
  "groups": [[0, 1, 4], [2], [3]]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
