"""Bài 3.8: RNN đọc câu "dp" đã pad tới độ dài 3; trạng thái cần lấy là h1, cột cuối h3 đã đi qua hai PAD."""
from pathlib import Path
import re, io, contextlib
from svg import SVG, BLUE, CLAY, LINE, INK

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-3/3.8.md'
ns = {'__name__': 'rnn_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
assert ns['ids'][1].tolist() == [3, 0, 0] and ns['lengths'].tolist() == [2, 1, 3]
same = ns['torch'].isclose(ns['last_column'], ns['last_valid']).all(dim=1).tolist()
assert same == [False, False, True]

s = SVG(640, 250)
xs = [215, 365, 515]
s.text(80, 112, 'h₀ = 0', 18)
s.arrow(118, 112, 181, 112)
for i, (x, tok) in enumerate(zip(xs, ['dp', 'PAD', 'PAD'])):
    color = CLAY if i == 0 else INK
    s.node(x, 112, f'h{"₁₂₃"[i]}', 30, color, 20)
    pad = i > 0
    s.rect(x - 40, 186, 80, 40, BLUE if not pad else LINE, LINE if pad else 'none', opacity=.14 if pad else 1)
    s.text(x, 206, tok, 18)
    s.arrow(x, 184, x, 146, INK if not pad else LINE)
    if i < 2:
        s.arrow(x + 32, 112, xs[i + 1] - 34, 112)
s.text(xs[0], 34, 'lengths − 1', 18, color=CLAY)
s.arrow(xs[0], 50, xs[0], 76, CLAY)
s.text(xs[2], 34, 'outputs[:, -1]', 18)
s.arrow(xs[2], 50, xs[2], 76)
s.save('3-8-rnn-pad', 'Câu “dp” dài 1: trạng thái cần đọc là h₁; cột cuối h₃ đã đi qua hai PAD.')
print('rnn pad figure verified', flush=True)
