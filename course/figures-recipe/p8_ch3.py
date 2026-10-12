"""Lượt 8 — hình chương 3 (bản gọn). Số liệu lấy từ code bài (lesson_ns) hoặc tính lại đúng như bài.
Chạy riêng: python -B -X utf8 p8_ch3.py [tên ...]"""
import math, sys
import numpy as np
from kit import *
from p8_ch1 import lesson_ns
from p8_ch2 import PAPER, sup, mnum, clip, segline, regions, jit

# ───────────────────────────── 3.1 ─────────────────────────────


def matrix(s, x, y, vals, col, cw=40, ch=34, fills=None, size=15):
    return s.tiles(x, y, [[mnum(v) if not isinstance(v, str) else v for v in row] for row in vals], cw, ch, col, 4, fills, size=size)


def shapes31():
    X = [[1, 2, 3], [4, 5, 6]]
    W = [[1, 0], [0, 1], [1, 1]]
    Y = [[4.5, 4.5], [10.5, 10.5]]
    s = Fig(640, 210)
    hx = {(0, j): (BLUE, .32) for j in range(3)}
    hw = {(i, 0): (CLAY, .32) for i in range(3)}
    hy = {(0, 0): (TEXT, .18)}
    matrix(s, 20, 58, X, BLUE, fills=hx)
    s.mono(80, 36, 'X  (2, 3)', 12.5, 'middle', MUTED)
    s.mono(178, 90, '@', 18, 'middle', MUTED)
    matrix(s, 196, 40, W, CLAY, fills=hw)
    s.mono(240, 22, 'W  (3, 2)', 12.5, 'middle', MUTED)
    s.mono(306, 90, '+', 18, 'middle', MUTED)
    matrix(s, 326, 75, [[.5, -.5]], SAND)
    s.mono(370, 58, 'b  (2,)', 12.5, 'middle', MUTED)
    s.mono(436, 90, '=', 18, 'middle', MUTED)
    matrix(s, 460, 58, Y, TEXT, cw=52, fills=hy)
    s.mono(516, 36, 'Y  (2, 2)', 12.5, 'middle', MUTED)
    s.mono(320, 178, '1·1 + 2·0 + 3·1 + 0.5 = 4.5', 13, 'middle', TEXT)
    s.label(320, 200, 'chiều 3 bị gộp; hai mẫu giữ nguyên', 12, color=MUTED)
    s.save('3-1-shapes', 'X @ W + b: hàng đầu của X nhân cột đầu của W rồi cộng bias cho ô 4.5; chiều 3 bị gộp, hai mẫu giữ nguyên.')


def reshape31():
    cols = [BLUE, BLUE, BLUE, CLAY, CLAY, CLAY]
    A = [[0, 1, 2], [3, 4, 5]]
    R = [[0, 1], [2, 3], [4, 5]]
    T = [[0, 3], [1, 4], [2, 5]]
    s = Fig(640, 200)
    for k_, (title, M, x0) in enumerate([('A  (2, 3)', A, 40), ('A.reshape(3, 2)', R, 250), ('A.transpose(0, 1)', T, 460)]):
        fills = {(i, j): (cols[v], .22) for i, row in enumerate(M) for j, v in enumerate(row)}
        y0 = 70 if k_ == 0 else 50
        matrix(s, x0 + (0 if k_ == 0 else 20), y0, M, TEXT, fills=fills)
        s.mono(x0 + 62, 24, title, 12.5, 'middle', TEXT)
    s.label(310, 186, 'hàng đầu sau reshape: [0, 1]', 12, color=MUTED)
    s.label(520, 186, 'hàng đầu: [0, 3]', 12, color=MUTED)
    s.save('3-1-reshape', 'Cùng shape (3, 2), khác nội dung: reshape giữ thứ tự 0, 1, 2, …; transpose đưa cột cũ thành hàng mới (màu là hàng gốc của A).')


def broadcast31():
    s = Fig(640, 200)
    matrix(s, 40, 60, [[1], [2]], BLUE)
    s.mono(60, 38, 'pred (2, 1)', 12, 'middle', MUTED)
    s.mono(110, 96, '−', 18, 'middle', MUTED)
    matrix(s, 134, 79, [[1, 2]], CLAY)
    s.mono(178, 60, 'target (2,)', 12, 'middle', MUTED)
    s.mono(246, 96, '=', 18, 'middle', MUTED)
    matrix(s, 272, 60, [[0, -1], [1, 0]], TEXT, fills={(0, 1): (CLAY, .3), (1, 0): (CLAY, .3), (0, 0): (GREEN, .2), (1, 1): (GREEN, .2)})
    s.mono(316, 38, '(2, 2)', 12, 'middle', MUTED)
    s.mono(410, 84, 'mean((·)²) = 0.5', 13, 'start', CLAY, 600)
    s.mono(410, 110, 'MSE đúng = 0', 13, 'start', GREEN, 600)
    s.label(320, 176, 'mỗi dự đoán bị trừ cho mọi nhãn; chỉ đường chéo là cặp đúng', 12, color=MUTED)
    s.save('3-1-broadcast', 'Trừ (2, 1) cho (2,) không báo lỗi mà broadcast thành (2, 2): hai ô lệch đường chéo làm MSE thành 0.5 thay vì 0.')


def node(s, x, y, val, name, col, r=24):
    s.circle(x, y, r, col, SURFACE, 1.6)
    s.mono(x, y + .5, val, 15, 'middle', TEXT)
    s.mono(x, y - r - 14, name, 12.5, 'middle', MUTED)


def graph31():
    s = Fig(640, 210)
    xs = [90, 320, 550]
    for x, v, nm, col in zip(xs, ['2', '6', '25'], ['w', 'u = 3w', 'J = (u − 1)²'], [BLUE, BLUE, CLAY]):
        node(s, x, 74, v, nm, col)
    for a, b, lab in [(0, 1, '× 3'), (1, 2, '(·−1)²')]:
        s.arrow(xs[a] + 28, 74, xs[b] - 28, 74, LINE, 1.4)
        s.mono((xs[a] + xs[b]) / 2, 62, lab, 11.5, 'middle', MUTED)
    for a, b, lab in [(2, 1, 'dJ/du = 2(u − 1) = 10'), (1, 0, 'du/dw = 3')]:
        s.arrow(xs[a] - 10, 150, xs[b] + 10, 150, CLAY, 1.6)
        s.mono((xs[a] + xs[b]) / 2, 138, lab, 11.5, 'middle', CLAY)
    for x, v in zip(xs, ['30', '10', '1']):
        s.mono(x, 172, v, 14, 'middle', CLAY, 600)
    s.mono(90, 194, 'dJ/dw = 10 × 3 = 30', 12, 'start', TEXT)
    s.save('3-1-graph', 'Forward tính 2 → 6 → 25; backward đi ngược, nhân các đạo hàm cục bộ: dJ/dw = 10 × 3 = 30.')


def gradsum31():
    s = Fig(640, 160)
    steps = [('backward', '30'), ('backward', '60'), ('grad = None', '–'), ('backward', '30')]
    x = 60
    s.mono(20, 30, 'v.grad', 12.5, 'start', MUTED)
    for k, (op, val) in enumerate(steps):
        cx = 110 + k * 140
        col = CLAY if val == '60' else (MUTED if val == '–' else BLUE)
        s.box(cx - 36, 70, 72, 40, 'none', col, r=8, width=0, opacity=.16)
        s.mono(cx, 90.5, val, 16, 'middle', TEXT, 600)
        s.mono(cx, 54, op, 11.5, 'middle', MUTED)
        if k:
            s.arrow(cx - 140 + 40, 90, cx - 40, 90, LINE, 1.3)
    s.label(250, 136, '30 + 30: cộng dồn, không ghi đè', 12, color=CLAY)
    s.save('3-1-autograd-sum', 'Mỗi lần backward cộng thêm vào v.grad: 30 rồi 60; đặt grad = None xong thì lượt mới lại ra 30.')


def detach31():
    s = Fig(640, 210)
    for r, (title, cut, g) in enumerate([('giữ nguyên graph: v · v²', False, '3v² = 12'), ('v² đã detach: hằng 4 · v', True, '4')]):
        y = 60 + r * 90
        s.label(20, y - 34, title, 12.5, 'start', TEXT, 600)
        node(s, 70, y, '2', '', BLUE, 20)
        s.box(190, y - 40, 76, 30, 'none', BLUE if not cut else FAINT, r=8, width=0, opacity=.16)
        s.mono(228, y - 24.5, 'v² = 4', 13, 'middle', TEXT)
        s.box(360, y - 15, 76, 30, 'none', CLAY, r=8, width=0, opacity=.16)
        s.mono(398, y + .5, 'v³ = 8', 13, 'middle', TEXT)
        s.arrow(90, y - 9, 188, y - 24, LINE, 1.3)
        s.arrow(266, y - 24, 358, y - 6, LINE if not cut else FAINT, 1.3, None if not cut else '4 3')
        s.arrow(91, y + 6, 358, y + 6, LINE, 1.3)
        if cut:
            cxm, cym = 312, y - 15
            s.line(cxm - 6, cym - 8, cxm + 6, cym + 8, CLAY, 2.2)
            s.line(cxm + 6, cym - 8, cxm - 6, cym + 8, CLAY, 2.2)
        s.mono(470, y, f'v.grad = {g}', 13, 'start', CLAY if cut else BLUE, 600)
    s.save('3-1-detach', 'Cùng giá trị forward 8: giữ graph thì gradient là 12; detach v² thì đường qua v² bị cắt, chỉ còn 4.')


# ───────────────────────────── 3.2 ─────────────────────────────

def xor32():
    s = Fig(640, 250)
    pts = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
    ax = s.axes(50, 34, 190, 190, (-.3, 1.3), (-.3, 1.3), xticks=[0, 1], yticks=[0, 1], grid=False)
    for (a, b), y in pts:
        s.circle(ax.X(a), ax.Y(b), 8, CLAY if y else BLUE)
    s.line(ax.X(-.3), ax.Y(.5), ax.X(1.3), ax.Y(.5), FAINT, 1.4, '5 4')
    s.mono(ax.X(1.3), ax.Y(.5) - 10, '?', 13, 'end', MUTED)
    s.label(145, 16, 'đầu vào (x₁, x₂)', 13, color=TEXT, weight=600)
    s.arrow(262, 128, 340, 128, MUTED, 1.4)
    s.mono(301, 114, 'ReLU', 11.5, 'middle', MUTED)
    ax2 = s.axes(380, 34, 230, 190, (-.3, 2.4), (-.3, 1.4), xticks=[0, 1, 2], yticks=[0, 1], grid=False)
    hid = {(0, 0): (0, 0), (0, 1): (1, 0), (1, 0): (1, 0), (1, 1): (2, 1)}
    for (a, b), y in pts:
        h1, h2 = hid[(a, b)]
        off = 0
        if (a, b) == (1, 0):
            off = 10
        s.circle(ax2.X(h1) + off, ax2.Y(h2), 8, CLAY if y else BLUE)
    segline(ax2, lambda h: (h - .5) / 2, TEXT, 1.6)
    s.mono(ax2.X(1) + 5, ax2.Y(0) + 22, '(0,1) và (1,0)', 11, 'middle', CLAY)
    s.mono(ax2.X(2) - 10, ax2.Y(1) - 16, '(1,1)', 11, 'end', BLUE)
    s.label(495, 16, 'lớp ẩn (h₁, h₂)', 13, color=TEXT, weight=600)
    s.save('3-2-xor', 'Trong mặt phẳng đầu vào, không đường thẳng nào tách hai cặp góc XOR; qua lớp ẩn ReLU, hai góc nhãn 1 dồn về (1, 0) và một đường thẳng tách được.')


def backprop32():
    s = Fig(640, 250)
    layers = [(70, 2, 'X', '(B, 2)'), (260, 3, 'H', '(B, 3)'), (450, 1, 'P', '(B, 1)')]
    pos = {}
    for x, n, nm, sh in layers:
        ys = [100 + (i - (n - 1) / 2) * 46 for i in range(n)]
        pos[nm] = (x, ys)
        s.mono(x, 26, nm, 14, 'middle', TEXT, 600)
        s.mono(x, 192, sh, 11.5, 'middle', MUTED)
    for a, b in [('X', 'H'), ('H', 'P')]:
        for ya in pos[a][1]:
            for yb in pos[b][1]:
                s.line(pos[a][0] + 9, ya, pos[b][0] - 9, yb, SOFT_LINE, 1)
    for nm, (x, ys) in pos.items():
        for y in ys:
            s.circle(x, y, 9, BLUE, SURFACE, 1.6)
    s.circle(570, 100, 18, CLAY, SURFACE, 1.6)
    s.mono(570, 100.5, 'J', 13, 'middle', CLAY, 600)
    s.line(459, 100, 552, 100, SOFT_LINE, 1)
    y = 226
    for x0, x1, lab in [(570, 450, 'G₂ = 2(P − Y)/B'), (450, 260, '· W₂ᵀ  ⊙ 1[Z₁ > 0]'), (260, 70, 'Xᵀ G₁ → dW₁')]:
        s.arrow(x0 - 8, y, x1 + 8, y, CLAY, 1.6)
        s.mono((x0 + x1) / 2, y - 12, lab, 11.5, 'middle', CLAY)
    s.save('3-2-backprop', 'Mạng 2 → 3 → 1: forward đi từ trái sang; gradient đi ngược từ J, nhân W₂ᵀ để về lớp ẩn, qua cổng ReLU′ rồi mới tới W₁.')


