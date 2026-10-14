"""Lượt 8 — hình chương 9 (bản gọn). Số liệu lấy từ code bài (lesson_ns) hoặc tính lại đúng như bài.
Chạy riêng: python -B -X utf8 p8_ch9.py [tên ...]"""
import math, sys
import numpy as np
from kit import *
from p8_ch1 import lesson_ns


# ───────────────────────────── 9.1 ─────────────────────────────

_T91 = {}


def ns91():
    if not _T91:
        _T91['ns'] = lesson_ns('9.1', upto=3)
    return _T91['ns']


ARROW = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}


def gridworld(s, x0, y0, c, values=None, arrows=None, fmt='{:.2f}', hi=None, size=11, tags=True):
    """Lưới 3×4 của bài: ô chắn (1,1), S (2,0), G (0,3); values: dict ô -> số; arrows: dict ô -> hành động."""
    for r in range(3):
        for col in range(4):
            x, y = x0 + col * c, y0 + r * c
            cell = (r, col)
            if cell == (1, 1):
                s.box(x + 2, y + 2, c - 4, c - 4, 'none', TEXT, r=4, width=0, opacity=.55)
                continue
            fill, op = (GREEN, .3) if cell == (0, 3) else (BLUE, .08)
            if hi and cell in hi:
                fill, op = hi[cell]
            s.box(x + 2, y + 2, c - 4, c - 4, 'none', fill, r=5, width=0, opacity=op)
            tag = 'S' if cell == (2, 0) else 'G' if cell == (0, 3) else None
            if tag and tags:
                s.label(x + 9, y + 12, tag, 10.5, 'start', MUTED, 600)
            if values is not None and cell in values:
                s.mono(x + c / 2, y + c / 2 + (8 if arrows else 0), fmt.format(values[cell]), size, 'middle', TEXT)
            if arrows and cell in arrows:
                dx, dy = ARROW[arrows[cell]]
                cx, cy = x + c / 2, y + c / 2 - 9
                s.arrow(cx - dx * 9, cy - dy * 9, cx + dx * 9, cy + dy * 9, CLAY, 1.6)


def value_iter(ns, rounds):
    states, step, goal, gamma = ns['states'], ns['step'], ns['goal'], ns['gamma']
    V = np.zeros(len(states))
    for _ in range(rounds):
        old = V.copy()
        for st in range(len(states)):
            if st == goal:
                continue
            V[st] = max(r + gamma * (0 if t else old[n]) for n, r, t in (step(st, a) for a in range(4)))
    return V


def loop91():
    s = Fig(640, 210)
    s.box(40, 70, 150, 60, 'none', BLUE, r=8, width=0, opacity=.2)
    s.label(115, 92, 'agent', 13, color=TEXT, weight=600)
    s.mono(115, 112, 'π(a | s), Q(s, a)', 10.5, 'middle', MUTED)
    s.box(450, 70, 150, 60, 'none', SAND, r=8, width=0, opacity=.3)
    s.label(525, 92, 'environment', 13, color=TEXT, weight=600)
    s.mono(525, 112, 'step(s, a)', 10.5, 'middle', MUTED)
    s.curve(190, 82, 450, 82, -.18, CLAY, 1.6)
    s.mono(320, 40, 'hành động A_t', 11.5, 'middle', CLAY, 600)
    s.curve(450, 120, 190, 120, -.18, GREEN, 1.6)
    s.mono(320, 172, 'thưởng R_{t+1}, trạng thái S_{t+1}', 11.5, 'middle', GREEN, 600)
    s.save('9-1-loop', 'Agent chọn hành động; environment trả phần thưởng và trạng thái mới.')


def grid91():
    ns = ns91()
    V = value_iter(ns, 200)
    states, step, goal, gamma = ns['states'], ns['step'], ns['goal'], ns['gamma']
    vals, arr = {}, {}
    for st, cell in enumerate(states):
        vals[cell] = V[st]
        if st != goal:
            q = [r + gamma * (0 if t else V[n]) for n, r, t in (step(st, a) for a in range(4))]
            arr[cell] = int(np.argmax(q))
    s = Fig(640, 270)
    gridworld(s, 160, 20, 78, vals, arr)
    s.mono(500, 60, 'mỗi bước −1', 11.5, 'start', TEXT)
    s.mono(500, 80, 'vào G +10, kết thúc', 11.5, 'start', TEXT)
    s.mono(500, 100, 'γ = 0.9', 11.5, 'start', TEXT)
    s.mono(500, 140, 'V*(S) = 3.122', 12, 'start', CLAY, 600)
    s.save('9-1-grid', 'Giá trị tối ưu V* của từng ô và một hành động tối ưu; từ S cần 5 bước.')


