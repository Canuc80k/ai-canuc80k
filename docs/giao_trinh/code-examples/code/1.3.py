# -*- coding: utf-8 -*-
# Code mẫu — Data split và cross-validation

# Ví dụ 1: Validation có còn mẫu của lớp hiếm không?
import numpy as np
from math import comb
from sklearn.model_selection import train_test_split

y = np.array([1, 1, 1] + [0] * 9)
ids = np.arange(len(y))
train_ids, valid_ids = train_test_split(
    ids, test_size=3, stratify=y, random_state=31,
)
print("Số hàng train/valid:", len(train_ids), len(valid_ids))
print("Số nhãn 1 train/valid:", int(y[train_ids].sum()), int(y[valid_ids].sum()))
print("Trùng hàng:", len(set(train_ids) & set(valid_ids)))
print(f"Xác suất thiếu lớp 1 nếu chọn đều ba hàng: {comb(9, 3)/comb(12, 3):.3f}")


# Ví dụ 2: Không trùng hàng, nhưng vẫn có thể trùng học sinh
import numpy as np
from sklearn.model_selection import GroupKFold

groups = np.repeat(["A", "B", "C", "D", "E", "F"], 2)
X = np.zeros((12, 1))
y = np.repeat([0, 1, 0, 1, 0, 1], 2)
row_train = np.arange(0, 12, 2)
row_valid = np.arange(1, 12, 2)
print("Split từng hàng, trùng hàng:", len(set(row_train) & set(row_valid)))
print("Split từng hàng, trùng người:", sorted(map(str, set(groups[row_train]) & set(groups[row_valid]))))

cv = GroupKFold(n_splits=3)
for fold, (train_ids, valid_ids) in enumerate(cv.split(X, y, groups), start=1):
    shared = set(groups[train_ids]) & set(groups[valid_ids])
    assert not shared
    valid_groups = sorted(map(str, set(groups[valid_ids])))
    print(f"Fold {fold}: valid={valid_groups}, nhãn 1={int(y[valid_ids].sum())}, trùng người={len(shared)}")


# Ví dụ 3: Nhãn của train phải hai tuần sau mới biết
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

weeks = np.arange(12)
label_known_at = weeks + 2
for gap in [0, 2]:
    cv = TimeSeriesSplit(n_splits=3, test_size=2, gap=gap)
    for fold, (train_ids, valid_ids) in enumerate(cv.split(weeks), start=1):
        prediction_week = int(weeks[valid_ids].min())
        latest_label = int(label_known_at[train_ids].max())
        available = latest_label < prediction_week
        print(f"gap={gap}, fold={fold}: train cuối={int(weeks[train_ids].max())}, valid đầu={prediction_week}, nhãn biết lúc={latest_label}, hợp lệ={available}")
        if gap == 2:
            assert available


# Ví dụ 4: Ghi dự đoán OOF về đúng hàng gốc
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

X = np.arange(9, dtype=float).reshape(-1, 1)
y = 2 * X[:, 0] + 1
oof = np.full(len(y), np.nan)
count = np.zeros(len(y), dtype=int)
chunks = []
cv = KFold(n_splits=3, shuffle=True, random_state=32)
for fold, (train_ids, valid_ids) in enumerate(cv.split(X), start=1):
    model = LinearRegression().fit(X[train_ids], y[train_ids])
    prediction = model.predict(X[valid_ids])
    oof[valid_ids] = prediction       # Ghi vào đúng vị trí gốc, để mỗi dự đoán đứng cạnh nhãn của chính nó.
    count[valid_ids] += 1
    chunks.append(prediction)
    print(f"Fold {fold}: valid IDs={valid_ids.tolist()}")
assert np.all(count == 1)
assert np.isfinite(oof).all()
assert np.allclose(oof, y)
print(f"OOF đúng: MAE={mean_absolute_error(y, oof):.3f}")
print(f"Nối theo fold rồi ghép với y gốc, cách sai: MAE={mean_absolute_error(y, np.concatenate(chunks)):.3f}")

