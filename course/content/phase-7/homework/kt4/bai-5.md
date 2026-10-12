# Lỗi lan truyền

Một ứng dụng nghe câu nói, chuyển thành chữ (ASR), rồi phân loại chủ đề: thời tiết (lớp $0$) hay đi lại (lớp $1$). Lỗi của bước nhận dạng có làm sai bước phân loại không? Bài này so nhãn đoán từ bản chữ chuẩn với nhãn đoán từ bản ASR.

Các câu viết không dấu, tách từ theo khoảng trắng.

1. **Bộ phân loại** Naive Bayes cho sẵn: `log_prior` (hai số) và `log_likelihood` (từ một từ tới hai số, theo lớp). Điểm của lớp $c$ là log-prior cộng log-likelihood của mọi từ trong câu có trong bảng (từ lặp thì cộng nhiều lần; từ không có trong bảng bỏ qua). Lớp có điểm lớn hơn thắng (bằng nhau thì lớp $0$).
2. Với mỗi câu: WER của bản ASR so với bản chuẩn (khoảng cách chỉnh sửa trên từ chia số từ của bản chuẩn), nhãn đoán từ bản chuẩn và nhãn đoán từ bản ASR.
3. Báo độ chính xác của hai cách đoán so với nhãn thật `label`; danh sách chỉ số (từ $0$) các câu mà hai nhãn đoán khác nhau; tỉ lệ câu đổi nhãn trong nhóm có WER lớn hơn `wer_cut` và trong nhóm còn lại.

## Dữ liệu vào

Một đối tượng JSON gồm `model`, `utterances` (mỗi câu là `{"reference", "hypothesis", "label"}`) và `wer_cut`.

## Kết quả

Một đối tượng JSON gồm `utterances` (với mỗi câu là `{"wer", "pred_reference", "pred_asr"}`), `accuracy_reference`, `accuracy_asr`, `flipped`, `flip_rate_high_wer` và `flip_rate_low_wer`.

## Giới hạn

- Không quá $12$ câu; mỗi nhóm WER có ít nhất một câu. Không câu nào có hai điểm lớp sát nhau.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Số thực được chấm với sai số khoảng $10^{-7}$.

## Ví dụ

```input
{
  "model": {
    "log_prior": [-0.693147, -0.693147],
    "log_likelihood": {
      "nang": [-1.71, -3.356],
      "mua": [-1.484, -3.795],
      "gio": [-1.994, -3.941],
      "may": [-1.7, -3.522],
      "bao": [-1.105, -2.742],
      "suong": [-1.16, -2.932],
      "xe": [-5.128, -3.394],
      "buyt": [-4.7, -2.791],
      "ga": [-5.942, -3.528],
      "tau": [-3.729, -2.105],
      "ve": [-4.588, -2.565],
      "chuyen": [-6.3, -3.75],
      "ngay": [-2.681, -2.718],
      "mai": [-3.453, -3.17],
      "toi": [-2.344, -2.136],
      "luc": [-2.223, -2.091],
      "dang": [-3.627, -3.87],
      "sap": [-3.009, -2.894],
      "rat": [-2.451, -2.175],
      "hom": [-2.353, -2.133],
      "se": [-2.971, -2.886],
      "nam": [-1.948, -2.177],
      "ca": [-2.581, -2.669]
    }
  },
  "utterances": [
    {
      "reference": "hom toi luc tau ve",
      "hypothesis": "hom toi luc tau ve",
      "label": 1
    },
    {
      "reference": "hom rat ngay luc xe",
      "hypothesis": "hom rat luc xe",
      "label": 1
    },
    {
      "reference": "tau mai dang buyt",
      "hypothesis": "tau mai dang buyt",
      "label": 1
    },
    {
      "reference": "chuyen rat ga",
      "hypothesis": "chuyen rat ga",
      "label": 1
    },
    {"reference": "gio hom", "hypothesis": "gi rat", "label": 0},
    {
      "reference": "hom bao gio toi",
      "hypothesis": "hom gio mai",
      "label": 0
    },
    {
      "reference": "ngay suong luc sap rat",
      "hypothesis": "ngay suong luc sap rat",
      "label": 0
    },
    {
      "reference": "nang dang toi",
      "hypothesis": "nam dang toi",
      "label": 0
    },
    {
      "reference": "hom chuyen sap luc ngay",
      "hypothesis": "hom chuyen luc hom",
      "label": 1
    },
    {
      "reference": "bao sap suong toi",
      "hypothesis": "bao sap mai",
      "label": 0
    },
    {"reference": "buyt hom", "hypothesis": "buyt hom", "label": 1}
  ],
  "wer_cut": 0.25
}
```

```output
{
  "utterances": [
    {"wer": 0.0, "pred_reference": 1, "pred_asr": 1},
    {"wer": 0.2, "pred_reference": 1, "pred_asr": 1},
    {"wer": 0.0, "pred_reference": 1, "pred_asr": 1},
    {"wer": 0.0, "pred_reference": 1, "pred_asr": 1},
    {"wer": 1.0, "pred_reference": 0, "pred_asr": 1},
    {"wer": 0.5, "pred_reference": 0, "pred_asr": 0},
    {"wer": 0.0, "pred_reference": 0, "pred_asr": 0},
    {"wer": 0.3333333333333333, "pred_reference": 0, "pred_asr": 0},
    {"wer": 0.4, "pred_reference": 1, "pred_asr": 1},
    {"wer": 0.5, "pred_reference": 0, "pred_asr": 0},
    {"wer": 0.0, "pred_reference": 1, "pred_asr": 1}
  ],
  "accuracy_reference": 1.0,
  "accuracy_asr": 0.9090909090909091,
  "flipped": [4],
  "flip_rate_high_wer": 0.2,
  "flip_rate_low_wer": 0.0
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::
