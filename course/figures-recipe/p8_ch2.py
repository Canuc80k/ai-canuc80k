"""Lượt 8 — hình chương 2 (bản gọn). Số liệu lấy từ code bài hoặc từ bản chụp matplotlib cũ trong capture/.
Chạy riêng: python -B -X utf8 p8_ch2.py [tên ...]"""
import math, pickle, sys
from pathlib import Path
import numpy as np
from kit import *
from p8_ch1 import lesson_ns

PAPER = 'var(--paper, var(--bg, #faf9f5))'
CAP = Path(__file__).resolve().parent / 'capture'


def cap(name):
    import matplotlib
    matplotlib.use('Agg')
    with (CAP / f'{name}.pickle').open('rb') as f:
        return pickle.load(f)


def sup(n):
    return str(n).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))


# ───────────────────────────── 2.1 ─────────────────────────────

def residuals21():
    a = cap('2-1-residuals').axes[0]
    pts = a.collections[0].get_offsets()
    line = a.lines[0]
    xs, ys = line.get_xdata(), line.get_ydata()
    w = (ys[-1] - ys[0]) / (xs[-1] - xs[0]); b = ys[0] - w * xs[0]
    s = Fig(640, 230)
    ax = s.axes(60, 20, 480, 170, (0, 10), (-1, 12), xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 4, 8, 12], xlabel='x')
    ax.line([0, 10], [b, b + 10 * w], TEXT, 1.6)
    for x, y in pts:
        yh = w * x + b
        s.line(ax.X(x), ax.Y(y), ax.X(x), ax.Y(yh), CLAY, 1.6)
        s.circle(ax.X(x), ax.Y(y), 4.5, BLUE)
    s.mono(ax.X(10) + 8, ax.Y(b + 10 * w), 'ŷ = wx + b', 12.5, 'start', TEXT)
    x0, y0 = pts[9]
    s.label(ax.X(x0) - 8, (ax.Y(y0) + ax.Y(w * x0 + b)) / 2, 'phần dư', 12, 'end', CLAY, 600)
    s.save('2-1-residuals', 'Phần dư là đoạn thẳng đứng từ điểm dữ liệu tới đường dự đoán.')


def projection21():
    s = Fig(640, 230)
    O = (190, 180)
    plane = [(110, 200), (250, 120), (520, 120), (380, 200)]
    s.path('M ' + ' L '.join(f'{x},{y}' for x, y in plane) + ' Z', 'none', 0, BLUE, opacity=.12)
    s.label(500, 132, 'mọi dự đoán Xθ', 12, 'end', BLUE)
    yh = (380, 150)
    yv = (380, 40)
    s.arrow(*O, *yv, TEXT, 2)
    s.arrow(*O, *yh, CLAY, 2)
    s.line(yv[0], yv[1] + 4, yh[0], yh[1] - 4, MUTED, 1.4, dash='4 3')
    s.path(f'M {yh[0] - 10},{yh[1]} L {yh[0] - 10},{yh[1] - 10} L {yh[0]},{yh[1] - 10}', MUTED, 1)
    s.label(yv[0] + 10, yv[1], 'y', 15, 'start', TEXT, 600)
    s.label(yh[0] + 12, yh[1] + 10, 'ŷ', 15, 'start', CLAY, 600)
    s.label(yv[0] + 10, 95, 'phần dư ⟂ mặt phẳng', 12.5, 'start', MUTED)
    s.save('2-1-projection', 'Least squares chiếu y vuông góc xuống mặt phẳng các dự đoán; phần dư vuông góc với mọi cột.')


def gd1d21():
    f = cap('2-1-gd1d')
    s = Fig(640, 220)
    for k_, (a, title, col) in enumerate([(f.axes[0], 'η = 0.3', GREEN), (f.axes[1], 'η = 1.1', CLAY)]):
        ax = s.axes(40 + k_ * 310, 34, 260, 150, (-2.6, 2.6), (0, 4.2), frame=False, grid=False)
        l = a.lines[0]
        xs_, ys_ = l.get_xdata(), l.get_ydata()
        keep = ys_ <= 4.2
        ax.line(xs_[keep], ys_[keep], FAINT, 1.4)
        pts = a.collections[0].get_offsets()
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            s.arrow(ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), col, 1.4)
        for x, y in pts:
            s.circle(ax.X(x), ax.Y(y), 3.2, col)
        s.label(40 + k_ * 310 + 130, 16, title, 14, color=col, weight=600)
        s.label(40 + k_ * 310 + 130, 204, ['tiến dần về đáy', 'vượt đáy, văng xa dần'][k_], 12.5, color=MUTED)
    s.line(320, 26, 320, 210, SOFT_LINE, 1)
    s.save('2-1-gd1d', 'Bước vừa phải đi dần về đáy; bước quá lớn vượt đáy rồi văng xa dần.')


def scaling21():
    f = cap('2-1-scaling')
    s = Fig(640, 230)
    for k_, (a, title, sx) in enumerate([(f.axes[0], 'chưa chuẩn hóa', 2.8), (f.axes[1], 'đã chuẩn hóa', 1.0)]):
        cx, cy, W, H = 40 + k_ * 310 + 130, 118, 260, 170
        s.label(cx, 16, title, 14, color=TEXT, weight=600)
        for r in (1, 2, 3, 4, 5):
            rx, ry = 22 * r * sx * (1 if k_ else .95), 13 * r * (1 if k_ else .55) if k_ == 0 else 15 * r
            if k_ == 1:
                rx = ry = 15 * r
            s.parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{min(rx, W / 2):g}" ry="{min(ry, H / 2 - 4):g}" fill="none" stroke="{SOFT_LINE}" stroke-width="1"/>')
        l = a.lines[0]
        xs, ys = l.get_xdata(), l.get_ydata()
        scx = (W / 2 - 6) / 2.9
        scy = (H / 2 - 10) / 1.7
        pts = [(cx + x * scx, cy - y * scy) for x, y in zip(xs, ys)]
        s.path('M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts), CLAY, 1.6)
        for x, y in pts:
            s.circle(x, y, 2.6, CLAY)
        s.circle(cx, cy, 5, BLUE)
        s.label(cx, 214, ['zigzag trong thung lũng hẹp', 'đi gần thẳng về đáy'][k_], 12.5, color=MUTED)
    s.line(320, 26, 320, 220, SOFT_LINE, 1)
    s.save('2-1-scaling', 'Đặc trưng chênh thang đo làm mặt loss thành thung lũng hẹp; chuẩn hóa đưa nó về gần tròn.')


def lr21():
    a = cap('2-1-lr').axes[0]
    s = Fig(640, 220)
    L = lambda v: math.log10(v)
    ax = s.axes(70, 20, 440, 160, (0, 40), (-1.2, 1.6), xticks=[0, 10, 20, 30, 40], xlabel='vòng lặp')
    for e in (-1, 0, 1):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    names = [('η = 0.01 · quá chậm', CLAY), ('η = 0.1 · vừa', BLUE), ('η = 1 · nổ', SAND)]
    for (lab, col), l in zip(names, a.lines[:3]):
        xs, ys = l.get_xdata(), np.minimum(l.get_ydata(), 10 ** 1.6)
        keep = l.get_ydata() <= 10 ** 1.6
        ax.line(xs[keep], [L(v) for v in ys[keep]], col, 2)
        xe, ye = xs[keep][-1], L(ys[keep][-1])
        s.label(min(ax.X(xe), ax.X(40)) + 8, ax.Y(ye), lab, 12, 'start', col, 600)
    ax.hline(L(.0881), FAINT, 1.2, '4 3')
    s.save('2-1-lr', 'Loss theo vòng lặp (thang log) với ba learning rate.')


def resplots21():
    f = cap('2-1-residual-plots')
    s = Fig(640, 190)
    for k_, (a, title) in enumerate(zip(f.axes, ['ổn', 'uốn cong', 'loe dần'])):
        pts = a.collections[0].get_offsets()
        xs, ys = pts[:, 0], pts[:, 1]
        x0 = 20 + k_ * 210
        ax = s.axes(x0, 30, 190, 120, (xs.min(), xs.max()), (-max(abs(ys)) * 1.05, max(abs(ys)) * 1.05), frame=False, grid=False)
        s.line(x0, ax.Y(0), x0 + 190, ax.Y(0), LINE, 1)
        ax.dots(xs, ys, [GREEN, CLAY, SAND][k_], 2.3)
        s.label(x0 + 95, 14, title, 13.5, color=[GREEN, CLAY, SAND][k_], weight=600)
    s.label(320, 176, 'phần dư theo dự đoán', 12, color=FAINT)
    s.save('2-1-residual-plots', 'Phần dư tốt nằm đều quanh 0; uốn cong báo thiếu quan hệ phi tuyến, loe dần báo nhiễu không đều.')


def loglog21():
    a = cap('2-1-loglog').axes[0]
    pts = a.collections[0].get_offsets()
    L = math.log10
    s = Fig(640, 220)
    ax = s.axes(80, 20, 430, 160, (2.8, 5.5), (-3.4, 2.2), frame=True, grid=False)
    for e in range(-3, 3):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    for e in (3, 4, 5):
        s.label(ax.X(e), ax.y + ax.h + 14, f'10{sup(e)}', 11, color=FAINT)
    s.label(ax.x + ax.w, ax.y + ax.h + 30, 'n', 11.5, 'end', FAINT)
    s.label(ax.x - 8, ax.y - 12, 'giây', 11.5, 'start', FAINT)
    l = a.lines[0]
    ax.line([L(v) for v in l.get_xdata()], [L(v) for v in l.get_ydata()], CLAY, 1.6)
    ax.hline(0, FAINT, 1.2, '4 3')
    s.label(ax.X(2.85), ax.Y(0) - 10, 'giới hạn 1 giây', 11.5, 'start', FAINT)
    for x, y in pts:
        s.circle(ax.X(L(x)), ax.Y(L(y)), 4, BLUE)
    s.circle(ax.X(L(2e5)), ax.Y(L(37.9)), 6, CLAY, PAPER, 2)
    s.label(ax.X(L(2e5)) - 10, ax.Y(L(37.9)), 'n = 2·10⁵: ~38 giây', 12, 'end', CLAY, 600)
    s.label(ax.X(4.05), ax.Y(-1.6), 'độ dốc ≈ 1.98', 12.5, 'start', CLAY)
    s.save('2-1-loglog', 'Trên trục log–log, thời gian theo n là đường thẳng; độ dốc gần 2 nghĩa là O(n²).')


def hand21():
    s = Fig(640, 210)
    ax = s.axes(80, 20, 300, 160, (0, 4), (0, 6), xticks=[0, 1, 2, 3, 4], yticks=[0, 2, 4, 6])
    pts = [(1, 2), (2, 3), (3, 5)]
    ax.line([0, 4], [1 / 3, 1.5 * 4 + 1 / 3], BLUE, 2)
    ax.line([0, 4], [.67, 1.53 * 4 + .67], CLAY, 1.4, dash='5 4')
    for x, y in pts:
        s.circle(ax.X(x), ax.Y(y), 5, TEXT)
        s.mono(ax.X(x) + 8, ax.Y(y) + 12, f'({x}, {y})', 11.5, 'start', MUTED)
    s.mono(410, 60, 'ŷ = 1.5x + 1/3', 13, 'start', BLUE, 600)
    s.label(410, 80, 'nghiệm least squares, J = 0.056', 12, 'start', MUTED)
    s.mono(410, 120, 'ŷ = 1.53x + 0.67', 13, 'start', CLAY, 600)
    s.label(410, 140, 'sau 1 bước GD từ 0, J = 0.22', 12, 'start', MUTED)
    s.save('2-1-hand', 'Ba điểm của ví dụ tính tay: nghiệm đóng và vị trí sau một bước gradient descent.')


# ───────────────────────────── 2.2 ─────────────────────────────

def logticks(ax, lo, hi, y=None):
    for e in range(lo, hi + 1):
        ax.f.label(ax.X(e), (y or ax.y + ax.h) + 14, f'10{sup(e)}', 11, color=FAINT)


def ellipse_pts(c, Q, level, n=160):
    vals, vecs = np.linalg.eigh(Q)
    t = np.linspace(0, 2 * np.pi, n)
    u = np.c_[np.cos(t), np.sin(t)] * np.sqrt(level / vals)
    return c + u @ vecs.T


def clip(s, cid, x, y, w, h):
    s.parts.append(f'<clipPath id="{cid}"><rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"/></clipPath><g clip-path="url(#{cid})">')


def mnum(v, fmt='{:g}'):
    return fmt.format(v).replace('-', '−')


def overfit22():
    ns = lesson_ns('2.2', upto=2)
    w = ns['fit_ols'](ns['A_tr'], ns['y_tr'])[0]
    s = Fig(640, 210)
    ax = s.axes(60, 24, 560, 150, (-.8, 31.8), (-1, 1.4), yticks=[-1, 0, 1], frame=False)
    s.line(ax.x, ax.Y(0), ax.x + ax.w, ax.Y(0), LINE, 1)
    for j, v in enumerate(w):
        col = CLAY if j < 2 else FAINT
        y0, y1 = sorted([ax.Y(0), ax.Y(v)])
        s.rect(ax.X(j) - 6, y0, 12, max(y1 - y0, .8), 'none', col, 2, .9 if j < 2 else .55, 0)
    s.label(ax.X(0) - 4, ax.Y(w[0]) - 12, 'diện tích', 12, 'start', CLAY, 600)
    s.label(ax.X(1) + 10, ax.Y(w[1]) + 4, 'khoảng cách', 12, 'start', CLAY, 600)
    k = 2 + int(np.abs(w[2:]).argmax())
    s.mono(ax.X(k), ax.Y(w[k]) + (-12 if w[k] > 0 else 14), f'{w[k]:.2f}', 11.5, 'middle', MUTED)
    s.label(ax.X(17), 196, '30 cột rác: lẽ ra hệ số bằng 0', 12.5, color=MUTED)
    s.save('2-2-overfit', 'Hệ số least squares trên 40 căn: cột rác cũng nhận trọng số đáng kể.')


def validation22():
    ns = lesson_ns('2.2', upto=3)
    fit, r2, A_tr, A_te, y_tr, y_te = (ns[k] for k in ('fit_ridge', 'r2', 'A_tr', 'A_te', 'y_tr', 'y_te'))
    lg = np.linspace(-2, 3, 121)
    tr, te = [], []
    for g in lg:
        w, b = fit(A_tr, y_tr, 10 ** g)
        tr.append(r2(A_tr @ w + b, y_tr)); te.append(r2(A_te @ w + b, y_te))
    s = Fig(640, 230)
    ax = s.axes(60, 20, 470, 170, (-2, 3), (0, 1), yticks=[0, .25, .5, .75, 1], xlabel='λ')
    logticks(ax, -2, 3)
    ax.line(lg, tr, CLAY, 2).line(lg, te, BLUE, 2)
    s.label(ax.X(3) + 8, ax.Y(tr[-1]) - 8, 'train', 12.5, 'start', CLAY, 600)
    s.label(ax.X(3) + 8, ax.Y(te[-1]) + 8, 'test', 12.5, 'start', BLUE, 600)
    k = int(np.argmax(te))
    s.line(ax.X(lg[k]), ax.Y(0), ax.X(lg[k]), ax.Y(te[k]), FAINT, 1, '3 3')
    s.circle(ax.X(lg[k]), ax.Y(te[k]), 4.5, BLUE, PAPER, 2)
    s.label(ax.X(lg[k]) + 8, ax.Y(te[k]) + 32, f'λ ≈ {10 ** lg[k]:.1f}', 12, 'start', BLUE)
    s.label(ax.X(-2) + 4, ax.Y(.86) , 'học thuộc', 12, 'start', MUTED)
    s.label(ax.X(3) - 4, ax.Y(.86), 'trói tay', 12, 'end', MUTED)
    s.save('2-2-validation', 'Tăng λ thì R² train giảm đều; R² test lên đỉnh ở khoảng giữa rồi giảm.')


def geometry22():
    c, Q = np.array([1.5, 2.2]), np.array([[1.0, .6], [.6, 1.2]])
    f = lambda W: np.einsum('ni,ij,nj->n', W - c, Q, W - c)
    t = np.linspace(0, 2 * np.pi, 20001)
    C = np.c_[np.cos(t), np.sin(t)]
    D = C / np.abs(C).sum(1, keepdims=True)
    s = Fig(640, 290)
    for k_, (B, title, ball) in enumerate([(C, 'Ridge · L2', 'circle'), (D, 'Lasso · L1', 'diamond')]):
        x0 = 30 + k_ * 320
        ax = s.axes(x0, 36, 260, 240, (-1.6, 3), (-1.3, 2.95), frame=False, grid=False)
        s.line(ax.X(-1.6), ax.Y(0), ax.X(3), ax.Y(0), SOFT_LINE, 1)
        s.line(ax.X(0), ax.Y(-1.3), ax.X(0), ax.Y(2.95), SOFT_LINE, 1)
        s.label(ax.X(-1.6) + 2, ax.Y(0) - 10, 'w₁', 11.5, 'start', FAINT)
        pts = ' L '.join(f'{ax.X(a):.1f},{ax.Y(b):.1f}' for a, b in B[::200])
        s.path(f'M {pts} Z', BLUE, 1.6, BLUE, .9)
        s.parts[-1] = s.parts[-1].replace('fill="' + BLUE + '"', f'fill="{BLUE}" fill-opacity=".12"')
        kmin = f(B).argmin()
        lv = f(B)[kmin]
        clip(s, f'cp-2-2-geometry-{k_}', x0, 36, 260, 240)
        for L, wd, col in [(lv, 1.6, CLAY)]:
            E = ellipse_pts(c, Q, L)
            s.path('M ' + ' L '.join(f'{ax.X(a):.1f},{ax.Y(b):.1f}' for a, b in E) + ' Z', col, wd)
        s.parts.append('</g>')
        s.circle(ax.X(c[0]), ax.Y(c[1]), 4, TEXT)
        s.label(ax.X(c[0]), ax.Y(c[1]) + 16, 'least squares', 11.5, 'middle', MUTED)
        p = B[kmin]
        s.circle(ax.X(p[0]), ax.Y(p[1]), 5.5, CLAY, PAPER, 2.2)
        s.label(x0 + 130, 14, title, 14, color=TEXT, weight=600)
        if k_:
            s.label(ax.X(-.45), ax.Y(1.0), 'w₁ = 0', 12, 'end', CLAY, 600)
    s.line(320, 30, 320, 278, SOFT_LINE, 1)
    s.save('2-2-geometry', 'Đường đồng mức của lỗi chạm hình tròn ở một điểm thường; chạm hình thoi ở góc, nơi w₁ = 0.')


def shrink22():
    s = Fig(640, 250)
    ax = s.axes(80, 16, 380, 200, (-3, 3), (-3, 3), xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-2, 0, 2], xlabel='z (hệ số least squares)')
    s.rect(ax.X(-1), ax.y, ax.X(1) - ax.X(-1), ax.h, 'none', CLAY, 0, .08, 0)
    z = np.linspace(-3, 3, 61)
    ax.line(z, z, FAINT, 1.4, '5 4')
    ax.line(z, z / 2, BLUE, 2)
    ax.line(z, np.sign(z) * np.maximum(np.abs(z) - 1, 0), CLAY, 2.2)
    s.label(ax.X(3) + 8, ax.Y(3), 'không phạt', 12, 'start', FAINT)
    s.label(ax.X(3) + 8, ax.Y(1.5), 'Ridge: z/2', 12.5, 'start', BLUE, 600)
    s.label(ax.X(3) + 8, ax.Y(2), 'Lasso: z − 1', 12.5, 'start', CLAY, 600)
    s.label(ax.X(0), ax.Y(-2.4), 'về đúng 0', 12, color=CLAY)
    s.save('2-2-shrink', 'Với λ = 1, Ridge chia đôi mọi hệ số; Lasso trừ 1 rồi cắt về 0 khi |z| ≤ 1.')


