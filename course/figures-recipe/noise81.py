"""Bài 8.1: phân bố chênh lệch accuracy public (B trừ A) khi public có 200 hoặc 1000 dòng, từ đúng thí nghiệm của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-8/8.1.md'
ns = {'__name__': 'noise_figure'}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
out = buf.getvalue()
assert '200 A >= B: 0.33 std 0.018' in out and '1000 A >= B: 0.05 std 0.006' in out, out
ca, cb = ns['correct_a'], ns['correct_b']
rng = np.random.default_rng(1)
bins = np.arange(-0.0825, 0.1, 0.005)
fig, ax = plt.subplots(figsize=(6.3, 3.0))
for size, color, label in ((200, '#c2603e', 'public 200 dòng'), (1000, '#3b6ea8', 'public 1000 dòng')):
    gaps = np.array([cb[r].mean() - ca[r].mean() for r in (rng.choice(2000, size=size, replace=False) for _ in range(5000))])
    ax.hist(gaps, bins=bins, color=color, alpha=0.55, label=label, density=True)
ax.axvline(0, color='#1f1e1c', lw=0.9)
ax.axvline(0.01, color='#b8892b', ls='--', lw=1.0)
ax.set(xlabel='accuracy public của B trừ A', yticks=[])
ax.spines['left'].set_visible(False)
ax.legend(frameon=False, fontsize=10, loc='upper left')
fig.tight_layout()
write(fig, '8-1-noise')
print('noise figure verified', flush=True)
