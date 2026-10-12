"""Hình động chương 8 (chiến lược thi). Số liệu chạy lại từ code bài (lesson_ns).
Ảnh thật: china.jpg, flower.jpg (scikit-learn, CC BY 2.0)."""
import io
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, font, sample,  # noqa: E402
                  plain_axes, fig_frame, grab)
from p8_ch1 import lesson_ns  # noqa: E402
from a_ch2 import bare, regions  # noqa: E402


# ───────────────────────────── 8.1 ─────────────────────────────

def a8_1_draws():
    """Đúng mô phỏng của bài (public 200 dòng, seed 0): chênh accuracy public B − A tích lũy qua số lần rút."""
    rng = np.random.default_rng(0)
    a = np.r_[np.ones(1540), np.ones(60), np.zeros(80), np.zeros(320)]
    b = np.r_[np.ones(1540), np.zeros(60), np.ones(80), np.zeros(320)]
    gaps = np.array([b[r].mean() - a[r].mean() for r in (rng.choice(2000, size=200, replace=False) for _ in range(5000))])
    marks = [1, 3, 10, 30, 100, 300, 1000, 5000]
    bins = np.arange(-.0625, .0876, .005)

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for m in marks:
            fig, ax = plain_axes(theme, 960, 420, (.06, .14, .9, .8))
            g = gaps[:m]
            h, e = np.histogram(g, bins)
            h = h / 5000 * 200 if m > 30 else h          # vài lần đầu vẽ theo số đếm để thấy từng lần rút
            ax.bar(e[:-1], h, width=.0045, align='edge', color=[t['clay'] if x + .0025 <= 0 else t['blue'] for x in e[:-1]], linewidth=0)
            ax.axvline(0, color=t['text'], lw=1.6)
            ax.axvline(.01, color=t['muted'], lw=1.2, ls=(0, (4, 3)))
            ax.set_xlim(-.065, .09); ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            ax.set_xticks([-.05, 0, .01, .05]); ax.set_xticklabels(['−0.05', '0', '0.01', '0.05'], color=t['muted'], fontsize=9)
            frames.append(grab(fig))
        return frames

    labels = [f'{m} lần rút public 200 dòng: B ≤ A ở {np.mean(gaps[:m] <= 0):.0%} số lần' for m in marks]
    return Anim('8-1-draws', 'Mô phỏng của bài: B thật sự hơn A 0.01 trên 2000 dòng, nhưng mỗi lần rút 200 dòng public cho một chênh lệch khác; phần cam là những lần public nói ngược.',
                labels, draw, dur=1000, hold=2400, key=[1, 3, 5, 7], photo=False, themed=True)


# ───────────────────────────── 8.2 ─────────────────────────────

def dhash(img, n=8):
    g = np.asarray(Image.fromarray(img).convert('L').resize((n + 1, n), Image.LANCZOS), float)
    return g[:, 1:] > g[:, :-1]


def jpeg(img, q):
    buf = io.BytesIO()
    Image.fromarray(img).save(buf, 'JPEG', quality=q)
    return np.asarray(Image.open(buf).convert('RGB'))


def a8_2_hash():
    """Hash ảnh dHash 64 bit: bản sửa nhẹ của cùng ảnh lệch vài bit, ảnh khác lệch hàng chục bit."""
    base = np.asarray(Image.fromarray(sample('china.jpg')).crop((40, 20, 400, 380)).resize((320, 320), Image.LANCZOS))
    other = np.asarray(Image.fromarray(sample('flower.jpg')).crop((140, 40, 500, 400)).resize((320, 320), Image.LANCZOS))
    variants = [
        ('ảnh gốc', base),
        ('nén JPEG chất lượng 15', jpeg(base, 15)),
        ('thu nhỏ còn 25% rồi phóng lại', np.asarray(Image.fromarray(base).resize((80, 80)).resize((320, 320)))),
        ('tăng sáng 25%', np.asarray(ImageEnhance.Brightness(Image.fromarray(base)).enhance(1.25))),
        ('cắt bớt 6% mỗi cạnh', np.asarray(Image.fromarray(base).crop((19, 19, 301, 301)).resize((320, 320)))),
        ('lật ngang', base[:, ::-1]),
        ('một ảnh khác', other),
    ]
    h0 = dhash(base)

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for name, im in variants:
            cv = canvas(960, 360)
            d = ImageDraw.Draw(cv, 'RGBA')
            paste(cv, base, 20, 20, 300, 300, radius=6)
            paste(cv, im, 340, 20, 300, 300, radius=6)
            h = dhash(im)
            cs = 34
            for i in range(8):
                for j in range(8):
                    x, y = 668 + j * cs, 34 + i * cs
                    diff = h[i, j] != h0[i, j]
                    fill = hexrgb(t['clay']) if diff else hexrgb(t['text'] if h[i, j] else t['soft'], 200)
                    d.rounded_rectangle([x, y, x + cs - 4, y + cs - 4], radius=4, fill=fill)
            frames.append(arr(cv))
        return frames

    labels = []
    for name, im in variants:
        dist = int((dhash(im) != h0).sum())
        labels.append(f'{name}: lệch {dist}/64 bit so với ảnh gốc (ô cam là bit khác)')
    return Anim('8-2-hash', 'dHash: thu ảnh về 9 × 8 điểm xám, mỗi bit ghi điểm bên phải sáng hơn bên trái hay không; bản sửa nhẹ của cùng ảnh chỉ lệch vài bit, lật ngang hay ảnh khác lệch rất nhiều.',
                labels, draw, dur=1700, hold=1400, key=[0, 1, 5, 6], themed=True)


