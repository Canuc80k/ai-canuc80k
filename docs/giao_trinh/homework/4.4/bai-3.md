# Adapter nhỏ

Gắn LoRA vào encoder của model nhỏ, rồi học để phân biệt chữ số $6$ và $9$. Encoder gốc giữ nguyên; chỉ adapter và head mới được học.

1. Encoder lấy từ `assets/pretrained.pt`, đóng băng. Trọng số hiệu dụng của nó là $W_e+2\,BA$, rồi $h=\operatorname{ReLU}\big((W_e+2BA)\,x/16+b_e\big)$.
2. Adapter hạng $4$: gọi `torch.manual_seed(42)` rồi tạo $A$ = `torch.randn(4, 64) * 0.01`; $B$ cỡ $32\times4$ bằng $0$. Hệ số $2$ là $\alpha/r$ với $\alpha=8$, $r=4$.
3. Head mới `Linear(32, 2)` có trọng số và bias bằng $0$. Mọi thứ kiểu `float64`.
4. `Adam(lr=0.02)` trên $A$, $B$ và head; $300$ bước, mỗi bước dùng toàn bộ train, loss `CrossEntropyLoss` trung bình.
5. Dự đoán nhãn cho test.

Mô hình chỉ học $4\cdot64+32\cdot4=384$ số của adapter và $66$ số của head.

## Dữ liệu vào

Mỗi thư mục test có `train.csv` (cột `p0` tới `p63` và `label`) và `test.csv` (cột `p0` tới `p63`). Model nằm ở `assets/` trong bộ kit.

## Kết quả

Một đối tượng JSON `{"predictions": [...]}`, theo thứ tự hàng của test.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Một test được điểm khi accuracy từ $0.85$ trở lên.

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
