"""Lượt 8 — hình chương 8 (bản gọn). Số liệu lấy từ code bài (lesson_ns) hoặc tính lại đúng như bài.
Chạy riêng: python -B -X utf8 p8_ch8.py [tên ...]"""
import math, sys
from itertools import product
import numpy as np
from kit import *
from p8_ch1 import lesson_ns
from p8_ch5 import kt_ns


def bars(s, ax, items, w=.6, fmt='{:.2f}', size=11.5):
    """Cột đứng: items = [(nhãn, giá trị, màu)], nhãn dưới trục, số trên đỉnh."""
    for k, (nm, v, col) in enumerate(items):
        s.rect(ax.X(k + (1 - w) / 2), ax.Y(v), ax.X(w) - ax.X(0), ax.Y(0) - ax.Y(v), 'none', col, 3, .5, 0)
        s.mono(ax.X(k + .5), ax.Y(v) - 9, fmt.format(v), size, 'middle', TEXT)
        s.label(ax.X(k + .5), ax.y + ax.h + 16, nm, 11.5, color=TEXT)


# ───────────────────────────── 8.1 ─────────────────────────────

_T81 = {}


def ns81():
    if not _T81:
        _T81['ns'] = lesson_ns('8.1', upto=3)
    return _T81['ns']


def runtime81():
    s = Fig(640, 180)
    parts = [(30, FAINT), (30, SAND), (360, BLUE), (40, CLAY)]
    x0, sc, t = 40, 540 / 480, 0
    for sec, col in parts:
        s.box(x0 + t * sc + 1, 50, sec * sc - 2, 34, 'none', col, r=4, width=0, opacity=.4)
        t += sec
    s.label(x0 + 30 * sc, 104, 'đọc, nạp asset', 11, color=TEXT)
    s.label(x0 + 240 * sc, 67, 'train 6 phút', 11.5, color=TEXT)
    s.label(x0 + 440 * sc, 104, 'predict 40 s', 11, color=CLAY)
    s.label(x0 + 440 * sc, 120, 'phần đội đã đo', 10.5, color=MUTED)
    lim = x0 + 300 * sc
    s.line(lim, 36, lim, 92, CLAY, 1.6, '4 4')
    s.mono(lim, 26, 'giới hạn 5 phút', 11, 'middle', CLAY, 600)
    for m in range(0, 9):
        s.mono(x0 + m * 60 * sc, 150, f'{m}', 10, 'middle', FAINT)
    s.mono(x0 + 480 * sc + 8, 150, 'phút', 10, 'start', FAINT)
    s.save('8-1-runtime', 'Máy chấm chạy lại cả notebook: đọc dữ liệu, nạp asset và train 6 phút đã vượt giới hạn 5 phút trước khi tới predict 40 giây mà đội đã bấm giờ.')


def logloss81():
    s = Fig(640, 220)
    ax = s.axes(100, 30, 420, 140, (0, 3), (0, 4.2), xticks=[], yticks=[0, 1, 2, 3, 4], grid=False)
    bars(s, ax, [('nhãn cứng 0/1', 3.45, CLAY), ('hằng 0.5', math.log(2), BLUE), ('0.9 cho lớp đoán', -(.9 * math.log(.9) + .1 * math.log(.1)), GREEN)], fmt='{:.3f}')
    s.label(ax.x - 8, ax.y - 12, 'log loss, 100 mẫu, đúng 90', 11, 'start', FAINT)
    s.save('8-1-logloss', 'Cùng 90/100 mẫu đúng: nộp nhãn cứng 0/1 bị cắt ở 10⁻¹⁵ nên mỗi mẫu sai tốn 34.5, log loss 3.45, tệ hơn nộp hằng 0.5 (0.693); nộp xác suất 0.9 cho lớp đoán (đúng 90%) tốn 0.325.')


def normalize81():
    s = Fig(640, 210)
    lo, hi, x0, W = .5, .95, 80, 480

    def X(v):
        return x0 + (v - lo) / (hi - lo) * W
    for r, (nm, b, u, raw, col) in enumerate([('A', .58, .90, .70, BLUE), ('B', .60, .90, .75, CLAY)]):
        y = 50 + r * 64
        n = 100 * (raw - b) / (u - b)
        s.label(x0 - 14, y + 11, nm, 13, 'end', TEXT, 600)
        s.box(X(b), y, X(u) - X(b), 22, 'none', col, r=4, width=0, opacity=.18)
        s.box(X(b), y, X(raw) - X(b), 22, 'none', col, r=4, width=0, opacity=.4)
        s.mono(X(b), y + 36, f'{b:.2f} → 0', 10.5, 'middle', MUTED)
        s.mono(X(u), y + 36, f'{u:.2f} → 100', 10.5, 'middle', MUTED)
        s.circle(X(raw), y + 11, 4.5, col, col)
        s.mono(X(raw), y - 10, f'{raw:.2f} → {n:.1f}', 11.5, 'middle', col, 600)
    s.label(320, 192, 'N(s) = 100 (s − b) / (u − b): cùng mức accuracy, khoảng chuẩn hóa khác nhau', 11, color=MUTED)
    s.save('8-1-normalize', 'Hai bài với baseline khác nhau (số từ code bài): accuracy 0.70 ở A thành 37.5 điểm, 0.75 ở B thành 50 điểm; đạt đúng baseline cho 0, đạt mốc u = 0.90 cho 100.')


def plans81():
    ns = ns81()
    plans = [ns['plan_total'](lv) for lv in product(range(3), repeat=3)]
    s = Fig(640, 260)
    ax = s.axes(80, 26, 440, 180, (0, 200), (0, 50), xticks=[0, 50, 100, 130, 150, 200], yticks=[0, 20, 40], grid=False, xlabel='phút')
    budgets = np.arange(0, 201)
    upper = [max(g for m, g in plans if m <= b) for b in budgets]
    ax.step(budgets, upper, BLUE, 1.6)
    ax.dots([m for m, g in plans], [g for m, g in plans], BLUE, 3.2, BLUE, .45)
    s.line(ax.X(130), ax.y, ax.X(130), ax.y + ax.h, SAND, 1, '4 4')
    s.circle(ax.X(130), ax.Y(40), 6, CLAY, CLAY)
    s.circle(ax.X(125), ax.Y(30), 6, TEXT, 'none', 1.5)
    s.mono(ax.X(130) + 12, ax.Y(40) + 10, 'duyệt hết: 40', 11, 'start', CLAY, 600)
    s.mono(ax.X(125) - 12, ax.Y(30) - 4, 'tham lam: 30', 11, 'end', TEXT)
    s.label(ax.x - 8, ax.y - 12, 'điểm dự kiến', 11, 'start', FAINT)
    s.save('8-1-plans', 'Mỗi chấm là một trong 27 kế hoạch (từ code bài); đường bậc thang là điểm tối đa trong từng ngân sách. Ở 130 phút, duyệt hết đạt 40 điểm, tham lam dừng ở 30.')


def priority81():
    s = Fig(640, 210)
    rows = [('sửa schema', .9, 8, 10), ('model mới', .3, 20, 40), ('thêm seed', .7, 2, 20)]
    for k, (nm, p, g, t) in enumerate(rows):
        y = 34 + k * 48
        v = p * g / t
        s.label(130, y + 14, nm, 12, 'end', TEXT, 600 if k == 0 else 400)
        s.box(146, y, 300 * v / .72, 28, 'none', CLAY if k == 0 else BLUE, r=4, width=0, opacity=.4 if k == 0 else .25)
        s.mono(146 + 300 * v / .72 + 8, y + 14.5, f'{v:.2f}', 12, 'start', TEXT, 600)
        s.mono(146 + 300 * v / .72 + 52, y + 14.5, f'= {p} × {g} / {t}', 10.5, 'start', MUTED)
    s.label(146, 186, 'điểm dự kiến mỗi phút V = p·ΔN / t', 11, 'start', FAINT)
    s.save('8-1-priority', 'Xếp ba thí nghiệm theo V = p·ΔN/t (số từ code bài): sửa schema 0.72 điểm dự kiến mỗi phút, model mới 0.15, thêm seed 0.07.')