def hand22():
    z = [3, .5, -1.2]
    s = Fig(640, 200)
    for k_, (title, col, rule) in enumerate([('Ridge: chia đôi', BLUE, lambda v: v / 2),
                                             ('Lasso: bớt 1, cắt ở 0', CLAY, lambda v: math.copysign(max(abs(v) - 1, 0), v))]):
        x0 = 40 + k_ * 310
        ax = s.axes(x0, 40, 260, 120, (-1.6, 3.4), (0, 3), xticks=[-1, 0, 1, 2, 3], frame=False, grid=False)
        if k_:
            s.rect(ax.X(-1), ax.y, ax.X(1) - ax.X(-1), ax.h, 'none', CLAY, 0, .08, 0)
        for i, v in enumerate(z):
            y = ax.y + 22 + i * 38
            w = rule(v)
            s.line(ax.X(-1.6), y, ax.X(3.4), y, SOFT_LINE, .8)
            s.circle(ax.X(v), y, 4.5, FAINT, PAPER, 1.6)
            if abs(ax.X(v) - ax.X(w)) > 12:
                s.arrow(ax.X(v) + (-7 if w < v else 7), y, ax.X(w) + (7 if w < v else -7), y, col, 1.5)
            s.circle(ax.X(w), y, 5, col)
            s.mono(ax.X(w), y - 12, mnum(w), 11.5, 'middle', col)
        s.label(x0 + 130, 16, title, 14, color=col, weight=600)
    s.line(320, 12, 320, 186, SOFT_LINE, 1)
    s.save('2-2-hand', 'Ví dụ tính tay với z = (3, 0.5, −1.2) và λ = 1: vòng rỗng là z, chấm đặc là hệ số sau khi phạt.')


def collinear22():
    s = Fig(640, 240)
    ax = s.axes(170, 20, 300, 200, (-1.2, 2.8), (-1.55, 1.117), frame=False, grid=False)
    s.line(ax.X(-1.2), ax.Y(0), ax.X(2.8), ax.Y(0), SOFT_LINE, 1)
    s.line(ax.X(0), ax.Y(-1.55), ax.X(0), ax.Y(1.117), SOFT_LINE, 1)
    s.label(ax.X(2.8), ax.Y(0) - 10, 'w₁', 11.5, 'end', FAINT)
    c = np.array([2.3, -1.3]); Q = np.array([[1, 1], [1, 1]]) + .015 * np.eye(2)
    clip(s, 'cp-2-2-collinear', ax.x, ax.y, ax.w, ax.h)
    for L, col, wd in [(.01, LINE, 1), (.04, LINE, 1), (.09, LINE, 1)]:
        E = ellipse_pts(c, Q, L, 240)
        s.path('M ' + ' L '.join(f'{ax.X(a):.1f},{ax.Y(b):.1f}' for a, b in E) + ' Z', col, wd)
    s.parts.append('</g>')
    s.line(ax.X(-.1), ax.Y(1.1), ax.X(2.55), ax.Y(-1.55), CLAY, 1.2, '4 4')
    s.circle(ax.X(c[0]), ax.Y(c[1]), 4, TEXT)
    s.label(ax.X(c[0]) - 16, ax.Y(c[1]) + 16, 'least squares', 11.5, 'end', MUTED)
    r = math.hypot(.5, .5)
    s.circle(ax.X(0), ax.Y(0), (ax.X(r) - ax.X(0)), BLUE, BLUE, 1.4, .1)
    s.circle(ax.X(.5), ax.Y(.5), 5.5, BLUE, PAPER, 2.2)
    s.label(ax.X(.5) + 10, ax.Y(.5) - 8, 'Ridge (0.5, 0.5)', 12, 'start', BLUE, 600)
    s.label(ax.X(-.1) - 6, ax.Y(1.1), 'w₁ + w₂ ≈ 1', 12, 'end', CLAY)
    s.save('2-2-collinear', 'Hai đặc trưng gần trùng nhau: lỗi gần như không đổi dọc rãnh w₁ + w₂ ≈ 1; Ridge chọn điểm gần gốc nhất trên rãnh.')


def path22():
    from sklearn.linear_model import lasso_path
    ns = lesson_ns('2.2', upto=1)
    A, y = ns['A_tr'], ns['y_tr']
    alphas, coefs, _ = lasso_path(A - A.mean(0), y - y.mean(), alphas=np.logspace(-3, .3, 160), max_iter=100000, tol=1e-10)
    lg = np.log10(alphas)
    s = Fig(640, 240)
    ax = s.axes(60, 20, 470, 170, (-3, .3), (-1, 1.5), yticks=[-1, -.5, 0, .5, 1, 1.5], xlabel='alpha (phạt tăng →)')
    logticks(ax, -3, 0)
    for j in range(2, coefs.shape[0]):
        ax.line(lg, coefs[j], FAINT, .9)
    ax.line(lg, coefs[0], CLAY, 2.2).line(lg, coefs[1], BLUE, 2.2)
    g = math.log10(.03162)
    s.line(ax.X(g), ax.y, ax.X(g), ax.y + ax.h, MUTED, 1, '3 3')
    s.label(ax.X(g) + 6, ax.y + 6, 'CV chọn', 11.5, 'start', MUTED)
    k = int(np.argmin(np.abs(lg - (-2.6))))
    s.label(ax.X(-3) + 4, ax.Y(coefs[0][-1]) - 12, 'diện tích', 12.5, 'start', CLAY, 600)
    s.label(ax.X(-3) + 4, ax.Y(coefs[1][-1]) + 18, 'khoảng cách', 12.5, 'start', BLUE, 600)
    s.label(ax.X(-1.15), ax.Y(.32), '30 cột rác', 12, 'start', FAINT)
    s.save('2-2-path', 'Hệ số Lasso khi mức phạt tăng: cột rác về 0 trước, khoảng cách rồi diện tích về 0 sau cùng.')


def units22():
    ns = lesson_ns('2.2', upto=1)
    from sklearn.linear_model import Ridge
    B, y = ns['X_tr'][:, :2], ns['y_tr']
    vals = [Ridge(alpha=1000).fit(B * np.array([1, sc]), y).coef_[1] * sc for sc in (1, 1000)]
    s = Fig(640, 170)
    ax = s.axes(250, 20, 340, 100, (-.2, 0), (0, 2), frame=False, grid=False)
    s.line(ax.X(0), 14, ax.X(0), 126, LINE, 1)
    ols = -.175
    for i, (lab, v) in enumerate(zip(['khoảng cách theo km', 'khoảng cách theo m'], vals)):
        y = 36 + i * 50
        s.rect(ax.X(v), y - 12, ax.X(0) - ax.X(v), 24, 'none', [BLUE, CLAY][i], 3, .75, 0)
        s.label(170, y, lab, 13, 'end', TEXT)
        s.mono(ax.X(v) - 8, y, mnum(v, '{:.3f}'), 12, 'end', [BLUE, CLAY][i])
    s.line(ax.X(ols), 14, ax.X(ols), 126, MUTED, 1.2, '4 3')
    s.label(ax.X(ols), 144, 'không phạt: −0.175', 11.5, color=MUTED)
    s.label(ax.X(0), 144, '0', 11.5, color=FAINT)
    s.save('2-2-units', 'Cùng Ridge(alpha=1000), chỉ đổi đơn vị: tính theo m thì hệ số khoảng cách gần như không bị phạt.')


def enet22():
    t = np.linspace(0, 2 * np.pi, 721)
    U = np.c_[np.cos(t), np.sin(t)]
    shapes = []
    for rho in (0, 1, .5):
        # bán kính theo hướng u: rho*r*|u|1 + (1-rho)/2*r^2 = 1 (rho=0: tròn, rho=1: thoi)
        l1 = np.abs(U).sum(1)
        if rho == 0:
            r = np.full(len(U), math.sqrt(2))
        else:
            a, bq = (1 - rho) / 2, rho * l1
            r = (-bq + np.sqrt(bq ** 2 + 4 * a)) / (2 * a) if a else 1 / l1
        shapes.append(U * r[:, None] / (math.sqrt(2) if rho == 0 else 1))
    s = Fig(640, 200)
    for k_, (P, title, col) in enumerate(zip(shapes, ['Ridge', 'Lasso', 'Elastic Net'], [BLUE, CLAY, GREEN])):
        cx, cy, sc = 110 + k_ * 210, 100, 62
        s.line(cx - 80, cy, cx + 80, cy, SOFT_LINE, 1)
        s.line(cx, cy - 76, cx, cy + 76, SOFT_LINE, 1)
        R_ = sc / np.abs(P).max()
        s.path('M ' + ' L '.join(f'{cx + a * R_:.1f},{cy - b * R_:.1f}' for a, b in P) + ' Z', col, 1.8)
        s.label(cx, 188, title, 14, color=col, weight=600)
    s.save('2-2-enet', 'Vùng ràng buộc của ba khoản phạt: Elastic Net vẫn có góc trên trục như Lasso nhưng cạnh cong như Ridge.')


# ───────────────────────────── 2.3 ─────────────────────────────

def sig(z):
    return 1 / (1 + np.exp(-np.asarray(z, float)))


def jit(n, seed, amp):
    return np.random.default_rng(seed).uniform(-amp, amp, n)


def segline(ax, f, color, width, dash=None, n=400):
    """Vẽ phần đường y = f(x) nằm trong khung (cắt bằng lấy mẫu, không dùng clipPath)."""
    xs = np.linspace(*ax.xlim, n)
    ys = f(xs)
    k = (ys >= ax.ylim[0]) & (ys <= ax.ylim[1])
    ax.line(xs[k], ys[k], color, width, dash, clip=False)


def linfail23():
    ns = lesson_ns('2.3', upto=3)
    from sklearn.linear_model import LinearRegression
    L_tr, y_tr, L_more, y_more = ns['L_tr'], ns['y_tr'], ns['L_more'], ns['y_more']
    s = Fig(640, 240)
    ax = s.axes(60, 20, 520, 170, (-.5, 25), (-.25, 1.45), xticks=[0, 5, 10, 15, 20, 25], yticks=[0, .5, 1], xlabel='số link')
    x = L_tr[:, 0]
    ax.dots(x + jit(len(x), 1, .25), y_tr + jit(len(x), 2, .05), FAINT, 2.2, opacity=.7)
    ex = L_more[300:, 0]
    ax.dots(ex, 1 + jit(len(ex), 3, .05), CLAY, 3)
    for k_, ((L, yy), col, dash) in enumerate([((L_tr, y_tr), BLUE, None), ((L_more, y_more), CLAY, '6 4')]):
        m = LinearRegression().fit(L, yy)
        segline(ax, lambda x: m.intercept_ + m.coef_[0] * x, col, 2, dash)
        t = (.5 - m.intercept_) / m.coef_[0]
        s.line(ax.X(t), ax.Y(.5), ax.X(t), ax.Y(-.25), col, 1.2, '3 3')
        s.mono(ax.X(t) + (-6 if k_ == 0 else 6), ax.Y(-.25) - 9, f'{t:.1f}', 11.5, 'end' if k_ == 0 else 'start', col)
        if k_ == 0:
            xl = (1.3 - m.intercept_) / m.coef_[0]
    ax.hline(.5, FAINT, 1, '2 4')
    s.label(ax.X(xl) - 10, ax.Y(1.3), '300 email gốc', 12, 'end', BLUE, 600)
    s.label(ax.X(19.5), ax.Y(.78), '+ 20 siêu spam', 12, 'middle', CLAY, 600)
    s.save('2-3-linfail', 'Linear regression trên nhãn 0/1: thêm 20 email siêu spam làm đường thoải xuống, ngưỡng 0.5 dịch từ 3.1 lên 6 link.')


