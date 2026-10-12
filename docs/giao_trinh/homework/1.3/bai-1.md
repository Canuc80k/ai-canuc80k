# Stratify

Tệp `rows.csv` có $135$ bông hoa Iris, mỗi loài $45$ bông. Hãy chia chúng thành ba phần `train`, `valid`, `test` sao cho mỗi loài có $27$ bông ở train, $9$ bông ở valid và $9$ bông ở test. Như vậy tỉ lệ các loài ở phần nào cũng giống hệt toàn bộ dữ liệu. Có rất nhiều cách chia đúng, cách nào cũng được.

Gợi ý: gọi `train_test_split(..., stratify=...)` hai lần, lần đầu tách $60\%$ làm train, lần sau chia đôi phần còn lại. Ở lần thứ hai, `stratify` là nhãn của phần còn lại. Chia trên mảng chỉ số `np.arange(len(rows))` thì biết ngay hàng nào đi đâu.

## Dữ liệu vào

Mỗi thư mục test có `rows.csv` gồm `row_id`, bốn số đo và `label`.

## Kết quả

Một đối tượng JSON `{"assignment": [...]}` gồm $135$ chuỗi `"train"`, `"valid"` hoặc `"test"`, theo thứ tự hàng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Hệ thống đếm số bông của từng loài trong từng phần.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