def xyz81():
    s = Fig(640, 200)
    x0, sc = 110, 12
    rows = [('theo V: X', [('X', 20, CLAY)], '0.5 × 40 = 20'), ('Y rồi Z', [('Y', 15, BLUE), ('Z', 15, BLUE)], '2 × 0.8 × 15 = 24')]
    for r, (nm, segs, val) in enumerate(rows):
        y = 40 + r * 56
        s.label(x0 - 12, y + 15, nm, 12, 'end', TEXT, 600)
        t = 0
        for lab, m, col in segs:
            s.box(x0 + t * sc + 1, y, m * sc - 2, 30, 'none', col, r=4, width=0, opacity=.35)
            s.mono(x0 + (t + m / 2) * sc, y + 15.5, lab, 12, 'middle', TEXT)
            t += m
        if t < 30:
            s.box(x0 + t * sc + 1, y, (30 - t) * sc - 2, 30, FAINT, 'none', r=4, width=1, dash='3 3')
            s.label(x0 + (t + (30 - t) / 2) * sc, y + 15, '10 phút thừa', 10.5, color=FAINT)
        s.mono(x0 + 30 * sc + 14, y + 15.5, val, 12, 'start', CLAY if r == 0 else GREEN, 600)
    for m in (0, 15, 30):
        s.mono(x0 + m * sc, 160, f'{m}', 10, 'middle', FAINT)
    s.mono(x0 + 30 * sc + 14, 160, 'phút', 10, 'start', FAINT)
    s.save('8-1-xyz', 'Ngân sách 30 phút: chọn X vì V cao nhất còn thừa 10 phút không đủ cho việc nào, được 20 điểm dự kiến; làm Y rồi Z dùng đủ 30 phút, được 24.')


def noise81():
    rng = np.random.default_rng(0)
    a = np.r_[np.ones(1540), np.ones(60), np.zeros(80), np.zeros(320)]
    b = np.r_[np.ones(1540), np.zeros(60), np.ones(80), np.zeros(320)]
    G = {}
    for n in (200, 1000):
        g = []
        for _ in range(5000):
            rows = rng.choice(2000, size=n, replace=False)
            g.append(b[rows].mean() - a[rows].mean())
        G[n] = np.array(g)
    assert round(float(np.mean(G[200] <= 0)), 2) == .33 and round(float(np.mean(G[1000] <= 0)), 2) == .05
    s = Fig(640, 250)
    for k, n in enumerate((200, 1000)):
        ax = s.axes(60 + k * 300, 30, 240, 150, (-.06, .08), (0, .3 if k == 0 else .3), xticks=[-.04, 0, .04, .08], yticks=[], grid=False)
        edges = np.arange(-.06, .0801, .005 if n == 200 else .002)
        h, _ = np.histogram(G[n], edges)
        h = h / h.sum() * (.005 / (edges[1] - edges[0]))
        for i in range(len(h)):
            x0, x1 = edges[i], edges[i + 1]
            col = CLAY if x1 <= 1e-9 else BLUE
            s.rect(ax.X(x0) + .3, ax.Y(min(h[i], .3)), ax.X(x1) - ax.X(x0) - .6, ax.Y(0) - ax.Y(min(h[i], .3)), 'none', col, 0, .5, 0)
        s.line(ax.X(0), ax.y, ax.X(0), ax.y + ax.h, TEXT, 1.2)
        s.line(ax.X(.01), ax.y, ax.X(.01), ax.y + ax.h, SAND, 1.2, '4 4')
        s.label(ax.x + 120, 16, f'public {n} dòng', 12, color=TEXT, weight=600)
        s.mono(ax.x + 120, 222, f'A ≥ B: {np.mean(G[n] <= 0):.2f} · std {G[n].std():.3f}', 11, 'middle', CLAY, 600)
    s.save('8-1-noise', 'Chênh accuracy public của B so với A qua 5000 lần rút (từ code bài); vạch đậm là 0, vạch đứt là chênh thật 0.01. Phần cam là những lần public xếp A ngang hoặc hơn B: 33% với 200 dòng, 5% với 1000 dòng.')


FIGS81 = {'8-1-runtime': runtime81, '8-1-logloss': logloss81, '8-1-normalize': normalize81, '8-1-plans': plans81,
          '8-1-priority': priority81, '8-1-xyz': xyz81, '8-1-noise': noise81}

# ───────────────────────────── 8.2 ─────────────────────────────

_T82 = {}


def ns82():
    if not _T82:
        _T82['ns'] = lesson_ns('8.2', upto=4)
    return _T82['ns']


def table82():
    df = ns82()['df']
    cols = ['id', 'document', 'device', 'signal', 'label']
    s = Fig(640, 300)
    xs = [70, 160, 270, 360, 450]
    for c, x in zip(cols, xs):
        s.mono(x, 24, c, 11, 'middle', MUTED)
    dup = df['id'].duplicated(keep=False)
    conflict = df['document'].eq('doc-b')
    for i, row in df.reset_index(drop=True).iterrows():
        y = 36 + i * 30
        if conflict[i]:
            s.box(30, y, 450, 26, 'none', SAND, r=4, width=0, opacity=.22)
        for c, x in zip(cols, xs):
            v = row[c]
            txt = '—' if (isinstance(v, float) and np.isnan(v)) else (f'{v:g}' if isinstance(v, float) else str(v))
            hot = (c == 'id' and dup[i]) or (c == 'signal' and txt == '—')
            if hot:
                s.box(x - 30, y + 2, 60, 22, CLAY, 'none', r=4, width=1.4)
            s.mono(x, y + 13.5, txt, 11.5, 'middle', CLAY if hot else TEXT)
    s.label(500, 259, 'id 003 lặp', 11, 'start', CLAY)
    s.label(500, 140, 'signal thiếu', 11, 'start', CLAY)
    s.label(500, 229, 'doc-b: nhãn 0 và 1', 11, 'start', SAND)
    s.save('8-2-table', 'Bảng tám dòng của bài: id 003 xuất hiện hai lần, một ô signal bị thiếu, và nhóm doc-b (dải vàng) cùng đặc trưng nhưng mang cả nhãn 0 lẫn 1.')


def hash82():
    import hashlib
    a, b = 'Phim hay, diễn viên tốt.', 'phim hay,  diễn viên tốt.'
    norm = lambda t: ' '.join(t.lower().split())
    h = lambda t: hashlib.sha256(t.encode()).hexdigest()[:10]
    s = Fig(640, 200)
    s.label(130, 22, 'băm bytes gốc', 12, color=TEXT, weight=600)
    s.label(470, 22, 'chuẩn hóa rồi băm', 12, color=TEXT, weight=600)
    for r, t in enumerate([a, b]):
        y = 40 + r * 54
        s.box(20, y, 220, 26, 'none', BLUE, r=4, width=0, opacity=.15)
        s.mono(130, y + 13.5, t.replace('  ', '··'), 10.5, 'middle', TEXT)
        s.mono(130, y + 40, h(t), 11, 'middle', CLAY, 600)
        s.box(360, y, 220, 26, 'none', GREEN, r=4, width=0, opacity=.15)
        s.mono(470, y + 13.5, norm(t), 10.5, 'middle', TEXT)
        s.mono(470, y + 40, h(norm(t)), 11, 'middle', GREEN, 600)
        s.arrow(246, y + 13, 354, y + 13, FAINT, 1.1)
    s.label(300, 30, 'lower, gộp khoảng trắng', 10.5, color=MUTED)
    s.label(130, 166, 'hai hash khác nhau', 11, color=CLAY)
    s.label(470, 166, 'cùng một hash', 11, color=GREEN)
    s.save('8-2-hash', 'Hai bài chỉ khác chữ hoa đầu câu và một dấu cách thừa (··): băm bytes gốc cho hai hash khác nhau; hạ chữ thường và gộp khoảng trắng trước khi băm thì ra cùng một hash.')


