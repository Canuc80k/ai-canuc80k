# Thêm noise

Diffusion làm hỏng dữ liệu dần dần bằng noise. Không cần thêm noise từng bước một: có công thức nhảy thẳng từ dữ liệu sạch $x_0$ tới bước $t$.

Với lịch `betas` $=[\beta_1,\dots,\beta_T]$, đặt $\alpha_s=1-\beta_s$ và $\bar\alpha_t=\alpha_1\alpha_2\cdots\alpha_t$. Khi đó
$$x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon.$$

Hãy tính $\bar\alpha_t$ và $x_t$ với noise $\varepsilon$ cho sẵn, rồi khôi phục lại $x_0$ từ $x_t$ và $\varepsilon$ để kiểm tra.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `x0`, `epsilon` (cùng độ dài), `betas` và `t` (từ $1$).

## Kết quả

Một đối tượng JSON gồm `alpha_bar`, `xt` và `recovered_x0`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "x0": [
    1.289783100746931, -0.765081991960241, 1.4560578817097856,
    -0.8821181980482352, -0.4104847159477657
  ],
  "epsilon": [
    -1.4851507532066648, -0.5892784016791289, -0.2716929192408032,
    -0.010106959976554775, -0.47104944812554067
  ],
  "betas": [0.01, 0.02, 0.03, 0.04],
  "t": 1
}
```

```output
{
  "alpha_bar": 0.99,
  "xt": [
    1.1348029065149516, -0.8201748105248607, 1.4215900080772332,
    -0.8787072210987789, -0.45553208030486037
  ],
  "recovered_x0": [
    1.289783100746931, -0.765081991960241, 1.4560578817097856,
    -0.8821181980482352, -0.41048471594776564
  ]
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
