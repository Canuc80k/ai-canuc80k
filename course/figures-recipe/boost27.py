"""Bài 2.7: MSE train và validation theo số cây, lấy từ đúng thí nghiệm staged_predict của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-2/2.7.md'
ns = {'__name__': 'boost_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
train, valid, best = np.array(ns['train_losses']), np.array(ns['valid_losses']), ns['best_round']
assert best == 31 and round(float(valid[best - 1]), 2) == 20.86 and round(float(valid[-1]), 2) == 23.05
rounds = np.arange(1, len(valid) + 1)
fig, ax = plt.subplots(figsize=(6.3, 3.1))
ax.plot(rounds, train, color='#3b6ea8', lw=1.5, label='train')
ax.plot(rounds, valid, color='#c2603e', lw=1.7, label='validation')
ax.axvline(best, color='#c2603e', ls='--', lw=0.8, alpha=0.6)
ax.scatter([best], [valid[best - 1]], color='#c2603e', s=26, zorder=4)
ax.set(xlabel='số cây', ylabel='MSE', ylim=(0, 40))
ax.legend(frameon=False, fontsize=10, loc='upper right')
fig.tight_layout()
write(fig, '2-7-early-stop')
print('boosting curve verified', flush=True)