def return91():
    r = np.array([-1, -1, -1, -1, 10.])
    g = .9 ** np.arange(5)
    s = Fig(640, 240)
    ax = s.axes(90, 26, 420, 160, (0, 5), (-2, 11), xticks=[], yticks=[0, 5, 10], grid=False)
    ax.hline(0, FAINT, 1, None)
    for t in range(5):
        for j, (v, col, op) in enumerate([(r[t], FAINT, .35), (r[t] * g[t], CLAY if r[t] > 0 else BLUE, .55)]):
            x = t + .18 + j * .34
            top, bot = max(v, 0), min(v, 0)
            s.rect(ax.X(x), ax.Y(top), ax.X(.3) - ax.X(0), ax.Y(bot) - ax.Y(top), 'none', col, 2, op, 0)
        s.mono(ax.X(t + .5), ax.Y(-2) + 16, f't = {t}', 10.5, 'middle', MUTED)
        s.mono(ax.X(t + .67), ax.Y(max(r[t] * g[t], 0)) - 10, f'{r[t] * g[t]:.3g}', 10, 'middle', TEXT)
    s.mono(530, 70, 'tổng thưởng 6', 11.5, 'start', MUTED)
    s.mono(530, 92, 'G₀ = 3.122', 12, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'thưởng (nhạt) và γᵗ · thưởng (đậm)', 11, 'start', FAINT)
    s.save('9-1-return', 'Thưởng càng xa càng bị chiết khấu: tổng thưởng 6 nhưng return chỉ 3.122.')


def vi91():
    ns = ns91()
    states = ns['states']
    s = Fig(640, 230)
    for k, rounds in enumerate([1, 2, 3, 5]):
        V = value_iter(ns, rounds)
        vals = {cell: V[i] for i, cell in enumerate(states) if cell != (0, 3)}
        x0 = 14 + k * 158
        gridworld(s, x0, 36, 36, vals, fmt='{:.1f}', size=9.5, hi={(2, 0): (CLAY, .3)}, tags=False)
        s.label(x0 + 72, 22, f'sau {rounds} vòng', 11.5, color=TEXT, weight=600)
        s.mono(x0 + 72, 166, f'S: {V[ns["start"]]:.3f}', 11, 'middle', CLAY, 600)
    s.label(320, 206, 'mỗi vòng đưa thông tin từ G lùi thêm một bước', 11, color=MUTED)
    s.save('9-1-vi', 'Value iteration: phải tới vòng 5, thưởng ở G mới lan về tới S.')


def egreedy91():
    s = Fig(640, 210)
    ax = s.axes(100, 30, 380, 130, (0, 4), (0, 1), xticks=[], yticks=[0, .5, 1], grid=False)
    p = [.85, .05, .05, .05]
    for k, v in enumerate(p):
        s.rect(ax.X(k + .2), ax.Y(.8 if k == 0 else 0), ax.X(.6) - ax.X(0), ax.Y(0) - ax.Y(.8 if k == 0 else 0), 'none', CLAY, 3, .5, 0) if k == 0 else None
        s.rect(ax.X(k + .2), ax.Y(v), ax.X(.6) - ax.X(0), ax.Y(v - .05 if k == 0 else 0) - ax.Y(v), 'none', BLUE, 3, .5, 0)
        s.mono(ax.X(k + .5), ax.Y(v) - 9, f'{v:.2f}', 11, 'middle', TEXT)
        s.label(ax.X(k + .5), ax.y + ax.h + 16, 'tốt nhất' if k == 0 else f'khác {k}', 11, color=TEXT)
    s.box(500, 60, 12, 12, 'none', CLAY, r=2, width=0, opacity=.5)
    s.label(518, 66, 'khai thác 0.8', 11, 'start', TEXT)
    s.box(500, 84, 12, 12, 'none', BLUE, r=2, width=0, opacity=.5)
    s.label(518, 90, 'explore 0.2 / 4', 11, 'start', TEXT)
    s.save('9-1-egreedy', 'Epsilon-greedy 0.2 với 4 hành động: hành động tốt nhất được chọn 85% số lần.')


def replay91():
    s = Fig(640, 210)
    vals_back = [3.122, 4.58, 6.2, 8.0, 10.0]
    for r, (nm, vals) in enumerate([('phát lại xuôi', [0, 0, 0, 0, 10.0]), ('phát lại ngược', vals_back)]):
        y = 40 + r * 70
        s.label(120, y + 16, nm, 12, 'end', TEXT, 600)
        for i, v in enumerate(vals):
            x = 120 + i * 84
            on = v != 0
            s.box(x, y, 70, 32, 'none', CLAY if on else FAINT, r=5, width=0, opacity=.15 + .35 * (v / 10) if on else .1)
            s.mono(x + 35, y + 16.5, f'{v:g}', 12, 'middle', TEXT if on else FAINT)
            if i < 4:
                s.arrow(x + 72, y + 16, x + 82, y + 16, FAINT, 1)
        s.mono(120 + 4 * 84 + 84, y + 16.5, 'Q(S) = ' + ('0' if r == 0 else '3.122'), 11.5, 'start', CLAY if r else MUTED, 600 if r else 400)
    for i, nm in enumerate(['S', '', '', '', '→ G']):
        s.mono(155 + i * 84, 128 + 40, nm, 10.5, 'middle', FAINT)
    s.save('9-1-replay', 'Phát lại ngược đưa thưởng về S sau một lượt; phát lại xuôi thì không.')


