"""Hình động chương 1 (nền tảng học máy). Số liệu chạy lại từ code bài (lesson_ns).
Ảnh thật: chữ số viết tay load_digits (UCI Optical Recognition of Handwritten Digits, CC BY 4.0)."""
import sys
from pathlib import Path
import numpy as np
from PIL import ImageDraw

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, font,  # noqa: E402
                  plain_axes, fig_frame, grab)
from p8_ch1 import lesson_ns  # noqa: E402
from a_ch2 import bare  # noqa: E402


def ink8(img):
    v = (255 - img / 16 * 235).astype(np.uint8)
    return np.stack([v] * 3, -1)


# ───────────────────────────── 1.1 ─────────────────────────────

def a1_1_row():
    """Bốn ảnh chữ số 8 × 8 thật trải thành bốn hàng 64 số của bảng X, nhãn vào cột y."""
    from sklearn.datasets import load_digits
    D = load_digits()
    pick = [int(np.nonzero(D.target == d)[0][0]) for d in (3, 7, 0, 5)]
    seq = []
    for r in range(4):
        seq += [(r, f) for f in (0, .5, 1)]
    seq += [(4, 1)]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        cell, big = 11, 26
        lo, hi = np.array(hexrgb(t['soft'])[:3], float), np.array(hexrgb(t['text'])[:3], float)

        def shade(v):          # 0 = nền giấy, 16 = mực; đổi theo nền sáng/tối
            return tuple(int(c) for c in lo + (hi - lo) * v / 16) + (255,)
        for cur, f in seq:
            cv = canvas(960, 450)
            d = ImageDraw.Draw(cv, 'RGBA')
            for r in range(4):
                img = D.images[pick[r]]
                y_row = 240 + r * 42
                if r < cur or (r == cur and f == 1) or cur == 4:
                    # hàng đã trải: 64 ô, mỗi ô một điểm ảnh, theo thứ tự hàng của ảnh
                    for k, v in enumerate(img.ravel()):
                        d.rectangle([20 + k * cell, y_row, 20 + k * cell + cell - 1, y_row + 30], fill=shade(v))
                    text(cv, 20 + 64 * cell + 46, y_row + 15, str(D.target[pick[r]]), hexrgb(t['clay']), 24, bold=True)
            if cur < 4:
                img = D.images[pick[cur]]
                x0 = 360
                for i in range(8):
                    for j in range(8):
                        sx, sy = x0 + j * big, 10 + i * big
                        k = i * 8 + j
                        ex, ey = 20 + k * cell, 240 + cur * 42
                        e = ease(f * 1.6 - i * .08)
                        x, y = lerp(sx, ex, e), lerp(sy, ey, e)
                        w, h = lerp(big, cell, e), lerp(big, 30, e)
                        d.rectangle([x, y, x + w - 1, y + h - 1], fill=shade(img[i, j]))
            text(cv, 20 + 64 * cell + 46, 428, 'y', hexrgb(t['muted']), 20)
            text(cv, 20 + 32 * cell, 428, 'X: 64 cột, mỗi cột là một điểm ảnh', hexrgb(t['muted']), 18)
            frames.append(arr(cv))
        return frames

    labels = []
    for cur, f in seq:
        if cur == 4:
            labels.append('4 ảnh thành bảng X shape (4, 64) và vector nhãn y shape (4,)')
        else:
            labels.append(f'ảnh {cur + 1}: lưới 8 × 8 trải theo từng hàng thành 64 số, nhãn {D.target[pick[cur]]}')
    return Anim('1-1-row', 'Ảnh chữ số viết tay thật 8 × 8 trải thành một hàng 64 số: mỗi ảnh là một hàng của X, chữ số đúng là giá trị y.',
                labels, draw, dur=[900, 300, 1000] * 4 + [2400], hold=1200, key=[0, 2, 8, 12], photo=False, themed=True)


# ───────────────────────────── 1.2 ─────────────────────────────

