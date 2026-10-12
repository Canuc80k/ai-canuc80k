"""Buổi kt3: tám xác suất validation và accuracy, F1 theo ngưỡng, lấy từ đúng code chọn threshold của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-5/kt3.md'
ns = {'__name__': 'kt3_threshold_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
prob, labels, metrics = ns['probabilities'], ns['labels'], ns['binary_metrics']
assert prob.tolist() == [0.9, 0.7, 0.6, 0.55, 0.45, 0.2, 0.1, 0.05] and int(labels.sum()) == 3
check = {t: tuple(round(v, 4) for v in metrics(prob >= t, labels)) for t in (0.5, 0.58, 0.65, 0.8)}
assert check == {0.5: (0.875, 0.8571), 0.58: (0.75, 0.6667), 0.65: (0.875, 0.8), 0.8: (0.75, 0.5)}, check

grid = np.linspace(0, 1, 2001)
acc, f1 = np.array([metrics(prob >= t, labels) for t in grid]).T
fig, (top, ax) = plt.subplots(2, 1, figsize=(6.3, 3.6), sharex=True, gridspec_kw={'height_ratios': [1, 2.3]})
top.scatter(prob[labels], np.ones(labels.sum()), s=46, color='#1f1e1c', zorder=3)
top.scatter(prob[~labels], np.zeros((~labels).sum()), s=46, facecolors='none', edgecolors='#1f1e1c', linewidths=1.3, zorder=3)
top.set(yticks=[0, 1], ylim=(-0.6, 1.6))
top.set_yticklabels(['âm', 'dương'])
top.spines['left'].set_visible(False)
top.spines['bottom'].set_visible(False)
top.tick_params(axis='y', length=0)
top.tick_params(axis='x', length=0)
ax.plot(grid, acc, color='#3b6ea8', lw=1.5, label='accuracy')
ax.plot(grid, f1, color='#c2603e', lw=1.7, label='F1')
for t in (0.5, 0.65):
    for a in (top, ax):
        a.axvline(t, color='#b8892b', ls='--', lw=1.0)
    ax.scatter([t, t], [check[t][0], check[t][1]], color=['#3b6ea8', '#c2603e'], s=22, zorder=4)
ax.set(xlabel='xác suất, ngưỡng', ylim=(0, 1.02), xlim=(0, 1))
ax.legend(frameon=False, fontsize=10, loc='lower left')
fig.tight_layout()
write(fig, '5-kt3-threshold')
print('kt3 threshold figure verified', flush=True)
