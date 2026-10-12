"""Hình động chương 2 (học máy cổ điển). Số liệu chạy lại từ code bài (lesson_ns) hoặc từ đúng dữ liệu của hình lượt 8.
Ảnh thật: china.jpg, flower.jpg (scikit-learn, CC BY 2.0)."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, sample,  # noqa: E402
                  plain_axes, fig_frame, grab, LORA)
from p8_ch1 import lesson_ns  # noqa: E402


def bare(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def regions(ax, pred, extent, theme, alpha=.16):
    """Tô vùng hai lớp: pred là bảng 0/1 trên lưới (hàng = y tăng dần)."""
    t = THEMES[theme]
    from matplotlib.colors import ListedColormap
    ax.imshow(pred, origin='lower', extent=extent, cmap=ListedColormap([t['blue'], t['clay']]), alpha=alpha,
              interpolation='nearest', aspect='auto', vmin=0, vmax=1)


def dots(ax, X, y, theme, s=9):
    t = THEMES[theme]
    for lab, col in [(0, t['blue']), (1, t['clay'])]:
        k = y == lab
        ax.scatter(X[k, 0], X[k, 1], s=s, color=col, linewidths=0, alpha=.9)


# ───────────────────────────── 2.1 ─────────────────────────────

def a2_1_race():
    """Cùng gradient descent của bài: dữ liệu gốc (η = 10⁻⁴) và dữ liệu đã chuẩn hóa (η = 0.1), giá dự đoán so với giá thật."""
    ns = lesson_ns('2.1')
    X, y, gd, predict = ns['X'], ns['y'], ns['gd'], ns['predict']
    mu, sigma = X.mean(0), X.std(0)
    Xs = (X - mu) / sigma
    epochs = [0, 1, 2, 3, 5, 8, 13, 20, 30, 50, 100, 300, 1000]
    runs = []
    for e in epochs:
        a, ha = gd(X, y, 1e-4, e) if e else (np.zeros(3), [])
        b, hb = gd(Xs, y, .1, e) if e else (np.zeros(3), [])
        runs.append((predict(X, a[:2], a[2]), predict(Xs, b[:2], b[2])))
    mse = lambda p: float(np.mean((p - y) ** 2))
    lo, hi = -.3, 7.6

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for pa, pb in runs:
            fig = fig_frame(960, 470)
            for k, (p, title) in enumerate([(pa, 'dữ liệu gốc, η = 10⁻⁴'), (pb, 'đã chuẩn hóa, η = 0.1')]):
                ax = fig.add_axes((.07 + k * .5, .13, .38, .74))
                ax.patch.set_alpha(0)
                ax.plot([lo, hi], [lo, hi], color=t['line'], lw=1.2, zorder=1)
                ax.scatter(y, np.clip(p, lo, hi), s=10, color=t['blue'] if k == 0 else t['clay'], linewidths=0, alpha=.85, zorder=2)
                ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
                ax.set_xticks([0, 2, 4, 6]); ax.set_yticks([0, 2, 4, 6])
                ax.tick_params(colors=t['muted'], labelsize=9, length=3)
                for s in ['left', 'bottom']:
                    ax.spines[s].set_color(t['line'])
                ax.set_xlabel('giá thật (tỷ)', color=t['muted'], fontsize=9.5)
                if k == 0:
                    ax.set_ylabel('giá dự đoán (tỷ)', color=t['muted'], fontsize=9.5)
                ax.set_title(title, color=t['text'], fontsize=11, pad=8)
            frames.append(grab(fig))
        return frames

    labels = [f'vòng {e}: MSE gốc {mse(pa):.3g}, đã chuẩn hóa {mse(pb):.3g}' for e, (pa, pb) in zip(epochs, runs)]
    return Anim('2-1-race', 'Cùng gradient descent trên 200 căn hộ: dữ liệu gốc tiến nhanh vài vòng đầu rồi gần như đứng yên; dữ liệu đã chuẩn hóa về sát đường chéo sau khoảng 20 vòng.',
                labels, draw, dur=[1100] + [800] * 11 + [600], hold=2800, key=[1, 4, 7, 12], photo=False, themed=True)


# ───────────────────────────── 2.2 ─────────────────────────────

def a2_2_shrink():
    """Hệ số của Ridge và Lasso (code bài) khi λ tăng: Ridge co đều, Lasso đưa từng hệ số về đúng 0."""
    ns = lesson_ns('2.2')
    A_tr, y_tr, A_te, y_te = ns['A_tr'], ns['y_tr'], ns['A_te'], ns['y_te']
    fit_ridge, fit_lasso, r2 = ns['fit_ridge'], ns['fit_lasso'], ns['r2']
    lams = [0.01, 0.1, 0.3, 1, 2, 4, 8, 12, 20, 30, 50, 80]
    R, L = [], []
    for lam in lams:
        wr, br = fit_ridge(A_tr, y_tr, lam)
        wl, bl = fit_lasso(A_tr, y_tr, lam, sweeps=300)
        R.append((wr, r2(A_te @ wr + br, y_te)))
        L.append((wl, r2(A_te @ wl + bl, y_te), int((np.abs(wl) > 1e-9).sum())))
    top = max(np.abs(R[0][0]).max(), np.abs(L[0][0]).max()) * 1.05

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for (wr, _), (wl, _, _) in zip(R, L):
            fig = fig_frame(960, 440)
            for k, (w, title) in enumerate([(wr, 'Ridge'), (wl, 'Lasso')]):
                ax = fig.add_axes((.04 + k * .5, .1, .44, .78))
                ax.patch.set_alpha(0)
                cols = [t['clay'], t['blue']] + [t['faint']] * (len(w) - 2)
                ax.bar(np.arange(len(w)), w, color=cols, width=.75)
                ax.axhline(0, color=t['line'], lw=1)
                ax.set_ylim(-top, top)
                ax.set_xlim(-1, len(w))
                bare(ax)
                ax.set_title(title, color=t['text'], fontsize=11.5, pad=6)
            frames.append(grab(fig))
        return frames

    labels = [f'λ = {lam:g}: R² test Ridge {rr:.2f}, Lasso {rl:.2f}; Lasso còn {nz}/32 hệ số khác 0'
              for lam, (_, rr), (_, rl, nz) in zip(lams, R, L)]
    return Anim('2-2-shrink', 'Hệ số của Ridge và Lasso khi λ tăng (cam: diện tích, xanh: khoảng cách, xám: 30 cột rác): Ridge co đều, Lasso đưa từng hệ số về đúng 0.',
                labels, draw, dur=900, hold=2600, key=[0, 4, 7, 11], photo=False, themed=True)


# ───────────────────────────── 2.3 ─────────────────────────────

def a2_3_boundary():
    """Ranh giới p = 0.5 và dải p = 0.1…0.9 dịch dần theo gradient descent của bài (η = 0.5) trên 300 email train."""
    ns = lesson_ns('2.3')
    X, y, grad, loss = ns['X_tr'], ns['y_tr'], ns['grad'], ns['loss']
    snaps = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 5000]
    theta = np.zeros(3)
    states = {}
    for e in range(snaps[-1] + 1):
        if e in snaps:
            states[e] = theta.copy()
        theta -= .5 * grad(theta, X, y)
    rng = np.random.default_rng(23)
    J = rng.uniform(-.22, .22, X.shape)
    xs, ys = np.linspace(-.6, 8.4, 181), np.linspace(-.6, 6.6, 145)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for e in snaps:
            th = states[e]
            fig, ax = plain_axes(theme, 960, 470, (.08, .13, .84, .8))
            z = (G @ th[:2] + th[2]).reshape(len(ys), len(xs))
            p = 1 / (1 + np.exp(-z))
            ax.contourf(xs, ys, p, levels=[0, .1, .5, .9, 1], colors=[t['blue'], t['blue'], t['clay'], t['clay']],
                        alpha=.0)
            ax.imshow(np.where(p > .5, 1, 0), origin='lower', extent=(xs[0], xs[-1], ys[0], ys[-1]), aspect='auto',
                      cmap=__import__('matplotlib.colors', fromlist=['x']).ListedColormap([t['blue'], t['clay']]), alpha=.12)
            if abs(th[1]) > 1e-9:
                for lvl, lw, ls in [(.1, 1, (0, (4, 3))), (.5, 2, '-'), (.9, 1, (0, (4, 3)))]:
                    ax.contour(xs, ys, p, levels=[lvl], colors=[t['text']], linewidths=lw, linestyles=[ls])
            dots(ax, X + J, y, theme, s=11)
            ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1])
            ax.set_xlabel('số link', color=t['muted'], fontsize=9.5)
            ax.set_ylabel('từ quảng cáo', color=t['muted'], fontsize=9.5)
            frames.append(grab(fig))
        return frames

    labels = []
    for e in snaps:
        th = states[e]
        labels.append(f'vòng {e}: loss {loss(th, X, y):.4f}' + ('; mọi email p = 0.5' if e == 0 else
                      f'; w = ({th[0]:.2f}, {th[1]:.2f}), b = {th[2]:.2f}'))
    return Anim('2-3-boundary', 'Gradient descent của bài trên 300 email: ranh giới p = 0.5 (nét liền) và hai mức 0.1, 0.9 (nét đứt) dịch dần về chỗ tách spam.',
                labels, draw, dur=[1300] + [800] * 10 + [600], hold=2800, key=[1, 4, 7, 11], photo=False, themed=True)


# ───────────────────────────── 2.4 ─────────────────────────────

def moons():
    from sklearn.datasets import make_moons
    return make_moons(200, noise=.3, random_state=0)   # cùng dữ liệu hình 2-4-k, 2-5-partition, 2-6-trees


def a2_4_k():
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import cross_val_score
    X, y = moons()
    ks = [1, 2, 3, 5, 8, 12, 15, 20, 30, 50, 80, 120]
    xs, ys = np.linspace(-1.6, 2.6, 211), np.linspace(-1.3, 1.7, 151)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    preds, cv = [], []
    for k in ks:
        m = KNeighborsClassifier(k).fit(X, y)
        preds.append(m.predict(G).reshape(len(ys), len(xs)))
        cv.append(cross_val_score(KNeighborsClassifier(k), X, y, cv=5).mean())

    def draw(theme):
        frames = []
        for p in preds:
            fig = fig_frame(960, 690)
            ax = fig.add_axes((0, 0, 1, 1))
            ax.patch.set_alpha(0)
            regions(ax, p, (xs[0], xs[-1], ys[0], ys[-1]), theme, .17)
            dots(ax, X, y, theme, s=16)
            ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1])
            bare(ax)
            frames.append(grab(fig))
        return frames

    labels = [f'k = {k}: accuracy 5-fold CV {c:.3f}' for k, c in zip(ks, cv)]
    return Anim('2-4-k', 'Cùng 200 điểm của hình trên, tăng k từ 1 tới 120: ranh giới đi từ bám từng điểm nhiễu tới quá phẳng.',
                labels, draw, dur=900, hold=2400, key=[0, 6, 9, 11], photo=False, themed=True, display=600)


# ───────────────── 2.5 – 2.7: cây, rừng, boosting trên cùng một ảnh thật ─────────────────

def photo_task():
    """Hồi quy màu theo tọa độ trên ảnh tháp 112×112: học từ 25% điểm ảnh ngẫu nhiên, chấm trên 75% còn lại."""
    img = np.asarray(Image.fromarray(sample('china.jpg')).crop((40, 20, 400, 380)).resize((112, 112), Image.LANCZOS), float)
    H, W = img.shape[:2]
    rr, cc = np.mgrid[0:H, 0:W]
    P = np.c_[rr.ravel(), cc.ravel()].astype(float)
    Y = img.reshape(-1, 3)
    rng = np.random.default_rng(25)
    tr = rng.random(len(P)) < .25
    return img, P, Y, tr


def rmse(pred, Y, mask):
    return float(np.sqrt(np.mean((pred[mask] - Y[mask]) ** 2)))


def seen(img, tr):
    """Ảnh chỉ còn các điểm train (điểm khác để trống) — cho thấy model học từ đâu."""
    a = np.concatenate([img, np.full(img.shape[:2] + (1,), 255.)], -1)
    a[~tr.reshape(img.shape[:2])] = 0
    return a.astype(np.uint8)


def two_panel(left, right, theme, size=420, gap=40):
    cv = canvas(2 * size + gap + 40, size + 20)
    paste(cv, left, 20, 10, size, size, nearest=True, radius=6)
    paste(cv, right, 20 + size + gap, 10, size, size, nearest=True, radius=6)
    return arr(cv)


def a2_5_photo():
    from sklearn.tree import DecisionTreeRegressor
    img, P, Y, tr = photo_task()
    depths = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 24]
    outs, errs, leaves = [], [], []
    for d in depths:
        m = DecisionTreeRegressor(max_depth=d, random_state=0).fit(P[tr], Y[tr])
        p = m.predict(P)
        outs.append(p.reshape(img.shape))
        errs.append((rmse(p, Y, tr), rmse(p, Y, ~tr)))
        leaves.append(m.get_n_leaves())

    def draw(theme):
        return [two_panel(seen(img, tr), o, theme) for o in outs]

    labels = [f'độ sâu {d}: {n} lá, RMSE train {a:.1f}, RMSE điểm chưa thấy {b:.1f}' for d, n, (a, b) in zip(depths, leaves, errs)]
    return Anim('2-5-photo', 'Decision tree đoán màu theo tọa độ, học từ 25% điểm ảnh (trái): mỗi lá là một hình chữ nhật một màu; càng sâu càng thuộc điểm train, còn điểm chưa thấy dừng ở mức sai cỡ 25.',
                labels, draw, dur=1000, hold=2600, key=[1, 4, 7, 10], themed=False, display=600)


def a2_6_photo():
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import DecisionTreeRegressor
    img, P, Y, tr = photo_task()
    forest = RandomForestRegressor(n_estimators=100, max_features=1, random_state=0, n_jobs=-1).fit(P[tr], Y[tr])
    per_tree = np.stack([e.predict(P) for e in forest.estimators_])
    Ts = [1, 2, 3, 5, 8, 12, 20, 35, 60, 100]
    outs, errs = [], []
    for T in Ts:
        p = per_tree[:T].mean(0)
        outs.append(p.reshape(img.shape))
        errs.append(rmse(p, Y, ~tr))
    full = DecisionTreeRegressor(random_state=0).fit(P[tr], Y[tr]).predict(P)
    e_tree = rmse(full, Y, ~tr)

    def draw(theme):
        return [two_panel(seen(img, tr), o, theme) for o in outs]

    labels = [f'trung bình {T} cây: RMSE điểm chưa thấy {e:.1f}' + (f' (một cây sâu không bootstrap: {e_tree:.1f})' if T == 1 else '')
              for T, e in zip(Ts, errs)]
    return Anim('2-6-photo', 'Random forest trên cùng bài đoán màu: mỗi cây học một mẫu bootstrap nên sai theo kiểu riêng; lấy trung bình nhiều cây thì ảnh mượt hơn và sai số trên điểm chưa thấy giảm.',
                labels, draw, dur=1000, hold=2600, key=[0, 3, 6, 9], themed=False, display=600)


def a2_7_photo():
    from sklearn.ensemble import GradientBoostingRegressor
    img, P, Y, tr = photo_task()
    stages = [1, 2, 3, 5, 10, 20, 40, 80, 150, 300]
    outs, errs = [], []
    preds = np.zeros((len(stages), len(P), 3))
    for c in range(3):
        m = GradientBoostingRegressor(n_estimators=stages[-1], max_depth=5, learning_rate=.2, random_state=0).fit(P[tr], Y[tr, c])
        allp = list(m.staged_predict(P))
        for k, s in enumerate(stages):
            preds[k, :, c] = allp[s - 1]
    for k in range(len(stages)):
        outs.append(preds[k].reshape(img.shape))
        errs.append((rmse(preds[k], Y, tr), rmse(preds[k], Y, ~tr)))

    def resid(p):
        r = np.abs(Y - p).mean(1).reshape(img.shape[:2])
        v = (255 - 225 * np.clip(r / 80, 0, 1))
        return np.repeat(v[..., None], 3, 2)

    def draw(theme):
        frames = []
        for p in outs:
            cv = canvas(960, 330)
            for k, im in enumerate([img, p, resid(p.reshape(-1, 3))]):
                paste(cv, im, 20 + k * 315, 10, 300, 300, nearest=True, radius=6)
            frames.append(arr(cv))
        return frames

    labels = [f'{s} cây độ sâu 5, η = 0.2: RMSE train {a:.1f}, điểm chưa thấy {b:.1f}' for s, (a, b) in zip(stages, errs)]
    return Anim('2-7-photo', 'Gradient boosting trên cùng bài đoán màu: ảnh gốc, dự đoán sau m cây, và phần dư (càng đậm càng sai) mà cây tiếp theo phải sửa.',
                labels, draw, dur=1000, hold=2600, key=[0, 3, 6, 9], themed=False)


# ───────────────────────────── 2.8 ─────────────────────────────

def a2_8_gamma():
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score
    X, y = moons()
    X = StandardScaler().fit_transform(X)
    gs = [.01, .03, .1, .3, 1, 3, 10, 30, 100, 300]
    xs = ys = np.linspace(-2.4, 2.4, 241)
    G = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    res = []
    for g in gs:
        m = SVC(kernel='rbf', C=1, gamma=g).fit(X, y)
        res.append((m.decision_function(G).reshape(len(ys), len(xs)), m.support_, cross_val_score(SVC(kernel='rbf', C=1, gamma=g), X, y, cv=5).mean()))

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for f, sv, _ in res:
            fig = fig_frame(720, 720)
            ax = fig.add_axes((0, 0, 1, 1))
            ax.patch.set_alpha(0)
            regions(ax, (f > 0).astype(int), (-2.4, 2.4, -2.4, 2.4), theme, .17)
            ax.contour(xs, ys, f, levels=[0], colors=[t['text']], linewidths=1.6)
            ax.contour(xs, ys, f, levels=[-1, 1], colors=[t['muted']], linewidths=1, linestyles=[(0, (4, 3))])
            dots(ax, X, y, theme, s=14)
            ax.scatter(X[sv, 0], X[sv, 1], s=60, facecolors='none', edgecolors=t['text'], linewidths=.7)
            ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
            bare(ax)
            frames.append(grab(fig))
        return frames

    labels = [f'γ = {g:g}: {len(sv)} support vector, accuracy 5-fold CV {c:.3f}' for g, (_, sv, c) in zip(gs, res)]
    return Anim('2-8-gamma', 'SVM kernel RBF, C = 1, trên dữ liệu trăng khuyết: tăng γ thì vùng ảnh hưởng của mỗi điểm hẹp lại, ranh giới uốn theo từng điểm (vòng tròn là support vector).',
                labels, draw, dur=1000, hold=2600, key=[0, 4, 7, 9], photo=False, themed=True, display=480)


def a2_8_lift():
    """Mười điểm trên một trục (dữ liệu hình 2-8-kernel) được nâng lên (x, x²): một đường ngang tách được hai lớp."""
    x = np.array([-2.6, -2.2, -1.8, -.4, -.1, .3, .6, 1.9, 2.3, 2.7])
    lab = (np.abs(x) > 1.2).astype(int)
    fs = [0, 0] + [ease(i / 7) for i in range(1, 8)] + [1, 1]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for k, f in enumerate(fs):
            fig, ax = plain_axes(theme, 960, 470, (.1, .12, .8, .8))
            xx = np.linspace(-3, 3, 200)
            ax.plot(xx, f * xx ** 2, color=t['line'], lw=1.2, alpha=f)
            ax.axhline(0, color=t['line'], lw=1)
            for l, col in [(0, t['blue']), (1, t['clay'])]:
                m = lab == l
                ax.scatter(x[m], f * x[m] ** 2, s=110, color=col, zorder=3, linewidths=0)
            if k >= len(fs) - 2:
                ax.axhline(2.25, color=t['text'], lw=1.8, ls='-')
            ax.set_xlim(-3, 3); ax.set_ylim(-.6, 8)
            ax.set_xticks([-2, 0, 2]); ax.set_yticks([0, 4, 8] if f > .3 else [])
            ax.set_xlabel('x', color=t['muted'], fontsize=10)
            ax.set_ylabel('x²' if f > .3 else '', color=t['muted'], fontsize=10)
            frames.append(grab(fig))
        return frames

    labels = ['trên trục x: lớp cam nằm hai đầu, lớp xanh ở giữa', 'không vạch nào trên trục tách được hai lớp'] + \
             ['nâng mỗi điểm lên độ cao x²'] * 7 + ['đường ngang x² = 2.25 tách hai lớp', 'trên trục x, đường ngang ấy ứng với hai ngưỡng x = ±1.5']
    return Anim('2-8-lift', 'Nâng mười điểm từ trục x lên (x, x²): hai lớp không tách được bằng một ngưỡng trên trục lại tách được bằng một đường thẳng.',
                labels, draw, dur=[1500, 1300] + [200] * 6 + [900] + [1800, 1800], hold=1800, key=[0, 5, 8, 9], photo=False, themed=True)


# ───────────────────────────── 2.9 ─────────────────────────────

def a2_9_svd():
    g = np.asarray(Image.fromarray(sample('china.jpg')).crop((40, 20, 400, 380)).convert('L').resize((256, 256), Image.LANCZOS), float)
    mean = g.mean(0)
    U, s, Vt = np.linalg.svd(g - mean, full_matrices=False)
    ks = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 128]
    share = np.cumsum(s ** 2) / np.sum(s ** 2)
    recon = [np.clip((U[:, :k] * s[:k]) @ Vt[:k] + mean, 0, 255) for k in ks]

    def draw(theme):
        frames = []
        for r in recon:
            cv = canvas(900, 440)
            paste(cv, np.repeat(g[..., None], 3, 2), 10, 10, 420, 420, radius=6)
            paste(cv, np.repeat(r[..., None], 3, 2), 470, 10, 420, 420, radius=6)
            frames.append(arr(cv))
        return frames

    labels = [f'giữ {k} thành phần: {k * (256 + 256 + 1) + 256:,} số thay cho {256 * 256:,}'.replace(',', ' ')
              + f'; phương sai giữ lại {share[k - 1]:.1%}' for k in ks]
    return Anim('2-9-svd', 'PCA trên 256 hàng của ảnh tháp (tính bằng SVD): ảnh gốc và ảnh dựng lại từ k thành phần đầu.',
                labels, draw, dur=1000, hold=2600, key=[0, 4, 6, 9], themed=False, display=600)


# ───────────────────────────── 2.10 ─────────────────────────────

def a2_10_colors():
    """K-Means (Lloyd, khởi tạo ngẫu nhiên) gom màu ảnh hoa thành 6 màu: ảnh và bảng màu sau từng vòng."""
    img = np.asarray(Image.fromarray(sample('flower.jpg')).resize((240, 160), Image.LANCZOS), float)
    Xp = img.reshape(-1, 3)
    rng = np.random.default_rng(10)
    K = 6
    C = Xp[rng.choice(len(Xp), K, replace=False)]
    states = []
    for it in range(12):
        d = ((Xp[:, None, :] - C[None]) ** 2).sum(2)
        a = d.argmin(1)
        inertia = float(d[np.arange(len(Xp)), a].sum())
        states.append((C.copy(), a.copy(), inertia))
        newC = np.array([Xp[a == k].mean(0) if (a == k).any() else C[k] for k in range(K)])
        if np.allclose(newC, C):
            break
        C = newC

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for C_, a, _ in states:
            cv = canvas(960, 330)
            paste(cv, img, 10, 10, 450, 300, radius=6)
            q = C_[a].reshape(img.shape)
            paste(cv, q, 490, 10, 450, 300, radius=6)
            frames.append(arr(cv))
        return frames

    labels = [f'vòng {i}: inertia {s[2] / 1e6:.1f} triệu' + (' (tâm là 6 điểm ảnh lấy ngẫu nhiên)' if i == 0 else '') for i, s in enumerate(states)]
    labels[-1] += '; tâm không đổi nữa, dừng'
    return Anim('2-10-colors', 'K-Means gom các màu của ảnh hoa thành 6 cụm: sau mỗi vòng gán rồi lấy trung bình, mỗi điểm ảnh được tô bằng màu tâm cụm của nó.',
                labels, draw, dur=900, hold=2600, key=[0, 1, 3, len(states) - 1], themed=False)


# ───────────────────────────── 2.11 ─────────────────────────────

def a2_11_cyclic():
    hours = list(range(18, 24)) + list(range(0, 7))

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for k, h in enumerate(hours):
            fig = fig_frame(960, 420)
            ax = fig.add_axes((.05, .2, .5, .6))
            ax.patch.set_alpha(0)
            ax.plot([0, 23], [0, 0], color=t['line'], lw=2)
            for v in [0, 6, 12, 18, 23]:
                ax.text(v, -.35, str(v), color=t['muted'], ha='center', va='top', fontsize=10)
            trail = hours[max(0, k - 3):k + 1]
            for j, hh in enumerate(trail):
                ax.scatter([hh], [0], s=150 if hh == h else 60, color=t['clay'], alpha=1 if hh == h else .25 + .2 * j, zorder=3, linewidths=0)
            ax.set_xlim(-1.5, 24.5); ax.set_ylim(-1, 1)
            bare(ax)
            ax.set_title('giờ là một số', color=t['text'], fontsize=11)
            ax2 = fig.add_axes((.64, .08, .3, .84))
            ax2.patch.set_alpha(0)
            th = np.linspace(0, 2 * np.pi, 200)
            ax2.plot(np.sin(th), np.cos(th), color=t['line'], lw=2)
            for v in [0, 6, 12, 18]:
                a = 2 * np.pi * v / 24
                ax2.text(1.22 * np.sin(a), 1.22 * np.cos(a), str(v), color=t['muted'], ha='center', va='center', fontsize=10)
            for j, hh in enumerate(trail):
                a = 2 * np.pi * hh / 24
                ax2.scatter([np.sin(a)], [np.cos(a)], s=150 if hh == h else 60, color=t['blue'], alpha=1 if hh == h else .25 + .2 * j, zorder=3, linewidths=0)
            ax2.set_xlim(-1.45, 1.45); ax2.set_ylim(-1.45, 1.45); ax2.set_aspect('equal')
            bare(ax2)
            ax2.set_title('(sin, cos) của giờ', color=t['text'], fontsize=11)
            frames.append(grab(fig))
        return frames

    labels = []
    for h in hours:
        a = 2 * np.pi * h / 24
        labels.append(f'{h} giờ: sin {np.sin(a):+.2f}, cos {np.cos(a):+.2f}'.replace('-', '−'))
    labels[hours.index(0)] += ' · trên trục số nhảy từ 23 về 0, trên vòng tròn chỉ đi một bước'
    return Anim('2-11-cyclic', 'Giờ trong ngày chạy từ 18 giờ qua nửa đêm: trên trục số 23 và 0 cách nhau xa nhất; mã hóa (sin, cos) đặt chúng cạnh nhau trên vòng tròn.',
                labels, draw, dur=[700] * 5 + [1200, 2400] + [700] * 6, hold=1500, key=[3, 5, 6, 9], photo=False, themed=True)


ANIMS = [a2_1_race, a2_2_shrink, a2_3_boundary, a2_4_k, a2_5_photo, a2_6_photo, a2_7_photo, a2_8_gamma, a2_8_lift,
         a2_9_svd, a2_10_colors, a2_11_cyclic]


# ───────────────────────────── kt1 ─────────────────────────────

def a2_kt1_folds():
    """Đúng ba fold của buổi kiểm tra: baseline trung vị và Ridge dự đoán phần validation của từng fold."""
    from sklearn.base import clone
    from sklearn.metrics import mean_absolute_error
    from p8_ch5 import kt_ns
    ns = kt_ns(2, 'kt1', upto=1)
    X, y, folds, cands = ns['X_train'], ns['y_train'], ns['folds'], ns['candidates']
    res = []
    for tr, va in folds:
        out = {}
        for name, m in cands.items():
            p = clone(m).fit(X[tr], y[tr]).predict(X[va])
            out[name] = (p, mean_absolute_error(y[va], p))
        res.append((va, out))
    lo, hi = y.min() - .5, y.max() + .5

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for va, out in res:
            fig = fig_frame(960, 440)
            for j, (name, col) in enumerate([('median', t['blue']), ('ridge', t['clay'])]):
                ax = fig.add_axes((.07 + j * .5, .13, .38, .78)); ax.patch.set_alpha(0)
                ax.plot([lo, hi], [lo, hi], color=t['line'], lw=1.2)
                ax.scatter(y[va], out[name][0], s=26, color=col, linewidths=0, zorder=3)
                for yt, yp in zip(y[va], out[name][0]):
                    ax.plot([yt, yt], [yt, yp], color=col, lw=.8, alpha=.5)
                ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
                ax.tick_params(colors=t['muted'], labelsize=9, length=2)
                for s in ['top', 'right']:
                    ax.spines[s].set_visible(False)
                for s in ['left', 'bottom']:
                    ax.spines[s].set_color(t['line'])
                ax.set_title(f'{name}: MAE {out[name][1]:.3f}', color=t['text'], fontsize=11.5)
                ax.set_xlabel('y thật', color=t['muted'], fontsize=9.5)
                if j == 0:
                    ax.set_ylabel('dự đoán', color=t['muted'], fontsize=9.5)
            frames.append(grab(fig))
        return frames

    labels = [f'fold {k + 1}: {len(va)} mẫu validation; đoạn đứng là sai số của từng mẫu' for k, (va, _) in enumerate(res)]
    m_med = np.mean([o['median'][1] for _, o in res])
    m_r = np.mean([o['ridge'][1] for _, o in res])
    labels[-1] += f'; MAE trung bình ba fold: median {m_med:.3f}, ridge {m_r:.3f}'
    return Anim('2-kt1-folds', 'Ba fold của buổi kiểm tra: baseline trung vị đoán một hằng số cho mọi mẫu, Ridge đoán gần đường chéo; cả hai được chấm trên đúng cùng những mẫu.',
                labels, draw, dur=2200, hold=1600, key=[0, 1, 2], photo=False, themed=True, pcols=1)


ANIMS.append(a2_kt1_folds)
