"""Bài 7.3: lưới α của CTC cho target `a` trên bảng xác suất ba frame của bài; số lấy từ đúng hàm ctc_forward trong bài."""
from pathlib import Path
import re, io, contextlib, math
from svg import SVG, BLUE, CLAY, LINE, INK

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-7/7.3.md'
ns = {'__name__': 'ctc_dp_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
history = [[round(float(v), 2) for v in row] for row in ns['history']]
assert history == [[0.6, 0.4, 0.0], [0.3, 0.5, 0.2], [0.12, 0.48, 0.28]], history
assert round(float(ns['probability_a']), 2) == 0.76

s = SVG(640, 330)
xs = [235, 375, 515]
ys = [92, 172, 252]
r = 27
for j, x in enumerate(xs):
    s.text(x, 34, f't = {j + 1}', 18)
for i, (y, label) in enumerate(zip(ys, ['_', 'a', '_'])):
    s.text(118, y, label, 22)


def edge(t, a, b, color=INK):
    x1, y1, x2, y2 = xs[t], ys[a], xs[t + 1], ys[b]
    ang = math.atan2(y2 - y1, x2 - x1)
    s.arrow(x1 + (r + 3) * math.cos(ang), y1 + (r + 3) * math.sin(ang),
            x2 - (r + 4) * math.cos(ang), y2 - (r + 4) * math.sin(ang), color, 1.1)


for t in range(2):
    for a in range(3):
        if history[t][a] == 0:
            continue
        for b in (a, a + 1):
            if b < 3:
                edge(t, a, b, CLAY if t == 1 and b >= 1 else INK)
for t, row in enumerate(history):
    for a, value in enumerate(row):
        if value == 0:
            s.circle(xs[t], ys[a], r, LINE, 'none')
            s.text(xs[t], ys[a], '0', 16, color=LINE)
            continue
        final = t == 2 and a >= 1
        s.node(xs[t], ys[a], f'{value:.2f}', r, CLAY if final else BLUE, 16)
s.text(375, 307, 'P(a) = 0.48 + 0.28 = 0.76', 19, color=CLAY)
s.save('7-3-ctc-dp', 'Lưới α của target `a`: mỗi ô cộng các ô được phép đi tới ở frame trước rồi nhân xác suất frame; hai ô cuối cộng ra 0.76.')
print('ctc alpha lattice verified', flush=True)
