# Làm mới list

Viết hàm `refreshList(L)` nhận một list số nguyên và **sửa ngay trên list ấy**. Hàm bỏ mọi số nhỏ hơn hoặc bằng $0$, và ngay sau mỗi số dương $n$ còn lại thì chèn $n$ chuỗi `"A"`. Các số còn lại giữ nguyên thứ tự.

Ví dụ, `L = [2, 0, -3, 4]` trở thành `[2, "A", "A", 4, "A", "A", "A", "A"]`.

Hàm không cần trả về gì. Điều quan trọng là chỗ gọi hàm phải thấy chính list của mình đã đổi. Trong `starter.py`, hàm `solve` gọi `refreshList(data)` rồi in `data` ra.

Bẫy hay gặp là dựng list mới rồi gán `L = moi`. Lệnh ấy chỉ dời cái tên `L` sang list mới, list của chỗ gọi vẫn y nguyên. Muốn đổi nội dung list cũ, có thể dùng `L.clear()` rồi `L.extend(moi)`.

## Dữ liệu vào

Một list số nguyên.

## Kết quả

List ấy sau khi gọi `refreshList`.

## Giới hạn

- List có không quá $100$ phần tử, mỗi phần tử trong đoạn $[-20, 20]$.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
[2, 0, -3, 4]
```

```output
[2, "A", "A", 4, "A", "A", "A", "A"]
```

```input
[0, -2, -1]
```

```output
[]
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
