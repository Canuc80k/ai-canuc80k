# Avatar

Một xưởng vẽ avatar pixel có mẫu chung `template`, là một lưới số, mỗi số là một màu từ $0$ đến $4$. Từ mẫu ấy, xưởng vẽ hai avatar. Avatar thứ nhất là mẫu được tô thêm theo `edits_a`, avatar thứ hai là mẫu được tô thêm theo `edits_b`.

Mỗi lần tô là một bộ `[hàng, cột, màu]`, hàng và cột đánh số từ $0$. Ô bị tô nhiều lần thì giữ màu cuối cùng.

Tô avatar này không được làm đổi avatar kia, cũng không được làm đổi mẫu. Cẩn thận với `template.copy()`. Lệnh này chỉ chép danh sách các hàng, còn các hàng bên trong vẫn dùng chung.

## Dữ liệu vào

Một đối tượng JSON gồm `template`, `edits_a`, `edits_b`.

## Kết quả

Danh sách hai lưới `[avatar_thứ_nhất, avatar_thứ_hai]`.

## Giới hạn

- Lưới có từ $1$ đến $12$ hàng, các hàng dài bằng nhau, từ $1$ đến $12$ ô.
- Mỗi danh sách tô có không quá $50$ lần tô, mọi ô đều nằm trong lưới.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "template": [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
  ],
  "edits_a": [[1, 1, 3], [1, 3, 3]],
  "edits_b": [[3, 1, 2], [3, 2, 2], [3, 3, 2]]
}
```

```output
[
  [
    [0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0],
    [0, 0, 0, 0, 0]
  ]
]
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
