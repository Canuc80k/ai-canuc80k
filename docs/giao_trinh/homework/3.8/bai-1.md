# Padding

Các câu có độ dài khác nhau, muốn xếp thành một tensor thì phải chèn thêm token PAD. Mask ghi lại vị trí nào là token thật.

Mỗi câu là một list ID token dương; PAD có ID $0$. Hãy chèn PAD vào bên phải để mọi câu dài bằng câu dài nhất, **giữ nguyên thứ tự các câu**, và tạo mask: $1$ ở vị trí token thật, $0$ ở vị trí PAD.

Câu rỗng vẫn là một hàng. Nếu mọi câu đều rỗng thì mỗi hàng là một list rỗng. Token có ID $1$ (UNK, từ lạ) vẫn là token thật.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `sequences`.

## Kết quả

Một đối tượng JSON gồm `padded`, `lengths` và `mask`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"sequences": [[1, 2, 3], [], [1, 4]]}
```

```output
{
  "padded": [[1, 2, 3], [0, 0, 0], [1, 4, 0]],
  "lengths": [3, 0, 2],
  "mask": [[1, 1, 1], [0, 0, 0], [1, 1, 0]]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