def learning91():
    ns = ns91()
    states, step, start, gamma = ns['states'], ns['step'], ns['start'], ns['gamma']
    rng = np.random.default_rng(7)
    Q = np.zeros((len(states), 4))
    alpha, eps = .3, .2
    trace = []
    for ep in range(3000):
        st = start
        for _ in range(100):
            if rng.random() < eps:
                a = int(rng.integers(4))
            else:
                best = np.flatnonzero(Q[st] == Q[st].max())
                a = int(rng.choice(best))
            n, r, t = step(st, a)
            target = r if t else r + gamma * np.max(Q[n])
            Q[st, a] += alpha * (target - Q[st, a])
            st = n
            if t:
                break
        trace.append(Q[start].max())
    assert abs(trace[-1] - 3.122) < 1e-3
    s = Fig(640, 240)
    ax = s.axes(80, 26, 440, 160, (0, 300), (-3, 4), xticks=[0, 100, 200, 300], yticks=[-2, 0, 2, 3.122], yfmt='{:g}', grid=False, xlabel='episode')
    ax.line(np.arange(300), trace[:300], BLUE, 1.8)
    ax.hline(3.122, CLAY, 1.2, '4 4')
    s.mono(ax.X(300) + 8, ax.Y(3.122), 'V*(S)', 11, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'max Q(S, ·)', 11, 'start', FAINT)
    s.save('9-1-learning', 'Q-learning tiến dần tới giá trị V*(S) = 3.122 mà value iteration đã tính.')


def bandit91():
    rng = np.random.default_rng(11)
    th, ps = 0., []
    sig = lambda z: 1 / (1 + math.exp(-z))
    for _ in range(400):
        p = sig(th)
        a = int(rng.random() < p)
        r = 3. if a else 1.
        th += .05 * (r - 2.) * (a - p)
        ps.append(sig(th))
    s = Fig(640, 240)
    ax = s.axes(80, 26, 440, 160, (0, 400), (.4, 1), xticks=[0, 100, 200, 300, 400], yticks=[.5, .75, 1], grid=False, xlabel='số mẫu')
    ax.line(np.arange(1, 401), ps, BLUE, 1.8)
    s.mono(ax.X(400) + 8, ax.Y(ps[-1]), f'{ps[-1]:.4f}', 11, 'start', BLUE, 600)
    s.label(ax.x - 8, ax.y - 12, 'p(phải)', 11, 'start', FAINT)
    s.mono(ax.X(210), ax.Y(.55), 'gradient kỳ vọng 2p(1 − p) nhỏ dần khi p gần 1', 10.5, 'middle', MUTED)
    s.save('9-1-bandit', 'Xác suất chọn hành động tốt tăng nhanh lúc đầu rồi chậm dần khi gần 1.')


FIGS91 = {'9-1-loop': loop91, '9-1-grid': grid91, '9-1-return': return91, '9-1-vi': vi91, '9-1-egreedy': egreedy91,
          '9-1-replay': replay91, '9-1-learning': learning91, '9-1-bandit': bandit91}

# ───────────────────────────── 9.2 ─────────────────────────────

_T92 = {}


def ns92(upto=3):
    if upto not in _T92:
        _T92[upto] = lesson_ns('9.2', upto=upto)
    return _T92[upto]


POS92 = {'S': (60, 120), 'A': (260, 50), 'B': (260, 190), 'G': (460, 120)}


def node(s, x, y, name, col=BLUE, op=.25, r=18, label=None):
    s.circle(x, y, r, col, col, 0, op)
    s.label(x, y, name, 13, color=TEXT, weight=600)
    if label:
        s.mono(x, y + r + 14, label, 10.5, 'middle', MUTED)


def edge(s, a, b, w, col=SOFT_LINE, width=1.4, r=18):
    (x1, y1), (x2, y2) = POS92[a], POS92[b]
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    s.arrow(x1 + ux * r, y1 + uy * r, x2 - ux * (r + 2), y2 - uy * (r + 2), col, width)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    s.mono(mx - uy * 14, my + ux * 14, str(w), 11.5, 'middle', col if col != SOFT_LINE else MUTED, 600)


def search92():
    s = Fig(640, 250)
    for a, b, w in [('S', 'B', 1), ('S', 'A', 2), ('A', 'G', 2), ('B', 'G', 10)]:
        good = (a, b) in [('S', 'A'), ('A', 'G')]
        edge(s, a, b, w, GREEN if good else CLAY, 2)
    for n, (x, y) in POS92.items():
        node(s, x, y, n, GREEN if n in 'SAG' else BLUE, .25)
    s.mono(500, 60, 'S–A–G: 4 giây', 11.5, 'start', GREEN, 600)
    s.mono(500, 200, 'S–B–G: 11 giây', 11.5, 'start', CLAY, 600)
    s.label(320, 236, 'cả hai đường đều 2 cạnh; BFS trả đường qua B', 11, color=MUTED)
    s.save('9-2-search', 'BFS đếm cạnh nên chọn đường 11 giây thay vì đường 4 giây.')


