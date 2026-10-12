# Code mẫu — Kiểm tra khóa 3

Một baseline hoàn chỉnh phải đi được từ đầu vào tới một file chấm được. Dọc đường, phải kiểm model sau khi lưu và mở lại, và kiểm từng ID mẫu. Ví dụ đầu nối bước xử lý tín hiệu với bộ phân loại. Ví dụ sau chuyển sang bản chép lời, để kiểm metric và các lỗi khi xuất file.

## Ví dụ 1: Lưu một baseline âm thanh, rồi đọc lại file xác suất

Nhãn 0 là âm cao rồi xuống thấp, nhãn 1 là âm thấp rồi lên cao. Các clip tổng hợp dài 1 giây, lấy mẫu 1024 lần mỗi giây, và được chia theo phiên sinh. Đặc trưng giữ năng lượng của hai dải tần trong từng nửa clip. Ta lưu model kèm theo quy định tiền xử lý, mở lại, rồi xuất xác suất theo đúng danh sách ID, dù lúc suy luận các clip bị xếp ngược thứ tự.

```python
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

rng = np.random.default_rng(704)
sample_rate = 1024
half_time = np.arange(512) / sample_rate
frequencies = np.fft.rfftfreq(512, d=1 / sample_rate)
band_masks = np.array([
    (frequencies >= 80) & (frequencies < 220),
    (frequencies >= 300) & (frequencies < 460),
], dtype=float)
window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(512) / 512)

def extract_features(waveform, rate):
    if rate != sample_rate or waveform.shape != (1024,):
        raise ValueError("can clip mono 1024 mau o 1024 Hz")
    frames = waveform.reshape(2, 512)
    spectrum = np.fft.rfft(frames * window, axis=1)
    power = (np.abs(spectrum) / window.sum()) ** 2
    return (10 * np.log10(np.maximum(band_masks @ power.T, 1e-9))).ravel()

waveforms, labels, recordings = [], [], []
for recording in range(16):
    offset = rng.uniform(-20, 20)
    low = np.sin(2 * np.pi * (128 + offset) * half_time)
    high = np.sin(2 * np.pi * (384 + offset) * half_time)
    low += rng.normal(0, 0.05, 512)
    high += rng.normal(0, 0.05, 512)
    for label, halves in [(0, [high, low]), (1, [low, high])]:
        waveforms.append(np.concatenate(halves))
        labels.append(label)
        recordings.append(recording)
waveforms, labels, recordings = np.array(waveforms), np.array(labels), np.array(recordings)
features = np.array([extract_features(w, sample_rate) for w in waveforms])
splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=7)
train, valid = next(splitter.split(features, labels, recordings))
assert not set(recordings[train]) & set(recordings[valid])
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300))
model.fit(features[train], labels[train])
print("features:", features.shape)
print("train/valid:", len(train), len(valid))
print("thu tu lop:", model.classes_.tolist())
```

```output
features: (32, 4)
train/valid: 24 8
thu tu lop: [0, 1]
```

Có 32 clip, mỗi clip bốn đặc trưng: hai dải tần nhân hai nửa. Validation giữ tám clip từ bốn phiên không có mặt trong train. Hàm trích đặc trưng tự kiểm sample rate và độ dài, nên một clip sai quy định sẽ bị chặn ngay.

Cột xác suất của model theo thứ tự lớp `[0, 1]`. Khi ghi file, tên cột phải theo đúng thứ tự này. Đặt tên cột ngược mà không đổi dữ liệu, file vẫn đúng shape, nhưng sai nghĩa.

```python
import csv
import joblib
from pathlib import Path
from tempfile import TemporaryDirectory

manifest_ids = [f"clip-{index:03d}" for index in valid]
original_p = model.predict_proba(features[valid])
contract = {
    "sample_rate": sample_rate,
    "num_samples": 1024,
    "frame_samples": 512,
    "bands_hz": [[80, 220], [300, 460]],
    "log_floor": 1e-9,
    "class_names": ["ket_thuc", "bat_dau"],
}
with TemporaryDirectory(prefix="kt4-audio-") as directory:
    checkpoint = Path(directory) / "baseline.joblib"
    joblib.dump({"model": model, "contract": contract}, checkpoint)
    model = None
    loaded = joblib.load(checkpoint)  # Chỉ nạp file do chính ví dụ này vừa tạo.
    assert loaded["contract"] == contract
    assert np.array_equal(loaded["model"].classes_, [0, 1])

    batch_indices = valid[::-1]
    reloaded_features = np.array([extract_features(waveforms[i], loaded["contract"]["sample_rate"])
                                 for i in batch_indices])
    batch_p = loaded["model"].predict_proba(reloaded_features)
    probability_by_id = {f"clip-{i:03d}": p for i, p in zip(batch_indices, batch_p)}
    assert len(manifest_ids) == len(set(manifest_ids))
    assert set(probability_by_id) == set(manifest_ids)
    ordered_p = np.array([probability_by_id[sample_id] for sample_id in manifest_ids])
    assert np.allclose(ordered_p, original_p)

    submission = Path(directory) / "submission.csv"
    with submission.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "p_ket_thuc", "p_bat_dau"])
        for sample_id, probabilities in zip(manifest_ids, ordered_p):
            writer.writerow([sample_id, *(f"{p:.6f}" for p in probabilities)])
    with submission.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

assert [row["id"] for row in rows] == manifest_ids
file_p = np.array([[float(row["p_ket_thuc"]), float(row["p_bat_dau"])] for row in rows])
assert file_p.shape == (len(valid), 2)
assert np.isfinite(file_p).all() and np.all((file_p >= 0) & (file_p <= 1))
assert np.allclose(file_p.sum(axis=1), 1, atol=1e-6)
assert np.allclose(file_p, original_p, atol=5e-7)
predictions = file_p.argmax(axis=1)
print("nap lai giu predictions:", np.array_equal(predictions, original_p.argmax(axis=1)))
print("ba ID dau:", manifest_ids[:3])
print(f"accuracy file = {accuracy_score(labels[valid], predictions):.3f}")
print(f"macro-F1 file = {f1_score(labels[valid], predictions, average='macro'):.3f}")
print("ID, shape, xac suat: PASS")
```

