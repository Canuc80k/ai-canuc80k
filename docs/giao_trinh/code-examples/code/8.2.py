# -*- coding: utf-8 -*-
# Code mẫu — Phân tích dữ liệu trước huấn luyện

# Ví dụ 1: Được dùng median nào để điền chỗ thiếu?
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

train = pd.DataFrame({"id": ["001", "002", "002", "004"],
                      "signal": [2.0, np.nan, 6.0, 10.0]})
validation = np.array([[100.0], [np.nan]])
print("thiếu:", int(train["signal"].isna().sum()))
print("ID lặp:", train.loc[train["id"].duplicated(), "id"].tolist())
X_train = train[["signal"]].to_numpy()
clean = SimpleImputer(strategy="median").fit(X_train)
leaky = SimpleImputer(strategy="median").fit(np.vstack([X_train, validation]))
assert clean.statistics_[0] == 6.0 and leaky.statistics_[0] == 8.0
print("median train:", clean.statistics_.tolist())
print("median ghép cả validation:", leaky.statistics_.tolist())
print("validation sau transform sạch:", clean.transform(validation).ravel().tolist())


# Ví dụ 2: Nhớ một tài liệu khác với đoán đúng tài liệu mới
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

groups = np.repeat(np.arange(4), 2)
X = np.eye(4)[groups]
y = np.array([0, 1, 1, 0])[groups]
row_train, row_val = np.array([0, 2, 4, 6]), np.array([1, 3, 5, 7])
splitter = GroupShuffleSplit(n_splits=1, test_size=0.5, random_state=0)
group_train, group_val = next(splitter.split(X, y, groups))
for name, fit_rows, val_rows in [
    ("theo đoạn", row_train, row_val), ("theo tài liệu", group_train, group_val)
]:
    overlap = sorted(map(int, set(groups[fit_rows]) & set(groups[val_rows])))
    model = KNeighborsClassifier(n_neighbors=1).fit(X[fit_rows], y[fit_rows])
    prediction = model.predict(X[val_rows])
    print(name, "nguồn chung:", overlap,
          "accuracy:", f"{accuracy_score(y[val_rows], prediction):.3f}")
    print("nhãn thật/dự đoán:", y[val_rows].tolist(), prediction.tolist())
assert not (set(groups[group_train]) & set(groups[group_val]))
assert np.array_equal(X[row_train], X[row_val])


# Ví dụ 3: Chia theo thời gian, và một cảm biến bị lệch
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

times = np.arange(12)
for number, (fit_rows, val_rows) in enumerate(
    TimeSeriesSplit(n_splits=3, test_size=2, gap=1).split(times), 1
):
    assert times[fit_rows].max() + 1 < times[val_rows].min()
    print("fold", number, "train cuối:", int(times[fit_rows].max()),
          "val đầu:", int(times[val_rows].min()))

X_train = np.array([0.0, 1.0, 3.0, 4.0]).reshape(-1, 1)
y_train = np.array([0, 0, 1, 1])
future = pd.DataFrame({"device": ["old", "old", "new", "new"],
                       "reading": [1.0, 3.0, 11.0, 13.0],
                       "known_offset": [0.0, 0.0, 10.0, 10.0],
                       "label": [0, 1, 0, 1]})
model = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X_train, y_train)
raw = model.predict(future[["reading"]].to_numpy())
corrected = model.predict((future["reading"] - future["known_offset"]).to_numpy().reshape(-1, 1))
for device in ["old", "new"]:
    rows = future["device"].eq(device).to_numpy()
    labels = future.loc[rows, "label"].to_numpy()
    print(device, "n:", int(rows.sum()), "raw/corrected:",
          f"{accuracy_score(labels, raw[rows]):.2f}",
          f"{accuracy_score(labels, corrected[rows]):.2f}")
assert np.array_equal(corrected, future["label"].to_numpy())

