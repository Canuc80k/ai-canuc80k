# Alpha-beta

Trong trò chơi hai người, nước đi tốt là nước đi tốt **trước mọi cách đáp trả** của đối thủ, không phải nước dẫn tới chiếc lá có điểm cao nhất. Minimax tính điều ấy; alpha-beta tính cùng kết quả mà bỏ bớt những nhánh chắc chắn không ảnh hưởng.

Cây trò chơi viết dạng list lồng nhau: một số là một lá (điểm cho người chơi MAX), một list là một nút có các con theo thứ tự. Gốc là lượt của MAX; các tầng xen kẽ MAX, MIN.

1. **Minimax:** giá trị của lá là chính nó; nút MAX lấy max các con, nút MIN lấy min. Báo giá trị gốc, giá trị của từng con của gốc, và nước đi tốt nhất (chỉ số con, bằng nhau thì con đầu tiên).
2. **Alpha-beta** bắt đầu ở gốc với $\alpha=-\infty$, $\beta=+\infty$; mỗi con nhận $\alpha$, $\beta$ hiện tại của cha. Duyệt con từ trái sang phải, gọi $v$ là giá trị tốt nhất của nút tính tới lúc ấy; ở nút MAX cập nhật $\alpha=\max(\alpha,v)$, ở nút MIN cập nhật $\beta=\min(\beta,v)$, và dừng xét các con còn lại ngay khi $\alpha\ge\beta$. Đếm số lá được đánh giá.
3. **Thứ tự tốt nhất:** sắp lại con của mọi nút theo giá trị minimax của con (nút MAX: giảm dần; nút MIN: tăng dần; bằng nhau giữ thứ tự cũ), rồi chạy alpha-beta và đếm số lá.

## Dữ liệu vào

Một đối tượng JSON gồm `tree`.

## Kết quả

Một đối tượng JSON gồm `value`, `best_move`, `child_values`, `leaves_total`, `leaves_alphabeta` và `leaves_best_order`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{"tree": [[3, 12, 8], [2, 4, 6], [14, 5, 2]]}
```

```output
{
  "value": 3,
  "best_move": 0,
  "child_values": [3, 2, 2],
  "leaves_total": 9,
  "leaves_alphabeta": 7,
  "leaves_best_order": 5
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
