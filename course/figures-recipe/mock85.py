"""Bài 8.5: accuracy theo thứ tự cột và nhật ký thời gian của hai buổi luyện, lấy từ đúng code của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-8/8.5.md'
ns = {'__name__': 'mock_figure'}
out = io.StringIO()
with contextlib.redirect_stdout(out):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)

# ---- hình 1: accuracy theo sáu thứ tự cột ----
log = out.getvalue()
for line in ["['x0', 'x1', 'x2'] 0.933", "['x2', 'x0', 'x1'] 0.700", "['x1', 'x0', 'x2'] 0.900"]:
    assert line in log, line
model, X_val, y_val, names = ns['model'], ns['X_val'], ns['y_val'], ns['feature_columns']
from itertools import permutations
from sklearn.metrics import accuracy_score
rows = []
for order in permutations(range(3)):
    rows.append((', '.join(names[i] for i in order),
                 accuracy_score(y_val, model.predict(X_val[:, list(order)])), order == (0, 1, 2)))
rows.sort(key=lambda r: -r[1])
assert [r[0] for r in rows][0] == 'x0, x1, x2' and round(rows[0][1], 3) == 0.933
fig, ax = plt.subplots(figsize=(6.3, 2.7))
labels = [r[0] for r in rows][::-1]
values = [r[1] for r in rows][::-1]
colors = ['#c2603e' if r[2] else '#3b6ea8' for r in rows][::-1]
ax.barh(labels, values, color=colors, height=0.62)
for y, v in enumerate(values):
    ax.text(v + 0.012, y, f'{v:.3f}', va='center', fontsize=10)
ax.set(xlim=(0, 1.08), xlabel='accuracy validation (30 mẫu)')
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
fig.tight_layout()
write(fig, '8-5-column-order')

# ---- hình 2: ba lịch 360 phút ----
minutes = ns['minutes']
assert minutes.sum().to_dict() == {'plan': 360, 'session1': 360, 'session2': 360}
closed = minutes.loc[['read', 'baseline', 'improve']].sum().to_dict()
assert closed == {'plan': 300, 'session1': 325, 'session2': 275}
stages = list(minutes.index)
names_vi = {'read': 'đọc đề', 'baseline': 'baseline', 'improve': 'cải thiện', 'rerun': 'chạy lại', 'check': 'kiểm file'}
palette = {'read': '#6f6b60', 'baseline': '#b8892b', 'improve': '#3b6ea8', 'rerun': '#c2603e', 'check': '#4f8a63'}
rows = [('kế hoạch', 'plan'), ('buổi 1', 'session1'), ('buổi 2', 'session2')]
fig, ax = plt.subplots(figsize=(6.3, 3.3))
for i, (label, col) in enumerate(rows):
    left = 0
    for st in stages:
        w = int(minutes.loc[st, col])
        if w:
            ax.barh(i, w, left=left, color=palette[st], edgecolor='white', linewidth=1.2, height=0.52,
                    label=names_vi[st] if i == 0 else None)
            ax.text(left + w / 2, i, str(w), ha='center', va='center', color='white', fontsize=9.5, fontweight='bold')
        left += w
    ax.plot([closed[col]], [i + 0.38], marker='^', color='#1f1e1c', markersize=5, clip_on=False)
    ax.text(closed[col], i + 0.47, str(closed[col]), ha='center', va='top', fontsize=9.5)
ax.set_yticks(range(3), [r[0] for r in rows])
ax.set(xlim=(0, 360), ylim=(2.85, -0.45), xlabel='phút')
ax.set_xticks(range(0, 361, 60))
ax.legend(frameon=False, ncol=5, fontsize=9, loc='lower center', bbox_to_anchor=(0.5, 1.12), columnspacing=1.1, handlelength=1.2)
fig.tight_layout()
write(fig, '8-5-sessions')
print('mock 8.5 figures verified', flush=True)
