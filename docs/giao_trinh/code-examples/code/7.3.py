# -*- coding: utf-8 -*-
# Code mẫu — Speech recognition

# Ví dụ 1: Ký hiệu trống giữ được hai chữ giống nhau liền nhau
def ctc_collapse(path, blank="_"):
    transcript = []
    previous = None
    for token in path:
        if token != previous and token != blank:
            transcript.append(token)
        previous = token  # Nhớ cả ký hiệu trống, để phân biệt a_a với aa.
    return "".join(transcript)

paths = ["aaa", "a_a", "aa_bb_b", "___", ""]
for path in paths:
    print(f"{path!r} -> {ctc_collapse(path)!r}")

assert ctc_collapse("aa") == "a"
assert ctc_collapse("a_a") == "aa"
assert ctc_collapse("aa_bb_b") == "abb"


# Ví dụ 2: Tám đường đi cùng góp vào CTC loss
import numpy as np
import torch
from itertools import product

torch.set_num_threads(1)
probabilities = np.array([[0.6, 0.4], [0.5, 0.5], [0.4, 0.6]])

def collapse_ids(path):
    return tuple(token for i, token in enumerate(path)
                 if token != 0 and (i == 0 or token != path[i - 1]))

totals = {}
for path in product([0, 1], repeat=3):
    transcript = collapse_ids(path)
    path_probability = np.prod(probabilities[np.arange(3), path])
    totals[transcript] = totals.get(transcript, 0.0) + path_probability

# Đường ___ và đường a_a, mỗi đường có xác suất 0.12. Sáu đường còn lại đều gộp thành a.
assert np.allclose([totals[()], totals[(1,)], totals[(1, 1)]], [0.12, 0.76, 0.12])
assert np.isclose(sum(totals.values()), 1)
log_probs = torch.tensor(probabilities, dtype=torch.float64).log()[:, None, :]
criterion = torch.nn.CTCLoss(blank=0, reduction="sum")
loss = criterion(log_probs, torch.tensor([1]), torch.tensor([3]), torch.tensor([1]))
assert np.isclose(loss.item(), -np.log(0.76))
too_short = criterion(log_probs[:2], torch.tensor([1, 1]), torch.tensor([2]), torch.tensor([2]))

print(f"P(rong)={totals[()]:.2f}, P(a)={totals[(1,)]:.2f}, P(aa)={totals[(1, 1)]:.2f}")
print("log_probs (frame, batch, class):", tuple(log_probs.shape))
print(f"CTCLoss = {loss.item():.4f}")
print("target aa chi co 2 frame, loss vo han:", torch.isinf(too_short).item())


# Ví dụ 3: WER trên cả tập, và một lần sửa sai nội dung
import numpy as np

def tokens(text):
    return text.lower().split()

def edit_distance(reference, prediction):
    previous = list(range(len(prediction) + 1))
    for row, reference_token in enumerate(reference, start=1):
        current = [row]
        for column, predicted_token in enumerate(prediction, start=1):
            current.append(min(
                previous[column] + 1,      # Xóa một từ của bản chuẩn.
                current[column - 1] + 1,   # Chèn một từ của bản đoán.
                previous[column - 1] + (reference_token != predicted_token),
            ))
        previous = current
    return previous[-1]

references = ["em học AI", "hôm nay lớp học cách chấm kết quả ai"]
predictions = ["em học", "hôm nay lớp học cách chấm kết quả ai"]
counts = [edit_distance(tokens(r), tokens(p)) for r, p in zip(references, predictions)]
lengths = [len(tokens(r)) for r in references]
assert counts == [1, 0] and lengths == [3, 9]
assert edit_distance([], ["ai", "ai"]) == 2
assert edit_distance(["ai"], []) == 1
assert sum(lengths) > 0  # Tập rỗng cần một quy ước riêng cho metric.

print("loi/token reference:", list(zip(counts, lengths)))
print(f"corpus WER = {sum(counts) / sum(lengths):.3f}")
print(f"mean WER cau = {np.mean(np.array(counts) / lengths):.3f}")
reference = tokens("mai thi ai")
for name, prediction in [("goc", "mai thi ai"), ("sua", "mai thi toán")]:
    print(f"{name}: WER = {edit_distance(reference, tokens(prediction)) / len(reference):.3f}")
many_insertions = edit_distance(tokens("ai"), tokens("ai học thêm hôm nay"))
print(f"nhieu token chen: WER = {many_insertions / 1:.3f}")


# Ví dụ 4: Phát hiện sample rate sai trước bước tiền xử lý
import numpy as np

actual_rate = 16000
waveform = np.sin(2 * np.pi * 1000 * np.arange(1600) / actual_rate)
peak_bin = np.abs(np.fft.rfft(waveform)).argmax()

def check_audio(signal, declared_rate, expected_rate):
    if signal.ndim != 1 or not np.isfinite(signal).all():
        raise ValueError("waveform can mono va huu han")
    if declared_rate != expected_rate:
        raise ValueError("sample rate chua khop hop dong processor")
    return signal

for declared_rate in [8000, 16000]:
    grid = np.fft.rfftfreq(len(waveform), d=1 / declared_rate)
    print(f"gan nhan {declared_rate} Hz: {len(waveform) / declared_rate:.3f} s, "
          f"dinh {grid[peak_bin]:.0f} Hz")
try:
    check_audio(waveform, 8000, 16000)
except ValueError as error:
    print("preflight:", error)
checked = check_audio(waveform, actual_rate, 16000)
assert checked is waveform
print("metadata dung: preflight dat")

