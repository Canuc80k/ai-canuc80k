"""Hình động chương 9 (RL, tìm kiếm, bài lý thuyết). Mọi số liệu chạy lại từ code bài (lesson_ns)."""
import sys
from pathlib import Path
import numpy as np
from PIL import ImageDraw

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import Anim, THEMES, canvas, rect, arr, hexrgb, text, font, fig_frame, grab  # noqa: E402
from p8_ch1 import lesson_ns  # noqa: E402


# ───────────────────────────── 9.1 ─────────────────────────────

def a9_1_vi():
    """Value iteration đồng bộ của bài trên grid world 3 × 4: giá trị lan từ đích về S qua từng vòng."""
    ns = lesson_ns('9.1', upto=2)
    states, step, goal, start, gamma = ns['states'], ns['step'], ns['goal'], ns['start'], ns['gamma']
    V = np.zeros(len(states))
    hist = [V.copy()]
    for _ in range(200):
        old = V.copy()
        for s in range(len(states)):
            if s == goal:
                continue
            V[s] = max(r + gamma * (0 if term else old[n]) for n, r, term in (step(s, a) for a in range(4)))
        hist.append(V.copy())
        if np.max(np.abs(V - old)) < 1e-12:
            break
    hist = hist[:9] + [hist[-1]] if len(hist) > 9 else hist

    def policy(Vv, s):
        q = [r + gamma * (0 if term else Vv[n]) for n, r, term in (step(s, a) for a in range(4))]
        return int(np.argmax(q)) if max(q) > min(q) + 1e-9 else None

    def draw(theme):
        t = THEMES[theme]
        frames = []
        cell = 150
        x0, y0 = (960 - 4 * cell) / 2, 20
        lo, hi = -5, 10
        for Vv in hist:
            cv = canvas(960, 3 * cell + 40)
            d = ImageDraw.Draw(cv, 'RGBA')
            for r in range(3):
                for c in range(4):
                    x, y = x0 + c * cell, y0 + r * cell
                    if (r, c) == (1, 1):
                        d.rounded_rectangle([x + 4, y + 4, x + cell - 4, y + cell - 4], radius=10, fill=hexrgb(t['text']))
                        continue
                    s = states.index((r, c))
                    v = Vv[s]
                    a = int(40 + 150 * min(1, abs(v) / (hi if v > 0 else -lo)))
                    col = t['clay'] if v > 0 else t['blue']
                    d.rounded_rectangle([x + 4, y + 4, x + cell - 4, y + cell - 4], radius=10, fill=hexrgb(col, a if v else 25),
                                        outline=hexrgb(t['line']), width=1)
                    if s == goal:
                        text(cv, x + cell / 2, y + cell / 2, 'G', hexrgb(t['text']), 34, bold=True)
                        continue
                    text(cv, x + cell / 2, y + cell / 2 - 8, f'{v:.2f}', hexrgb(t['text']), 26)
                    if s == start:
                        text(cv, x + 18, y + 20, 'S', hexrgb(t['text']), 20, bold=True)
                    p = policy(Vv, s)
                    if p is not None:
                        dr, dc = [(-1, 0), (1, 0), (0, -1), (0, 1)][p]
                        cx, cy = x + cell / 2, y + cell / 2 + 38
                        d.line([cx - dc * 16, cy - dr * 16, cx + dc * 16, cy + dr * 16], fill=hexrgb(t['muted']), width=4)
                        hx, hy = cx + dc * 16, cy + dr * 16
                        d.polygon([(hx + dc * 8, hy + dr * 8), (hx - dr * 7, hy + dc * 7), (hx + dr * 7, hy - dc * 7)], fill=hexrgb(t['muted']))
            frames.append(arr(cv))
        return frames

    labels = [f'vòng {k}: V(S) = {h[start]:.3f}' for k, h in enumerate(hist)]
    labels[0] = 'vòng 0: mọi ô bắt đầu bằng 0'
    labels[-1] = f'hội tụ: V(S) = {hist[-1][start]:.3f}, mũi tên là hành động tốt nhất ở mỗi ô'
    return Anim('9-1-vi', 'Value iteration của bài: mỗi vòng, mỗi ô lấy thưởng tốt nhất của một bước cộng giá trị chiết khấu của ô kế; giá trị lan dần từ đích G về S.',
                labels, draw, dur=[1400] + [1100] * (len(hist) - 2) + [1600], hold=2400, key=[1, 3, 5, len(hist) - 1],
                photo=False, themed=True, display=600)


# ───────────────────────────── 9.2 ─────────────────────────────