def hand32():
    s = Fig(640, 210)
    xs = [70, 230, 390, 550]
    for x, v, nm, col in zip(xs, ['2', '1', '2', '4'], ['x', 'h = ReLU(0.5x)', 'p = 2h', 'J = (p − 0)²'], [BLUE, BLUE, BLUE, CLAY]):
        s.circle(x, 70, 22, col, SURFACE, 1.6)
        s.mono(x, 70.5, v, 15, 'middle', TEXT)
        s.mono(x, 34, nm, 11.5, 'middle', MUTED)
    for a in range(3):
        s.arrow(xs[a] + 26, 70, xs[a + 1] - 26, 70, LINE, 1.3)
    grads = [('dJ/dw₁ = 16', 70), ('dJ/dh = 8', 230), ('dJ/dp = 4', 390)]
    for (lab, x) in grads:
        s.mono(x, 160, lab.split(' = ')[1], 16, 'middle', CLAY, 600)
        s.mono(x, 184, lab.split(' = ')[0], 11.5, 'middle', CLAY)
    for x0, x1, m in [(390, 230, '× w₂ = 2'), (230, 70, '× x = 2 (ReLU mở)')]:
        s.arrow(x0 - 22, 160, x1 + 22, 160, CLAY, 1.5)
        s.mono((x0 + x1) / 2, 146, m, 11, 'middle', CLAY)
    s.arrow(550, 94, 410, 152, CLAY, 1.5)
    s.mono(500, 136, '2(p − y)', 11, 'start', CLAY)
    s.save('3-2-hand-backprop', 'Ví dụ tính tay x = 2, y = 0: forward 2 → 1 → 2 → 4; backward nhân dần 4 → 8 → 16 để ra dJ/dw₁ = 16.')


def mask32():
    s = Fig(640, 200)
    Z = [[1.1, .1], [.1, -.5]]
    fills = {(1, 1): (CLAY, .35)}
    matrix(s, 60, 64, Z, BLUE, cw=56, fills=fills)
    s.mono(118, 40, 'Z₁', 13, 'middle', TEXT, 600)
    s.mono(208, 98, '>', 16, 'middle', MUTED)
    s.mono(232, 98, '0', 16, 'middle', MUTED)
    matrix(s, 270, 64, [[1, 1], [1, 0]], BLUE, cw=44, fills=fills)
    s.mono(318, 40, 'mask', 13, 'middle', TEXT, 600)
    s.label(400, 82, 'mẫu 2, neuron 2 đóng:', 12.5, 'start', TEXT)
    s.label(400, 104, 'gradient qua ô này bằng 0', 12.5, 'start', CLAY, 600)
    s.label(320, 182, 'hàng là mẫu, cột là neuron ẩn', 11.5, color=MUTED)
    s.save('3-2-mask', 'Ở batch hai mẫu của bài, Z₁ chỉ có một ô âm; mask (Z₁ > 0) chặn gradient qua đúng ô đó, ba ô còn lại cho gradient đi qua.')


def learned32():
    import torch
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    corners = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    lab = np.array([0, 1, 1, 0])
    idx = rng.integers(0, 4, 200)
    X = corners[idx] + rng.normal(0, .15, (200, 2))
    y = lab[idx]
    tx, ty = torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)
    s = Fig(640, 230)
    xs = ys = np.linspace(-.5, 1.5, 101)
    G = torch.tensor(np.array(np.meshgrid(xs, ys)).reshape(2, -1).T, dtype=torch.float32)
    for k_, (title, hidden) in enumerate([('linear (không lớp ẩn)', 0), ('MLP 2 → 8 → 1', 8)]):
        torch.manual_seed(0)
        m = torch.nn.Linear(2, 1) if hidden == 0 else torch.nn.Sequential(torch.nn.Linear(2, 8), torch.nn.ReLU(), torch.nn.Linear(8, 1))
        opt = torch.optim.Adam(m.parameters(), lr=.05)
        for _ in range(500):
            opt.zero_grad()
            loss = torch.nn.functional.binary_cross_entropy_with_logits(m(tx).squeeze(-1), ty)
            loss.backward()
            opt.step()
        with torch.no_grad():
            pr = (m(G).squeeze(-1) > 0).numpy().astype(int).reshape(101, 101)
            acc = ((m(tx).squeeze(-1) > 0).float() == ty).float().mean().item()
        x0 = 60 + k_ * 300
        ax = s.axes(x0, 30, 190, 190, (-.5, 1.5), (-.5, 1.5), frame=False, grid=False)
        regions(s, ax, pr, xs, ys, [BLUE, CLAY], .14)
        for c_, col in [(0, BLUE), (1, CLAY)]:
            ax.dots(X[y == c_, 0], X[y == c_, 1], col, 2.4)
        s.label(x0 + 95, 14, f'{title} · train {acc:.0%}', 12.5, color=TEXT, weight=600)
    s.save('3-2-learned', '200 điểm quanh bốn góc XOR, cùng 500 bước Adam: mô hình linear chỉ đúng 57%; thêm một lớp ẩn 8 neuron ReLU thì học được cả bốn vùng.')


FIGS32 = {'3-2-xor': xor32, '3-2-backprop': backprop32, '3-2-hand-backprop': hand32, '3-2-mask': mask32, '3-2-learned': learned32}


# ───────────────────────────── 3.3 ─────────────────────────────

def sigm(z):
    return 1 / (1 + np.exp(-z))


def activation33():
    z = np.linspace(-5, 5, 201)
    s = Fig(640, 210)
    fs = [('ReLU', np.maximum(z, 0), (z > 0).astype(float), (-1, 4), CLAY),
          ('tanh', np.tanh(z), 1 - np.tanh(z) ** 2, (-1.1, 1.1), BLUE),
          ('sigmoid', sigm(z), sigm(z) * (1 - sigm(z)), (-.1, 1.1), SAND)]
    for k_, (nm, f, d, yl, col) in enumerate(fs):
        x0 = 30 + k_ * 205
        ax = s.axes(x0, 30, 180, 140, (-5, 5), yl, xticks=[-5, 0, 5], frame=False, grid=False)
        s.line(ax.X(-5), ax.Y(0), ax.X(5), ax.Y(0), SOFT_LINE, 1)
        s.line(ax.X(0), ax.y, ax.X(0), ax.y + ax.h, SOFT_LINE, 1)
        ax.line(z, d, col, 1.4, '4 3')
        ax.line(z, f, col, 2.4)
        s.label(x0 + 90, 14, nm, 13.5, color=col, weight=600)
    s.label(320, 202, 'nét liền: hàm · nét đứt: đạo hàm', 11.5, color=MUTED)
    s.save('3-3-activation', 'ReLU, tanh và sigmoid (nét liền) cùng đạo hàm của chúng (nét đứt): tanh và sigmoid có đạo hàm gần 0 ở hai đầu; ReLU có đạo hàm 0 hoặc 1.')


def depth33():
    ns = lesson_ns('3.3', upto=2)
    small, he = ns['scales_small'], ns['scales_he']
    L = math.log10
    s = Fig(640, 230)
    ax = s.axes(80, 20, 430, 170, (1, 10), (-10, 1), xticks=list(range(1, 11)), xlabel='lớp')
    for e in range(-10, 1, 2):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    layers = np.arange(1, 11)
    for v, col, nm in [(he, BLUE, 'He'), (small, CLAY, 'N(0, 0.01²)')]:
        lv = [L(x) for x in v]
        ax.line(layers, lv, col, 2.2).dots(layers, lv, col, 3)
        s.label(ax.X(10) + 8, ax.Y(lv[-1]), nm, 12.5, 'start', col, 600)
    s.label(ax.x - 8, ax.y - 12, 'std pre-activation', 11.5, 'start', FAINT)
    s.save('3-3-depth-scale', 'Độ lệch chuẩn pre-activation qua 10 lớp ReLU (trục log, số từ code bài): khởi tạo N(0, 0.01²) co khoảng 9 lần mỗi lớp, He giữ quanh 1.4.')


def residual33():
    r = np.linspace(-10.5, 10.5, 211)
    s = Fig(640, 220)
    ax = s.axes(80, 20, 420, 160, (-10.5, 10.5), (0, 110), xticks=[-10, -5, 0, 2, 5, 10], yticks=[0, 25, 50, 100], xlabel='phần dư r')
    hub = np.where(np.abs(r) <= 1, .5 * r ** 2, np.abs(r) - .5)
    ax.line(r, r ** 2, CLAY, 2.2).line(r, np.abs(r), BLUE, 2.2).line(r, hub, GREEN, 1.6, '5 4')
    for v in (2, 10):
        s.circle(ax.X(v), ax.Y(v * v), 4.5, CLAY, PAPER, 2)
    s.mono(ax.X(2) + 8, ax.Y(4) - 10, '4', 11.5, 'start', CLAY)
    s.mono(ax.X(10) - 6, ax.Y(100) - 14, '100', 11.5, 'end', CLAY)
    s.label(ax.X(6) + 10, ax.Y(36) + 4, 'MSE: r²', 12.5, 'start', CLAY, 600)
    s.label(ax.X(10.5) + 8, ax.Y(10) - 8, 'MAE: |r|', 12.5, 'start', BLUE, 600)
    s.label(ax.X(10.5) + 8, ax.Y(9.5) + 10, 'Huber', 12, 'start', GREEN, 600)
    s.save('3-3-residual-loss', 'Mức phạt theo phần dư: MSE tăng theo bình phương (sai 10 phạt 100, gấp 25 lần sai 2), MAE tăng tuyến tính; Huber là bình phương gần 0 và tuyến tính ở xa.')


def squares33():
    s = Fig(640, 190)
    base = 160
    unit = 13
    for x0, r, col in [(60, 1, BLUE), (130, 2, BLUE), (230, 10, CLAY)]:
        side = r * unit
        s.box(x0, base - side, side, side, col, col, r=2, width=1.2, opacity=.15)
        s.line(x0, base + 10, x0 + side, base + 10, col, 1.4)
        s.mono(x0 + side / 2, base + 24, f'r = {r}', 11.5, 'middle', col)
        s.mono(x0 + side + 8, base - side + 10, f'{r * r}', 13, 'start', TEXT, 600)
    s.mono(420, 100, 'MSE = (1 + 4 + 100)/3 = 35', 12, 'start', MUTED)
    s.save('3-3-loss-metrics', 'Phần dư 1, 2, 10 của ví dụ: bình phương biến chúng thành diện tích 1, 4, 100, nên một mẫu đóng gần hết MSE = 35.')


def constant33():
    ys = [10, 12, 13, 15, 90]
    s = Fig(640, 150)
    X = lambda v: 160 + (v - 5) / 90 * 430
    s.line(X(5), 80, X(95), 80, LINE, 1)
    for v in ys:
        s.circle(X(v), 80, 5, TEXT)
    s.mono(X(12.5), 104, '10 12 13 15', 11, 'middle', MUTED)
    s.mono(X(90), 104, '90', 11, 'middle', MUTED)
    for v, col, lab, anc, dx in [(13, BLUE, 'median 13 (MAE)', 'end', -6), (28, CLAY, 'mean 28 (MSE)', 'start', 6)]:
        s.line(X(v), 50, X(v), 92, col, 2)
        s.label(X(v) + dx, 46, lab, 12.5, anc, col, 600)
    s.save('3-3-constant', 'Năm thời gian 10, 12, 13, 15, 90: hằng số tốt nhất theo MSE là trung bình 28, bị bài 90 phút kéo đi; theo MAE là trung vị 13.')


