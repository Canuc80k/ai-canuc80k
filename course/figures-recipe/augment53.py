"""Bài 5.3: một ảnh chữ số 2 của tập train, bản dời 1 pixel và bản lật ngang, lấy từ đúng code của bài."""
from pathlib import Path
import re, io, contextlib
import torch
from svg import SVG, BLUE, CLAY

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-5/5.3.md'
ns = {'__name__': 'augment_figure'}
blocks = re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S)
with contextlib.redirect_stdout(io.StringIO()):
    for code in blocks:
        if 'def run(' in code:   # khối train bốn cấu hình không cần cho hình
            break
        exec(compile(code, str(p), 'exec'), ns)

train_x, train_y, shift = ns['train_x'], ns['train_y'], ns['shift']
assert tuple(ns['versions'].shape) == (5, 300, 1, 8, 8)
k = int(torch.nonzero(train_y == 2)[0])
original = train_x[k, 0]
moved = shift(train_x[k:k + 1], 0, 1)[0, 0]        # MOVES[0]: dời sang phải
flipped = original.flip(-1)
assert torch.equal(moved[:, 1:], original[:, :-1]) and float(moved[:, 0].abs().sum()) == 0
assert torch.equal(ns['versions'][1, k, 0], moved)

s = SVG(640, 270)
for j, (img, title, color) in enumerate([(original, 'Gốc', BLUE), (moved, 'Dời 1 pixel', BLUE),
                                          (flipped, 'Lật ngang', CLAY)]):
    x = 44 + j * 206
    s.text(x + 72, 30, title, 19)
    s.image(x, 56, 144, 144, img.tolist(), lo=0, hi=1, color=color)
    s.text(x + 72, 232, 'nhãn 2', 17)
s.save('5-3-digit-aug', 'Dời một pixel vẫn là chữ 2; lật ngang tạo một hình không còn là chữ 2 nhưng vẫn mang nhãn 2.')
print('digit augmentation figure verified, train index', k, flush=True)