def frontier92():
    rows = [('Dijkstra, h = 0', ['S', 'B', 'A', 'G'], '4', GREEN), ('A*, h đúng', ['S', 'A', 'G'], '4', GREEN),
            ('A*, h(A) = 100', ['S', 'B', 'G'], '11', CLAY)]
    s = Fig(640, 200)
    for r, (nm, seq, cost, col) in enumerate(rows):
        y = 40 + r * 52
        s.label(150, y, nm, 12, 'end', TEXT, 600)
        for i, n in enumerate(seq):
            x = 190 + i * 64
            s.circle(x, y, 17, BLUE, BLUE, 0, .2 + .1 * i)
            s.label(x, y, n, 12.5, color=TEXT, weight=600)
            if i:
                s.arrow(x - 64 + 19, y, x - 20, y, FAINT, 1.1)
        s.mono(470, y + .5, f'mở {len(seq)} · chi phí {cost}', 11.5, 'start', col, 600)
    s.label(320, 186, 'thứ tự lấy đỉnh ra khỏi heap', 11, color=MUTED)
    s.save('9-2-astar-frontier', 'Heuristic tốt giúp A* mở ít đỉnh hơn Dijkstra; heuristic ước lượng quá làm A* trả đường sai.')


def king92():
    s = Fig(640, 230)
    c = 34
    x0, y0 = 60, 30
    for i in range(4):
        for j in range(4):
            s.box(x0 + j * c + 1, y0 + i * c + 1, c - 2, c - 2, 'none', BLUE, r=3, width=0, opacity=.08)
    s.label(x0 + c / 2, y0 + 3 * c + c / 2, 'S', 12, color=TEXT, weight=600)
    s.label(x0 + 3 * c + c / 2, y0 + c / 2, 'G', 12, color=GREEN, weight=600)
    for k in range(3):
        s.arrow(x0 + k * c + c / 2 + 6, y0 + (3 - k) * c + c / 2 - 6, x0 + (k + 1) * c + c / 2 - 6, y0 + (2 - k) * c + c / 2 + 6, CLAY, 1.8)
    s.mono(x0 + 2 * c, y0 + 4 * c + 22, '3 bước chéo', 11, 'middle', CLAY, 600)
    rows = [('Manhattan |Δx| + |Δy|', 6, CLAY, 'vượt'), ('Euclid', 4.24, CLAY, 'vượt'), ('max(|Δx|, |Δy|)', 3, GREEN, 'đúng bằng'),
            ('min(|Δx|, |Δy|)', 3, BLUE, 'yếu khi lệch khác nhau')]
    for k, (nm, v, col, note) in enumerate(rows):
        y = 44 + k * 40
        s.mono(270, y, nm, 11, 'start', TEXT)
        s.mono(450, y, f'{v:g}', 12, 'start', col, 600)
        s.label(490, y, note, 10.5, 'start', col)
    s.save('9-2-king', 'Đi 8 hướng: Manhattan và Euclid ước lượng quá, max(|Δx|, |Δy|) đúng bằng 3.')


def maps92():
    ns = ns92(4)
    walls, dist = ns['random_map'](0)
    N, START, GOAL, nbr = ns['N'], ns['START'], ns['GOAL'], ns['neighbors']
    import heapq

    def run(h, w):
        best = {START: 0}
        heap = [(w * h(START), 0, START)]
        seen = []
        while heap:
            _, cost, cell = heapq.heappop(heap)
            if cost != best[cell]:
                continue
            seen.append(cell)
            if cell == GOAL:
                return cost, seen
            for nx in nbr(cell, walls):
                if cost + 1 < best.get(nx, math.inf):
                    best[nx] = cost + 1
                    heapq.heappush(heap, (cost + 1 + w * h(nx), cost + 1, nx))
    man = ns['manhattan']
    setups = [('Dijkstra', lambda c: 0, 1), ('A* Manhattan', man, 1), ('weighted A*, w = 2', man, 2)]
    s = Fig(640, 260)
    cs = 6
    for k, (nm, h, w) in enumerate(setups):
        cost, seen = run(h, w)
        x0 = 20 + k * 208
        for (r, c) in walls:
            s.rect(x0 + c * cs, 30 + r * cs, cs, cs, 'none', TEXT, 0, .55, 0)
        for (r, c) in seen:
            s.rect(x0 + c * cs, 30 + r * cs, cs, cs, 'none', CLAY if nm != 'Dijkstra' or True else BLUE, 0, .35, 0)
        s.label(x0 + 90, 18, nm, 11.5, color=TEXT, weight=600)
        s.mono(x0 + 90, 30 + N * cs + 14, f'mở {len(seen)} · dài {cost}', 11, 'middle', CLAY, 600)
    s.label(320, 248, f'bản đồ seed 0 của bài; đường ngắn nhất dài {dist[START]}; ô đen là tường, ô cam là ô đã mở', 10.5, color=MUTED)
    s.save('9-2-maps', 'A* mở ít ô hơn Dijkstra mà vẫn tối ưu; weighted A* mở ít nhất nhưng có thể trả đường dài hơn.')


