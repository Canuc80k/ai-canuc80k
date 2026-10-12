"""Bài 5.2: loss train theo bước của bốn mạng 18 lớp (plain/residual, có/không BatchNorm), lấy từ đúng thí nghiệm của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-5/5.2.md'
ns = {'__name__': 'depth_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
curves = {k: np.array(v) for k, v in ns['curves'].items()}
assert round(float(curves['plain'][-1]), 4) == 0.6931
assert round(float(curves['plain + BN'][10]), 4) == 0.3354 and round(float(curves['residual + BN'][10]), 4) == 0.0061
assert round(float(curves['residual'].max()), 4) == 19.1213
steps = np.arange(len(curves['plain']))
fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.1), sharey=True)
for ax, (plain, res), title in zip(axes, [('plain', 'residual'), ('plain + BN', 'residual + BN')],
                                   ['Không BatchNorm', 'Có BatchNorm']):
    ax.plot(steps, np.maximum(curves[plain], 1e-6), color='#c2603e', lw=1.5, label='plain')
    ax.plot(steps, np.maximum(curves[res], 1e-6), color='#3b6ea8', lw=1.5, label='residual')
    ax.set(xlabel='bước', title=title, yscale='log')
axes[0].set_ylabel('loss train')
axes[0].legend(frameon=False, fontsize=9, loc='lower left')
fig.tight_layout(w_pad=1.8)
write(fig, '5-2-depth')
print('depth curves verified', flush=True)