def bce33():
    z = np.linspace(-6, 6, 241)
    s = Fig(640, 220)
    for k_, (title, f1, f0, yl, yt) in enumerate([('BCE theo logit z', np.log1p(np.exp(-z)), np.log1p(np.exp(z)), (0, 6.2), [0, 2, 4, 6]),
                                                    ('gradient = σ(z) − y', sigm(z) - 1, sigm(z), (-1.05, 1.05), [-1, 0, 1])]):
        x0 = 50 + k_ * 310
        ax = s.axes(x0, 30, 250, 150, (-6, 6), yl, xticks=[-6, 0, 6], yticks=yt, xlabel='z')
        ax.line(z, f1, CLAY, 2.2).line(z, f0, BLUE, 2.2)
        s.label(x0 - 8, 14, title, 12.5, 'start', TEXT, 600)
        if k_ == 0:
            s.label(ax.X(3.5), ax.Y(0) - 14, 'y = 1', 12, 'middle', CLAY, 600)
            s.label(ax.X(-3.5), ax.Y(0) - 14, 'y = 0', 12, 'middle', BLUE, 600)
        else:
            s.label(ax.X(-4), ax.Y(0) - 14, 'y = 0', 12, 'middle', BLUE, 600)
            s.label(ax.X(-4), ax.Y(-1) - 14, 'y = 1', 12, 'middle', CLAY, 600)
    s.save('3-3-bce', 'BCEWithLogits theo logit: đoán đúng tự tin thì loss về 0; đoán sai tự tin thì loss tăng gần tuyến tính và gradient σ(z) − y dần tới ±1, không tắt.')


def bars(s, x0, y0, vals, cols, labels, h=70, w=34, gap=14, vmax=1, fmt='{:.2f}', below=False):
    for i, (v, c, lb) in enumerate(zip(vals, cols, labels)):
        x = x0 + i * (w + gap)
        hh = h * v / vmax
        s.rect(x, y0 + h - hh, w, hh, 'none', c, 3, .75, 0)
        if below:
            s.mono(x + w / 2, y0 + h + 30, fmt.format(v), 11, 'middle', TEXT)
        else:
            s.mono(x + w / 2, y0 + h - hh - 9, fmt.format(v), 11, 'middle', TEXT)
        s.mono(x + w / 2, y0 + h + 14, lb, 11, 'middle', MUTED)


def twice33():
    z = np.array([math.log(2), 0])
    p = np.exp(z) / np.exp(z).sum()
    q = np.exp(p) / np.exp(p).sum()
    s = Fig(640, 200)
    for k_, (title, v, vmax, fmt) in enumerate([('logits', z, 1, '{:.2f}'), ('softmax 1 lần', p, 1, '{:.3f}'), ('softmax 2 lần', q, 1, '{:.3f}')]):
        x0 = 60 + k_ * 200
        bars(s, x0, 46, v, [CLAY, BLUE], ['lớp 0', 'lớp 1'], h=90, w=40, gap=18, vmax=vmax, fmt=fmt)
        s.label(x0 + 49, 18, title, 13, color=TEXT if k_ < 2 else CLAY, weight=600)
        if k_:
            s.arrow(x0 - 80, 100, x0 - 30, 100, MUTED, 1.3)
    s.save('3-3-softmax-twice', 'Logits (log 2, 0) cho xác suất (0.667, 0.333); softmax thêm lần nữa nén chênh lệch còn (0.583, 0.417), nên CrossEntropyLoss nhận nhầm một bài toán khác.')


def multilabel33():
    z = np.array([1.2, -.4, .1])
    sg = sigm(z)
    sm = np.exp(z) / np.exp(z).sum()
    s = Fig(640, 230)
    for k_, (title, v, col) in enumerate([('sigmoid từng logit (đa nhãn)', sg, GREEN), ('softmax (loại trừ nhau)', sm, MUTED)]):
        x0 = 70 + k_ * 300
        y0 = 50
        h = 110
        s.line(x0 - 10, y0 + h - h * .5, x0 + 150, y0 + h - h * .5, CLAY, 1.2, '4 3')
        bars(s, x0, y0, v, [col if (k_ == 0 and x > .5) else FAINT for x in v] if k_ == 0 else [FAINT, FAINT, FAINT], ['0', '1', '2'], h=h, w=36, gap=16, below=True)
        s.label(x0 + 70, 20, title, 12.5, color=TEXT, weight=600)
    s.mono(232, 105, '0.5', 11, 'start', CLAY)
    s.save('3-3-multilabel', 'Logits (1.2, −0.4, 0.1) với ngưỡng 0.5: sigmoid từng thuộc tính bật được cả 0 và 2; softmax bắt ba thuộc tính chia nhau tổng 1 nên chỉ ô lớn nhất vượt 0.5.')


FIGS33 = {'3-3-activation': activation33, '3-3-depth-scale': depth33, '3-3-residual-loss': residual33, '3-3-loss-metrics': squares33,
          '3-3-constant': constant33, '3-3-bce': bce33, '3-3-softmax-twice': twice33, '3-3-multilabel': multilabel33}


# ───────────────────────────── 3.4 ─────────────────────────────

def loop34():
    steps = [('zero_grad', '.grad = None'), ('forward', 'logits'), ('loss', 'một số'), ('backward', '.grad mới'), ('step', 'θ thay đổi')]
    s = Fig(640, 210)
    xs = [70 + k * 125 for k in range(5)]
    for k, ((nm, eff), x) in enumerate(zip(steps, xs)):
        col = CLAY if nm in ('backward', 'step') else BLUE
        s.box(x - 50, 60, 100, 44, 'none', col, r=10, width=0, opacity=.15)
        s.mono(x, 82.5, nm, 13, 'middle', TEXT, 600)
        s.label(x, 44, eff, 11.5, color=MUTED)
        if k < 4:
            s.arrow(x + 52, 82, xs[k + 1] - 52, 82, LINE, 1.3)
    s.curve(xs[4], 106, xs[0], 106, -.1, MUTED, 1.3)
    s.label(320, 168, 'batch tiếp theo', 11.5, color=MUTED)
    s.label(320, 198, 'đổi thứ tự backward / zero_grad / step là mất hoặc dùng sai gradient', 12, color=CLAY)
    s.save('3-4-loop', 'Mỗi batch đi đúng một vòng zero_grad → forward → loss → backward → step rồi mới sang batch tiếp theo.')


def batches34():
    s = Fig(640, 170)
    x = 40
    sizes = [16, 16, 16, 16, 8]
    unit = 6
    for k, n in enumerate(sizes):
        w = n * unit
        s.box(x, 50, w - 4, 40, 'none', BLUE if n == 16 else CLAY, r=6, width=0, opacity=.18)
        s.mono(x + (w - 4) / 2, 70.5, f'{n}', 13, 'middle', TEXT)
        s.mono(x + (w - 4) / 2, 108, f'step {k + 1}', 11, 'middle', MUTED)
        x += w
    s.label(40, 30, '1 epoch = 72 mẫu train', 12.5, 'start', TEXT, 600)
    s.label(x + 12, 70, '× 20 epoch = 100 step', 12.5, 'start', CLAY, 600)
    s.label(320, 150, 'batch cuối 8 mẫu vẫn là một lần cập nhật', 11.5, color=MUTED)
    s.save('3-4-batches', '72 mẫu train, batch size 16: mỗi epoch có 5 batch (bốn batch 16 và một batch 8), mỗi batch một step, nên 20 epoch là 100 step.')


def curves34():
    ns = lesson_ns('3.4', upto=4)
    h = np.array(ns['history'])
    ep, tr, va, acc = h[:, 0], h[:, 1], h[:, 2], h[:, 3]
    b = int(ns['best_epoch'])
    s = Fig(640, 262)
    ax = s.axes(70, 20, 440, 140, (1, 35), (0, .7), xticks=[1, 10, 20, 32, 35], yticks=[0, .2, .4, .6], yfmt='{:.1f}')
    ax.line(ep, tr, BLUE, 2).line(ep, va, CLAY, 2.2)
    s.line(ax.X(b), ax.y, ax.X(b), ax.y + ax.h, FAINT, 1, '3 3')
    s.circle(ax.X(b), ax.Y(va[b - 1]), 4.5, CLAY, PAPER, 2)
    s.label(ax.X(b) - 6, ax.y + 8, 'lưu checkpoint', 11.5, 'end', MUTED)
    s.label(ax.X(35) + 8, ax.Y(tr[-1]) + 8, 'train', 12, 'start', BLUE, 600)
    s.label(ax.X(35) + 8, ax.Y(va[-1]) - 8, 'validation', 12, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 10, 'loss', 11.5, 'start', FAINT)
    ax2 = s.axes(70, 206, 440, 40, (1, 35), (.4, 1.05), frame=False, grid=False)
    ax2.step(ep, acc, GREEN, 1.6)
    s.label(ax.X(35) + 8, ax2.Y(1), 'accuracy', 12, 'start', GREEN, 600)
    s.mono(ax2.X(7), ax2.Y(1) - 10, '1.0 từ epoch 7', 11, 'start', GREEN)
    s.save('3-4-curves', 'Log 35 epoch của bài: train loss giảm đều; validation loss thấp nhất ở epoch 32 rồi tăng nhẹ, nên checkpoint lấy epoch 32. Accuracy đạt 1.0 từ epoch 7 và không còn phân biệt được các epoch.')


def checkpoint34():
    s = Fig(640, 210)
    keys = ['state', 'mean', 'scale', 'query', 'expected', 'epoch']
    s.box(40, 36, 170, 6 * 24 + 12, LINE, SURFACE, r=10, width=1.2)
    s.mono(125, 22, '3-4-best.pt', 12.5, 'middle', TEXT, 600)
    for i, k in enumerate(keys):
        s.mono(60, 54 + i * 24, k, 12.5, 'start', BLUE if k in ('state', 'mean', 'scale') else MUTED)
    s.arrow(222, 110, 300, 110, MUTED, 1.4)
    s.box(310, 66, 150, 88, 'none', CLAY, r=10, width=0, opacity=.12)
    s.label(385, 92, 'tiến trình Python mới', 12.5, color=TEXT, weight=600)
    s.mono(385, 114, 'make_model()', 11.5, 'middle', MUTED)
    s.mono(385, 134, 'load_state_dict', 11.5, 'middle', MUTED)
    s.arrow(470, 110, 520, 110, MUTED, 1.4)
    s.mono(530, 100, 'match: True', 12.5, 'start', GREEN, 600)
    s.mono(530, 122, '[1, 0]', 12.5, 'start', TEXT)
    s.label(125, 200, 'đủ để suy luận, chưa đủ để train tiếp', 11.5, color=MUTED)
    s.save('3-4-checkpoint', 'Packet checkpoint của bài: trọng số, mean và scale của train, cùng đầu vào kiểm và logits mong đợi; một tiến trình Python mới chỉ dùng packet mà vẫn cho cùng kết quả.')


def wmean34():
    s = Fig(640, 170)
    unit = 10
    x = 120
    for n, l, col in [(16, .2, BLUE), (8, .8, CLAY)]:
        w = n * unit
        hh = l * 100
        s.rect(x, 120 - hh, w - 4, hh, 'none', col, 4, .7, 0)
        s.mono(x + (w - 4) / 2, 120 - hh - 10, f'{l}', 12, 'middle', TEXT)
        s.mono(x + (w - 4) / 2, 136, f'{n} mẫu', 11.5, 'middle', MUTED)
        x += w
    yb = 120 - 40
    s.line(110, yb, x + 6, yb, GREEN, 1.6)
    s.mono(x + 14, yb, 'theo mẫu: 0.4', 12.5, 'start', GREEN, 600)
    ya = 120 - 50
    s.line(110, ya, x + 6, ya, MUTED, 1.2, '4 3')
    s.mono(x + 14, ya - 8, 'trung bình hai batch: 0.5', 12, 'start', MUTED)
    s.label(60, 100, 'loss', 11.5, 'end', FAINT)
    s.save('3-4-weighted-mean', 'Batch 16 mẫu loss 0.2 và batch 8 mẫu loss 0.8: chiều rộng là số mẫu; trung bình theo mẫu là 0.4, không phải 0.5.')


def collate34():
    """3.4 mục collate_fn: ba chuỗi dài 3, 1, 4 đệm 0 thành ma trận (3, 4), giữ lengths."""
    seqs = [[5, 2, 9], [7], [3, 3, 1, 4]]
    cw, ch, g = 34, 30, 4
    w4 = 4 * (cw + g) - g
    x1 = 92; x2 = x1 + w4 + 108; xl = x2 + w4 + 46
    s = Fig(640, 132)
    s.label(x1, 12, 'ba mẫu', 13, 'start')
    for i, q in enumerate(seqs):
        s.tiles(x1, 24 + i * (ch + g), [[str(v) for v in q]], cw, ch, BLUE, g, {}, 14)
    ym = 24 + ch + g + ch / 2
    s.curve(x1 + w4 + 16, ym, x2 - 16, ym, .0, CLAY, 1.4)
    s.mono((x1 + w4 + x2) / 2, ym - 10, 'pad_collate', 12, 'middle', CLAY)
    s.label(x2, 12, 'tokens', 13, 'start', CLAY)
    vals = [[str(v) for v in q] + ['0'] * (4 - len(q)) for q in seqs]
    fills = {(i, j): (FAINT, .12) for i, q in enumerate(seqs) for j in range(len(q), 4)}
    colors = {(i, j): FAINT for i, q in enumerate(seqs) for j in range(len(q), 4)}
    s.tiles(x2, 24, vals, cw, ch, BLUE, g, fills, 14, colors=colors)
    s.label(xl, 12, 'lengths', 13, 'middle', CLAY)
    for i, q in enumerate(seqs):
        s.mono(xl, 24 + i * (ch + g) + ch / 2 + 4, str(len(q)), 14, 'middle', CLAY)
    s.save('3-4-collate', 'collate_fn đệm 0 cho bằng chuỗi dài nhất và giữ độ dài thật.')


