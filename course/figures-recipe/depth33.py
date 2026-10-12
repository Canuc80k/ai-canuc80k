"""Bài 3.3: độ lệch chuẩn pre-activation qua 10 lớp ReLU, lấy từ đúng thí nghiệm depth_probe của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-3/3.3.md'
ns = {'__name__': 'depth_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
small, he = np.array(ns['scales_small']), np.array(ns['scales_he'])
assert len(small) == len(he) == 10
assert f'{small[0]:.2g}' == '0.16' and f'{small[-1]:.2g}' == '4.9e-10'
assert [f'{v:.2g}' for v in he[::3]] == ['1.4', '1.3', '1.3', '1.4']
assert np.allclose(small / he, (0.01 / (2 / 256) ** 0.5) ** np.arange(1, 11), rtol=1e-3)
layers = np.arange(1, 11)
fig, ax = plt.subplots(figsize=(6.3, 3.1))
ax.plot(layers, he, color='#3b6ea8', lw=1.6, marker='o', ms=3.5, label='He')
ax.plot(layers, small, color='#c2603e', lw=1.6, marker='o', ms=3.5, label='N(0, 0.01²)')
ax.set_yscale('log')
ax.set(xlabel='lớp', ylabel='std pre-activation', xticks=layers, ylim=(1e-10, 10))
ax.legend(frameon=False, fontsize=10, loc='lower left')
fig.tight_layout()
write(fig, '3-3-depth-scale')
print('depth scale verified', flush=True)
