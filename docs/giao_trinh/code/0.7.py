# -*- coding: utf-8 -*-
# Xác suất và thống kê — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

rng = np.random.default_rng(0)
rolls = rng.integers(1, 7, size=100_000)       # số nguyên từ 1 đến 6
print(round((rolls >= 5).mean(), 4), round(1 / 3, 4))
print(round(rolls.mean(), 3))

# Bước 2
pass_ = np.array([1] * 20 + [0] * 5 + [1] * 6 + [0] * 9)      # đạt hay không
homework = np.array([1] * 25 + [0] * 15)                    # làm bài tập đều hay không
p_pass = pass_.mean()
p_pass_given_hw = pass_[homework == 1].mean()
p_both = (pass_ & homework).mean()
print(p_pass, p_pass_given_hw, p_both / homework.mean())

# Bước 3
p_b = 0.01             # tỉ lệ mắc bệnh
p_d_b = 0.95           # dương tính khi có bệnh
p_d_not_b = 0.05       # dương tính nhầm khi khỏe
p_d = p_d_b * p_b + p_d_not_b * (1 - p_b)
print(round(p_d, 4), round(p_d_b * p_b / p_d, 4))

sick = rng.random(1_000_000) < p_b
positive = np.where(sick, rng.random(1_000_000) < p_d_b, rng.random(1_000_000) < p_d_not_b)
print(round(sick[positive].mean(), 4))

# Bước 4
a = np.array([6, 7, 7, 8, 7], dtype=float)
b = np.array([4, 9, 5, 10, 7], dtype=float)
for g in (a, b):
    print(g.mean(), round(g.var(), 2), round(g.std(), 2), round((10 - g.mean()) / g.std(), 2))
print(np.var(a, ddof=1))

# Bước 5
z = rng.normal(0, 1, size=100_000)
print(round((np.abs(z) < 1).mean(), 3), round((np.abs(z) < 2).mean(), 3))
means = rng.integers(1, 7, size=(100_000, 30)).mean(axis=1)
print(round(means.mean(), 3), round(means.std(), 3), round(np.sqrt(35 / 12 / 30), 3))
print(round((np.abs(means - 3.5) < means.std()).mean(), 3))

# Bước 6
p_true = 0.85
for n in [200, 2000]:
    acc = rng.binomial(n, p_true, size=10_000) / n       # 10 000 bộ validation, mỗi bộ n ảnh
    lo, hi = np.percentile(acc, [2.5, 97.5])
    print(n, round(acc.std(), 4), round(np.sqrt(p_true * (1 - p_true) / n), 4), lo, hi)

# Bước 7
print(round(0.9 * 0.2 / (0.9 * 0.2 + 0.02 * 0.8), 3), round(np.sqrt(0.92 * 0.08 / 400), 4))
