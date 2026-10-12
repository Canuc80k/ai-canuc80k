"""Buổi kt2: ba vùng quyết định của head đặt tay và bốn mẫu, lấy từ đúng pipeline nhỏ của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
import torch
from matplotlib.patches import Polygon
from matplotlib.path import Path as MplPath
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-4/kt2.md'
ns = {'__name__': 'kt2_regions_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
X = ns['features'].numpy()
y = np.asarray(ns['targets'])
pred = np.asarray(ns['predictions'])
W = ns['head'].weight.detach().numpy()
assert X.tolist() == [[2, 0], [0, 2], [-1, -1], [1.5, 0]]
assert y.tolist() == [0, 1, 2, 1] and pred.tolist() == [0, 1, 2, 0]
assert W.tolist() == [[1, 0], [0, 1], [-1, -1]]

colors = ['#c2603e', '#3b6ea8', '#b8892b']
L = 2.6
# Ba biên là ba tia từ gốc: x1 = x2 (lớp 0/1), x2 = -2 x1 (lớp 0/2), x1 = -2 x2 (lớp 1/2).
polys = [[(0, 0), (L / 2, -L), (L, -L), (L, L)],
         [(0, 0), (L, L), (-L, L), (-L, L / 2)],
         [(0, 0), (-L, L / 2), (-L, -L), (L / 2, -L)]]
g = np.linspace(-2.5, 2.5, 100)
grid = np.array([(a + .013, b + .029) for a in g for b in g])  # lệch hai trục khác nhau: không điểm nào nằm đúng trên biên
with torch.inference_mode():
    region = ns['head'](torch.tensor(grid, dtype=torch.float32)).argmax(1).numpy()
for k, poly in enumerate(polys):
    inside = MplPath(poly).contains_points(grid)
    assert (region[inside] == k).all() and inside.sum() > 1000

fig, ax = plt.subplots(figsize=(4.4, 3.9))
for k, poly in enumerate(polys):
    ax.add_patch(Polygon(poly, closed=True, facecolor=colors[k], edgecolor='none', alpha=.13))
for end in [(L, L), (L / 2, -L), (-L, L / 2)]:
    ax.plot([0, end[0]], [0, end[1]], color='#1f1e1c', lw=.8, alpha=.55)
for k in range(3):
    ok = (y == k) & (pred == y)
    ax.scatter(X[ok, 0], X[ok, 1], s=70, color=colors[k], zorder=4)
bad = pred != y
ax.scatter(X[bad, 0], X[bad, 1], s=95, facecolors='none', edgecolors=colors[int(y[bad][0])], linewidths=2.2, zorder=5)
for k, (tx, ty) in enumerate([(2.0, 1.2), (-1.2, 2.1), (-1.8, -1.8)]):
    ax.text(tx, ty, f'vùng {k}', color=colors[k], fontsize=11, ha='center', va='center')
ax.set(xlabel='đặc trưng 1', ylabel='đặc trưng 2', xlim=(-2.6, 2.6), ylim=(-2.6, 2.6), aspect='equal')
fig.tight_layout()
write(fig, '4-kt2-regions')
print('kt2 regions verified', flush=True)
