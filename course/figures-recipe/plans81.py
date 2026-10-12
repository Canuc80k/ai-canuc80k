"""Bài 8.1: 27 kế hoạch (phút, điểm), bao trên theo ngân sách và kế hoạch tham lam, từ đúng code của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from itertools import product
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-8/8.1.md'
ns = {'__name__': 'plans_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S)[:2]:
        exec(compile(code, str(p), 'exec'), ns)
plan_total, best_plan, greedy_plan = ns['plan_total'], ns['best_plan'], ns['greedy_plan']
assert best_plan(130) == ((1, 1, 2), 130, 40) and greedy_plan(130) == ((2, 1, 1), 125, 30)

plans = [plan_total(lv) for lv in product(range(3), repeat=3)]
minutes = np.array([m for m, g in plans])
gains = np.array([g for m, g in plans])
budgets = np.arange(0, 201)
upper = np.array([max(g for m, g in plans if m <= b) for b in budgets])

fig, ax = plt.subplots(figsize=(6.3, 3.3))
ax.step(budgets, upper, where='post', color='#3b6ea8', lw=1.6)
ax.scatter(minutes, gains, s=20, color='#3b6ea8', alpha=0.5, zorder=3)
ax.axvline(130, color='#b8892b', ls='--', lw=1.0)
ax.scatter([130], [40], s=70, color='#c2603e', zorder=5)
ax.scatter([125], [30], s=70, facecolors='none', edgecolors='#1f1e1c', linewidths=1.5, zorder=5)
ax.annotate('duyệt hết: 40', (130, 40), (150, 36), color='#c2603e', fontsize=10,
            arrowprops=dict(arrowstyle='-', color='#c2603e', lw=0.8))
ax.annotate('tham lam: 30', (125, 30), (72, 34), color='#1f1e1c', fontsize=10,
            arrowprops=dict(arrowstyle='-', color='#1f1e1c', lw=0.8))
ax.set(xlabel='tổng phút', ylabel='điểm dự kiến', xlim=(0, 205), ylim=(0, 50))
fig.tight_layout()
write(fig, '8-1-plans')
print('plans figure verified', flush=True)
