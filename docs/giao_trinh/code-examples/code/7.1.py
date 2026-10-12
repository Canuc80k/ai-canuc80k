# -*- coding: utf-8 -*-
# Code mẫu — Dữ liệu âm thanh

# Ví dụ 1: Hai cao độ khác nhau, cùng tám mẫu
import numpy as np

sample_rate = 8
indices = np.arange(8)
times = indices / sample_rate
low = np.cos(2 * np.pi * 2 * times)
high = np.cos(2 * np.pi * 6 * times)

assert np.allclose(low, high)
print("mau:", np.round(low).astype(int))
print(f"thoi luong = {len(low) / sample_rate:.3f} s")
print(f"mau cuoi o = {times[-1]:.3f} s")
print("hai day giong nhau:", np.allclose(low, high))

# Cùng một mảng, gắn sample rate khác thì cách hiểu thời gian cũng khác.
wrong_rate = 16
print(f"gan nhan 16 Hz: {len(low) / wrong_rate:.3f} s")


# Ví dụ 2: Tìm lúc tín hiệu chuyển từ 100 Hz sang 300 Hz
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from numpy.lib.stride_tricks import sliding_window_view

sample_rate = 1000
time = np.arange(1000) / sample_rate
waveform = np.where(
    time < 0.5,
    np.sin(2 * np.pi * 100 * time),
    np.sin(2 * np.pi * 300 * time),
)
window_size, hop = 100, 50
frames = sliding_window_view(waveform, window_size)[::hop]
# Cửa sổ Hann: hai mép giảm dần về 0, để mép frame không bị gãy đột ngột khi tính FFT.
window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(window_size) / window_size)
spectrum = np.fft.rfft(frames * window, axis=1)
power = (np.abs(spectrum) / window.sum()) ** 2
frequencies = np.fft.rfftfreq(window_size, d=1 / sample_rate)
centers = (np.arange(len(frames)) * hop + window_size / 2) / sample_rate
peak_hz = frequencies[power.argmax(axis=1)]

assert power.shape == (19, 51)
assert np.array_equal(peak_hz[[0, -1]], [100, 300])
print("shape (frame, bin):", power.shape)
print("tam frame dau/cuoi:", centers[[0, -1]].round(2))
print("dinh dau/cuoi, Hz:", peak_hz[[0, -1]].astype(int))
print(f"buoc bin = {frequencies[1] - frequencies[0]:.1f} Hz")

plt.rcParams["svg.hashsalt"] = "7.1-stft-code"
plt.rcParams["font.size"] = 14
fig, ax = plt.subplots(figsize=(5.0, 3.8), layout="constrained")
db = 10 * np.log10(np.maximum(power, 1e-8) / power.max())
image = ax.pcolormesh(centers, frequencies, db.T, shading="auto", vmin=-60, vmax=0)
ax.axvline(0.5, color="white", linestyle="--", linewidth=1)
ax.set(xlabel="Thời gian (s)", ylabel="Tần số (Hz)", ylim=(0, 500))
fig.colorbar(image, ax=ax, label="dB so với đỉnh clip")
Path("fig").mkdir(exist_ok=True)
fig.savefig("fig/7.1-stft-code.svg", metadata={"Date": None})
plt.show()
plt.close(fig)


# Ví dụ 3: Gộp phổ thành log-mel, và kiểm clip im lặng
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

sample_rate, window_size, hop = 1024, 64, 32
frequencies = np.fft.rfftfreq(window_size, d=1 / sample_rate)
max_mel = 2595 * np.log10(1 + frequencies[-1] / 700)
mel_edges = np.linspace(0, max_mel, 14)  # 12 tam giác cần 14 mép.
hz_edges = 700 * (10 ** (mel_edges / 2595) - 1)
filters = []
for left, middle, right in zip(hz_edges, hz_edges[1:], hz_edges[2:]):
    rising = (frequencies - left) / (middle - left)
    falling = (right - frequencies) / (right - middle)
    filters.append(np.maximum(0, np.minimum(rising, falling)))
filters = np.array(filters)
window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(window_size) / window_size)

def log_mel(signal):
    if signal.ndim != 1 or len(signal) < window_size:
        raise ValueError("can waveform mono du dai cho mot frame")
    frames = sliding_window_view(signal, window_size)[::hop]
    spectrum = np.fft.rfft(frames * window, axis=1)
    power = (np.abs(spectrum) / window.sum()) ** 2
    mel_power = filters @ power.T  # (dải mel, mức tần số) @ (mức tần số, frame).
    return 10 * np.log10(np.maximum(mel_power, 1e-8))

time = np.arange(512) / sample_rate
waveform = np.sin(2 * np.pi * 128 * time)
features = log_mel(waveform)
quiet = log_mel(np.zeros(512))
half_amplitude = log_mel(waveform * 0.5)
strongest_band = features[:, 0].argmax()
drop_db = half_amplitude[strongest_band, 0] - features[strongest_band, 0]

# Kiểm bằng tay: 0.5 * 1 + 1 * 4 + 0.5 * 1 = 5.
assert np.dot([0.5, 1, 0.5], [1, 4, 1]) == 5
assert np.isfinite(quiet).all()
assert np.allclose(drop_db, 10 * np.log10(0.25))
print("filter/log-mel:", filters.shape, features.shape)
print("clip im lang, dB:", np.unique(quiet))
print(f"giam bien do mot nua: {drop_db:.2f} dB")
try:
    log_mel(np.zeros(10))
except ValueError as error:
    print("clip qua ngan:", error)

