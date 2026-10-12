"""Lượt 8 — hình chương 1 (bản gọn). Số liệu lấy bằng cách chạy chính code của bài.
Chạy riêng: python -B -X utf8 p8_ch1.py [tên ...]"""
import contextlib, io, re, sys
from pathlib import Path
from kit import *

PAPER = 'var(--paper, var(--bg, #faf9f5))'
CONTENT = Path(__file__).resolve().parent.parent / 'content'


def lesson_ns(lesson, upto=None):
    """Chạy các khối ```python của bài (tới khối thứ `upto`) và trả không gian tên."""
    text = (CONTENT / f'phase-{lesson.split(".")[0]}' / f'{lesson}.md').read_text(encoding='utf-8')
    blocks = re.findall(r'^```python\n(.*?)^```', text, re.M | re.S)
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for b in blocks[:upto]:
            exec(compile(b, lesson, 'exec'), ns)
    return ns


# ───────────────────────────── 1.1 ─────────────────────────────

def contract11():
    s = Fig(640, 196)
    rows = [('21', '0.02', '19'), ('21', '0.84', '15'), ('54', '0.47', '41')]
    s.label(118, 14, 'X: biết chiều thứ Sáu', 13, color=BLUE)
    s.label(530, 14, 'y: đếm sáng thứ Bảy', 13, color=CLAY)
    for j, h in enumerate(['registered', 'rain']):
        s.mono(58 + j * 96, 40, h, 12, 'middle', MUTED)
    s.mono(530, 40, 'attendance', 12, 'middle', MUTED)
    for i, (r, p, a) in enumerate(rows):
        y = 58 + i * 34
        s.tiles(20, y, [[r, p]], 76, 28, BLUE, 20, size=14)
        s.tiles(492, y, [[a]], 76, 28, CLAY, size=14)
    s.box(250, 76, 136, 62, LINE, 'none', r=10, width=1.3)
    s.label(318, 101, 'mô hình', 14, color=TEXT, weight=600)
    s.mono(318, 121, 'f(x) = ŷ', 12.5, 'middle', MUTED)
    s.arrow(196, 107, 246, 107, BLUE, 1.4)
    s.arrow(390, 107, 486, 107, MUTED, 1.4, dash='4 3')
    s.label(438, 94, 'so sánh', 12, color=MUTED)
    s.label(320, 176, 'mỗi hàng là một buổi sinh hoạt', 12.5, color=MUTED)
    s.save('1-1-contract', 'Từ thông tin chiều thứ Sáu, mô hình đoán số người đến; nhãn chỉ có sau buổi.')


def tasks11():
    s = Fig(640, 196)
    cols = [(110, 'Classification', '≥ 30 người?'), (320, 'Regression', 'bao nhiêu người?'), (530, 'Clustering', 'không có nhãn')]
    for x, title, q in cols:
        s.label(x, 16, title, 14, color=TEXT, weight=600)
        s.label(x, 176, q, 13, color=MUTED)
    # classification: hai nhãn
    for k, (lab, col) in enumerate([('có', CLAY), ('không', BLUE)]):
        s.pill(110, 70 + k * 46, lab, col, 14)
    # regression: một số
    s.mono(320, 92, '28.4', 26, 'middle', CLAY, 600)
    s.label(320, 124, 'một số thực', 12.5, color=FAINT)
    # clustering: hai nhóm điểm
    import math
    for (cx, cy, col) in [(500, 74, BLUE), (562, 120, CLAY)]:
        s.circle(cx, cy, 26, col, 'none', 1.2)
        for k in range(4):
            a = k * math.pi / 2 + .5
            s.circle(cx + 11 * math.cos(a), cy + 11 * math.sin(a), 4, col)
    s.line(215, 40, 215, 160, SOFT_LINE, 1)
    s.line(425, 40, 425, 160, SOFT_LINE, 1)
    s.save('1-1-task-types', 'Loại bài toán do đầu ra quyết định: một nhãn, một số, hay chưa có nhãn.')


def timeline11():
    s = Fig(640, 120)
    x0, W, y = 30, 580, 36
    parts = [('train', 80, BLUE), ('valid', 20, CLAY), ('test', 20, SAND)]
    x = x0
    for name, n, col in parts:
        w = W * n / 120
        s.box(x + 2, y, w - 4, 36, 'none', col, r=6, width=0, opacity=.22)
        s.label(x + w / 2, y + 18, f'{name} · {n}', 14, color=col, weight=600)
        x += w
    s.arrow(x0, y + 60, x0 + W, y + 60, FAINT, 1.2)
    s.label(x0 + W, y + 76, 'thời gian', 12, 'end', FAINT)
    for v in (0, 80, 100, 120):
        s.label(x0 + W * v / 120, y + 46, str(v), 11.5, color=FAINT)
    s.save('1-1-timeline', 'Chia theo thứ tự buổi: học trên quá khứ, chọn và chấm trên các buổi sau.')


def mae11():
    s = Fig(640, 186)
    true, pred = [20, 30, 40], [18, 33, 39]
    for k, (tv, pv) in enumerate(zip(true, pred)):
        y = 34 + k * 52
        X = lambda v: 300 + (v - tv) * 34
        s.label(30, y, f'buổi {k + 1}', 13, 'start', MUTED)
        s.line(X(tv - 4.5), y, X(tv + 4.5), y, SOFT_LINE, 1)
        for v in range(tv - 4, tv + 5):
            s.line(X(v), y - 3, X(v), y + 3, LINE, 1)
        s.label(X(tv - 4), y + 16, str(tv - 4), 11, color=FAINT)
        s.label(X(tv + 4), y + 16, str(tv + 4), 11, color=FAINT)
        s.line(X(tv), y, X(pv), y, CLAY, 4)
        s.circle(X(tv), y, 6, TEXT)
        s.circle(X(pv), y, 6, CLAY, PAPER, 2)
        s.label((X(tv) + X(pv)) / 2, y - 16, str(abs(tv - pv)), 14, color=CLAY, weight=600)
    s.circle(500, 34, 5, TEXT)
    s.label(512, 34, 'thật', 12.5, 'start', MUTED)
    s.circle(500, 58, 5, CLAY, PAPER, 2)
    s.label(512, 58, 'dự đoán', 12.5, 'start', MUTED)
    s.mono(500, 112, '(2 + 3 + 1) / 3', 13, 'start', CLAY)
    s.mono(500, 134, '= 2 người', 13, 'start', CLAY, 600)
    s.save('1-1-mae', 'MAE là trung bình độ dài các đoạn sai số, tính theo đơn vị người.')


