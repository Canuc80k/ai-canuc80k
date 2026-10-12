# Bản nộp trọn vẹn

Một bản nộp trọn vẹn: học, chọn checkpoint theo validation, lưu, rồi nạp lại ở tiến trình mới để dự đoán.

1. Encoder lấy từ `assets/pretrained.pt` ($h=\operatorname{ReLU}(W_e\,x/16+b_e)$), đóng băng và ở chế độ `eval`. Head mới `Linear(32, 2)` có trọng số và bias bằng $0$. Mọi thứ kiểu `float64`.
2. `Adam(lr=0.02)` cho head; $200$ bước, mỗi bước dùng toàn bộ train, loss `CrossEntropyLoss` trung bình.
3. Sau mỗi bước, tính loss trên valid. Giữ bản sao trạng thái head có loss valid nhỏ nhất (hòa thì bước sớm hơn).
4. Lưu trạng thái ấy, nạp lại bằng `torch.load(..., weights_only=True)` ở một tiến trình Python mới, rồi dự đoán test.

Nhãn $0$ là chữ số $6$, nhãn $1$ là chữ số $9$.

## Dữ liệu vào

Mỗi thư mục test có `train.csv`, `valid.csv` (cột `p0` tới `p63` và `label`) và `test.csv` (cột `p0` tới `p63`). Model nằm ở `assets/` trong bộ kit.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.85$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