FIGS34 = {'3-4-loop': loop34, '3-4-batches': batches34, '3-4-curves': curves34, '3-4-checkpoint': checkpoint34, '3-4-weighted-mean': wmean34, '3-4-collate': collate34}


# ───────────────────────────── 3.5 ─────────────────────────────

def opt_path(kind, lr, steps=25, mu=.8, start=(-2., 1.)):
    import torch
    p = torch.nn.Parameter(torch.tensor(start))
    if kind == 'momentum':
        o = torch.optim.SGD([p], lr=lr, momentum=mu)
    elif kind == 'adam':
        o = torch.optim.Adam([p], lr=lr)
    else:
        o = torch.optim.SGD([p], lr=lr)
    pts, losses = [p.detach().numpy().copy()], [(p[0] ** 2 + 8 * p[1] ** 2).item()]
    for _ in range(steps):
        o.zero_grad()
        l = p[0] ** 2 + 8 * p[1] ** 2
        l.backward()
        o.step()
        pts.append(p.detach().numpy().copy())
        losses.append((p[0] ** 2 + 8 * p[1] ** 2).item())
    return np.array(pts), np.array(losses)


def contours(s, ax, levels=(.5, 2, 4.5, 8)):
    t = np.linspace(0, 2 * np.pi, 181)
    for L in levels:
        xs, ys = math.sqrt(L) * np.cos(t), math.sqrt(L / 8) * np.sin(t)
        s.path('M ' + ' L '.join(f'{ax.X(a):.1f},{ax.Y(b):.1f}' for a, b in zip(xs, ys)) + ' Z', SOFT_LINE, 1)


def paths35():
    s = Fig(640, 230)
    for k_, (kind, lr, title, col) in enumerate([('sgd', .09, 'SGD', BLUE), ('momentum', .09, 'momentum μ = 0.8', CLAY), ('adam', .15, 'Adam', GREEN)]):
        P, _ = opt_path(kind, lr)
        x0 = 15 + k_ * 210
        ax = s.axes(x0, 30, 195, 190, (-2.4, 2.4), (-1.25, 1.25), frame=False, grid=False)
        clip(s, f'cp-3-5-paths-{k_}', ax.x, ax.y, ax.w, ax.h)
        contours(s, ax)
        s.path('M ' + ' L '.join(f'{ax.X(a):.1f},{ax.Y(b):.1f}' for a, b in P), col, 1.4)
        for a, b in P:
            s.circle(ax.X(a), ax.Y(b), 1.8, col)
        s.parts.append('</g>')
        s.circle(ax.X(0), ax.Y(0), 3.5, TEXT)
        s.circle(ax.X(-2), ax.Y(1), 4, col, PAPER, 1.6)
        s.label(x0 + 97, 14, title, 13, color=col, weight=600)
    s.save('3-5-paths', '25 bước trên J = w₁² + 8w₂² từ (−2, 1): SGD (η = 0.09) zigzag theo chiều dốc rồi về đáy; momentum vượt đáy rồi vòng lại; Adam (η = 0.15) đi gần chéo vì mỗi tọa độ bước cỡ η.')


def budget35():
    s = Fig(640, 230)
    L = math.log10
    ax = s.axes(70, 20, 440, 170, (0, 40), (-4, 1.3), xticks=[0, 10, 20, 30, 40], xlabel='bước')
    for e in range(-4, 2):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    for kind, lr, col, nm in [('sgd', .03, BLUE, 'SGD 0.03'), ('momentum', .03, CLAY, 'momentum 0.03'), ('adam', .15, GREEN, 'Adam 0.15')]:
        _, l = opt_path(kind, lr, 40)
        ax.line(np.arange(41), [L(max(v, 1e-4)) for v in l], col, 2)
        s.label(ax.X(40) + 8, ax.Y(L(max(l[-1], 1e-4))) + (12 if kind == 'adam' else -4 if kind == 'sgd' else 0), nm, 12, 'start', col, 600)
    for b in (30, 40):
        s.line(ax.X(b), ax.y, ax.X(b), ax.y + ax.h, FAINT, 1, '3 3')
    s.label(ax.x - 8, ax.y - 10, 'loss', 11.5, 'start', FAINT)
    s.save('3-5-budget', 'Loss theo bước (thang log): SGD rate nhỏ đi xuống đều, Adam và momentum vừa xuống vừa dao động, nên thứ hạng ở bước 30 và bước 40 khác nhau.')


def threshold35():
    eta = np.linspace(0, .16, 321)
    s = Fig(640, 220)
    ax = s.axes(80, 20, 420, 160, (0, .16), (0, 1.6), xticks=[0, .04, .08, .125, .16], yticks=[0, .5, 1, 1.5], xfmt='{:g}', xlabel='learning rate η')
    s.rect(ax.X(.125), ax.y, ax.X(.16) - ax.X(.125), ax.h, 'none', CLAY, 0, .08, 0)
    ax.hline(1, FAINT, 1, '4 3')
    ax.line(eta, np.abs(1 - 16 * eta), CLAY, 2.2).line(eta, np.abs(1 - 2 * eta), BLUE, 2.2)
    s.label(ax.X(.16) + 8, ax.Y(min(abs(1 - 16 * .16), 1.6)) + 6, '|1 − 16η|  (w₂)', 12, 'start', CLAY, 600)
    s.label(ax.X(.16) + 8, ax.Y(1 - 2 * .16), '|1 − 2η|  (w₁)', 12, 'start', BLUE, 600)
    s.label(ax.X(.1425), ax.Y(.25), 'nổ', 12, color=CLAY, weight=600)
    s.label(ax.x - 8, ax.y - 10, 'hệ số nhân mỗi bước', 11.5, 'start', FAINT)
    s.save('3-5-threshold', 'SGD trên J = w₁² + 8w₂²: mỗi bước nhân w₂ với |1 − 16η| và w₁ với |1 − 2η|; η vượt 1/8 thì chiều w₂ nổ, còn ngay dưới ngưỡng chiều w₁ vẫn chỉ co 0.75.')


def momentum35():
    v = [sum(.9 ** i for i in range(k + 1)) for k in range(30)]
    s = Fig(640, 200)
    ax = s.axes(70, 20, 440, 140, (0, 31), (0, 10.5), xticks=[1, 10, 20, 30], yticks=[0, 1, 5, 10], xlabel='bước')
    for k, val in enumerate(v):
        s.rect(ax.X(k + .6), ax.Y(val), ax.X(1) - ax.X(0) - 4, ax.Y(0) - ax.Y(val), 'none', CLAY, 2, .7, 0)
    ax.hline(10, FAINT, 1.2, '4 3')
    s.label(ax.X(31) + 8, ax.Y(10), 'g/(1 − μ) = 10g', 12, 'start', MUTED)
    s.label(ax.X(31) + 8, ax.Y(1), 'SGD: g', 12, 'start', BLUE, 600)
    ax.hline(1, BLUE, 1.4, None)
    s.label(ax.x - 8, ax.y - 10, 'độ dài v', 11.5, 'start', FAINT)
    s.save('3-5-momentum', 'Gradient không đổi g, μ = 0.9: v = g(1 + 0.9 + 0.9² + …) tăng dần tới 10g, nên bước momentum về sau dài gấp 10 bước SGD.')


def adamscale35():
    gs = [.01, 1, 100]
    s = Fig(640, 200)
    L = math.log10
    ax = s.axes(130, 20, 330, 130, (-4, 2.3), (0, 3.2), frame=False, grid=False)
    for e in range(-4, 3):
        s.line(ax.X(e), ax.y, ax.X(e), ax.y + ax.h, SOFT_LINE, .8)
        s.label(ax.X(e), ax.y + ax.h + 14, f'10{sup(e)}', 11, color=FAINT)
    s.label(ax.X(2.3), ax.y + ax.h + 30, 'độ dài bước (η = 0.1, thang log)', 11.5, 'end', FAINT)
    for i, g in enumerate(gs):
        y = ax.Y(2.6 - i)
        sgd = .1 * g
        s.line(ax.X(-4), y - 7, ax.X(L(sgd)), y - 7, BLUE, 6)
        s.line(ax.X(-4), y + 7, ax.X(L(.1)), y + 7, GREEN, 6)
        s.mono(ax.x - 14, y, f'g = {g:g}', 12, 'end', TEXT)
    s.label(480, 60, 'SGD: ηg', 12, 'start', BLUE, 600)
    s.label(480, 80, 'Adam bước đầu: ≈ η', 12, 'start', GREEN, 600)
    s.save('3-5-adam-scale', 'Gradient 0.01, 1 hay 100: bước SGD tỉ lệ với g, còn bước đầu của Adam luôn dài cỡ η = 0.1 vì gradient đã được chia cho độ lớn của chính nó.')


def schedule35():
    ns_rates = [0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025]
    T = 60
    t = np.arange(T + 1)
    cos = .1 * .5 * (1 + np.cos(np.pi * t / T))
    wu = 6
    warm = np.where(t < wu, .1 * (t + 1) / wu, .1 * .5 * (1 + np.cos(np.pi * (t - wu) / (T - wu))))
    s = Fig(640, 200)
    panels = [('StepLR (code bài)', np.arange(9), ns_rates, 'epoch', 8), ('cosine', t, cos, 'bước', T), ('warmup + cosine', t, warm, 'bước', T)]
    for k_, (title, x, y, xl, xm) in enumerate(panels):
        x0 = 40 + k_ * 205
        ax = s.axes(x0, 30, 175, 120, (0, xm), (0, .11), xticks=[0, xm], yticks=[0, .05, .1] if k_ == 0 else None, xlabel=xl, grid=k_ == 0)
        if k_ == 0:
            ax.step(np.r_[x, 9], np.r_[y, y[-1]], CLAY, 2.2)
        else:
            ax.line(x, y, CLAY, 2.2)
        s.label(x0 + 87, 14, title, 12.5, color=TEXT, weight=600)
    s.save('3-5-schedule', 'Ba lịch learning rate: StepLR của bài nhân 0.5 sau mỗi 3 epoch; cosine giảm trơn về 0; warmup tăng tuyến tính vài bước đầu rồi mới giảm.')


FIGS35 = {'3-5-paths': paths35, '3-5-budget': budget35, '3-5-threshold': threshold35, '3-5-momentum': momentum35,
          '3-5-adam-scale': adamscale35, '3-5-schedule': schedule35}


# ───────────────────────────── 3.6 ─────────────────────────────

def capacity36():
    from p8_ch2 import cap
    a = cap('3-6-capacity').axes[0]
    deg = np.array(a.lines[0].get_xdata(), float)
    tr, va = np.array(a.lines[0].get_ydata()), np.array(a.lines[1].get_ydata())
    s = Fig(640, 230)
    ax = s.axes(70, 20, 430, 160, (1, 12), (0, .17), xticks=list(range(1, 13)), yticks=[0, .05, .1, .15], yfmt='{:.2f}', xlabel='bậc đa thức')
    ax.line(deg, tr, BLUE, 2).dots(deg, tr, BLUE, 3).line(deg, va, CLAY, 2.2).dots(deg, va, CLAY, 3)
    s.label(ax.X(12) + 8, ax.Y(tr[-1]), 'train', 12, 'start', BLUE, 600)
    s.label(ax.X(12) + 8, ax.Y(va[-1]), 'validation', 12, 'start', CLAY, 600)
    s.circle(ax.X(2), ax.Y(va[1]), 6.5, TEXT, 'none', 1.3)
    s.line(ax.X(2), ax.Y(va[1]) + 8, ax.X(2.6), ax.Y(.06), FAINT, 1)
    s.label(ax.X(2.7), ax.Y(.065), 'bậc 2: đúng dạng y = x²', 11.5, 'start', MUTED)
    s.label(ax.x - 8, ax.y - 10, 'MSE', 11.5, 'start', FAINT)
    s.save('3-6-capacity', '16 điểm có nhiễu quanh y = x²: tăng bậc đa thức thì train MSE giảm mãi, còn validation MSE thấp nhất ở bậc 2–3 rồi tăng vọt khi model bám cả nhiễu.')


