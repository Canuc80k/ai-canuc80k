"""Lượt 8 — hình chương 0 (bản gọn): mỗi hình một ý, chỉ giữ nhãn mắt cần, lời giải thích để ở caption và bài.
Chạy riêng: python -B -X utf8 p8_ch0.py [tên ...]"""
import sys
from kit import *

PAPER = 'var(--paper, var(--bg, #faf9f5))'
LOPC = {'10A1': BLUE, '10A2': GREEN, '10A3': CLAY, '10A4': SAND, 'A': BLUE, 'B': CLAY}


# ───────────────────────────── 0.1 Python ─────────────────────────────

def notebook():
    s = Fig(668, 150)
    steps = [('1. Chạy cả hai ô', '3', (True, True), '6', TEXT, False),
             ('2. Sửa n, chỉ chạy ô trên', '5', (True, False), '6', SAND, True),
             ('3. Chạy lại ô dưới', '5', (False, True), '15', GREEN, False)]
    for i, (title, n, ran, out, col, stale) in enumerate(steps):
        x = 6 + i * 224
        s.label(x + 2, 16, title, 13.5, 'start', TEXT, 600)
        s.cell(x, 34, 200, [f'n = {n}'], size=12, accent=BLUE if ran[0] else None)
        used = s.cell(x, 76, 200, ['total = sum(range(n + 1))'], size=12, accent=BLUE if ran[1] else None)
        oy = 76 + used + 20
        txt = f'total = {out}'
        s.mono(x + 12, oy, txt, 13, color=col, weight=600)
        if stale:
            s.pill(x + 12 + s.mono_width(txt, 13) + 10, oy, 'cũ', SAND, 11.5, 'start')
    s.save('0-1-notebook', 'Sửa n mà chưa chạy lại ô dưới thì total vẫn là 6.')


def floordiv():
    s = Fig(640, 200)
    X = lambda v: 360 + v * 50
    for y, expr, val, targets in [(78, '7 / 2', 3.5, [(3, GREEN, '3', 'end')]),
                                  (168, '−7 / 2', -3.5, [(-4, CLAY, 'Python  −4', 'end'), (-3, BLUE, 'C++  −3', 'start')])]:
        s.label(28, y, expr, 15, 'start', TEXT)
        s.line(X(-5.4), y, X(5.4), y, LINE, 1.2)
        for v in range(-5, 6):
            s.line(X(v), y - 4, X(v), y + 4, LINE, 1)
            s.label(X(v), y + 19, str(v).replace('-', '−'), 12)
        for tv, col, lab, anc in targets:
            x1, x2 = X(val), X(tv)
            s.path(f'M {x1:g},{y - 8:g} Q {(x1 + x2) / 2:g},{y - 46:g} {x2:g},{y - 9:g}', col, 1.6)
            a = 0.42
            import math as m
            ang = m.atan2((y - 9) - (y - 46), x2 - (x1 + x2) / 2)
            pts = [(x2 - 8 * m.cos(ang - a), y - 9 - 8 * m.sin(ang - a)), (x2 - 8 * m.cos(ang + a), y - 9 - 8 * m.sin(ang + a))]
            s.path(f'M {pts[0][0]:.1f},{pts[0][1]:.1f} L {x2:g},{y - 9:g} L {pts[1][0]:.1f},{pts[1][1]:.1f}', col, 1.6)
            s.circle(x2, y, 4.5, col, PAPER, 2)
            lx = (x1 + x2) / 2 + (-16 if anc == 'end' else 16)
            s.label(lx, y - 40, lab, 13.5, anc, col, 600)
        s.circle(X(val), y, 5, TEXT)
    s.save('0-1-floordiv', '// làm tròn xuống; phép chia nguyên của C++ cắt về 0.')


def float_grid():
    from decimal import Decimal
    s = Fig(640, 160)
    X = lambda k: 200 + k * 220
    y = 76
    s.line(X(-0.5), y, X(1.5), y, LINE, 1.2)
    for k in (-0.6, 1.6):
        s.label(X(k), y, '…', 14, color=FAINT)
    for k in (0, 1):
        s.line(X(k), y - 8, X(k), y + 8, LINE, 1.2)
    s.circle(X(0), y, 6, BLUE)
    s.circle(X(1), y, 6, CLAY)
    s.label(X(0), y - 44, '0.3', 15, color=BLUE, weight=600)
    s.mono(X(0), y - 24, f'{Decimal(0.3):.20f}', 11.5, 'middle', BLUE)
    s.label(X(1), y - 44, '0.1 + 0.2', 15, color=CLAY, weight=600)
    s.mono(X(1), y - 24, f'{Decimal(0.1 + 0.2):.20f}', 11.5, 'middle', CLAY)
    s.path(f'M {X(0)},{y + 22} L {X(0)},{y + 28} L {X(1)},{y + 28} L {X(1)},{y + 22}', MUTED, 1.1)
    s.label((X(0) + X(1)) / 2, y + 44, 'không có số float64 nào ở giữa', 12.5, color=MUTED)
    s.save('0-1-float', '0.3 và 0.1 + 0.2 rơi vào hai số float64 liền kề.')


def names():
    s = Fig(640, 188)
    panels = [(0, ['b = a', 'b.append(4)'], [('a', 0), ('b', 0)], [[1, 2, 3, 4]]),
              (214, ['c = a.copy()', 'c.append(4)'], [('a', 0), ('c', 1)], [[1, 2, 3], [1, 2, 3, 4]]),
              (428, ['y = x', 'y += 1'], [('x', 0), ('y', 1)], [[5], [6]])]
    for x0, code, nm, objs in panels:
        for i, line in enumerate(code):
            s.code(x0 + 24, 20 + i * 19, line, 13)
        oys = [84, 140] if len(objs) == 2 else [112]
        for k, vals in enumerate(objs):
            col = CLAY if k == 1 else BLUE
            s.tiles(x0 + 98, oys[k] - 14, [[str(v) for v in vals]], 24, 28, col, gap=2, size=13.5)
        for j, (n, tgt) in enumerate(nm):
            ny = 84 + j * 56
            s.box(x0 + 22, ny - 14, 30, 28, LINE, 'none', r=6, width=1.2)
            s.mono(x0 + 37, ny, n, 14, 'middle')
            col = BLUE if tgt == 0 else CLAY
            if len(objs) == 1:
                col = BLUE if j == 0 else CLAY
                ty = oys[0] + (-5 if j == 0 else 5)
            else:
                ty = oys[tgt]
            s.arrow(x0 + 55, ny, x0 + 94, ty, col, 1.3)
        if x0:
            s.line(x0 - 6, 14, x0 - 6, 176, SOFT_LINE, 1)
    s.save('0-1-names', 'Gán chỉ dán thêm tên; copy() tạo list mới; int bất biến.')


