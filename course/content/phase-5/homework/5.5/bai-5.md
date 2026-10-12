# mAP COCO

AP ở ngưỡng IoU $0.5$ chỉ hỏi detector có tìm thấy vật không; box lệch khá nhiều vẫn được tính là đúng. Bộ COCO chấm khắt khe hơn: tính AP ở mười ngưỡng IoU $0.5,0.55,\dots,0.95$ rồi lấy trung bình. Bài này so hai detector, một đặt box sát, một đặt box lỏng, theo cả hai cách chấm.

Với mỗi ngưỡng $t$, tính AP như bài C của buổi này, chỉ đổi ngưỡng $0.5$ thành $t$:

1. Xét các box dự đoán theo điểm giảm dần. Với mỗi box, tìm trong các box thật chưa ghép box có IoU lớn nhất (hòa thì box thật số nhỏ). Nếu IoU ấy ít nhất $t$, ghép hai box và ghi TP; ngược lại ghi FP.
2. Sau $k$ box đầu: precision là số TP chia $k$, recall là số TP chia số box thật.
3. Với mỗi mức recall $r=0,0.01,\dots,1$, lấy precision lớn nhất trong các vị trí có recall ít nhất $r$, hoặc $0$ nếu không có. AP là trung bình $101$ số ấy.

mAP là trung bình AP trên mười ngưỡng; AP50 và AP75 là AP ở ngưỡng $0.5$ và $0.75$.

Box viết dạng $[x_1,y_1,x_2,y_2]$ theo tọa độ liên tục: bề rộng là $x_2-x_1$.

## Dữ liệu vào

Một đối tượng JSON gồm `gt` (các box thật của một ảnh, một lớp) và `detectors`: từ tên detector tới `{"boxes", "scores"}`. Điểm của mỗi detector đôi một khác nhau.

## Kết quả

Một đối tượng JSON: với mỗi tên detector là `{"ap_by_threshold", "ap50", "ap75", "map"}`, trong đó `ap_by_threshold` gồm mười AP theo ngưỡng tăng dần.

## Giới hạn

- Không quá $5$ box thật và $8$ box dự đoán mỗi detector.
- Không IoU nào đúng bằng một ngưỡng.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "gt": [[0, 0, 10, 10], [20, 0, 30, 10], [0, 20, 10, 30]],
  "detectors": {
    "tight": {
      "boxes": [
        [0.4, 0.2, 10.3, 10.1],
        [20.2, 0.3, 30.1, 9.8],
        [0.1, 20.3, 9.6, 30.2]
      ],
      "scores": [0.9, 0.8, 0.7]
    },
    "loose": {
      "boxes": [
        [-1.1, -1.3, 11.2, 11.4],
        [18.7, -1.2, 31.6, 11.3],
        [-1.4, 18.9, 11.1, 31.5]
      ],
      "scores": [0.95, 0.85, 0.75]
    }
  }
}
```

```output
{
  "tight": {
    "ap_by_threshold": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
    "ap50": 1.0,
    "ap75": 1.0,
    "map": 0.9
  },
  "loose": {
    "ap_by_threshold": [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "ap50": 1.0,
    "ap75": 0.0,
    "map": 0.3
  }
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
