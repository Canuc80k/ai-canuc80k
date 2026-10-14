"""Lượt 10 (14/10/2026) — hình cho các bài toán mới của chương 0 (0.4–0.7).
Mỗi hình một ý; số liệu tính lại bằng NumPy ngay trong hàm, khớp với code của bài.
Chạy riêng: python -B -X utf8 p10_math.py [tên ...]"""
import sys
import numpy as np
from kit import *

PAPER = 'var(--paper, var(--bg, #faf9f5))'


def _plot(ax, f, a, b, color, width=2, n=200, dash=None):
    xs = np.linspace(a, b, n)
    ax.line(xs, f(xs), color, width, dash=dash)


# ───────────────────────────── 0.4 Hàm số, mũ và log ─────────────────────────────

def explog():
    s = Fig(640, 300)
    ax = s.axes(170, 14, 300, 260, (-3, 4.5), (-3, 4.5), grid=False, frame=False)
    s.line(ax.X(-3), ax.Y(0), ax.X(4.5), ax.Y(0), LINE, 1)
    s.line(ax.X(0), ax.Y(-3), ax.X(0), ax.Y(4.5), LINE, 1)
    for v in (2, 3, 4):
        s.label(ax.X(v), ax.Y(0) + 14, str(v), 11, color=FAINT)
        s.label(ax.X(0) - 8, ax.Y(v), str(v), 11, 'end', FAINT)
    ax.line([-3, 4.5], [-3, 4.5], FAINT, 1.2, dash='4 4')
    _plot(ax, np.exp, -3, np.log(4.5), CLAY)
    _plot(ax, np.log, np.exp(-3), 4.5, BLUE)
    s.circle(ax.X(0), ax.Y(1), 4, CLAY)
    s.circle(ax.X(1), ax.Y(0), 4, BLUE)
    s.label(ax.X(1.05), ax.Y(3.9), 'eˣ', 16, 'end', CLAY, 600)
    s.label(ax.X(4.3), ax.Y(1.75), 'log x', 15, 'end', BLUE, 600)
    s.label(ax.X(4.4), ax.Y(3.5), 'y = x', 12, 'end', FAINT)
    s.label(ax.X(0) - 8, ax.Y(1), '(0, 1)', 12, 'end', CLAY)
    s.label(ax.X(1), ax.Y(0) + 16, '(1, 0)', 12, 'middle', BLUE)
    s.save('0-4-explog', 'eˣ và log x đối xứng qua đường y = x.')


def sigmoid04():
    sig = lambda z: 1 / (1 + np.exp(-z))
    s = Fig(640, 230)
    ax = s.axes(80, 18, 480, 170, (-7, 7), (0, 1), xticks=[-6, -4, -2, 0, 2, 4, 6], yticks=[0, .5, 1], xlabel='z')
    s.line(ax.X(0), ax.Y(0), ax.X(0), ax.Y(1), SOFT_LINE, 1)
    _plot(ax, sig, -7, 7, BLUE)
    for z in (-2, 0, 2):
        p = sig(z)
        s.line(ax.X(z), ax.Y(0), ax.X(z), ax.Y(p), FAINT, 1, dash='3 3')
        s.circle(ax.X(z), ax.Y(p), 4.5, CLAY)
        s.label(ax.X(z) + (10 if z >= 0 else -10), ax.Y(p) + (12 if z >= 0 else -12), f'{p:.2f}', 12.5, 'start' if z >= 0 else 'end', CLAY, 600)
    s.label(ax.X(7), ax.Y(1) - 12, 'σ(z)', 14, 'end', BLUE, 600)
    s.save('0-4-sigmoid', 'Sigmoid đưa mọi z vào khoảng (0, 1); σ(0) = 0.5.')