def sigmoid23():
    s = Fig(640, 210)
    ax = s.axes(80, 16, 460, 150, (-7, 7), (0, 1), xticks=[-6, -3, 0, 3, 6], yticks=[0, .5, 1], xlabel='z')
    z = np.linspace(-7, 7, 141)
    ax.line(z, sig(z), CLAY, 2.4)
    for zz, lab, anc, dx, dy in [(-3, 'p ≈ 0.05', 'end', -10, -12), (0, 'p = 0.5', 'start', 10, 12), (3, 'p ≈ 0.95', 'start', 10, 12)]:
        s.circle(ax.X(zz), ax.Y(sig(zz)), 4.5, CLAY, PAPER, 2)
        s.label(ax.X(zz) + dx, ax.Y(sig(zz)) + dy, lab, 12, anc, TEXT)
    s.save('2-3-sigmoid', 'Sigmoid nhận mọi số thực z và trả về một xác suất trong (0, 1).')


def boundary23():
    ns = lesson_ns('2.3', upto=8)
    m, X, y = ns['model'], ns['X_tr'], ns['y_tr']
    w, b = m.coef_[0], m.intercept_[0]
    s = Fig(640, 280)
    ax = s.axes(170, 16, 300, 225, (-.6, 8.4), (-1.5, 6.15), xticks=[0, 2, 4, 6, 8], yticks=[0, 2, 4, 6], xlabel='số link', ylabel=None, grid=False)
    s.label(ax.x - 30, ax.y + 6, 'từ quảng cáo', 11.5, 'end', FAINT)
    jx, jy = jit(len(y), 4, .22), jit(len(y), 5, .22)
    for lab, col in [(0, BLUE), (1, CLAY)]:
        k = y == lab
        ax.dots(X[k, 0] + jx[k], X[k, 1] + jy[k], col, 2.4, opacity=.75)
    for p, wd, dash in [(.1, 1.1, '4 4'), (.5, 2, None), (.9, 1.1, '4 4')]:
        c = math.log(p / (1 - p)) - b
        segline(ax, lambda x: (c - w[0] * x) / w[1], TEXT, wd, dash)
        xr = (c - w[1] * -1.5) / w[0]
        s.label(ax.X(xr) + 6, ax.Y(-1.5) - 8, f'p = {p}', 11.5, 'start', TEXT if p == .5 else MUTED, 600 if p == .5 else 400)
    s.label(ax.x + ax.w + 14, ax.y + 30, 'spam', 12.5, 'start', CLAY, 600)
    s.label(ax.x + ax.w + 14, ax.y + 50, 'thư thường', 12.5, 'start', BLUE, 600)
    s.save('2-3-boundary', 'Các mức xác suất của logistic regression là những đường thẳng song song; p = 0.5 là ranh giới.')


def loss23():
    p = np.linspace(.005, 1, 200)
    s = Fig(640, 220)
    for k_, (title, ce, sq, ylim, yt) in enumerate([
            ('loss', -np.log(p), (1 - p) ** 2, (0, 6), [0, 2, 4, 6]),
            ('|gradient theo z|', 1 - p, 2 * (1 - p) * p * (1 - p), (0, 1), [0, .5, 1])]):
        x0 = 50 + k_ * 320
        ax = s.axes(x0, 30, 250, 150, (0, 1), ylim, xticks=[0, .5, 1], yticks=yt, xlabel='p đoán cho email spam')
        s.label(x0 - 8, 14, title, 12.5, 'start', TEXT, 600)
        ax.line(p, ce, CLAY, 2.2).line(p, sq, BLUE, 2.2)
    for x0 in (50, 370):
        s.label(x0 + 250, 44, 'cross-entropy', 12, 'end', CLAY, 600)
        s.label(x0 + 250, 62, 'bình phương', 12, 'end', BLUE, 600)
    s.save('2-3-loss', 'Với email spam bị đoán p nhỏ: cross-entropy phạt nặng và cho gradient lớn; bình phương cho gradient gần 0.')


def odds23():
    ns = lesson_ns('2.3', upto=8)
    m = ns['model']
    xs = np.linspace(0, 10, 101)
    P = m.predict_proba(np.c_[xs, np.ones_like(xs)])[:, 1]
    pt = m.predict_proba(np.array([[1, 1], [2, 1], [7, 1], [8, 1]], float))[:, 1]
    s = Fig(640, 220)
    ax = s.axes(80, 16, 440, 160, (0, 10), (0, 1), xticks=list(range(0, 11)), yticks=[0, .5, 1], xlabel='số link (1 từ quảng cáo)')
    ax.line(xs, P, CLAY, 2.2)
    for (a, b_), (pa, pb) in [((1, 2), (pt[0], pt[1])), ((7, 8), (pt[2], pt[3]))]:
        s.line(ax.X(a), ax.Y(pa), ax.X(b_), ax.Y(pa), FAINT, 1)
        s.line(ax.X(b_), ax.Y(pa), ax.X(b_), ax.Y(pb), TEXT, 1.6)
        for xx, pp in [(a, pa), (b_, pb)]:
            s.circle(ax.X(xx), ax.Y(pp), 4, CLAY, PAPER, 2)
    s.label(ax.X(2) + 8, ax.Y((pt[0] + pt[1]) / 2), f'+{pt[1] - pt[0]:.2f}', 12.5, 'start', TEXT, 600)
    s.label(ax.X(8) + 8, ax.Y(pt[3]) + 16, f'+{pt[3] - pt[2]:.2f}', 12.5, 'start', TEXT, 600)
    s.label(ax.X(4.6), ax.Y(.2), 'mỗi link: odds × 3.08', 12.5, 'start', MUTED)
    s.save('2-3-odds', 'Mỗi link nhân odds lên khoảng 3 lần, nhưng xác suất tăng nhiều ở giữa và gần như đứng yên khi đã gần 1.')


def threshold23():
    ns = lesson_ns('2.3', upto=10)
    p, y = ns['p_te'], ns['y_te']
    s = Fig(640, 230)
    ax = s.axes(110, 20, 470, 150, (0, 1), (-.5, 1.5), xticks=[0, .25, .5, .75, 1], xlabel='p dự đoán', grid=False)
    rows = {1: (ax.Y(1), CLAY, 'spam'), 0: (ax.Y(0), BLUE, 'thư thật')}
    for lab, (yy, col, name) in rows.items():
        k = y == lab
        jj = jit(k.sum(), 6 + lab, 14)
        for pp, j in zip(p[k], jj):
            s.circle(ax.X(pp), yy + j, 3.2, col, None, 0, .75)
        s.label(ax.x - 14, yy, name, 12.5, 'end', col, 600)
    for t, lab in [(.3, '0.3'), (.5, '0.5'), (.9, '0.9')]:
        s.line(ax.X(t), ax.y, ax.X(t), ax.y + ax.h, TEXT if t == .5 else FAINT, 1.4 if t == .5 else 1.1, None if t == .5 else '4 3')
        s.label(ax.X(t), ax.y + 2 - 8, lab, 11.5, color=TEXT if t == .5 else MUTED)
    s.save('2-3-threshold', '100 email test theo xác suất dự đoán: email bên phải ngưỡng bị chặn; dời ngưỡng là đổi số thư thật bị chặn nhầm lấy số spam lọt.')


def weights23():
    ns = lesson_ns('2.3', upto=14)
    W, D, t = ns['W'], ns['D_tr'], ns['t_tr']
    s = Fig(640, 186)
    c, gap = 6, 6.5
    side = 8 * c
    vmax = np.abs(W).max()
    s.label(14, 52, 'trung bình', 11.5, 'start', FAINT)
    s.label(14, 128, 'trọng số', 11.5, 'start', FAINT)
    for k in range(10):
        x0 = 86 + k * (side + gap)
        mean = D[t == k].mean(0).reshape(8, 8)
        wk = W[:, k].reshape(8, 8)
        s.label(x0 + side / 2, 14, str(k), 13, color=TEXT, weight=600)
        for i in range(8):
            for j in range(8):
                v = mean[i, j]
                if v > .03:
                    s.rect(x0 + j * c, 28 + i * c, c + .2, c + .2, 'none', TEXT, 0, min(.9, v), 0)
                u = wk[i, j] / vmax
                if abs(u) > .04:
                    s.rect(x0 + j * c, 104 + i * c, c + .2, c + .2, 'none', BLUE if u > 0 else CLAY, 0, min(.95, abs(u) * 1.6), 0)
        s.box(x0, 28, side, side, SOFT_LINE, 'none', r=2, width=.8)
        s.box(x0, 104, side, side, SOFT_LINE, 'none', r=2, width=.8)
    s.label(320, 172, 'xanh: nét mực ở đây tăng điểm lớp · cam: giảm điểm', 11.5, color=MUTED)
    s.save('2-3-weights', 'Hàng trên: ảnh trung bình của mỗi chữ số. Hàng dưới: 64 trọng số của lớp đó xếp thành ảnh 8 × 8.')


def softmax23():
    z = np.array([2., 1., 0.])
    e = np.exp(z - z.max())
    p = e / e.sum()
    s = Fig(640, 190)
    cols = [('z', [f'{v:g}' for v in z], SAND), ('e^(z − max)', [f'{v:.3g}' for v in e], BLUE), ('p', [f'{v:.3f}' for v in p], CLAY)]
    xs = [90, 290, 490]
    for (head, vals, col), x in zip(cols, xs):
        s.mono(x + 30, 20, head, 13, 'middle', MUTED)
        s.tiles(x, 36, [[v] for v in vals], 60, 36, col, 6, size=14)
    s.arrow(162, 91, 280, 91, MUTED, 1.4)
    s.mono(221, 79, 'exp', 12.5, 'middle', MUTED)
    s.arrow(362, 91, 480, 91, MUTED, 1.4)
    s.mono(421, 79, '÷ 1.503', 12.5, 'middle', MUTED)
    s.label(520, 176, 'tổng = 1', 12, 'middle', CLAY)
    s.save('2-3-softmax', 'Softmax của (2, 1, 0): trừ max, lấy mũ, chia cho tổng.')


FIGS23 = {'2-3-linfail': linfail23, '2-3-sigmoid': sigmoid23, '2-3-boundary': boundary23, '2-3-loss': loss23,
          '2-3-odds': odds23, '2-3-threshold': threshold23, '2-3-weights': weights23, '2-3-softmax': softmax23}


# ───────────────────────────── 2.4 ─────────────────────────────

def regions(s, ax, pred, xs, ys, colors, opacity=.1):
    """Tô vùng quyết định: pred[i, j] là lớp tại (xs[j], ys[i]); gộp các ô liền nhau cùng lớp trên một hàng."""
    dx, dy = xs[1] - xs[0], ys[1] - ys[0]
    paths = {}
    for i, yv in enumerate(ys):
        j = 0
        while j < len(xs):
            c = pred[i, j]
            j2 = j
            while j2 + 1 < len(xs) and pred[i, j2 + 1] == c:
                j2 += 1
            x0, x1 = ax.X(xs[j] - dx / 2), ax.X(xs[j2] + dx / 2)
            y0, y1 = ax.Y(yv + dy / 2), ax.Y(yv - dy / 2)
            paths.setdefault(c, []).append(f'M{x0:.1f},{y0:.1f}H{x1 + .4:.1f}V{y1 + .4:.1f}H{x0:.1f}Z')
            j = j2 + 1
    for c, d in paths.items():
        s.parts.append(f'<path d="{"".join(d)}" fill="{colors[c]}" fill-opacity="{opacity:g}" stroke="none"/>')


def k24():
    from sklearn.datasets import make_moons
    from sklearn.neighbors import KNeighborsClassifier
    X, y = make_moons(200, noise=.3, random_state=0)
    xs, ys = np.linspace(-1.6, 2.6, 106), np.linspace(-1.3, 1.7, 76)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    s = Fig(640, 220)
    for k_, k in enumerate((1, 15)):
        m = KNeighborsClassifier(k).fit(X, y)
        x0 = 20 + k_ * 315
        ax = s.axes(x0, 26, 290, 180, (-1.6, 2.6), (-1.3, 1.7), frame=False, grid=False)
        regions(s, ax, m.predict(G).reshape(len(ys), len(xs)), xs, ys, [BLUE, CLAY], .13)
        for lab, col in [(0, BLUE), (1, CLAY)]:
            ax.dots(X[y == lab, 0], X[y == lab, 1], col, 2.4)
        s.label(x0 + 145, 12, f'k = {k}', 14, color=TEXT, weight=600)
    s.save('2-4-k', 'Cùng 200 điểm: k = 1 vẽ ranh giới bám từng điểm nhiễu; k = 15 cho ranh giới mượt.')


def vote24():
    pts = {'A': (1, 1, 0), 'B': (2, 1, 0), 'C': (4, 3, 1), 'D': (5, 4, 1), 'E': (3, 2, 1)}
    s = Fig(640, 250)
    ax = s.axes(170, 14, 300, 210, (0, 6), (0, 4.2), xticks=[1, 2, 3, 4, 5], yticks=[1, 2, 3, 4], grid=False)
    r = ax.X(math.sqrt(2)) - ax.X(0)
    s.circle(ax.X(2), ax.Y(2), r, SAND, SAND, 1.2, .08)
    for n_, (x, y, lab) in pts.items():
        col = CLAY if lab == 0 else BLUE
        if n_ in 'ABE':
            s.line(ax.X(2), ax.Y(2), ax.X(x), ax.Y(y), FAINT, 1.1, '3 3')
        s.circle(ax.X(x), ax.Y(y), 5.5, col)
        if n_ == 'A':
            s.label(ax.X(x) - 10, ax.Y(y) + 10, n_, 13, 'end', col, 600)
        else:
            s.label(ax.X(x) + 10, ax.Y(y) - 10, n_, 13, 'start', col, 600)
    s.circle(ax.X(2), ax.Y(2), 6, TEXT, PAPER, 2)
    s.label(ax.X(2) - 10, ax.Y(2) - 10, 'q', 14, 'end', TEXT, 600)
    s.mono(ax.X(2.5), ax.Y(2) - 10, '1', 11.5, 'middle', MUTED)
    s.mono(ax.X(2) + 8, ax.Y(1.5), '1', 11.5, 'start', MUTED)
    s.mono(ax.X(1.5) - 8, ax.Y(1.5) - 6, '2', 11.5, 'end', MUTED)
    s.label(500, 70, 'đỏ: A, B', 13, 'start', CLAY, 600)
    s.label(500, 92, 'xanh: C, D, E', 13, 'start', BLUE, 600)
    s.label(500, 130, 'k = 3: B, E, A', 13, 'start', TEXT)
    s.label(500, 150, '→ đỏ thắng 2–1', 13, 'start', CLAY, 600)
    s.save('2-4-knn-vote', 'Truy vấn q = (2, 2), số trên nét đứt là d²: ba láng giềng gần nhất B, E, A; đỏ thắng 2–1.')


def units24():
    s = Fig(640, 230)
    u = 64
    for k_, (title, unit) in enumerate([('giờ', 1), ('phút', 60)]):
        cx, cy = 90 + k_ * 320, 148
        s.label(cx + 100, 16, f'giờ tự học tính bằng {title}', 13.5, color=TEXT, weight=600)
        s.circle(cx, cy, u, SAND, SAND, 1.2, .08)
        s.line(cx, cy, cx + u, cy, FAINT, 1.1, '3 3')
        s.circle(cx + u, cy, 5.5, CLAY)
        s.label(cx + u + 10, cy + 2, 'A (9, 5)', 12.5, 'start', CLAY, 600)
        if unit == 1:
            s.line(cx, cy, cx, cy - u, FAINT, 1.1, '3 3')
            s.circle(cx, cy - u, 5.5, BLUE)
            s.label(cx + 10, cy - u - 6, 'B (8, 6)', 12.5, 'start', BLUE, 600)
            s.mono(cx + u / 2, cy + 18, '1', 12, 'middle', MUTED)
            s.mono(cx - 8, cy - u / 2, '1', 12, 'end', MUTED)
        else:
            s.arrow(cx, cy - 8, cx, 38, BLUE, 1.6, '5 4')
            s.label(cx + 10, 52, 'B: cách 60, xa ngoài hình', 12.5, 'start', BLUE, 600)
            s.mono(cx + u / 2, cy + 18, '1', 12, 'middle', MUTED)
        s.circle(cx, cy, 6, TEXT, PAPER, 2)
        s.label(cx - 10, cy + 16, 'q', 13, 'end', TEXT, 600)
    s.line(320, 30, 320, 220, SOFT_LINE, 1)
    s.save('2-4-units', 'Cùng ba hồ sơ, chỉ đổi giờ sang phút: B từ cách q một đơn vị thành cách 60, nên A thành láng giềng duy nhất.')


