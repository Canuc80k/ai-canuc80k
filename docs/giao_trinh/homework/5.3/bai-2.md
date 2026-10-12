# Mixup

Mixup trộn hai ảnh theo tỉ lệ $\lambda$ và trộn nhãn theo đúng tỉ lệ ấy: nhãn mới là $\lambda\cdot\text{onehot}(a)+(1-\lambda)\cdot\text{onehot}(b)$, một vector xác suất chứ không còn là một lớp.

Cho logits của $n$ ảnh đã trộn (ba lớp), hai nhãn gốc $a$, $b$ của mỗi ảnh và $\lambda$. Hãy tính nhãn mềm, cross-entropy trung bình với nhãn mềm

$$
\ell=-\sum_k t_k\log\operatorname{softmax}(z)_k,
$$

và gradient của loss trung bình theo logits.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `logits`, `y_a`, `y_b` và `lambda`.

## Kết quả

Một đối tượng JSON gồm `targets`, `loss` và `gradient`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "logits": [
    [0.9941649847270383, 0.8714908410965864, 0.4778359318420114],
    [-0.20362094367134093, 0.8034539093416588, -0.10027453719883658],
    [-0.8648482046319442, -0.2130301157834983, -0.6578936361113877],
    [0.21772600459652044, 1.3850889084688136, 1.8634260914104992],
    [-1.2527331997986315, -0.4707816111094908, -0.7425036294286324]
  ],
  "y_a": [0, 2, 0, 2, 1],
  "y_b": [1, 2, 1, 2, 1],
  "lambda": 0.2
}
```

```output
{
  "targets": [
    [0.2, 0.8, 0.0],
    [0.0, 0.0, 1.0],
    [0.2, 0.8, 0.0],
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0]
  ],
  "loss": 0.955067600494378,
  "gradient": [
    [0.040604246033498895, -0.0887013648549807, 0.04809711882148181],
    [0.04126726039019249, 0.11297248708875948, -0.15423974747895197],
    [0.008204929025639223, -0.06749345797433219, 0.059288528948692965],
    [0.02128079426129736, 0.06838598404157016, -0.08966677830286754],
    [0.04122515131297075, -0.1098927950518112, 0.06866764373884046]
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