def softmax04():
    z = np.array([2.0, 1.0, 0.0])
    e = np.exp(z)
    p = e / e.sum()
    names = ['mèo', 'chó', 'chim']
    s = Fig(640, 236)
    cols = [(40, 'logits', z, 2.2, lambda v: f'{v:g}'), (250, 'eᶻ', e, 8, lambda v: f'{v:.2f}'), (460, 'chia tổng', p, .75, lambda v: f'{v:.2f}')]
    base = 176
    for x0, title, vals, top, fmt in cols:
        s.label(x0 + 70, 18, title, 14, color=TEXT, weight=600)
        s.line(x0, base, x0 + 140, base, LINE, 1)
        for k, v in enumerate(vals):
            h = v / top * 130
            bx = x0 + 10 + k * 44
            col = [BLUE, CLAY, SAND][k]
            s.box(bx, base - h, 32, h, col, col, r=3, width=0, opacity=.75)
            s.label(bx + 16, base - h - 10, fmt(v), 12, color=col, weight=600)
            s.label(bx + 16, base + 16, names[k], 12, color=MUTED)
    for x in (196, 406):
        s.arrow(x, 110, x + 34, 110, MUTED, 1.4)
    s.label(530, 222, f'tổng = {e.sum():.2f} → 1', 12, color=FAINT)
    s.save('0-4-softmax', 'Softmax: lấy mũ từng logit rồi chia cho tổng.')


def logloss04():
    s = Fig(640, 236)
    ax = s.axes(80, 18, 480, 170, (0, 1), (0, 5), xticks=[0, .25, .5, .75, 1], yticks=[0, 1, 2, 3, 4, 5],
                xlabel='p cho đáp án đúng', ylabel='−log p')
    _plot(ax, lambda p: -np.log(p), np.exp(-5), 1, CLAY, n=400)
    for p in (.9, .5, .1):
        L = -np.log(p)
        s.circle(ax.X(p), ax.Y(L), 4.5, CLAY)
        s.label(ax.X(p) + (4 if p < .8 else -4), ax.Y(L) - 16, f'p = {p:g}: {L:.2f}', 12.5, 'start' if p < .8 else 'end', TEXT)
    s.save('0-4-logloss', '−log p: gần 0 khi p sát 1, tăng vọt khi p tiến về 0.')


# ───────────────────────────── 0.5 Vector và ma trận ─────────────────────────────

def _plane(s, x, y, w, h, lim, ticks=True):
    ax = s.axes(x, y, w, h, lim[0], lim[1], grid=False, frame=False)
    for v in range(int(lim[0][0]), int(lim[0][1]) + 1):
        s.line(ax.X(v), ax.Y(lim[1][0]), ax.X(v), ax.Y(lim[1][1]), SOFT_LINE, .7)
    for v in range(int(lim[1][0]), int(lim[1][1]) + 1):
        s.line(ax.X(lim[0][0]), ax.Y(v), ax.X(lim[0][1]), ax.Y(v), SOFT_LINE, .7)
    s.line(ax.X(lim[0][0]), ax.Y(0), ax.X(lim[0][1]), ax.Y(0), LINE, 1.1)
    s.line(ax.X(0), ax.Y(lim[1][0]), ax.X(0), ax.Y(lim[1][1]), LINE, 1.1)
    return ax


def _vec(s, ax, x0, y0, x1, y1, col, width=2.2, dash=None):
    s.arrow(ax.X(x0), ax.Y(y0), ax.X(x1), ax.Y(y1), col, width, dash)