def grid_alias():
    s = Fig(640, 196)
    for x0, code, shared in [(14, '[[0] * 3] * 3', True), (334, '[[0] * 3 for _ in range(3)]', False)]:
        col = CLAY if shared else GREEN
        s.code(x0 + 10, 18, code, 13)
        ox, oy = x0 + 26, 46
        for i in range(3):
            s.box(ox, oy + i * 44, 34, 40, col, 'none', r=6, width=1.3)
            s.circle(ox + 17, oy + i * 44 + 20, 3.5, col)
        if shared:
            ry = oy + 44 + 6
            s.tiles(ox + 140, ry, [['9', '0', '0']], 32, 28, col, gap=2, size=14, fills={(0, 0): (col, .3)})
            for i in range(3):
                s.curve(ox + 21, oy + i * 44 + 20, ox + 136, ry + 14, bend=.12 * (1 - i), color=col, width=1.2)
        else:
            for i in range(3):
                vals = ['9', '0', '0'] if i == 0 else ['0', '0', '0']
                s.tiles(ox + 140, oy + i * 44 + 6, [vals], 32, 28, col, gap=2, size=14, fills={(0, 0): (col, .3)} if i == 0 else None)
                s.arrow(ox + 21, oy + i * 44 + 20, ox + 136, oy + i * 44 + 20, col, 1.2)
    s.line(322, 12, 322, 184, SOFT_LINE, 1)
    s.save('0-1-grid', 'Gán 9 vào ô đầu: bên trái cả ba hàng đổi, bên phải chỉ một hàng đổi.')


def lookup():
    s = Fig(640, 168)
    vals = [16, 26, 12, 5, 47]
    s.code(24, 20, '99 in list', 13)
    s.tiles(24, 52, [[str(v) for v in vals]], 44, 34, BLUE, gap=4, size=15)
    for i in range(5):
        s.label(24 + i * 48 + 22, 108, str(i + 1), 12.5, color=CLAY, weight=600)
    s.label(24 + 118, 140, '5 lần so', 14, color=CLAY, weight=600)
    X0 = 336
    s.code(X0, 20, '99 in set', 13)
    slots = [''] * 8
    for v in vals:
        slots[v % 8] = str(v)
    s.tiles(X0, 52, [slots], 32, 34, GREEN, gap=3, size=14, fills={(0, 3): (CLAY, .22)})
    s.label(X0 + 3 * 35 + 16, 108, 'hash(99) % 8 = 3', 12.5, color=CLAY)
    s.arrow(X0 + 3 * 35 + 16, 98, X0 + 3 * 35 + 16, 90, CLAY, 1.2)
    s.label(X0 + 4 * 35, 140, '1 lần nhìn', 14, color=GREEN, weight=600)
    s.line(312, 14, 312, 156, SOFT_LINE, 1)
    s.save('0-1-lookup', 'List so từng phần tử; set nhảy thẳng tới một ngăn của bảng băm.')


def default_arg():
    s = Fig(640, 176)
    s.code(24, 20, 'history=[]', 13)
    s.box(30, 52, 92, 40, LINE, 'none', r=8, width=1.2)
    s.mono(76, 72, 'add_score', 12.5, 'middle')
    s.tiles(176, 57, [['1', '2']], 30, 30, CLAY, gap=2, size=14)
    s.arrow(124, 72, 172, 72, CLAY, 1.3)
    for k, y in enumerate([124, 156]):
        s.code(30, y, f'add_score({k + 1})', 12.5)
        s.curve(140, y - 3, 191 + 32 * k, 90, bend=.15 if k == 0 else .08, color=CLAY, width=1.2)
    X = 340
    s.code(X, 20, 'history=None', 13)
    for k, y in enumerate([72, 124]):
        s.code(X + 4, y, f'add_score({k + 1})', 12.5)
        s.arrow(X + 118, y, X + 166, y, GREEN, 1.3)
        s.tiles(X + 172, y - 15, [[str(k + 1)]], 30, 30, GREEN, size=14)
    s.line(316, 12, 316, 166, SOFT_LINE, 1)
    s.save('0-1-default', 'List mặc định tạo một lần và dùng chung; None cho mỗi lần gọi một list mới.')


def class_fig():
    """0.1 mục Class: ba hàm đặc biệt và chỗ chúng xuất hiện lại trong PyTorch."""
    s = Fig(640, 206)
    s.t(24, 18, 'viết', 13.5, 'start', MUTED, font='sans')
    s.t(250, 18, 'Python gọi', 13.5, 'start', MUTED, font='sans')
    rows = [('len(ds)', 'ds.__len__()', None, 'Dataset'), ('ds[i]', 'ds.__getitem__(i)', None, 'Dataset'),
            ('model(x)', 'model.__call__(x)', 'forward(x)', 'nn.Module')]
    for k, (left, mid, right, tag) in enumerate(rows):
        y = 56 + k * 52
        s.box(18, y - 17, 150, 34, LINE, CODE_BG, r=8, width=1)
        s.code(32, y, left, 14)
        s.arrow(176, y, 236, y, CLAY, 1.4)
        s.code(250, y, mid, 14)
        if right:
            x0 = 250 + s.mono_width(mid, 14) + 10
            s.arrow(x0, y, x0 + 34, y, CLAY, 1.4)
            s.code(x0 + 44, y, right, 14, color=CLAY)
        s.pill(596, y, tag, BLUE if tag == 'Dataset' else CLAY, 12.5)
    s.save('0-1-class', 'Ba cú pháp và hàm đặc biệt mà chúng gọi.')


def traceback_fig():
    s = Fig(640, 222)
    lines = [('Traceback (most recent call last):', MUTED),
             ('  File "…/diem.py", line 7, in <module>', MUTED),
             ('    print(mean_of("Dũng"))', None),
             ('          ~~~~~~~^^^^^^^^', MUTED),
             ('  File "…/diem.py", line 4, in mean_of', MUTED),
             ('    marks = scores[name]', None),
             ('            ~~~~~~^^^^^^', CLAY),
             ("KeyError: 'Dũng'", CLAY)]
    x, y0, lh = 22, 24, 24
    s.box(10, 8, 330, lh * len(lines) + 8, 'none', CODE_BG, r=8, width=0)
    for i, (line, col) in enumerate(lines):
        y = y0 + i * lh
        if col is None:
            s.code(x, y, line, 12.5)
        else:
            s.mono(x, y, line, 12.5, color=col, weight=600 if line.startswith('KeyError') else 400)
    for a, b, text, col in [(7, 7, '① lỗi gì', CLAY), (4, 6, '② ở dòng nào', TEXT), (1, 3, '③ ai đã gọi', MUTED)]:
        ya, yb = y0 + a * lh - 8, y0 + b * lh + 8
        s.path(f'M 352,{ya:g} L 358,{ya:g} L 358,{yb:g} L 352,{yb:g}', col, 1.3)
        s.label(372, (ya + yb) / 2, text, 14, 'start', col, 600)
    s.arrow(520, y0 + 7 * lh, 520, y0 + 1 * lh, FAINT, 1.2)
    s.label(530, y0 + 4 * lh, 'đọc từ dưới lên', 12.5, 'start', MUTED)
    s.save('0-1-traceback', 'Traceback thật của Python 3.13: đọc từ dòng cuối lên.')