def tree(s, x0, vals, prune=(), title=None):
    """Cây MAX → MIN → lá; vals: [[lá]...]; prune: tập (i, j) lá bị cắt."""
    nb = len(vals)
    W = 150 * nb
    xr = x0 + W / 2
    mins = [min(v) if not any((i, j) in prune for j in range(len(v))) else None for i, v in enumerate(vals)]
    s.circle(xr, 40, 16, CLAY, CLAY, 0, .3)
    for i, leaves in enumerate(vals):
        xm = x0 + 75 + i * 150
        s.line(xr, 56, xm, 104, SOFT_LINE, 1.2)
        s.circle(xm, 120, 16, BLUE, BLUE, 0, .3)
        for j, v in enumerate(leaves):
            xl = xm - 30 + j * 60
            cut = (i, j) in prune
            s.line(xm, 136, xl, 182, FAINT if cut else SOFT_LINE, 1.2, '3 3' if cut else None)
            s.box(xl - 16, 184, 32, 26, FAINT if cut else 'none', 'none' if cut else TEXT, r=4, width=1 if cut else 0, opacity=1 if cut else .08, dash='3 3' if cut else None)
            s.mono(xl, 197.5, str(v), 12, 'middle', FAINT if cut else TEXT)
    return xr


def minimax92():
    s = Fig(640, 250)
    vals = [[3, 5], [2, 9]]
    xr = tree(s, 170, vals)
    s.mono(xr, 40.5, '3', 12, 'middle', TEXT, 600)
    for i, v in enumerate(vals):
        s.mono(170 + 75 + i * 150, 120.5, str(min(v)), 12, 'middle', TEXT, 600)
        s.label(170 + 75 + i * 150 - 26, 120, 'A' if i == 0 else 'B', 11, color=MUTED)
    s.label(xr + 30, 40, 'MAX', 10.5, 'start', CLAY)
    s.label(170 + 75 + 150 + 30, 120, 'MIN', 10.5, 'start', BLUE)
    s.label(320, 236, 'lá 9 lớn nhất cây nhưng MIN ở B chọn 2', 11, color=MUTED)
    s.save('9-2-minimax', 'MIN chọn 3 ở A, 2 ở B; MAX chọn A.')


def alphabeta92():
    s = Fig(640, 250)
    vals = [[6, 4], [3, 8], [5, 1]]
    xr = tree(s, 95, vals, prune={(1, 1)})
    s.mono(xr, 40.5, '4', 12, 'middle', TEXT, 600)
    for i, txt in enumerate(['4', '≤ 3', '1']):
        s.mono(95 + 75 + i * 150, 120.5, txt, 11.5, 'middle', TEXT, 600)
        s.label(95 + 75 + i * 150 - 26, 120, 'ABC'[i], 11, color=MUTED)
    s.label(320, 236, 'sau A, MAX đã có 4; lá 3 ở B đủ biết B không hơn 4, nên bỏ lá 8', 11, color=MUTED)
    s.save('9-2-alphabeta', 'Alpha-beta bỏ được lá 8 mà giá trị gốc vẫn là 4.')


def constraints92():
    s = Fig(640, 210)
    P = {'A': (150, 90), 'B': (320, 90), 'C': (490, 90)}
    room = {'A': 0, 'B': 1, 'C': 0}
    for a, b in [('A', 'B'), ('B', 'C')]:
        s.line(P[a][0] + 26, P[a][1], P[b][0] - 26, P[b][1], TEXT, 1.4)
        s.mono((P[a][0] + P[b][0]) / 2, P[a][1] - 12, '≠', 13, 'middle', TEXT, 600)
    s.path(f'M {P["A"][0]} {P["A"][1] + 26} Q 320 190 {P["C"][0]} {P["C"][1] + 26}', FAINT, 1.2, 'none', 1, '4 4')
    s.label(320, 168, 'không có ràng buộc A–C', 10.5, color=FAINT)
    for n, (x, y) in P.items():
        col = BLUE if room[n] == 0 else CLAY
        s.circle(x, y, 24, col, col, 0, .3)
        s.label(x, y, n, 13, color=TEXT, weight=600)
        s.mono(x, y - 40, f'phòng {room[n]}', 11, 'middle', col, 600)
    s.mono(116, 90.5, 'A = 0', 10.5, 'end', MUTED)
    s.save('9-2-constraints', 'A ở phòng 0 buộc B ở phòng 1 và C ở phòng 0.')


def forward92():
    s = Fig(640, 230)
    steps = [('ban đầu', {'A': '0', 'B': '0 1', 'C': '0 1', 'D': '0 1'}),
             ('gán A = 0', {'A': '0', 'B': '1', 'C': '0 1', 'D': '1'}),
             ('gán B = 1', {'A': '0', 'B': '1', 'C': '0', 'D': '∅'})]
    for k, (nm, dom) in enumerate(steps):
        x0 = 30 + k * 205
        s.label(x0 + 90, 24, nm, 12, color=TEXT, weight=600)
        for r, v in enumerate('ABCD'):
            y = 44 + r * 40
            s.label(x0 + 20, y + 14, v, 12, 'middle', TEXT, 600)
            empty = dom[v] == '∅'
            s.box(x0 + 40, y, 130, 28, 'none', CLAY if empty else BLUE, r=4, width=0, opacity=.4 if empty else .12)
            s.mono(x0 + 105, y + 14.5, dom[v], 12, 'middle', CLAY if empty else TEXT, 600 if empty else 400)
    s.label(320, 214, 'D khác A và khác B: hai phòng đã bị chiếm, domain của D rỗng trước khi gán C', 11, color=MUTED)
    s.save('9-2-forward', 'Forward checking phát hiện D hết giá trị nên bỏ nhánh ngay.')