def vector05():
    s = Fig(640, 250)
    ax = _plane(s, 30, 14, 260, 210, ((-0.5, 4.5), (-0.5, 3.5)))
    a, b = (3, 1), (1, 2)
    _vec(s, ax, 0, 0, *a, BLUE)
    _vec(s, ax, 0, 0, *b, SAND)
    _vec(s, ax, a[0], a[1], a[0] + b[0], a[1] + b[1], SAND, 1.6, '5 4')
    _vec(s, ax, 0, 0, a[0] + b[0], a[1] + b[1], CLAY)
    s.label(ax.X(3) + 6, ax.Y(1) + 14, 'a = (3, 1)', 13, 'start', BLUE, 600)
    s.label(ax.X(1) - 6, ax.Y(2) - 8, 'b = (1, 2)', 13, 'end', SAND, 600)
    s.label(ax.X(4) - 6, ax.Y(3) - 12, 'a + b = (4, 3)', 13, 'end', CLAY, 600)
    ax2 = _plane(s, 350, 14, 260, 210, ((-0.5, 6.5), (-0.5, 3.5)))
    _vec(s, ax2, 0, 0, 6, 2, CLAY, 2.2)
    _vec(s, ax2, 0, 0, 3, 1, BLUE, 3.2)
    s.label(ax2.X(3), ax2.Y(1) + 18, 'a', 14, 'middle', BLUE, 600)
    s.label(ax2.X(6) - 4, ax2.Y(2) - 14, '2a = (6, 2)', 13, 'end', CLAY, 600)
    s.save('0-5-vector', 'Cộng hai vector là nối đuôi chúng; nhân với 2 kéo dài mũi tên gấp đôi.')


def dot05():
    s = Fig(640, 210)
    cases = [((3, 1), (2, 2), 'cùng hướng'), ((2, 1), (-1, 2), 'vuông góc'), ((3, 1), (-2, -1), 'ngược hướng')]
    for k, (a, b, name) in enumerate(cases):
        x0 = 14 + k * 210
        ax = _plane(s, x0 + 20, 14, 160, 130, ((-3.2, 3.2), (-2.2, 2.6)))
        _vec(s, ax, 0, 0, *a, BLUE)
        _vec(s, ax, 0, 0, *b, CLAY)
        for v, col, n in ((a, BLUE, 'a'), (b, CLAY, 'b')):
            s.label(ax.X(v[0] * 1.12), ax.Y(v[1] * 1.12) + (4 if v[1] < 0 else -4), n, 13, 'middle', col, 600)
        d = a[0] * b[0] + a[1] * b[1]
        s.label(x0 + 100, 166, name, 13.5, color=TEXT, weight=600)
        s.label(x0 + 100, 188, f'a · b = {d}'.replace('-', '−'), 13, color=[GREEN, MUTED, CLAY][k], weight=600)
    s.save('0-5-dot', 'a · b dương khi cùng hướng, bằng 0 khi vuông góc, âm khi ngược hướng.')


def matmul05():
    X = np.array([[6.0, 7.5, 1.0], [2.0, 6.0, 4.0], [10.0, 8.5, 0.0], [4.0, 5.5, 2.0]])
    W = np.array([[0.1, -0.2], [0.8, 0.5], [-0.3, 0.4]])
    H = X @ W
    f = lambda v: f'{v:g}'.replace('-', '−')
    s = Fig(640, 210)
    i, j = 1, 1
    cw, ch, gap = 42, 30, 3
    y0 = 46
    s.label(20 + 1.5 * (cw + gap), 22, 'X  (4, 3)', 13, color=TEXT, weight=600)
    s.tiles(20, y0, [[f(v) for v in r] for r in X], cw, ch, BLUE, gap, {(i, c): (CLAY, .28) for c in range(3)}, size=13)
    s.label(176, y0 + 2 * (ch + gap), '@', 18, color=MUTED)
    s.label(200 + (cw + gap), 22, 'W  (3, 2)', 13, color=TEXT, weight=600)
    s.tiles(200, y0, [[f(v) for v in r] for r in W], cw, ch, SAND, gap, {(r, j): (CLAY, .28) for r in range(3)}, size=13)
    s.label(310, y0 + 2 * (ch + gap), '=', 18, color=MUTED)
    s.label(340 + (cw + gap), 22, 'H  (4, 2)', 13, color=TEXT, weight=600)
    s.tiles(340, y0, [[f(round(v, 2)) for v in r] for r in H], cw + 6, ch, GREEN, gap, {(i, j): (CLAY, .45)}, size=13)
    terms = ' + '.join(f'{f(X[i, c])}·' + (f'({f(W[c, j])})' if W[c, j] < 0 else f(W[c, j])) for c in range(3))
    parts = terms.split(' + ')
    yc = y0 + i * (ch + gap) + ch / 2
    s.label(458, yc, '←', 14, 'start', CLAY)
    s.mono(476, yc - 18, parts[0] + ' + ' + parts[1], 12, 'start', CLAY)
    s.mono(476, yc, '+ ' + parts[2], 12, 'start', CLAY)
    s.mono(476, yc + 18, f'= {f(round(H[i, j], 2))}', 12, 'start', CLAY)
    s.save('0-5-matmul', '(4, 3) @ (3, 2) → (4, 2): ô tô đậm là tích của hàng tô đậm với cột tô đậm.')