def bars(s, rows, X0, W, vmax, top, step, unit_label, ticks):
    for k, (label, v, col) in enumerate(rows):
        y = top + k * step
        s.code(X0 - 12 - s.mono_width(label, 12.5), y + 13, label, 12.5)
        w = max(3, W * v / vmax)
        s.box(X0, y, w, 26, 'none', col, r=4, width=0, opacity=.8)
        s.label(X0 + w + 8, y + 13, f'{v:.2f} ms', 13.5, 'start', TEXT)
    ya = top + len(rows) * step
    for t in ticks:
        s.label(X0 + W * t / vmax, ya + 4, str(t), 11.5, color=FAINT)
    s.label(X0 + W + 16, ya + 4, unit_label, 11.5, 'start', FAINT)


def speed():
    s = Fig(640, 150)
    bars(s, [('for i in range(n): s += i', 17.04, CLAY), ('sum(range(n))', 6.63, BLUE), ('np.arange(n).sum()', 0.26, GREEN)], 210, 330, 20, 18, 40, 'ms', [0, 5, 10, 15, 20])
    s.save('0-1-speed', 'Cùng một tổng của 500 000 số, đo trên một máy CPU.')


# ───────────────────────────── 0.2 NumPy ─────────────────────────────

def image_array():
    from sklearn.datasets import load_sample_image
    im = load_sample_image('china.jpg')            # (427, 640, 3) uint8; danielbuechele / Flickr, CC BY 2.0
    s = Fig(640, 210)
    px, py, pw = 14, 30, 276
    ph = pw * im.shape[0] / im.shape[1]
    s.photo(px, py, pw, ph, im, max_px=640, border=False, radius=8)
    r0, c0, k = 266, 196, 8
    sx, sy = px + c0 / im.shape[1] * pw, py + r0 / im.shape[0] * ph
    side = k / im.shape[1] * pw
    s.box(sx - 2, sy - 2, side + 4, side + 4, '#ffffff', 'none', r=1, width=1.6)
    s.mono(px, 14, '(427, 640, 3)', 13, color=MUTED)
    zx, zy, cell = 326, 30, 23
    patch = im[r0:r0 + k, c0:c0 + k]
    for i in range(k):
        for j in range(k):
            s.box(zx + j * cell, zy + i * cell, cell, cell, 'none', '#%02x%02x%02x' % tuple(int(v) for v in patch[i, j]), r=0, width=0)
    s.path(f'M {sx + side + 3:g},{sy - 2:g} L {zx:g},{zy:g} M {sx + side + 3:g},{sy + side + 2:g} L {zx:g},{zy + k * cell:g}', FAINT, 1, dash='3 3')
    hi, hj = 2, 7                                 # ô ở cột cuối để đường nối không cắt qua ô khác
    s.box(zx + hj * cell, zy + hi * cell, cell, cell, '#ffffff', 'none', r=0, width=2)
    R, G, B = (int(v) for v in patch[hi, hj])
    tx = 540
    s.line(zx + k * cell + 2, zy + (hi + .5) * cell, tx - 10, zy + (hi + .5) * cell, FAINT, 1)
    for n, (name, v, col) in enumerate([('R', R, '#c0392b'), ('G', G, '#3d8b40'), ('B', B, '#2f6fb5')]):
        y = zy + (hi + .5) * cell - 28 + n * 28
        s.label(tx, y, name, 13, 'start', col, 600)
        s.mono(tx + 20, y, str(v), 14)
    s.save('0-2-image', 'Ảnh màu là mảng (cao, rộng, 3): mỗi điểm ảnh là ba số R, G, B.')


def reshape_fig():
    s = Fig(640, 196)
    cw, gap = 30, 3
    x0 = (640 - 12 * (cw + gap)) / 2
    fill = lambda n: (BLUE, .07 + .05 * n)
    s.tiles(x0, 22, [[str(j) for j in range(12)]], cw, 28, BLUE, gap, {(0, j): fill(j) for j in range(12)}, 13.5)
    s.mono(x0 - 10, 36, '(12,)', 12.5, 'end', MUTED)
    for rows, cols, X in [(3, 4, 120), (2, 6, 380)]:
        vals = [[str(i * cols + j) for j in range(cols)] for i in range(rows)]
        s.tiles(X, 92, vals, cw, 28, BLUE, gap, {(i, j): fill(i * cols + j) for i in range(rows) for j in range(cols)}, 13.5)
        s.mono(X - 10, 106, f'({rows}, {cols})', 12.5, 'end', MUTED)
    s.save('0-2-reshape', 'Cùng 12 số, cùng thứ tự; reshape chỉ đổi cách chia hàng.')


