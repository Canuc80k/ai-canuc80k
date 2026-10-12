"""Hình động chương 0 (Python, NumPy, Pandas). Ảnh thật: china.jpg (scikit-learn, CC BY 2.0). Số liệu bảng từ code bài."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, font, sample,  # noqa: E402
                  plain_axes, fig_frame, grab)
from p8_ch1 import lesson_ns  # noqa: E402


# ───────────────────────────── 0.1 ─────────────────────────────

def a0_1_count():
    """Đếm từ như Counter trong bài: đọc từng từ, tăng đúng một ô của dict."""
    words = 'mèo chó mèo gà mèo chó'.split()

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for k in range(len(words) + 2):
            cv = canvas(960, 330)
            d = ImageDraw.Draw(cv, 'RGBA')
            f = font(30, 'serif')
            x = 40
            for i, w in enumerate(words):
                col = t['clay'] if i == k else (t['text'] if i < k else t['faint'])
                if i == k:
                    tw = d.textlength(w, font=f)
                    d.rounded_rectangle([x - 8, 26, x + tw + 8, 76], radius=8, fill=hexrgb(t['clay'], 40))
                d.text((x, 51), w, fill=hexrgb(col), font=f, anchor='lm')
                x += d.textlength(w, font=f) + 26
            counts = {}
            for w in words[:min(k + 1, len(words))] if k < len(words) else words:
                counts[w] = counts.get(w, 0) + 1
            if k == len(words) + 1:
                items = sorted(counts.items(), key=lambda kv: -kv[1])
            else:
                items = list(counts.items())
            for j, (w, c) in enumerate(items):
                y = 120 + j * 64
                hot = k < len(words) and w == words[k]
                d.rounded_rectangle([40, y, 200, y + 48], radius=8, fill=hexrgb(t['soft']), outline=hexrgb(t['clay'] if hot else t['line']), width=3 if hot else 1)
                d.text((60, y + 24), f'"{w}"', fill=hexrgb(t['text']), font=font(24), anchor='lm')
                d.rounded_rectangle([230, y + 8, 230 + 150 * c, y + 40], radius=6, fill=hexrgb(t['clay'] if hot else t['blue'], 210))
                d.text((240 + 150 * c, y + 24), str(c), fill=hexrgb(t['text']), font=font(24, bold=True), anchor='lm')
            frames.append(arr(cv))
        return frames

    labels = []
    for k in range(len(words)):
        before = words[:k].count(words[k])
        labels.append(f'từ “{words[k]}”: ' + (f'đã có khóa, tăng {before} → {before + 1}' if before else 'khóa mới, đặt bằng 1'))
    labels += ['hết câu: dict có 3 khóa', '`most_common(2)` sắp theo số lần giảm dần: mèo 3, chó 2']
    return Anim('0-1-count', 'Đếm “mèo chó mèo gà mèo chó” bằng dict: mỗi từ chỉ chạm đúng một khóa, khóa mới bắt đầu từ 1.',
                labels, draw, dur=1300, hold=2200, key=[0, 2, 4, 7], photo=False, themed=True)


# ───────────────────────────── 0.2 ─────────────────────────────

def a0_2_photo():
    """Mười dòng NumPy trên cùng một ảnh thật (H, W, 3) uint8."""
    img = np.asarray(Image.fromarray(sample('china.jpg')).resize((480, 320), Image.LANCZOS))
    g = img.mean(axis=2)
    steps = [
        ('img', img),
        ('img[::-1]', img[::-1]),
        ('img[:, ::-1]', img[:, ::-1]),
        ('img[60:260, 140:360]', img[60:260, 140:360]),
        ('img[::8, ::8]', img[::8, ::8]),
        ('img[:, :, 0]', np.stack([img[..., 0]] * 3, -1)),
        ('img.mean(axis=2)', np.stack([g] * 3, -1).astype(np.uint8)),
        ('img * [1.0, 0.6, 0.6]', (img * np.array([1.0, .6, .6])).astype(np.uint8)),
        ('img + 100', img + np.uint8(100)),
        ('np.clip(img.astype(int) + 100, 0, 255)', np.clip(img.astype(int) + 100, 0, 255).astype(np.uint8)),
        ('255 - img', 255 - img),
    ]
    shapes = ['(320, 480, 3)', '(320, 480, 3)', '(320, 480, 3)', '(200, 220, 3)', '(40, 60, 3)', '(320, 480)', '(320, 480)',
              '(320, 480, 3), float64', '(320, 480, 3), uint8 tràn vòng', '(320, 480, 3)', '(320, 480, 3)']

    def draw(theme):
        frames = []
        for code, a in steps:
            cv = canvas(960, 520)
            h, w = a.shape[:2]
            s = min(900 / w, 500 / h)          # mọi kết quả phóng cho vừa khung; shape thật ghi ở nhãn
            W, H = round(w * s), round(h * s)
            paste(cv, a, (960 - W) / 2, (520 - H) / 2, W, H, nearest=code == 'img[::8, ::8]', radius=6)
            frames.append(arr(cv))
        return frames

    notes = ['ảnh màu', 'đảo thứ tự hàng: lật dọc', 'đảo thứ tự cột: lật ngang', 'lát cắt hàng 60–259, cột 140–359',
             'lấy mỗi 8 hàng, 8 cột một điểm', 'chỉ kênh đỏ', 'trung bình ba kênh: ảnh xám', 'broadcast: nhân từng kênh với một hệ số',
             '200 + 100 trong uint8 thành 44: màu sáng bị vỡ', 'đổi sang int rồi kẹp về 0–255', 'âm bản']
    labels = [f'`{c}` → {sh}: {n}' for (c, _), sh, n in zip(steps, shapes, notes)]
    return Anim('0-2-photo', 'Một ảnh thật (320, 480, 3) qua mười dòng NumPy: lát cắt, chọn kênh, gộp trục, broadcast, và cái bẫy tràn số uint8.',
                labels, draw, dur=1600, hold=1200, key=[2, 4, 8, 9], themed=False)


# ───────────────────────────── 0.3 ─────────────────────────────

def a0_3_groupby():
    """Split–apply–combine trên 400 học sinh của bài: điểm toán tách theo lớp, mỗi lớp lấy trung bình."""
    ns = lesson_ns('0.3', upto=1)
    full = ns['full'].iloc[:400]
    ns['demo_directory'].cleanup()
    classes = sorted(full.lop.unique())
    rng = np.random.default_rng(3)
    jit = rng.uniform(-.28, .28, len(full))
    yrow = np.array([classes.index(c) for c in full.lop])
    means = full.groupby('lop')['diem_toan'].mean()
    seq = [('all', 0)] + [('split', f) for f in (1 / 3, 2 / 3, 1)] + [('mean', 1), ('bar', 1)]

    def draw(theme):
        t = THEMES[theme]
        cols = [t['blue'], t['clay'], t['green'], t['sand']]
        frames = []
        for kind, f in seq:
            fig, ax = plain_axes(theme, 960, 420, (.12, .12, .84, .84))
            if kind in ('all', 'split'):
                e = ease(f) if kind == 'split' else 0
                yy = lerp(1.5 + jit * 3.2, yrow + jit, e)
                ax.scatter(full.diem_toan, yy, s=10, color=[cols[i] for i in yrow], linewidths=0, alpha=.8)
            elif kind == 'mean':
                ax.scatter(full.diem_toan, yrow + jit, s=10, color=[cols[i] for i in yrow], linewidths=0, alpha=.35)
                for i, c in enumerate(classes):
                    ax.plot([means[c]] * 2, [i - .4, i + .4], color=t['text'], lw=2.6)
            else:
                for i, c in enumerate(classes):
                    ax.barh(i, means[c], color=cols[i], height=.5)
                    ax.text(means[c] + .1, i, f'{means[c]:.2f}', va='center', color=t['text'], fontsize=11)
            ax.set_xlim(0, 10.5); ax.set_ylim(-.7, 3.7)
            ax.set_yticks(range(4)); ax.set_yticklabels(classes if kind != 'all' else [''] * 4, color=t['muted'], fontsize=10)
            ax.set_xlabel('diem_toan', color=t['muted'], fontsize=10)
            frames.append(grab(fig))
        return frames

    labels = ['400 dòng của train.csv, mỗi chấm là một học sinh'] + ['split: tách các dòng theo cột `lop`'] * 3 + \
             ['apply: mỗi nhóm lấy trung bình `diem_toan` (vạch đậm)'] + \
             ['combine: `df.groupby("lop")["diem_toan"].mean()` thành một dòng mỗi lớp']
    return Anim('0-3-groupby', 'groupby trên 400 học sinh của bài: tách dòng theo lớp, tính trung bình điểm toán trong từng nhóm, rồi gộp thành một bảng bốn dòng.',
                labels, draw, dur=[1600, 300, 300, 1100, 1800, 2200], hold=1400, key=[0, 3, 4, 5], photo=False, themed=True)


ANIMS = [a0_1_count, a0_2_photo, a0_3_groupby]