def a9_2_frontier():
    """Bản đồ seed 0 của bài: Dijkstra và A* Manhattan mở ô theo thứ tự thật; đường tìm được ở khung cuối."""
    import heapq
    import math
    ns = lesson_ns('9.2', upto=4)
    random_map, neighbors, manhattan, START, GOAL, N = ns['random_map'], ns['neighbors'], ns['manhattan'], ns['START'], ns['GOAL'], ns['N']
    walls, dist = random_map(0)

    def run(h):
        best, parent = {START: 0}, {START: None}
        heap = [(h(START), 0, START)]
        order = []
        while heap:
            _, cost, cell = heapq.heappop(heap)
            if cost != best[cell]:
                continue
            order.append(cell)
            if cell == GOAL:
                break
            for nxt in neighbors(cell, walls):
                if cost + 1 < best.get(nxt, math.inf):
                    best[nxt] = cost + 1
                    parent[nxt] = cell
                    heapq.heappush(heap, (cost + 1 + h(nxt), cost + 1, nxt))
        path, c = [], GOAL
        while c is not None:
            path.append(c)
            c = parent[c]
        return order, path[::-1]
    runs = {'Dijkstra': run(lambda c: 0), 'A* Manhattan': run(manhattan)}
    longest = max(len(o) for o, _ in runs.values())
    stops = [int(x) for x in np.linspace(1, longest, 16)]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        cs = 14
        for k in stops + ['path']:
            cv = canvas(960, N * cs + 50)
            d = ImageDraw.Draw(cv, 'RGBA')
            for j, (name, (order, path)) in enumerate(runs.items()):
                x0 = 30 + j * (N * cs + 60)
                n_open = len(order) if k == 'path' else min(k, len(order))
                opened = set(order[:n_open])
                for r in range(N):
                    for c in range(N):
                        x, y = x0 + c * cs, 10 + r * cs
                        if (r, c) in walls:
                            d.rectangle([x, y, x + cs - 2, y + cs - 2], fill=hexrgb(t['text'], 200))
                        elif (r, c) in opened:
                            d.rectangle([x, y, x + cs - 2, y + cs - 2], fill=hexrgb(t['clay'], 120))
                        else:
                            d.rectangle([x, y, x + cs - 2, y + cs - 2], fill=hexrgb(t['soft']))
                if k == 'path' or n_open == len(order):
                    pts = [(x0 + c * cs + cs / 2 - 1, 10 + r * cs + cs / 2 - 1) for r, c in path]
                    d.line(pts, fill=hexrgb(t['blue']), width=4, joint='curve')
                for (r, c), lab in [(START, 'S'), (GOAL, 'G')]:
                    d.rectangle([x0 + c * cs, 10 + r * cs, x0 + c * cs + cs - 2, 10 + r * cs + cs - 2], fill=hexrgb(t['blue']))
                text(cv, x0 + N * cs / 2, N * cs + 32, f'{name}: đã mở {n_open} ô', hexrgb(t['text']), 19)
            frames.append(arr(cv))
        return frames

    od, oa = runs['Dijkstra'][0], runs['A* Manhattan'][0]
    labels = [f'sau {k} lần lấy ô khỏi heap' for k in stops] + \
             [f'cả hai tìm đường dài {len(runs["Dijkstra"][1]) - 1} bước; Dijkstra mở {len(od)} ô, A* Manhattan mở {len(oa)} ô']
    return Anim('9-2-frontier', 'Bản đồ 30 × 30 seed 0 của bài: Dijkstra mở ô loang đều mọi hướng, A* với heuristic Manhattan mở lệch về phía đích; cả hai cho cùng độ dài đường đi.',
                labels, draw, dur=[450] * len(stops) + [2400], hold=2000, key=[3, 8, 12, len(stops)], photo=False, themed=True)


# ───────────────────────────── 9.3 ─────────────────────────────

def a9_3_base():
    """Cùng detector (bắt 90% bài lỗi, báo nhầm 10% bài sạch) trên 1000 bài khi tỉ lệ lỗi tăng dần."""
    qs = [.01, .02, .05, .1, .2, .3, .5]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for q in qs:
            bad = round(1000 * q)
            tp = round(.9 * bad)
            fp = round(.1 * (1000 - bad))
            kinds = ['tp'] * tp + ['fn'] * (bad - tp) + ['fp'] * fp + ['tn'] * (1000 - bad - fp)
            cv = canvas(960, 420)
            d = ImageDraw.Draw(cv, 'RGBA')
            cs = 15
            for i, kd in enumerate(kinds):
                r, c = divmod(i, 50)
                x, y = 105 + c * cs, 10 + r * cs
                if kd == 'tp':
                    d.rectangle([x, y, x + cs - 3, y + cs - 3], fill=hexrgb(t['clay']))
                elif kd == 'fn':
                    d.rectangle([x, y, x + cs - 3, y + cs - 3], outline=hexrgb(t['clay']), width=2)
                elif kd == 'fp':
                    d.rectangle([x, y, x + cs - 3, y + cs - 3], fill=hexrgb(t['blue']))
                else:
                    d.rectangle([x, y, x + cs - 3, y + cs - 3], fill=hexrgb(t['soft']))
            frames.append(arr(cv))
        return frames

    labels = []
    for q in qs:
        bad = round(1000 * q); tp = round(.9 * bad); fp = round(.1 * (1000 - bad))
        labels.append(f'{bad} bài lỗi trên 1000: {tp + fp} cảnh báo, {tp} đúng (cam đặc), {fp} nhầm (xanh); P(lỗi | cảnh báo) = {tp / (tp + fp):.3f}')
    return Anim('9-3-base', 'Cùng detector bắt 90% bài lỗi và báo nhầm 10% bài sạch, trên 1000 bài: tỉ lệ lỗi càng thấp thì phần cảnh báo đúng trong mọi cảnh báo càng nhỏ.',
                labels, draw, dur=1800, hold=1800, key=[1, 3, 6], photo=False, themed=True, pcols=3)


ANIMS = [a9_1_vi, a9_2_frontier, a9_3_base]
