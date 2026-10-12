# -*- coding: utf-8 -*-
# Code mẫu — Thi thử

# Ví dụ 1: Bộ chấm ghép nhãn theo ID, không theo vị trí tình cờ
from io import StringIO
import numpy as np
import pandas as pd
from sklearn.metrics import log_loss

truth = pd.Series([0, 1, 1], index=["001", "007", "010"])
def score_csv(text):
    frame = pd.read_csv(StringIO(text), dtype={"id": str})
    if frame.columns.tolist() != ["id", "probability"]:
        raise ValueError("schema phải là id,probability")
    if frame["id"].tolist() != truth.index.tolist() or not frame["id"].is_unique:
        raise ValueError("ID hoặc thứ tự không đúng")
    p = frame["probability"].to_numpy(dtype=float)
    if not np.isfinite(p).all() or not ((0 <= p) & (p <= 1)).all():
        raise ValueError("xác suất không hợp lệ")
    return log_loss(truth.to_numpy(), np.column_stack([1 - p, p]), labels=[0, 1])

good = pd.DataFrame({"id": truth.index, "probability": [0.1, 0.8, 0.9]})
swapped = good.copy()
swapped["probability"] = [0.9, 0.8, 0.1]
for name, frame in [("đúng mapping", good), ("đảo hai xác suất", swapped)]:
    text = frame.to_csv(index=False, lineterminator="\n")
    print(name, "log-loss:", f"{score_csv(text):.4f}")
try:
    score_csv(good.to_csv(index=True))
except ValueError as error:
    print("file thừa index:", error)
else:
    raise AssertionError("Scorer phải từ chối cột ngoài schema")
assert score_csv(good.to_csv(index=False)) < score_csv(swapped.to_csv(index=False))


# Ví dụ 2: Train, lưu, nạp lại, và chấm một file thật
import json
import pickle
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(85)
features = ["signal", "aux"]
X = rng.normal(size=(120, 2))
y = (X[:, 0] + 0.4 * X[:, 1] > 0).astype(int)
X[3, 1] = np.nan
train_rows, val_rows = train_test_split(
    np.arange(len(y)), test_size=0.25, random_state=85, stratify=y)
model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                      LogisticRegression(C=1.0, max_iter=300, random_state=85))
model.fit(X[train_rows], y[train_rows])
reference = model.predict_proba(X[val_rows])[:, 1]
assert model.classes_.tolist() == [0, 1]
validation = pd.DataFrame(X[val_rows], columns=features)
validation.insert(0, "id", [f"{row:03d}" for row in val_rows])

temporary = TemporaryDirectory(prefix="ai85-")
folder = Path(temporary.name)
(folder / "model.pkl").write_bytes(pickle.dumps(model, protocol=5))
(folder / "config.json").write_text(json.dumps({"features": features, "class": 1}), encoding="utf-8")
del model
print("train/validation:", len(train_rows), len(val_rows))
print("artifact có model và config:", all((folder / name).is_file()
                                         for name in ["model.pkl", "config.json"]))

from hashlib import sha256
from sklearn.metrics import log_loss

def infer_from_artifact(directory, frame):
    config = json.loads((directory / "config.json").read_text(encoding="utf-8"))
    loaded = pickle.loads((directory / "model.pkl").read_bytes())
    column = loaded.classes_.tolist().index(config["class"])
    values = frame[config["features"]].to_numpy()
    return loaded.predict_proba(values)[:, column]

try:
    # Cố tình đảo thứ tự cột đầu vào. Config phải đưa các cột về đúng thứ tự lúc train.
    probabilities = infer_from_artifact(folder, validation[["id", "aux", "signal"]])
    assert np.allclose(probabilities, reference, rtol=0, atol=1e-12)
    output = pd.DataFrame({"id": validation["id"], "probability": probabilities})
    destination = folder / "submission.csv"
    output.to_csv(destination, index=False, float_format="%.8f", lineterminator="\n")
    readback = pd.read_csv(destination, dtype={"id": str})
    assert readback.columns.tolist() == ["id", "probability"]
    assert readback["id"].tolist() == validation["id"].tolist()
    assert readback["id"].is_unique
    p = readback["probability"].to_numpy()
    assert np.isfinite(p).all() and ((0 <= p) & (p <= 1)).all()
    scored = log_loss(y[val_rows], np.column_stack([1 - p, p]), labels=[0, 1])
    memory_score = log_loss(y[val_rows], np.column_stack([1 - reference, reference]), labels=[0, 1])
    assert abs(scored - memory_score) < 1e-6
    print("nạp lại trùng dự đoán:", True)
    print("ba hàng đầu:")
    print(readback.head(3).to_csv(index=False, float_format="%.8f", lineterminator="\n").rstrip())
    print("scorer đọc file, log-loss:", f"{scored:.6f}")
    print("sha256 CSV:", sha256(destination.read_bytes()).hexdigest())
finally:
    temporary.cleanup()

