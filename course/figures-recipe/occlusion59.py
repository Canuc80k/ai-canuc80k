"""Bài 5.9: ba đầu vào occlusion và xác suất lớp 1 của hai model, lấy từ đúng code của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from svg import SVG, BLUE, CLAY, INK

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-5/5.9.md'
ns = {'__name__': 'occlusion_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
batch, score_a, score_b = ns['batch'], ns['score_a'], ns['score_b']
assert batch.shape == (3, 8, 8) and ns['labels'][1] == 1
assert score_a.round(4).tolist() == [0.891, 0.1057, 0.891]
assert score_b.round(4).tolist() == [0.9589, 0.9589, 0.4995]

s = SVG(640, 268)
size, cell, top = 112, 14, 54
covers = [None, (0, 0, 2, 2), (2, 2, 4, 4)]          # (hàng, cột, cao, rộng) của vùng bị che
for i, (title, cover) in enumerate(zip(['Gốc', 'Che góc', 'Che nét'], covers)):
    x = 62 + i * 204
    s.text(x + size / 2, 26, title, 19)
    s.image(x, top, size, size, np.clip(batch[i], 0, 1).tolist(), lo=0, hi=1, color=BLUE)
    if cover:
        r, c, h, w = cover
        s.rect(x + c * cell, top + r * cell, w * cell, h * cell, CLAY, width=1.8)
    for k, (name, scores) in enumerate([('A', score_a), ('B', score_b)]):
        value = round(float(scores[i]), 4)
        dropped = value < scores[0] - 0.2
        s.text(x + size / 2, top + size + 30 + k * 28, f'{name}  {value:g}', 17, color=CLAY if dropped else INK)
s.save('5-9-occlusion-scores', 'Che góc kéo xác suất lớp 1 của A xuống; che nét kéo xác suất của B xuống.')
print('occlusion scores verified', flush=True)