def metrics24():
    s = Fig(640, 210)
    t = np.linspace(0, 2 * np.pi, 181)
    sc = 58
    for k_, (title, col) in enumerate([('Euclid', BLUE), ('Manhattan', CLAY), ('Cosine', GREEN)]):
        cx, cy = 110 + k_ * 210, 100
        s.line(cx - 80, cy, cx + 80, cy, SOFT_LINE, 1)
        s.line(cx, cy - 76, cx, cy + 76, SOFT_LINE, 1)
        if k_ < 2:
            U = np.c_[np.cos(t), np.sin(t)]
            if k_ == 1:
                U = U / np.abs(U).sum(1, keepdims=True)
            s.path('M ' + ' L '.join(f'{cx + a * sc:.1f},{cy - b * sc:.1f}' for a, b in U) + ' Z', col, 1.8)
        else:
            b = np.array([.5, .3]); a = 2 * b
            s.line(cx, cy, cx + 1.25 * sc * 1.25, cy - .75 * sc * 1.25, col, 1, '4 4')
            s.arrow(cx, cy, cx + a[0] * sc, cy - a[1] * sc, col, 2)
            s.arrow(cx, cy, cx + b[0] * sc, cy - b[1] * sc, TEXT, 2)
            s.label(cx + b[0] * sc + 4, cy - b[1] * sc + 14, 'B', 12.5, 'start', TEXT, 600)
            s.label(cx + a[0] * sc + 6, cy - a[1] * sc + 12, 'A = 2B', 12.5, 'start', col, 600)
            s.arrow(cx, cy, cx - .2 * sc, cy - .9 * sc, MUTED, 1.4)
            s.label(cx - .2 * sc - 6, cy - .9 * sc, 'C', 12.5, 'end', MUTED, 600)
        s.label(cx, 192, title, 14, color=col, weight=600)
    s.save('2-4-metrics', 'Euclid và Manhattan: các điểm cách gốc đúng 1. Cosine chỉ xét hướng: A = 2B có khoảng cách 0 tới B, còn C khác hướng thì xa.')


def curse24():
    s = Fig(640, 224)
    ax = s.axes(80, 30, 460, 150, (0, 2), (0, 1), yticks=[0, .5, 1], xlabel='số chiều d (thang log)')
    for e in (0, 1, 2):
        s.label(ax.X(e), ax.y + ax.h + 14, ['1', '10', '100'][e], 11, color=FAINT)
    lg = np.linspace(0, 2, 101)
    ax.line(lg, .1 ** (1 / 10 ** lg), CLAY, 2.4)
    for d, v, anc, dx, dy in [(1, .1, 'start', 10, 12), (10, .79, 'end', -10, -8), (100, .98, 'end', -10, 14)]:
        x = math.log10(d)
        s.circle(ax.X(x), ax.Y(v), 4.5, CLAY, PAPER, 2)
        s.mono(ax.X(x) + dx, ax.Y(v) + dy, f'{v:g}', 12, anc, TEXT)
    s.label(ax.x - 8, ax.y - 18, 'cạnh khối chứa 10% dữ liệu', 11.5, 'start', FAINT)
    s.save('2-4-curse', 'Muốn gom 10% dữ liệu rải đều, cạnh của khối lân cận dài 0.1 ở 1 chiều nhưng 0.98 ở 100 chiều.')


def wine24():
    from sklearn.datasets import load_wine
    D = load_wine()
    v = D.data.var(0)
    raw = v / v.sum()
    names = D.feature_names
    order = np.argsort(-raw)[:6]
    s = Fig(640, 230)
    for k_, (title, share) in enumerate([('chưa chuẩn hóa', raw), ('sau StandardScaler', np.full(13, 1 / 13))]):
        x0 = 160 + k_ * 250
        s.label(x0 + 100, 14, title, 13.5, color=TEXT, weight=600)
        for i, j in enumerate(order):
            y = 40 + i * 28
            w = 200 * share[j]
            s.rect(x0, y - 9, max(w, 1.5), 18, 'none', CLAY if names[j] == 'proline' else BLUE, 3, .8, 0)
            s.mono(x0 + max(w, 1.5) + 6, y, f'{share[j] * 100:.1f}%' if share[j] >= .001 else '<0.1%', 11, 'start', MUTED)
            if k_ == 0:
                s.mono(x0 - 12, y, names[j], 11.5, 'end', TEXT)
    s.label(320, 218, 'phần của mỗi cột trong bình phương khoảng cách (6 cột lớn nhất trên 13)', 11.5, color=MUTED)
    s.save('2-4-wine', 'Bộ wine: chưa chuẩn hóa, proline chiếm 99.8% bình phương khoảng cách; sau StandardScaler mỗi cột góp như nhau.')


FIGS24 = {'2-4-k': k24, '2-4-knn-vote': vote24, '2-4-units': units24, '2-4-metrics': metrics24, '2-4-curse': curse24,
          '2-4-wine': wine24}


# ───────────────────────────── 2.5 ─────────────────────────────

def node(s, x, y, text, w=None, color=LINE, size=12.5, fill=None, op=1):
    w = w or s.mono_width(text, size) + 22
    s.box(x - w / 2, y - 15, w, 30, color, fill or SURFACE, r=7, width=1.2, opacity=op)
    s.mono(x, y + .5, text, size, 'middle', TEXT)
    return w


def leaf(s, x, y, lab, counts, col):
    s.box(x - 62, y - 22, 124, 44, 'none', col, r=8, width=0, opacity=.14)
    s.label(x, y - 7, lab, 12.5, color=col, weight=600)
    s.mono(x, y + 11, counts, 11, 'middle', MUTED)


def partition25():
    from sklearn.datasets import make_moons
    from sklearn.tree import DecisionTreeClassifier
    X, y = make_moons(200, noise=.3, random_state=0)
    xs, ys = np.linspace(-1.6, 2.6, 106), np.linspace(-1.3, 1.7, 76)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    s = Fig(640, 220)
    for k_, dpt in enumerate((2, 8)):
        m = DecisionTreeClassifier(max_depth=dpt, random_state=0).fit(X, y)
        x0 = 20 + k_ * 315
        ax = s.axes(x0, 26, 290, 180, (-1.6, 2.6), (-1.3, 1.7), frame=False, grid=False)
        regions(s, ax, m.predict(G).reshape(len(ys), len(xs)), xs, ys, [BLUE, CLAY], .13)
        for lab, col in [(0, BLUE), (1, CLAY)]:
            ax.dots(X[y == lab, 0], X[y == lab, 1], col, 2.4)
        s.label(x0 + 145, 12, f'max_depth = {dpt}', 14, color=TEXT, weight=600)
    s.save('2-5-partition', 'Cây chia mặt phẳng thành các hộp có cạnh song song với trục; sâu 8 thì hộp nhỏ dần để ôm từng điểm nhiễu.')


def tree25():
    from sklearn.datasets import load_breast_cancer
    from sklearn.tree import DecisionTreeClassifier
    D = load_breast_cancer()
    t = DecisionTreeClassifier(max_depth=2, random_state=0).fit(D.data, D.target).tree_
    nm = lambda i: f'{D.feature_names[t.feature[i]]} ≤ {t.threshold[i]:.2f}'
    s = Fig(640, 250)
    pos = {0: (320, 26), 1: (170, 104), 4: (470, 104), 2: (95, 196), 3: (245, 196), 5: (395, 196), 6: (545, 196)}
    for p, (a, b) in [(0, (1, 4)), (1, (2, 3)), (4, (5, 6))]:
        for c_, side in [(a, 'có'), (b, 'không')]:
            s.line(pos[p][0], pos[p][1] + 15, pos[c_][0], pos[c_][1] - (15 if t.children_left[c_] >= 0 else 22), LINE, 1.2)
        mx, my = (pos[p][0] + pos[a][0]) / 2, (pos[p][1] + pos[a][1]) / 2
        s.label(mx - 8, my - 2, 'có', 11, 'end', FAINT)
        mx, my = (pos[p][0] + pos[b][0]) / 2, (pos[p][1] + pos[b][1]) / 2
        s.label(mx + 8, my - 2, 'không', 11, 'start', FAINT)
    for i in (0, 1, 4):
        node(s, *pos[i], nm(i), size=11.5)
    for i in (2, 3, 5, 6):
        v = t.value[i][0] * t.n_node_samples[i]
        mal, ben = int(round(v[0])), int(round(v[1]))
        lab, col = ('lành tính', GREEN) if ben > mal else ('ác tính', CLAY)
        leaf(s, *pos[i], lab, f'{mal} ác · {ben} lành', col)
    s.save('2-5-tree', 'Cây độ sâu 2 học trên bộ breast cancer (569 mẫu): mỗi lá ghi số mẫu ác tính và lành tính rơi vào đó.')


def gini25():
    p = np.linspace(0, 1, 201)
    s = Fig(640, 210)
    ax = s.axes(80, 20, 420, 150, (0, 1), (0, 1), xticks=[0, .25, .5, .75, 1], yticks=[0, .5, 1], xlabel='tỉ lệ lớp 1 trong nút')
    ent = -(np.where(p > 0, p * np.log2(np.clip(p, 1e-12, 1)), 0) + np.where(p < 1, (1 - p) * np.log2(np.clip(1 - p, 1e-12, 1)), 0))
    ax.line(p, ent, SAND, 2).line(p, 2 * p * (1 - p), CLAY, 2.2)
    s.label(ax.X(.5), ax.Y(1) - 10, 'entropy', 12.5, 'middle', SAND, 600)
    s.label(ax.X(.5), ax.Y(.5) + 18, 'Gini', 12.5, 'middle', CLAY, 600)
    s.circle(ax.X(.25), ax.Y(.375), 4.5, CLAY, PAPER, 2)
    s.mono(ax.X(.25) + 4, ax.Y(.375) + 18, '0.375', 11.5, 'start', CLAY)
    s.label(ax.X(1) + 12, ax.Y(0) - 4, 'nút thuần', 12, 'start', MUTED)
    s.save('2-5-gini', 'Gini và entropy của nút hai lớp: bằng 0 khi nút thuần, lớn nhất khi hai lớp chia đều; 3 mẫu lớp 0, 1 mẫu lớp 1 cho Gini 0.375.')


def splits25():
    s = Fig(640, 230)
    rows = [('A', [(4, 1), (1, 4)], [.32, .32], .18), ('B', [(5, 3), (0, 2)], [.469, 0], .125)]
    for r, (name, kids, gs, delta) in enumerate(rows):
        y = 50 + r * 100
        s.label(30, y + 10, name, 16, 'start', TEXT, 600)
        for c_, ((pos_, neg), g) in enumerate(zip(kids, gs)):
            x0 = 80 + c_ * 210
            vals = ['+'] * pos_ + ['−'] * neg
            for k, v in enumerate(vals):
                col = CLAY if v == '+' else BLUE
                s.circle(x0 + 12 + k * 20, y, 7, col, col, 0, .85)
            s.box(x0, y - 16, 20 * max(len(vals), 2) + 4, 32, LINE, 'none', r=8, width=1)
            s.mono(x0 + 2, y + 30, f'Gini {g:g}', 11.5, 'start', MUTED)
        s.mono(560, y, f'Δ = {delta:g}', 14, 'end', CLAY if r == 0 else MUTED, 600 if r == 0 else 400)
    s.label(560, 20, 'cha: 5+, 5−, Gini 0.5', 11.5, 'end', FAINT)
    s.save('2-5-splits', 'Hai cách chia cùng nút 5+, 5−: B có một lá thuần nhưng chỉ 2 mẫu; A giảm Gini nhiều hơn.')


def stump25():
    s = Fig(640, 200)
    ax = s.axes(120, 10, 300, 170, (.5, 4.5), (0, 3), frame=False, grid=False)
    for r, (t_, g) in enumerate([(1.5, .167), (2.5, .5), (3.5, .167)]):
        y = 34 + r * 56
        s.line(ax.X(.6), y, ax.X(4.4), y, SOFT_LINE, 1)
        for xv, lab in zip([1, 2, 3, 4], [0, 0, 1, 1]):
            s.circle(ax.X(xv), y, 6.5, BLUE if lab == 0 else CLAY)
        s.line(ax.X(t_), y - 18, ax.X(t_), y + 18, TEXT if t_ == 2.5 else FAINT, 1.6, '4 3')
        s.mono(ax.X(.6) - 14, y, f't = {t_}', 12.5, 'end', TEXT)
        s.mono(ax.X(4.4) + 30, y, f'giảm Gini {g:g}', 12.5, 'start', CLAY if t_ == 2.5 else MUTED, 600 if t_ == 2.5 else 400)
    for xv in (1, 2, 3, 4):
        s.mono(ax.X(xv), 188, str(xv), 11.5, 'middle', FAINT)
    s.save('2-5-stump', 'Ba ngưỡng trên bốn mẫu x = 1, 2, 3, 4 (nhãn 0, 0, 1, 1): chỉ t = 2.5 cho hai lá thuần.')


def stumptree25():
    s = Fig(640, 170)
    node(s, 320, 30, 'x ≤ 2.5', 120)
    for xx, lab, col, txt in [(200, 'lớp 0', BLUE, 'x = 1, 2'), (440, 'lớp 1', CLAY, 'x = 3, 4')]:
        s.line(320, 45, xx, 108, LINE, 1.2)
        leaf(s, xx, 130, lab, txt, col)
    s.label(250, 72, 'có', 11, 'end', FAINT)
    s.label(390, 72, 'không', 11, 'start', FAINT)
    s.save('2-5-stump-tree', 'Decision stump ngưỡng 2.5: hai lá thuần, Gini sau chia bằng 0.')


def staircase25():
    from sklearn.tree import DecisionTreeClassifier
    rng = np.random.default_rng(0)
    X = rng.random((2000, 2))
    y = (X[:, 1] > X[:, 0]).astype(int)
    xs = ys = np.linspace(0, 1, 101)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    s = Fig(640, 240)
    for k_, dpt in enumerate((3, 8)):
        m = DecisionTreeClassifier(max_depth=dpt, random_state=0).fit(X, y)
        x0 = 90 + k_ * 270
        ax = s.axes(x0, 30, 190, 190, (0, 1), (0, 1), frame=False, grid=False)
        regions(s, ax, m.predict(G).reshape(101, 101), xs, ys, [BLUE, CLAY], .16)
        s.line(ax.X(0), ax.Y(0), ax.X(1), ax.Y(1), TEXT, 1.4, '5 4')
        s.box(ax.x, ax.y, ax.w, ax.h, LINE, 'none', r=0, width=1)
        s.label(x0 + 95, 14, f'max_depth = {dpt} · {m.get_n_leaves()} lá', 13.5, color=TEXT, weight=600)
    s.save('2-5-staircase', 'Ranh giới thật là đường chéo x₂ = x₁ (nét đứt): cây chỉ xấp xỉ được bằng bậc thang, càng sát càng nhiều lá.')