def dropout36():
    h = [1, 2, 3, 4]
    rows = [('h', h, None), ('train, lượt 1', [0, 4, 6, 8], [0, 1, 1, 1]), ('train, lượt 2', [2, 0, 6, 0], [1, 0, 1, 0]), ('eval', h, None)]
    s = Fig(640, 230)
    for r, (nm, v, keep) in enumerate(rows):
        y = 20 + r * 50
        s.label(160, y + 17, nm, 12.5, 'end', TEXT, 600 if r in (0, 3) else 400)
        fills = {}
        if keep:
            fills = {(0, j): ((CLAY, .28) if k else (FAINT, .12)) for j, k in enumerate(keep)}
        s.tiles(180, y, [[str(x) for x in v]], 50, 34, BLUE, 8, fills, size=15)
    s.label(430, 87, '× 1/(1 − p) = × 2', 12, 'start', CLAY, 600)
    s.label(430, 107, 'ô 0: bị bỏ ở lượt này', 12, 'start', MUTED)
    s.label(430, 187, 'không mask, không nhân', 12, 'start', MUTED)
    s.save('3-6-dropout', 'Dropout p = 0.5 trên h = (1, 2, 3, 4), output của code bài: mỗi lượt train bốc một mask mới và nhân phần còn lại với 2; eval giữ nguyên h.')


def earlystop36():
    ns = lesson_ns('3.6', upto=2)
    _, _, hist = ns['fit_small'](0.)
    h = np.array(hist)
    tr, va = h[:, 0], h[:, 1]
    ep = np.arange(1, len(tr) + 1)
    L = np.log10
    b = int(np.argmin(va))
    s = Fig(640, 230)
    ax = s.axes(70, 20, 430, 170, (1, 160), (-2.6, -.6), xticks=[1, 26, 60, 100, 160], xlabel='epoch')
    for e in (-2, -1):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    nm = ns['y_train'] - ns['x_train'] ** 2
    noise = float((nm ** 2).mean())
    ax.hline(L(noise), SAND, 1.2, '4 3')
    ax.line(ep, L(tr), BLUE, 2).line(ep, L(va), CLAY, 2)
    s.line(ax.X(b + 1), ax.y, ax.X(b + 1), ax.y + ax.h, FAINT, 1, '3 3')
    s.circle(ax.X(b + 1), ax.Y(L(va[b])), 4.5, CLAY, PAPER, 2)
    s.label(ax.X(160) + 8, ax.Y(L(tr[-1])) + 8, 'train', 12, 'start', BLUE, 600)
    s.label(ax.X(160) + 8, ax.Y(L(va[-1])), 'validation', 12, 'start', CLAY, 600)
    s.label(ax.X(160) + 8, ax.Y(L(noise)) - 8, 'MSE của nhiễu', 11.5, 'start', SAND)
    s.label(ax.x - 8, ax.y - 10, 'MSE (thang log)', 11.5, 'start', FAINT)
    s.save('3-6-early-stop', 'Mạng nhỏ trên 16 điểm (decay 0, số từ code bài): validation MSE chạm một đáy hẹp ở epoch 26 rồi nhích dần lên; train loss xuống dưới MSE của nhiễu, tức đã khớp một phần nhiễu.')


def patience36():
    vals = [.50, .46, .455, .453, .452, .451]
    s = Fig(640, 210)
    ax = s.axes(80, 30, 420, 130, (.5, 6.5), (.44, .51), xticks=[1, 2, 3, 4, 5, 6], yticks=[.45, .47, .49], yfmt='{:.2f}', xlabel='epoch')
    s.rect(ax.X(.5), ax.Y(.46), ax.w, ax.Y(.45) - ax.Y(.46), 'none', SAND, 0, .12, 0)
    ax.hline(.45, SAND, 1, '4 3')
    ax.line(range(1, 7), vals, TEXT, 1.4)
    for i, v in enumerate(vals, 1):
        col = GREEN if i <= 2 else CLAY
        s.circle(ax.X(i), ax.Y(v), 5, col)
        if 3 <= i <= 5:
            s.mono(ax.X(i), ax.Y(.475), f'lần {i - 2}', 11, 'middle', CLAY)
    s.line(ax.X(5.5), ax.y, ax.X(5.5), ax.y + ax.h, CLAY, 1.2)
    s.label(ax.X(5.5) + 6, ax.y + 8, 'dừng sau epoch 5', 12, 'start', CLAY, 600)
    s.label(ax.X(6.5) + 8, ax.Y(.455), 'vùng chưa đủ', 11.5, 'start', SAND)
    s.label(ax.X(6.5) + 8, ax.Y(.455) + 16, 'min_delta 0.01', 11.5, 'start', SAND)
    s.save('3-6-patience', 'Patience 3, min_delta 0.01: tốt nhất là 0.46 ở epoch 2; ba epoch sau chỉ giảm chưa tới 0.01 (vùng tô) nên được đếm 1, 2, 3 và huấn luyện dừng sau epoch 5.')


def bnstats36():
    s = Fig(640, 220)
    rows = [('batch', [[1, 2], [3, 4]], BLUE), ('train: chia B', [[-1, -1], [1, 1]], GREEN), ('eval: running var chia B − 1', [[-.7071, -.7071], [.7071, .7071]], CLAY)]
    for k_, (nm, M, col) in enumerate(rows):
        x0 = 40 + k_ * 205
        s.label(x0 + 70, 22, nm, 12.5, color=col, weight=600)
        s.tiles(x0 + (10 if k_ < 2 else 0), 40, [[mnum(v, '{:g}') for v in row] for row in M], 60 if k_ < 2 else 70, 34, col, 6, size=14)
    s.mono(110, 136, 'mean (2, 3)', 12, 'middle', MUTED)
    s.mono(110, 156, 'var: B → 1, B − 1 → 2', 12, 'middle', MUTED)
    s.label(320, 200, 'cùng input, khác output: running variance ghi bằng ước lượng chia B − 1', 11.5, color=MUTED)
    s.save('3-6-bn-stats', 'BatchNorm affine=False, momentum=1 trên hai hàng (1, 2) và (3, 4): train chuẩn hóa bằng phương sai chia B (ra ±1); running variance ghi chia B − 1 nên eval ra ±0.707.')


def bndeep36():
    ns = lesson_ns('3.6', upto=4)
    import torch
    x = torch.randn(128, 64, generator=torch.Generator().manual_seed(1))
    curves = {}
    for use_bn in (False, True):
        h, stds = x, []
        for layer in ns['deep_relu'](use_bn):
            h = layer(h)
            if isinstance(layer, torch.nn.ReLU):
                stds.append(h.std().item())
        curves[use_bn] = stds
    L = math.log10
    s = Fig(640, 230)
    ax = s.axes(80, 20, 420, 170, (1, 10), (-14, 1), xticks=list(range(1, 11)), xlabel='lớp')
    for e in range(-14, 1, 2):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    for k, col, nm in [(True, GREEN, 'có BatchNorm'), (False, CLAY, 'không BatchNorm')]:
        v = [L(t) for t in curves[k]]
        ax.line(range(1, 11), v, col, 2.2).dots(range(1, 11), v, col, 3)
        s.label(ax.X(10) + 8, ax.Y(v[-1]), nm, 12, 'start', col, 600)
    s.label(ax.x - 8, ax.y - 10, 'std activation', 11.5, 'start', FAINT)
    s.save('3-6-bn-deep', '10 lớp ReLU rộng 64, khởi tạo N(0, 0.01²) (số từ code bài): không BatchNorm, std co còn cỡ 10⁻¹³; chèn BatchNorm sau mỗi Linear, std giữ quanh 0.58 ở mọi lớp.')


def bnln36():
    s = Fig(640, 220)
    nB, nC = 6, 5
    for k_, (title, axis, col) in enumerate([('BatchNorm: mỗi feature một mean', 0, BLUE), ('LayerNorm: mỗi mẫu một mean', 1, CLAY)]):
        x0 = 70 + k_ * 300
        fills = {}
        for i in range(nB):
            for j in range(nC):
                on = (j == 1) if axis == 0 else (i == 2)
                fills[(i, j)] = (col, .45) if on else (FAINT, .1)
        s.tiles(x0 + 24, 40, [[''] * nC] * nB, 26, 22, col, 4, fills)
        s.label(x0 + 75, 20, title, 12.5, color=col, weight=600)
        s.label(x0 + 75, 202, 'feature →', 11, color=MUTED)
        s.label(x0 + 14, 100, 'mẫu ↓', 11, 'end', MUTED)
    s.save('3-6-bn-ln', 'Trên bảng (mẫu × feature): BatchNorm lấy mean theo cột, gộp qua các mẫu trong batch; LayerNorm lấy mean theo hàng, chỉ trong một mẫu nên không phụ thuộc batch.')


FIGS36 = {'3-6-capacity': capacity36, '3-6-dropout': dropout36, '3-6-early-stop': earlystop36, '3-6-patience': patience36,
          '3-6-bn-stats': bnstats36, '3-6-bn-deep': bndeep36, '3-6-bn-ln': bnln36}


# ───────────────────────────── 3.7 ─────────────────────────────

def overfit37():
    import torch
    from torch import nn
    torch.set_num_threads(1)
    torch.manual_seed(31)
    xb = torch.tensor([[-1., -1.], [-1., 1.], [1., -1.], [1., 1.]])
    yb = torch.tensor([0, 0, 1, 1])
    model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
    opt = torch.optim.Adam(model.parameters(), lr=.05)
    crit = nn.CrossEntropyLoss()
    losses = [crit(model(xb), yb).item()]
    for _ in range(100):
        opt.zero_grad(set_to_none=True)
        l = crit(model(xb), yb)
        l.backward()
        opt.step()
        losses.append(crit(model(xb), yb).item())
    L = math.log10
    s = Fig(640, 210)
    ax = s.axes(80, 20, 420, 150, (0, 100), (-5, .5), xticks=[0, 25, 50, 75, 100], xlabel='bước trên cùng 4 mẫu')
    for e in range(-5, 1):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    ax.line(range(101), [L(v) for v in losses], CLAY, 2.2)
    ax.hline(L(math.log(2)), FAINT, 1, '4 3')
    s.label(ax.X(100) + 8, ax.Y(L(math.log(2))), 'ln 2: đoán đều', 11.5, 'start', MUTED)
    s.label(ax.X(100) + 8, ax.Y(L(losses[-1])), f'{losses[-1]:.1e}', 12, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 10, 'loss', 11.5, 'start', FAINT)
    s.save('3-7-overfit', 'Overfit một batch bốn mẫu (code bài): loss đi từ gần ln 2 xuống cỡ 10⁻⁵ sau 100 bước, chứng tỏ forward, loss, backward và step đã nối đúng.')


def debug37():
    s = Fig(640, 190)
    items = [('xb', 'GPU', BLUE, 40), ('model', 'GPU', BLUE, 170), ('logits', 'GPU', BLUE, 300), ('loss', '', CLAY, 450)]
    for nm, dev, col, x in items:
        s.box(x, 50, 100, 46, 'none', col, r=8, width=0, opacity=.15)
        s.mono(x + 50, 67, nm, 13, 'middle', TEXT, 600)
        if dev:
            s.mono(x + 50, 86, dev, 11, 'middle', MUTED)
    for a, b in [(140, 168), (270, 298), (400, 448)]:
        s.arrow(a, 73, b, 73, LINE, 1.3)
    s.box(450, 132, 100, 40, CLAY, 'none', r=8, width=1.4, dash='4 3')
    s.mono(500, 147, 'yb', 13, 'middle', TEXT, 600)
    s.mono(500, 163, 'CPU', 11, 'middle', CLAY, 600)
    s.arrow(500, 130, 500, 100, CLAY, 1.4)
    s.mono(560, 73, '✗', 18, 'start', CLAY, 600)
    s.label(170, 152, 'forward chạy êm; lỗi chỉ hiện ở phép đầu tiên chạm yb', 12, color=MUTED)
    s.save('3-7-debug', 'Model và xb đã ở GPU nên forward chạy được; target yb còn ở CPU nên lỗi device chỉ hiện ra ở dòng tính loss.')


def memory37():
    s = Fig(640, 200)
    rows = [('SGD', [('θ', BLUE), ('∇θ', CLAY)]), ('SGD momentum', [('θ', BLUE), ('∇θ', CLAY), ('v', SAND)]),
            ('Adam', [('θ', BLUE), ('∇θ', CLAY), ('m', SAND), ('v', GREEN)])]
    u = 70
    for r, (nm, parts) in enumerate(rows):
        y = 34 + r * 48
        s.label(150, y + 15, nm, 12.5, 'end', TEXT)
        for k, (lab, col) in enumerate(parts):
            s.box(170 + k * u, y, u - 4, 30, 'none', col, r=5, width=0, opacity=.25)
            s.mono(170 + k * u + (u - 4) / 2, y + 15.5, lab, 12.5, 'middle', TEXT)
        s.mono(170 + len(parts) * u + 8, y + 15.5, f'{4 * len(parts)} B', 13, 'start', TEXT, 600)
    s.label(320, 186, 'mỗi ô 4 byte (FP32), tính cho một tham số; activation tính riêng', 11.5, color=MUTED)
    s.save('3-7-memory', 'Mỗi tham số FP32 cần 4 byte cho trọng số, 4 cho gradient, cộng trạng thái optimizer: SGD 8 byte, SGD momentum 12, Adam 16.')


