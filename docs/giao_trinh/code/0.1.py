# -*- coding: utf-8 -*-
# Python — chạy các bước như notebook từ trên xuống.

# Bước 1
n = 3
total = sum(range(n + 1))
n = 5                       # giống như chạy lại riêng ô đầu
print(n, total)
total = sum(range(n + 1))    # chạy lại bước phụ thuộc
print(n, total)

# Bước 2
def passed_scores(values, threshold=5.0):
    result = []
    for value in values:
        if value >= threshold:
            result.append(value)
    return result

print(passed_scores([4.5, 7.0, 5.0]))
print(list(range(1, 5)))      # đầu được lấy, cuối không được lấy

# Bước 3
print(2 ** 100)
print(2 ** 63 - 1 + 1)               # vượt LLONG_MAX của C++ vẫn đúng

# Bước 4
print(7 / 2, 6 / 2)
print(7 // 2, -7 // 2)
print(7 % 3, -7 % 3)
print(int(-3.7))                     # int() cắt phần thập phân, về phía 0

# Bước 5
import math
print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9, abs_tol=1e-12))
print(round(2.5), round(3.5), round(0.125, 2))

# Bước 6
a = [1, 2, 3]
b = a
b.append(4)
print(a, b, a is b)

# Bước 7
x = 5
y = x
y += 1
print(x, y)

# Bước 8
a = [1, 2, 3]
c = a.copy()                          # hoặc a[:], list(a)
c.append(4)
print(a, c)

# Bước 9
grid = [[0] * 3] * 3                  # SAI: ba tên cho cùng một hàng
grid[0][0] = 9
print(grid)

grid = [[0] * 3 for _ in range(3)]    # ĐÚNG: mỗi lần lặp tạo một hàng mới
grid[0][0] = 9
print(grid)

# Bước 10
a = [5, 3, 8, 1, 9, 2]
print(a[1:4], a[-1], a[-2:], a[::-1])
print([x * x for x in a if x % 2 == 1])

scores = {"An": 8.5, "Bình": 6.0}
scores["Chi"] = 9.0
print(scores.get("Dũng", 0.0), len(scores), "An" in scores)

# Bước 11
from collections import Counter
words = "mèo chó mèo gà mèo chó".split()
print(Counter(words).most_common(2))
print(sorted(scores.items(), key=lambda kv: -kv[1]))

# Bước 12
L = list(range(10**5))
S = set(L)
queries = range(-500, 500)

r1 = [query in L for query in queries]
r2 = [query in S for query in queries]
print(r1 == r2, sum(r2))

# Bước 13
names = ["An", "Bình", "Chi"]
marks = [8.5, 6.0, 9.0]
for i, (name, mark) in enumerate(zip(names, marks), start=1):
    print(f"{i}. {name}: {mark}")

# Bước 14
def stats(xs, ddof=0):
    n = len(xs)
    if not 0 <= ddof < n:
        raise ValueError("cần 0 <= ddof < số phần tử")
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - ddof)
    return mean, var

m, v = stats(marks)
print(round(m, 3), round(v, 3), round(stats(marks, ddof=1)[1], 3))

# Bước 15
def add_score(x, history=[]):          # SAI
    history.append(x)
    return history

print(add_score(1), add_score(2))

def add_score(x, history=None):        # ĐÚNG
    if history is None:
        history = []
    history.append(x)
    return history

print(add_score(1), add_score(2))

# Bước 16
import numpy as np

def loop_sum(n):
    s = 0
    for i in range(n):
        s += i
    return s

n = 500_000
expected = n * (n - 1) // 2
print(loop_sum(n), expected)
print(loop_sum(n) == sum(range(n)) == int(np.arange(n, dtype=np.int64).sum()))

# Bước 17
from timeit import repeat

jobs = [
    ("for", lambda: loop_sum(n)),
    ("sum", lambda: sum(range(n))),
    ("numpy", lambda: int(np.arange(n, dtype=np.int64).sum())),
]
timings = {}
for label, job in jobs:
    assert job() == expected
    timings[label] = min(repeat(job, repeat=5, number=3)) / 3
print("nhanh -> chậm:", sorted(timings, key=timings.get))

# Bước 18
name, acc = "logistic", 0.85432
print(f"{name:>10} | accuracy = {acc:.3f} | {acc:.1%}")
line = "  12, 7.5 ,An \n"
print(line.strip().split(","), [s.strip() for s in line.split(",")])
print(" - ".join(["a", "b", "c"]))

# Bước 19
import csv
from pathlib import Path
from tempfile import TemporaryDirectory

preds = {1: 0.91, 2: 0.15, 3: 0.67}
with TemporaryDirectory(dir=".") as directory:
    path = Path(directory) / "submission.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "prediction"])
        for student_id, prediction in preds.items():
            writer.writerow([student_id, prediction])
    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.reader(file))
print(rows)
print(type(rows[1][1]), float(rows[1][1]) + 1)

# Bước 20
tests = [lambda: "Điểm: " + 9, lambda: scores["Dũng"], lambda: marks[3], lambda: int("7.5")]
for f in tests:
    try:
        f()
    except Exception as e:
        print(type(e).__name__ + ":", e)

# Bước 21
sum = 0
try:
    sum([1, 2, 3])
except TypeError as e:
    print("TypeError:", e)
del sum                               # gỡ cái tên, sum dựng sẵn quay lại
print(sum([1, 2, 3]))
