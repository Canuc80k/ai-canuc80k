"""Buổi kt4: điểm chuẩn hóa theo metric của hai bài (macro-F1 và WER), lấy từ đúng hàm normalized_score của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-7/kt4.md'
ns = {'__name__': 'kt4_score_figure'}
out = io.StringIO()
with contextlib.redirect_stdout(out):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
score = ns['normalized_score']
assert 'A, macro-F1 0.70 -> 50.0' in out.getvalue() and 'B, WER 0.45      -> 0.0' in out.getvalue()
A = dict(baseline=0.50, best=0.90, points=[0.70, 0.74])
B = dict(baseline=0.40, best=0.15, points=[0.30, 0.45])
assert [round(score(x, A['baseline'], A['best']), 6) for x in A['points']] == [50, 60]
assert [round(score(x, B['baseline'], B['best']), 6) for x in B['points']] == [40, 0]
assert round(score(0.38, B['baseline'], B['best']), 6) == 8  # hỏi nhanh của mục

fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.7), sharey=True)
for ax, task, lo, hi, color, label in [(axes[0], A, 0.40, 0.90, '#3b6ea8', 'macro-F1 (bài A)'),
                                       (axes[1], B, 0.15, 0.50, '#c2603e', 'WER (bài B)')]:
    x = np.linspace(lo, hi, 401)
    ax.plot(x, [score(v, task['baseline'], task['best']) for v in x], color=color, lw=1.7)
    ax.axvline(task['baseline'], color='#b8892b', ls='--', lw=1.0)
    pts = task['points']
    ax.scatter(pts, [score(v, task['baseline'], task['best']) for v in pts], color=color, s=28, zorder=3)
    ax.set(xlabel=label, xlim=(lo, hi), ylim=(-4, 104))
axes[0].set_ylabel('điểm')
axes[0].set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
axes[1].set_xticks([0.15, 0.2, 0.3, 0.4, 0.5])
fig.tight_layout()
write(fig, '7-kt4-score')
print('kt4 score figure verified', flush=True)
