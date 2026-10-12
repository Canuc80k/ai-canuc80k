# Bản vá

Gradient boosting học từng bước. Mỗi bước nhìn phần còn sai của mô hình hiện tại, rồi cộng thêm một bản vá nhỏ.

Cho nhãn thật $y$, dự đoán hiện tại $F$, bản vá `correction` mà cây mới đề xuất, và tốc độ học $\nu$. Hãy tính phần còn sai trước khi vá, $r=y-F$, dự đoán sau khi vá, $F+\nu\cdot\text{correction}$, và MSE sau khi vá.

Bản vá không nhất thiết bằng đúng $r$. Cây chỉ xấp xỉ phần còn sai, nên đừng thay `correction` bằng $r$.

## Dữ liệu vào

Mỗi tệp `input.json` gồm `y`, `F`, `correction` (cùng độ dài) và `learning_rate`.

## Kết quả

Một đối tượng JSON gồm `residual_before`, `predictions` và `mse_after`.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "y": [
    -2.0293021486634464, 0.018851207453313517, 0.7696875714199833,
    -0.007219495096140607, -0.8833190069705763, 0.9206604133795265,
    0.42166265837930256, 0.2518202207969097
  ],
  "F": [
    -1.205839480798117, 1.0915953995829177, 0.22657041090575394,
    0.2491333225312491, 1.0104316642080668, 0.9448556850613351,
    0.1742191007047443, 1.5011554491020194
  ],
  "correction": [
    -1.1676333515625303, -0.7756513320610583, -0.7732788059487598,
    0.22152363295726624, -0.43395925313312006, 0.050681431721894064,
    1.6358842030375078, -3.0293669306603497
  ],
  "learning_rate": 0.05
}
```

```output
{
  "residual_before": [
    -0.8234626678653294, -1.0727441921296041, 0.5431171605142294,
    -0.2563528176273897, -1.8937506711786432, -0.024195271681808572,
    0.24744355767455825, -1.2493352283051098
  ],
  "predictions": [
    -1.2642211483762436, 1.0528128329798647, 0.18790647060831595,
    0.2602095041791124, 0.9887337015514108, 0.9473897566474299,
    0.2560133108566197, 1.3496871025690018
  ],
  "mse_after": 0.8503075370849603
}
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.json`, `02.json`, …, `20.json`. Nộp tệp ZIP ấy, chọn **Output**.
:::
