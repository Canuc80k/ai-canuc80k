# Giá trị lá

XGBoost chọn giá trị của lá và quyết định có nên chia nút hay không bằng gradient $g_i$ và đạo hàm bậc hai $h_i$ của loss tại từng mẫu. Với một lá chứa các mẫu có tổng $G=\sum g_i$, $H=\sum h_i$, giá trị tối ưu của lá là

$$
w^*=-\frac{G}{H+\lambda}.
$$

Khi chia một nút thành hai nhánh trái, phải, lợi ích của phép chia là

$$
\text{Gain}=\frac12\left[\frac{G_L^2}{H_L+\lambda}+\frac{G_R^2}{H_R+\lambda}-\frac{(G_L+G_R)^2}{H_L+H_R+\lambda}\right]-\gamma .
$$

Hãy tính giá trị hai lá và lợi ích của phép chia. Lợi ích âm nghĩa là phép chia không đáng với chi phí $\gamma$, cứ ghi đúng giá trị âm ấy.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `gL`, `hL`, `gR`, `hR` (gradient và đạo hàm bậc hai của các mẫu hai nhánh), `lambda` và `gamma`.

## Kết quả

Một đối tượng JSON gồm `left_value`, `right_value` và `gain`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "gL": [
    -2.0293021486634464, 0.018851207453313517, 0.7696875714199833,
    -0.007219495096140607
  ],
  "gR": [
    -0.8833190069705763, 0.9206604133795265, 0.42166265837930256,
    0.2518202207969097, -1.205839480798117
  ],
  "hL": [
    1.1809258099472473, 0.3512596018846058, 1.3318514324327548,
    0.28551328752165983
  ],
  "hR": [
    1.4469023923318087, 1.8037427220879862, 1.7326243501955256,
    1.3928173804495714, 1.877861146264592
  ],
  "lambda": 0.0,
  "gamma": 0.0
}
```

```output
{
  "left_value": 0.3962416258408614,
  "right_value": 0.059973142032510085,
  "gain": 0.1288885962795964
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
