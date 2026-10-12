# -*- coding: utf-8 -*-
# Code mẫu — Chiến lược thi

# Ví dụ 1: Ba xác suất đều đúng mà file vẫn có thể sai
from io import StringIO
import numpy as np
import pandas as pd

expected = ["001", "007", "010"]
predictions = pd.DataFrame({
    "id": ["010", "001", "007"], "probability": [0.55, 0.15, 0.80]
})
assert predictions["id"].is_unique
assert set(predictions["id"]) == set(expected)
ordered = predictions.set_index("id").loc[expected].reset_index()

def check_csv(text):
    frame = pd.read_csv(StringIO(text), dtype={"id": str})
    if frame.columns.tolist() != ["id", "probability"]:
        raise ValueError("sai cột")
    if frame["id"].tolist() != expected or not frame["id"].is_unique:
        raise ValueError("sai ID hoặc thứ tự")
    p = frame["probability"].to_numpy(dtype=float)
    if not np.isfinite(p).all() or not ((0 <= p) & (p <= 1)).all():
        raise ValueError("xác suất ngoài miền")
    return frame

csv_text = ordered.to_csv(index=False, lineterminator="\n")
checked = check_csv(csv_text)
print(csv_text.rstrip())
print("đọc lại:", checked.shape)
bad = ordered.copy()
bad.loc[1, "probability"] = 1.2
try:
    check_csv(bad.to_csv(index=False))
except ValueError as error:
    print("bắt lỗi:", error)
else:
    raise AssertionError("Bộ kiểm bỏ sót xác suất 1.2")


# Ví dụ 2: Đo đúng phần việc mà máy chấm sẽ chạy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
import numpy as np
import pandas as pd

with TemporaryDirectory(prefix="ai81-") as directory:
    folder = Path(directory)
    (folder / "model.json").write_text(
        json.dumps({"weights": [0.5, -0.25], "bias": 0.0}), encoding="utf-8")
    pd.DataFrame({"id": ["001", "002", "003"],
                  "x0": [0.0, 2.0, -2.0], "x1": [0.0, 0.0, 0.0]}).to_csv(
        folder / "input.csv", index=False)

    start = perf_counter()
    config = json.loads((folder / "model.json").read_text(encoding="utf-8"))
    data = pd.read_csv(folder / "input.csv", dtype={"id": str})
    X = data[["x0", "x1"]].to_numpy(dtype=np.float64)
    w = np.array(config["weights"], dtype=np.float64)
    blocks = []
    for first in range(0, len(X), 2):
        logits = X[first:first + 2] @ w + config["bias"]
        blocks.append(1 / (1 + np.exp(-logits)))
    probabilities = np.concatenate(blocks)
    destination = folder / "submission.csv"
    pd.DataFrame({"id": data["id"], "probability": probabilities}).to_csv(
        destination, index=False, float_format="%.6f")
    elapsed_seconds = perf_counter() - start
    readback = pd.read_csv(destination, dtype={"id": str})
    assert elapsed_seconds >= 0
    assert readback["id"].tolist() == data["id"].tolist()
    assert np.allclose(probabilities, [0.5, 1 / (1 + np.exp(-1)),
                                      1 / (1 + np.exp(1))])
    print("batch:", len(blocks), "số mẫu:", len(probabilities))
    print("bytes X và w:", X.nbytes + w.nbytes)
    print("xác suất:", readback["probability"].tolist())


# Ví dụ 3: Một cải tiến cần một bước chuẩn bị trước
from itertools import product

cost = {"A": 10, "B": 20, "C": 20}
gain = {"A": 1, "B": 8, "C": 5}
valid = []
for flags in product([False, True], repeat=3):
    chosen = {name for name, flag in zip(cost, flags) if flag}
    if "B" in chosen and "A" not in chosen:
        continue
    minutes = sum(cost[name] for name in chosen)
    if minutes <= 30:
        valid.append((sum(gain[name] for name in chosen), -minutes,
                      tuple(sorted(chosen))))
best_gain, negative_cost, plan = max(valid)
assert plan == ("A", "B") and best_gain == 9
print("kế hoạch:", plan)
print("phút giả định:", -negative_cost, "điểm tăng dự kiến:", best_gain)
print("nếu giữ 10 phút chạy cuối, phương án:",
      max(item for item in valid if -item[1] <= 20)[2])