def attention37():
    s = Fig(640, 180)
    for r, (L, mib) in enumerate([(1024, 512), (512, 128)]):
        y = 40 + r * 56
        w = mib * .75
        s.rect(160, y, w, 32, 'none', CLAY, 4, .7, 0)
        s.mono(150, y + 16, f'L = {L}', 12.5, 'end', TEXT)
        s.mono(160 + w + 8, y + 16, f'{mib} MiB', 12.5, 'start', TEXT, 600)
    s.label(320, 166, 'score (16, 8, L, L) FP32: L giảm một nửa, bộ nhớ giảm bốn lần', 11.5, color=MUTED)
    s.save('3-7-attention', 'Tensor attention score (16, 8, L, L) ở FP32: 512 MiB với L = 1024 nhưng chỉ 128 MiB với L = 512, vì kích thước tỉ lệ với L².')


def accum37():
    s = Fig(640, 220)
    for k in range(4):
        x = 40 + k * 110
        s.box(x, 40, 90, 34, 'none', BLUE, r=6, width=0, opacity=.18)
        s.mono(x + 45, 57.5, '8 mẫu', 12, 'middle', TEXT)
        s.arrow(x + 45, 78, x + 45, 104, MUTED, 1.2)
        s.mono(x + 45, 118, 'loss / 4', 11.5, 'middle', CLAY)
        s.mono(x + 45, 136, 'backward', 11.5, 'middle', MUTED)
    s.line(85, 150, 415, 150, LINE, 1.2)
    s.arrow(250, 150, 250, 172, MUTED, 1.2)
    s.box(190, 174, 120, 30, 'none', CLAY, r=6, width=0, opacity=.18)
    s.mono(250, 189.5, '.grad cộng dồn', 11.5, 'middle', TEXT)
    s.arrow(314, 189, 380, 189, MUTED, 1.2)
    s.mono(386, 189.5, 'step × 1', 12.5, 'start', TEXT, 600)
    s.mono(500, 60, 'chia 4: tỉ lệ 1.0', 12.5, 'start', GREEN, 600)
    s.mono(500, 82, 'không chia: 4.0', 12.5, 'start', CLAY, 600)
    s.label(500, 104, 'so với gradient batch 32', 11.5, 'start', MUTED)
    s.save('3-7-accum', 'Gradient accumulation: bốn microbatch 8 mẫu, mỗi cái backward với loss chia 4, .grad cộng dồn rồi mới step một lần; kết quả trùng gradient của batch 32.')


def fp16_37():
    s = Fig(640, 190)
    L = math.log10
    X = lambda e: 60 + (e + 10) / 16 * 520
    s.rect(X(L(6e-8)), 60, X(L(65504)) - X(L(6e-8)), 40, 'none', BLUE, 6, .12, 0)
    s.label((X(L(6e-8)) + X(L(65504))) / 2, 46, 'khoảng FP16 biểu diễn được', 12, color=BLUE, weight=600)
    for e in range(-10, 7, 2):
        s.label(X(e), 118, f'10{sup(e)}', 11, color=FAINT)
    s.line(X(-10), 100, X(6), 100, LINE, 1)
    s.circle(X(-8), 80, 6, CLAY)
    s.mono(X(-8), 140, '1e-8 → 0', 12, 'middle', CLAY, 600)
    s.curve(X(-8), 72, X(L(6.55e-4)), 72, -.25, MUTED, 1.4)
    s.circle(X(L(6.55e-4)), 80, 6, GREEN)
    s.mono(X(L(6.55e-4)), 140, '× 65536 = 6.55e-4', 12, 'middle', GREEN, 600)
    s.save('3-7-fp16', 'Gradient 10⁻⁸ nằm dưới số dương nhỏ nhất của FP16 nên thành 0; GradScaler nhân 65536 đưa nó vào khoảng biểu diễn được (6.55·10⁻⁴), rồi chia lại ở FP32.')


def budget37():
    s = Fig(640, 160)
    u = 26
    s.rect(60, 50, 15.6 * u, 34, 'none', BLUE, 4, .7, 0)
    s.mono(60 + 15.6 * u / 2, 67, 'train 15.6 phút', 12, 'middle', PAPER, 600)
    s.rect(60 + 15.6 * u, 50, 5 * u, 34, 'none', CLAY, 4, .7, 0)
    s.mono(60 + 18.1 * u, 67, 'val 5', 12, 'middle', PAPER, 600)
    s.line(60 + 20 * u, 34, 60 + 20 * u, 100, TEXT, 1.6)
    s.label(60 + 20 * u - 6, 26, 'ngân sách 20 phút', 12, 'end', TEXT, 600)
    for m in (0, 5, 10, 15, 20):
        s.mono(60 + m * u, 112, str(m), 11, 'middle', FAINT)
    s.label(60 + 20.6 * u + 8, 67, '20.6', 12, 'start', CLAY, 600)
    s.label(320, 142, '20 epoch × 391 step × 0.12 s, cộng 20 lần validation 15 s', 11.5, color=MUTED)
    s.save('3-7-budget', 'Ước lượng ngân sách: train 20 × 391 × 0.12 s ≈ 15.6 phút, cộng validation 5 phút đã vượt 20 phút trước khi tính đọc dữ liệu và checkpoint.')


FIGS37 = {'3-7-overfit': overfit37, '3-7-debug': debug37, '3-7-memory': memory37, '3-7-attention': attention37,
          '3-7-accum': accum37, '3-7-fp16': fp16_37, '3-7-budget': budget37}


# ───────────────────────────── 3.8 ─────────────────────────────

NAMES38 = {0: 'PAD', 1: 'UNK', 2: 'đồ_thị', 3: 'dp', 4: 'toán'}


def padding38():
    ids = [[2, 3, 0], [3, 0, 0], [4, 2, 3]]
    s = Fig(640, 200)
    s.label(140, 18, 'ids (3, 3)', 12.5, color=TEXT, weight=600)
    fills = {(i, j): ((FAINT, .12) if v == 0 else (BLUE, .18)) for i, r in enumerate(ids) for j, v in enumerate(r)}
    s.tiles(40, 32, [[NAMES38[v] for v in r] for r in ids], 66, 34, BLUE, 4, fills, size=12)
    s.arrow(256, 87, 300, 87, MUTED, 1.4)
    s.label(390, 18, 'mask = ids ≠ PAD', 12.5, color=TEXT, weight=600)
    fm = {(i, j): ((FAINT, .12) if v == 0 else (GREEN, .22)) for i, r in enumerate(ids) for j, v in enumerate(r)}
    s.tiles(320, 32, [[('1' if v else '0') for v in r] for r in ids], 40, 34, GREEN, 4, fm, size=14)
    s.label(500, 50, 'độ dài 2', 12, 'start', MUTED)
    s.label(500, 88, 'độ dài 1', 12, 'start', MUTED)
    s.label(500, 126, 'độ dài 3', 12, 'start', MUTED)
    s.label(320, 182, 'bảng rộng bằng câu dài nhất trong batch; ô xám là PAD', 11.5, color=MUTED)
    s.save('3-8-padding', 'Ba câu của bài sau pad_sequence thành bảng (3, 3); mask đánh dấu 1 ở token thật, nên tổng mỗi hàng chính là độ dài câu.')


def lookup38():
    table = [[0, 0], [1, 1], [2, 0], [0, 4], [2, 2]]
    s = Fig(640, 220)
    s.label(110, 18, 'embedding.weight (5, 2)', 12.5, color=TEXT, weight=600)
    for i, (row, nm) in enumerate(zip(table, ['PAD', 'UNK', 'đồ_thị', 'dp', 'toán'])):
        y = 34 + i * 34
        hl = i in (2, 3)
        s.mono(56, y + 15, f'{i} {nm}', 11.5, 'end', CLAY if hl else MUTED)
        s.tiles(66, y, [[str(v) for v in row]], 44, 28, CLAY if hl else BLUE, 4, None, size=13, opacity=.28 if hl else .12)
    s.label(330, 72, 'ids[0] = (2, 3, 0)', 12.5, color=TEXT)
    s.arrow(250, 92, 410, 92, MUTED, 1.4)
    s.label(330, 112, 'tra theo hàng', 11.5, color=MUTED)
    s.label(520, 18, 'vectors[0] (3, 2)', 12.5, color=TEXT, weight=600)
    s.tiles(470, 34, [['2', '0'], ['0', '4'], ['0', '0']], 44, 28, CLAY, 4, {(2, 0): (FAINT, .12), (2, 1): (FAINT, .12)}, size=13, opacity=.28)
    s.label(320, 206, 'ID là địa chỉ hàng, không phải độ lớn', 11.5, color=MUTED)
    s.save('3-8-lookup', 'Bảng embedding đặt tay của bài: câu đầu (2, 3, PAD) tra ra ba hàng của bảng, nên vectors có thêm chiều cuối d = 2.')


def space38():
    vec = {'đồ_thị': (2, 0), 'dp': (0, 4), 'toán': (2, 2)}
    sent = [('câu 1', (1, 2), 'đồ_thị dp'), ('câu 2', (0, 4), 'dp'), ('câu 3', (4 / 3, 2), 'toán đồ_thị dp')]
    s = Fig(640, 290)
    ax = s.axes(170, 16, 300, 260, (-1.6, 3.4), (-.2, 4.33), frame=False, grid=False)
    s.line(ax.X(2), ax.Y(0), ax.X(0), ax.Y(4), FAINT, 1, '4 3')
    for nm, (a, b) in vec.items():
        s.circle(ax.X(a), ax.Y(b), 6, BLUE)
        s.label(ax.X(a) + 10, ax.Y(b) + (-12 if nm == 'toán' else 2 if nm == 'dp' else -10), nm, 12.5, 'start', BLUE, 600)
    s.circle(ax.X(1), ax.Y(2), 6, CLAY, PAPER, 2)
    s.mono(ax.X(1) - 10, ax.Y(2) - 12, 'câu 1 (1, 2)', 11.5, 'end', CLAY)
    s.circle(ax.X(4 / 3), ax.Y(2), 6, GREEN, PAPER, 2)
    s.mono(ax.X(4 / 3) + 4, ax.Y(2) + 22, 'câu 3 (1.33, 2)', 11.5, 'start', GREEN)
    s.circle(ax.X(2 / 3), ax.Y(4 / 3), 5, MUTED, PAPER, 1.6)
    s.mono(ax.X(2 / 3) - 10, ax.Y(4 / 3) + 4, 'mean ngây thơ', 11.5, 'end', MUTED)
    s.save('3-8-space', 'Vector token đặt tay trong mặt phẳng: câu 1 là trung điểm của đồ_thị và dp; mean ngây thơ chia cho 3 ô (tính cả PAD) kéo điểm về phía gốc.')


def pooling38():
    s = Fig(640, 200)
    s.label(60, 18, 'm', 12.5, color=TEXT, weight=600)
    s.tiles(44, 34, [['1'], ['1'], ['0']], 32, 30, GREEN, 4, {(2, 0): (FAINT, .12)}, size=13, opacity=.22)
    s.label(150, 18, 'vectors[0]', 12.5, color=TEXT, weight=600)
    s.tiles(104, 34, [['2', '0'], ['0', '4'], ['0', '0']], 44, 30, BLUE, 4, {(2, 0): (FAINT, .12), (2, 1): (FAINT, .12)}, size=13)
    s.arrow(208, 82, 250, 82, MUTED, 1.4)
    s.mono(229, 70, 'Σ', 13, 'middle', MUTED)
    s.tiles(258, 66, [['2', '4']], 44, 30, CLAY, 4, size=13, opacity=.2)
    for r, (op, res, col, lab) in enumerate([('÷ 2 token thật', ['1', '2'], GREEN, 'masked mean'), ('÷ 3 ô', ['0.67', '1.33'], MUTED, 'mean ngây thơ')]):
        y = 40 + r * 60
        s.arrow(356, 82, 400, y + 15, MUTED, 1.2)
        s.tiles(410, y, [res], 50, 30, col, 4, size=13, opacity=.22)
        s.label(522, y + 8, lab, 12.5, 'start', col, 600)
        s.mono(522, y + 26, op, 11.5, 'start', MUTED)
    s.save('3-8-pooling', 'Masked mean của câu đầu: cộng vector theo mask được (2, 4), chia cho 2 token thật ra (1, 2); chia cho cả 3 ô thì ra (0.67, 1.33).')