def a1_2_k():
    ns = lesson_ns('1.2', upto=1)
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.metrics import mean_squared_error
    Xt, yt, Xv, yv = ns['X_train'], ns['y_train'], ns['X_valid'], ns['y_valid']
    ks = [80, 60, 40, 25, 15, 10, 6, 3, 2, 1]
    xs = np.linspace(0, 1, 600)[:, None]
    fits = []
    for k in ks:
        m = KNeighborsRegressor(n_neighbors=k).fit(Xt, yt)
        fits.append((m.predict(xs), mean_squared_error(yt, m.predict(Xt)), mean_squared_error(yv, m.predict(Xv))))

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for curve, _, _ in fits:
            fig, ax = plain_axes(theme, 960, 460, (.06, .1, .9, .86))
            ax.plot(xs[:, 0], np.sin(2 * np.pi * xs[:, 0]), color=t['muted'], lw=1.2, ls=(0, (4, 3)))
            ax.scatter(Xt[:, 0], yt, s=22, color=t['blue'], linewidths=0, zorder=3)
            ax.plot(xs[:, 0], curve, color=t['clay'], lw=2.2, zorder=4)
            ax.set_xlim(0, 1); ax.set_ylim(-1.8, 1.8)
            ax.set_xticks([0, .5, 1]); ax.set_yticks([-1, 0, 1])
            frames.append(grab(fig))
        return frames

    labels = [f'k = {k}: train MSE {a:.4f}, validation MSE {b:.4f}' for k, (_, a, b) in zip(ks, fits)]
    return Anim('1-2-k', 'kNN hồi quy trên 80 điểm train của bài khi giảm k từ 80 về 1: đường cam đi từ quá phẳng tới bám từng điểm nhiễu; nét đứt là quy luật thật.',
                labels, draw, dur=1000, hold=2400, key=[0, 3, 6, 9], photo=False, themed=True)


# ───────────────────────────── 1.3 ─────────────────────────────

def a1_3_oof():
    ns = lesson_ns('1.3', upto=4)
    from sklearn.linear_model import LogisticRegression
    X, y, cv = ns['X'], ns['y'], ns['cv']
    folds = list(cv.split(X, y))
    oof = np.full(len(y), np.nan)
    states = [(None, oof.copy(), None)]
    for f, (tr, va) in enumerate(folds):
        states.append((f, oof.copy(), 'train'))
        p = LogisticRegression(max_iter=500).fit(X[tr], y[tr]).predict_proba(X[va])[:, 1]
        oof[va] = p
        states.append((f, oof.copy(), 'pred'))
    fold_of = np.zeros(len(y), int)
    for f, (_, va) in enumerate(folds):
        fold_of[va] = f

    def draw(theme):
        t = THEMES[theme]
        frames = []
        cs = 34
        for f, o, stage in states:
            cv_ = canvas(960, 330)
            d = ImageDraw.Draw(cv_, 'RGBA')
            for i in range(len(y)):
                r, c = divmod(i, 24)
                x, yy = 70 + c * cs, 20 + r * (cs + 40)
                if f is not None and fold_of[i] == f:
                    d.rounded_rectangle([x - 2, yy - 2, x + cs - 4, yy + cs - 4], radius=6, outline=hexrgb(t['clay']), width=3)
                elif f is not None:
                    d.rounded_rectangle([x, yy, x + cs - 6, yy + cs - 6], radius=5, fill=hexrgb(t['soft']))
                if not np.isnan(o[i]):
                    col = np.array(hexrgb(t['blue'])[:3]) * (1 - o[i]) + np.array(hexrgb(t['clay'])[:3]) * o[i]
                    d.rounded_rectangle([x + 3, yy + 3, x + cs - 9, yy + cs - 9], radius=4, fill=tuple(int(v) for v in col) + (255,))
                d.text((x + cs / 2 - 3, yy + cs + 2), str(int(y[i])), fill=hexrgb(t['muted']), font=font(13), anchor='mt')
            frames.append(arr(cv_))
        return frames

    labels = ['96 mẫu (số nhỏ là nhãn thật), cột OOF còn trống']
    from sklearn.metrics import accuracy_score
    for f, o, stage in states[1:]:
        va = folds[f][1]
        if stage == 'train':
            labels.append(f'fold {f + 1}: train trên {len(y) - len(va)} mẫu, giữ {len(va)} mẫu viền cam')
        else:
            acc = accuracy_score(y[va], o[va] >= .5)
            labels.append(f'fold {f + 1}: dự đoán ghi về đúng vị trí gốc, accuracy fold {acc:.3f}')
    labels[-1] += f'; OOF đủ 96 ô, accuracy gộp {accuracy_score(y, oof >= .5):.3f}'
    return Anim('1-3-oof', 'StratifiedKFold 3 fold của bài trên 96 mẫu: mỗi fold, model chưa thấy các ô viền cam sẽ đoán chúng; xác suất (xanh 0, cam 1) ghi về đúng vị trí cho đủ cột OOF.',
                labels, draw, dur=[1500] + [1100, 1500] * 3, hold=2200, key=[1, 2, 4, 6], photo=False, themed=True)


