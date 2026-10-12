# Groupby

Các đội rồng ghi điểm luyện tập vào tệp `training.csv`. Có buổi đội vắng mặt, ô điểm để trống. Hãy tính điểm trung bình của từng đội.

Ô trống nghĩa là không có điểm, không phải được $0$ điểm. Rất may, `mean` của pandas tự bỏ qua ô trống, nên chỉ cần `frame.groupby("team")["score"].mean()`. Đội không có điểm nào sẽ ra `NaN`. Đổi `NaN` thành `None` trước khi trả về, vì `NaN` không phải JSON hợp lệ.

Các đội xếp theo tên tăng dần, đúng thứ tự `groupby` cho sẵn. Thứ tự này so theo mã ký tự, nên đội tên bắt đầu bằng `Đ` đứng sau đội bắt đầu bằng `R`.

## Dữ liệu vào

Mỗi thư mục test có tệp `training.csv` gồm hai cột `team` và `score`.

## Kết quả

Danh sách các cặp `[tên đội, điểm trung bình]`, đội không có điểm thì trung bình là `null`.

## Giới hạn

- Có từ $5$ đến $24$ hàng, điểm là số nguyên từ $0$ đến $100$ hoặc để trống.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
training.csv:
team,score
Băng,5
Băng,97
Rồng,40
Rồng,
Đội chưa thi,
```

```output
[["Băng", 51.0], ["Rồng", 40.0], ["Đội chưa thi", null]]
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