def rnnpad38():
    s = Fig(640, 200)
    xs = [190, 320, 450]
    for k, (x, tok) in enumerate(zip(xs, ['dp', 'PAD', 'PAD'])):
        col = CLAY if k == 0 else FAINT
        s.circle(x, 80, 24, col, SURFACE, 1.6)
        s.mono(x, 80.5, f'h{"₁₂₃"[k]}', 14, 'middle', TEXT)
        s.box(x - 32, 136, 64, 30, 'none', BLUE if k == 0 else FAINT, r=6, width=0, opacity=.16)
        s.mono(x, 151.5, tok, 12.5, 'middle', TEXT)
        s.arrow(x, 134, x, 108, MUTED, 1.2)
        if k:
            s.arrow(xs[k - 1] + 26, 80, x - 26, 80, LINE, 1.3)
    s.mono(80, 80.5, 'h₀ = 0', 13, 'middle', MUTED)
    s.arrow(110, 80, 164, 80, LINE, 1.3)
    s.mono(190, 30, 'lengths − 1', 12, 'middle', CLAY, 600)
    s.arrow(190, 38, 190, 54, CLAY, 1.3)
    s.mono(450, 30, 'outputs[:, −1]', 12, 'middle', MUTED)
    s.arrow(450, 38, 450, 54, MUTED, 1.3)
    s.label(500, 80, 'vẫn đổi qua PAD', 11.5, 'start', MUTED)
    s.save('3-8-rnn-pad', 'Câu “dp” dài 1 trong bảng rộng 3: trạng thái cần đọc là h₁; cột cuối h₃ đã đi qua hai bước PAD và vẫn bị W_hh, bias làm đổi.')


def vanish38():
    ns = lesson_ns('3.8', upto=8)
    g = ns['grad_norm'].numpy().astype(float)
    L = np.log10
    s = Fig(640, 220)
    ax = s.axes(80, 20, 420, 160, (1, 40), (-10.5, .5), xticks=[1, 10, 20, 30, 40], xlabel='vị trí token t')
    for e in range(-10, 1, 2):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    ax.line(range(1, 41), L(g), CLAY, 2).dots(range(1, 41), L(g), CLAY, 2.4)
    s.label(ax.X(40) + 8, ax.Y(L(g[-1])), f'{g[-1]:.2f}', 12, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 10, '‖∂h₄₀/∂xₜ‖', 11.5, 'start', FAINT)
    s.save('3-8-vanish', 'RNN của bài trên chuỗi dài 40 (số từ code): độ lớn gradient của trạng thái cuối theo từng token giảm hai đến ba bậc mỗi mười bước, token đầu chỉ còn cỡ 10⁻¹⁰.')


def lstm38():
    s = Fig(640, 180)
    xs = [80, 230, 380]
    for k, x in enumerate(xs):
        s.circle(x, 70, 22, CLAY, SURFACE, 1.6)
        s.mono(x, 70.5, f'c{"₁₂₃"[k]}', 14, 'middle', TEXT)
        if k:
            s.arrow(xs[k - 1] + 24, 70, x - 24, 70, CLAY, 1.8)
            s.mono((xs[k - 1] + x) / 2, 58, '× f', 12, 'middle', CLAY, 600)
            s.mono((xs[k - 1] + x) / 2, 112, '+ i ⊙ c̃', 11.5, 'middle', MUTED)
            s.arrow((xs[k - 1] + x) / 2, 100, (xs[k - 1] + x) / 2 + 10, 76, MUTED, 1)
    s.arrow(406, 70, 450, 70, CLAY, 1.8)
    s.label(466, 64, 'f ≈ 1: gradient đi qua', 12, 'start', TEXT, 600)
    s.label(466, 82, 'gần nguyên vẹn', 12, 'start', MUTED)
    s.label(320, 156, 'đường cell state chỉ nhân với cổng quên, không nhân W_hh và tanh′ mỗi bước', 11.5, color=MUTED)
    s.save('3-8-lstm', 'Cell state của LSTM: từ c₁ tới c₃ chỉ nhân với cổng quên f rồi cộng nội dung mới, nên khi f gần 1 gradient đi qua nhiều bước mà không tắt dần.')


FIGS38 = {'3-8-padding': padding38, '3-8-lookup': lookup38, '3-8-space': space38, '3-8-pooling': pooling38,
          '3-8-rnn-pad': rnnpad38, '3-8-vanish': vanish38, '3-8-lstm': lstm38}


# ───────────────────────────── 3.9 ─────────────────────────────

def attention39():
    a1, a2 = math.e / (math.e + 1), 1 / (math.e + 1)
    s = Fig(640, 220)
    s.label(40, 22, 'q = [1]', 12.5, 'start', TEXT, 600)
    rows = [('k₁ = [1]', 1, a1, '[2, 0]', BLUE), ('k₂ = [0]', 0, a2, '[0, 4]', CLAY)]
    for r, (k, sc, w, v, col) in enumerate(rows):
        y = 60 + r * 70
        s.mono(40, y, k, 12.5, 'start', TEXT)
        s.mono(150, y, f'score {sc}', 12, 'start', MUTED)
        s.arrow(230, y, 262, y, LINE, 1.2)
        s.rect(272, y - 11, 120 * w, 22, 'none', col, 3, .7, 0)
        s.mono(272 + 120 * w + 8, y, f'{w:.3f}', 12, 'start', col, 600)
        s.mono(440, y, f'× v = {v}', 12, 'start', MUTED)
    s.label(272, 22, 'softmax', 12, 'start', MUTED)
    s.line(430, 175, 600, 175, LINE, 1)
    s.mono(440, 196, 'output = [1.462, 1.076]', 13, 'start', TEXT, 600)
    s.save('3-9-attention', 'Ví dụ tính tay: score 1 và 0 qua softmax thành 0.731 và 0.269, rồi trộn hai value (2, 0) và (0, 4) thành (1.462, 1.076).')


def scale39():
    dks = [4, 64, 1024]
    raw = [.524, .878, .968]
    scaled = [.342, .360, .358]
    s = Fig(640, 210)
    ax = s.axes(120, 20, 400, 140, (-.5, 2.5), (0, 1), yticks=[0, .125, .5, 1], frame=True, grid=True)
    for i, (d, r_, sc) in enumerate(zip(dks, raw, scaled)):
        for j, (v, col) in enumerate([(r_, CLAY), (sc, BLUE)]):
            x = ax.X(i) + (-26 if j == 0 else 4)
            s.rect(x, ax.Y(v), 22, ax.Y(0) - ax.Y(v), 'none', col, 3, .75, 0)
            s.mono(x + 11, ax.Y(v) - 9, f'{v:.2f}', 10.5, 'middle', col)
        s.mono(ax.X(i), ax.y + ax.h + 16, f'd_k = {d}', 11.5, 'middle', MUTED)
    s.label(ax.X(2.5) + 8, ax.Y(.9), 'không chia', 12, 'start', CLAY, 600)
    s.label(ax.X(2.5) + 8, ax.Y(.32), 'chia √d_k', 12, 'start', BLUE, 600)
    s.label(ax.X(2.5) + 8, ax.Y(.125), 'chia đều: 1/8', 11.5, 'start', FAINT)
    s.label(ax.x - 8, ax.y - 10, 'trọng số lớn nhất (TB)', 11.5, 'start', FAINT)
    s.save('3-9-scale', 'Thí nghiệm của bài (8 key mỗi query): không chia √d_k, key mạnh nhất chiếm 0.52 → 0.97 trọng số khi d_k tăng; có chia, giữ quanh 0.35 ở mọi độ rộng.')


def heads39():
    ns = lesson_ns('3.9', upto=4)
    w = ns['attn'][0].numpy().astype(float)
    s = Fig(640, 210)
    labs = ['t1', 't2', 'PAD']
    for h in range(2):
        x0 = 90 + h * 260
        s.label(x0 + 66, 18, f'head {h + 1}', 13, color=TEXT, weight=600)
        fills = {(i, j): (CLAY, float(max(.04, w[h, i, j] * .9))) for i in range(3) for j in range(3)}
        s.tiles(x0, 34, [[f'{w[h, i, j]:.2f}' for j in range(3)] for i in range(3)], 44, 36, CLAY, 4, fills, size=12)
        for j, l in enumerate(labs):
            s.mono(x0 + j * 48 + 22, 162, l, 11, 'middle', MUTED)
        for i, l in enumerate(labs):
            s.mono(x0 - 8, 52 + i * 40, l, 11, 'end', MUTED)
    s.label(320, 192, 'hàng: query · cột: key · cột PAD bằng 0 ở cả hai head', 11.5, color=MUTED)
    s.save('3-9-heads', 'Trọng số attention thật của TinyEncoder (mẫu đầu, 2 head): mỗi head có phân phối riêng, mỗi hàng cộng bằng 1, cột PAD bằng 0 nhờ key_padding_mask.')


def masks39():
    s = Fig(640, 220)
    L = 4
    panels = [('padding mask', lambda i, j: j < 3), ('causal mask', lambda i, j: j <= i), ('cả hai', lambda i, j: j <= i and j < 3)]
    for k_, (title, ok) in enumerate(panels):
        x0 = 50 + k_ * 200
        fills = {(i, j): ((BLUE, .45) if ok(i, j) else (FAINT, .1)) for i in range(L) for j in range(L)}
        s.tiles(x0, 40, [[''] * L] * L, 30, 30, BLUE, 4, fills)
        s.label(x0 + 66, 20, title, 12.5, color=TEXT, weight=600)
        for j in range(L):
            s.mono(x0 + j * 34 + 15, 184, 'PAD' if j == 3 and k_ != 1 else str(j + 1), 10.5, 'middle', MUTED)
    s.label(320, 206, 'hàng: query · cột: key · ô tô: được đọc', 11.5, color=MUTED)
    s.save('3-9-masks', 'Các key mỗi query được đọc (ô tô) trong câu 3 token và một PAD: padding mask bỏ cột PAD, causal mask bỏ tương lai, dùng cùng lúc thì bỏ cả hai.')


def maskflow39():
    sc = [1., 0., 2.]
    sm = np.exp([1, 0]) / np.exp([1, 0]).sum()
    s = Fig(640, 210)
    cols = [('score', ['1', '0', '2'], BLUE), ('sau mask', ['1', '0', '−∞'], CLAY), ('softmax', [f'{sm[0]:.3f}', f'{sm[1]:.3f}', '0'], GREEN)]
    for k_, (title, vals, col) in enumerate(cols):
        x0 = 70 + k_ * 190
        fills = {(2, 0): (FAINT, .14)} if k_ else None
        s.tiles(x0, 40, [[v] for v in vals], 80, 36, col, 6, fills, size=14)
        s.label(x0 + 40, 22, title, 12.5, color=TEXT, weight=600)
        if k_:
            s.arrow(x0 - 100, 98, x0 - 10, 98, MUTED, 1.3)
    s.mono(40, 141, 'key 3', 11.5, 'end', MUTED)
    s.label(320, 198, 'cấm trước softmax: hai key còn lại tự chia lại tổng 1', 11.5, color=MUTED)
    s.save('3-9-mask-flow', 'Key thứ ba bị cấm: đặt score thành −∞ trước softmax, nên trọng số của nó bằng 0 và hai key còn lại nhận 0.731 và 0.269, tổng vẫn bằng 1.')


def encoder39():
    s = Fig(640, 190)
    boxes = [('x', None), ('attention', BLUE), ('+ x', None), ('LayerNorm', SAND), ('FFN', CLAY), ('+', None), ('LayerNorm', SAND)]
    xs = [30, 100, 210, 280, 390, 480, 540]
    ws = [40, 96, 50, 96, 76, 40, 96]
    for (nm, col), x, w in zip(boxes, xs, ws):
        if col:
            s.box(x, 60, w, 40, 'none', col, r=8, width=0, opacity=.18)
        s.mono(x + w / 2, 80.5, nm, 12, 'middle', TEXT, 600 if col else 400)
    for i in range(len(xs) - 1):
        s.arrow(xs[i] + ws[i] + 2, 80, xs[i + 1] - 2, 80, LINE, 1.2)
    s.path('M 50,66 L 50,36 L 235,36', MUTED, 1.2)
    s.arrow(235, 36, 235, 68, MUTED, 1.2)
    s.path('M 382,94 L 382,124 L 500,124', MUTED, 1.2)
    s.arrow(500, 124, 500, 92, MUTED, 1.2)
    s.label(142, 26, 'residual', 11.5, color=MUTED)
    s.label(441, 138, 'residual', 11.5, color=MUTED)
    s.label(320, 176, 'post-norm: norm(x + attention(x)) rồi norm(x + FFN(x)); shape (B, L, d) giữ nguyên', 11.5, color=MUTED)
    s.save('3-9-encoder', 'Encoder block của bài (post-norm): attention trộn ngữ cảnh, cộng residual rồi LayerNorm; FFN biến đổi từng vị trí, lại cộng residual rồi LayerNorm.')


