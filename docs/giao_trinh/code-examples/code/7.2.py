# -*- coding: utf-8 -*-
# Code mẫu — Audio classification

# Ví dụ 1: Lấy trung bình có giữ được thứ tự thấp rồi cao không?
import numpy as np

clip_a = np.array([[4.0, 0.0], [0.0, 4.0]])
clip_b = np.array([[0.0, 4.0], [4.0, 0.0]])
pooled_a = clip_a.mean(axis=1)
pooled_b = clip_b.mean(axis=1)
assert np.array_equal(pooled_a, pooled_b)

print("mean A:", pooled_a)
print("mean B:", pooled_b)
print("flatten A:", clip_a.ravel())
print("flatten B:", clip_b.ravel())


# Ví dụ 2: Chia 24 đoạn cắt mà không để lẫn bản ghi gốc
import numpy as np
from sklearn.model_selection import train_test_split, GroupShuffleSplit

recording_ids = np.repeat(np.arange(8), 3)
crop_ids = np.arange(len(recording_ids))
row_train, row_valid = train_test_split(crop_ids, test_size=0.25, random_state=7)
splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=7)
group_train, group_valid = next(splitter.split(crop_ids, groups=recording_ids))

def shared_recordings(train, valid):
    return sorted(set(recording_ids[train].tolist()) & set(recording_ids[valid].tolist()))

assert not shared_recordings(group_train, group_valid)
assert set(group_train) | set(group_valid) == set(crop_ids)
print("chia crop, recording chung:", shared_recordings(row_train, row_valid))
print("chia group, recording chung:", shared_recordings(group_train, group_valid))
print("so crop train/valid:", len(group_train), len(group_valid))
print("recording validation:", sorted(set(recording_ids[group_valid].tolist())))


# Ví dụ 3: Phân loại âm thanh theo thứ tự đầu và cuối
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

rng = np.random.default_rng(72)
sample_rate, window_size = 1024, 128
half_time = np.arange(512) / sample_rate
frequencies = np.fft.rfftfreq(window_size, d=1 / sample_rate)
band_masks = np.array([
    (frequencies >= 50) & (frequencies < 250),
    (frequencies >= 250) & (frequencies <= 500),
], dtype=float)
window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(window_size) / window_size)

def log_band_features(waveform):
    frames = waveform.reshape(8, window_size)
    spectrum = np.fft.rfft(frames * window, axis=1)
    power = (np.abs(spectrum) / window.sum()) ** 2
    return 10 * np.log10(np.maximum(band_masks @ power.T, 1e-9))

features, labels, recordings = [], [], []
for recording in range(24):
    offset = rng.uniform(-15, 15)
    for repetition in range(2):
        amplitude = rng.uniform(0.4, 0.9)
        phase = rng.uniform(0, 2 * np.pi)
        low = amplitude * np.sin(2 * np.pi * (128 + offset) * half_time + phase)
        high = amplitude * np.sin(2 * np.pi * (384 + offset) * half_time + phase)
        low += rng.normal(0, 0.04, len(low))
        high += rng.normal(0, 0.04, len(high))
        for label, halves in [(1, [low, high]), (0, [high, low])]:
            features.append(log_band_features(np.concatenate(halves)))
            labels.append(label)
            recordings.append(recording)
features = np.array(features)
labels, recordings = np.array(labels), np.array(recordings)
splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=7)
train, valid = next(splitter.split(features, labels, recordings))
assert not set(recordings[train]) & set(recordings[valid])

# Làm tròn để loại sai số cộng số thực, cho hai mean bằng nhau đúng như toán học.
pooled = np.round(features.mean(axis=2), 8)
assert np.array_equal(pooled[0::2], pooled[1::2])
representations = [("mean", pooled), ("giu thu tu", features.reshape(len(features), -1))]
print("features (clip, band, frame):", features.shape)
print("train/valid:", len(train), len(valid))
for name, representation in representations:
    # Scaler nằm trong Pipeline, nên chỉ học mean và std từ train.
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300))
    model.fit(representation[train], labels[train])
    predictions = model.predict(representation[valid])
    print(f"{name}: accuracy={accuracy_score(labels[valid], predictions):.3f}, "
          f"macro-F1={f1_score(labels[valid], predictions, average='macro', zero_division=0):.3f}")
    print(confusion_matrix(labels[valid], predictions, labels=[0, 1]))