# ───────────────────────────── 1.4 ─────────────────────────────

def a1_4_table():
    ns = lesson_ns('1.4', upto=3)
    model, X_valid = ns['model'], ns['X_valid']
    pre = model.named_steps['preprocess']
    rows = [i for i in range(len(X_valid)) if X_valid.iloc[i].isna().any()][:2] + [0, 1, 2, 3]
    rows = sorted(set(rows))[:6]
    raw = X_valid.iloc[rows]
    num, cat = pre.named_transformers_['num'], pre.named_transformers_['cat']
    imputed = num.named_steps['impute'].transform(raw[['registered', 'rain']])
    scaled = num.named_steps['scale'].transform(imputed)
    onehot = cat.transform(raw[['slot']])
    pred = model.predict(raw)
    med = num.named_steps['impute'].statistics_

    def fmt(v):
        return '—' if v != v else (f'{v:.2f}' if isinstance(v, float) else str(v))
    stages = [
        ('raw', ['registered', 'rain', 'slot'], [[fmt(r.registered), fmt(r.rain), r.slot] for r in raw.itertuples()]),
        ('impute', ['registered', 'rain', 'slot'], [[f'{a:.2f}', f'{b:.2f}', r.slot] for (a, b), r in zip(imputed, raw.itertuples())]),
        ('scale', ['z_registered', 'z_rain', 'slot'], [[f'{a:+.2f}', f'{b:+.2f}', r.slot] for (a, b), r in zip(scaled, raw.itertuples())]),
        ('onehot', ['z_registered', 'z_rain', 'chieu', 'sang'], [[f'{a:+.2f}', f'{b:+.2f}', f'{c:g}', f'{e:g}'] for (a, b), (c, e) in zip(scaled, onehot)]),
        ('pred', ['z_registered', 'z_rain', 'chieu', 'sang', 'dự đoán'], [[f'{a:+.2f}', f'{b:+.2f}', f'{c:g}', f'{e:g}', f'{p:.1f}'] for (a, b), (c, e), p in zip(scaled, onehot, pred)]),
    ]
    nan_mask = raw[['registered', 'rain']].isna().to_numpy()

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for key, head, body in stages:
            cv = canvas(960, 380)
            d = ImageDraw.Draw(cv, 'RGBA')
            cw = 900 / len(head)
            for j, h in enumerate(head):
                text(cv, 30 + cw * (j + .5), 26, h, hexrgb(t['muted']), 19)
            for i, row in enumerate(body):
                y = 58 + i * 50
                d.rounded_rectangle([30, y, 930, y + 42], radius=6, fill=hexrgb(t['soft'], 120))
                for j, v in enumerate(row):
                    col = t['text']
                    if key == 'impute' and j < 2 and nan_mask[i, j]:
                        col = t['clay']
                    if key == 'onehot' and j >= 2:
                        col = t['blue']
                    if key == 'pred' and j == len(row) - 1:
                        col = t['clay']
                    text(cv, 30 + cw * (j + .5), y + 21, v, hexrgb(col), 22, bold=(col != t['text']))
            frames.append(arr(cv))
        return frames

    labels = ['6 hàng validation thô: có ô trống (—) và cột chữ slot',
              f'SimpleImputer: ô trống thay bằng trung vị học từ train ({med[0]:.1f} và {med[1]:.2f})',
              'StandardScaler: trừ mean, chia std đã học từ train',
              'OneHotEncoder: slot thành hai cột 0/1',
              'LinearRegression đọc 4 cột và cho dự đoán']
    return Anim('1-4-table', 'Sáu hàng validation của bài đi qua Pipeline đã fit trên train: điền trung vị, chuẩn hóa, one-hot, rồi model dự đoán; mọi con số dùng thống kê của train.',
                labels, draw, dur=2100, hold=1500, key=[0, 1, 3, 4], photo=False, themed=True, pcols=2)