# ───────────────────────────── 8.3 ─────────────────────────────

def a8_3_game():
    """Một ván của player nhỏ trong bài (hidden 5, biểu diễn public): mỗi lượt chọn đề xuất làm giảm số ứng viên kỳ vọng."""
    ns = lesson_ns('8.3', upto=3)
    public, verdict_of, choose = ns['public'], ns['predicted_verdict'], ns['choose_proposal']
    hidden = 5                                   # một ván cần đủ 3 lượt (bài in: turns by hidden [3, 3, 2, 2, 2, 3, 1, 3])
    possible = list(range(len(public)))
    asked, champion = set(), 0
    trace = [(list(possible), champion, None, None)]
    for turn in range(1, 9):
        proposal = choose(possible, asked, champion, public)
        asked.add(proposal)
        if proposal == hidden:
            trace.append(([hidden], proposal, proposal, 'đúng'))
            break
        v = verdict_of(public, champion, proposal, hidden)
        trace.append((list(possible), champion, proposal, v))
        possible = [h for h in possible if h != proposal and verdict_of(public, champion, proposal, h) == v]
        if v == 1:
            champion = proposal
        trace.append((list(possible), champion, None, None))
    word = {-1: 'giữ champion', 0: 'hòa', 1: 'đề xuất thắng'}

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for poss, champ, prop, v in trace:
            cv = canvas(960, 260)
            d = ImageDraw.Draw(cv, 'RGBA')
            for h in range(8):
                x = 60 + h * 112
                alive = h in poss
                d.rounded_rectangle([x, 70, x + 90, 160], radius=12, fill=hexrgb(t['blue'] if alive else t['soft'], 200 if alive else 255),
                                    outline=hexrgb(t['line']), width=1)
                text(cv, x + 45, 115, str(h), hexrgb('#ffffff' if alive else t['faint']), 34, bold=True)
                if h == champ:
                    text(cv, x + 45, 45, 'champion', hexrgb(t['sand']), 18, bold=True)
                if prop is not None and h == prop:
                    d.rounded_rectangle([x - 5, 65, x + 95, 165], radius=14, outline=hexrgb(t['clay']), width=5)
                    text(cv, x + 45, 190, 'đề xuất', hexrgb(t['clay']), 18, bold=True)
            frames.append(arr(cv))
        return frames

    labels = []
    turn = 0
    for poss, champ, prop, v in trace:
        if prop is None:
            labels.append(f'còn {len(poss)} ứng viên xanh' + (f', champion là {champ}' if turn else ', champion ban đầu là 0'))
        elif v == 'đúng':
            turn += 1
            labels.append(f'lượt {turn}: đề xuất {prop} chính là hidden, giải xong')
        else:
            turn += 1
            labels.append(f'lượt {turn}: đề xuất {prop}, phản hồi “{word[v]}”')
    return Anim('8-3-game', 'Một ván của player nhỏ trong bài, hidden là 5: mỗi lượt chọn đề xuất chia đều ứng viên nhất, rồi bỏ mọi ứng viên mâu thuẫn với phản hồi.',
                labels, draw, dur=1700, hold=2400, key=list(range(min(4, len(trace)))) if len(trace) <= 4 else [0, 1, 2, len(trace) - 1],
                photo=False, themed=True, pcols=1)


# ───────────────────────────── 8.4 ─────────────────────────────

