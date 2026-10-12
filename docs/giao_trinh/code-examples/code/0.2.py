# -*- coding: utf-8 -*-
# Code mẫu — NumPy

# Ví dụ 1: Trung bình theo môn, theo học sinh, và theo trọng số
import numpy as np

scores = np.array([[4, 6], [6, 8], [8, 10]], dtype=np.float64)
weights = np.array([0.25, 0.75])
print("shape:", scores.shape)
print("từng môn:", scores.mean(axis=0).tolist())
print("từng học sinh:", scores.mean(axis=1).tolist())

# Phép @ nhân hai điểm với hai trọng số rồi cộng lại, ra một điểm cho mỗi hàng.
weighted_scores = scores @ weights
print("có trọng số:", weighted_scores.tolist())
assert np.allclose(weighted_scores, (scores * weights).sum(axis=1))

row_mean = scores.mean(axis=1, keepdims=True)
print("shape trung bình hàng:", row_mean.shape)
print("lệch trung bình hàng:", (scores - row_mean).tolist())


# Ví dụ 2: Chuẩn hóa dữ liệu mới bằng thống kê đã tính trên train
import numpy as np

train = np.array([[1, 10], [3, 10], [5, 10]], dtype=np.float64)
test = np.array([[7, 10], [9, 10]], dtype=np.float64)

mean = train.mean(axis=0)
std = train.std(axis=0, ddof=0)
# Cột hằng có độ lệch chuẩn bằng 0. Thay mẫu số bằng 1 để không chia cho 0.
scale = np.where(std == 0, 1.0, std)
train_z = (train - mean) / scale
test_z = (test - mean) / scale
print("mean train:", mean.tolist())
print("std train:", std.round(3).tolist())
print("train đã đổi:", train_z.round(3).tolist())
print("test dùng thống kê train:", test_z.round(3).tolist())

# Làm sai để so: tính lại thống kê trên test là đổi luôn cả thước đo.
test_std = test.std(axis=0, ddof=0)
test_scale = np.where(test_std == 0, 1.0, test_std)
test_refitted = (test - test.mean(axis=0)) / test_scale
print("test học lại thống kê:", test_refitted.round(3).tolist())
assert np.allclose(train_z.mean(axis=0), 0)
assert np.isfinite(train_z).all() and np.isfinite(test_z).all()


# Ví dụ 3: Tăng sáng ảnh mà không làm hỏng ảnh gốc
import numpy as np

raw = np.array([[240, 10], [100, 200]], dtype=np.uint8)
crop = raw[:, :1]
crop[0, 0] = 0
print("sửa view, gốc đổi:", raw.tolist())
print("dùng chung bộ nhớ:", np.shares_memory(raw, crop))

raw = np.array([[240, 10], [100, 200]], dtype=np.uint8)
crop = raw[:, :1].copy()
crop[0, 0] = 0
print("sửa copy, giữ gốc:", raw.tolist())

wrapped = raw + 30
# Đổi sang kiểu rộng hơn trước khi cộng, rồi dùng clip để kẹp về khoảng 0–255.
bright = np.clip(raw.astype(np.int16) + 30, 0, 255).astype(np.uint8)
print("cộng uint8:", wrapped.tolist())
print("đổi kiểu rồi kẹp:", bright.tolist())
assert np.array_equal(raw, [[240, 10], [100, 200]])


# Ví dụ 4: Gán nhãn theo điểm mẫu gần nhất, và bắt một lỗi shape không báo lỗi
import numpy as np

references = np.array([[0, 0], [3, 4], [6, 0]], dtype=np.float64)
labels = np.array(["A", "B", "C"])
queries = np.array([[0, 3], [4, 4], [5, 1]], dtype=np.float64)

# Ba trục lần lượt là: điểm mới, điểm mẫu, tọa độ.
delta = queries[:, None, :] - references[None, :, :]
distance2 = (delta ** 2).sum(axis=2)
nearest = distance2.argmin(axis=1)
predicted = labels[nearest]
print("shape trung gian:", delta.shape)
print("bình phương khoảng cách:", distance2.tolist())
print("nhãn dự đoán:", predicted.tolist())
print("byte của delta:", delta.nbytes)

# Tính lại từng cặp bằng vòng lặp thường để kiểm phép broadcast ở trên.
expected_distance2 = np.array([
    [sum((float(q[k]) - float(r[k])) ** 2 for k in range(2))
     for r in references] for q in queries
])
assert np.array_equal(distance2, expected_distance2)

truth = np.array(["A", "B", "C"])
predicted_column = predicted[:, None]
wrong_comparison = predicted_column == truth
print("shape so sánh sai:", wrong_comparison.shape)
print("accuracy tính nhầm:", round(float(wrong_comparison.mean()), 3))

# Mỗi mẫu có đúng một nhãn, nên đưa dự đoán về lại một trục.
aligned = predicted_column.ravel()
assert aligned.shape == truth.shape
print("accuracy theo từng mẫu:", float((aligned == truth).mean()))