def groups82():
    ns = ns82()
    g = ns['groups']
    s = Fig(640, 230)
    for k, (nm, tr, va) in enumerate([('chia ngẫu nhiên theo dòng', ns['random_train'], ns['random_val']),
                                      ('chia theo tài liệu', ns['group_train'], ns['group_val'])]):
        y0 = 30 + k * 96
        inval = np.zeros(len(g), bool)
        inval[va] = True
        both = set(g[tr]) & set(g[va])
        s.label(20, y0 - 10, nm, 12, 'start', TEXT, 600)
        for d in range(60):
            x = 20 + d * 9
            for j in range(4):
                r = d * 4 + j
                s.box(x, y0 + j * 11, 7.5, 9.5, 'none', CLAY if inval[r] else BLUE, r=1.5, width=0, opacity=.55 if inval[r] else .2)
        s.mono(620, y0 + 22, f'chung {len(both)}', 11, 'end', CLAY if both else GREEN, 600)
    s.label(320, 220, 'mỗi cột là một tài liệu, bốn ô là bốn đoạn; cam là validation', 11, color=MUTED)
    s.save('8-2-groups', 'Split của bài trên 60 tài liệu × 4 đoạn (từ code): chia ngẫu nhiên theo dòng để 39 tài liệu có đoạn ở cả hai phía; chia theo tài liệu giữ mỗi cột trọn ở một phía.')


def sizes82():
    s = Fig(640, 190)
    rows = [('ít nhất', [5] * 10, 50), ('nhiều nhất', [100] * 4 + [5] * 6, 430)]
    sc = 1.0
    for r, (nm, parts, tot) in enumerate(rows):
        y = 40 + r * 56
        s.label(100, y + 14, nm, 12, 'end', TEXT, 600)
        x = 112
        for p in parts:
            s.box(x, y, p * sc - 1, 28, 'none', CLAY if p == 100 else BLUE, r=2, width=0, opacity=.4 if p == 100 else .3)
            x += p * sc
        s.mono(x + 10, y + 14.5, f'{tot} dòng', 12, 'start', TEXT, 600)
    s.line(112 + 145, 28, 112 + 145, 136, FAINT, 1, '4 4')
    s.mono(112 + 145, 152, '25% số dòng = 145', 10.5, 'middle', FAINT)
    s.label(320, 178, 'cùng 10 tài liệu validation; tài liệu dài 100 đoạn, ngắn 5 đoạn', 11, color=MUTED)
    s.save('8-2-sizes', 'GroupShuffleSplit chọn 10 trong 40 tài liệu: nếu cả 10 là tài liệu ngắn thì validation có 50 dòng; nếu gồm 4 tài liệu dài và 6 ngắn thì có 430 dòng, xa mốc 145 dòng.')


def domains82():
    ns = ns82()
    s = Fig(640, 250)
    rng = np.random.default_rng(5)
    for k, (nm, X, y) in enumerate([('miền nguồn: shortcut trùng nhãn 95%', ns['X_source'], ns['y_source']),
                                    ('miền mới: chỉ 5%', ns['X_shift'], ns['y_shift'])]):
        ax = s.axes(70 + k * 300, 34, 230, 160, (-3, 3), (-1.8, 1.8), xticks=[-2, 0, 2], yticks=[-1, 1] if k == 0 else [],
                    grid=False, xlabel='signal')
        n = min(300, len(y))
        jy = X[:n, 1] + rng.uniform(-.35, .35, n)
        for c, col in ((0, BLUE), (1, CLAY)):
            m = y[:n] == c
            ax.dots(X[:n][m, 0], jy[m], col, 2.2, col, .55)
        s.label(ax.x + 115, 18, nm, 11.5, color=TEXT, weight=600)
    s.label(40, 30, 'shortcut', 10.5, 'start', FAINT)
    s.save('8-2-domains', 'Dữ liệu tự sinh của bài (300 điểm mỗi miền, cam là nhãn 1): signal tách hai lớp như nhau ở cả hai miền; shortcut (±1, rải dọc cho dễ nhìn) trùng nhãn ở miền nguồn nhưng bị đảo ở miền mới.')


def shift82():
    s = Fig(640, 230)
    ax = s.axes(90, 30, 420, 150, (0, 2), (0, 1), xticks=[], yticks=[0, .5, 1], grid=False)
    vals = [('cả hai cột', .970, .383), ('chỉ signal', .830, .863)]
    for k, (nm, a, b) in enumerate(vals):
        for j, (v, col) in enumerate([(a, BLUE), (b, CLAY)]):
            x = k + .18 + j * .33
            s.rect(ax.X(x), ax.Y(v), ax.X(.3) - ax.X(0), ax.Y(0) - ax.Y(v), 'none', col, 3, .5, 0)
            s.mono(ax.X(x + .15), ax.Y(v) - 9, f'{v:.3f}', 11, 'middle', TEXT)
        s.label(ax.X(k + .5), ax.y + ax.h + 16, nm, 12, color=TEXT)
    ax.hline(.5, FAINT, 1, '3 3')
    s.box(530, 60, 12, 12, 'none', BLUE, r=2, width=0, opacity=.5)
    s.label(548, 66, 'trong miền', 11, 'start', TEXT)
    s.box(530, 84, 12, 12, 'none', CLAY, r=2, width=0, opacity=.5)
    s.label(548, 90, 'miền mới', 11, 'start', TEXT)
    s.label(ax.x - 8, ax.y - 12, 'accuracy', 11, 'start', FAINT)
    s.save('8-2-shift', 'Ablation của bài (số từ output): dùng cả shortcut đạt 0.970 trong miền nhưng rơi còn 0.383 khi quan hệ bị đảo; chỉ dùng signal đạt 0.830 và giữ 0.863 ở miền mới.')