def a8_4_blend():
    """Bản đồ xác suất lớp 1 của ba model trong bài và của trung bình có trọng số đã chọn trên tập tune."""
    from sklearn.metrics import log_loss
    ns = lesson_ns('8.4', upto=6)
    models, X_train, y_train = ns['models'], ns['X_train'], ns['y_train']
    tune_probs, y_tune, chosen = ns['tune_probs'], ns['y_tune'], ns['chosen_weights']
    xs, ys = np.linspace(-1.6, 2.6, 260), np.linspace(-1.2, 1.7, 180)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    maps = {n: m.predict_proba(G)[:, 1].reshape(len(ys), len(xs)) for n, m in models.items()}
    names = list(models)
    seq = [(n, maps[n], log_loss(y_tune, tune_probs[i])) for i, n in enumerate(names)]
    eq = np.full(3, 1 / 3)
    seq.append(('equal', sum(w * maps[n] for w, n in zip(eq, names)), log_loss(y_tune, np.tensordot(eq, tune_probs, axes=(0, 0)))))
    seq.append(('chosen', sum(w * maps[n] for w, n in zip(chosen, names)), log_loss(y_tune, np.tensordot(chosen, tune_probs, axes=(0, 0)))))

    def draw(theme):
        t = THEMES[theme]
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list('p', [t['blue'], t['soft'], t['clay']])
        frames = []
        for _, P, _ in seq:
            fig = fig_frame(960, 660)
            ax = fig.add_axes((0, 0, 1, 1)); ax.patch.set_alpha(0)
            ax.imshow(P, origin='lower', extent=(xs[0], xs[-1], ys[0], ys[-1]), aspect='auto', cmap=cmap, vmin=0, vmax=1, alpha=.55)
            ax.contour(xs, ys, P, levels=[.5], colors=[t['text']], linewidths=1.6)
            for lab, col in [(0, t['blue']), (1, t['clay'])]:
                k = y_train == lab
                ax.scatter(X_train[k, 0], X_train[k, 1], s=10, color=col, linewidths=0, alpha=.9)
            ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1])
            bare(ax)
            frames.append(grab(fig))
        return frames

    nm = {'linear': 'logistic regression', 'forest': 'random forest', 'knn': 'kNN 15 láng giềng',
          'equal': 'trung bình đều ba model', 'chosen': f'trọng số đã chọn trên tune {tuple(float(w) for w in chosen)}'}
    labels = [f'{nm[n]}: log loss tune {l:.4f}' for n, _, l in seq]
    return Anim('8-4-blend', 'Bản đồ xác suất lớp 1 của ba model trong bài (nét đậm là mức 0.5), rồi của trung bình đều và trung bình có trọng số chọn trên tập tune.',
                labels, draw, dur=1900, hold=1600, key=[0, 1, 2, 4], photo=False, themed=True, display=560)


# ───────────────────────────── 8.5 ─────────────────────────────

def a8_5_clock():
    """Bảng phút của bài: kế hoạch và hai buổi thi thử chạy song song theo đồng hồ 360 phút."""
    ns = lesson_ns('8.5', upto=8)
    M = ns['minutes']
    stages = list(M.index)
    rows = ['plan', 'session1', 'session2']
    names = {'plan': 'kế hoạch', 'session1': 'buổi 1', 'session2': 'buổi 2'}
    stage_vi = {'read': 'đọc đề', 'baseline': 'baseline', 'improve': 'cải tiến', 'rerun': 'chạy lại', 'check': 'kiểm'}
    clocks = list(range(0, 361, 30))

    def draw(theme):
        t = THEMES[theme]
        cols = [t['muted'], t['blue'], t['clay'], t['sand'], t['green']]
        frames = []
        for now in clocks:
            cv = canvas(960, 300)
            d = ImageDraw.Draw(cv, 'RGBA')
            x0, W = 140, 780
            for r, row in enumerate(rows):
                y = 30 + r * 80
                text(cv, x0 - 16, y + 20, names[row], hexrgb(t['text']), 20, anchor='rm')
                start = 0
                for s, stg in enumerate(stages):
                    dur = int(M.loc[stg, row])
                    a, b = start, min(start + dur, now)
                    if b > a:
                        d.rounded_rectangle([x0 + W * a / 360, y, x0 + W * b / 360 - 2, y + 40], radius=5, fill=hexrgb(cols[s], 210))
                        if b - a > 28:
                            text(cv, x0 + W * (a + b) / 720, y + 20, stage_vi[stg], hexrgb('#ffffff'), 15, bold=True)
                    start += dur
            d.line([x0 + W * now / 360, 18, x0 + W * now / 360, 262], fill=hexrgb(t['text']), width=2)
            for m in range(0, 361, 60):
                text(cv, x0 + W * m / 360, 285, f'{m}', hexrgb(t['muted']), 15)
            frames.append(arr(cv))
        return frames

    labels = [f'phút {m}' for m in clocks]
    labels[-1] = 'hết 360 phút: buổi 1 dồn 225 phút cho cải tiến, không chạy lại; buổi 2 dành 70 phút chạy lại trước khi kiểm'
    return Anim('8-5-clock', 'Bảng phút của bài theo đồng hồ 360 phút: kế hoạch, buổi 1 và buổi 2 chia thời gian cho đọc đề, baseline, cải tiến, chạy lại, kiểm.',
                labels, draw, dur=[700] * (len(clocks) - 1) + [800], hold=3000, key=[4, 8, 12], photo=False, themed=True, pcols=1)


ANIMS = [a8_1_draws, a8_2_hash, a8_3_game, a8_4_blend, a8_5_clock]