def xor25():
    s = Fig(640, 200)
    for k_, (title, vert) in enumerate([('chia theo x₁', True), ('chia theo x₂', False)]):
        x0 = 120 + k_ * 260
        ax = s.axes(x0, 30, 140, 140, (-.3, 1.3), (-.3, 1.3), frame=False, grid=False)
        for (a, b), lab in [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]:
            s.circle(ax.X(a), ax.Y(b), 9, BLUE if lab == 0 else CLAY)
            s.mono(ax.X(a), ax.Y(b) + .5, str(lab), 11, 'middle', PAPER)
        if vert:
            s.line(ax.X(.5), ax.y, ax.X(.5), ax.y + ax.h, TEXT, 1.4, '5 4')
        else:
            s.line(ax.x, ax.Y(.5), ax.x + ax.w, ax.Y(.5), TEXT, 1.4, '5 4')
        s.label(x0 + 70, 14, title, 13.5, color=TEXT, weight=600)
        s.mono(x0 + 70, 188, 'giảm Gini = 0', 12, 'middle', CLAY)
    s.save('2-5-xor', 'XOR: chia ở gốc theo x₁ hay x₂ đều để mỗi bên một mẫu mỗi lớp, nên giảm Gini bằng 0 dù tầng sau tách được hết.')


def extrap25():
    from sklearn.tree import DecisionTreeRegressor
    rng = np.random.default_rng(3)
    x = rng.uniform(0, 10, 60)
    y = 2 * x + 3 + rng.normal(0, 2, 60)
    t = DecisionTreeRegressor(max_depth=3, random_state=0).fit(x[:, None], y)
    w, b = np.polyfit(x, y, 1)
    xs = np.linspace(0, 15, 601)
    s = Fig(640, 220)
    ax = s.axes(60, 20, 500, 160, (0, 15), (0, 36), xticks=[0, 5, 10, 15], yticks=[0, 10, 20, 30], xlabel='x')
    s.rect(ax.X(10), ax.y, ax.X(15) - ax.X(10), ax.h, 'none', SAND, 0, .1, 0)
    s.label(ax.X(12.5), ax.y + ax.h - 14, 'ngoài vùng train', 12, color=SAND, weight=600)
    ax.dots(x, y, FAINT, 2.8)
    ax.line(xs, w * xs + b, BLUE, 2, '6 4')
    ax.step(xs, t.predict(xs[:, None]), CLAY, 2.2)
    s.label(ax.X(15) + 6, ax.Y(w * 15 + b), 'tuyến tính', 12, 'start', BLUE, 600)
    s.label(ax.X(15) + 6, ax.Y(t.predict([[15]])[0]), 'cây', 12, 'start', CLAY, 600)
    s.save('2-5-extrapolate', 'Cây hồi quy là hằng số từng khúc: ra ngoài vùng train nó giữ nguyên giá trị lá cuối, còn đường thẳng kéo dài xu hướng.')


FIGS25 = {'2-5-partition': partition25, '2-5-tree': tree25, '2-5-gini': gini25, '2-5-splits': splits25, '2-5-stump': stump25,
          '2-5-stump-tree': stumptree25, '2-5-staircase': staircase25, '2-5-xor': xor25, '2-5-extrapolate': extrap25}


# ───────────────────────────── 2.6 ─────────────────────────────

def variance26():
    B = np.arange(1, 101)
    s = Fig(640, 220)
    ax = s.axes(70, 20, 440, 160, (1, 100), (0, 1), xticks=[1, 25, 50, 75, 100], yticks=[0, .25, .5, .75, 1], xlabel='số cây B')
    for rho, col in [(.5, CLAY), (.1, BLUE)]:
        ax.line(B, rho + (1 - rho) / B, col, 2.2)
        ax.hline(rho, col, 1, '4 4')
        s.label(ax.X(100) + 8, ax.Y(rho + (1 - rho) / 100), f'ρ = {rho}', 12.5, 'start', col, 600)
    s.label(ax.X(52), ax.Y(.5) - 10, 'sàn ρσ²', 11.5, 'start', MUTED)
    s.save('2-6-variance', 'Phương sai của trung bình B cây (σ² = 1): thêm cây chỉ kéo về mức sàn ρσ²; giảm tương quan mới hạ được sàn.')


def bootstrap26():
    ns = lesson_ns('2.6', upto=1)
    draw = ns['draw']
    s = Fig(640, 190)
    s.label(40, 34, 'rút', 12.5, 'start', MUTED)
    s.tiles(110, 18, [[str(v) for v in draw]], 44, 34, SAND, 8, size=15)
    cnt = np.bincount(draw, minlength=5)
    s.label(40, 128, 'mẫu', 12.5, 'start', MUTED)
    for i in range(5):
        x = 110 + i * 52
        oob = cnt[i] == 0
        s.box(x, 108, 44, 40, CLAY if oob else BLUE, 'none' if oob else BLUE, r=6, width=1.6 if oob else 0, opacity=1 if oob else .14,
              dash='4 3' if oob else None)
        s.mono(x + 22, 128.5, str(i), 15, 'middle', CLAY if oob else TEXT)
        s.mono(x + 22, 164, '×' + str(cnt[i]), 11.5, 'middle', MUTED)
    s.label(400, 120, 'OOB của cây này', 13, 'start', CLAY, 600)
    s.mono(400, 140, ', '.join(str(i) for i in range(5) if cnt[i] == 0), 13, 'start', CLAY)
    s.save('2-6-bootstrap', f'Một lượt bootstrap từ code bài: rút {", ".join(map(str, draw))}; mẫu 3 và 4 lặp hai lần, mẫu 0 và 1 không được rút nên là OOB.')


def oobtable26():
    boots = [[1, 1, 3, 4, 4], [2, 2, 3, 5, 5], [1, 2, 2, 4, 5]]
    s = Fig(640, 200)
    for j in range(5):
        s.mono(170 + j * 64 + 26, 20, f'mẫu {j + 1}', 12, 'middle', MUTED)
    for i, b in enumerate(boots):
        y = 36 + i * 46
        s.label(150, y + 18, f'cây {i + 1}', 13, 'end', TEXT, 600)
        for j in range(5):
            c = b.count(j + 1)
            x = 170 + j * 64
            if c:
                s.box(x, y, 52, 36, 'none', BLUE, r=6, width=0, opacity=.08 + .1 * c)
                s.mono(x + 26, y + 18.5, f'×{c}', 13, 'middle', TEXT)
            else:
                s.box(x, y, 52, 36, CLAY, 'none', r=6, width=1.5, dash='4 3')
                s.mono(x + 26, y + 18.5, 'OOB', 12, 'middle', CLAY)
    s.save('2-6-oob-table', 'Ví dụ tính tay: ba tập bootstrap trên 5 mẫu; ô nét đứt là mẫu cây đó chưa thấy, dùng để chấm OOB.')


def vote26():
    s = Fig(640, 200)
    ax = s.axes(120, 20, 330, 140, (0, 1), (-.5, 3.5), xticks=[0, .5, 1], frame=False, grid=False, xlabel='xác suất lớp 1')
    s.line(ax.X(0), ax.y + ax.h, ax.X(1), ax.y + ax.h, LINE, 1)
    for i, p in enumerate([.9, .4, .4]):
        y = ax.Y(3 - i)
        col = CLAY if p > .5 else BLUE
        s.rect(ax.X(0), y - 10, ax.X(p) - ax.X(0), 20, 'none', col, 3, .75, 0)
        s.label(ax.X(0) - 10, y, f'cây {i + 1}', 12.5, 'end', TEXT)
        s.mono(ax.X(p) + 6, y, f'{p}', 12, 'start', MUTED)
    m = (0.9 + .4 + .4) / 3
    y = ax.Y(0)
    s.rect(ax.X(0), y - 10, ax.X(m) - ax.X(0), 20, 'none', TEXT, 3, .6, 0)
    s.label(ax.X(0) - 10, y, 'trung bình', 12.5, 'end', TEXT, 600)
    s.mono(ax.X(m) + 6, y, f'{m:.2f} → lớp 1', 12, 'start', TEXT, 600)
    s.line(ax.X(.5), ax.y - 4, ax.X(.5), ax.y + ax.h, FAINT, 1.2, '4 3')
    s.label(470, ax.Y(2), 'bỏ phiếu: 1 trên 3', 12.5, 'start', BLUE, 600)
    s.label(470, ax.Y(2) + 20, '→ lớp 0', 12.5, 'start', BLUE, 600)
    s.save('2-6-vote', 'Ba cây cho xác suất 0.9, 0.4, 0.4: trung bình xác suất chọn lớp 1, bỏ phiếu chọn lớp 0.')