def models92():
    from itertools import product
    worlds = list(product([False, True], repeat=3))
    s = Fig(640, 300)
    heads = ['P', 'Q', 'R', 'KB', 'KB bỏ P']
    xs = [90, 150, 210, 300, 400]
    for h, x in zip(heads, xs):
        s.mono(x, 22, h, 11.5, 'middle', MUTED, 600)
    for i, (P, Q, R) in enumerate(worlds):
        y = 38 + i * 30
        kb = P and (P != Q) and (Q != R)
        kb2 = (P != Q) and (Q != R)
        if kb:
            s.box(60, y, 390, 26, 'none', GREEN, r=4, width=0, opacity=.25)
        elif kb2:
            s.box(60, y, 390, 26, 'none', CLAY, r=4, width=0, opacity=.15)
        for v, x in zip((P, Q, R, kb, kb2), xs):
            s.mono(x, y + 13.5, '1' if v else '0', 12, 'middle', TEXT if v else FAINT, 600 if v else 400)
    s.mono(462, 38 + 5 * 30 + 13.5, 'model duy nhất: R đúng', 10.5, 'start', GREEN)
    s.mono(462, 38 + 2 * 30 + 13.5, 'phản ví dụ: R sai', 10.5, 'start', CLAY)
    s.save('9-2-models', 'KB chỉ có một model và R đúng ở đó, nên KB suy ra R.')


FIGS92 = {'9-2-search': search92, '9-2-astar-frontier': frontier92, '9-2-king': king92, '9-2-maps': maps92,
          '9-2-minimax': minimax92, '9-2-alphabeta': alphabeta92, '9-2-constraints': constraints92,
          '9-2-forward': forward92, '9-2-models': models92}

# ───────────────────────────── 9.3 ─────────────────────────────

def bayes93():
    s = Fig(640, 280)
    cols, c, g = 40, 8, 1.5
    x0, y0 = 40, 30
    # 1000 ô: 20 bài lỗi đầu tiên (18 cảnh báo, 2 sót), rồi 980 bài sạch (98 cảnh báo nhầm)
    for i in range(1000):
        r, k = divmod(i, cols)
        if i < 18:
            col, op = CLAY, .85
        elif i < 20:
            col, op = CLAY, .25
        elif i < 20 + 98:
            col, op = SAND, .7
        else:
            col, op = BLUE, .12
        s.rect(x0 + k * (c + g), y0 + r * (c + g), c, c, 'none', col, 1.5, op, 0)
    s.box(450, 40, 10, 10, 'none', CLAY, r=2, width=0, opacity=.85)
    s.label(466, 45, 'lỗi, bị cảnh báo: 18', 10.5, 'start', TEXT)
    s.box(450, 62, 10, 10, 'none', CLAY, r=2, width=0, opacity=.25)
    s.label(466, 67, 'lỗi, bị sót: 2', 10.5, 'start', TEXT)
    s.box(450, 84, 10, 10, 'none', SAND, r=2, width=0, opacity=.7)
    s.label(466, 89, 'sạch, cảnh báo nhầm: 98', 10.5, 'start', TEXT)
    s.box(450, 106, 10, 10, 'none', BLUE, r=2, width=0, opacity=.12)
    s.label(466, 111, 'sạch: 882', 10.5, 'start', TEXT)
    s.mono(450, 150, 'P(lỗi | cảnh báo)', 11, 'start', MUTED)
    s.mono(450, 170, '= 18 / 116 ≈ 0.155', 11.5, 'start', CLAY, 600)
    s.save('9-3-bayes', 'Trong 116 cảnh báo chỉ có 18 bài thật sự lỗi.')


def prior93():
    s = Fig(640, 240)
    ax = s.axes(80, 26, 420, 160, (0, 1), (0, 1), xticks=[.02, .25, .5, .75, 1], yticks=[0, .5, 1], grid=False, xlabel='tỉ lệ bài lỗi P(B)')
    xs = np.linspace(.001, 1, 300)
    ax.line(xs, .9 * xs / (.9 * xs + .1 * (1 - xs)), CLAY, 2)
    for q in (.02, .5):
        v = .9 * q / (.9 * q + .1 * (1 - q))
        s.circle(ax.X(q), ax.Y(v), 5, CLAY, CLAY)
        s.mono(ax.X(q) + 10, ax.Y(v) + (12 if q < .1 else -10), f'{v:.3f}', 11, 'start', CLAY, 600)
    ax.hline(.9, FAINT, 1, '3 3')
    s.mono(ax.X(1) + 8, ax.Y(.9), 'recall 0.9', 10.5, 'start', FAINT)
    s.label(ax.x - 8, ax.y - 12, 'P(lỗi | cảnh báo)', 11, 'start', FAINT)
    s.save('9-3-prior', 'Tỉ lệ lỗi càng thấp, phần cảnh báo đúng càng nhỏ.')