# ───────────────────────────── 1.5 ─────────────────────────────

def a1_5_threshold():
    ns = lesson_ns('1.5', upto=1)
    y, p = ns['y_valid'], ns['p_valid']
    ths = [1.0, .9, .75, .68, .62, .58, .5, .45, .35, .25, .15, .05]
    from sklearn.metrics import roc_curve
    fpr_all, tpr_all, _ = roc_curve(y, p)

    def stats(th):
        pr = (p >= th).astype(int)
        tp = int(((pr == 1) & (y == 1)).sum()); fp = int(((pr == 1) & (y == 0)).sum())
        fn = int(((pr == 0) & (y == 1)).sum()); tn = int(((pr == 0) & (y == 0)).sum())
        return tp, fp, fn, tn

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for th in ths:
            tp, fp, fn, tn = stats(th)
            fig = fig_frame(960, 420)
            ax = fig.add_axes((.04, .55, .56, .3)); ax.patch.set_alpha(0)
            ax.axhline(0, color=t['line'], lw=1)
            for pi, yi in zip(p, y):
                ax.scatter(pi, 0, s=170, color=t['clay'] if yi else t['blue'], zorder=3, edgecolors=t['text'] if pi >= th else 'none', linewidths=1.6)
            ax.axvline(th, color=t['text'], lw=2)
            ax.axvspan(th, 1.05, color=t['sand'], alpha=.12, lw=0)
            ax.set_xlim(-.02, 1.04); ax.set_ylim(-1, 1)
            bare(ax)
            for v in (0, .5, 1):
                ax.text(v, -.85, f'{v:g}', ha='center', color=t['muted'], fontsize=10)
            fig.text(.04, .9, 'xác suất model cho lớp 1 (viền đậm: đoán 1)', color=t['muted'], fontsize=10.5)
            # confusion matrix
            axc = fig.add_axes((.08, .06, .22, .4)); axc.patch.set_alpha(0)
            M = np.array([[tn, fp], [fn, tp]])
            axc.imshow(M, cmap=__import__('matplotlib.colors', fromlist=['x']).LinearSegmentedColormap.from_list('m', [t['soft'], t['sand']]), vmin=0, vmax=7)
            for i in range(2):
                for j in range(2):
                    axc.text(j, i, str(M[i, j]), ha='center', va='center', color=t['text'], fontsize=15)
            axc.set_xticks([0, 1]); axc.set_xticklabels(['đoán 0', 'đoán 1'], color=t['muted'], fontsize=9.5)
            axc.set_yticks([0, 1]); axc.set_yticklabels(['thật 0', 'thật 1'], color=t['muted'], fontsize=9.5)
            axc.tick_params(length=0)
            for s in axc.spines.values():
                s.set_visible(False)
            # ROC
            axr = fig.add_axes((.68, .12, .28, .74)); axr.patch.set_alpha(0)
            axr.plot(fpr_all, tpr_all, color=t['line'], lw=1.6, drawstyle='steps-post')
            axr.plot([0, 1], [0, 1], color=t['line'], lw=1, ls=(0, (3, 3)))
            fpr, tpr = fp / max(1, fp + tn), tp / max(1, tp + fn)
            axr.scatter([fpr], [tpr], s=90, color=t['clay'], zorder=4)
            axr.set_xlim(-.02, 1.02); axr.set_ylim(-.02, 1.02)
            axr.set_xticks([0, 1]); axr.set_yticks([0, 1])
            axr.tick_params(colors=t['muted'], labelsize=9, length=2)
            for s in ['top', 'right']:
                axr.spines[s].set_visible(False)
            for s in ['left', 'bottom']:
                axr.spines[s].set_color(t['line'])
            axr.set_xlabel('FPR', color=t['muted'], fontsize=9.5); axr.set_ylabel('TPR', color=t['muted'], fontsize=9.5)
            frames.append(grab(fig))
        return frames

    labels = []
    for th in ths:
        tp, fp, fn, tn = stats(th)
        prec = tp / (tp + fp) if tp + fp else float('nan')
        rec = tp / (tp + fn)
        labels.append(f'threshold {th:g}: TP {tp}, FP {fp}, FN {fn}, TN {tn}; precision ' + ('—' if prec != prec else f'{prec:.2f}') + f', recall {rec:.2f}')
    return Anim('1-5-threshold', 'Mười mẫu validation của bài khi hạ threshold từ 1 xuống 0: confusion matrix đổi theo, và điểm (FPR, TPR) chạy dọc đường ROC.',
                labels, draw, dur=1300, hold=2200, key=[2, 6, 9, 11], photo=False, themed=True)


