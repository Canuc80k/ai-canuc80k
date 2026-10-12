"""Hình động chương 3 (mạng neural). Ảnh thật: china.jpg, flower.jpg (scikit-learn, CC BY 2.0); Fashion-MNIST (Zalando, MIT).
Model thật: all-MiniLM-L6-v2 (sentence-transformers) cho attention."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, sample,  # noqa: E402
                  plain_axes, fig_frame, grab)
from p8_ch1 import lesson_ns  # noqa: E402
from a_ch2 import bare  # noqa: E402


# ───────────────────────────── 3.1 ─────────────────────────────

def a3_1_permute():
    """Ảnh (H, W, 3) đổi sang (3, H, W): permute giữ ý nghĩa từng kênh, reshape thì trộn các kênh với nhau."""
    import torch
    img = np.asarray(Image.fromarray(sample('flower.jpg')).crop((140, 40, 500, 400)).resize((96, 96), Image.LANCZOS))
    x = torch.tensor(img)
    good = x.permute(2, 0, 1).numpy()          # (3, 96, 96)
    bad = x.reshape(3, 96, 96).numpy()         # cùng shape, sai ý nghĩa
    back = torch.tensor(bad).permute(1, 2, 0).numpy()

    def planes(cv, P):
        for c in range(3):
            g = P[c]
            tint = np.zeros((96, 96, 3), np.uint8)
            tint[..., c] = g                    # kênh R/G/B tô đúng màu của nó
            paste(cv, tint, 30 + c * 310, 20, 280, 280, nearest=True, radius=6)

    def draw(theme):
        frames = []
        cv = canvas(960, 320); paste(cv, img, 340, 20, 280, 280, nearest=True, radius=6); frames.append(arr(cv))
        cv = canvas(960, 320); planes(cv, good); frames.append(arr(cv))
        cv = canvas(960, 320); planes(cv, bad); frames.append(arr(cv))
        cv = canvas(960, 320); paste(cv, back, 340, 20, 280, 280, nearest=True, radius=6); frames.append(arr(cv))
        return frames

    labels = ['`x`: shape (96, 96, 3), kênh màu ở chiều cuối', '`x.permute(2, 0, 1)`: (3, 96, 96), ba lát là đúng ba kênh R, G, B',
              '`x.reshape(3, 96, 96)`: cũng (3, 96, 96), nhưng mỗi “kênh” là một phần ba dãy số, trộn cả R, G, B',
              'xem lại kết quả reshape như một ảnh: hình bị xé thành sọc']
    return Anim('3-1-permute', 'Ảnh hoa thật đổi từ (H, W, 3) sang (3, H, W): permute giữ đúng ba kênh màu; reshape cho cùng shape nhưng trộn lẫn các kênh.',
                labels, draw, dur=[1800, 2600, 2800, 2600], hold=1000, key=[0, 1, 2, 3], themed=False)


# ───────────────────────────── 3.2 ─────────────────────────────

def a3_2_fold():
    """200 điểm quanh bốn góc XOR đi qua lớp ẩn đặt tay của bài: z = xW + b, rồi ReLU, rồi một đường thẳng tách."""
    rng = np.random.default_rng(0)                  # cùng dữ liệu với hình 3-2-learned
    corners = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    lab = np.array([0, 1, 1, 0])
    idx = rng.integers(0, 4, 200)
    X = corners[idx] + rng.normal(0, .15, (200, 2))
    y = lab[idx]
    Z = X @ np.ones((2, 2)) + np.array([0., -1.])
    Hh = np.maximum(Z, 0)
    acc = float((((Hh @ np.array([1., -2.])) > .5).astype(int) == y).mean())
    seq = [('x', 0), ('x', 0)] + [('lin', f) for f in np.linspace(.2, 1, 5)] + [('lin', 1)] + \
          [('relu', f) for f in np.linspace(.25, 1, 4)] + [('relu', 1), ('cut', 1), ('cut', 1)]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for kind, f in seq:
            if kind == 'x':
                P = X
            elif kind == 'lin':
                P = X + (Z - X) * ease(f)
            else:
                P = Z + (Hh - Z) * ease(f)
            fig, ax = plain_axes(theme, 960, 520, (.08, .1, .86, .84))
            ax.axhline(0, color=t['line'], lw=1); ax.axvline(0, color=t['line'], lw=1)
            if kind in ('relu', 'cut'):
                ax.axhspan(-1.6, 0, color=t['soft'], alpha=.5 * ease(f), lw=0)
                ax.axvspan(-1.6, 0, color=t['soft'], alpha=.5 * ease(f), lw=0)
            for l, col in [(0, t['blue']), (1, t['clay'])]:
                m = y == l
                ax.scatter(P[m, 0], P[m, 1], s=16, color=col, linewidths=0, alpha=.85, zorder=3)
            if kind == 'cut':
                hh = np.linspace(-.6, 3.2, 10)
                ax.plot(hh, (hh - .5) / 2, color=t['text'], lw=2, zorder=4)
            ax.set_xlim(-.6, 3.0); ax.set_ylim(-1.5, 1.6)
            ax.set_aspect('equal')
            ax.set_xticks([0, 1, 2]); ax.set_yticks([-1, 0, 1])
            frames.append(grab(fig))
        return frames

    names = {'x': 'đầu vào (x₁, x₂): không đường thẳng nào tách hai cặp góc',
             'lin': 'z = xW + b với W toàn 1, b = (0, −1): z₂ = z₁ − 1, mọi điểm dồn lên một đường thẳng',
             'relu': 'ReLU: tọa độ âm bị ép về 0, nửa dưới gập lên trục ngang',
             'cut': f'h₁ − 2h₂ = 0.5 tách hai lớp: đúng {acc:.0%} trong 200 điểm'}
    labels = [names[k] for k, _ in seq]
    return Anim('3-2-fold', 'Lớp ẩn đặt tay của bài biến 200 điểm XOR: phép tuyến tính dồn mọi điểm lên một đường thẳng, ReLU gập phần âm về trục, rồi một đường thẳng tách được hai lớp.',
                labels, draw, dur=[1500, 1000] + [220] * 4 + [500, 1500] + [240] * 3 + [500, 1300, 2200, 1000], hold=1200,
                key=[0, 7, 12, 14], photo=False, themed=True, display=600)


# ───────────────────────────── 3.3 ─────────────────────────────

def a3_3_bend():
    """Lưới điểm tô màu theo ảnh hoa đi qua cùng một lớp tuyến tính rồi ReLU, tanh, sigmoid: mỗi activation uốn mặt phẳng một kiểu."""
    img = np.asarray(Image.fromarray(sample('flower.jpg')).crop((140, 40, 500, 400)).resize((60, 60), Image.LANCZOS)) / 255
    u = np.linspace(-1, 1, 60)
    gx, gy = np.meshgrid(u, -u)
    P = np.c_[gx.ravel(), gy.ravel()] * 2
    col = img.reshape(-1, 3)
    W = np.array([[1.2, .5], [-.6, 1.1]])
    b = np.array([.3, -.4])
    Z = P @ W + b
    acts = [('ReLU', lambda z: np.maximum(z, 0)), ('tanh', np.tanh), ('sigmoid', lambda z: 1 / (1 + np.exp(-z)))]
    seq = [('in', 0)] + [('lin', f) for f in np.linspace(.25, 1, 4)] + [('act', f) for f in np.linspace(.2, 1, 5)] + [('act', 1)]

    MID = '#8f8b81'                     # xám giữa, đọc được trên nền sáng lẫn tối

    def draw(theme):
        frames = []
        for kind, f in seq:
            fig = fig_frame(960, 360)
            for k, (name, act) in enumerate(acts):
                ax = fig.add_axes((.02 + k * .335, .04, .3, .84))
                ax.patch.set_alpha(0)
                if kind == 'in':
                    Q = P
                elif kind == 'lin':
                    Q = P + (Z - P) * ease(f)
                else:
                    Q = Z + (act(Z) - Z) * ease(f)
                ax.axhline(0, color=MID, lw=.8, zorder=1); ax.axvline(0, color=MID, lw=.8, zorder=1)
                ax.scatter(Q[:, 0], Q[:, 1], s=2.2, c=col, linewidths=0, zorder=2)
                ax.set_xlim(-3.3, 3.3); ax.set_ylim(-3.3, 3.3); ax.set_aspect('equal')
                bare(ax)
                ax.set_title(name, color=MID, fontsize=11, pad=4)
            frames.append(grab(fig))
        return frames

    lab = {'in': 'ảnh hoa trải thành lưới 60 × 60 điểm trên mặt phẳng', 'lin': 'cùng một lớp tuyến tính: xoay, kéo giãn, dịch, lưới vẫn thẳng',
           'act': 'activation: ReLU gập phần âm về trục, tanh ép vào hình vuông (−1, 1), sigmoid ép vào (0, 1)'}
    return Anim('3-3-bend', 'Lưới điểm tô theo ảnh hoa qua cùng một lớp tuyến tính rồi ba activation: phép tuyến tính giữ lưới thẳng, activation mới uốn cong mặt phẳng.',
                [lab[k] for k, _ in seq], draw, dur=[1600] + [260] * 3 + [1200] + [260] * 4 + [800, 1800], hold=1400,
                key=[0, 4, 7, 10], themed=False, quality=80)


# ───────────────────────────── 3.4 và 3.7: Fashion-MNIST ─────────────────────────────

def fashion_grid(imgs, preds, truth, theme, cols=8, cell=100, w=960, h=None):
    from models import FASHION_VI
    t = THEMES[theme]
    rows = (len(imgs) + cols - 1) // cols
    h = h or rows * (cell + 40) + 10
    cv = canvas(w, h)
    x0 = (w - cols * (cell + 16) + 16) / 2
    for i, (im, p, y) in enumerate(zip(imgs, preds, truth)):
        r, c = divmod(i, cols)
        x, yy = x0 + c * (cell + 16), 6 + r * (cell + 40)
        v = 255 - im                              # mực đậm trên nền sáng, giống ảnh sản phẩm
        paste(cv, np.stack([v] * 3, -1), x, yy, cell, cell, nearest=False, radius=6)
        if p is not None:
            ok = p == y
            rect(cv, x - 3, yy - 3, cell + 6, cell + 6, hexrgb(t['green'] if ok else t['clay']), 3, radius=8)
            text(cv, x + cell / 2, yy + cell + 17, FASHION_VI[p], hexrgb(t['green'] if ok else t['clay']), 19)
    return arr(cv)


def a3_4_fashion():
    """Vòng huấn luyện đầy đủ (MLP 784 → 128 → 10, Adam) trên 6000 ảnh Fashion-MNIST; dự đoán 16 ảnh validation sau từng mốc."""
    import torch
    from torch import nn
    from models import fashion
    X, y = fashion('train')
    rng = np.random.default_rng(34)
    idx = rng.permutation(len(X))
    tr, va = idx[:6000], idx[6000:8000]
    Xt = torch.tensor(X[tr].reshape(-1, 784) / 255, dtype=torch.float32); yt = torch.tensor(y[tr])
    Xv = torch.tensor(X[va].reshape(-1, 784) / 255, dtype=torch.float32); yv = torch.tensor(y[va])
    show = np.r_[[np.nonzero(y[va] == c)[0][0] for c in range(10)], np.nonzero(y[va] == 6)[0][1:4], np.nonzero(y[va] == 2)[0][1:4]]
    torch.manual_seed(34)
    model = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
    opt = torch.optim.Adam(model.parameters(), 1e-3)
    snaps = []

    def snap(step):
        model.eval()
        with torch.no_grad():
            out = model(Xv)
            snaps.append((step, out[show].argmax(1).numpy(), float((out.argmax(1) == yv).float().mean()),
                          float(nn.functional.cross_entropy(out, yv))))
        model.train()

    marks = {0, 2, 5, 10, 20, 40, 80, 160, 300, 470, 940, 1880}
    step = 0
    snap(0)
    for epoch in range(20):
        perm = torch.randperm(6000)
        for k in range(0, 6000, 64):
            b = perm[k:k + 64]
            opt.zero_grad()
            loss = nn.functional.cross_entropy(model(Xt[b]), yt[b])
            loss.backward()
            opt.step()
            step += 1
            if step in marks:
                snap(step)
        if step >= max(marks):
            break
    imgs = X[va][show]
    truth = y[va][show]

    def draw(theme):
        return [fashion_grid(imgs, p, truth, theme) for _, p, _, _ in snaps]

    labels = [f'bước {s} (epoch {s / 94:.1f}): accuracy validation {a:.3f}, loss {l:.3f}' for s, _, a, l in snaps]
    return Anim('3-4-fashion', 'Cùng vòng train, chấm validation, lần này trên 6000 ảnh Fashion-MNIST thật: viền xanh là đoán đúng, viền cam là đoán sai.',
                labels, draw, dur=900, hold=2600, key=[0, 3, 6, len(snaps) - 1], themed=True)


def a3_7_onebatch():
    """Overfit đúng một batch 16 ảnh Fashion-MNIST: loss về gần 0 chứng tỏ forward, loss, backward, step nối đúng."""
    import torch
    from torch import nn
    from models import fashion
    X, y = fashion('train')
    rng = np.random.default_rng(37)
    b = rng.choice(len(X), 16, replace=False)
    xb = torch.tensor(X[b].reshape(-1, 784) / 255, dtype=torch.float32); yb = torch.tensor(y[b])
    torch.manual_seed(37)
    model = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
    opt = torch.optim.Adam(model.parameters(), 1e-3)
    marks = [0, 5, 10, 20, 30, 50, 75, 100, 150, 200]
    snaps = []
    for s in range(marks[-1] + 1):
        if s in marks:
            with torch.no_grad():
                out = model(xb)
                snaps.append((s, out.argmax(1).numpy(), float(nn.functional.cross_entropy(out, yb))))
        opt.zero_grad()
        nn.functional.cross_entropy(model(xb), yb).backward()
        opt.step()

    def draw(theme):
        return [fashion_grid(X[b], p, y[b], theme) for _, p, _ in snaps]

    labels = [f'bước {s}: loss {l:.2g}, đúng {int((p == y[b]).sum())}/16' for s, p, l in snaps]
    return Anim('3-7-onebatch', 'Overfit một batch 16 ảnh Fashion-MNIST: lặp lại trên cùng batch, loss phải về gần 0 và cả 16 ảnh được đoán đúng.',
                labels, draw, dur=800, hold=2600, key=[0, 3, 5, 9], themed=True)


# ───────────────────────────── 3.5 ─────────────────────────────

def a3_5_race():
    """25 bước trên J = w₁² + 8w₂² từ (−2, 1), đúng cấu hình hình 3-5-paths (opt_path của recipe lượt 8)."""
    from p8_ch3 import opt_path
    paths = {'SGD': opt_path('sgd', .09)[0], 'momentum': opt_path('momentum', .09)[0], 'Adam': opt_path('adam', .15)[0]}
    J = lambda w: w[0] ** 2 + 8 * w[1] ** 2
    steps = list(range(0, 26))

    def draw(theme):
        t = THEMES[theme]
        cols = {'SGD': t['blue'], 'momentum': t['clay'], 'Adam': t['green']}
        xs, ys = np.linspace(-2.4, 2.4, 240), np.linspace(-1.25, 1.25, 160)
        G = xs[None] ** 2 + 8 * ys[:, None] ** 2
        frames = []
        for k in steps:
            fig, ax = plain_axes(theme, 960, 560, (.06, .08, .9, .88))
            ax.contour(xs, ys, G, levels=[.05, .25, .75, 1.5, 3, 5, 8], colors=[t['line']], linewidths=1)
            for name, P in paths.items():
                ax.plot(P[:k + 1, 0], P[:k + 1, 1], color=cols[name], lw=1.6, alpha=.9)
                ax.scatter(P[k, 0], P[k, 1], s=55, color=cols[name], zorder=4, linewidths=0)
            ax.scatter([0], [0], marker='+', s=90, color=t['text'], zorder=5)
            ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.25, 1.25); ax.set_aspect('equal')
            ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_yticks([-1, 0, 1])
            for i, (name, c) in enumerate(cols.items()):
                ax.text(.99, .97 - i * .075, name, transform=ax.transAxes, ha='right', va='top', color=c, fontsize=11)
            frames.append(grab(fig))
        return frames

    labels = [f'bước {k}: J của SGD {J(paths["SGD"][k]):.3g}, momentum {J(paths["momentum"][k]):.3g}, Adam {J(paths["Adam"][k]):.3g}' for k in steps]
    return Anim('3-5-race', 'Ba optimizer chạy cùng lúc trên J = w₁² + 8w₂² từ (−2, 1), như hình trên: SGD (η = 0.09) zigzag, momentum (η = 0.09, μ = 0.8) vượt đáy rồi vòng lại, Adam (η = 0.15) đi chéo.',
                labels, draw, dur=[1200] + [420] * 24 + [600], hold=2800, key=[0, 5, 12, 25], photo=False, themed=True, display=600)


# ───────────────────────────── 3.6 ─────────────────────────────

def a3_6_curve():
    """Đường cong của mạng nhỏ trong bài (fit_small, decay 0) qua 160 epoch: tốt nhất ở epoch 26 rồi bám dần nhiễu."""
    import torch
    from torch import nn
    ns = lesson_ns('3.6')
    xt, yt, xv, yv = ns['x_train'], ns['y_train'], ns['x_valid'], ns['y_valid']
    torch.manual_seed(29)
    model = nn.Sequential(nn.Linear(1, 16), nn.Tanh(), nn.Linear(16, 16), nn.Tanh(), nn.Linear(16, 1))
    opt = torch.optim.AdamW(model.parameters(), lr=.02, weight_decay=0.0)
    xs = torch.linspace(-1.05, 1.05, 200).unsqueeze(1)
    marks = [1, 3, 6, 10, 15, 20, 26, 40, 60, 80, 110, 160]
    snaps, best = [], (1e9, 0)
    for epoch in range(160):
        model.train()
        opt.zero_grad(set_to_none=True)
        tl = (model(xt) - yt).square().mean()
        tl.backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            vl = (model(xv) - yv).square().mean().item()
            if vl < best[0]:
                best = (vl, epoch + 1)
            if epoch + 1 in marks:
                snaps.append((epoch + 1, model(xs).squeeze(1).numpy(), tl.item(), vl))
    assert best[1] == 26, best                    # khớp output của bài: best epoch 26

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for e, curve, _, _ in snaps:
            fig, ax = plain_axes(theme, 960, 480, (.07, .1, .88, .84))
            ax.plot(xs.squeeze(1), xs.squeeze(1) ** 2, color=t['muted'], lw=1.2, ls=(0, (4, 3)))
            ax.scatter(xt.squeeze(1), yt.squeeze(1), s=40, color=t['blue'], zorder=3, linewidths=0)
            ax.plot(xs.squeeze(1), curve, color=t['clay'], lw=2.4, zorder=4)
            ax.set_xlim(-1.08, 1.08); ax.set_ylim(-.45, 1.45)
            ax.set_xticks([-1, 0, 1]); ax.set_yticks([0, 1])
            frames.append(grab(fig))
        return frames

    labels = [f'epoch {e}: train MSE {a:.4f}, validation MSE {b:.5f}' + (' (tốt nhất)' if e == 26 else '') for e, _, a, b in snaps]
    return Anim('3-6-curve', 'Mạng nhỏ của bài trên 16 điểm nhiễu (chấm xanh), quy tắc thật y = x² (nét đứt): đường cam khớp nhất ở epoch 26, sau đó uốn theo nhiễu.',
                labels, draw, dur=[700] * 6 + [2200] + [700] * 5, hold=2600, key=[2, 6, 9, 11], photo=False, themed=True)


# ───────────────────────────── 3.9 ─────────────────────────────

def a3_9_heads():
    """Attention thật của all-MiniLM-L6-v2 trên một câu: mỗi khung là một query, cột cao là trọng số đặt lên từng key."""
    import os
    os.environ.setdefault('HF_HUB_OFFLINE', '1')
    import torch
    from transformers import AutoTokenizer, AutoModel
    from huggingface_hub import snapshot_download
    path = snapshot_download('sentence-transformers/all-MiniLM-L6-v2', local_files_only=True)
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModel.from_pretrained(path, attn_implementation='eager').eval()
    sent = 'The animal did not cross the street because it was too tired.'
    enc = tok(sent, return_tensors='pt')
    with torch.no_grad():
        att = model(**enc, output_attentions=True).attentions      # 6 lớp × (1, 12, L, L)
    toks = tok.convert_ids_to_tokens(enc['input_ids'][0])
    it, animal = toks.index('it'), toks.index('animal')
    best = max(((l, h) for l in range(6) for h in range(12)), key=lambda lh: float(att[lh[0]][0, lh[1], it, animal]))
    A = att[best[0]][0, best[1]].numpy()
    L = len(toks)
    order = list(range(1, L - 1))                                   # bỏ [CLS], [SEP] khỏi vai query
    order = order + [it] * 2

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for q in order:
            fig = fig_frame(960, 380)
            ax = fig.add_axes((.02, .33, .96, .6))
            ax.patch.set_alpha(0)
            w = A[q]
            ax.bar(np.arange(L), w, width=.7, color=[t['clay'] if j == q else t['blue'] for j in range(L)])
            ax.set_ylim(0, 1); ax.set_xlim(-.6, L - .4)
            bare(ax)
            ax.axhline(0, color=t['line'], lw=1)
            for j, s in enumerate(toks):
                fig.text(.02 + .96 * (j + .5) / L + .008, .27, s, ha='right', va='top', rotation=40, rotation_mode='anchor',
                         color=t['clay'] if j == q else t['text'], fontsize=12,
                         fontweight='bold' if j == q else 'normal')
            frames.append(grab(fig))
        return frames

    labels = [f'query “{toks[q]}”: trọng số lớn nhất ở “{toks[int(A[q].argmax())]}” ({A[q].max():.2f})' for q in order]
    labels[-2] += f'; “animal” nhận {A[it, animal]:.2f}'
    labels[-1] = labels[-2]
    return Anim('3-9-heads', f'Một head thật của MiniLM (lớp {best[0] + 1}, head {best[1] + 1}) trên một câu: mỗi khung là một query, cột là trọng số softmax đặt lên từng token, cộng lại bằng 1.',
                labels, draw, dur=[900] * (len(order) - 2) + [1600, 1600], hold=1200, key=[1, 4, len(order) - 3, len(order) - 1],
                photo=False, themed=True)


# ───────────────────────────── 3.10 ─────────────────────────────

def a3_10_denoise():
    """Denoising autoencoder (784 → 64 → 784) trên Fashion-MNIST: input có nhiễu, target là ảnh sạch."""
    import torch
    from torch import nn
    from models import fashion
    X, y = fashion('train')
    Xte, yte = fashion('test')
    rng = np.random.default_rng(310)
    tr = rng.choice(len(X), 12000, replace=False)
    Xt = torch.tensor(X[tr].reshape(-1, 784) / 255, dtype=torch.float32)
    show = np.array([np.nonzero(yte == c)[0][0] for c in [0, 1, 2, 5, 7, 8, 9, 3]])
    clean = torch.tensor(Xte[show].reshape(-1, 784) / 255, dtype=torch.float32)
    g = torch.Generator().manual_seed(310)
    noisy = (clean + .35 * torch.randn(clean.shape, generator=g)).clamp(0, 1)
    torch.manual_seed(310)
    model = nn.Sequential(nn.Linear(784, 256), nn.ReLU(), nn.Linear(256, 64), nn.ReLU(),
                          nn.Linear(64, 256), nn.ReLU(), nn.Linear(256, 784), nn.Sigmoid())
    opt = torch.optim.Adam(model.parameters(), 1e-3)
    marks = [0, 10, 30, 60, 120, 250, 500, 1000, 1880]
    snaps = []
    step = 0
    for epoch in range(20):
        perm = torch.randperm(len(Xt))
        for k in range(0, len(Xt), 128):
            if step in marks:
                with torch.no_grad():
                    out = model(noisy)
                    snaps.append((step, out.numpy(), float(((out - clean) ** 2).mean())))
            if step >= marks[-1]:
                break
            xb = Xt[perm[k:k + 128]]
            xn = (xb + .35 * torch.randn(xb.shape)).clamp(0, 1)
            opt.zero_grad()
            nn.functional.mse_loss(model(xn), xb).backward()
            opt.step()
            step += 1
        if step >= marks[-1]:
            break
    base = float(((noisy - clean) ** 2).mean())

    def draw(theme):
        frames = []
        for _, out, _ in snaps:
            cv = canvas(960, 350)
            for i in range(8):
                x = 14 + i * 118
                for r, im in enumerate([noisy[i].numpy(), out[i], clean[i].numpy()]):
                    v = (255 - 255 * im.reshape(28, 28)).astype(np.uint8)
                    paste(cv, np.stack([v] * 3, -1), x, 8 + r * 114, 106, 106, radius=5)
            frames.append(arr(cv))
        return frames

    labels = [f'bước {s}: MSE output so với ảnh sạch {m:.4f} (input nhiễu: {base:.4f})' for s, _, m in snaps]
    return Anim('3-10-denoise', 'Denoising autoencoder trên ảnh Fashion-MNIST thật: hàng trên là input có nhiễu, hàng giữa là output sau từng mốc huấn luyện, hàng dưới là ảnh sạch dùng làm target.',
                labels, draw, dur=900, hold=2600, key=[0, 2, 4, 8], themed=False)


ANIMS = [a3_1_permute, a3_2_fold, a3_3_bend, a3_4_fashion, a3_5_race, a3_6_curve, a3_7_onebatch, a3_9_heads, a3_10_denoise]


# ───────────────────────────── 3.8 ─────────────────────────────

CATS = {'con vật': ['mèo', 'chó', 'gà', 'bò'], 'trái cây': ['cam', 'táo', 'chuối', 'xoài'],
        'con số': ['một', 'hai', 'ba', 'bốn'], 'màu': ['đỏ', 'xanh', 'vàng', 'tím']}
TEMPLATES = {'con vật': ['con {} chạy ngoài sân', 'nhà em nuôi con {}', 'con {} kêu rất to', 'con {} đang ngủ'],
             'trái cây': ['quả {} rất ngọt', 'mẹ mua quả {}', 'em ăn quả {}', 'quả {} chín rồi'],
             'con số': ['lớp có {} bạn', 'em có {} cái bút', 'bây giờ là {} giờ', 'đếm đến {} thì dừng'],
             'màu': ['áo màu {}', 'tường sơn màu {}', 'chiếc xe màu {}', 'lá cờ màu {}']}


def a3_8_skipgram():
    """Embedding 2 chiều học bằng skip-gram (đoán từ đứng cạnh) trên 64 câu ngắn: từ cùng loại dần đứng gần nhau."""
    import torch
    from torch import nn
    sents = [tpl.format(w).split() for cat, ws in CATS.items() for w in ws for tpl in TEMPLATES[cat]]
    vocab = sorted({w for s in sents for w in s})
    ix = {w: i for i, w in enumerate(vocab)}
    pairs = [(ix[s[i]], ix[s[j]]) for s in sents for i in range(len(s)) for j in range(max(0, i - 2), min(len(s), i + 3)) if i != j]
    pairs = torch.tensor(pairs)
    torch.manual_seed(38)
    emb = nn.Embedding(len(vocab), 2)
    ctx = nn.Embedding(len(vocab), 2)
    nn.init.normal_(emb.weight, 0, .3)
    nn.init.normal_(ctx.weight, 0, .3)
    opt = torch.optim.Adam(list(emb.parameters()) + list(ctx.parameters()), .03)
    words = [w for ws in CATS.values() for w in ws]
    marks = [0, 5, 10, 20, 35, 50, 80, 120, 180, 260, 400]
    snaps = []
    g = torch.Generator().manual_seed(38)
    for ep in range(marks[-1] + 1):
        if ep in marks:
            snaps.append(emb.weight.detach().numpy()[[ix[w] for w in words]].copy())
        c, o = pairs[:, 0], pairs[:, 1]
        neg = torch.randint(0, len(vocab), (len(pairs), 4), generator=g)
        pos = (emb(c) * ctx(o)).sum(1)
        ng = (emb(c)[:, None] * ctx(neg)).sum(2)
        loss = nn.functional.softplus(-pos).mean() + nn.functional.softplus(ng).sum(1).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    lim = np.abs(np.concatenate(snaps)).max() * 1.12

    def draw(theme):
        t = THEMES[theme]
        cols = [t['clay'], t['blue'], t['green'], t['sand']]
        frames = []
        for E in snaps:
            # mỗi khung tự co giãn theo độ trải của các vector để thấy được cấu trúc, cả lúc còn nhỏ
            rx, ry = np.abs(E[:, 0]).max() * 1.3, np.abs(E[:, 1]).max() * 1.35
            fig, ax = plain_axes(theme, 960, 560, (.04, .05, .92, .9))
            ax.axhline(0, color=t['line'], lw=.8); ax.axvline(0, color=t['line'], lw=.8)
            off = [(-9, 8, 'right', 'bottom'), (9, 8, 'left', 'bottom'), (-9, -8, 'right', 'top'), (9, -8, 'left', 'top')]
            for k, (cat, ws) in enumerate(CATS.items()):
                for j, w in enumerate(ws):
                    x, y = E[words.index(w)]
                    ax.scatter(x, y, s=60, color=cols[k], zorder=3, linewidths=0)
                    dx, dy, ha, va = off[j]      # bốn từ một nhóm nhãn ở bốn góc, không đè nhau khi điểm trùng
                    ax.annotate(w, (x, y), xytext=(dx, dy), textcoords='offset points', color=cols[k], ha=ha, va=va, fontsize=12)
            ax.set_xlim(-rx, rx); ax.set_ylim(-ry, ry)
            bare(ax)
            frames.append(grab(fig))
        return frames

    labels = [f'epoch {e}' + (': vector khởi tạo ngẫu nhiên' if e == 0 else '') for e in marks]
    labels[-1] += ': con vật, trái cây, con số, màu tách thành bốn nhóm'
    return Anim('3-8-skipgram', 'Embedding hai chiều học bằng skip-gram trên 64 câu ngắn: chỉ nhờ đoán từ đứng cạnh, các từ cùng loại dần đứng gần nhau.',
                labels, draw, dur=900, hold=2800, key=[0, 4, 7, 10], photo=False, themed=True)


ANIMS.insert(ANIMS.index(a3_9_heads), a3_8_skipgram)