def transform05():
    M = np.array([[2.0, 1.0], [0.0, 1.0]])
    sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
    img = sq @ M.T
    s = Fig(640, 230)
    ax = _plane(s, 170, 14, 300, 190, ((-0.5, 3.5), (-0.4, 1.8)))
    poly = lambda P: 'M ' + ' L '.join(f'{ax.X(x):.1f},{ax.Y(y):.1f}' for x, y in P) + ' Z'
    s.path(poly(sq), BLUE, 1.6, 'none')
    s.path(poly(sq), 'none', 0, BLUE, opacity=.12)
    s.path(poly(img), CLAY, 1.6, 'none')
    s.path(poly(img), 'none', 0, CLAY, opacity=.12)
    _vec(s, ax, 0, 0, 1, 0, BLUE, 2.4)
    _vec(s, ax, 0, 0, 0, 1, BLUE, 2.4)
    _vec(s, ax, 0, 0, *img[1], CLAY, 2.4)
    _vec(s, ax, 0, 0, *img[3], CLAY, 2.4)
    s.label(ax.X(2), ax.Y(0) + 16, '(2, 0)', 12.5, 'middle', CLAY, 600)
    s.label(ax.X(1) + 8, ax.Y(1) - 10, '(1, 1)', 12.5, 'start', CLAY, 600)
    s.label(ax.X(0) - 8, ax.Y(1), '(0, 1)', 12.5, 'end', BLUE, 600)
    s.label(ax.X(1), ax.Y(0) + 16, '(1, 0)', 12.5, 'middle', BLUE, 600)
    s.mono(500, 80, 'M = [[2, 1],', 13, 'start', TEXT)
    s.mono(500, 98, '     [0, 1]]', 13, 'start', TEXT)
    s.save('0-5-transform', 'Cột của M là nơi (1, 0) và (0, 1) đi tới.')


# ───────────────────────────── 0.6 Đạo hàm và gradient ─────────────────────────────

def tangent06():
    f = lambda x: x ** 2
    s = Fig(640, 250)
    ax = s.axes(90, 14, 460, 196, (0, 4.6), (0, 18), xticks=[0, 1, 2, 3, 4], yticks=[0, 4, 8, 12, 16], xlabel='x')
    _plot(ax, f, 0, 4.25, TEXT, 2)
    for h, col, op in [(1, SAND, 1), (.5, BLUE, 1)]:
        k = (f(3 + h) - f(3)) / h
        xs = np.array([1.6, 4.4])
        ax.line(xs, f(3) + k * (xs - 3), col, 1.5, dash='5 4')
        s.circle(ax.X(3 + h), ax.Y(f(3 + h)), 4, col)
        s.label(110, 24 + (0 if h == 1 else 20), f'h = {h:g}: độ dốc {k:g}', 12.5, 'start', col, 600)
    xs = np.array([1.6, 4.4])
    ax.line(xs, 9 + 6 * (xs - 3), CLAY, 2)
    s.label(110, 64, 'tiếp tuyến: độ dốc 6', 12.5, 'start', CLAY, 600)
    s.circle(ax.X(3), ax.Y(9), 5, CLAY)
    s.label(ax.X(3) - 8, ax.Y(9) - 4, '(3, 9)', 12.5, 'end', CLAY, 600)
    s.label(ax.X(1.2), ax.Y(f(1.2)) - 12, 'x²', 14, 'middle', TEXT, 600)
    s.save('0-6-tangent', 'Đường nối hai điểm xoay về tiếp tuyến khi h nhỏ dần; độ dốc tiến về f′(3) = 6.')


