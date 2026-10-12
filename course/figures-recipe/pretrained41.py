"""Bài 4.1: một mẫu đi qua gói checkpoint nhỏ của bài; số lấy từ đúng code của bài (x = (12, 8))."""
from pathlib import Path
import re, io, contextlib
from svg import SVG, BLUE, CLAY, INK

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-4/4.1.md'
ns = {'__name__': 'pretrained_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
raw, loaded, logits = ns['raw'], ns['loaded'], ns['logits']
z = ns['process'](raw[:1])[0]
assert raw[0].tolist() == [12., 8.]
assert loaded['mean'].tolist() == [10., 10.] and loaded['scale'].tolist() == [2., 2.]
assert z.tolist() == [1., -1.]
assert [round(v, 2) for v in logits[0].tolist()] == [2., -2., .25]
k = int(logits[0].argmax())
assert k == 0 and loaded['labels'][k] == 'hoat_dong_A'

s = SVG(640, 330)
cx, ys = 320, [30, 120, 210, 300]
values = ['x = (12, 8)', 'z = (1, −1)', 'ℓ = (2, −2, 0.25)', 'hoat_dong_A']
for i, (y, v) in enumerate(zip(ys, values)):
    s.rect(cx - 115, y - 23, 230, 46, CLAY if i == 3 else BLUE, radius=5)
    s.text(cx, y, v, 20)
steps = [('processor', '(x − mean) / scale'), ('state_dict', 'W z + b'), ('labels', 'argmax = 0 → labels[0]')]
for (a, b), (name, op) in zip(zip(ys, ys[1:]), steps):
    s.arrow(cx, a + 28, cx, b - 28, CLAY)
    mid = (a + b) / 2
    s.text(cx - 22, mid, name, 18, 'end', CLAY)
    s.text(cx + 22, mid, op, 17, 'start')
s.save('4-1-flow', 'Một mẫu đi qua ba phần của gói: processor, trọng số trong state_dict, rồi bảng nhãn.')
print('pretrained flow figure verified', flush=True)
