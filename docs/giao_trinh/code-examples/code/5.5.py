# -*- coding: utf-8 -*-
# Code mẫu — Object detection

# Ví dụ 1: Hai box lệch nhau một đơn vị có IoU bao nhiêu?
import numpy as np

def iou(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if not (np.all(a[2:] > a[:2]) and np.all(b[2:] > b[:2])):
        raise ValueError("Box phải có rộng và cao dương")
    intersection = np.maximum(0, np.minimum(a[2:], b[2:]) - np.maximum(a[:2], b[:2])).prod()
    area_a, area_b = (a[2:] - a[:2]).prod(), (b[2:] - b[:2]).prod()
    return float(intersection / (area_a + area_b - intersection))

a, b = [0, 0, 4, 4], [1, 1, 5, 5]
print("IoU lệch:", round(iou(a, b), 4))
print("IoU trùng:", iou(a, a))
print("IoU chạm cạnh:", iou(a, [4, 0, 8, 4]))
assert np.isclose(iou(a, b), 9 / 23)
assert iou(a, b) == iou(b, a)
try:
    iou([2, 0, 1, 4], a)
except ValueError:
    print("Box đảo hai biên: bị từ chối")
else:
    raise AssertionError("Chưa bắt box sai")


# Ví dụ 2: NMS theo từng lớp giữ được vật thể khác lớp
import numpy as np

boxes = np.array([[0, 0, 4, 4], [0.5, 0.5, 4.5, 4.5],
                  [6, 0, 10, 4], [0, 0, 4, 4]], dtype=float)
scores = np.array([0.9, 0.8, 0.7, 0.6])
classes = np.array([0, 0, 0, 1])

def overlap(a, b):
    intersection = np.maximum(0, np.minimum(a[2:], b[2:]) - np.maximum(a[:2], b[:2])).prod()
    return intersection / ((a[2:] - a[:2]).prod() + (b[2:] - b[:2]).prod() - intersection)

def nms(boxes, scores, classes, threshold, per_class=True):
    pending = list(np.argsort(-scores, kind="stable"))
    kept = []
    while pending:
        best = pending.pop(0)
        kept.append(int(best))
        pending = [j for j in pending
                   if (per_class and classes[j] != classes[best])
                   or overlap(boxes[best], boxes[j]) <= threshold]
    return kept

print("Theo lớp:", nms(boxes, scores, classes, 0.5))
print("Trộn lớp:", nms(boxes, scores, classes, 0.5, per_class=False))
print("Ngưỡng 0.9:", nms(boxes, scores, classes, 0.9))
print("Không ứng viên:", nms(boxes[:0], scores[:0], classes[:0], 0.5))
assert nms(boxes, scores, classes, 0.5) == [0, 2, 3]
assert nms(boxes, scores, classes, 0.5, False) == [0, 2]


# Ví dụ 3: Box trùng lặp không được tính đúng lần thứ hai
import numpy as np

targets = np.array([[0, 0, 4, 4], [6, 0, 10, 4]], dtype=float)
predictions = targets[[0, 0, 1]]

def overlap(a, b):
    intersection = np.maximum(0, np.minimum(a[2:], b[2:]) - np.maximum(a[:2], b[:2])).prod()
    return intersection / ((a[2:] - a[:2]).prod() + (b[2:] - b[:2]).prod() - intersection)

matched, flags = set(), []
for box in predictions:
    candidates = [j for j in range(len(targets)) if j not in matched]
    best = max(candidates, key=lambda j: overlap(box, targets[j]), default=None)
    correct = best is not None and overlap(box, targets[best]) >= 0.5
    flags.append(int(correct))
    if correct:
        matched.add(best)
tp = np.cumsum(flags)
precision = tp / np.arange(1, len(flags) + 1)
recall = tp / len(targets)
# AP kiểu all-points: nâng precision thành đường bao không tăng, rồi cộng diện tích theo từng đoạn recall.
p = np.r_[0., precision, 0.]
r = np.r_[0., recall, 1.]
envelope = np.maximum.accumulate(p[::-1])[::-1]
ap = float(np.sum(np.diff(r) * envelope[1:]))
print("TP:", flags)
print("Precision:", precision.round(4).tolist())
print("Recall:", recall.tolist())
print("AP all-points toy:", round(ap, 4))
assert flags == [1, 0, 1]
assert np.isclose(ap, 5 / 6)