def baseline11():
    import numpy as np
    ns = lesson_ns('1.1', upto=3)            # dừng trước khối học lại trên train + validation
    yv = ns['y_valid'].to_numpy()
    pl = ns['models']['linear'].predict(ns['X_valid'])
    pm = ns['models']['mean'].predict(ns['X_valid'])
    s = Fig(640, 236)
    X = lambda i: 70 + i * 28
    Y = lambda v: 204 - v * 2.8
    for v in range(0, 61, 20):
        s.line(56, Y(v), 616, Y(v), SOFT_LINE, .8)
        s.label(46, Y(v), str(v), 11.5, 'end', FAINT)
    s.line(X(-0.4), Y(pm[0]), X(19.4), Y(pm[0]), SAND, 1.8, dash='6 4')
    for i in range(len(yv)):
        s.circle(X(i), Y(yv[i]), 4.5, TEXT)
        s.circle(X(i), Y(pl[i]), 5, GREEN, 'none', 1.6)
    mae_m = float(np.abs(pm - yv).mean()); mae_l = float(np.abs(pl - yv).mean())
    lx = 70
    s.circle(lx, 14, 4.5, TEXT); s.label(lx + 10, 14, 'số người thật', 12.5, 'start', MUTED)
    s.circle(lx + 130, 14, 5, GREEN, 'none', 1.6); s.label(lx + 140, 14, f'linear · MAE {mae_l:.1f}', 12.5, 'start', GREEN, 600)
    s.line(lx + 300, 14, lx + 322, 14, SAND, 1.8, dash='6 4'); s.label(lx + 330, 14, f'đoán hằng số · MAE {mae_m:.1f}', 12.5, 'start', SAND, 600)
    s.label(340, 226, '20 buổi validation', 12, color=FAINT)
    s.save('1-1-baseline', 'Trên 20 buổi validation: đường hằng số lệch xa, linear bám sát số người thật.')


# ───────────────────────────── 1.2 ─────────────────────────────

def fits12():
    import numpy as np
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.metrics import mean_squared_error
    ns = lesson_ns('1.2', upto=1)
    Xt, yt, Xv, yv = ns['X_train'], ns['y_train'], ns['X_valid'], ns['y_valid']
    grid = np.linspace(0, 1, 400)
    s = Fig(640, 212)
    for k_, (k, col) in enumerate([(1, CLAY), (10, BLUE), (80, SAND)]):
        ax = s.axes(24 + k_ * 208, 34, 184, 130, (0, 1), (-1.6, 1.6), frame=False, grid=False)
        ax.line(grid, np.sin(2 * np.pi * grid), FAINT, 1.2, dash='4 3')
        ax.dots(Xt[:, 0], yt, FAINT, 2.4, opacity=.9)
        m = KNeighborsRegressor(n_neighbors=k).fit(Xt, yt)
        ax.line(grid, m.predict(grid[:, None]), col, 1.6)
        mse = mean_squared_error(yv, m.predict(Xv))
        s.label(24 + k_ * 208 + 92, 16, f'k = {k}', 14, color=TEXT, weight=600)
        s.label(24 + k_ * 208 + 92, 186, f'valid MSE {mse:.3f}', 12.5, color=col, weight=600)
    s.save('1-2-fits', 'k = 1 bám nhiễu, k = 80 san phẳng, k = 10 vừa đủ.')


def learning12():
    ns = lesson_ns('1.2', upto=2)
    sizes = ns['sizes']; tr = -ns['train_scores'].mean(axis=1); va = -ns['valid_scores'].mean(axis=1)
    s = Fig(640, 210)
    ax = s.axes(70, 30, 500, 140, (0, 320), (0, .25), xticks=[20, 60, 140, 300], yticks=[0, .05, .1, .15, .2, .25],
                yfmt='{:.2f}', xlabel='số mẫu train')
    ax.hline(.0625, FAINT, 1.2, '4 3')
    s.label(ax.X(320) + 6, ax.Y(.0625), 'nhiễu', 11.5, 'start', FAINT)
    for ys, col in [(tr, BLUE), (va, CLAY)]:
        ax.line(sizes, ys, col, 2)
        for a, b in zip(sizes, ys):
            s.circle(ax.X(a), ax.Y(b), 3.5, col)
    for k, (lab, col) in enumerate([('train', BLUE), ('validation', CLAY)]):
        x = 430 + k * 70
        s.circle(x, 14, 4, col)
        s.label(x + 9, 14, lab, 12.5, 'start', col, 600)
    s.save('1-2-learning', 'Thêm mẫu, hai đường lỗi gần nhau và sát mức nhiễu.')