def logloss93():
    s = Fig(640, 240)
    ax = s.axes(80, 26, 420, 160, (0, 1), (0, 1.6), xticks=[.02, .3, .5, 1], yticks=[0, .5, 1, 1.5], grid=False, xlabel='xác suất dự đoán p')
    xs = np.linspace(.003, .997, 400)
    for q, col in [(.02, BLUE), (.3, CLAY)]:
        L = -q * np.log(xs) - (1 - q) * np.log(1 - xs)
        keep = L <= 1.6
        ax.line(xs[keep], L[keep], col, 2)
        Lq = -q * math.log(q) - (1 - q) * math.log(1 - q)
        s.circle(ax.X(q), ax.Y(Lq), 5, col, col)
        s.mono(ax.X(q) + (10 if q < .1 else 0), ax.Y(Lq) + (14 if q < .1 else -18), f'q = {q}: {Lq:.3f}', 10.5, 'start' if q < .1 else 'middle', col, 600)
    s.label(ax.x - 8, ax.y - 12, 'kỳ vọng log-loss', 11, 'start', FAINT)
    s.save('9-3-logloss', 'Log loss kỳ vọng nhỏ nhất khi dự đoán đúng bằng tỉ lệ thật.')


def null93():
    s = Fig(640, 240)
    ax = s.axes(90, 20, 240, 180, (-1, 4), (-2, 2), xticks=[0, 2, 4], yticks=[-2, 0, 2], grid=False, xlabel='w₁')
    ts = np.linspace(-1.5, 1.5, 50)
    ax.line(1 + 2 * ts, .5 - ts, CLAY, 2)
    for t in (-.5, 0, .5, 1):
        ax.dots([1 + 2 * t], [.5 - t], CLAY, 4, CLAY)
    s.label(ax.x - 34, ax.y + 10, 'w₂', 11, 'end', FAINT)
    s.mono(370, 70, 'X = [[1, 2], [2, 4]]', 11.5, 'start', TEXT)
    s.mono(370, 96, 'X (2, −1) = (0, 0)', 11.5, 'start', TEXT)
    s.mono(370, 134, 'mọi w trên đường cam', 11, 'start', CLAY)
    s.mono(370, 152, 'cho cùng dự đoán Xw', 11, 'start', CLAY)
    s.save('9-3-null', 'Cột thứ hai gấp đôi cột thứ nhất nên hệ số không duy nhất.')


def gradient93():
    s = Fig(640, 230)
    nodes = [('x = (1, 2)', 60), ('z = w·x + b = 0', 210), ('p = σ(z) = 0.5', 370), ('L = 0.693', 520)]
    for k, (t, x) in enumerate(nodes):
        s.box(x - 62, 40, 124, 36, 'none', BLUE if k < 3 else CLAY, r=6, width=0, opacity=.18)
        s.mono(x, 58.5, t, 10.5, 'middle', TEXT)
        if k < 3:
            s.arrow(x + 64, 58, nodes[k + 1][1] - 64, 58, MUTED, 1.2)
    s.curve(520, 78, 210, 118, -.15, CLAY, 1.4)
    s.mono(370, 132, '∂L/∂z = p − y = −0.5', 11, 'middle', CLAY, 600)
    s.mono(210, 160, '∇_w L = (p − y)·x = (−0.5, −1)', 11, 'middle', CLAY)
    s.mono(210, 180, '∂L/∂b = −0.5', 11, 'middle', CLAY)
    s.mono(470, 172, 'bước η = 0.1: L → 0.554', 11, 'middle', GREEN, 600)
    s.save('9-3-gradient', 'Lượt xuôi cho loss 0.693; một bước gradient hạ còn 0.554.')


def conv93():
    s = Fig(640, 220)

    def block(x, y, w, h, d, col, label, sub):
        for k in range(d):
            s.box(x + k * 6, y - k * 6, w, h, col, 'none' if k < d - 1 else col, r=2, width=1, opacity=1 if k < d - 1 else .2)
        s.mono(x + w / 2 + 3 * d, y + h + 18, label, 11, 'middle', TEXT, 600)
        s.mono(x + w / 2 + 3 * d, y + h + 34, sub, 10, 'middle', MUTED)
    block(60, 70, 80, 80, 3, BLUE, '(4, 3, 8, 8)', '3 channel, 8 × 8')
    s.arrow(180, 110, 260, 110, MUTED, 1.4)
    s.mono(220, 92, 'k = 3, p = 1, s = 2', 10, 'middle', CLAY)
    block(290, 90, 40, 40, 2, CLAY, '(4, 2, 4, 4)', '⌊(8 + 2 − 3)/2⌋ + 1 = 4')
    s.mono(440, 80, 'tham số', 11, 'start', MUTED)
    s.mono(440, 104, '2 × (3·3·3 + 1) = 56', 12, 'start', TEXT, 600)
    s.mono(440, 132, 'batch 4 không nhân vào', 10.5, 'start', MUTED)
    s.save('9-3-conv', 'Conv2d: input (4, 3, 8, 8) ra (4, 2, 4, 4), 56 tham số.')


