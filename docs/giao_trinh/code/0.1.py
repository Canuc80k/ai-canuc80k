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
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('device:', device)

# Bước 3
def passed_scores(values, threshold=5.0):
    result = []
    for value in values:
        if value >= threshold:
            result.append(value)
    return result

print(passed_scores([4.5, 7.0, 5.0]))
print(list(range(1, 5)))      # đầu được lấy, cuối không được lấy

# Bước 4
print(2 ** 100)
print(2 ** 63 - 1 + 1)               # vượt LLONG_MAX của C++ vẫn đúng

# Bước 5
print(7 / 2, 6 / 2)
print(7 // 2, -7 // 2)
print(7 % 3, -7 % 3)
print(int(-3.7))                     # int() cắt phần thập phân, về phía 0

# Bước 6
import math
print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9, abs_tol=1e-12))
print(round(2.5), round(3.5), round(0.125, 2))

# Bước 7
a = [1, 2, 3]
b = a
b.append(4)
print(a, b, a is b)

# Bước 8
x = 5
y = x
y += 1
print(x, y)

# Bước 9
a = [1, 2, 3]
c = a.copy()                          # hoặc a[:], list(a)
c.append(4)
print(a, c)

# Bước 10
grid = [[0] * 3] * 3                  # SAI: ba tên cho cùng một hàng
grid[0][0] = 9
print(grid)

grid = [[0] * 3 for _ in range(3)]    # ĐÚNG: mỗi lần lặp tạo một hàng mới
grid[0][0] = 9
print(grid)

# Bước 11
a = [5, 3, 8, 1, 9, 2]
print(a[1:4], a[-1], a[-2:], a[::-1])
print([x * x for x in a if x % 2 == 1])

scores = {"An": 8.5, "Bình": 6.0}
scores["Chi"] = 9.0
print(scores.get("Dũng", 0.0), len(scores), "An" in scores)

# Bước 12
from collections import Counter
words = "mèo chó mèo gà mèo chó".split()
print(Counter(words).most_common(2))
print(sorted(scores.items(), key=lambda kv: -kv[1]))

# Bước 13
L = list(range(10**5))
S = set(L)
queries = range(-500, 500)

r1 = [query in L for query in queries]
r2 = [query in S for query in queries]
print(r1 == r2, sum(r2))

# Bước 14
names = ["An", "Bình", "Chi"]
marks = [8.5, 6.0, 9.0]
for i, (name, mark) in enumerate(zip(names, marks), start=1):
    print(f"{i}. {name}: {mark}")

# Bước 15
def stats(xs, ddof=0):
    n = len(xs)
    if not 0 <= ddof < n:
        raise ValueError("cần 0 <= ddof < số phần tử")
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - ddof)
    return mean, var

m, v = stats(marks)
print(round(m, 3), round(v, 3), round(stats(marks, ddof=1)[1], 3))

# Bước 16
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

# Bước 17
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

# Bước 18
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

# Bước 19
name, acc = "logistic", 0.85432
print(f"{name:>10} | accuracy = {acc:.3f} | {acc:.1%}")
line = "  12, 7.5 ,An \n"
print(line.strip().split(","), [s.strip() for s in line.split(",")])
print(" - ".join(["a", "b", "c"]))

# Bước 20
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

# Bước 21
tests = [lambda: "Điểm: " + 9, lambda: scores["Dũng"], lambda: marks[3], lambda: int("7.5")]
for f in tests:
    try:
        f()
    except Exception as e:
        print(type(e).__name__ + ":", e)

# Bước 22
class ScoreBook:
    def __init__(self, names, marks):
        assert len(names) == len(marks), "mỗi tên một điểm"
        self.names = list(names)
        self.marks = list(marks)

    def __len__(self):
        return len(self.marks)

    def __getitem__(self, i):
        return self.names[i], self.marks[i]

    def mean(self):
        return sum(self.marks) / len(self)

book = ScoreBook(["An", "Bình", "Chi"], [8.5, 6.0, 9.0])
print(len(book), book[1], round(book.mean(), 3))
for name, mark in book:
    print(name, mark)

# Bước 23
class Scaler:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, values):
        return self.forward(values)

    def forward(self, values):
        return [v * self.factor for v in values]

class ShiftScaler(Scaler):
    def __init__(self, factor, shift):
        super().__init__(factor)
        self.shift = shift

    def forward(self, values):
        return [v + self.shift for v in super().forward(values)]

f = ShiftScaler(2, 1)
print(f([1, 2, 3]), f.factor, isinstance(f, Scaler))

# Bước 24
sum = 0
try:
    sum([1, 2, 3])
except TypeError as e:
    print("TypeError:", e)
del sum                               # gỡ cái tên, sum dựng sẵn quay lại
print(sum([1, 2, 3]))