def trees26():
    from sklearn.datasets import make_moons
    from sklearn.ensemble import RandomForestClassifier
    X, y = make_moons(200, noise=.3, random_state=0)
    rf = RandomForestClassifier(200, random_state=0).fit(X, y)
    xs, ys = np.linspace(-1.6, 2.6, 141), np.linspace(-1.3, 1.7, 101)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    s = Fig(640, 360)
    panels = [(rf.estimators_[k].predict(G), f'cây {k + 1}') for k in range(3)] + [((rf.predict_proba(G)[:, 1] > .5).astype(int), 'rừng 200 cây')]
    for k_, (pred, title) in enumerate(panels):
        x0, y0 = 30 + (k_ % 2) * 300, 26 + (k_ // 2) * 172
        ax = s.axes(x0, y0, 280, 140, (-1.6, 2.6), (-1.3, 1.7), frame=False, grid=False)
        regions(s, ax, pred.astype(int).reshape(len(ys), len(xs)), xs, ys, [BLUE, CLAY], .16)
        for lab, col in [(0, BLUE), (1, CLAY)]:
            ax.dots(X[y == lab, 0], X[y == lab, 1], col, 2, opacity=.85)
        s.label(x0 + 140, y0 - 13, title, 13, color=TEXT, weight=600 if k_ == 3 else 400)
    s.save('2-6-trees', 'Ba cây trong cùng một rừng, mỗi cây học một tập bootstrap nên ranh giới khác nhau; trung bình 200 cây cho ranh giới mượt hơn.')


def ntrees26():
    from sklearn.datasets import load_breast_cancer
    from sklearn.ensemble import RandomForestClassifier
    import warnings
    X, y = load_breast_cancer(return_X_y=True)
    Bs = [10, 15, 20, 30, 40, 60, 80, 120, 160, 240, 320]
    s = Fig(640, 220)
    ax = s.axes(70, 20, 440, 160, (0, 320), (.91, .975), xticks=[0, 80, 160, 240, 320], yticks=[.91, .93, .95, .97],
                xlabel='số cây', yfmt='{:.2f}')
    for mf, col, lab in [('sqrt', BLUE, 'max_features = √d'), (None, CLAY, 'xét mọi feature (bagging)')]:
        acc = []
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            for b in Bs:
                acc.append(RandomForestClassifier(b, max_features=mf, oob_score=True, random_state=0).fit(X, y).oob_score_)
        ax.line(Bs, acc, col, 2)
        ax.dots(Bs, acc, col, 2.6)
        k = 7 if mf else 9
        s.label(ax.X(Bs[k]), ax.Y(acc[k]) + (-12 if mf else 16), lab, 12, 'middle', col, 600)
    s.label(ax.x - 8, ax.y - 12, 'OOB accuracy', 11.5, 'start', FAINT)
    s.save('2-6-ntrees', 'Breast cancer: OOB accuracy theo số cây. Với √d feature mỗi nút, sau khoảng 80 cây đường gần như đứng yên; bagging thuần cần nhiều cây hơn mới bắt kịp.')


FIGS26 = {'2-6-variance': variance26, '2-6-bootstrap': bootstrap26, '2-6-oob-table': oobtable26, '2-6-vote': vote26,
          '2-6-trees': trees26, '2-6-ntrees': ntrees26}


# ───────────────────────────── 2.7 ─────────────────────────────

def fitstages27():
    from sklearn.ensemble import GradientBoostingRegressor
    rng = np.random.default_rng(0)
    x = np.sort(rng.uniform(0, 6, 120))
    y = np.sin(x) + rng.normal(0, .25, 120)
    m = GradientBoostingRegressor(n_estimators=100, max_depth=1, learning_rate=.3, random_state=0).fit(x[:, None], y)
    xs = np.linspace(0, 6, 601)
    stages = list(m.staged_predict(xs[:, None]))
    s = Fig(640, 190)
    for k_, M in enumerate((1, 10, 100)):
        x0 = 20 + k_ * 210
        ax = s.axes(x0, 26, 190, 140, (0, 6), (-1.7, 1.7), frame=False, grid=False)
        ax.dots(x, y, FAINT, 1.8, opacity=.8)
        ax.line(xs, np.sin(xs), MUTED, 1, '4 3')
        ax.step(xs, stages[M - 1], CLAY, 2)
        s.label(x0 + 95, 12, f'{M} cây', 13.5, color=TEXT, weight=600)
    s.save('2-7-fit-stages', 'Cộng dần các stump: 1 cây chỉ là một bậc, 10 cây đã theo dáng sóng, 100 cây bám sát đường cong (nét đứt là hàm thật).')


def stages27():
    preds = [2, 1.5, 1.25, 1.125]
    mse = [1, .25, .0625, .015625]
    s = Fig(640, 220)
    ax = s.axes(90, 20, 420, 150, (-.2, 3.2), (.8, 3.2), xticks=[0, 1, 2, 3], yticks=[1, 2, 3], grid=False)
    s.label(ax.x - 8, ax.y + ax.h + 14, 'số cây', 11, 'end', FAINT)
    for tgt, col, lab in [(1, BLUE, 'mẫu 0, 1'), (3, CLAY, 'mẫu 2, 3')]:
        ax.hline(tgt, col, 1, '4 4')
        vals = [p if tgt == 1 else 4 - p for p in preds]
        ax.line([0, 1, 2, 3], vals, col, 2.2)
        for i, v in enumerate(vals):
            s.circle(ax.X(i), ax.Y(v), 4.5, col, PAPER, 2)
        s.label(ax.X(3.2) + 8, ax.Y(tgt), f'{lab}: target {tgt}', 12, 'start', col, 600)
    for i, e in enumerate(mse):
        s.mono(ax.X(i), ax.y + ax.h + 30, f'MSE {e:g}', 11.5, 'middle', MUTED)
    s.save('2-7-stages', 'Bốn mẫu target 1, 1, 3, 3, learning rate 0.5: mỗi cây sửa một nửa phần còn thiếu, MSE giảm 1 → 0.25 → 0.0625 → 0.015625.')


def hand27():
    x = np.array([1, 2, 3, 4]); y = np.array([1, 2, 6, 7])
    F1 = np.array([2.75, 2.75, 5.25, 5.25])
    s = Fig(640, 230)
    ax = s.axes(110, 16, 360, 180, (.4, 4.6), (0, 8), xticks=[1, 2, 3, 4], yticks=[0, 2, 4, 6, 8], xlabel='x')
    ax.hline(4, FAINT, 1.4, '5 4')
    s.label(ax.X(4.6) + 8, ax.Y(4), 'F₀ = 4', 12, 'start', MUTED)
    ax.step([.4, 2.5, 4.6], [2.75, 5.25, 5.25], CLAY, 2.2)
    s.label(ax.X(4.6) + 8, ax.Y(5.25), 'F₁', 12.5, 'start', CLAY, 600)
    s.line(ax.X(2.5), ax.y, ax.X(2.5), ax.y + ax.h, SOFT_LINE, 1)
    s.mono(ax.X(2.5) + 6, ax.y + 6, 'x ≤ 2.5', 11, 'start', MUTED)
    for xi, yi, fi in zip(x, y, F1):
        s.line(ax.X(xi) + 6, ax.Y(4), ax.X(xi) + 6, ax.Y(yi), BLUE, 1.2, '2 3')
        s.circle(ax.X(xi), ax.Y(yi), 5, TEXT)
    s.label(500, 70, 'phần dư từ F₀', 12, 'start', BLUE, 600)
    s.mono(500, 90, '−3  −2  2  3', 12, 'start', BLUE)
    s.label(500, 130, 'MSE', 12, 'start', MUTED)
    s.mono(500, 150, '6.5 → 1.81', 12.5, 'start', TEXT)
    s.save('2-7-hand', 'Ví dụ tính tay: F₀ = 4, stump chia ở 2.5 khớp phần dư; cộng một nửa bản sửa cho F₁, MSE từ 6.5 xuống 1.81.')


def rfboost27():
    s = Fig(640, 210)
    s.label(20, 22, 'random forest', 13.5, 'start', TEXT, 600)
    for i in range(4):
        x = 40 + i * 70
        s.box(x, 44, 52, 30, BLUE, BLUE, r=6, width=0, opacity=.16)
        s.label(x + 26, 59, f'cây {i + 1}', 11.5, color=TEXT)
        s.line(x + 26, 76, 180, 104, LINE, 1)
    s.box(130, 104, 100, 28, LINE, SURFACE, r=6, width=1.2)
    s.label(180, 118, 'trung bình', 12, color=TEXT)
    s.label(170, 160, 'song song, cây sâu', 12, color=MUTED)
    s.label(170, 180, 'giảm variance', 12, color=BLUE, weight=600)
    s.line(330, 20, 330, 194, SOFT_LINE, 1)
    s.label(360, 22, 'boosting', 13.5, 'start', TEXT, 600)
    for i in range(4):
        x = 360 + i * 70
        s.box(x, 60, 52, 30, CLAY, CLAY, r=6, width=0, opacity=.16)
        s.label(x + 26, 75, f'cây {i + 1}', 11.5, color=TEXT)
        if i:
            s.arrow(x - 16, 75, x - 3, 75, CLAY, 1.3)
    s.label(495, 110, 'mỗi cây sửa phần dư của tổng trước nó', 11.5, color=MUTED)
    s.label(495, 160, 'nối tiếp, cây nông', 12, color=MUTED)
    s.label(495, 180, 'giảm bias', 12, color=CLAY, weight=600)
    s.save('2-7-rf-vs-boost', 'Random forest học các cây độc lập rồi lấy trung bình; boosting học các cây nối tiếp, cây sau sửa lỗi của tổng trước nó.')


def pseudo27():
    r = np.linspace(-3, 3, 241)
    s = Fig(640, 210)
    for k_, (title, f, col) in enumerate([('bình phương: r', r, BLUE), ('trị tuyệt đối: sign(r)', np.sign(r), CLAY)]):
        x0 = 60 + k_ * 300
        ax = s.axes(x0, 30, 240, 140, (-3, 3), (-3, 3), xticks=[-3, 0, 3], yticks=[-3, 0, 3], xlabel='r = y − F')
        s.line(ax.X(0), ax.y, ax.X(0), ax.y + ax.h, SOFT_LINE, 1)
        if k_:
            ax.line(r[r < 0], f[r < 0], col, 2.4).line(r[r > 0], f[r > 0], col, 2.4)
        else:
            ax.line(r, f, col, 2.4)
        s.label(x0 + 120, 14, title, 13, color=col, weight=600)
    s.save('2-7-pseudo', 'Pseudo-residual mà cây phải khớp: với bình phương là chính phần dư; với trị tuyệt đối chỉ còn ±1, nên outlier lệch xa không có tiếng nói lớn hơn.')


def earlystop27():
    ns = lesson_ns('2.7', upto=2)
    tr, va = np.array(ns['train_losses']), np.array(ns['valid_losses'])
    b = ns['best_round']
    rounds = np.arange(1, len(tr) + 1)
    s = Fig(640, 220)
    ax = s.axes(70, 20, 440, 160, (0, 300), (0, 40), xticks=[0, 31, 100, 200, 300], yticks=[0, 10, 20, 30, 40], xlabel='số cây')
    ax.line(rounds, tr, BLUE, 2).line(rounds, va, CLAY, 2.2)
    s.line(ax.X(b), ax.y, ax.X(b), ax.y + ax.h, FAINT, 1, '3 3')
    s.circle(ax.X(b), ax.Y(va[b - 1]), 4.5, CLAY, PAPER, 2)
    s.mono(ax.X(b) + 8, ax.Y(va[b - 1]) + 16, f'{va[b - 1]:.2f}', 11.5, 'start', CLAY)
    s.label(ax.X(300) + 8, ax.Y(va[-1]), f'validation {va[-1]:.2f}', 12, 'start', CLAY, 600)
    s.label(ax.X(300) + 8, ax.Y(tr[-1]) - 6, f'train {tr[-1]:.2f}', 12, 'start', BLUE, 600)
    s.label(ax.x - 8, ax.y - 12, 'MSE', 11.5, 'start', FAINT)
    s.save('2-7-early-stop', 'Friedman1 nhiễu 4, cây sâu 3: MSE train giảm mãi; MSE validation thấp nhất ở vòng 31 rồi tăng lại.')


def lr27():
    from sklearn.datasets import make_friedman1
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    X, y = make_friedman1(2000, noise=1.0, random_state=0)
    Xt, Xv, yt, yv = train_test_split(X, y, test_size=.3, random_state=0)
    s = Fig(640, 220)
    N = 3000
    L = math.log10
    ax = s.axes(70, 20, 470, 160, (0, L(N)), (0, 26), yticks=[0, 8, 16, 24], xlabel='số cây (thang log)')
    for e, lab in [(0, '1'), (1, '10'), (2, '100'), (3, '1000')]:
        s.label(ax.X(e), ax.y + ax.h + 14, lab, 11, color=FAINT)
    for lr, col in [(.1, CLAY), (.01, BLUE)]:
        m = GradientBoostingRegressor(n_estimators=N, max_depth=3, learning_rate=lr, random_state=0).fit(Xt, yt)
        v = np.array([np.mean((p - yv) ** 2) for p in m.staged_predict(Xv)])
        ax.line(np.log10(np.arange(1, N + 1)), v, col, 2)
        b = int(np.argmin(v))
        s.circle(ax.X(L(b + 1)), ax.Y(v[b]), 4.5, col, PAPER, 2)
        if lr == .1:
            s.mono(ax.X(L(b + 1)) - 10, ax.Y(v[b]) - 9, f'vòng {b + 1}', 11, 'end', col)
        else:
            s.mono(ax.X(L(b + 1)), ax.Y(v[b]) - 14, f'vòng {b + 1}', 11, 'middle', col)
        xl = 12 if lr == .1 else 120
        s.label(ax.X(L(xl)) + 8, ax.Y(v[xl]) - 6, f'η = {lr}', 12.5, 'start', col, 600)
    s.label(ax.x - 8, ax.y - 12, 'MSE validation', 11.5, 'start', FAINT)
    s.save('2-7-lr', 'Friedman1, cây sâu 3: learning rate 0.01 cần nhiều cây hơn hẳn 0.1 mới tới đáy (chấm tròn là vòng tốt nhất).')


def oof27():
    """2.7 mục K-fold: mỗi fold chấm phần màu, ghép năm phần thành dự đoán out-of-fold."""
    auc = [.929, .898, .920, .905, .934]
    s = Fig(640, 236)
    x0, w, h, g = 92, 72, 22, 4
    for c in range(5):
        s.t(x0 + c * (w + g) + w / 2, 14, f'phần {c + 1}', 12, 'middle', MUTED, font='sans')
    for k in range(5):
        y = 30 + k * 32
        s.mono(x0 - 14, y + h / 2 + 4, f'fold {k}', 12.5, 'end', MUTED)
        for c in range(5):
            on = c == k
            s.box(x0 + c * (w + g), y, w, h, CLAY if on else SOFT_LINE, ACCENT_SOFT if on else CODE_BG, r=5, width=1.4 if on else 1)
        s.mono(x0 + 5 * (w + g) + 10, y + h / 2 + 4, f'AUC {auc[k]:.3f}', 12.5, 'start', TEXT)
    y = 30 + 5 * 32 + 12
    s.mono(x0 - 14, y + h / 2 + 4, 'oof', 12.5, 'end', CLAY, weight=600)
    for c in range(5):
        s.box(x0 + c * (w + g), y, w, h, CLAY, ACCENT_SOFT, r=5, width=1.4)
    s.mono(x0 + 5 * (w + g) + 10, y + h / 2 + 4, 'AUC 0.917', 12.5, 'start', CLAY, weight=600)
    s.save('2-7-oof', 'Mỗi fold chấm một phần; ghép năm phần được dự đoán out-of-fold.')


FIGS27 = {'2-7-fit-stages': fitstages27, '2-7-stages': stages27, '2-7-hand': hand27, '2-7-rf-vs-boost': rfboost27,
          '2-7-pseudo': pseudo27, '2-7-early-stop': earlystop27, '2-7-lr': lr27, '2-7-oof': oof27}


# ───────────────────────────── 2.8 ─────────────────────────────

def svm_lines(s, ax, w, b, col=TEXT, n=300):
    """Vẽ f = 0 (liền) và f = ±1 (nét đứt) của SVM tuyến tính 2 chiều, cắt theo khung."""
    for c, wd, dash in [(0, 2, None), (1, 1.2, '5 4'), (-1, 1.2, '5 4')]:
        segline(ax, lambda x: (c - b - w[0] * x) / w[1], col, wd, dash, n)


def margin28():
    from sklearn.svm import SVC
    rng = np.random.default_rng(4)
    A = rng.normal([1.2, 1.4], .45, (22, 2)); B = rng.normal([3, 3.1], .45, (22, 2))
    X = np.r_[A, B]; y = np.r_[-np.ones(22), np.ones(22)]
    m = SVC(kernel='linear', C=1e4).fit(X, y)
    w, b = m.coef_[0], m.intercept_[0]
    s = Fig(640, 290)
    ax = s.axes(150, 16, 300, 260, (-.6, 4.6), (-.2, -.2 + 5.2 * 260 / 300), frame=False, grid=False)
    svm_lines(s, ax, w, b)
    for lab, col in [(-1, BLUE), (1, CLAY)]:
        k = y == lab
        ax.dots(X[k, 0], X[k, 1], col, 4)
    for i in m.support_:
        s.circle(ax.X(X[i, 0]), ax.Y(X[i, 1]), 8.5, TEXT, 'none', 1.4)
    s.label(500, 70, 'f(x) = 0', 12.5, 'start', TEXT, 600)
    s.label(500, 92, 'f(x) = ±1 (nét đứt)', 12.5, 'start', MUTED)
    s.label(500, 130, 'khoanh: support vector', 12.5, 'start', MUTED)
    s.mono(500, 160, f'lề = 2/‖w‖ = {2 / np.linalg.norm(w):.2f}', 12.5, 'start', TEXT)
    s.save('2-8-margin', 'SVM lề cứng: vạch f = 0 nằm giữa hai đường lề; chỉ các điểm khoanh tròn trên lề quyết định vị trí vạch.')


def hinge28():
    m = np.linspace(-2, 3, 201)
    s = Fig(640, 220)
    ax = s.axes(80, 20, 420, 160, (-2, 3), (0, 3), xticks=[-2, -1, 0, 1, 2, 3], yticks=[0, 1, 2, 3], xlabel='y·f(x)')
    s.rect(ax.X(0), ax.y, ax.X(1) - ax.X(0), ax.h, 'none', SAND, 0, .1, 0)
    ax.line(m, np.log1p(np.exp(-m)) / math.log(2), BLUE, 2, '6 4')
    ax.line(m, np.maximum(0, 1 - m), CLAY, 2.4)
    s.label(ax.X(.5), ax.y + 12, 'trong lề', 11.5, color=SAND, weight=600)
    s.label(ax.X(-1.6), ax.Y(2.9) + 4, 'hinge', 12.5, 'start', CLAY, 600)
    s.label(ax.X(3) + 8, ax.Y(np.log1p(np.exp(-3)) / math.log(2)) - 8, 'log loss', 12, 'start', BLUE, 600)
    s.label(ax.X(3) + 8, ax.Y(0) + 6, 'hinge = 0', 12, 'start', CLAY, 600)
    s.save('2-8-hinge', 'Hinge loss bằng đúng 0 khi y·f(x) ≥ 1; log loss (chia ln 2 để cùng mốc) thì luôn dương, nên mọi điểm đều có tiếng nói.')


def c28():
    from sklearn.svm import SVC
    rng = np.random.default_rng(1)
    A = rng.normal([1.4, 1.5], .7, (40, 2)); B = rng.normal([2.8, 2.9], .7, (40, 2))
    X = np.r_[A, B]; y = np.r_[-np.ones(40), np.ones(40)]
    s = Fig(640, 290)
    for k_, C in enumerate((.01, 100)):
        m = SVC(kernel='linear', C=C).fit(X, y)
        w, b = m.coef_[0], m.intercept_[0]
        x0 = 30 + k_ * 320
        ax = s.axes(x0, 32, 260, 240, (-.8, 4.8), (-.6, -.6 + 5.6 * 240 / 260), frame=False, grid=False)
        svm_lines(s, ax, w, b)
        for lab, col in [(-1, BLUE), (1, CLAY)]:
            kk = y == lab
            ax.dots(X[kk, 0], X[kk, 1], col, 3)
        for i in m.support_:
            s.circle(ax.X(X[i, 0]), ax.Y(X[i, 1]), 6.5, TEXT, 'none', 1)
        s.label(x0 + 130, 14, f'C = {C:g} · {len(m.support_)} support vector', 13, color=TEXT, weight=600)
    s.line(320, 20, 320, 276, SOFT_LINE, 1)
    s.save('2-8-c', 'Cùng dữ liệu chồng nhau: C nhỏ chịu nhiều vi phạm, lề rộng, nhiều support vector; C lớn ép lề hẹp quanh vùng chồng lấn.')


def gamma28():
    from sklearn.datasets import make_moons
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler
    X, y = make_moons(200, noise=.3, random_state=0)
    X = StandardScaler().fit_transform(X)
    xs, ys = np.linspace(-2.4, 2.4, 121), np.linspace(-2.4, 2.4, 121)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    s = Fig(640, 230)
    for k_, g in enumerate((.1, 1, 100)):
        m = SVC(kernel='rbf', C=1, gamma=g).fit(X, y)
        x0 = 20 + k_ * 210
        ax = s.axes(x0, 26, 190, 190, (-2.4, 2.4), (-2.4, 2.4), frame=False, grid=False)
        regions(s, ax, m.predict(G).reshape(121, 121), xs, ys, [BLUE, CLAY], .15)
        for lab, col in [(0, BLUE), (1, CLAY)]:
            ax.dots(X[y == lab, 0], X[y == lab, 1], col, 2)
        s.label(x0 + 95, 12, f'γ = {g:g}', 13.5, color=TEXT, weight=600)
    s.save('2-8-gamma', 'SVM RBF, C = 1: γ nhỏ cho ranh giới gần thẳng; γ = 1 theo dáng hai mặt trăng; γ = 100 khoanh từng điểm, dấu hiệu overfit.')


def kernel28():
    x = np.array([-2.6, -2.2, -1.8, -.4, -.1, .3, .6, 1.9, 2.3, 2.7])
    y = (np.abs(x) > 1.2).astype(int)
    s = Fig(640, 230)
    ax = s.axes(40, 40, 240, 150, (-3, 3), (-1, 1), frame=False, grid=False)
    s.line(ax.X(-3), ax.Y(0), ax.X(3), ax.Y(0), LINE, 1)
    for xi, yi in zip(x, y):
        s.circle(ax.X(xi), ax.Y(0), 6, CLAY if yi else BLUE)
    s.label(160, 18, 'trên trục x: không vạch nào tách được', 12.5, color=TEXT, weight=600)
    s.mono(160, 210, 'x', 12, 'middle', MUTED)
    s.arrow(296, 115, 340, 115, MUTED, 1.4)
    s.mono(318, 103, 'φ', 13, 'middle', MUTED)
    ax2 = s.axes(370, 40, 240, 150, (-3, 3), (-.5, 8), frame=False, grid=False)
    s.line(ax2.X(-3), ax2.Y(0), ax2.X(3), ax2.Y(0), LINE, 1)
    s.line(ax2.X(0), ax2.Y(-.5), ax2.X(0), ax2.Y(8), SOFT_LINE, 1)
    for xi, yi in zip(x, y):
        s.circle(ax2.X(xi), ax2.Y(xi * xi), 6, CLAY if yi else BLUE)
    ax2.hline(1.6 ** 2 / 1.0 * .6 + .4, TEXT, 1.6, '6 4')
    s.label(490, 18, 'sau φ(x) = (x, x²): một đường ngang', 12.5, color=TEXT, weight=600)
    s.mono(490, 210, '(x, x²)', 12, 'middle', MUTED)
    s.save('2-8-kernel', 'Hai lớp xen kẽ trên một trục không tách được bằng một ngưỡng; thêm tọa độ x² thì một đường thẳng tách được ngay.')


def hand28():
    w, b = np.array([3., 4.]), -10.
    s = Fig(640, 280)
    ax = s.axes(160, 14, 300, 240, (1.4, 3.6), (.4, .4 + 2.2 * 240 / 300), xticks=[2, 3], yticks=[1, 2], grid=False)
    svm_lines(s, ax, w, b)
    pts = [((2, 1), MUTED), ((3, 2), GREEN), ((2, 1.1), CLAY)]
    for (px, py), col in pts:
        s.circle(ax.X(px), ax.Y(py), 5, col)
    s.mono(480, 60, 'w = (3, 4), b = −10', 12.5, 'start', TEXT)
    s.mono(480, 84, 'lề = 2/5 = 0.4', 12.5, 'start', TEXT)
    s.label(480, 124, '(3, 2): ngoài lề, hinge 0', 12, 'start', GREEN, 600)
    s.label(480, 146, '(2, 1.1): trong lề, hinge 0.6', 12, 'start', CLAY, 600)
    s.label(480, 168, '(2, 1): ngay trên vạch', 12, 'start', MUTED, 600)
    s.save('2-8-hand', 'Ví dụ tính tay: vạch 3x₁ + 4x₂ = 10 và hai đường lề; điểm (2, 1.1) đúng phía nhưng nằm trong lề nên vẫn chịu hinge 0.6.')


FIGS28 = {'2-8-margin': margin28, '2-8-hinge': hinge28, '2-8-c': c28, '2-8-gamma': gamma28, '2-8-kernel': kernel28, '2-8-hand': hand28}


# ───────────────────────────── 2.9 ─────────────────────────────

def gray_img(s, x, y, img, c=5, vmax=16):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            v = max(0., min(1., img[i, j] / vmax))
            if v > .04:
                s.rect(x + j * c, y + i * c, c + .2, c + .2, 'none', TEXT, 0, min(.92, v), 0)
    s.box(x, y, img.shape[1] * c, img.shape[0] * c, SOFT_LINE, 'none', r=2, width=.8)


def pca29():
    rng = np.random.default_rng(2)
    X = rng.multivariate_normal([0, 0], [[2.5, 1.5], [1.5, 1.2]], 120)
    X -= X.mean(0)
    vals, vecs = np.linalg.eigh(np.cov(X.T, bias=True))
    s = Fig(640, 260)
    ax = s.axes(170, 10, 300, 240, (-3.6, 3.6), (-2.88, 2.88), frame=False, grid=False)
    u1, u2 = vecs[:, 1] * np.sign(vecs[0, 1]), vecs[:, 0] * -np.sign(vecs[0, 0])
    for p in X[::8]:
        q = (p @ u1) * u1
        s.line(ax.X(p[0]), ax.Y(p[1]), ax.X(q[0]), ax.Y(q[1]), FAINT, .8)
    ax.dots(X[:, 0], X[:, 1], BLUE, 2.6, opacity=.7)
    for u, lam, col, lab in [(u1, vals[1], CLAY, 'PC1'), (u2, vals[0], GREEN, 'PC2')]:
        e = u * 2 * math.sqrt(lam)
        s.arrow(ax.X(0), ax.Y(0), ax.X(e[0]), ax.Y(e[1]), col, 2.4)
        s.label(500, 90 if lab == 'PC1' else 114, f'{lab} · λ = {lam:.2f}', 12.5, 'start', col, 600)
    s.save('2-9-pca', 'Đám mây đã trừ trung bình: PC1 theo hướng trải dài nhất, PC2 vuông góc; nét mảnh là phép chiếu xuống PC1.')


def hand29():
    X = np.array([[-2., -1.], [-1., -1.], [1., 1.], [2., 1.]])
    u = np.array([.851, .526])
    s = Fig(640, 230)
    ax = s.axes(180, 14, 280, 200, (-2.8, 2.8), (-2, 2), frame=False, grid=False)
    s.line(ax.X(-2.8), ax.Y(0), ax.X(2.8), ax.Y(0), SOFT_LINE, 1)
    s.line(ax.X(0), ax.Y(-2), ax.X(0), ax.Y(2), SOFT_LINE, 1)
    s.line(ax.X(-2.7 * u[0]), ax.Y(-2.7 * u[1]), ax.X(2.7 * u[0]), ax.Y(2.7 * u[1]), CLAY, 1.8)
    for p in X:
        q = (p @ u) * u
        s.line(ax.X(p[0]), ax.Y(p[1]), ax.X(q[0]), ax.Y(q[1]), MUTED, 1, '3 3')
        s.circle(ax.X(q[0]), ax.Y(q[1]), 4, CLAY, PAPER, 1.8)
        s.circle(ax.X(p[0]), ax.Y(p[1]), 5, BLUE)
    s.label(ax.X(2.7 * u[0]) + 8, ax.Y(2.7 * u[1]), 'u₁ ≈ (0.851, 0.526)', 12, 'start', CLAY, 600)
    s.label(490, 120, 'λ₁ ≈ 3.427 · λ₂ ≈ 0.073', 12, 'start', TEXT)
    s.label(490, 142, 'PC1 giữ 97.9%', 12, 'start', CLAY, 600)
    s.label(490, 172, 'vòng rỗng: điểm tái tạo', 11.5, 'start', MUTED)
    s.save('2-9-hand', 'Ví dụ tính tay: bốn điểm gần một đường thẳng; chiếu xuống PC1 rồi tái tạo, mỗi điểm chỉ lệch một đoạn ngắn.')


def label29():
    rng = np.random.default_rng(5)
    n = 80
    big = rng.normal(0, 2.2, 2 * n)
    small = np.r_[rng.normal(-.45, .15, n), rng.normal(.45, .15, n)]
    lab = np.r_[np.zeros(n), np.ones(n)]
    s = Fig(640, 240)
    ax = s.axes(40, 20, 280, 190, (-6, 6), (-4, 4), frame=False, grid=False)
    s.line(ax.X(-6), ax.Y(0), ax.X(6), ax.Y(0), CLAY, 1.6)
    s.label(ax.X(6) - 4, ax.Y(0) - 10, 'PC1', 12, 'end', CLAY, 600)
    for c_, col in [(0, BLUE), (1, CLAY)]:
        k = lab == c_
        ax.dots(big[k], small[k] * 3, col, 2.4, opacity=.8)
    s.label(180, 226, 'hai lớp chỉ khác nhau theo chiều dọc', 11.5, color=MUTED)
    for r, (title, v, sc) in enumerate([('tọa độ PC1', big, 6), ('tọa độ PC2', small, 1.2)]):
        y0 = 70 + r * 90
        s.label(360, y0 - 26, title, 12.5, 'start', TEXT, 600)
        s.line(360, y0, 620, y0, SOFT_LINE, 1)
        for c_, col in [(0, BLUE), (1, CLAY)]:
            k = lab == c_
            for val, j in zip(v[k], jit(k.sum(), 9 + c_ + r, 7)):
                s.circle(490 + val / sc * 125, y0 + j + (-9 if c_ == 0 else 9) * r, 2.2, col, None, 0, .75)
    s.save('2-9-label', 'PCA không biết nhãn: PC1 chọn hướng nhiễu trải rộng nên hai lớp trộn lẫn; hướng phương sai nhỏ PC2 mới tách được chúng.')


def scree29():
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    X, _ = load_digits(return_X_y=True)
    s = Fig(640, 220)
    ax = s.axes(70, 20, 440, 160, (1, 64), (0, 1), xticks=[1, 16, 32, 48, 64], yticks=[0, .5, .95], yfmt='{:g}', xlabel='số thành phần giữ lại')
    ax.hline(.95, FAINT, 1, '4 3')
    for name, data, col in [('thô', X, BLUE), ('chuẩn hóa', StandardScaler().fit_transform(X), CLAY)]:
        c = np.cumsum(PCA().fit(data).explained_variance_ratio_)
        ax.line(np.arange(1, 65), c, col, 2.2)
        k = int(np.searchsorted(c, .95)) + 1
        s.line(ax.X(k), ax.Y(.95), ax.X(k), ax.y + ax.h, col, 1, '3 3')
        s.circle(ax.X(k), ax.Y(.95), 4.5, col, PAPER, 2)
        s.mono(ax.X(k) + 5, ax.y + ax.h - 10, f'{k}', 11.5, 'start', col)
        s.label(ax.X(64) + 8, ax.Y(c[-1]) + (-8 if name == 'thô' else 8), name, 12.5, 'start', col, 600)
    s.label(ax.x - 8, ax.y - 12, 'phương sai giữ lại (tích lũy)', 11.5, 'start', FAINT)
    s.save('2-9-scree', 'Digits: giữ 95% phương sai cần 29 thành phần trên dữ liệu thô nhưng 40 sau khi chuẩn hóa từng pixel.')


def recon29():
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA
    X, y = load_digits(return_X_y=True)
    idx = [int(np.where(y == d)[0][0]) for d in (0, 3, 5, 8)]
    s = Fig(640, 296)
    ks = [2, 5, 10, 29, 64]
    for j, k in enumerate(ks):
        s.label(132 + j * 100 + 28, 16, f'k = {k}' if k < 64 else 'gốc', 12.5, color=TEXT, weight=600)
    for i, r in enumerate(idx):
        for j, k in enumerate(ks):
            img = X[r] if k == 64 else PCA(k).fit(X).inverse_transform(PCA(k).fit(X).transform(X[r:r + 1]))[0]
            gray_img(s, 132 + j * 100, 30 + i * 66, img.reshape(8, 8), 7)
    s.save('2-9-recon', 'Ảnh chữ số 8 × 8 tái tạo từ k thành phần chính: 2 thành phần chỉ còn vệt mờ, 10 đã đọc được, 29 gần như ảnh gốc.')


def tsne29():
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    X, y = load_digits(return_X_y=True)
    s = Fig(640, 270)
    for k_, (title, Z) in enumerate([('PCA 2 chiều', PCA(2).fit_transform(X)),
                                     ('t-SNE', TSNE(2, random_state=0, init='pca', perplexity=30).fit_transform(X))]):
        x0 = 30 + k_ * 310
        Z = np.asarray(Z, dtype=float)
        lo, hi = Z.min(0), Z.max(0)
        ax = s.axes(x0, 30, 270, 225, (lo[0], hi[0]), (lo[1], hi[1]), frame=False, grid=False)
        ax.dots(Z[:, 0], Z[:, 1], FAINT, 1.6, opacity=.55)
        for d in range(10):
            m = np.median(Z[y == d], 0)
            s.circle(ax.X(m[0]), ax.Y(m[1]), 10, CLAY, PAPER, 1.4)
            s.mono(ax.X(m[0]), ax.Y(m[1]) + .5, str(d), 12, 'middle', CLAY, 600)
        s.label(x0 + 135, 14, title, 13.5, color=TEXT, weight=600)
    s.line(320, 20, 320, 260, SOFT_LINE, 1)
    s.save('2-9-tsne', 'Digits xuống 2 chiều: PCA để các chữ số chồng lên nhau, t-SNE tách thành cụm; khoảng cách giữa các cụm t-SNE không mang nghĩa.')


FIGS29 = {'2-9-pca': pca29, '2-9-hand': hand29, '2-9-label': label29, '2-9-scree': scree29, '2-9-recon': recon29, '2-9-tsne': tsne29}


# ───────────────────────────── 2.10 ─────────────────────────────

def numrow(s, x0, x1, y, lo, hi, ticks=None):
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    s.line(x0, y, x1, y, LINE, 1)
    for t_ in ticks or []:
        s.mono(X(t_), y + 18, f'{t_:g}', 11, 'middle', FAINT)
    return X


def cross(s, x, y, col, r=6):
    s.line(x - r, y - r, x + r, y + r, col, 2.6)
    s.line(x - r, y + r, x + r, y - r, col, 2.6)


def assign210():
    s = Fig(640, 200)
    pts = [0, 1, 5, 6]
    for r, (title, cen, J) in enumerate([('gán', [0, 6], 2), ('cập nhật tâm', [.5, 5.5], 1)]):
        y = 50 + r * 80
        X = numrow(s, 150, 470, y, -.5, 6.5, [0, 1, 5, 6] if r else None)
        s.label(20, y, title, 12.5, 'start', TEXT, 600 if r else 400)
        for p in pts:
            s.circle(X(p), y, 6, BLUE if p < 3 else CLAY)
        for c_, col in zip(cen, [BLUE, CLAY]):
            cross(s, X(c_), y - 20, col)
            s.mono(X(c_), y - 36, f'{c_:g}', 11, 'middle', col)
        s.mono(500, y, f'inertia {J}', 12.5, 'start', TEXT if r else MUTED, 600 if r else 400)
    s.save('2-10-kmeans-assign', 'Một vòng Lloyd trên bốn điểm 0, 1, 5, 6: gán theo tâm gần nhất, rồi dời tâm (dấu ×) về trung bình nhóm; inertia từ 2 xuống 1.')


def lloyd210():
    steps = [([1, 2], [0, 1, 1, 1, 1], 194), ([1, 8], [0, 1, 1, 1, 1], 50), ([1, 8], [0, 0, 1, 1, 1], 15), ([1.5, 10], [0, 0, 1, 1, 1], 2.5)]
    names = ['khởi tạo', 'cập nhật', 'gán lại', 'cập nhật']
    pts = [1, 2, 9, 10, 11]
    s = Fig(640, 270)
    for r, ((cen, lab, J), nm) in enumerate(zip(steps, names)):
        y = 44 + r * 58
        X = numrow(s, 130, 500, y, 0, 12, [1, 2, 9, 10, 11] if r == 3 else None)
        s.label(20, y, nm, 12.5, 'start', TEXT)
        for p, l_ in zip(pts, lab):
            s.circle(X(p), y, 6, BLUE if l_ == 0 else CLAY)
        for c_, col in zip(cen, [BLUE, CLAY]):
            cross(s, X(c_), y - 20, col, 5)
        s.mono(530, y, f'J = {J:g}', 12.5, 'start', TEXT if r == 3 else MUTED)
    s.save('2-10-lloyd', 'Ví dụ tính tay với khởi tạo tệ (tâm 1 và 2): sau hai vòng điểm 2 đổi cụm, J giảm 194 → 50 → 15 → 2.5.')


def moons210():
    ns = lesson_ns('2.10', upto=4)
    X, y = ns['X'], ns['y']
    from sklearn.cluster import DBSCAN, KMeans
    from sklearn.metrics import adjusted_rand_score, silhouette_score
    s = Fig(640, 240)
    for k_, (name, m) in enumerate([('K-Means', KMeans(n_clusters=2, n_init=10, random_state=0)), ('DBSCAN', DBSCAN(eps=.3, min_samples=5))]):
        lab = m.fit_predict(X)
        ari, sil = adjusted_rand_score(y, lab), silhouette_score(X, lab)
        x0 = 30 + k_ * 310
        lo, hi = X.min(0) - .1, X.max(0) + .1
        ax = s.axes(x0, 34, 270, 190, (lo[0], hi[0]), (lo[1], hi[1]), frame=False, grid=False)
        for c_, col in [(0, BLUE), (1, CLAY), (-1, SAND)]:
            ax.dots(X[lab == c_, 0], X[lab == c_, 1], col, 2.4, opacity=.85)
        s.label(x0 + 135, 12, name, 13.5, color=TEXT, weight=600)
        s.mono(x0 + 135, 28, f'ARI {ari:.2f} · silhouette {sil:.2f}', 11.5, 'middle', MUTED)
    s.line(320, 10, 320, 230, SOFT_LINE, 1)
    s.save('2-10-moons', 'Hai trăng khuyết (code bài): K-Means cắt theo tâm nên trộn hai trăng; DBSCAN theo mật độ tách đúng, dù silhouette chấm thấp hơn.')


def density210():
    s = Fig(640, 180)
    pos = {0: 80, .1: 170, .2: 260, .35: 395, 3: 560}
    kind = {0: ('border', BLUE), .1: ('core', CLAY), .2: ('core', CLAY), .35: ('border', BLUE), 3: ('noise', SAND)}
    y = 90
    s.line(50, y, 450, y, LINE, 1)
    s.line(520, y, 600, y, LINE, 1)
    s.mono(485, y, '…', 14, 'middle', FAINT)
    for k_, c_ in enumerate((.1, .2)):
        x = pos[c_]
        yy = y - 26 - k_ * 14
        s.line(x - .16 * 900, yy, x + .16 * 900, yy, CLAY, 1.4)
        s.line(x - .16 * 900, yy - 4, x - .16 * 900, yy + 4, CLAY, 1.4)
        s.line(x + .16 * 900, yy - 4, x + .16 * 900, yy + 4, CLAY, 1.4)
    s.mono(pos[.2] + .16 * 900 + 8, y - 40, 'eps = 0.16', 11.5, 'start', CLAY)
    for v, x in pos.items():
        nm, col = kind[v]
        s.circle(x, y, 7, col)
        s.mono(x, y + 22, f'{v:g}', 11.5, 'middle', MUTED)
        s.label(x, y + 44, nm, 12.5, color=col, weight=600)
    s.save('2-10-density', 'eps = 0.16, min_samples = 3: 0.1 và 0.2 là core (đoạn ngang là bán kính quanh chúng); 0 và 0.35 là border, vẫn vào cụm; 3 là noise.')


def elbow210():
    from sklearn.cluster import KMeans
    from sklearn.datasets import make_blobs
    from sklearn.metrics import silhouette_score
    X, _ = make_blobs(400, centers=4, cluster_std=1.0, random_state=3)
    Ks = list(range(2, 10))
    inert, sil = [], []
    for K in Ks:
        m = KMeans(K, n_init=10, random_state=0).fit(X)
        inert.append(m.inertia_); sil.append(silhouette_score(X, m.labels_))
    s = Fig(640, 220)
    for k_, (title, v, col) in enumerate([('inertia', inert, BLUE), ('silhouette', sil, CLAY)]):
        x0 = 60 + k_ * 310
        lo, hi = min(v), max(v)
        ax = s.axes(x0, 34, 240, 140, (1.6, 9.4), (0 if k_ == 0 else lo - .05, hi * 1.05), xticks=Ks, xlabel='K', grid=False)
        ax.line(Ks, v, col, 2).dots(Ks, v, col, 3)
        b = 4
        s.circle(ax.X(b), ax.Y(v[b - 2]), 6.5, TEXT, 'none', 1.4)
        s.label(x0 - 8, 16, title, 13, 'start', col, 600)
    s.save('2-10-elbow', 'Bốn cụm sinh sẵn: inertia giảm mãi theo K nhưng gãy khúc ở K = 4; silhouette cao nhất cũng ở K = 4.')


def linkage210():
    s = Fig(640, 150)
    X = numrow(s, 80, 560, 110, -.5, 10.5, [0, 1, 3, 10])
    for p, col in [(0, BLUE), (1, BLUE), (3, CLAY), (10, CLAY)]:
        s.circle(X(p), 110, 7, col)
    s.curve(X(1), 100, X(3), 100, -.45, GREEN, 1.8, head=False)
    s.label((X(1) + X(3)) / 2, 128, 'single: 2', 12.5, color=GREEN, weight=600)
    s.curve(X(0), 98, X(10), 98, -.3, SAND, 1.8, head=False)
    s.label((X(0) + X(10)) / 2, 18, 'complete: 10', 12.5, color=SAND, weight=600)
    s.save('2-10-linkage', 'Hai cụm {0, 1} và {3, 10}: single linkage đo cặp gần nhất (2), complete linkage đo cặp xa nhất (10).')


def circles210():
    from sklearn.cluster import KMeans, SpectralClustering
    from sklearn.datasets import make_circles
    from sklearn.metrics import adjusted_rand_score
    X, y = make_circles(400, factor=.4, noise=.05, random_state=0)
    s = Fig(640, 250)
    for k_, (name, m) in enumerate([('K-Means', KMeans(2, n_init=10, random_state=0)),
                                     ('spectral', SpectralClustering(2, affinity='nearest_neighbors', random_state=0))]):
        lab = m.fit_predict(X)
        x0 = 60 + k_ * 310
        ax = s.axes(x0, 34, 210, 200, (-1.2, 1.2), (-1.2, 1.2 * 200 / 210 * 1.0 + 0.0), frame=False, grid=False)
        ax.ylim = (-1.2 * 200 / 210, 1.2 * 200 / 210)
        for c_, col in [(0, BLUE), (1, CLAY)]:
            ax.dots(X[lab == c_, 0], X[lab == c_, 1], col, 2.4, opacity=.85)
        s.label(x0 + 105, 12, name, 13.5, color=TEXT, weight=600)
        a = adjusted_rand_score(y, lab)
        s.mono(x0 + 105, 28, f'ARI {abs(a) if abs(a) < .005 else a:.2f}', 11.5, 'middle', MUTED)
    s.line(320, 10, 320, 240, SOFT_LINE, 1)
    s.save('2-10-circles', 'Hai vòng đồng tâm: K-Means cắt đôi theo một đường thẳng; spectral clustering trên đồ thị láng giềng tách đúng từng vòng.')


FIGS210 = {'2-10-kmeans-assign': assign210, '2-10-lloyd': lloyd210, '2-10-moons': moons210, '2-10-density': density210,
           '2-10-elbow': elbow210, '2-10-linkage': linkage210, '2-10-circles': circles210}


# ───────────────────────────── 2.11 ─────────────────────────────

def cyclic211():
    s = Fig(640, 240)
    X = numrow(s, 30, 290, 120, 0, 23, [0, 6, 12, 18, 23])
    for h in range(24):
        s.circle(X(h), 120, 3, FAINT)
    for h, col in [(0, CLAY), (23, CLAY), (12, BLUE)]:
        s.circle(X(h), 120, 6, col)
    s.curve(X(0), 108, X(23), 108, -.18, CLAY, 1.4, head=False)
    s.mono((X(0) + X(23)) / 2, 66, '|23 − 0| = 23', 12, 'middle', CLAY)
    s.label(160, 22, 'số giờ thô', 13, color=TEXT, weight=600)
    s.line(320, 20, 320, 224, SOFT_LINE, 1)
    cx, cy, R = 480, 128, 80
    s.circle(cx, cy, R, LINE, 'none', 1)
    s.line(cx, cy - R, cx, cy + R, BLUE, 1, '4 3')
    for h in range(24):
        a = 2 * math.pi * h / 24
        x, y = cx + R * math.sin(a), cy - R * math.cos(a)
        col = CLAY if h in (0, 23) else BLUE if h == 12 else FAINT
        s.circle(x, y, 6 if h in (0, 23, 12) else 3, col)
        if h in (6, 12, 18):
            s.mono(cx + (R + 16) * math.sin(a), cy - (R + 16) * math.cos(a), str(h), 11, 'middle', MUTED)
    s.mono(cx + 10, cy - R - 12, '0', 11, 'start', CLAY)
    s.mono(cx - 28, cy - R - 10, '23', 11, 'end', CLAY)
    s.mono(cx + 40, cy - R - 12, '0–23: 0.26', 11.5, 'start', CLAY)
    s.mono(cx + 8, cy + 30, '0–12: 2', 11.5, 'start', BLUE)
    s.label(cx, 14, '(sin, cos) trên vòng tròn', 13, color=TEXT, weight=600)
    s.save('2-11-cyclic', 'Số giờ thô đặt 23 giờ xa 0 giờ nhất; mã hóa (sin, cos) đặt chúng cạnh nhau trên vòng tròn.')


def time211():
    sales = [5, 7, 6]
    s = Fig(640, 230)
    xs = {1: 150, 2: 270, 3: 390}
    s.label(150, 20, 'giờ 1', 12, color=MUTED); s.label(270, 20, 'giờ 2', 12, color=MUTED); s.label(390, 20, 'giờ 3 (cần dự đoán)', 12, color=CLAY, weight=600)
    for h, v in zip((1, 2, 3), sales):
        col = CLAY if h == 3 else BLUE
        s.box(xs[h] - 32, 36, 64, 34, 'none', col, r=6, width=0, opacity=.14)
        s.mono(xs[h], 53.5, f'{v}', 15, 'middle', TEXT)
    rows = [('lag_1 = 7', [2], GREEN, 'đúng'), ('shift(1).rolling(2) = 6', [1, 2], GREEN, 'đúng'), ('rolling(2) = 6.5', [2, 3], CLAY, 'sai: chứa target')]
    for r, (lab, hs, col, note) in enumerate(rows):
        y = 104 + r * 40
        x0, x1 = xs[min(hs)] - 30, xs[max(hs)] + 30
        s.line(x0, y, x1, y, col, 2.4)
        s.line(x0, y - 6, x0, y + 6, col, 2); s.line(x1, y - 6, x1, y + 6, col, 2)
        s.mono(470, y, lab, 12, 'start', TEXT)
        s.label(110, y, note, 12, 'end', col, 600)
    s.save('2-11-time', 'Dự đoán giờ 3 của cửa hàng A: lag và rolling sau shift(1) chỉ dùng giờ 1–2; rolling thẳng ôm luôn doanh số giờ 3 cần dự đoán.')


def log211():
    rng = np.random.default_rng(0)
    x = rng.lognormal(2.5, 1.0, 3000)
    s = Fig(640, 210)
    for k_, (title, v, col) in enumerate([('thu nhập (lệch phải)', x, BLUE), ('log(1 + x)', np.log1p(x), CLAY)]):
        x0 = 40 + k_ * 310
        hist, edges = np.histogram(v, bins=40, range=(0, np.percentile(v, 99.5)))
        ax = s.axes(x0, 30, 260, 140, (edges[0], edges[-1]), (0, hist.max() * 1.05), frame=True, grid=False)
        for h, a, b in zip(hist, edges[:-1], edges[1:]):
            s.rect(ax.X(a) + .5, ax.Y(h), max(ax.X(b) - ax.X(a) - 1, .5), ax.Y(0) - ax.Y(h), 'none', col, 1, .75, 0)
        s.label(x0 + 130, 14, title, 13, color=col, weight=600)
    s.save('2-11-log', 'Cùng 3000 giá trị thu nhập: phân phối gốc dồn sát 0 với đuôi dài; sau log(1 + x) gần cân đối, hợp với mô hình tuyến tính và kNN.')


def te211():
    n = np.arange(0, 61)
    s = Fig(640, 220)
    ax = s.axes(80, 20, 420, 160, (0, 60), (0, 1), xticks=[0, 3, 10, 20, 40, 60], yticks=[0, .3, .5, 1], xlabel='số mẫu n_c của giá trị')
    ax.hline(.3, FAINT, 1, '4 3')
    for yb, col, lab in [(1, CLAY, 'trung bình riêng 1.0'), (.5, BLUE, 'trung bình riêng 0.5')]:
        ax.line(n, (n * yb + 10 * .3) / (n + 10), col, 2.2)
        s.label(ax.X(60) + 8, ax.Y((60 * yb + 3) / 70), lab, 12, 'start', col, 600)
    for nc, yb, nm, col in [(3, 1, 'A', CLAY), (20, .5, 'B', BLUE)]:
        v = (nc * yb + 3) / (nc + 10)
        s.circle(ax.X(nc), ax.Y(v), 5, col, PAPER, 2)
        s.mono(ax.X(nc) + (-8 if nm == 'A' else 0), ax.Y(v) + (-16 if nm == 'A' else -16), f'{nm}: {v:.2f}', 11.5, 'end' if nm == 'A' else 'middle', col)
    s.label(ax.X(60) + 8, ax.Y(.3), 'tỉ lệ chung 0.3', 11.5, 'start', FAINT)
    s.save('2-11-te', 'Target encoding làm mượt với m = 10: giá trị ít mẫu bị kéo về tỉ lệ chung 0.3, nhiều mẫu thì tiến dần về trung bình riêng.')


FIGS211 = {'2-11-cyclic': cyclic211, '2-11-time': time211, '2-11-log': log211, '2-11-te': te211}


# ───────────────────────────── kt1 ─────────────────────────────

def splits_kt1():
    rng = np.random.default_rng(3)
    nS, nT = 5, 5
    rand = rng.random((nS, nT)) < .25
    panels = [('random theo hàng', rand), ('group theo học sinh', np.array([[i == 3] * nT for i in range(nS)])),
              ('theo thời gian', np.array([[t >= 4 for t in range(nT)] for _ in range(nS)]))]
    s = Fig(640, 230)
    for k_, (title, V) in enumerate(panels):
        x0 = 60 + k_ * 200
        s.label(x0 + 70, 16, title, 13, color=TEXT, weight=600)
        fills = {(i, j): ((CLAY, .55) if V[i, j] else (BLUE, .14)) for i in range(nS) for j in range(nT)}
        s.tiles(x0, 32, [[''] * nT] * nS, 24, 24, BLUE, 5, fills)
        if k_ == 0:
            for i in range(nS):
                s.label(x0 - 10, 44 + i * 29, f'HS {i + 1}', 11, 'end', MUTED)
        s.label(x0 + 70, 194, 'lần đo →', 11, color=FAINT)
    s.box(250, 212, 14, 12, 'none', BLUE, r=3, width=0, opacity=.14)
    s.label(270, 218, 'train', 11.5, 'start', MUTED)
    s.box(330, 212, 14, 12, 'none', CLAY, r=3, width=0, opacity=.55)
    s.label(350, 218, 'validation', 11.5, 'start', MUTED)
    s.save('2-kt1-splits', 'Ba cách chia cùng một bảng học sinh × lần đo: random theo hàng để mỗi người nằm cả hai phía; group giữ người mới cho validation; theo thời gian giữ lần đo sau mốc cắt.')


def folds_kt1():
    sc = {'median': [1.362, 1.345, 1.22], 'ridge': [.352, .345, .252]}
    s = Fig(640, 140)
    ax = s.axes(150, 6, 400, 84, (0, 1.5), (.3, 2.6), xticks=[0, .5, 1, 1.5], xlabel='MAE theo fold', frame=True, grid=False)
    for r, (nm, v) in enumerate(sc.items()):
        y = ax.Y(2 - r * 1.1)
        col = MUTED if nm == 'median' else CLAY
        s.line(ax.X(min(v)), y, ax.X(max(v)), y, col, 1.2)
        for k, x in enumerate(v):
            s.circle(ax.X(x), y, 5, col)
        s.mono(ax.x - 14, y, nm, 12.5, 'end', col)
        s.mono(ax.X(max(v)) + 10, y, f'mean {np.mean(v):.3f}', 11.5, 'start', col)
    s.save('2-kt1-folds', 'MAE của median baseline và Ridge trên đúng ba fold: Ridge thấp hơn ở mọi fold, không chỉ ở trung bình.')


FIGSKT1 = {'2-kt1-splits': splits_kt1, '2-kt1-folds': folds_kt1}


FIGS = {'2-1-residuals': residuals21, '2-1-projection': projection21, '2-1-gd1d': gd1d21, '2-1-scaling': scaling21,
        '2-1-lr': lr21, '2-1-residual-plots': resplots21, '2-1-loglog': loglog21, '2-1-hand': hand21,
        '2-2-overfit': overfit22, '2-2-validation': validation22, '2-2-geometry': geometry22, '2-2-shrink': shrink22,
        '2-2-hand': hand22, '2-2-collinear': collinear22, '2-2-path': path22, '2-2-units': units22, '2-2-enet': enet22, **FIGS23, **FIGS24, **FIGS25, **FIGS26, **FIGS27, **FIGS28, **FIGS29, **FIGS210, **FIGS211, **FIGSKT1}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