def attention93():
    s = Fig(640, 230)
    W = np.array([[0.6698, 0.3302], [0.3302, 0.6698]])
    Wm = np.array([[1.0, 0.0], [0.3302, 0.6698]])
    for k, (nm, M, out) in enumerate([('không mask', W, ['(1.34, 1.32)', '(0.66, 2.68)']), ('causal mask', Wm, ['(2, 0)', '(0.66, 2.68)'])]):
        x0 = 60 + k * 300
        s.label(x0 + 75, 22, nm, 12, color=TEXT, weight=600)
        s.label(x0 + 34, 42, 'key 1', 10, color=FAINT)
        s.label(x0 + 104, 42, 'key 2', 10, color=FAINT)
        for i in range(2):
            for j in range(2):
                v = M[i, j]
                masked = k == 1 and i == 0 and j == 1
                s.box(x0 + j * 70, 52 + i * 46, 66, 40, FAINT if masked else 'none', 'none' if masked else CLAY, r=4,
                      width=1 if masked else 0, opacity=1 if masked else .1 + .6 * v, dash='3 3' if masked else None)
                s.mono(x0 + j * 70 + 33, 72.5 + i * 46, f'{v:.2f}', 11, 'middle', TEXT)
            s.label(x0 - 10, 72 + i * 46, f'q{i + 1}', 10.5, 'end', MUTED)
            s.mono(x0 + 160, 72.5 + i * 46, '→ ' + out[i], 10.5, 'start', BLUE)
    s.label(320, 170, 'mỗi hàng là một phân phối trên key, nhân với value (2, 0) và (0, 4)', 11, color=MUTED)
    s.save('9-3-attention', 'Mỗi hàng trọng số cộng thành 1; causal mask chặn key tương lai.')


def confusion93():
    s = Fig(640, 230)
    M = [['18', '2'], ['98', '882']]
    fills = {(0, 0): (CLAY, .5), (0, 1): (CLAY, .15), (1, 0): (SAND, .45), (1, 1): (BLUE, .1)}
    s.tiles(150, 50, M, 90, 52, BLUE, 6, fills, size=15)
    s.label(195, 36, 'cảnh báo', 11, color=MUTED)
    s.label(291, 36, 'không', 11, color=MUTED)
    s.label(140, 76, 'có lỗi', 11, 'end', MUTED)
    s.label(140, 134, 'sạch', 11, 'end', MUTED)
    s.box(147, 47, 96, 116, CLAY, 'none', r=6, width=1.4, dash='4 4')
    s.mono(400, 66, 'recall 18/20 = 0.900', 11.5, 'start', TEXT)
    s.mono(400, 90, 'precision 18/116 = 0.155', 11.5, 'start', CLAY, 600)
    s.mono(400, 114, 'accuracy 900/1000 = 0.900', 11.5, 'start', TEXT)
    s.mono(400, 138, 'F1 36/136 = 0.265', 11.5, 'start', TEXT)
    s.mono(400, 172, 'luôn đoán sạch: acc 0.98, recall 0', 10.5, 'start', MUTED)
    s.save('9-3-confusion-metrics', 'Recall 0.9 nhưng precision chỉ 0.155; luôn đoán sạch vẫn có accuracy 0.98.')


def se93():
    s = Fig(640, 230)
    ax = s.axes(80, 26, 420, 150, (50, 1000), (0, .045), xticks=[100, 250, 500, 750, 1000], yticks=[0, .01, .02, .03, .04], yfmt='{:.2f}', grid=False, xlabel='số mẫu validation n')
    ns_ = np.linspace(50, 1000, 300)
    ax.line(ns_, np.sqrt(.09 / ns_), BLUE, 2)
    for n in (100, 1000):
        v = math.sqrt(.09 / n)
        s.circle(ax.X(n), ax.Y(v), 5, CLAY, CLAY)
        s.mono(ax.X(n) + (10 if n < 900 else -10), ax.Y(v) - 12, f'{v:.4f}', 11, 'start' if n < 900 else 'end', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'độ lệch chuẩn của accuracy (p = 0.9)', 11, 'start', FAINT)
    s.save('9-3-se', 'Giảm số mẫu 10 lần làm độ lệch chuẩn của accuracy tăng √10 lần.')


FIGS93 = {'9-3-bayes': bayes93, '9-3-prior': prior93, '9-3-logloss': logloss93, '9-3-null': null93, '9-3-gradient': gradient93,
          '9-3-conv': conv93, '9-3-attention': attention93, '9-3-confusion-metrics': confusion93, '9-3-se': se93}

FIGS = {**FIGS91, **FIGS92, **FIGS93}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