def slices82():
    s = Fig(640, 210)
    x0, c, g = 30, 19, 3
    for i in range(100):
        new = i >= 90
        k = i if not new else i - 90
        ok = (k < 81) if not new else (k < 2)
        col_i, row_i = (i % 20, i // 20)
        s.box(x0 + col_i * (c + g), 30 + row_i * (c + g), c, c, 'none', (CLAY if new else BLUE) if ok else FAINT,
              r=3, width=0 if ok else 1, opacity=.5 if ok else .12)
    s.box(x0 + 10 * (c + g) - 3, 30 + 4 * (c + g) - 3, 10 * (c + g) + 3, c + 6, CLAY, 'none', r=5, width=1.4)
    s.mono(490, 60, 'cũ  81/90 = 0.90', 11.5, 'start', BLUE, 600)
    s.mono(490, 86, 'mới  2/10 = 0.20', 11.5, 'start', CLAY, 600)
    s.mono(490, 124, 'chung 0.83', 11.5, 'start', TEXT)
    s.mono(490, 146, 'trung bình', 11, 'start', MUTED)
    s.mono(490, 162, 'hai miền 0.55', 11, 'start', MUTED)
    s.label(250, 186, 'ô đặc là đoán đúng; hàng cuối, khung cam là 10 ảnh camera mới', 11, color=MUTED)
    s.save('8-2-validation-slices', 'Mỗi ô là một mẫu validation, ô đặc là đúng: camera cũ đúng 81/90, camera mới (khung cam) chỉ 2/10; accuracy chung 0.83 che khuất nhóm 0.20.')


def se82():
    s = Fig(640, 190)
    ax = s.axes(130, 30, 400, 110, (0, 1), (0, 2), xticks=[0, .25, .5, .75, 1], yticks=[], grid=False, xlabel='accuracy')
    for r, (nm, p, n, col) in enumerate([('camera cũ, n = 90', .9, 90, BLUE), ('camera mới, n = 10', .2, 10, CLAY)]):
        y = 1.5 - r
        se = math.sqrt(p * (1 - p) / n)
        lo, hi = max(0, p - 2 * se), min(1, p + 2 * se)
        s.line(ax.X(lo), ax.Y(y), ax.X(hi), ax.Y(y), col, 3)
        s.circle(ax.X(p), ax.Y(y), 5, col, col)
        s.label(ax.x - 10, ax.Y(y), nm, 11.5, 'end', TEXT)
        s.mono(ax.X(hi) + 8, ax.Y(y) - 12, f'{p:.2f} ± {2 * se:.2f}', 11, 'start', col, 600)
    s.save('8-2-se', 'Khoảng accuracy ± 2 sai số chuẩn: camera cũ 0.90 ± 0.06 với 90 mẫu, camera mới 0.20 ± 0.25 với 10 mẫu, trải từ gần 0 đến khoảng 0.45.')


FIGS82 = {'8-2-table': table82, '8-2-hash': hash82, '8-2-groups': groups82, '8-2-sizes': sizes82, '8-2-domains': domains82,
          '8-2-shift': shift82, '8-2-validation-slices': slices82, '8-2-se': se82}

# ───────────────────────────── 8.3 ─────────────────────────────

_T83 = {}


def ns83():
    if not _T83:
        _T83['ns'] = lesson_ns('8.3', upto=5)
    return _T83['ns']


VCOL = {-1: BLUE, 0: SAND, 1: CLAY}


def numline(s, y, pos, x0=70, dx=70, labels=None, cols=None, r=13):
    for i in range(7):
        s.line(x0 + i * dx + r + 2, y, x0 + (i + 1) * dx - r - 2, y, SOFT_LINE, 1.2)
    for i in range(8):
        x = x0 + pos[i] * dx
        col = cols[i] if cols else BLUE
        s.circle(x, y, r, col, col, 0, .3)
        s.mono(x, y + .5, str(labels[i] if labels else i), 11.5, 'middle', TEXT)


def partition83():
    ns = ns83()
    v = [int(ns['predicted_verdict'](ns['public'], 0, 6, h)) for h in range(8)]
    s = Fig(640, 170)
    numline(s, 70, list(range(8)), cols=[VCOL[x] for x in v])
    s.line(70 + 3 * 70, 36, 70 + 3 * 70, 54, SAND, 1.2, '4 4')
    s.line(70 + 3 * 70, 86, 70 + 3 * 70, 104, SAND, 1.2, '4 4')
    s.mono(70, 40, 'A', 12, 'middle', BLUE, 600)
    s.mono(70 + 6 * 70, 40, 'B', 12, 'middle', CLAY, 600)
    s.label(70 + 1 * 70, 118, 'A gần hơn: 0, 1, 2', 11, color=BLUE)
    s.label(70 + 3 * 70, 138, 'hòa: 3', 11, color=SAND)
    s.label(70 + 5.5 * 70, 118, 'B gần hơn: 4, 5, 6, 7', 11, color=CLAY)
    s.save('8-3-partition', 'So A tại 0 với B tại 6 trên biểu diễn public (từ code bài): trung điểm 3 cho hòa, ba ứng viên 0, 1, 2 nghiêng về A, bốn ứng viên 4 đến 7 nghiêng về B.')


def split83():
    ns = ns83()
    pv, pub = ns['predicted_verdict'], ns['public']
    s = Fig(640, 230)
    for k, q in enumerate([1, 4, 6, 7]):
        y = 30 + k * 42
        n = {r: sum(int(pv(pub, 0, q, h)) == r for h in range(8)) for r in (-1, 0, 1)}
        e = sum(c * c for c in n.values()) / 8
        s.label(110, y + 13, f'đề xuất {q}', 12, 'end', TEXT, 600 if q == 6 else 400)
        x = 124
        for r in (-1, 0, 1):
            if n[r]:
                s.box(x, y, n[r] * 40 - 2, 26, 'none', VCOL[r], r=3, width=0, opacity=.35)
                s.mono(x + n[r] * 20 - 1, y + 13.5, str(n[r]), 11, 'middle', TEXT)
                x += n[r] * 40
        s.mono(124 + 8 * 40 + 20, y + 13.5, f'E = {e:.2f}', 12, 'start', CLAY if q == 6 else TEXT, 600 if q == 6 else 400)
    s.label(124 + 160, 210, 'ba nhóm phản hồi: A thắng, hòa, B thắng (champion 0)', 11, color=MUTED)
    s.save('8-3-split', 'Champion 0, tám ứng viên đồng xác suất (từ code bài): đề xuất 1 chia thành 1 và 7 nên còn 6.25 ứng viên kỳ vọng; đề xuất 6 chia 3, 1, 4, còn 3.25.')


def turns83():
    ns = ns83()
    t = ns['turns']
    s = Fig(640, 200)
    ax = s.axes(80, 30, 440, 120, (0, 8), (0, 4), xticks=[], yticks=[0, 1, 2, 3], grid=False)
    for h, v in enumerate(t):
        s.rect(ax.X(h + .2), ax.Y(v), ax.X(.6) - ax.X(0), ax.Y(0) - ax.Y(v), 'none', BLUE, 3, .45, 0)
        s.mono(ax.X(h + .5), ax.Y(0) + 14, f'h = {h}', 10.5, 'middle', MUTED)
    ax.hline(np.mean(t), CLAY, 1.2, '4 4')
    s.mono(ax.X(8) + 8, ax.Y(np.mean(t)), f'mean {np.mean(t):.3f}', 11, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'số lượt', 11, 'start', FAINT)
    s.save('8-3-turns', 'Player nhỏ của bài chơi đủ tám hidden khi public trùng judge (từ code): mọi ván đều giải được trong 1 đến 3 lượt, trung bình 2.375.')


def mismatch83():
    s = Fig(640, 210)
    pos_j = [0, 1, 2, 3, 5, 4, 6, 7]
    cols = [BLUE] * 5 + [FAINT] * 3
    s.label(20, 50, 'public', 12, 'start', TEXT, 600)
    numline(s, 50, list(range(8)), x0=110, dx=64, cols=cols)
    s.label(20, 140, 'judge', 12, 'start', TEXT, 600)
    numline(s, 140, pos_j, x0=110, dx=64)
    for i in (4, 5):
        s.line(110 + i * 64, 64, 110 + pos_j[i] * 64, 126, CLAY, 1.2, '3 3')
    s.circle(110 + 6 * 64, 140, 17, CLAY, 'none', 1.6)
    s.circle(110 + 6 * 64, 50, 17, CLAY, 'none', 1.6)
    s.label(110 + 6 * 64, 176, 'hidden 6', 11, color=CLAY)
    s.label(110 + 2 * 64, 86, 'lọc cứng giữ 0–4', 11, color=BLUE)
    s.label(110 + 6.5 * 64, 86, 'bị loại', 11, color=FAINT)
    s.save('8-3-mismatch', 'Judge đổi chỗ 4 và 5 so với public (từ code bài): judge thấy A = 4 gần hidden 6 hơn nên trả “A thắng”; public dự đoán ngược lại, nên lọc cứng chỉ giữ 0 đến 4 và loại mất hidden 6.')


def penalty83():
    ns = ns83()
    pen = ns['penalty']
    s = Fig(640, 190)
    ax = s.axes(80, 30, 440, 100, (0, 8), (0, 1.3), xticks=[], yticks=[0, 1], grid=False)
    for h, v in enumerate(pen):
        col = CLAY if h == 6 else BLUE
        hgt = max(v, .03)
        s.rect(ax.X(h + .2), ax.Y(hgt), ax.X(.6) - ax.X(0), ax.Y(0) - ax.Y(hgt), 'none', col, 3, .5 if h == 6 else .35, 0)
        s.mono(ax.X(h + .5), ax.Y(0) + 14, str(h), 11, 'middle', CLAY if h == 6 else MUTED)
    s.mono(ax.X(6.5), ax.Y(1) - 12, 'hidden', 10.5, 'middle', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'penalty', 11, 'start', FAINT)
    s.label(300, 176, 'hidden bị phạt 1 nhưng vẫn còn trong ranking', 11, color=MUTED)
    s.save('8-3-penalty', 'Ràng buộc mềm sau phản hồi “A thắng” (từ code bài, m = 0): ứng viên 5, 6, 7 bị phạt 1 thay vì bị xóa, nên hidden 6 vẫn có thể được hỏi ở lượt sau.')


def ablation83():
    s = Fig(640, 240)
    rows = [('quét 0..7', 2400, 4.50, FAINT), ('cứng + cân đối', 1440, 4.92, CLAY), ('mềm + cân đối', 2400, 2.84, GREEN), ('mềm + quét', 2400, 4.50, BLUE)]
    s.label(330, 22, 'điểm (ván thua tính 9 lượt), thấp là tốt', 11, color=FAINT)
    s.label(580, 22, 'giải được', 11, color=FAINT)
    for k, (nm, solved, sc, col) in enumerate(rows):
        y = 38 + k * 46
        s.label(140, y + 14, nm, 12, 'end', TEXT, 600 if k == 2 else 400)
        s.box(154, y, sc * 70, 28, 'none', col, r=4, width=0, opacity=.45)
        s.mono(154 + sc * 70 + 8, y + 14.5, f'{sc:.2f}', 12, 'start', TEXT, 600)
        s.mono(610, y + 14.5, f'{solved / 2400:.0%}', 11.5, 'end', CLAY if solved < 2400 else MUTED)
    s.line(154 + 4.5 * 70, 32, 154 + 4.5 * 70, 222, FAINT, 1, '3 3')
    s.save('8-3-ablation', 'Bảng ablation của bài trên 2400 ván (số từ output): lọc cứng với truy vấn cân đối chỉ giải 60% ván và đạt 4.92, tệ hơn quét 4.50; chỉ khi có cả lọc mềm lẫn truy vấn cân đối điểm mới xuống 2.84.')


def field83():
    rng = np.random.default_rng(0)
    grid = np.linspace(-1, 1, 64)
    gx, gy = np.meshgrid(grid, grid)
    pts = np.stack([gx.ravel(), gy.ravel()], axis=1)
    src = np.array([.35, -.2])

    def make(fn):
        off = pts - src
        r = np.linalg.norm(off, axis=1)
        return (fn(r) / r)[:, None] * off + rng.normal(0, .02, off.shape)

    def locate(F):
        sq = (F ** 2).sum(axis=1)
        N = sq[:, None, None] * np.eye(2) - F[:, :, None] * F[:, None, :]
        return np.linalg.solve(N.sum(axis=0), np.einsum('nij,nj->i', N, pts))
    make(lambda r: 1 / (r + .1))
    F = make(lambda r: np.sin(5 * r))
    est = locate(F)
    s = Fig(640, 300)
    ax = s.axes(170, 20, 250, 250, (-1, 1), (-1, 1), xticks=[-1, 0, 1], yticks=[-1, 0, 1], grid=False)
    idx = [i * 64 + j for i in range(3, 64, 6) for j in range(3, 64, 6)]
    for n in idx:
        p, f = pts[n], F[n]
        L = np.linalg.norm(f)
        if L < 1e-6:
            continue
        u = f / L * .1
        col = CLAY if np.dot(f, p - src) > 0 else BLUE
        s.arrow(ax.X(p[0] - u[0] / 2), ax.Y(p[1] - u[1] / 2), ax.X(p[0] + u[0] / 2), ax.Y(p[1] + u[1] / 2), col, 1.1)
    s.circle(ax.X(src[0]), ax.Y(src[1]), 7, TEXT, 'none', 1.6)
    s.circle(ax.X(est[0]), ax.Y(est[1]), 3, CLAY, CLAY)
    s.mono(440, 120, 'f(r) = sin 5r', 11.5, 'start', TEXT)
    s.mono(440, 144, 'cam: đẩy ra', 11, 'start', CLAY)
    s.mono(440, 162, 'xanh: kéo vào', 11, 'start', BLUE)
    s.mono(440, 196, f'ước lượng ({est[0]:.2f}, {est[1]:.2f})', 11, 'start', CLAY, 600)
    s.mono(440, 214, 'nguồn thật (0.35, −0.20)', 11, 'start', MUTED)
    s.save('8-3-field', 'Trường lực tự sinh của bài với f(r) = sin 5r (vẽ thưa, mỗi mũi tên cùng độ dài): lực đổi chiều theo khoảng cách nhưng mọi mũi tên vẫn nằm trên đường qua nguồn; bình phương tối thiểu tìm lại nguồn (0.35, −0.20).')


FIGS83 = {'8-3-partition': partition83, '8-3-split': split83, '8-3-turns': turns83, '8-3-mismatch': mismatch83,
          '8-3-penalty': penalty83, '8-3-ablation': ablation83, '8-3-field': field83}

# ───────────────────────────── 8.4 ─────────────────────────────

_T84 = {}


def ns84():
    if not _T84:
        _T84['ns'] = lesson_ns('8.4', upto=11)
    return _T84['ns']


def voting84():
    P = np.array([[0.51, 0.51, 0.01], [0.90, 0.60, 0.60], [0.20, 0.80, 0.70], [0.80, 0.10, 0.10]])
    hard = ((P >= .5).sum(axis=1) >= 2).astype(int)
    m = P.mean(axis=1)
    soft = (m >= .5).astype(int)
    s = Fig(640, 230)
    x0, cw, ch, g = 120, 66, 30, 6
    for j, nm in enumerate(['model 1', 'model 2', 'model 3']):
        s.label(x0 + j * (cw + g) + cw / 2, 22, nm, 11, color=MUTED)
    s.label(x0 + 3 * (cw + g) + 50, 22, 'hard', 11, color=MUTED)
    s.label(x0 + 3 * (cw + g) + 130, 22, 'mean', 11, color=MUTED)
    s.label(x0 + 3 * (cw + g) + 205, 22, 'soft', 11, color=MUTED)
    for i in range(4):
        y = 36 + i * (ch + g)
        s.label(x0 - 12, y + ch / 2, f'mẫu {i + 1}', 11.5, 'end', TEXT, 600 if i == 0 else 400)
        for j in range(3):
            v = P[i, j]
            s.box(x0 + j * (cw + g), y, cw, ch, 'none', CLAY if v >= .5 else BLUE, r=4, width=0, opacity=.1 + .5 * abs(v - .5) * 2 * .6)
            s.mono(x0 + j * (cw + g) + cw / 2, y + ch / 2 + .5, f'{v:.2f}', 11.5, 'middle', TEXT)
        xh = x0 + 3 * (cw + g)
        diff = hard[i] != soft[i]
        s.mono(xh + 50, y + ch / 2 + .5, str(hard[i]), 13, 'middle', CLAY if diff else TEXT, 600 if diff else 400)
        s.mono(xh + 130, y + ch / 2 + .5, f'{m[i]:.3f}', 11.5, 'middle', MUTED)
        s.mono(xh + 205, y + ch / 2 + .5, str(soft[i]), 13, 'middle', CLAY if diff else TEXT, 600 if diff else 400)
    s.box(x0 - 70, 36 - 3, 3 * (cw + g) + 70 + 230, ch + 6, CLAY, 'none', r=6, width=1.2, dash='4 4')
    s.label(320, 214, 'ô cam: nghiêng về lớp 1; mẫu 1 là chỗ hai cách gộp khác nhau', 11, color=MUTED)
    s.save('8-4-voting', 'Bảng bốn mẫu của bài (từ code): ở mẫu 1, hai model hơi nghiêng về lớp 1 nên hard voting chọn 1, nhưng model thứ ba rất chắc lớp 0 kéo trung bình xác suất xuống 0.343.')


def logit84():
    s = Fig(640, 240)
    ax = s.axes(80, 26, 440, 170, (-6, 6), (0, 1), xticks=[-6, -2, 0, 2, 6], yticks=[0, .5, 1], grid=False, xlabel='logit')
    xs = np.linspace(-6, 6, 200)
    ax.line(xs, 1 / (1 + np.exp(-xs)), FAINT, 1.6)
    ax.hline(.5, FAINT, 1, '3 3')
    sig = lambda z: 1 / (1 + math.exp(-z))
    for z in (5, -2, -2):
        s.circle(ax.X(z), ax.Y(sig(z)), 4.5, BLUE, BLUE)
    zbar = 1 / 3
    pbar = (sig(5) + 2 * sig(-2)) / 3
    s.circle(ax.X(zbar), ax.Y(sig(zbar)), 6, CLAY, CLAY)
    s.mono(ax.X(zbar) - 12, ax.Y(sig(zbar)) - 14, f'mean logit → {sig(zbar):.3f}', 11, 'end', CLAY, 600)
    s.line(ax.X(-6), ax.Y(pbar), ax.X(6), ax.Y(pbar), GREEN, 1.4, '5 3')
    s.mono(ax.X(6) + 8, ax.Y(pbar), f'mean p = {pbar:.3f}', 11, 'start', GREEN, 600)
    s.mono(ax.X(5), ax.Y(sig(5)) + 16, '+5', 10.5, 'middle', BLUE)
    s.mono(ax.X(-2), ax.Y(sig(-2)) - 14, '−2, −2', 10.5, 'middle', BLUE)
    s.save('8-4-logit', 'Ba logit +5, −2, −2: trung bình logit là 1/3, qua sigmoid được 0.583 (lớp 1); trung bình ba xác suất 0.993, 0.119, 0.119 là 0.411 (lớp 0), vì sigmoid ép logit +5 về gần 1.')


def rank84():
    y = np.array([0, 0, 0, 1, 1, 1])
    a = np.array([0.47, 0.48, 0.50, 0.49, 0.52, 0.53])
    b = np.array([0.20, 0.70, 0.05, 0.85, 0.40, 0.95])
    from scipy.stats import rankdata
    rows = [('A', a, (.4, .6), '0.889'), ('B', b, (0, 1), '0.889'), ('mean', (a + b) / 2, (.25, .75), '0.889'),
            ('rank mean', (rankdata(a) + rankdata(b)) / 2, (1, 6), '1.000')]
    s = Fig(640, 250)
    x0, W = 120, 380
    for r, (nm, v, (lo, hi), auc) in enumerate(rows):
        yy = 40 + r * 50
        s.label(x0 - 14, yy, nm, 12, 'end', TEXT, 600 if r == 3 else 400)
        s.line(x0, yy, x0 + W, yy, SOFT_LINE, 1.2)
        order = np.argsort(v, kind='stable')
        for i in range(6):
            x = x0 + (v[i] - lo) / (hi - lo) * W
            col = CLAY if y[i] else BLUE
            s.circle(x, yy, 6, col, col, 0, .7)
        s.mono(x0 + W + 16, yy + .5, f'AUC {auc}', 11.5, 'start', GREEN if r == 3 else TEXT, 600 if r == 3 else 400)
    s.label(x0 + W / 2, 236, 'xanh: mẫu âm, cam: mẫu dương; mỗi dòng dùng thang riêng của nó', 11, color=MUTED)
    s.save('8-4-rank', 'Sáu mẫu của bài trên bốn thang điểm: A và B mỗi model sai một cặp; trung bình điểm thô để B lấn át nên vẫn sai cặp của B; trung bình hạng tách hẳn ba mẫu dương khỏi ba mẫu âm, AUC 1.000.')


def correlation84():
    s = Fig(640, 240)
    ax = s.axes(80, 26, 420, 170, (1, 20), (0, 1), xticks=[1, 5, 10, 15, 20], yticks=[0, .5, 1], grid=False, xlabel='số model K')
    ks = np.arange(1, 21)
    for rho, col in [(0, GREEN), (.5, BLUE), (.9, CLAY)]:
        ratio = (1 + (ks - 1) * rho) / ks
        ax.line(ks, ratio, col, 2)
        ax.hline(rho, col, .8, '3 3') if rho else None
        s.mono(ax.X(20) + 8, ax.Y(ratio[-1]), f'ρ = {rho:g}', 11, 'start', col, 600)
    s.label(ax.x - 8, ax.y - 12, 'Var(trung bình) / σ²', 11, 'start', FAINT)
    s.save('8-4-correlation', 'Phương sai của sai số trung bình theo số model, theo công thức của bài: ρ = 0 giảm như 1/K; ρ = 0.5 và ρ = 0.9 dừng ở mức ρ (vạch đứt) dù thêm bao nhiêu model.')


def vote84():
    from math import comb
    maj = lambda p, k: sum(comb(k, j) * p ** j * (1 - p) ** (k - j) for j in range(k // 2 + 1, k + 1))
    s = Fig(640, 240)
    ax = s.axes(80, 26, 420, 170, (1, 15), (.3, 1), xticks=[1, 3, 5, 7, 9, 11, 13, 15], yticks=[.4, .6, .8, 1], grid=False, xlabel='số model K (lẻ)')
    ks = np.arange(1, 16, 2)
    for p, col in [(.7, GREEN), (.45, CLAY)]:
        v = [maj(p, k) for k in ks]
        ax.line(ks, v, col, 2)
        ax.dots(ks, v, col, 3.5, col)
        s.mono(ax.X(15) + 8, ax.Y(v[-1]), f'p = {p}: {v[-1]:.3f}', 11, 'start', col, 600)
    s.mono(ax.X(3) + 8, ax.Y(maj(.7, 3)) + 14, '0.784', 10.5, 'start', GREEN)
    s.label(ax.x - 8, ax.y - 12, 'accuracy của bỏ phiếu đa số', 11, 'start', FAINT)
    s.save('8-4-vote', 'Bỏ phiếu đa số của K model sai độc lập: mỗi model đúng 70% thì 3 model đạt 0.784, 15 model đạt 0.950; mỗi model chỉ đúng 45% thì thêm model làm bỏ phiếu tệ đi, 15 model còn 0.346.')


def moons84():
    ns = ns84()
    s = Fig(640, 260)
    for k, (nm, X, y) in enumerate([('train 360', ns['X_train'], ns['y_train']), ('tune 120', ns['X_tune'], ns['y_tune']),
                                    ('audit 120', ns['X_audit'], ns['y_audit'])]):
        ax = s.axes(30 + k * 205, 34, 180, 160, (-1.8, 2.8), (-1.4, 1.9), xticks=[], yticks=[], grid=False)
        for c, col in ((0, BLUE), (1, CLAY)):
            m = y == c
            ax.dots(X[m, 0], X[m, 1], col, 2.2 if k == 0 else 2.8, col, .6)
        s.label(ax.x + 90, 20, nm, 12, color=TEXT, weight=600)
    s.label(320, 236, 'cùng make_moons, chia một lần: tune chọn trọng số, audit chỉ mở cho phương án đã khóa', 11, color=MUTED)
    s.save('8-4-moons', 'Dữ liệu make_moons của bài (từ code): 360 mẫu để fit model, 120 mẫu tune để chọn trọng số, 120 mẫu audit giữ riêng; hai bán nguyệt chồng lên nhau ở giữa, nơi mọi model đều dễ sai.')


def tune84():
    ns = ns84()
    grid, losses = ns['weight_grid'], ns['losses']
    s = Fig(640, 270)
    # tam giác: đỉnh linear (trên), forest (trái dưới), kNN (phải dưới)
    A, B, C = np.array([250., 40.]), np.array([80., 230.]), np.array([420., 230.])
    lo, hi = min(losses), max(losses)
    s.path(f'M {A[0]} {A[1]} L {B[0]} {B[1]} L {C[0]} {C[1]} Z', SOFT_LINE, 1, 'none')
    for w, L in zip(grid, losses):
        p = w[0] * A + w[1] * B + w[2] * C
        t = (L - lo) / (hi - lo)
        s.circle(p[0], p[1], 11, BLUE, BLUE, 0, .15 + .7 * (1 - t))
        s.mono(p[0], p[1] + 21, f'{L:.3f}', 9, 'middle', MUTED)
    pc = np.array(ns['chosen_weights']) @ np.stack([A, B, C])
    pe = np.full(3, 1 / 3) @ np.stack([A, B, C])
    s.circle(pc[0], pc[1], 15, CLAY, 'none', 2)
    s.circle(pe[0], pe[1], 6, TEXT, 'none', 1.4)
    s.label(A[0], A[1] - 14, 'linear', 11.5, color=TEXT, weight=600)
    s.label(B[0] - 20, B[1], 'forest', 11.5, 'end', TEXT, 600)
    s.label(C[0] + 20, C[1], 'kNN', 11.5, 'start', TEXT, 600)
    s.mono(480, 100, 'chọn (0, 0.25, 0.75)', 11, 'start', CLAY, 600)
    s.mono(480, 118, 'tune 0.169 · audit 0.211', 10.5, 'start', CLAY)
    s.mono(480, 152, 'đều (1/3, 1/3, 1/3)', 11, 'start', TEXT)
    s.mono(480, 170, 'tune 0.219 · audit 0.238', 10.5, 'start', MUTED)
    s.save('8-4-tune-audit', 'Lưới 15 bộ trọng số của bài trên tam giác ba model (đỉnh là model đơn); số dưới mỗi chấm là log loss tune, chấm đậm hơn là thấp hơn. Bộ được chọn (0, 0.25, 0.75) đạt 0.169 trên tune và 0.211 trên audit.')


def extreme84():
    ns = ns84()
    p = ns['tune_probs'][2, :, 1]
    y = ns['y_tune']
    s = Fig(640, 250)
    ax = s.axes(80, 26, 440, 150, (0, 1), (0, 50), xticks=[0, .25, .5, .75, 1], yticks=[0, 20, 40], grid=False, xlabel='xác suất lớp 1 của kNN trên tune')
    edges = np.linspace(0, 1, 16)
    edges[-1] = 1.0001
    for i in range(15):
        m = (p >= edges[i]) & (p < edges[i + 1])
        n = int(m.sum())
        if n:
            s.rect(ax.X(edges[i]) + 1, ax.Y(n), ax.X(edges[1]) - ax.X(0) - 2, ax.Y(0) - ax.Y(n), 'none',
                   CLAY if i in (0, 14) else BLUE, 2, .5, 0)
            if i in (0, 14):
                s.mono(ax.X((edges[i] + min(edges[i + 1], 1)) / 2), ax.Y(n) - 9, str(n), 11, 'middle', CLAY, 600)
    wrong = (p == 0) | (p == 1)
    wrong &= (p >= .5) != y
    s.mono(ax.X(.5), 226, f'{int(((p == 0) | (p == 1)).sum())} / 120 xác suất đúng 0 hoặc 1; {int(wrong.sum())} trong số đó sai', 11, 'middle', CLAY)
    s.label(ax.x - 8, ax.y - 12, 'số mẫu', 11, 'start', FAINT)
    s.save('8-4-extreme', 'Xác suất lớp 1 của kNN (15 hàng xóm) trên 120 mẫu tune, từ code bài: 71 mẫu nhận đúng 0 hoặc 1, và một mẫu tự tin sai một mình góp khoảng 36 trên tổng 50.4 của log loss.')


def seeds84():
    s = Fig(640, 206)
    v = [0.224, 0.2336, 0.232, 0.2106, 0.2025]
    lo, hi, x0, W = .195, .24, 90, 460

    def X(t):
        return x0 + (t - lo) / (hi - lo) * W
    s.line(x0, 70, x0 + W, 70, SOFT_LINE, 1.2)
    for t in v:
        s.circle(X(t), 70, 6, BLUE, BLUE, 0, .6)
    s.line(X(min(v)), 46, X(max(v)), 46, BLUE, 1.2)
    s.mono((X(min(v)) + X(max(v))) / 2, 34, 'năm seed forest: dao động 0.031', 11, 'middle', BLUE)
    s.circle(X(.2192), 70, 7, CLAY, 'none', 2)
    s.mono(X(.2192), 96, 'trung bình 5 seed 0.219', 10.5, 'middle', CLAY)
    s.line(X(.2190), 120, X(.2240), 120, GREEN, 3)
    s.mono(X(.2215), 138, 'equal weights so với forest: 0.005', 10.5, 'middle', GREEN)
    for t in (.20, .21, .22, .23, .24):
        s.mono(X(t), 172, f'{t:.2f}', 10, 'middle', FAINT)
    s.mono(x0 + W / 2, 192, 'log loss tune', 10, 'middle', FAINT)
    s.save('8-4-seeds', 'Log loss tune của năm seed forest (số từ output bài) trải 0.031, lớn hơn sáu lần mức chênh 0.005 giữa equal weights và forest; trung bình năm seed 0.219 nằm sát trung bình các bản đơn.')


def stacking84():
    s = Fig(640, 230)
    names = ['linear', 'forest', 'kNN', 'tree']
    a = [0.52, 1.7, 1.7, 4.85]
    b = [0.59, 1.27, 3.23, 1.73]
    ax = s.axes(90, 30, 420, 140, (0, 4), (0, 5), xticks=[], yticks=[0, 2, 4], grid=False)
    for k in range(4):
        for j, (v, col) in enumerate([(a[k], CLAY), (b[k], GREEN)]):
            x = k + .14 + j * .37
            s.rect(ax.X(x), ax.Y(v), ax.X(.33) - ax.X(0), ax.Y(0) - ax.Y(v), 'none', col, 3, .5, 0)
            s.mono(ax.X(x + .165), ax.Y(v) - 9, f'{v:g}', 10.5, 'middle', TEXT)
        s.label(ax.X(k + .5), ax.y + ax.h + 16, names[k], 12, color=TEXT)
    s.box(530, 60, 12, 12, 'none', CLAY, r=2, width=0, opacity=.5)
    s.label(548, 66, 'in-sample', 11, 'start', TEXT)
    s.mono(548, 82, 'tune 0.208', 10.5, 'start', MUTED)
    s.box(530, 104, 12, 12, 'none', GREEN, r=2, width=0, opacity=.5)
    s.label(548, 110, 'OOF', 11, 'start', TEXT)
    s.mono(548, 126, 'tune 0.176', 10.5, 'start', MUTED)
    s.label(ax.x - 8, ax.y - 14, 'hệ số của meta-model', 11, 'start', FAINT)
    s.save('8-4-stacking', 'Hệ số của meta-model logistic regression (số từ output bài): học trên dự đoán in-sample, cây quyết định đúng 100% trên train nhận hệ số 4.85; học trên OOF, hệ số của cây còn 1.73 và log loss tune tốt hơn.')


FIGS84 = {'8-4-voting': voting84, '8-4-logit': logit84, '8-4-rank': rank84, '8-4-correlation': correlation84, '8-4-vote': vote84,
          '8-4-moons': moons84, '8-4-tune-audit': tune84, '8-4-extreme': extreme84, '8-4-seeds': seeds84, '8-4-stacking': stacking84}

# ───────────────────────────── 8.5 ─────────────────────────────

_T85 = {}


def ns85():
    if not _T85:
        _T85['ns'] = lesson_ns('8.5', upto=6)
    return _T85['ns']


def pipeline85():
    s = Fig(640, 150)
    steps = [('fit', 'pipeline'), ('lưu', 'artifact'), ('nạp', 'tiến trình mới'), ('predict', 'theo tên cột'), ('CSV', 'đọc lại'), ('hash', 'SHA-256')]
    w, g = 92, 12
    for i, (a, b) in enumerate(steps):
        x = 14 + i * (w + g)
        col = CLAY if i == 2 else BLUE
        s.box(x, 40, w, 52, 'none', col, r=6, width=0, opacity=.28 if i == 2 else .15)
        s.label(x + w / 2, 58, a, 12, color=TEXT, weight=600)
        s.label(x + w / 2, 77, b, 10.5, color=MUTED)
        if i < 5:
            s.arrow(x + w + 1, 66, x + w + g - 1, 66, MUTED, 1.2)
    s.label(320, 122, 'tiến trình mới không thấy biến nào trong RAM của notebook', 11, color=CLAY)
    s.save('8-5-pipeline', 'Đường chạy của bài: fit pipeline, lưu artifact, nạp ở một tiến trình mới, dự đoán với cột chọn theo tên, ghi CSV rồi đọc lại, cuối cùng ghi hash của đúng file sẽ nộp.')


def colorder85():
    rows = [('x0, x1, x2', .933), ('x0, x2, x1', .800), ('x1, x0, x2', .900), ('x1, x2, x0', .667), ('x2, x0, x1', .700), ('x2, x1, x0', .633)]
    s = Fig(640, 270)
    for k, (nm, v) in enumerate(rows):
        y = 24 + k * 38
        s.mono(140, y + 13, nm, 11.5, 'end', TEXT, 600 if k == 0 else 400)
        s.box(152, y, 400 * v, 26, 'none', GREEN if k == 0 else BLUE, r=4, width=0, opacity=.45 if k == 0 else .25)
        s.mono(152 + 400 * v + 8, y + 13.5, f'{v:.3f}', 11.5, 'start', TEXT, 600 if k == 0 else 400)
    s.label(352, 256, 'cùng model, cùng ma trận (30, 3); chỉ đổi thứ tự cột', 11, color=MUTED)
    s.save('8-5-column-order', 'Accuracy validation của cùng một model theo sáu thứ tự cột (số từ output bài): chỉ thứ tự x0, x1, x2 lúc fit cho 0.933; các thứ tự khác không báo lỗi nhưng tụt tới 0.633.')


def refit85():
    ns = ns85()
    sc = ns['model'].named_steps['standardscaler']
    imp = ns['model'].named_steps['simpleimputer']
    T = ns['test_features'].copy()
    Ti = np.where(np.isnan(T), imp.statistics_, T)
    z_train = (Ti - sc.mean_) / sc.scale_
    z_test = (Ti - Ti.mean(axis=0)) / Ti.std(axis=0)
    s = Fig(640, 170)
    ids = ['001', '009', '010']
    s.label(140, 24, 'x0 sau chuẩn hóa', 12, color=TEXT, weight=600)
    for r, (nm, z, col) in enumerate([('mean, std của train', z_train[:, 0], GREEN), ('mean, std của 3 dòng test', z_test[:, 0], CLAY)]):
        y = 60 + r * 64
        s.label(190, y, nm, 11.5, 'end', TEXT)
        s.line(210, y, 590, y, SOFT_LINE, 1.2)
        for i, v in enumerate(z):
            x = 400 + v * 70
            s.circle(x, y, 6, col, col, 0, .7)
            s.mono(x, y - 14, ids[i], 10, 'middle', MUTED)
            s.mono(x, y + 16, f'{v:+.2f}', 10, 'middle', col)
    s.save('8-5-refit', 'Ba dòng test của bài: chuẩn hóa x0 bằng thống kê train (đã lưu trong pipeline) và bằng thống kê tính lại trên chính ba dòng test cho các giá trị khác hẳn, nên cùng một mẫu nhận đầu vào khác.')


def pickle85():
    s = Fig(640, 210)
    s.box(20, 30, 200, 120, 'none', BLUE, r=8, width=0, opacity=.12)
    s.label(120, 48, 'tiến trình tạo file', 12, color=TEXT, weight=600)
    s.mono(36, 76, 'def clip_log(v):', 10.5, 'start', TEXT)
    s.mono(50, 94, 'return np.log1p(...)', 10.5, 'start', TEXT)
    s.mono(36, 122, 'pickle.dumps(step)', 10.5, 'start', MUTED)
    s.box(250, 62, 140, 56, 'none', SAND, r=6, width=0, opacity=.3)
    s.label(320, 50, 'bytes trong pickle', 11, color=MUTED)
    s.mono(320, 82, '__main__.clip_log', 10.5, 'middle', TEXT)
    s.mono(320, 102, 'không có log1p', 10.5, 'middle', CLAY)
    s.arrow(222, 90, 248, 90, MUTED, 1.2)
    s.arrow(392, 90, 418, 90, MUTED, 1.2)
    s.box(420, 30, 200, 120, 'none', CLAY, r=8, width=0, opacity=.12)
    s.label(520, 48, 'tiến trình máy chấm', 12, color=TEXT, weight=600)
    s.mono(436, 82, 'pickle.loads(...)', 10.5, 'start', MUTED)
    s.mono(436, 104, "AttributeError:", 10.5, 'start', CLAY, 600)
    s.mono(436, 122, "no 'clip_log'", 10.5, 'start', CLAY)
    s.label(320, 182, 'pickle ghi tên hàm, không ghi thân hàm', 11.5, color=MUTED)
    s.save('8-5-pickle', 'Pickle của FunctionTransformer(clip_log) chỉ chứa tên __main__.clip_log, không chứa thân hàm; tiến trình máy chấm không có hàm ấy nên dừng với AttributeError.')


def hash85():
    ns = ns85()
    from hashlib import sha256
    a = ns['csv_text']
    b = a.replace('0.994059', '0.994058')
    ha, hb = sha256(a.encode()).hexdigest(), sha256(b.encode()).hexdigest()
    s = Fig(640, 200)
    for r, (txt, h, nm, col) in enumerate([(a, ha, 'bản đã kiểm', GREEN), (b, hb, 'đổi một chữ số', CLAY)]):
        y = 30 + r * 80
        last = txt.strip().splitlines()[-1]
        s.label(20, y + 10, nm, 12, 'start', TEXT, 600)
        s.mono(20, y + 34, f'…{last}', 11, 'start', col if r else TEXT)
        s.mono(200, y + 22, h[:32], 11, 'start', col)
        s.mono(200, y + 40, h[32:], 11, 'start', col)
    s.label(320, 186, 'hash khác hẳn dù file chỉ khác một chữ số', 11, color=MUTED)
    s.save('8-5-hash', 'SHA-256 của CSV trong bài và của cùng file chỉ đổi chữ số cuối của xác suất cuối: hai hash khác hẳn nhau, nên hash nhận diện đúng từng byte của file đã kiểm, không nói gì về chất lượng.')


def seedsplit85():
    from sklearn.model_selection import train_test_split
    ids = np.array([f'm{i}' for i in range(10)])
    rev = ids[::-1]
    s = Fig(640, 200)
    for r, (nm, arr) in enumerate([('đọc theo thứ tự A', ids), ('đọc theo thứ tự B', rev)]):
        _, va = train_test_split(np.arange(10), test_size=.3, random_state=85)
        y = 40 + r * 70
        s.label(150, y + 14, nm, 12, 'end', TEXT, 600)
        for i in range(10):
            on = i in va
            s.box(164 + i * 42, y, 38, 28, 'none', CLAY if on else BLUE, r=4, width=0, opacity=.45 if on else .15)
            s.mono(183 + i * 42, y + 14.5, arr[i], 10.5, 'middle', TEXT)
        sel = sorted(arr[va])
        s.mono(164, y + 44, 'validation: ' + ', '.join(sel), 10.5, 'start', CLAY)
    s.label(320, 190, 'cùng random_state = 85 chọn cùng vị trí; mẫu ở các vị trí ấy đã khác', 11, color=MUTED)
    s.save('8-5-seedsplit', 'Mười mẫu đọc theo hai thứ tự, cùng train_test_split với random_state = 85: các vị trí được chọn giống nhau nhưng mẫu nằm ở đó khác, nên validation gồm những mẫu khác.')


def sessions85():
    data = {'kế hoạch': [30, 75, 195, 45, 15], 'buổi 1': [20, 80, 225, 0, 35], 'buổi 2': [30, 65, 180, 70, 15]}
    cols = [FAINT, SAND, BLUE, GREEN, CLAY]
    names = ['đọc', 'baseline', 'cải thiện', 'chạy lại', 'kiểm']
    s = Fig(640, 250)
    x0, sc = 110, 500 / 360
    for r, (nm, v) in enumerate(data.items()):
        y = 40 + r * 56
        s.label(x0 - 12, y + 14, nm, 12, 'end', TEXT, 600)
        t = 0
        for k, m in enumerate(v):
            if m:
                s.box(x0 + t * sc + 1, y, m * sc - 2, 28, 'none', cols[k], r=3, width=0, opacity=.45)
                if m >= 45:
                    s.mono(x0 + (t + m / 2) * sc, y + 14.5, str(m), 10.5, 'middle', TEXT)
            t += m
        close = sum(v[:3])
        s.path(f'M {x0 + close * sc} {y - 2} l -5 -7 l 10 0 Z', TEXT, 0, TEXT)
        s.mono(x0 + close * sc, y - 14, str(close), 10, 'middle', TEXT, 600)
    for k, nm in enumerate(names):
        s.box(x0 + k * 100, 214, 12, 12, 'none', cols[k], r=2, width=0, opacity=.55)
        s.label(x0 + k * 100 + 18, 220, nm, 11, 'start', TEXT)
    s.save('8-5-sessions', 'Ba lịch 360 phút từ bảng nhật ký của bài; tam giác là phút đóng thí nghiệm. Buổi 2 đóng ở phút 275 để chạy lại 70 phút; buổi 1 đóng ở phút 325, không chạy lại và dùng 35 phút cuối để sửa file.')


def causes85():
    s = Fig(640, 190)
    rows = [('hàm tự viết khi nạp', 35, 'quy trình', CLAY), ('đảo thứ tự cột', 20, 'quy trình', CLAY), ('nhầm hướng metric', 5, 'kiến thức', BLUE)]
    for k, (nm, m, grp, col) in enumerate(rows):
        y = 30 + k * 42
        s.label(170, y + 13, nm, 12, 'end', TEXT)
        s.box(184, y, m * 9, 26, 'none', col, r=4, width=0, opacity=.45)
        s.mono(184 + m * 9 + 8, y + 13.5, f'{m} phút', 11.5, 'start', TEXT, 600)
        s.label(184 + m * 9 + 70, y + 13, grp, 11, 'start', col)
    s.label(320, 172, 'quy trình 55 trên 60 phút: luyện nạp ở môi trường trống và readback trước', 11, color=MUTED)
    s.save('8-5-causes', 'Ba lần mất giờ trong nhật ký: hai lỗi quy trình (35 và 20 phút) chiếm 55 trên 60 phút, lỗi kiến thức chỉ 5 phút; việc luyện tiếp nên bắt đầu từ quy trình.')


FIGS85 = {'8-5-pipeline': pipeline85, '8-5-column-order': colorder85, '8-5-refit': refit85, '8-5-pickle': pickle85,
          '8-5-hash': hash85, '8-5-seedsplit': seedsplit85, '8-5-sessions': sessions85, '8-5-causes': causes85}

FIGS = {**FIGS81, **FIGS82, **FIGS83, **FIGS84, **FIGS85}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