# ───────────────────────────── 1.6 ─────────────────────────────

def a1_6_outlier():
    ns = lesson_ns('1.6', upto=1)
    y, pred0 = ns['y'], ns['prediction']
    errs = [-3, -6, -10, -15, -20, -30, -45]

    def scores(e):
        pr = pred0.copy(); pr[2] = y[2] + e
        r = pr - y
        return pr, np.abs(r).mean(), np.sqrt((r ** 2).mean())

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for e in errs:
            pr, mae, rmse = scores(e)
            fig = fig_frame(960, 400)
            ax = fig.add_axes((.06, .12, .5, .8)); ax.patch.set_alpha(0)
            for i in range(3):
                ax.plot([i, i], [y[i], pr[i]], color=t['clay'], lw=2.4)
                ax.scatter(i, y[i], s=80, color=t['blue'], zorder=3)
                ax.scatter(i, pr[i], s=80, color=t['clay'], zorder=3, marker='D')
            ax.set_xlim(-.6, 2.6); ax.set_ylim(-20, 36)
            ax.set_xticks([0, 1, 2]); ax.set_xticklabels(['mẫu 1', 'mẫu 2', 'mẫu 3'], color=t['muted'], fontsize=10)
            ax.tick_params(colors=t['muted'], labelsize=9, length=0)
            for s in ['top', 'right']:
                ax.spines[s].set_visible(False)
            for s in ['left', 'bottom']:
                ax.spines[s].set_color(t['line'])
            axb = fig.add_axes((.66, .12, .3, .8)); axb.patch.set_alpha(0)
            axb.bar([0, 1], [mae, rmse], color=[t['blue'], t['clay']], width=.6)
            for k, v in enumerate([mae, rmse]):
                axb.text(k, v + .8, f'{v:.2f}', ha='center', color=t['text'], fontsize=12)
            axb.set_xticks([0, 1]); axb.set_xticklabels(['MAE', 'RMSE'], color=t['text'], fontsize=11)
            axb.set_ylim(0, 30); axb.set_yticks([])
            for s in axb.spines.values():
                s.set_visible(False)
            axb.tick_params(length=0)
            frames.append(grab(fig))
        return frames

    labels = [f'mẫu 3 lệch {abs(e)}: MAE {scores(e)[1]:.2f}, RMSE {scores(e)[2]:.2f}' for e in errs]
    return Anim('1-6-outlier', 'Ba mẫu của ví dụ trong bài, chỉ mẫu 3 lệch ngày càng xa: MAE tăng theo đúng phần lệch chia 3, RMSE tăng nhanh hơn vì bình phương dồn trọng số vào lỗi lớn.',
                labels, draw, dur=1300, hold=2200, key=[0, 2, 4, 6], photo=False, themed=True)