def pe39():
    P, d = 48, 16
    pos = np.arange(P)[:, None]
    i = np.arange(0, d, 2)
    freq = np.exp(-np.log(10000.) * i / d)
    pe = np.zeros((P, d))
    pe[:, 0::2] = np.sin(pos * freq)
    pe[:, 1::2] = np.cos(pos * freq)
    s = Fig(640, 230)
    cw, ch = 8, 9
    x0, y0 = 110, 30
    paths = {BLUE: [], CLAY: []}
    for p in range(P):
        for j in range(d):
            v = pe[p, j]
            col = BLUE if v >= 0 else CLAY
            s.rect(x0 + p * cw, y0 + j * ch, cw, ch, 'none', col, 0, abs(v) * .85, 0)
    s.box(x0, y0, P * cw, d * ch, SOFT_LINE, 'none', r=2, width=.8)
    s.label(x0 + P * cw / 2, y0 + d * ch + 18, 'vị trí p = 0 … 47', 11.5, color=MUTED)
    s.label(x0 - 10, y0 + 6, 'tần số cao', 11, 'end', MUTED)
    s.label(x0 - 10, y0 + d * ch - 6, 'tần số thấp', 11, 'end', MUTED)
    s.label(x0 + P * cw + 12, y0 + 30, 'xanh: dương', 11.5, 'start', BLUE)
    s.label(x0 + P * cw + 12, y0 + 50, 'cam: âm', 11.5, 'start', CLAY)
    s.save('3-9-pe', 'Positional encoding sin/cos với d = 16 cho 48 vị trí: các chiều đầu dao động nhanh, chiều sau dao động chậm, nên mỗi vị trí có một mẫu riêng.')


def cost39():
    L = np.array([128, 256, 512, 1024, 2048])
    s = Fig(640, 200)
    for i, l in enumerate(L):
        y = 24 + i * 30
        w = l * l / 2048 ** 2 * 380
        s.rect(150, y, max(w, 1.5), 22, 'none', CLAY, 3, .7, 0)
        s.mono(140, y + 11, f'L = {l}', 12, 'end', TEXT)
        s.mono(150 + max(w, 1.5) + 8, y + 11, f'{l * l / 1e6:.2f} triệu ô', 11.5, 'start', MUTED)
    s.label(320, 186, 'số ô score L × L của một head, một câu: L gấp đôi thì gấp bốn', 11.5, color=MUTED)
    s.save('3-9-cost', 'Số ô của ma trận score L × L: từ 128 lên 2048 token, độ dài gấp 16 nhưng số ô gấp 256.')


FIGS39 = {'3-9-attention': attention39, '3-9-scale': scale39, '3-9-heads': heads39, '3-9-masks': masks39,
          '3-9-mask-flow': maskflow39, '3-9-encoder': encoder39, '3-9-pe': pe39, '3-9-cost': cost39}


# ───────────────────────────── 3.10 ─────────────────────────────

def bottleneck310():
    s = Fig(640, 210)
    cols = [(110, 4, 'x', BLUE), (320, 1, 'z', CLAY), (530, 4, 'x̂', BLUE)]
    pos = {}
    for x, n, nm, col in cols:
        ys = [100 + (i - (n - 1) / 2) * 36 for i in range(n)]
        pos[nm] = (x, ys)
        s.mono(x, 24, nm, 15, 'middle', TEXT, 600)
    for a, b in [('x', 'z'), ('z', 'x̂')]:
        for ya in pos[a][1]:
            for yb in pos[b][1]:
                s.line(pos[a][0] + 9, ya, pos[b][0] - 9, yb, SOFT_LINE, 1)
    for x, n, nm, col in cols:
        for y in pos[nm][1]:
            s.circle(x, y, 9 if n > 1 else 12, col, SURFACE, 1.6)
    s.label(215, 176, 'encoder 4 → 1', 12.5, color=MUTED)
    s.label(425, 176, 'decoder 1 → 4', 12.5, color=MUTED)
    s.label(110, 196, '4 cảm biến', 11.5, color=FAINT)
    s.label(530, 196, 'dựng lại 4 số', 11.5, color=FAINT)
    s.save('3-10-bottleneck', 'Autoencoder 4 → 1 → 4 của bài: encoder nén bốn cảm biến thành một số z, decoder dựng lại bốn số từ z.')


def recon310():
    s = Fig(640, 240)
    ax = s.axes(170, 14, 300, 210, (-.4, 3.6), (-.4, 2.4 * 1.0), frame=False, grid=False)
    ax.ylim = (-.4, -.4 + 4 * 210 / 300)
    s.line(ax.X(-.4), ax.Y(-.4), ax.X(2.4), ax.Y(2.4), BLUE, 2)
    s.label(ax.X(2.4) + 6, ax.Y(2.4), 'x₂ = x₁', 12, 'start', BLUE, 600)
    pts = [((1, 1), (1, 1), GREEN, '[1, 1]: lỗi 0'), ((.9, .1), (.5, .5), CLAY, '[0.9, 0.1]: lỗi 0.16'), ((2.2, 2.2), (2.2, 2.2), GREEN, '[2.2, 2.2]: xa gốc, vẫn lỗi 0')]
    for (p, q, col, lab) in pts:
        if p != q:
            s.line(ax.X(p[0]), ax.Y(p[1]), ax.X(q[0]), ax.Y(q[1]), col, 1.4, '4 3')
            s.circle(ax.X(q[0]), ax.Y(q[1]), 5, col, PAPER, 1.8)
        s.circle(ax.X(p[0]), ax.Y(p[1]), 5.5, col)
    s.label(ax.X(1) - 12, ax.Y(1) - 2, '[1, 1]: lỗi 0', 12, 'end', GREEN, 600)
    s.label(ax.X(.9) + 12, ax.Y(.1) + 4, '[0.9, 0.1] → [0.5, 0.5]: lỗi 0.16', 12, 'start', CLAY, 600)
    s.label(ax.X(2.2) - 12, ax.Y(2.2) - 2, '[2.2, 2.2]: xa gốc, lỗi vẫn 0', 12, 'end', GREEN, 600)
    s.save('3-10-reconstruction', 'Encoder (x₁ + x₂)/2, decoder (z, z) chiếu mọi điểm lên đường x₂ = x₁: điểm lệch khỏi đường có lỗi tái tạo, điểm nằm trên đường thì lỗi 0 dù xa gốc đến đâu.')


def ae_curve310():
    import torch
    ns = lesson_ns('3.10', upto=2)
    train = ns['train']
    torch.manual_seed(43)
    ae = ns['LinearAutoencoder']() if 'LinearAutoencoder' in ns else None
    if ae is None:
        from torch import nn

        class LinearAutoencoder(nn.Module):
            def __init__(self):
                super().__init__()
                self.encoder = nn.Linear(4, 1, bias=False)
                self.decoder = nn.Linear(1, 4, bias=False)

            def forward(self, x):
                return self.decoder(self.encoder(x))
        ae = LinearAutoencoder()
    opt = torch.optim.Adam(ae.parameters(), lr=.03)
    hist = [(ae(train) - train).square().mean().item()]
    for _ in range(300):
        opt.zero_grad(set_to_none=True)
        loss = (ae(train) - train).square().mean()
        loss.backward()
        opt.step()
        with torch.no_grad():
            hist.append((ae(train) - train).square().mean().item())
    L = math.log10
    s = Fig(640, 220)
    ax = s.axes(80, 20, 420, 160, (0, 300), (-3.2, 0), xticks=[0, 100, 200, 300], xlabel='bước Adam')
    for e in (-3, -2, -1, 0):
        s.line(ax.x, ax.Y(e), ax.x + ax.w, ax.Y(e), SOFT_LINE, .8)
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    ax.hline(L(.001006), GREEN, 1.4, '5 4')
    ax.line(range(301), [L(v) for v in hist], CLAY, 2.2)
    s.label(ax.X(300) + 8, ax.Y(L(.001006)) + 10, 'cận dưới PCA 0.001006', 11.5, 'start', GREEN, 600)
    s.label(ax.X(300) + 8, ax.Y(L(hist[-1])) - 8, f'AE {hist[-1]:.6f}', 11.5, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 10, 'train MSE', 11.5, 'start', FAINT)
    s.save('3-10-ae-pca', 'Linear autoencoder 4 → 1 → 4 của bài: train MSE giảm từ 0.228 xuống sát cận dưới PCA 0.001006 sau 300 bước, không bao giờ xuống dưới mức đó.')


def errors310():
    ns = lesson_ns('3.10', upto=4)
    err = ns['test_error'].numpy().astype(float)
    thr = ns['threshold']
    lab = ns['test_labels'].numpy()
    L = np.log10
    s = Fig(640, 200)
    ax = s.axes(130, 20, 440, 120, (-4.6, -.6), (0, 2), frame=False, grid=False)
    s.line(ax.x, ax.y + ax.h, ax.x + ax.w, ax.y + ax.h, LINE, 1)
    for e in range(-4, 0):
        s.label(ax.X(e), ax.y + ax.h + 14, f'10{sup(e)}', 11, color=FAINT)
    s.label(ax.X(-.6), ax.y + ax.h + 30, 'lỗi tái tạo (thang log)', 11.5, 'end', FAINT)
    for c_, y, col, nm in [(0, 1.5, BLUE, 'bình thường'), (1, .5, CLAY, 'bất thường')]:
        k = lab == c_
        jj = jit(k.sum(), 11 + c_, 12)
        for e_, j in zip(err[k], jj):
            s.circle(ax.X(L(e_)), ax.Y(y) + j, 3, col, None, 0, .8)
        s.label(ax.x - 12, ax.Y(y), nm, 12.5, 'end', col, 600)
    s.line(ax.X(L(thr)), ax.y - 4, ax.X(L(thr)), ax.y + ax.h, SAND, 1.6, '5 4')
    s.label(ax.X(L(thr)), ax.y - 10, f'ngưỡng {thr:.4f}', 11.5, color=SAND, weight=600)
    s.label(320, 192, 'TP 16 · FP 2 · FN 0', 12, color=TEXT)
    s.save('3-10-errors', 'Lỗi tái tạo của 48 mẫu test (số từ code bài, thang log); vạch đứt là ngưỡng phân vị 95% của validation. Nhóm bất thường nằm xa ngưỡng hơn một bậc độ lớn; hai mẫu bình thường vượt ngưỡng là hai FP.')


def denoise310():
    rng = np.random.default_rng(3)
    t = np.linspace(-1.6, 1.6, 9)
    u = np.array([1, .6]) / np.linalg.norm([1, .6])
    clean = t[:, None] * u
    noisy = clean + rng.normal(0, .28, clean.shape)
    proj = (noisy @ u)[:, None] * u
    s = Fig(640, 240)
    ax = s.axes(170, 14, 300, 212, (-2, 2), (-1.42, 1.42), frame=False, grid=False)
    s.line(ax.X(-2 * u[0]), ax.Y(-2 * u[1]), ax.X(2 * u[0]), ax.Y(2 * u[1]), BLUE, 2)
    for a, b in zip(noisy, proj):
        s.line(ax.X(a[0]), ax.Y(a[1]), ax.X(b[0]), ax.Y(b[1]), FAINT, 1, '3 3')
        s.circle(ax.X(a[0]), ax.Y(a[1]), 4.5, CLAY)
        s.circle(ax.X(b[0]), ax.Y(b[1]), 4, GREEN, PAPER, 1.6)
    s.label(500, 70, 'đầu vào nhiễu', 12, 'start', CLAY, 600)
    s.label(500, 92, 'sau khi chiếu', 12, 'start', GREEN, 600)
    s.label(500, 114, 'cấu trúc sạch', 12, 'start', BLUE, 600)
    s.label(500, 150, 'chỉ giữ phần nhiễu', 11.5, 'start', MUTED)
    s.label(500, 166, 'nằm dọc theo đường', 11.5, 'start', MUTED)
    s.save('3-10-denoise', 'Tín hiệu sạch nằm trên một đường; nhiễu đẳng hướng rải ra mọi phía. Chiếu lên đường bỏ phần nhiễu vuông góc, chỉ giữ phần dọc theo nó; trong 4 chiều, đó là khoảng 1/4 năng lượng nhiễu.')


FIGS310 = {'3-10-bottleneck': bottleneck310, '3-10-reconstruction': recon310, '3-10-ae-pca': ae_curve310,
           '3-10-errors': errors310, '3-10-denoise': denoise310}


FIGS = {'3-1-shapes': shapes31, '3-1-reshape': reshape31, '3-1-broadcast': broadcast31, '3-1-graph': graph31,
        '3-1-autograd-sum': gradsum31, '3-1-detach': detach31, **FIGS32, **FIGS33, **FIGS34, **FIGS35, **FIGS36, **FIGS37, **FIGS38, **FIGS39, **FIGS310}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
