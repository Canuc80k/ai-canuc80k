# -*- coding: utf-8 -*-
# Phân tích dữ liệu trước huấn luyện — chạy các bước như notebook từ trên xuống.

# Bước 1
from io import StringIO
import numpy as np
import pandas as pd

csv_data = """id,document,device,signal,label
001,doc-a,old,1.2,1
002,doc-a,old,1.3,1
003,doc-b,old,-0.8,0
004,doc-c,new,,1
005,doc-d,new,0.4,0
006,doc-e,old,-0.8,0
007,doc-b,old,-0.8,1
003,doc-b,old,-0.8,0
"""
df = pd.read_csv(StringIO(csv_data), dtype={"id": str})
print("shape", df.shape)
print("missing", df.isna().sum().to_dict())
print("duplicated ids", df.loc[df["id"].duplicated(), "id"].tolist())
print("labels", df["label"].value_counts().sort_index().to_dict())

# Bước 2
key = ["document", "device", "signal"]
unique_labels = df.groupby(key, dropna=False)["label"].nunique()
conflicts = unique_labels[unique_labels > 1]
print("conflicting feature groups", len(conflicts))
print(conflicts.index.tolist())
print("exact duplicated rows", int(df.duplicated().sum()))

# Bước 3
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(82)
groups = np.repeat(np.arange(60), 4)
document_labels = rng.integers(0, 2, size=60)
X = np.eye(60)[groups]             # (240, 60), dấu vết nguồn
y = document_labels[groups]       # (240,), nhãn theo tài liệu
rows = np.arange(len(y))
random_train, random_val = train_test_split(
    rows, test_size=0.25, random_state=0, stratify=y)
splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=1)
group_train, group_val = next(splitter.split(X, y, groups))

for name, train_rows, val_rows in [
    ("random", random_train, random_val),
    ("group", group_train, group_val),
]:
    model = KNeighborsClassifier(n_neighbors=1).fit(X[train_rows], y[train_rows])
    prediction = model.predict(X[val_rows])
    overlap = set(groups[train_rows]) & set(groups[val_rows])
    print(name, "overlap", len(overlap),
          "accuracy", f"{accuracy_score(y[val_rows], prediction):.3f}")
    if name == "group":
        print("group predictions", np.unique(prediction).tolist(),
              "val label counts", np.bincount(y[val_rows]).tolist())

# Bước 4
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def make_domain(n, shortcut_agreement, seed):
    generator = np.random.default_rng(seed)
    signal = generator.normal(size=n)
    labels = (signal + generator.normal(0, 0.5, n) > 0).astype(int)
    shortcut = 2 * labels - 1
    flips = generator.random(n) > shortcut_agreement
    shortcut[flips] *= -1
    features = np.column_stack([signal, shortcut])
    return features, labels

X_source, y_source = make_domain(800, 0.95, 1)
X_shift, y_shift = make_domain(400, 0.05, 2)
train_rows, val_rows = train_test_split(
    np.arange(800), test_size=0.25, random_state=3, stratify=y_source)

for name, columns in [("both", [0, 1]), ("signal-only", [0])]:
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))
    model.fit(X_source[train_rows][:, columns], y_source[train_rows])
    in_domain = model.predict(X_source[val_rows][:, columns])
    out_domain = model.predict(X_shift[:, columns])
    print(name,
          "in-domain", f"{accuracy_score(y_source[val_rows], in_domain):.3f}",
          "shifted", f"{accuracy_score(y_shift, out_domain):.3f}")

# Bước 5
slice_counts = pd.DataFrame({
    "device": ["old", "new"],
    "n": [90, 10],
    "correct": [81, 2],
})
slice_counts["accuracy"] = slice_counts["correct"] / slice_counts["n"]
print(slice_counts.to_string(index=False))
print("overall", slice_counts["correct"].sum() / slice_counts["n"].sum())
print("equal-domain mean", slice_counts["accuracy"].mean())