def variance12():
    import numpy as np
    from sklearn.neighbors import KNeighborsRegressor
    rng = np.random.default_rng(5)
    grid = np.linspace(0, 1, 300)
    s = Fig(640, 196)
    for k_, (k, col) in enumerate([(1, CLAY), (80, SAND)]):
        ax = s.axes(40 + k_ * 310, 30, 260, 130, (0, 1), (-1.6, 1.6), frame=False, grid=False)
        ax.line(grid, np.sin(2 * np.pi * grid), FAINT, 1.2, dash='4 3')
        for _ in range(5):
            X = rng.uniform(0, 1, (80, 1)); y = np.sin(2 * np.pi * X[:, 0]) + rng.normal(0, .25, 80)
            ax.line(grid, KNeighborsRegressor(n_neighbors=k).fit(X, y).predict(grid[:, None]), col, 1.1)
        s.label(40 + k_ * 310 + 130, 14, f'k = {k}', 14, color=TEXT, weight=600)
        s.label(40 + k_ * 310 + 130, 182, ['variance cao: mỗi bộ train một đường', 'bias cao: sai giống nhau mọi lần'][k_], 12.5, color=col)
    s.line(320, 20, 320, 186, SOFT_LINE, 1)
    s.save('1-2-variance', 'Năm bộ train: k = 1 đổi theo từng bộ, k = 80 lần nào cũng sai như nhau.')


# ───────────────────────────── 1.3 ─────────────────────────────

def groups13():
    import numpy as np
    from sklearn.model_selection import train_test_split, GroupKFold
    groups = np.repeat(np.arange(6), 3)
    all_ids = np.arange(18)
    tr, va = train_test_split(all_ids, test_size=1 / 3, random_state=13)       # đúng như code bài
    rand = np.zeros(18, bool); rand[va] = True
    gtr, gva = next(GroupKFold(n_splits=3).split(np.zeros((18, 1)), np.repeat([0, 1, 0, 1, 0, 1], 3), groups))
    grp = np.zeros(18, bool); grp[gva] = True
    s = Fig(640, 244)
    cw, ch, g = 30, 26, 4
    for k_, (title, mask, x0) in enumerate([('Random split', rand, 110), ('Group split', grp, 430)]):
        s.label(x0 + 48, 14, title, 14, color=TEXT, weight=600)
        for person in range(6):
            y = 34 + person * (ch + g)
            if k_ == 0:
                s.label(x0 - 40, y + ch / 2, f'người {person}', 12, 'end', MUTED)
            vals = mask[person * 3:person * 3 + 3]
            mixed = vals.any() and not vals.all()
            for j, v in enumerate(vals):
                col = CLAY if v else BLUE
                s.box(x0 + j * (cw + g), y, cw, ch, 'none', col, r=4, width=0, opacity=.75 if v else .3)
            if mixed:
                s.label(x0 + 3 * (cw + g) + 6, y + ch / 2, 'trùng', 11.5, 'start', CLAY, 600)
    for k, (lab, col, op) in enumerate([('train', BLUE, .3), ('validation', CLAY, .75)]):
        x = 250 + k * 90
        s.box(x, 224, 14, 12, 'none', col, r=3, width=0, opacity=op)
        s.label(x + 20, 230, lab, 12.5, 'start', MUTED)
    s.line(330, 30, 330, 210, SOFT_LINE, 1)
    s.save('1-3-groups', 'Chia ngẫu nhiên: năm người có mặt ở cả hai phía. Group split: mỗi người một phía.')


def time13():
    import numpy as np
    from sklearn.model_selection import TimeSeriesSplit
    weeks = np.arange(12)
    s = Fig(640, 178)
    cw, g, x0 = 38, 4, 110
    for f, (tr, va) in enumerate(TimeSeriesSplit(n_splits=3, test_size=2, gap=1).split(weeks)):
        y = 22 + f * 40
        s.label(x0 - 14, y + 14, f'Fold {f + 1}', 12.5, 'end', MUTED)
        for w in weeks:
            x = x0 + w * (cw + g)
            if w in tr:
                s.box(x, y, cw, 28, 'none', BLUE, r=4, width=0, opacity=.3)
            elif w in va:
                s.box(x, y, cw, 28, 'none', CLAY, r=4, width=0, opacity=.75)
            elif w == va.min() - 1:
                s.box(x + .5, y + .5, cw - 1, 27, FAINT, 'none', r=4, width=1, dash='3 3')
                s.label(x + cw / 2, y + 14, 'gap', 11, color=FAINT)
    for w in weeks:
        s.label(x0 + w * (cw + g) + cw / 2, 152, str(w), 11, color=FAINT)
    s.label(x0 + 12 * (cw + g) - 4, 168, 'tuần', 11.5, 'end', FAINT)
    s.save('1-3-time', 'Train luôn đứng trước; bỏ một tuần sát ranh giới rồi chấm hai tuần sau.')


def window13():
    s = Fig(640, 124)
    cw, g, x0 = 38, 4, 64
    for w in range(13):
        x = x0 + w * (cw + g)
        s.box(x, 70, cw, 26, 'none', BLUE if w < 8 else CLAY, r=4, width=0, opacity=.3 if w < 8 else .6)
        s.label(x + cw / 2, 108, str(w), 11, color=FAINT)
    s.label(x0 + 4 * (cw + g), 60, 'train', 12.5, color=BLUE, weight=600)
    s.label(x0 + 10.5 * (cw + g), 60, 'validation', 12.5, color=CLAY, weight=600)
    xr = x0 + 6 * (cw + g)
    s.circle(xr + cw / 2, 30, 5, BLUE)
    s.label(xr + cw / 2 - 10, 30, 'hàng tuần 6', 12, 'end', BLUE)
    a, b = x0 + 7 * (cw + g), x0 + 10 * (cw + g) - g
    s.path(f'M {a},{30} L {b},{30}', CLAY, 2)
    s.path(f'M {a},{24} L {a},{36} M {b},{24} L {b},{36}', CLAY, 2)
    s.label(b + 8, 30, 'nhãn: tổng tuần 7–9', 12, 'start', CLAY, 600)
    s.path(f'M {x0 + 8 * (cw + g) - g / 2},{48} L {x0 + 8 * (cw + g) - g / 2},{100}', TEXT, 1.2, dash='4 3')
    s.save('1-3-window', 'Nhãn là tổng ba tuần sau, nên hàng train sát ranh giới đã nhìn vào validation.')