```output
nap lai giu predictions: True
ba ID dau: ['clip-004', 'clip-005', 'clip-010']
accuracy file = 1.000
macro-F1 file = 1.000
ID, shape, xac suat: PASS
```

Gói lưu chứa model và một bảng quy định: sample rate, độ dài clip, độ dài frame, các dải tần, mức sàn của log, và tên lớp. Sau khi lưu, biến `model` cũ bị xóa, để chắc chắn mọi dự đoán phía sau đều đi từ bản đã mở lại.

Lúc suy luận, các clip được xếp ngược. Ta gom kết quả vào một từ điển theo ID, rồi lấy ra theo đúng thứ tự trong danh sách gốc, nên file vẫn đúng thứ tự. File CSV được đọc lại và kiểm: ID khớp danh sách, xác suất nằm trong khoảng 0 tới 1, mỗi hàng cộng lại bằng 1, và khớp với xác suất ban đầu. Accuracy và macro-F1 tính từ chính file đều bằng 1.

Đây là điểm trên sóng sin tổng hợp, với model vừa train trên CPU. File joblib chỉ nên mở lại trong môi trường có phiên bản thư viện tương thích. Và chỉ mở file joblib từ nguồn đáng tin, vì mở file joblib lạ có thể chạy mã độc.

## Ví dụ 2: Bản chép lời đúng ID, và phải chấm bằng metric của nhận dạng giọng nói

Ba bản chép lời được đặt bằng tay, với bản chuẩn dài ngắn khác nhau. File kết quả trả các hàng theo thứ tự `c, a, b`. Bộ chấm phải ghép theo ID, rồi cộng số lỗi và số từ trên cả tập. Ta cũng thử một file có ID trùng, để thấy lỗi ấy phải bị chặn trước khi báo WER.

```python
def align_rows(rows, expected_ids):
    received_ids = [sample_id for sample_id, _ in rows]
    if len(received_ids) != len(set(received_ids)):
        raise ValueError("ID prediction bi trung")
    if len(expected_ids) != len(set(expected_ids)) or set(received_ids) != set(expected_ids):
        raise ValueError("ID prediction thieu hoac thua")
    by_id = dict(rows)
    return [by_id[sample_id] for sample_id in expected_ids]

def token_errors(reference, prediction):
    left, right = reference.lower().split(), prediction.lower().split()
    previous = list(range(len(right) + 1))
    for row, token in enumerate(left, start=1):
        current = [row]
        for column, predicted_token in enumerate(right, start=1):
            current.append(min(previous[column] + 1, current[column - 1] + 1,
                               previous[column - 1] + (token != predicted_token)))
        previous = current
    return previous[-1], len(left)

expected_ids = ["clip-a", "clip-b", "clip-c"]
references = ["em học ai", "mai lớp học lập trình thi đấu", "mai thi"]
rows = [("clip-c", "mai"), ("clip-a", "em học"), ("clip-b", "mai lớp học lập trình thi đấu")]
transcripts = align_rows(rows, expected_ids)
counts = [token_errors(r, p) for r, p in zip(references, transcripts)]
assert counts == [(1, 3), (0, 7), (1, 2)]
total_errors = sum(errors for errors, _ in counts)
total_tokens = sum(length for _, length in counts)
assert total_tokens > 0
print("loi/token:", counts)
print(f"corpus WER = {total_errors / total_tokens:.3f}")
print(f"mean WER cau = {sum(e / n for e, n in counts) / len(counts):.3f}")
print("cau dung hoan toan:", sum(e == 0 for e, _ in counts), "/", len(counts))
try:
    align_rows(rows + [("clip-a", "em học ai")], expected_ids)
except ValueError as error:
    print("file loi:", error)
```

```output
loi/token: [(1, 3), (0, 7), (1, 2)]
corpus WER = 0.167
mean WER cau = 0.278
cau dung hoan toan: 1 / 3
file loi: ID prediction bi trung
```

Cả tập có 2 lỗi trên 12 từ, nên WER trên cả tập là 0.167. Lấy trung bình WER của ba câu thì ra 0.278, vì câu ngắn “mai thi” sai một từ đã chiếm tới 50% WER của riêng nó. Hai cách tính trả lời hai câu hỏi khác nhau. Tỉ lệ câu đúng hoàn toàn chỉ là một trên ba, và cũng không thay được WER.

File có ID trùng bị từ chối ngay. Nếu không kiểm, từ điển trong Python sẽ lặng lẽ giữ bản sau và xóa bản trước, và ta không bao giờ biết. Nguyên tắc ghép theo ID và chặn ID trùng hay thiếu áp dụng cho mọi loại file kết quả, dù là nhãn phân loại, box, hay mask.
