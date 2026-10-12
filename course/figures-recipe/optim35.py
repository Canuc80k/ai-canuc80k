"""Bài 3.5: loss theo bước của SGD, momentum và Adam, lấy từ đúng hàm run_optimizer của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-3/3.5.md'
ns = {'__name__': 'optim_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
run = ns['run_optimizer']
configs = [('sgd', .03, 'SGD 0.03', '#3b6ea8'), ('momentum', .03, 'Momentum 0.03', '#b8892b'), ('adam', .15, 'Adam 0.15', '#c2603e')]
steps = np.arange(0, 41)
curves = {kind: np.array([run(kind, lr, int(k))[1] for k in steps]) for kind, lr, _, _ in configs}
# Khớp đúng các khối output của bài.
assert f"{curves['sgd'][40]:.4g}" == '0.02833' and f"{curves['momentum'][40]:.4g}" == '0.0005109'
assert f"{curves['adam'][40]:.4g}" == '0.01883'
assert f"{curves['sgd'][30]:.3g}" == '0.0977' and f"{curves['adam'][30]:.3g}" == '0.314'
fig, ax = plt.subplots(figsize=(6.3, 3.1))
for kind, lr, label, color in configs:
    ax.plot(steps, curves[kind], color=color, lw=1.6, label=label)
ax.axvline(30, color='#1f1e1c', ls=':', lw=0.8, alpha=0.6)
ax.set_yscale('log')
ax.set(xlabel='bước', ylabel='loss', xlim=(0, 40))
ax.legend(frameon=False, fontsize=10, loc='lower left')
fig.tight_layout()
write(fig, '3-5-budget')
print('optimizer curves verified', flush=True)