def chain06():
    s = Fig(640, 176)
    nodes = [(60, 'w', '1'), (275, 'ŷ = wx', '2'), (530, 'L = (ŷ − y)²', '−16')]
    vals = ['w = 1', 'ŷ = 2', 'L = 16']
    y = 76
    for (x, t, _), v in zip(nodes, vals):
        w = 50 if len(t) < 3 else (110 if len(t) < 8 else 140)
        s.box(x - w / 2, y - 22, w, 44, BLUE, SURFACE, r=8, width=1.4)
        s.t(x, y, t, 16, color=TEXT)
        s.label(x, y + 40, v, 12.5, color=MUTED)
    s.arrow(90, y, 214, y, MUTED, 1.4)
    s.arrow(336, y, 454, y, MUTED, 1.4)
    s.label(152, y - 34, '∂ŷ/∂w = x = 2', 12.5, color=CLAY, weight=600)
    s.label(395, y - 34, '∂L/∂ŷ = 2(ŷ − y) = −8', 12.5, color=CLAY, weight=600)
    s.label(320, 156, '∂L/∂w = 2 · (−8) = −16', 14, color=CLAY, weight=700)
    s.save('0-6-chain', 'Từ w tới loss qua hai bước; đạo hàm của loss theo w là tích đạo hàm của từng bước.')


def gradient06():
    s = Fig(640, 280)
    ax = s.axes(190, 14, 260, 250, (-2.6, 2.6), (-2.5, 2.5), grid=False, frame=False)
    sx = ax.w / 5.2
    for r in (0.5, 1.0, 1.5, 2.0, 2.5):
        s.circle(ax.X(0), ax.Y(0), r * sx, SOFT_LINE if r != 2.5 else SOFT_LINE, 'none', 1.2)
    s.line(ax.X(-2.6), ax.Y(0), ax.X(2.6), ax.Y(0), LINE, 1)
    s.line(ax.X(0), ax.Y(-2.5), ax.X(0), ax.Y(2.5), LINE, 1)
    for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False) + .3:
        px, py = 1.5 * np.cos(ang), 1.5 * np.sin(ang)
        gx, gy = 2 * px * .25, 2 * py * .25
        s.circle(ax.X(px), ax.Y(py), 3, TEXT)
        s.arrow(ax.X(px), ax.Y(py), ax.X(px + gx), ax.Y(py + gy), BLUE, 1.6)
    px, py = 1.0, 2.0
    s.circle(ax.X(px), ax.Y(py) , 4, CLAY)
    s.arrow(ax.X(px), ax.Y(py), ax.X(px - .5 * px), ax.Y(py - .5 * py), CLAY, 2)
    s.label(ax.X(px) + 8, ax.Y(py) - 6, '(1, 2)', 12.5, 'start', CLAY, 600)
    s.label(ax.X(.5) - 6, ax.Y(1.0) + 12, '−∇f', 13, 'end', CLAY, 600)
    s.label(520, 60, '∇f = (2x, 2y)', 13, 'start', BLUE, 600)
    s.label(520, 82, 'chỉ ra xa đáy', 12.5, 'start', MUTED)
    s.save('0-6-gradient', 'Bát x² + y²: gradient (2x, 2y) chỉ ra xa đáy, vuông góc với các vòng đồng mức; −∇f chỉ về đáy.')