# ───────────────────────────── 1.7 ─────────────────────────────

def a1_7_search():
    ns = lesson_ns('1.7', upto=3)
    from sklearn.base import clone
    from sklearn.model_selection import cross_val_score
    pipe, cv, X, y = ns['pipeline'], ns['cv'], ns['X_dev'], ns['y_dev']
    ks = list(range(3, 34, 2))
    land = {w: [cross_val_score(clone(pipe).set_params(knn__n_neighbors=k, knn__weights=w), X, y, scoring='f1', cv=cv).mean() for k in ks]
            for w in ['uniform', 'distance']}
    grid_pts = [(p['knn__n_neighbors'], p['knn__weights']) for p in ns['grid'].cv_results_['params']]
    rand_pts = [(p['knn__n_neighbors'], p['knn__weights']) for p in ns['random_search'].cv_results_['params']]
    seq = [('land', None, 0)] + [('grid', grid_pts, i + 1) for i in range(len(grid_pts))] + [('rand', rand_pts, i + 1) for i in range(len(rand_pts))]

    def score(k, w):
        return land[w][ks.index(k)]

    def draw(theme):
        t = THEMES[theme]
        cols = {'uniform': t['blue'], 'distance': t['clay']}
        frames = []
        for kind, pts, n in seq:
            fig, ax = plain_axes(theme, 960, 440, (.07, .12, .9, .82))
            for w, c in cols.items():
                ax.plot(ks, land[w], color=c, lw=1.4, alpha=.45)
                ax.text(ks[-1] + .4, land[w][-1], w, color=c, fontsize=10, va='center')
            if kind != 'land':
                shown = pts[:n]
                for k, w in shown:
                    ax.scatter(k, score(k, w), s=110, color=cols[w], zorder=4, marker='s' if kind == 'grid' else 'o',
                               edgecolors=t['text'], linewidths=1)
                bk, bw = max(shown, key=lambda kw: score(*kw))
                ax.scatter(bk, score(bk, bw), s=380, facecolors='none', edgecolors=t['text'], linewidths=1.6, zorder=5)
            ax.set_xlim(1, 38); ax.set_xticks([3, 9, 15, 21, 27, 33])
            ax.set_xlabel('n_neighbors', color=t['muted'], fontsize=10)
            ax.set_ylabel('F1 cross-validation', color=t['muted'], fontsize=10)
            frames.append(grab(fig))
        return frames

    labels = ['F1 cross-validation của mọi k lẻ từ 3 tới 33, hai kiểu weights (nét mờ, chỉ để nhìn; thường không có)']
    for kind, pts, n in seq[1:]:
        k, w = pts[n - 1]
        best = max(pts[:n], key=lambda kw: score(*kw))
        labels.append(f'{"grid" if kind == "grid" else "random"} thử {n}/{len(pts)}: k = {k}, {w}, F1 {score(k, w):.3f}; tốt nhất đến giờ k = {best[0]}, {best[1]}')
    return Anim('1-7-search', 'Cùng pipeline và cross-validation của bài: grid search thử 6 tổ hợp cố định (ô vuông), random search bốc 4 tổ hợp (chấm tròn); vòng lớn là tổ hợp tốt nhất đã thấy.',
                labels, draw, dur=[2200] + [800] * len(grid_pts) + [1100] * len(rand_pts), hold=2400, key=[0, 6, 10], photo=False, themed=True, pcols=3)


ANIMS = [a1_1_row, a1_2_k, a1_3_oof, a1_4_table, a1_5_threshold, a1_6_outlier, a1_7_search]
