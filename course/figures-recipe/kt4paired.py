"""Buổi kt4: đúng/sai theo từng ID của ba cấu hình (ảnh, chữ, fusion), lấy từ đúng code đọc lỗi của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from matplotlib.patches import Rectangle
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-7/kt4.md'
ns = {'__name__': 'kt4_paired_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
img, txt, fus = ns['image_ok'], ns['text_ok'], ns['fusion_ok']
assert len(img) == 25 and (img.mean(), txt.mean(), fus.mean()) == (0.80, 0.76, 0.84)
fixed = np.flatnonzero(~img & fus).tolist()
broken = np.flatnonzero(img & ~fus).tolist()
common = np.flatnonzero(~img & ~txt & ~fus).tolist()
assert (fixed, broken, common) == ([3, 11, 17], [8, 21], [5, 14])
assert ((img | txt).mean()) == 0.92  # trần của hỏi nhanh: chỉ 5 và 14 cả hai nhánh cùng sai

INK, BLUE, CLAY = '#1f1e1c', '#3b6ea8', '#c2603e'
fig, ax = plt.subplots(figsize=(6.3, 1.9))
rows = [('ảnh', img), ('chữ', txt), ('fusion', fus)]
for r, (name, ok) in enumerate(rows):
    y = len(rows) - 1 - r
    for i, good in enumerate(ok):
        edge, face = INK, (INK if good else 'none')
        if name == 'fusion' and i in fixed:
            edge = face = BLUE
        if name == 'fusion' and i in broken:
            edge, face = CLAY, 'none'
        ax.add_patch(Rectangle((i + 0.1, y + 0.1), 0.8, 0.8, facecolor=face, edgecolor=edge,
                               lw=1.6 if edge != INK else 0.8, alpha=0.85 if face == INK else 1))
ax.set(xlim=(0, 25), ylim=(0, 3))
ax.set_yticks([2.5, 1.5, 0.5])
ax.set_yticklabels([n for n, _ in rows])
ticks = sorted(fixed + broken + common)
ax.set_xticks([t + 0.5 for t in ticks])
ax.set_xticklabels([str(t) for t in ticks])
ax.tick_params(length=0)
for side in ('left', 'bottom'):
    ax.spines[side].set_visible(False)
ax.set_aspect('equal')
ax.set_xlabel('ID mẫu validation')
fig.tight_layout()
write(fig, '7-kt4-paired')
print('kt4 paired figure verified', flush=True)