def wrap():
    import math as m
    s = Fig(640, 210)
    cx, cy, r = 320, 108, 78
    s.circle(cx, cy, r, LINE, 'none', 1.4)
    ang = lambda v: -m.pi / 2 + 2 * m.pi * v / 256
    pt = lambda v, rr=r: (cx + rr * m.cos(ang(v)), cy + rr * m.sin(ang(v)))
    x1, y1 = pt(0, r - 6); x2, y2 = pt(0, r + 6)
    s.line(x1, y1, x2, y2, MUTED, 1.4)
    tx, ty = pt(0, r + 18)
    s.label(tx, ty, '0', 12.5)
    tx, ty = pt(255.5, r + 18)
    a0, a1 = ang(200), ang(300)
    pts = [(cx + (r - 14) * m.cos(a0 + (a1 - a0) * k / 40), cy + (r - 14) * m.sin(a0 + (a1 - a0) * k / 40)) for k in range(41)]
    s.path('M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts), CLAY, 2)
    (x, y), (xp, yp) = pts[-1], pts[-3]
    a = m.atan2(y - yp, x - xp)
    s.path(f'M {x - 8 * m.cos(a - .42):.1f},{y - 8 * m.sin(a - .42):.1f} L {x:.1f},{y:.1f} L {x - 8 * m.cos(a + .42):.1f},{y - 8 * m.sin(a + .42):.1f}', CLAY, 2)
    for v, col in [(200, BLUE), (44, CLAY)]:
        px_, py_ = pt(v)
        s.circle(px_, py_, 5.5, col)
        tx, ty = pt(v, r + 24)
        s.label(tx, ty, str(v), 15, color=col, weight=600)
    s.label(cx, cy, '+100', 15, color=CLAY)
    s.save('0-2-wrap', 'uint8 chạy trên một vòng 256 giá trị: 200 + 100 thành 44.')


def indexing():
    s = Fig(640, 150)
    exprs = [('a[1, 2]', {(1, 2)}, BLUE), ('a[:, 0]', {(0, 0), (1, 0), (2, 0)}, BLUE),
             ('a[-1, ::2]', {(2, 0), (2, 2)}, BLUE), ('a[a % 5 == 0]', {(0, 0), (1, 1), (2, 2)}, CLAY)]
    for k, (expr, sel, col) in enumerate(exprs):
        x0 = 20 + k * 156
        s.code(x0, 18, expr, 13)
        vals = [[str(i * 4 + j) for j in range(4)] for i in range(3)]
        s.tiles(x0, 40, vals, 30, 30, LINE, 3, {c: (col, .35) for c in sel}, 13, opacity=.25)
    s.save('0-2-indexing', 'Bốn cách lấy dữ liệu từ cùng một mảng 3 × 4.')


def speed02():
    s = Fig(640, 110)
    bars(s, [('[sigmoid(v) for v in zs]', 23.61, CLAY), ('1 / (1 + np.exp(-z))', 1.12, GREEN)], 210, 330, 25, 14, 40, 'ms', [0, 5, 10, 15, 20, 25])
    s.save('0-2-speed', 'Sigmoid của 200 000 số, đo trên một máy CPU.')


def view_copy():
    s = Fig(640, 168)
    x0, cw = 150, 44
    s.mono(x0 - 14, 50, 'a', 15, 'end', TEXT, 600)
    s.tiles(x0, 34, [['0', '100', '2', '3', '4', '5']], cw, 32, LINE, 3, {(0, 1): (BLUE, .3)}, 14, opacity=.25)
    s.box(x0 + cw + 1, 30, 3 * cw + 4, 40, BLUE, 'none', r=7, width=1.8)
    s.label(x0 + 2.5 * (cw + 3), 18, 's = a[1:4]  ·  dùng chung', 13, color=BLUE)
    fx = 360
    s.mono(fx - 14, 128, 'f', 15, 'end', CLAY, 600)
    s.tiles(fx, 112, [['-1', '2', '3']], cw, 32, CLAY, 3, {(0, 0): (CLAY, .3)}, 14)
    s.curve(x0 + 2.5 * (cw + 3), 76, fx + 1.5 * cw, 106, bend=-.15, color=CLAY, width=1.2, dash='4 3')
    s.label(fx + 1.5 * (cw + 3), 160, 'f = a[[1, 2, 3]]  ·  bản sao', 13, color=CLAY)
    s.save('0-2-view', 'Lát cắt là view của cùng vùng nhớ; fancy indexing chép ra bản sao.')


def axis_fig():
    import numpy as np
    sc = np.array([[9, 8, 7], [5, 6, 4], [4, 4, 5], [9, 8, 10], [7, 8, 10]], dtype=float)
    s = Fig(640, 232)
    x0, y0, cw, ch, g = 200, 16, 40, 28, 3
    s.tiles(x0, y0, [[f'{v:g}' for v in row] for row in sc], cw, ch, LINE, g, size=13.5, opacity=.25)
    by = y0 + 5 * (ch + g) + 22
    for j in range(3):
        s.arrow(x0 + j * (cw + g) + cw / 2, by - 18, x0 + j * (cw + g) + cw / 2, by - 4, BLUE, 1.2)
    s.tiles(x0, by, [[f'{v:g}' for v in sc.mean(axis=0)]], cw, ch, BLUE, g, size=13.5, opacity=.2)
    s.mono(x0 - 12, by + ch / 2, 'axis=0', 12.5, 'end', BLUE)
    rx = x0 + 3 * (cw + g) + 26
    for i in range(5):
        s.arrow(rx - 20, y0 + i * (ch + g) + ch / 2, rx - 4, y0 + i * (ch + g) + ch / 2, CLAY, 1.2)
    s.tiles(rx, y0, [[f'{v:.2f}'.rstrip('0').rstrip('.')] for v in sc.mean(axis=1)], 50, ch, CLAY, g, size=13.5, opacity=.2)
    s.mono(rx + 62, y0 + 2 * (ch + g) + ch / 2, 'axis=1', 12.5, 'start', CLAY)
    s.save('0-2-axis', 'Trục ghi trong axis là trục bị gộp và biến mất.')


def digits_axis():
    from sklearn.datasets import load_digits
    X = load_digits().images                      # (1797, 8, 8); UCI Optical Recognition of Handwritten Digits, CC BY 4.0
    s = Fig(640, 196)
    size, gap, x0, y0 = 42, 12, 96, 16
    for k in range(10):
        s.image(x0 + k * (size + gap), y0, size, size, X[k].tolist(), 0, 16, TEXT)
        s.mono(x0 + k * (size + gap) + size / 2, y0 + size + 16, f'{X[k].mean():.1f}', 12, 'middle', CLAY)
    s.mono(x0 - 14, y0 + size + 16, 'axis=(1, 2)', 12, 'end', CLAY)
    s.image(x0, 112, 66, 66, X.mean(axis=0).tolist(), 0, 16, BLUE)
    s.mono(x0 - 14, 145, 'axis=0', 12, 'end', BLUE)
    s.save('0-2-digits', '1797 chữ số viết tay 8 × 8: độ sáng từng ảnh và ảnh trung bình.')


def stack_fig():
    s = Fig(640, 196)
    cw, ch, g = 26, 18, 2
    s.label(150, 16, 'concatenate', 14, color=TEXT, weight=600)
    px, py = 50, 40
    s.tiles(px, py, [[''] * 3] * 2, cw, ch, BLUE, g, opacity=.3)
    s.tiles(px, py + 2 * (ch + g) + 12, [[''] * 3] * 3, cw, ch, CLAY, g, opacity=.3)
    s.arrow(px + 92, py + 58, px + 128, py + 58, FAINT, 1.2)
    rx = px + 142
    s.tiles(rx, py + 6, [[''] * 3] * 2, cw, ch, BLUE, g, opacity=.3)
    s.tiles(rx, py + 6 + 2 * (ch + g), [[''] * 3] * 3, cw, ch, CLAY, g, opacity=.3)
    s.mono(rx + 40, py + 5 * (ch + g) + 22, '(5, 3)', 12.5, 'middle')
    X = 360
    s.label(X + 120, 16, 'stack', 14, color=TEXT, weight=600)
    for k, col in enumerate([CLAY, BLUE]):
        ox, oy = X + 66 + (1 - k) * 26, 36 + k * 24
        s.box(ox - 3, oy - 3, 3 * (cw + g) + 4, 5 * (ch + g) + 4, 'none', PAPER, r=4, width=0)
        s.tiles(ox, oy, [[''] * 3] * 5, cw, ch, col, g, opacity=.3)
    s.mono(X + 130, 172, '(2, 5, 3)', 12.5, 'middle')
    s.line(320, 12, 320, 186, SOFT_LINE, 1)
    s.save('0-2-stack', 'concatenate nối trục đã có; stack thêm một trục mới.')


def broadcast_fig():
    s = Fig(640, 176)
    cw, ch, g = 38, 28, 3
    A, B = [0, 10, 20, 30], [0, 1, 2]
    ax, ay = 40, 30
    for i, v in enumerate(A):
        for j in range(3):
            real = j == 0
            s.box(ax + j * (cw + g), ay + i * (ch + g), cw, ch, BLUE if not real else 'none', BLUE, r=4, width=.9 if not real else 0, opacity=.25 if real else 0, dash=None if real else '3 3')
            s.t(ax + j * (cw + g) + cw / 2, ay + i * (ch + g) + ch / 2, str(v), 13.5, color=TEXT if real else FAINT, font='mono')
    bx = ax + 3 * (cw + g) + 40
    s.label(bx - 20, ay + 2 * (ch + g) - 2, '+', 20, color=TEXT)
    for j, v in enumerate(B):
        for i in range(4):
            real = i == 0
            s.box(bx + j * (cw + g), ay + i * (ch + g), cw, ch, CLAY if not real else 'none', CLAY, r=4, width=.9 if not real else 0, opacity=.25 if real else 0, dash=None if real else '3 3')
            s.t(bx + j * (cw + g) + cw / 2, ay + i * (ch + g) + ch / 2, str(v), 13.5, color=TEXT if real else FAINT, font='mono')
    rx = bx + 3 * (cw + g) + 40
    s.label(rx - 20, ay + 2 * (ch + g) - 2, '=', 20, color=TEXT)
    s.tiles(rx, ay, [[str(a + b) for b in B] for a in A], cw, ch, LINE, g, size=13.5, opacity=.25)
    for x, lab in [(ax + 1.5 * (cw + g), '(4, 1)'), (bx + 1.5 * (cw + g), '(3,)'), (rx + 1.5 * (cw + g), '(4, 3)')]:
        s.mono(x, ay + 4 * (ch + g) + 16, lab, 12.5, 'middle', MUTED)
    s.save('0-2-broadcast', 'Trục độ dài 1 được kéo dãn cho khớp; ô nét đứt không bị chép thật.')


def pairwise():
    s = Fig(640, 200)
    X = lambda x: 64 + x * 36
    Y = lambda y: 176 - y * 36
    A, B = [(0, 0), (3, 4)], [(0, 4), (3, 0)]
    s.path(f'M {X(0)},{Y(0)} L {X(0)},{Y(4)} L {X(3)},{Y(4)} L {X(3)},{Y(0)} Z', FAINT, 1, dash='3 3')
    for (x, y), lab in [((-0.35, 2), '4'), ((1.5, -0.45), '3'), ((1.5, 4.4), '3'), ((3.35, 2), '4')]:
        s.label(X(x), Y(y), lab, 12.5)
    for pts, col, nm in [(A, BLUE, 'A'), (B, CLAY, 'B')]:
        for i, (x, y) in enumerate(pts):
            s.circle(X(x), Y(y), 6, col)
            s.mono(X(x) + (-12 if x == 0 else 12), Y(y) + (12 if y == 0 else -12), f'{nm}{i}', 12.5, 'middle', col)
    gx, gy = 330, 50
    s.tiles(gx, gy, [['4', '3'], ['3', '4']], 70, 46, LINE, 4, size=16, opacity=.25)
    for j in range(2):
        s.mono(gx + j * 74 + 35, gy - 14, f'B{j}', 12.5, 'middle', CLAY)
        s.mono(gx - 14, gy + j * 50 + 23, f'A{j}', 12.5, 'end', BLUE)
    s.mono(gx + 72, gy + 118, 'D', 14, 'middle', TEXT, 600)
    s.save('0-2-pairwise', 'Ô (i, j) của D là khoảng cách từ Ai tới Bj.')


def mismatch():
    s = Fig(640, 186)
    cw, ch, g = 42, 32, 3
    gx, gy = 220, 50
    y = [1, 2, 3]
    for j, v in enumerate(y):
        s.mono(gx + j * (cw + g) + cw / 2, gy - 14, str(v), 13, 'middle', CLAY)
    for i, v in enumerate(y):
        s.mono(gx - 14, gy + i * (ch + g) + ch / 2, str(v), 13, 'end', BLUE)
    s.mono(gx + 1.5 * (cw + g), gy - 32, 'y  (3,)', 12.5, 'middle', CLAY)
    s.mono(gx - 34, gy + 1.5 * (ch + g), 'y_hat  (3, 1)', 12.5, 'end', BLUE)
    vals = [[f'{y[i] - y[j]:g}'.replace('-', '−') for j in range(3)] for i in range(3)]
    fills = {(i, j): ((GREEN, .3) if i == j else (CLAY, .12)) for i in range(3) for j in range(3)}
    s.tiles(gx, gy, vals, cw, ch, LINE, g, fills, 14)
    tx = gx + 3 * (cw + g) + 30
    s.mono(tx, gy + 32, 'MSE sai  1.333', 13, 'start', CLAY)
    s.mono(tx, gy + 58, 'MSE đúng 0', 13, 'start', GREEN)
    s.save('0-2-shape-mismatch', '(3, 1) − (3,) thành bảng 3 × 3; chỉ đường chéo là phần dư thật.')


def matmul():
    s = Fig(640, 176)
    cw, ch, g = 34, 32, 3
    def eq(x0, a, op, b, res, hl_a, hl_b, hl_r, col):
        s.tiles(x0, 50, a, cw, ch, LINE, g, {c: (col, .3) for c in hl_a}, 14, opacity=.25)
        x = x0 + len(a[0]) * (cw + g) + 14
        s.label(x, 50 + ch + 2, op, 17, color=TEXT)
        x += 14
        s.tiles(x, 50 + (0 if len(b) == 2 else ch / 2 + 2), b, cw, ch, LINE, g, {c: (col, .3) for c in hl_b}, 14, opacity=.25)
        x += len(b[0]) * (cw + g) + 14
        s.label(x, 50 + ch + 2, '=', 17, color=TEXT)
        x += 14
        s.tiles(x, 50, res, cw, ch, LINE, g, {c: (col, .3) for c in hl_r}, 14, opacity=.25)
    s.code(30, 20, 'M @ v', 14)
    eq(30, [['2', '1'], ['1', '3']], '@', [['1'], ['2']], [['4'], ['7']], {(0, 0), (0, 1)}, {(0, 0), (1, 0)}, {(0, 0)}, BLUE)
    s.mono(30, 140, '2·1 + 1·2 = 4', 13, 'start', BLUE)
    s.code(360, 20, 'M * v', 14)
    eq(360, [['2', '1'], ['1', '3']], '*', [['1', '2']], [['2', '2'], ['1', '6']], set(), {(0, 0), (0, 1)}, set(), CLAY)
    s.mono(360, 140, 'nhân từng ô', 13, 'start', CLAY)
    s.line(330, 12, 330, 166, SOFT_LINE, 1)
    s.save('0-2-matmul', '@ là tích vô hướng từng hàng; * nhân từng ô.')


def argsort_fig():
    """0.2 mục Sắp xếp: argsort trả về chỉ số; đọc scores theo các chỉ số ấy được dãy giảm dần."""
    s = Fig(640, 204)
    vals = [7.5, 9.0, 4.0, 9.0, 6.5]
    order = [1, 3, 0, 4, 2]
    cw, g, x0 = 56, 6, 196
    cx = lambda j: x0 + j * (cw + g) + cw / 2
    s.mono(x0 - 16, 46, 'scores', 13, 'end', MUTED)
    for j in range(5):
        s.mono(cx(j), 18, str(j), 12, 'middle', FAINT)
    s.tiles(x0, 30, [[f'{v:g}' for v in vals]], cw, 32, LINE, g, {}, 14)
    s.mono(x0 - 16, 156, 'scores[order]', 13, 'end', CLAY)
    s.mono(x0 - 16, 194, 'order', 12, 'end', CLAY)
    s.tiles(x0, 140, [[f'{vals[i]:g}' for i in order]], cw, 32, LINE, g, {(0, j): (CLAY, .14) for j in range(5)}, 14)
    for j, i in enumerate(order):
        s.curve(cx(i), 66, cx(j), 132, .0, CLAY, 1.1)
        s.mono(cx(j), 194, str(i), 12, 'middle', CLAY)
    s.save('0-2-argsort', 'Đọc scores theo order được dãy giảm dần.')


def rng_fig():
    s = Fig(640, 160)
    tape = [0, 7, 6, 4, 4, 8, 0, 6, 2, 0]
    cw, g = 30, 3
    x0 = 160
    s.mono(x0 - 16, 40, 'seed 42', 12.5, 'end', MUTED)
    s.tiles(x0, 24, [[str(v) for v in tape]], cw, 32, LINE, g, {(0, j): ((BLUE, .25) if j < 5 else (CLAY, .25)) for j in range(10)}, 14)
    s.label(x0 + 10 * (cw + g) + 6, 40, '…', 16, 'start')
    s.label(x0 + 2.5 * (cw + g), 74, 'a', 14, color=BLUE, weight=600)
    s.label(x0 + 7.5 * (cw + g), 74, 'b', 14, color=CLAY, weight=600)
    s.mono(x0 - 16, 120, 'seed 42', 12.5, 'end', MUTED)
    s.tiles(x0, 104, [[str(v) for v in tape[:5]]], cw, 32, LINE, g, {(0, j): (BLUE, .25) for j in range(5)}, 14)
    s.label(x0 + 5 * (cw + g) + 12, 120, 'bắt đầu lại', 13, 'start', BLUE)
    s.save('0-2-rng', 'Seed cố định cả dãy; mỗi lần gọi lấy phần tiếp theo.')


# ───────────────────────────── 0.3 pandas ─────────────────────────────

def folder03():
    """0.3 mục dữ liệu không phải bảng: đọc ảnh theo thứ tự của labels.csv."""
    s = Fig(640, 196)
    disk = [('c.png', 120), ('a.png', 40), ('b.png', 200)]
    table = [('a.png', 'toi'), ('b.png', 'sang'), ('c.png', 'vua')]
    gray = lambda v: f'#{v:02x}{v:02x}{v:02x}'
    s.mono(40, 22, 'images/', 13, 'start', MUTED)
    s.mono(232, 22, 'labels.csv', 13, 'start', MUTED)
    s.mono(470, 22, 'X[i], y[i]', 13, 'start', CLAY)
    ys = [52 + k * 48 for k in range(3)]
    for k, (name, v) in enumerate(disk):
        s.box(40, ys[k] - 15, 30, 30, LINE, gray(v), r=4, width=1)
        s.mono(80, ys[k] + 4, name, 13, 'start', TEXT)
    for k, (name, lab) in enumerate(table):
        s.box(224, ys[k] - 15, 168, 30, SOFT_LINE, CODE_BG, r=6, width=1)
        s.mono(238, ys[k] + 4, name, 13, 'start', TEXT)
        s.mono(326, ys[k] + 4, lab, 13, 'start', BLUE)
        j = [n for n, _ in disk].index(name)
        s.curve(140, ys[j], 218, ys[k], .0, FAINT, 1.1)
        v = dict(disk)[name]
        s.box(470, ys[k] - 15, 30, 30, LINE, gray(v), r=4, width=1)
        s.mono(512, ys[k] + 4, lab, 13, 'start', CLAY)
        s.curve(398, ys[k], 462, ys[k], .0, CLAY, 1.1)
    s.mono(470, 190, 'shape (3, 3, 4)', 12, 'start', MUTED)
    s.save('0-3-folder', 'Đọc ảnh theo cột file của labels.csv: ảnh thứ i luôn đi với nhãn thứ i.')


def data03():
    """Dữ liệu giả lập đúng như ô đầu của bài 0.3 (seed 7)."""
    import numpy as np, pandas as pd
    rng = np.random.default_rng(7)
    n = 500
    lop = rng.choice(['10A1', '10A2', '10A3', '10A4'], size=n)
    gio = rng.gamma(2.0, 3.0, n).round(1)
    hk1 = np.clip(rng.normal(6.5, 1.3, n), 0, 10).round(1)
    bonus = pd.Series(lop).map({'10A1': 0.6, '10A2': 0.0, '10A3': -0.3, '10A4': 0.2}).to_numpy()
    toan = np.clip(0.55 * hk1 + 0.12 * gio + bonus + rng.normal(0, 0.8, n) + 2.0, 0, 10).round(2)
    gio[rng.random(n) < 0.06] = np.nan
    full = pd.DataFrame({'id': np.arange(1, n + 1), 'lop': lop, 'gio_tu_hoc': gio, 'diem_hk1': hk1, 'diem_toan': toan})
    return full.iloc[:400].copy(), full.iloc[400:].drop(columns='diem_toan').copy()


def table(s, x, y, header, rows, widths, hl=None, rh=22, size=12, name=None):
    """Bảng gọn: tiêu đề nền nhạt, không kẻ lưới trong. hl: {cột: màu}."""
    hl = hl or {}
    if name:
        s.mono(x, y - 12, name, 12.5, 'start', TEXT, 600)
    W = sum(widths)
    s.box(x, y, W, rh, 'none', CODE_BG, r=5, width=0)
    cx = x
    for j, w in enumerate(widths):
        if j in hl:
            s.box(cx, y, w, rh * (len(rows) + 1), 'none', hl[j], r=4, width=0, opacity=.13)
        s.mono(cx + 6, y + rh / 2, header[j], size, color=hl.get(j, MUTED))
        for i, row in enumerate(rows):
            v, col = row[j] if isinstance(row[j], tuple) else (row[j], TEXT)
            s.mono(cx + 6, y + rh * (i + 1.5), v, size, color=col)
        cx += w
    return W


def files03():
    s = Fig(640, 212)
    table(s, 14, 30, ['id', 'lop', 'gio', 'hk1', 'diem_toan'], [['1', '10A4', '0.4', '9.1', '6.72'], ['…', '', '', '', '']],
          [36, 50, 46, 46, 82], hl={4: CLAY}, name='train.csv')
    table(s, 14, 130, ['id', 'lop', 'gio', 'hk1'], [['401', '10A2', 'NaN', '7.1'], ['…', '', '', '']],
          [42, 50, 46, 46], name='test.csv')
    table(s, 450, 30, ['lop', 'chuyen', 'si_so'], [['10A1', 'True', '38'], ['…', '', '']], [50, 58, 52], name='lop.csv')
    table(s, 450, 130, ['id', 'diem_toan'], [['401', '0.0'], ['…', '']], [44, 82], hl={1: CLAY}, name='sample_submission.csv')
    s.curve(278, 60, 446, 60, bend=0, color=FAINT, width=1.1, dash='4 3')
    s.label(362, 50, 'lop', 12.5, color=MUTED)
    s.curve(200, 160, 446, 160, bend=0, color=FAINT, width=1.1, dash='4 3')
    s.label(323, 150, 'id', 12.5, color=MUTED)
    s.save('0-3-files', 'Bốn file của đề và hai khóa ghép: lop và id.')


def dataframe03():
    tr, _ = data03()
    s = Fig(640, 188)
    cols = ['id', 'lop', 'gio_tu_hoc', 'diem_hk1', 'diem_toan']
    widths = [46, 64, 96, 82, 84]
    rows = []
    for _, r in tr.head(4).iterrows():
        g = 'NaN' if r['gio_tu_hoc'] != r['gio_tu_hoc'] else f"{r['gio_tu_hoc']:g}"
        rows.append([str(r['id']), r['lop'], (g, SAND) if g == 'NaN' else g, f"{r['diem_hk1']:g}", f"{r['diem_toan']:.2f}"])
    x0, y0, rh = 100, 40, 24
    W = table(s, x0, y0, cols, rows, widths, hl={2: BLUE}, rh=rh, size=12.5)
    for i in range(4):
        s.mono(x0 - 12, y0 + rh * (i + 1.5), str(i), 12.5, 'end', FAINT)
    cx = x0
    for w, d in zip(widths, ['int64', 'object', 'float64', 'float64', 'float64']):
        s.mono(cx + 6, y0 + 5 * rh + 14, d, 11.5, color=FAINT)
        cx += w
    s.label(x0 - 12, y0 - 14, 'index', 12.5, 'end', MUTED)
    s.label(x0 + 46 + 64 + 48, y0 - 14, 'Series', 12.5, 'middle', BLUE)
    s.label(x0 + W + 14, y0 + rh * 4.5, 'NaN: ô thiếu', 12.5, 'start', SAND)
    s.label(x0 + W + 14, y0 + 5 * rh + 14, 'dtype', 12.5, 'start', MUTED)
    s.save('0-3-dataframe', 'DataFrame: index, các cột Series, mỗi cột một dtype.')


def skew03():
    import numpy as np
    tr, _ = data03()
    g = tr['gio_tu_hoc'].dropna().to_numpy()
    s = Fig(640, 200)
    bins = np.arange(0, 25.5, 1.5)
    hist, _ = np.histogram(g, bins)
    X = lambda v: 80 + v * 20
    Y = lambda c: 166 - c * 1.7
    for k, c in enumerate(hist):
        s.box(X(bins[k]) + 1.5, Y(c), 30 - 3, 166 - Y(c), 'none', BLUE, r=3, width=0, opacity=.4)
    for t in range(0, 25, 5):
        s.label(X(t), 182, str(t), 12, color=FAINT)
    s.label(X(24) + 18, 182, 'giờ', 12, 'start', FAINT)
    med, mean = float(np.median(g)), float(g.mean())
    for v, col, lab, anc, dx in [(med, GREEN, f'median {med:.1f}', 'end', -6), (mean, CLAY, f'mean {mean:.2f}', 'start', 6)]:
        s.line(X(v), 14, X(v), 166, col, 1.6, dash='5 3' if col == CLAY else None)
        s.label(X(v) + dx, 14, lab, 13, anc, col, 600)
    s.save('0-3-skew', 'Giờ tự học lệch phải: đuôi dài kéo mean lên trên median.')


def chained03():
    s = Fig(640, 176)
    s.code(20, 18, 'df[mask]["col"] = 0', 13)
    s.tiles(40, 46, [['6.7'], ['5.5'], ['8.1']], 60, 28, LINE, 3, {(1, 0): (CLAY, .14), (2, 0): (CLAY, .14)}, size=13.5, opacity=.25)
    s.path('M 106,78 L 112,78 L 112,138 L 106,138', CLAY, 1.2)
    s.box(170, 82, 72, 52, CLAY, 'none', r=6, width=1.2, dash='4 3')
    s.mono(206, 108, '0, 0', 13, 'middle', CLAY)
    s.arrow(114, 108, 166, 108, CLAY, 1.2)
    s.label(206, 148, 'bảng tạm, bị bỏ', 12.5, color=CLAY)
    s.label(70, 156, 'df không đổi', 13, color=MUTED)
    X = 350
    s.code(X, 18, 'df.loc[mask, "col"] = 0', 13)
    s.tiles(X + 80, 46, [['6.7'], ['0'], ['0']], 60, 28, LINE, 3, {(1, 0): (GREEN, .3), (2, 0): (GREEN, .3)}, 13.5, opacity=.25)
    s.label(X + 110, 156, 'sửa thẳng df', 13, color=GREEN)
    s.line(322, 12, 322, 166, SOFT_LINE, 1)
    s.save('0-3-chained', 'Gán nối chuỗi rơi vào bảng tạm; một lần loc sửa thẳng bảng gốc.')


def fill03():
    s = Fig(640, 180)
    rows = [('10A4', None), ('10A2', None), ('10A1', 5.2), ('10A1', None), ('10A5', None)]
    med = {'10A1': 4.2, '10A2': 4.4, '10A3': 4.7, '10A4': 4.45}
    x0, y0, rh = 110, 16, 30
    for i, (l, v) in enumerate(rows):
        y = y0 + i * rh + rh / 2
        col = LOPC.get(l, MUTED)
        s.mono(x0, y, l, 13, color=col)
        s.mono(x0 + 62, y, 'NaN' if v is None else f'{v:g}', 13, color=SAND if v is None else TEXT)
        new = v if v is not None else med.get(l, 4.4)
        s.arrow(x0 + 108, y, x0 + 190, y, (col if l in med else FAINT) if v is None else SOFT_LINE, 1.1, dash=None if (v is None and l in med) else '3 3')
        s.mono(x0 + 200, y, f'{new:g}', 13, color=GREEN if v is None else TEXT, weight=600 if v is None else 400)
        if v is None and l not in med:
            s.label(x0 + 240, y, 'median chung', 12.5, 'start', MUTED)
    s.box(470, 40, 140, 112, 'none', CODE_BG, r=8, width=0)
    s.label(540, 24, 'median từ train', 12.5, color=MUTED)
    for k, (l, m) in enumerate(med.items()):
        s.mono(486, 62 + k * 22, f'{l}  {m:g}', 12.5, color=LOPC[l])
    s.save('0-3-fillna', 'Ô thiếu nhận median của lớp mình; lớp lạ nhận median chung.')


def align03():
    s = Fig(640, 160)
    rh = 34
    left = [(10, '101'), (20, '102'), (30, '103')]
    right = [(30, '6.0'), (10, '7.0'), (20, '8.0')]
    cols = {10: BLUE, 20: GREEN, 30: CLAY}
    score = dict((k, v) for k, v in right)
    s.label(140, 14, 'tiny', 13, color=MUTED)
    s.label(470, 14, 'values', 13, color=MUTED)
    for i, (ix, idv) in enumerate(left):
        y = 30 + i * rh
        s.mono(80, y + rh / 2 - 2, str(ix), 13, 'end', cols[ix], 600)
        s.box(88, y, 120, rh - 6, 'none', cols[ix], r=6, width=0, opacity=.12)
        s.mono(98, y + rh / 2 - 2, idv, 13)
        s.mono(150, y + rh / 2 - 2, score[ix], 13, color=cols[ix], weight=600)
    for i, (ix, v) in enumerate(right):
        y = 30 + i * rh
        s.mono(440, y + rh / 2 - 2, str(ix), 13, 'end', cols[ix], 600)
        s.box(448, y, 60, rh - 6, 'none', cols[ix], r=6, width=0, opacity=.12)
        s.mono(462, y + rh / 2 - 2, v, 13)
        j = [l[0] for l in left].index(ix)
        s.curve(412, y + rh / 2 - 2, 212, 30 + j * rh + rh / 2 - 2, bend=0, color=cols[ix], width=1.2)
    s.save('0-3-align', 'pandas ghép theo nhãn index, không theo vị trí.')


def groupby03():
    tr, _ = data03()
    sub = tr.head(8)
    means = tr.groupby('lop')['diem_toan'].mean()
    s = Fig(640, 250)
    x0, y0, rh = 40, 48, 24
    s.label(150, 12, 'transform: 400 dòng', 13, color=MUTED)
    for hx, h in [(x0 + 10, 'lop'), (x0 + 80, 'điểm'), (x0 + 160, 'TB lớp')]:
        s.label(hx, y0 - 14, h, 11.5, 'start', FAINT)
    s.label(500, 12, 'agg: 4 dòng', 13, color=MUTED)
    for i, (_, r) in enumerate(sub.iterrows()):
        y = y0 + i * rh
        col = LOPC[r['lop']]
        s.box(x0, y, 230, rh - 4, 'none', col, r=5, width=0, opacity=.13)
        s.mono(x0 + 10, y + rh / 2 - 2, r['lop'], 12.5, color=col)
        s.mono(x0 + 80, y + rh / 2 - 2, f"{r['diem_toan']:.2f}", 12.5)
        s.mono(x0 + 160, y + rh / 2 - 2, f"{means[r['lop']]:.2f}", 12.5, color=col, weight=600)
    for k, (l, m) in enumerate(means.items()):
        y = 50 + k * 36
        col = LOPC[l]
        s.box(430, y, 140, 28, 'none', col, r=6, width=0, opacity=.15)
        s.mono(444, y + 14, l, 13, color=col)
        s.mono(520, y + 14, f'{m:.2f}', 13, weight=600)
    s.save('0-3-groupby', 'transform giữ mọi dòng; agg thu về một dòng mỗi lớp.')


def merge03():
    s = Fig(640, 196)
    rh = 30
    left = [('1', 'A'), ('2', 'A'), ('3', 'B')]
    right = [('A', '38'), ('A', '38'), ('B', '42')]
    out = [('1', 'A', '38'), ('1', 'A', '38'), ('2', 'A', '38'), ('2', 'A', '38'), ('3', 'B', '42')]
    def row(x, y, cells, key):
        s.box(x, y, 22 + 36 * len(cells), rh - 6, 'none', LOPC[key], r=6, width=0, opacity=.14)
        for k, c in enumerate(cells):
            s.mono(x + 12 + 36 * k, y + rh / 2 - 3, c, 13, color=LOPC[key] if c == key else TEXT)
    s.label(70, 14, '3 dòng', 13, color=MUTED)
    s.label(250, 14, 'A lặp', 13, color=CLAY)
    s.label(530, 14, '5 dòng', 13, color=CLAY, weight=600)
    for i, (a, b) in enumerate(left):
        row(30, 30 + i * rh, [a, b], b)
    for i, (a, b) in enumerate(right):
        row(210, 30 + i * rh, [a, b], a)
    for i, (_, b) in enumerate(left):
        for j, (a, _) in enumerate(right):
            if a == b:
                s.line(126, 30 + i * rh + 12, 206, 30 + j * rh + 12, LOPC[b], 1, dash='3 3')
    for i, cells in enumerate(out):
        row(470, 30 + i * rh, list(cells), cells[1])
    s.arrow(318, 75, 456, 75, FAINT, 1.2)
    s.save('0-3-merge', 'Khóa lặp ở bảng phải làm left merge nhân bản dòng.')


def submission03():
    s = Fig(640, 160)
    rh = 34
    pred = [('403', '6.414'), ('402', '6.579'), ('401', '5.964')]
    samp = ['401', '402', '403']
    cols = {'401': BLUE, '402': GREEN, '403': CLAY}
    s.label(100, 14, 'dự đoán (đã đảo)', 13, color=MUTED)
    s.label(530, 14, 'file nộp theo sample', 13, color=MUTED)
    for i, (a, v) in enumerate(pred):
        y = 30 + i * rh
        s.box(40, y, 120, rh - 8, 'none', cols[a], r=6, width=0, opacity=.14)
        s.mono(52, y + rh / 2 - 4, a, 13, color=cols[a])
        s.mono(100, y + rh / 2 - 4, v, 13)
    for i, a in enumerate(samp):
        y = 30 + i * rh
        j = [p[0] for p in pred].index(a)
        s.box(470, y, 120, rh - 8, 'none', cols[a], r=6, width=0, opacity=.14)
        s.mono(482, y + rh / 2 - 4, a, 13, color=cols[a])
        s.mono(530, y + rh / 2 - 4, dict(pred)[a], 13)
        s.curve(164, 30 + j * rh + 13, 466, y + 13, bend=0, color=cols[a], width=1.2)
    s.save('0-3-submission', 'Ghép theo id vào khung sample: đúng học sinh, đúng thứ tự.')


FIGS = {f.__name__: f for f in []}
FIGS = {
    '0-1-notebook': notebook, '0-1-floordiv': floordiv, '0-1-float': float_grid, '0-1-names': names, '0-1-grid': grid_alias,
    '0-1-lookup': lookup, '0-1-default': default_arg, '0-1-traceback': traceback_fig, '0-1-class': class_fig, '0-1-speed': speed,
    '0-2-image': image_array, '0-2-reshape': reshape_fig, '0-2-wrap': wrap, '0-2-indexing': indexing, '0-2-speed': speed02,
    '0-2-view': view_copy, '0-2-axis': axis_fig, '0-2-digits': digits_axis, '0-2-stack': stack_fig, '0-2-broadcast': broadcast_fig,
    '0-2-pairwise': pairwise, '0-2-shape-mismatch': mismatch, '0-2-matmul': matmul, '0-2-rng': rng_fig, '0-2-argsort': argsort_fig,
    '0-3-files': files03, '0-3-dataframe': dataframe03, '0-3-skew': skew03, '0-3-chained': chained03, '0-3-fillna': fill03,
    '0-3-align': align03, '0-3-groupby': groupby03, '0-3-merge': merge03, '0-3-folder': folder03, '0-3-submission': submission03,
}

if __name__ == '__main__':
    names_ = sys.argv[1:] or list(FIGS)
    for n in names_:
        FIGS[n]()
        print('ok', n)