def oof13():
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.model_selection import StratifiedKFold
    X, y = make_classification(n_samples=96, n_features=4, n_informative=3, n_redundant=0, random_state=13)
    fold_of = np.zeros(96, int)
    for f, (_, va) in enumerate(StratifiedKFold(n_splits=3, shuffle=True, random_state=13).split(X, y)):
        fold_of[va] = f
    cols = [BLUE, GREEN, SAND]
    n = 24
    s = Fig(640, 196)
    cw, g, x0 = 19, 3, 88
    for f in range(3):
        y0 = 22 + f * 30
        s.label(x0 - 12, y0 + 11, f'Fold {f + 1}', 12, 'end', MUTED)
        for i in range(n):
            on = fold_of[i] == f
            s.box(x0 + i * (cw + g), y0, cw, 22, 'none', cols[f] if on else LINE, r=3, width=0, opacity=.8 if on else .25)
    y0 = 132
    s.label(x0 - 12, y0 + 11, 'OOF', 12, 'end', TEXT, 600)
    for i in range(n):
        s.box(x0 + i * (cw + g), y0, cw, 22, 'none', cols[fold_of[i]], r=3, width=0, opacity=.8)
    for i in (0, 23):
        s.label(x0 + i * (cw + g) + cw / 2, y0 + 36, str(i), 11, color=FAINT)
    s.save('1-3-oof-mapping', 'Mỗi fold chấm một phần; OOF ghép về đúng vị trí, mỗi mẫu một lần.')


# ───────────────────────────── 1.4 ─────────────────────────────

def scale_line(s, y, title, mu, sd, pts, col, note=None):
    """Một trục số đăng ký với các điểm và giá trị z tương ứng."""
    X = lambda v: 210 + (v - 5) * 13
    s.label(24, y - 8, title, 13, 'start', col, 600)
    s.line(X(5), y, X(35), y, LINE, 1.2)
    for v in (10, 20, 30):
        s.line(X(v), y - 4, X(v), y + 4, LINE, 1)
    for v, c, filled in pts:
        s.circle(X(v), y, 6, c, None if filled else PAPER, 2)
        z = (v - mu) / sd
        s.mono(X(v), y - 20, f'{z:g}', 13, 'middle', c, 600)
        s.label(X(v), y + 18, str(v), 11.5, color=FAINT)
    if note:
        s.label(24, y + 12, note, 11.5, 'start', MUTED)


def pipeline14():
    s = Fig(640, 170)
    scale_line(s, 54, 'Dùng scaler train', 15, 5, [(10, BLUE, True), (20, BLUE, True), (30, CLAY, False)], GREEN, 'μ = 15, σ = 5')
    scale_line(s, 132, 'Fit riêng valid', 30, 1, [(30, CLAY, False)], CLAY, 'chỉ có một giá trị')
    s.save('1-4-pipeline', 'Validation phải dùng μ, σ học từ train; fit riêng biến buổi đông nhất thành 0.')


def leakage14():
    s = Fig(640, 182)
    for k_, (title, leak, x0) in enumerate([('Fit trên toàn bảng', True, 30), ('Fit trong Pipeline', False, 350)]):
        col = CLAY if leak else GREEN
        s.label(x0 + 130, 16, title, 14, color=col, weight=600)
        s.box(x0, 46, 110, 34, 'none', BLUE, r=6, width=0, opacity=.25)
        s.label(x0 + 55, 63, 'train', 13, color=BLUE, weight=600)
        s.box(x0, 108, 110, 34, 'none', CLAY, r=6, width=0, opacity=.3)
        s.label(x0 + 55, 125, 'validation', 13, color=CLAY, weight=600)
        s.box(x0 + 170, 76, 90, 38, LINE, 'none', r=8, width=1.3)
        s.mono(x0 + 215, 95, 'fit', 13, 'middle')
        s.arrow(x0 + 112, 63, x0 + 166, 88, BLUE, 1.4)
        if leak:
            s.arrow(x0 + 112, 125, x0 + 166, 102, CLAY, 1.6)
            s.label(x0 + 140, 160, 'median, μ, σ đã thấy validation', 12.5, color=CLAY)
        else:
            s.arrow(x0 + 172, 108, x0 + 114, 124, FAINT, 1.2, dash='4 3')
            s.label(x0 + 200, 132, 'transform', 11.5, 'start', FAINT)
            s.label(x0 + 140, 160, 'validation chỉ được transform', 12.5, color=GREEN)
    s.line(320, 30, 320, 170, SOFT_LINE, 1)
    s.save('1-4-leakage', 'Fit trên toàn bảng để validation lọt vào tiền xử lý; Pipeline chỉ fit trên train.')


def columns14():
    s = Fig(640, 196)
    cols = [('registered', BLUE), ('rain', BLUE), ('slot', SAND)]
    for k, (c, col) in enumerate(cols):
        y = 40 + k * 46 + (8 if k == 2 else 0)
        s.box(20, y - 15, 104, 30, 'none', col, r=6, width=0, opacity=.22)
        s.mono(72, y, c, 12.5, 'middle', TEXT)
    steps = [(54, ['impute median', 'scale'], BLUE, ['z_registered', 'z_rain']), (146, ['impute mode', 'one-hot'], SAND, ['slot_chieu', 'slot_sang'])]
    for y, st, col, outs in steps:
        x = 160
        for k, name in enumerate(st):
            s.box(x, y - 17, 118, 34, col, 'none', r=8, width=1.2)
            s.mono(x + 59, y, name, 12, 'middle')
            if k == 0:
                s.arrow(x + 120, y, x + 136, y, FAINT, 1.1)
            x += 138
        for j, o in enumerate(outs):
            s.box(462, y - 26 + j * 28, 112, 24, 'none', col, r=5, width=0, opacity=.22)
            s.mono(518, y - 14 + j * 28, o, 11.5, 'middle')
    s.path('M 126,40 L 142,40 L 142,86 L 126,86 M 142,63 L 156,54', BLUE, 1.2)
    s.arrow(126, 140, 156, 146, SAND, 1.2)
    s.arrow(440, 54, 458, 54, FAINT, 1.1)
    s.arrow(440, 146, 458, 146, FAINT, 1.1)
    s.label(518, 186, '4 cột → LinearRegression', 12.5, color=MUTED)
    s.save('1-4-columns', 'Cột số và cột chữ đi hai nhánh riêng rồi ghép thành 4 cột.')