def descent06():
    x, y = 2.0, 6.0
    L = lambda w: (w * x - y) ** 2
    def path(eta, steps, w=0.0):
        out = [w]
        for _ in range(steps):
            w = w - eta * 2 * (w * x - y) * x
            out.append(w)
        return out
    s = Fig(640, 250)
    for k, (eta, steps, lim, col, title) in enumerate([(.05, 6, (-1, 7), BLUE, 'η = 0.05'), (.3, 3, (-4, 13), CLAY, 'η = 0.3')]):
        x0 = 50 + k * 310
        top = L(lim[1]) if k == 0 else 820
        ax = s.axes(x0, 30, 250, 170, lim, (0, top), xticks=[0, 3, 6] if k == 0 else [-3, 0, 3, 6, 9, 12], yticks=None, xlabel='w', grid=False)
        _plot(ax, L, lim[0], lim[1], LINE, 1.6)
        ws = path(eta, steps)
        for a, b in zip(ws, ws[1:]):
            s.line(ax.X(a), ax.Y(min(L(a), top)), ax.X(b), ax.Y(min(L(b), top)), col, 1.2, dash='3 3')
        for i, w in enumerate(ws):
            s.circle(ax.X(w), ax.Y(min(L(w), top)), 4 if i else 5, col)
        s.label(x0 + 125, 16, title, 14, color=col, weight=600)
        s.line(ax.X(3), ax.Y(0), ax.X(3), ax.Y(0) - 6, TEXT, 1.4)
    s.label(205, 232, f'{path(.05, 6)[-1]:.2f} sau 6 bước', 12.5, color=BLUE)
    s.label(515, 232, '0 → 7.2 → −2.88 → 11.23', 12.5, color=CLAY)
    s.save('0-6-descent', 'Learning rate 0.05 đi dần xuống đáy w = 3; learning rate 0.3 nhảy qua đáy và văng ra xa hơn sau mỗi bước.')


# ───────────────────────────── 0.7 Xác suất và thống kê ─────────────────────────────

def bayes07():
    s = Fig(640, 250)
    def node(x, y, w, top, bottom, col, fill=None):
        s.box(x - w / 2, y - 22, w, 44, col, fill or SURFACE, r=8, width=1.4)
        s.t(x, y - 7, top, 15, color=TEXT, weight=600)
        s.label(x, y + 11, bottom, 11.5, color=MUTED)
    node(320, 30, 120, '10 000', 'người', LINE)
    node(160, 110, 120, '100', 'có bệnh (1%)', CLAY)
    node(480, 110, 120, '9 900', 'khỏe', BLUE)
    s.arrow(290, 52, 190, 87, MUTED, 1.2)
    s.arrow(350, 52, 450, 87, MUTED, 1.2)
    leaves = [(90, '95', 'dương (95%)', CLAY, True), (230, '5', 'âm', CLAY, False),
              (410, '495', 'dương nhầm (5%)', BLUE, True), (550, '9 405', 'âm', BLUE, False)]
    for x, top, bottom, col, pos in leaves:
        px = 160 if x < 320 else 480
        s.arrow(px + (x - px) * .3, 132, x, 167, MUTED, 1.1)
        node(x, 190, 110, top, bottom, col if pos else LINE)
        if pos:
            s.box(x - 55, 168, 110, 44, 'none', col, r=8, width=0, opacity=.12)
    s.label(320, 238, 'dương tính: 95 + 495 = 590 người, có bệnh 95/590 ≈ 0.16', 13, color=CLAY, weight=600)
    s.save('0-7-bayes', '10 000 người: 95 người bệnh dương tính và 495 người khỏe dương tính nhầm; trong 590 kết quả dương chỉ 16% là bệnh thật.')


