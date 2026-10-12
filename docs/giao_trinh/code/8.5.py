# -*- coding: utf-8 -*-
# Thi thử — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

seed = 85
rng = np.random.default_rng(seed)
X = rng.normal(size=(150, 3))
y = (X[:, 0] + 0.6 * X[:, 1] + rng.normal(0, 0.3, 150) > 0).astype(int)
X[7, 2] = np.nan
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=seed, stratify=y)
model = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    LogisticRegression(C=1.0, max_iter=500, random_state=seed),
)
model.fit(X_train, y_train)
print("train/val", X_train.shape, X_val.shape)
print("val accuracy", f"{accuracy_score(y_val, model.predict(X_val)):.3f}")

# Bước 2
feature_columns = ["x0", "x1", "x2"]
test_frame = pd.DataFrame({
    "id": ["001", "009", "010"],
    "x0": [-0.7, 0.4, 1.2],
    "x1": [0.1, -0.6, 0.3],
    "x2": [0.0, np.nan, 0.2],
})
test_features = test_frame[feature_columns].to_numpy()
assert np.array_equal(model.classes_, [0, 1])
probability = model.predict_proba(test_features)[:, 1]
print("feature shape", test_features.shape)
print("class-1 probabilities", probability.round(6).tolist())

# Bước 3
from itertools import permutations

for order in permutations(range(3)):
    predicted = model.predict(X_val[:, list(order)])
    print([feature_columns[i] for i in order],
          f"{accuracy_score(y_val, predicted):.3f}")

# Bước 4
import base64
import json
import pickle
import subprocess
import sys

model_bytes = pickle.dumps(model, protocol=5)
payload = {
    "model": base64.b64encode(model_bytes).decode("ascii"),
    "X": np.nan_to_num(test_features, nan=0.0).tolist(),
    "missing": np.isnan(test_features).tolist(),
}
child_program = """
import base64, json, pickle, sys
import numpy as np
payload = json.loads(sys.stdin.read())
loaded = pickle.loads(base64.b64decode(payload["model"]))
features = np.array(payload["X"], dtype=float)
features[np.array(payload["missing"], dtype=bool)] = np.nan
prediction = loaded.predict_proba(features)[:, 1]
print(json.dumps(prediction.tolist()))
"""
child = subprocess.run(
    [sys.executable, "-B", "-c", child_program],
    input=json.dumps(payload), text=True, capture_output=True,
    check=True, timeout=30,
)
fresh_probability = np.array(json.loads(child.stdout))
print("fresh-process shape", fresh_probability.shape)
print("same probabilities", np.allclose(
    probability, fresh_probability, rtol=0, atol=1e-12))

# Bước 5
session_program = """
import base64, pickle, sys
import numpy as np
from sklearn.preprocessing import FunctionTransformer

def clip_log(values):
    return np.log1p(np.clip(values, 0, None))

step = FunctionTransformer(clip_log)
sys.stdout.write(base64.b64encode(pickle.dumps(step)).decode())
"""
load_program = """
import base64, pickle, sys
pickle.loads(base64.b64decode(sys.stdin.read()))
"""
session = subprocess.run([sys.executable, "-B", "-c", session_program],
                         text=True, capture_output=True, check=True, timeout=60)
raw = base64.b64decode(session.stdout)
print("name in pickle", b"clip_log" in raw)
print("body in pickle", b"log1p" in raw)
judge = subprocess.run([sys.executable, "-B", "-c", load_program],
                       input=session.stdout, text=True,
                       capture_output=True, timeout=60)
print("return code", judge.returncode)
print(judge.stderr.strip().splitlines()[-1].split(" on ")[0])

# Bước 6
from io import StringIO
from hashlib import sha256

submission = pd.DataFrame({
    "id": test_frame["id"],
    "probability": fresh_probability,
})
csv_text = submission.to_csv(index=False, float_format="%.6f",
                             lineterminator="\n")
readback = pd.read_csv(StringIO(csv_text), dtype={"id": str})
assert readback.columns.tolist() == ["id", "probability"]
assert readback["id"].tolist() == test_frame["id"].tolist()
assert readback["id"].is_unique
assert np.isfinite(readback["probability"]).all()
assert readback["probability"].between(0, 1).all()
csv_hash = sha256(csv_text.encode("utf-8")).hexdigest()
print(csv_text.rstrip())
print("readback", readback.shape, "OK")
print("sha256", csv_hash)

# Bước 7
import sklearn

manifest = {
    "seed": seed,
    "features": feature_columns,
    "classes": model.classes_.tolist(),
    "train_rows": len(y_train),
    "val_rows": len(y_val),
    "python": sys.version.split()[0],
    "numpy": np.__version__,
    "sklearn": sklearn.__version__,
    "submission_sha256": csv_hash,
}
print(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2))

# Bước 8
stages = ["read", "baseline", "improve", "rerun", "check"]
minutes = pd.DataFrame({
    "plan":     [30, 75, 195, 45, 15],
    "session1": [20, 80, 225, 0, 35],
    "session2": [30, 65, 180, 70, 15],
}, index=stages)
print(minutes.to_string())
print("total", minutes.sum().to_dict())
closed = minutes.loc[["read", "baseline", "improve"]].sum()
print("experiments closed at minute", closed.to_dict())
