"""Bài 3.6: train loss và validation MSE theo epoch (decay 0), lấy từ đúng thí nghiệm early stopping của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-3/3.6.md'
ns = {'__name__': 'regul_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
    best_epoch, best, history = ns['fit_small'](0.)
noise = (ns['y_train'] - ns['x_train'].square()).square().mean().item()
train, valid = np.array(history).T
assert best_epoch == 26 and round(best, 5) == 0.00367 and round(float(valid[-1]), 5) == 0.01294
assert round(noise, 4) == 0.0491 and round(float(train[-1]), 4) == 0.0359
epochs = np.arange(1, len(valid) + 1)
fig, ax = plt.subplots(figsize=(6.3, 3.1))
ax.plot(epochs, train, color='#3b6ea8', lw=1.5, label='train')
ax.plot(epochs, valid, color='#c2603e', lw=1.7, label='validation')
ax.axhline(noise, color='#b8892b', ls=':', lw=1.2, label='MSE của nhiễu')
ax.axvline(best_epoch, color='#c2603e', ls='--', lw=0.8, alpha=0.6)
ax.scatter([best_epoch], [best], color='#c2603e', s=26, zorder=4)
ax.set(xlabel='epoch', ylabel='MSE', yscale='log', xlim=(0, 161))
ax.legend(frameon=False, fontsize=10, loc='upper right')
fig.tight_layout()
write(fig, '3-6-early-stop')
print('early stopping curve verified', flush=True)