def normal07():
    pdf = lambda z: np.exp(-z * z / 2) / np.sqrt(2 * np.pi)
    s = Fig(640, 230)
    ax = s.axes(70, 20, 500, 170, (-3.6, 3.6), (0, .43), xticks=None, yticks=None, grid=False)
    for k, (lo, col, op) in enumerate([(2, BLUE, .12), (1, BLUE, .22)]):
        zs = np.linspace(-lo, lo, 120)
        d = f'M {ax.X(-lo):.1f},{ax.Y(0):.1f} ' + ' '.join(f'L {ax.X(z):.1f},{ax.Y(pdf(z)):.1f}' for z in zs) + f' L {ax.X(lo):.1f},{ax.Y(0):.1f} Z'
        s.path(d, 'none', 0, col, opacity=op)
    _plot(ax, pdf, -3.6, 3.6, TEXT, 1.8)
    for z, t in [(-3, 'μ−3σ'), (-2, 'μ−2σ'), (-1, 'μ−σ'), (0, 'μ'), (1, 'μ+σ'), (2, 'μ+2σ'), (3, 'μ+3σ')]:
        s.line(ax.X(z), ax.Y(0), ax.X(z), ax.Y(0) + 5, LINE, 1)
        s.label(ax.X(z), ax.Y(0) + 18, t, 11.5, color=FAINT)
    s.label(ax.X(0), ax.Y(.17), '68%', 15, color=BLUE, weight=700)
    for z in (-1.5, 1.5):
        s.label(ax.X(z), ax.Y(.035), '13.5%', 11.5, color=BLUE)
    s.label(ax.X(0), ax.Y(0) - 12, '← 95% từ μ−2σ đến μ+2σ →', 11.5, color=BLUE)
    s.save('0-7-normal', 'Phân phối chuẩn: 68% giá trị trong μ ± σ, 95% trong μ ± 2σ.')


def se07():
    rng = np.random.default_rng(1)
    p = .85
    s = Fig(640, 250)
    ax = s.axes(70, 20, 500, 170, (.76, .94), (0, 1), xticks=[.78, .8, .82, .84, .86, .88, .9, .92], yticks=None, grid=False, xlabel='accuracy đo được', xfmt='{:.2f}')
    for n, col, op in [(200, CLAY, .4), (2000, BLUE, .65)]:
        acc = rng.binomial(n, p, size=10_000) / n
        bins = np.arange(.7575, .9426, .005)
        h, _ = np.histogram(acc, bins)
        h = h / h.max()
        for k, v in enumerate(h):
            if v:
                x0 = ax.X(bins[k]) + .5
                s.box(x0, ax.Y(v * .92), ax.X(bins[k + 1]) - x0 - .5, ax.Y(0) - ax.Y(v * .92), 'none', col, r=0, width=0, opacity=op)
        lo, hi = np.percentile(acc, [2.5, 97.5])
        y = ax.Y(.97) if n == 200 else ax.Y(.97) - 0
    s.line(ax.X(p), ax.Y(0), ax.X(p), ax.Y(1), TEXT, 1.2, dash='4 3')
    s.label(ax.X(p) + 6, ax.Y(1) + 2, 'thật 0.85', 12, 'start', TEXT)
    s.label(ax.X(.775), ax.Y(.55), 'n = 200', 13, 'start', CLAY, 600)
    s.label(ax.X(.875), ax.Y(.75), 'n = 2000', 13, 'start', BLUE, 600)
    s.save('0-7-se', 'Accuracy đo được của cùng một model (thật 0.85) trên 10 000 bộ validation: 200 ảnh dao động rộng, 2000 ảnh hẹp hơn khoảng ba lần.')


FIGS = {
    '0-4-explog': explog, '0-4-sigmoid': sigmoid04, '0-4-softmax': softmax04, '0-4-logloss': logloss04,
    '0-5-vector': vector05, '0-5-dot': dot05, '0-5-matmul': matmul05, '0-5-transform': transform05,
    '0-6-tangent': tangent06, '0-6-chain': chain06, '0-6-gradient': gradient06, '0-6-descent': descent06,
    '0-7-bayes': bayes07, '0-7-normal': normal07, '0-7-se': se07,
}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