def onehot14():
    s = Fig(640, 168)
    s.label(150, 16, 'Mã số 0, 1, 2', 14, color=CLAY, weight=600)
    X = lambda v: 60 + v * 90
    s.line(X(-0.2), 84, X(2.2), 84, LINE, 1.2)
    for v, name in enumerate(['sáng', 'chiều', 'tối']):
        s.circle(X(v), 84, 6, CLAY)
        s.label(X(v), 108, name, 13, color=TEXT)
        s.mono(X(v), 62, str(v), 13, 'middle', MUTED)
    s.label(150, 144, 'tối bị ép = 2 × chiều', 12.5, color=CLAY)
    s.label(480, 16, 'One-hot', 14, color=GREEN, weight=600)
    rows = [('sáng', '1 0 0'), ('chiều', '0 1 0'), ('tối', '0 0 1')]
    for k, (name, v) in enumerate(rows):
        y = 52 + k * 34
        s.label(420, y, name, 13, 'end', TEXT)
        s.tiles(436, y - 13, [v.split()], 30, 26, GREEN, 3, {(0, j): (GREEN, .45) for j, c in enumerate(v.split()) if c == '1'}, 13, opacity=.12)
    s.label(480, 158, 'mỗi buổi một hệ số riêng', 12.5, color=GREEN)
    s.line(320, 30, 320, 156, SOFT_LINE, 1)
    s.save('1-4-onehot', 'Mã số áp một thứ tự cách đều; one-hot cho mỗi danh mục một cột riêng.')


# ───────────────────────────── 1.5 ─────────────────────────────

