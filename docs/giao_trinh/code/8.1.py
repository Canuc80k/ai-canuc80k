# -*- coding: utf-8 -*-
# Chiến lược thi — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

def normalized_score(raw, baseline, upper):
    assert upper > baseline
    return 100 * (raw - baseline) / (upper - baseline)

for name, baseline, upper, raw in [
    ("A", 0.58, 0.90, 0.70),
    ("B", 0.60, 0.90, 0.75),
]:
    print(name, f"{normalized_score(raw, baseline, upper):.2f}")
print("baseline", normalized_score(0.58, 0.58, 0.90))

# Bước 2
from itertools import product

options = {
    "A": [(0, 0), (30, 10), (60, 14)],
    "B": [(0, 0), (40, 14), (80, 17)],
    "C": [(0, 0), (25, 2), (60, 16)],
}

def plan_total(levels):
    chosen = [options[name][level]
              for name, level in zip(options, levels)]
    minutes = sum(cost for cost, gain in chosen)
    return minutes, sum(gain for cost, gain in chosen)

def best_plan(budget):
    plans = []
    for levels in product(range(3), repeat=3):
        minutes, gain = plan_total(levels)
        if minutes <= budget:
            plans.append((gain, -minutes, levels))
    gain, negative_minutes, levels = max(plans)
    return levels, -negative_minutes, gain

def greedy_plan(budget):
    levels = [0, 0, 0]
    while True:
        steps = []
        for i, name in enumerate(options):
            if levels[i] == 2:
                continue
            (c0, g0), (c1, g1) = options[name][levels[i]:levels[i] + 2]
            if plan_total(levels)[0] + c1 - c0 <= budget:
                steps.append(((g1 - g0) / (c1 - c0), i))
        if not steps:
            return tuple(levels), *plan_total(levels)
        levels[max(steps)[1]] += 1

print("duyệt hết", best_plan(130))
print("tham lam ", greedy_plan(130))

# Bước 3
experiments = [
    ("fix-schema", 0.9, 8, 10),
    ("new-model", 0.3, 20, 40),
    ("another-seed", 0.7, 2, 20),
]
ranked = sorted(experiments,
                key=lambda item: item[1] * item[2] / item[3],
                reverse=True)
for name, probability, gain, minutes in ranked:
    value = probability * gain / minutes
    print(name, f"{value:.2f} expected-points/min")

# Bước 4
rng = np.random.default_rng(0)
# 2000 dòng chấm kín; 1 = đoán đúng, 0 = đoán sai
correct_a = np.r_[np.ones(1540), np.ones(60), np.zeros(80), np.zeros(320)]
correct_b = np.r_[np.ones(1540), np.zeros(60), np.ones(80), np.zeros(320)]
print("hidden", correct_a.mean(), correct_b.mean())
for public_size in (200, 1000):
    gaps = []
    for _ in range(5000):
        rows = rng.choice(2000, size=public_size, replace=False)
        gaps.append(correct_b[rows].mean() - correct_a[rows].mean())
    gaps = np.array(gaps)
    print(public_size, f"A >= B: {np.mean(gaps <= 0):.2f}",
          f"std {gaps.std():.3f}")

# Bước 5
import pandas as pd
from io import StringIO

expected_ids = ["001", "007", "010"]
submission = pd.DataFrame({
    "id": expected_ids,
    "probability": [0.15, 0.80, 0.55],
})
csv_text = submission.to_csv(index=False, lineterminator="\n")
readback = pd.read_csv(StringIO(csv_text),
                       dtype={"id": str})
assert readback.columns.tolist() == ["id", "probability"]
assert readback["id"].tolist() == expected_ids
assert readback["id"].is_unique
assert np.isfinite(readback["probability"]).all()
assert readback["probability"].between(0, 1).all()
print(csv_text.rstrip())
print("readback", readback.shape, "OK")
