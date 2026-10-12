# MAP@k

Tủ truyện gợi ý cho mỗi bạn một danh sách xếp hạng. Truyện bạn ấy thật sự thích nằm trong `relevant`. Gợi ý tốt là gợi ý đưa truyện được thích lên đầu. Thước đo AP@k chấm đúng điều đó.

Xét $k$ vị trí đầu của `ranking`. Mỗi lần gặp một truyện được thích **lần đầu tiên** ở vị trí $i$, ghi lại precision tại $i$, tức số truyện được thích đã gặp chia cho $i$. AP@k là tổng các precision ấy chia cho $\min(\text{số truyện được thích}, k)$. Không có truyện được thích nào thì AP bằng $0$.

Danh sách có thể lặp một truyện hai lần. Lần lặp không được tính thêm, nhưng vẫn chiếm một vị trí. Đây đúng là cách hàm `apk` trong thư viện Metrics của Ben Hamner chấm.

MAP@k là trung bình AP@k của mọi bạn. Mã truyện là chuỗi, `"002"` và `"2"` là hai truyện khác nhau.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `k` và `queries`, mỗi phần tử có `relevant` và `ranking`.

## Kết quả

Một đối tượng JSON gồm `ap` (một số cho mỗi bạn, theo thứ tự) và `map`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "k": 3,
  "queries": [
    {"relevant": ["002", "2"], "ranking": ["002", "002", "2"]},
    {"relevant": [], "ranking": ["book1", "book2"]},
    {"relevant": ["book7"], "ranking": ["book1", "book6"]},
    {
      "relevant": ["book6", "book1"],
      "ranking": ["book0", "book5", "book0"]
    }
  ],
  "duplicate_policy": "only_first_hit_but_keep_rank_position"
}
```

```output
{"ap": [0.8333333333333333, 0.0, 0.0, 0.0], "map": 0.20833333333333331}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