Y15 = [1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
P15 = [0.95, 0.80, 0.70, 0.65, 0.60, 0.55, 0.40, 0.30, 0.20, 0.10]


def confusion15():
    s = Fig(640, 200)
    x0, y0, cw, ch = 190, 40, 120, 64
    s.label(x0 + cw / 2, 22, 'đoán 0', 13, color=MUTED)
    s.label(x0 + cw * 1.5 + 6, 22, 'đoán 1', 13, color=MUTED)
    s.label(x0 - 14, y0 + ch / 2, 'thật 0', 13, 'end', MUTED)
    s.label(x0 - 14, y0 + ch * 1.5 + 6, 'thật 1', 13, 'end', MUTED)
    cells = [((0, 0), 'TN', 3, BLUE), ((0, 1), 'FP', 3, CLAY), ((1, 0), 'FN', 1, CLAY), ((1, 1), 'TP', 3, BLUE)]
    for (i, j), name, v, col in cells:
        x, y = x0 + j * (cw + 6), y0 + i * (ch + 6)
        s.box(x, y, cw, ch, 'none', col, r=8, width=0, opacity=.22)
        s.label(x + cw / 2, y + ch / 2 - 10, name, 13, color=col, weight=600)
        s.mono(x + cw / 2, y + ch / 2 + 12, str(v), 18, 'middle', TEXT, 600)
    s.label(x0 + 2 * cw + 20, y0 + ch / 2, 'báo nhầm', 12.5, 'start', CLAY)
    s.label(x0 + cw / 2, y0 + 2 * ch + 24, 'bỏ sót', 12.5, color=CLAY)
    s.save('1-5-confusion', 'Mười buổi validation ở ngưỡng 0.5: hàng là nhãn thật, cột là dự đoán.')


def scores15():
    s = Fig(640, 156)
    X = lambda v: 40 + v * 560
    y = 70
    s.line(X(0), y, X(1), y, LINE, 1.2)
    for v in (0, .5, 1):
        s.label(X(v), y + 30, f'{v:g}', 11.5, color=FAINT)
    s.box(X(.5), y - 34, X(1) - X(.5), 56, 'none', CLAY, r=0, width=0, opacity=.06)
    s.line(X(.5), y - 40, X(.5), y + 22, TEXT, 1.4, dash='5 4')
    s.label(X(.5) + 6, y - 46, 't = 0.5', 12, 'start', TEXT, 600)
    s.label(X(.75), 128, 'báo cần', 12.5, color=CLAY)
    s.label(X(.25), 128, 'báo chưa cần', 12.5, color=BLUE)
    for yy, pp in zip(Y15, P15):
        name = ('TP' if pp >= .5 else 'FN') if yy else ('FP' if pp >= .5 else 'TN')
        col = CLAY if name in ('FP', 'FN') else BLUE
        s.circle(X(pp), y, 7, TEXT, None if yy else PAPER, 2)
        s.label(X(pp), y - 18, name, 11, color=col, weight=600)
    s.circle(470, 146, 5, TEXT)
    s.label(480, 146, 'dương thật', 11.5, 'start', MUTED)
    s.circle(560, 146, 5, TEXT, PAPER, 2)
    s.label(570, 146, 'âm', 11.5, 'start', MUTED)
    s.save('1-5-scores', 'Ngưỡng 0.5 chia mười score thành bốn ô của confusion matrix.')


def threshold15():
    import numpy as np
    y, p = np.array(Y15), np.array(P15)
    ts = [0.3, 0.5, 0.7, 0.9]
    rows = []
    for t_ in ts:
        pr = p >= t_
        tp = (pr & (y == 1)).sum(); fp = (pr & (y == 0)).sum(); fn = (~pr & (y == 1)).sum()
        P = tp / (tp + fp) if tp + fp else 0
        R = tp / (tp + fn)
        F = 2 * tp / (2 * tp + fp + fn)
        rows.append((P, R, F))
    s = Fig(640, 210)
    ax = s.axes(70, 30, 440, 140, (.25, .95), (0, 1), xticks=ts, yticks=[0, .5, 1], xlabel='threshold')
    for k, (name, col) in enumerate([('precision', BLUE), ('recall', SAND), ('F1', CLAY)]):
        ys = [r[k] for r in rows]
        ax.line(ts, ys, col, 2)
        for a, b in zip(ts, ys):
            s.circle(ax.X(a), ax.Y(b), 3.5, col)
        s.label(ax.X(.9) + 10, ax.Y(ys[-1]) + (12 if name == 'precision' else 0), name, 12.5, 'start', col, 600)
    s.line(ax.X(.5), ax.Y(0), ax.X(.5), ax.Y(1), FAINT, 1, dash='3 3')
    s.label(ax.X(.5), 18, 'F1 cao nhất', 11.5, color=CLAY)
    s.save('1-5-threshold', 'Tăng ngưỡng: precision lên, recall xuống; F1 cao nhất ở 0.5.')


def roc15():
    from sklearn.metrics import roc_curve
    fpr, tpr, _ = roc_curve(Y15, P15)
    s = Fig(640, 260)
    ax = s.axes(170, 20, 200, 200, (0, 1), (0, 1), xticks=[0, .5, 1], yticks=[0, .5, 1], xlabel='FPR', ylabel='TPR')
    ax.line([0, 1], [0, 1], FAINT, 1.2, dash='4 3')
    pts = 'M ' + ' L '.join(f'{ax.X(a):.1f},{ax.Y(b):.1f}' for a, b in zip(fpr, tpr)) + f' L {ax.X(1)},{ax.Y(0)} L {ax.X(0)},{ax.Y(0)} Z'
    s.path(pts, 'none', 0, BLUE, opacity=.15)
    ax.line(fpr, tpr, BLUE, 2)
    for a, b in zip(fpr, tpr):
        s.circle(ax.X(a), ax.Y(b), 3, BLUE)
    s.label(ax.X(.62), ax.Y(.28), 'AUC 0.625', 14, color=BLUE, weight=600)
    s.mono(420, 70, '15 cặp xếp đúng', 13, 'start', BLUE)
    s.mono(420, 92, '÷ 24 cặp (dương, âm)', 13, 'start', MUTED)
    s.mono(420, 114, '= 0.625', 13, 'start', BLUE, 600)
    s.save('1-5-roc', 'Diện tích dưới ROC bằng tỉ lệ cặp dương–âm được xếp đúng thứ tự.')


def imbalance15():
    s = Fig(640, 150)
    cell, g = 14, 3
    x0, y0 = 40, 24
    pos = {13, 47, 88}
    for k in range(100):
        i, j = divmod(k, 20)
        col = CLAY if k in pos else BLUE
        s.box(x0 + j * (cell + g), y0 + i * (cell + g), cell, cell, 'none', col, r=3, width=0, opacity=.85 if k in pos else .22)
    s.label(x0 + 10 * (cell + g), y0 + 5 * (cell + g) + 18, '100 buổi, 3 buổi cần hỗ trợ', 12.5, color=MUTED)
    X = 420
    s.label(X, 30, 'luôn đoán “không cần”', 13, 'start', TEXT, 600)
    for k, (name, v, col) in enumerate([('accuracy', '0.97', GREEN), ('recall', '0', CLAY), ('F1', '0', CLAY)]):
        s.label(X, 64 + k * 30, name, 13, 'start', MUTED)
        s.mono(X + 110, 64 + k * 30, v, 15, 'start', col, 600)
    s.save('1-5-imbalance', 'Đoán toàn lớp đông: accuracy 0.97 mà bỏ sót cả ba buổi cần hỗ trợ.')


def logloss15():
    import numpy as np
    s = Fig(640, 210)
    ax = s.axes(80, 30, 420, 140, (0, 1), (0, 5), xticks=[0, .5, 1], yticks=[0, 1, 2, 3, 4, 5], xlabel='p cho nhãn đúng')
    ps = np.linspace(.008, 1, 200)
    ax.line(ps, -np.log(ps), CLAY, 2)
    for pv, lab in [(.01, '4.605'), (.4, '0.916')]:
        s.circle(ax.X(pv), ax.Y(-np.log(pv)), 5, CLAY, PAPER, 2)
        s.mono(ax.X(pv) + 12, ax.Y(-np.log(pv)) - (16 if pv > .1 else 0), f'p = {pv:g} → {lab}', 12.5, 'start', TEXT)
    s.label(80, 12, 'loss = −log p', 12.5, 'start', MUTED)
    s.save('1-5-logloss', 'Sai càng tự tin càng bị phạt nặng: p = 0.01 mất 4.6, p = 0.4 chỉ mất 0.9.')


# ───────────────────────────── 1.6 ─────────────────────────────

def losses16():
    import numpy as np
    s = Fig(640, 210)
    ax = s.axes(90, 20, 400, 150, (-4.4, 4.4), (0, 18), xticks=[-4, -2, 0, 2, 4], yticks=[0, 4, 8, 12, 16], xlabel='phần dư r')
    r = np.linspace(-4, 4, 200)
    ax.line(r, r ** 2, CLAY, 2)
    ax.line(r, np.abs(r), BLUE, 2)
    for x in (1, 4):
        s.circle(ax.X(x), ax.Y(x * x), 4, CLAY)
        s.circle(ax.X(x), ax.Y(x), 4, BLUE)
    s.mono(ax.X(4.4) + 8, ax.Y(16), 'r² = 16', 12.5, 'start', CLAY, 600)
    s.mono(ax.X(4.4) + 8, ax.Y(4), '|r| = 4', 12.5, 'start', BLUE, 600)
    s.save('1-6-losses', 'Lỗi 4 góp 16 vào MSE nhưng chỉ 4 vào MAE.')


def r2_16():
    s = Fig(640, 236)
    y = [10, 20, 30]
    k = 8
    base = 140
    for k_, (title, ref, col, total) in enumerate([('model', [12, 18, 27], CLAY, '4 + 4 + 9 = 17'), ('đoán trung bình 20', [20, 20, 20], SAND, '100 + 0 + 100 = 200')]):
        x0 = 40 + k_ * 300
        s.label(x0, 16, title, 13, 'start', TEXT, 600)
        x = x0
        for yi, ri in zip(y, ref):
            d = abs(yi - ri)
            side = d * k
            if side:
                s.box(x, base - side, side, side, 'none', col, r=3, width=0, opacity=.45)
            s.mono(x + max(side, 12) / 2, base + 14, str(d * d), 12, 'middle', col)
            x += max(side, 12) + 16
        s.mono(x0, base + 40, total, 12.5, 'start', col, 600)
    s.mono(320, 222, 'R² = 1 − 17 / 200 = 0.915', 13.5, 'middle', TEXT, 600)
    s.save('1-6-r2', 'Mỗi ô vuông là một lỗi bình phương: tổng 17 của model so với 200 của mốc trung bình.')


def relative16():
    s = Fig(640, 170)
    rows = [(1, 2, 100), (10, 11, 10), (100, 101, 1)]
    for k, (t_, p_, pct) in enumerate(rows):
        y = 34 + k * 46
        s.mono(30, y, f'thật {t_:>3}, đoán {p_:>3}', 12.5, 'start', MUTED)
        w = 300 * pct / 100
        s.box(220, y - 12, max(w, 3), 24, 'none', CLAY, r=4, width=0, opacity=.75)
        s.label(220 + max(w, 3) + 8, y, f'{pct}%', 13, 'start', CLAY, 600)
    s.label(30, 156, 'cùng sai 1 đơn vị', 12.5, 'start', FAINT)
    s.save('1-6-relative', 'Cùng lỗi tuyệt đối 1, lỗi tương đối phụ thuộc độ lớn target.')


def center16():
    s = Fig(640, 150)
    X = lambda v: 60 + v * 10
    y = 90
    s.line(X(0), y, X(54), y, LINE, 1.2)
    for v in (0, 10, 20, 30, 40, 50):
        s.label(X(v), y + 20, str(v), 11.5, color=FAINT)
    for k in range(3):
        s.circle(X(10), y - 9 - k * 11, 4.5, TEXT)
    s.circle(X(50), y - 9, 4.5, TEXT)
    s.line(X(10), y - 38, X(10), y - 56, GREEN, 1.8)
    s.label(X(10) - 6, y - 64, 'median 10 · tối ưu MAE', 12.5, 'start', GREEN, 600)
    s.line(X(20), y - 2, X(20), y - 34, CLAY, 1.8, dash='5 3')
    s.label(X(20) + 6, y - 34, 'mean 20 · tối ưu MSE', 12.5, 'start', CLAY, 600)
    s.save('1-6-center', 'Target 10, 10, 10, 50: mean bị điểm 50 kéo lên, median thì không.')


def ranking16():
    s = Fig(640, 170)
    rel = {'A', 'C', 'E'}
    for k, (lst, ap) in enumerate([(['A', 'B', 'C'], '5/9'), (['C', 'E', 'B'], '2/3')]):
        y = 34 + k * 72
        hits = 0
        for i, it in enumerate(lst):
            ok = it in rel
            hits += ok
            x = 60 + i * 64
            s.box(x, y, 50, 40, 'none', GREEN if ok else LINE, r=8, width=0, opacity=.3 if ok else .2)
            s.label(x + 25, y + 20, it, 15, color=TEXT, weight=600)
            if ok:
                s.mono(x + 25, y - 10, f'{hits}/{i + 1}', 11.5, 'middle', GREEN)
        s.mono(270, y + 20, f'AP@3 = {ap}', 14, 'start', TEXT, 600)
    s.label(470, 40, 'relevant: A, C, E', 12.5, 'start', MUTED)
    s.label(470, 62, 'P@3 cả hai = 2/3', 12.5, 'start', MUTED)
    s.save('1-6-ranking', 'Cùng hai bài đúng trong top 3; đặt bài đúng sớm hơn cho AP cao hơn.')


# ───────────────────────────── 1.7 ─────────────────────────────

def gridlog17():
    import pandas as pd
    r = pd.DataFrame(lesson_ns('1.7', upto=2)['grid'].cv_results_)
    s = Fig(640, 220)
    ks = [3, 9, 21]
    ax = s.axes(70, 30, 420, 150, (1, 23), (.55, 1.05), xticks=ks, yticks=[.6, .7, .8, .9, 1], yfmt='{:.1f}', xlabel='k', ylabel='F1')
    for w, col in [('uniform', BLUE), ('distance', CLAY)]:
        sub = r[r.param_knn__weights == w].sort_values('param_knn__n_neighbors')
        tr, cv = sub.mean_train_score.tolist(), sub.mean_test_score.tolist()
        ax.line(ks, tr, col, 1.4, dash='5 4')
        ax.line(ks, cv, col, 2.2)
        for a, b in zip(ks, cv):
            s.circle(ax.X(a), ax.Y(b), 3.5, col)
    best = r.loc[r.mean_test_score.idxmax()]
    s.circle(ax.X(9), ax.Y(best.mean_test_score), 8, CLAY, 'none', 1.6)
    s.label(ax.X(9), ax.Y(.575), f'CV cao nhất {best.mean_test_score:.3f}', 12, color=CLAY, weight=600)
    for k, (lab, col) in enumerate([('uniform', BLUE), ('distance', CLAY)]):
        s.circle(530, 60 + k * 22, 4, col)
        s.label(540, 60 + k * 22, lab, 12.5, 'start', col, 600)
    s.line(522, 112, 542, 112, MUTED, 2)
    s.label(548, 112, 'CV', 12, 'start', MUTED)
    s.line(522, 132, 542, 132, MUTED, 1.4, dash='5 4')
    s.label(548, 132, 'train', 12, 'start', MUTED)
    s.save('1-7-grid-log', 'Nét liền là F1 trên CV, nét đứt là trên train; distance luôn khớp train 1.0.')


def search17():
    import numpy as np
    rng = np.random.default_rng(7)
    s = Fig(640, 236)
    W = 200
    pts_grid = [(i, j) for i in range(3) for j in range(3)]
    pts_rand = rng.uniform(.06, .94, (9, 2))
    for k_, (title, pts, col) in enumerate([('Grid · 9 lượt', [((i + .5) / 3, (j + .5) / 3) for i, j in pts_grid], BLUE),
                                            ('Random · 9 lượt', [tuple(p) for p in pts_rand], CLAY)]):
        x0, y0 = 60 + k_ * 300, 30
        s.label(x0 + W / 2, 14, title, 13.5, color=TEXT, weight=600)
        s.box(x0, y0, W, 150, LINE, 'none', r=6, width=1)
        for a, b in pts:
            s.circle(x0 + a * W, y0 + 150 - b * 150, 4.5, col)
            s.line(x0 + a * W, y0 + 156, x0 + a * W, y0 + 166, col, 1.6)
        s.label(x0 - 10, y0 + 75, 'B', 12.5, 'end', MUTED)
        s.label(x0 + W / 2, y0 + 184, 'A (tham số quan trọng)', 12, color=MUTED)
        n = len({round(a, 3) for a, _ in pts})
        s.label(x0 + W + 8, y0 + 161, f'{n} giá trị A', 12, 'start', col, 600)
    s.save('1-7-search', 'Cùng 9 lượt: grid chỉ thử 3 giá trị của tham số quan trọng, random thử 9.')


def cost17():
    s = Fig(640, 196)
    cfgs = ['k=3 uni', 'k=3 dist', 'k=9 uni', 'k=9 dist', 'k=21 uni', 'k=21 dist']
    for i, c in enumerate(cfgs):
        y = 18 + i * 24
        s.mono(130, y + 9, c, 11.5, 'end', MUTED)
        for f in range(3):
            s.box(140 + f * 34, y, 30, 18, 'none', BLUE, r=3, width=0, opacity=.35)
    for f in range(3):
        s.label(155 + f * 34, 172, f'fold {f + 1}', 10.5, color=FAINT)
    s.box(280, 18 + 3 * 24, 30, 18, 'none', CLAY, r=3, width=0, opacity=.8)
    s.label(318, 18 + 3 * 24 + 9, 'refit trên toàn dev', 12, 'start', CLAY)
    s.mono(470, 70, '6 cấu hình × 3 fold', 13, 'start', TEXT)
    s.mono(470, 94, '+ 1 refit', 13, 'start', CLAY)
    s.mono(470, 118, '= 19 lần fit', 13, 'start', TEXT, 600)
    s.save('1-7-cost', 'Grid của bài: 6 cấu hình × 3 fold, cộng một lần refit, tổng 19 lần fit.')


def nested17():
    s = Fig(640, 210)
    cw, x0 = 44, 150
    for f in range(3):
        y = 22 + f * 56
        s.label(x0 - 12, y + 14, f'ngoài {f + 1}', 12, 'end', MUTED)
        for j in range(9):
            outer_test = f * 3 <= j < f * 3 + 3
            s.box(x0 + j * (cw + 3), y, cw, 28, 'none', CLAY if outer_test else BLUE, r=4, width=0, opacity=.75 if outer_test else .25)
        dev = [j for j in range(9) if not (f * 3 <= j < f * 3 + 3)]
        a, b = x0 + dev[0] * (cw + 3), x0 + dev[-1] * (cw + 3) + cw
        if f == 0:
            s.path(f'M {a},{y + 34} L {a},{y + 40} L {b},{y + 40} L {b},{y + 34}', BLUE, 1.2)
            s.label((a + b) / 2, y + 50, 'vòng trong: CV chọn cấu hình', 11.5, color=BLUE)
    s.label(x0 + 9 * (cw + 3) + 6, 36, 'chấm', 12, 'start', CLAY, 600)
    s.save('1-7-nested', 'Nested CV: phần chấm ở vòng ngoài không tham gia lựa chọn nào.')


FIGS = {'1-7-grid-log': gridlog17, '1-7-search': search17, '1-7-cost': cost17, '1-7-nested': nested17,
        '1-6-losses': losses16, '1-6-r2': r2_16, '1-6-relative': relative16, '1-6-center': center16, '1-6-ranking': ranking16,
        '1-5-confusion': confusion15, '1-5-scores': scores15, '1-5-threshold': threshold15, '1-5-roc': roc15,
        '1-5-imbalance': imbalance15, '1-5-logloss': logloss15,
        '1-1-contract': contract11, '1-1-task-types': tasks11, '1-1-timeline': timeline11, '1-1-mae': mae11, '1-1-baseline': baseline11,
        '1-2-fits': fits12, '1-2-learning': learning12, '1-2-variance': variance12,
        '1-3-groups': groups13, '1-3-time': time13, '1-3-window': window13, '1-3-oof-mapping': oof13,
        '1-4-pipeline': pipeline14, '1-4-leakage': leakage14, '1-4-columns': columns14, '1-4-onehot': onehot14}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
