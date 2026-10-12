"""Bài 3.10: lỗi tái tạo từng mẫu test và ngưỡng phân vị 95% validation, lấy từ đúng code của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-3/3.10.md'
ns = {'__name__': 'autoencoder_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
err = ns['test_error'].numpy()
labels = ns['test_labels'].numpy()
threshold = ns['threshold']
normal, anomaly = err[labels == 0], err[labels == 1]
assert round(threshold, 6) == 0.002907
assert (int((anomaly > threshold).sum()), int((normal > threshold).sum()), int((anomaly <= threshold).sum())) == (16, 2, 0)
medians = [round(ns['test_error'][s].median().item(), 6) for s in (slice(0, 32), slice(32, None))]
assert medians == [0.000808, 0.106747], medians

rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(6.3, 2.4))
for row, values, color in [(1, normal, '#3b6ea8'), (0, anomaly, '#c2603e')]:
    jitter = rng.uniform(-0.18, 0.18, len(values))
    ax.scatter(values, row + jitter, s=16, color=color, alpha=0.85, linewidths=0)
ax.axvline(threshold, color='#b8892b', ls='--', lw=1.2)
ax.set_xscale('log')
ax.set(xlabel='lỗi tái tạo (log)', yticks=[0, 1], ylim=(-0.5, 1.5))
ax.set_yticklabels(['bất thường', 'bình thường'])
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.tight_layout()
write(fig, '3-10-errors')
print('reconstruction error figure verified', flush=True)
