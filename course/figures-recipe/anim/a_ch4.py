"""Hình động chương 4 (model pretrained). Ảnh thật: chelsea, coffee, astronaut, rocket, horse, coins (scikit-image, CC0/public domain),
china.jpg, flower.jpg (scikit-learn, CC BY 2.0); CIFAR-10 (Krizhevsky 2009). Model: ResNet-18 ImageNet, CLIP ViT-B/32."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, sample, skdata,  # noqa: E402
                  plain_axes, fig_frame, grab)
from p8_ch1 import lesson_ns  # noqa: E402
from a_ch2 import bare  # noqa: E402


# ───────────────────────────── 4.1 ─────────────────────────────

def a4_1_pipeline():
    """Ảnh mèo thật đi qua preprocessing ImageNet rồi ResNet-18: resize cạnh ngắn 256, cắt giữa 224, chuẩn hóa, top-5."""
    import torch
    from models import resnet18, to_tensor, MEAN, STD
    m, cats = resnet18()
    src = skdata('chelsea')                     # 300 x 451
    H, W = src.shape[:2]
    s = 256 / min(H, W)
    rs = np.asarray(Image.fromarray(src).resize((round(W * s), round(H * s)), Image.BILINEAR))
    h2, w2 = rs.shape[:2]
    l, t0 = (w2 - 224) // 2, (h2 - 224) // 2
    crop = rs[t0:t0 + 224, l:l + 224]
    norm = (crop / 255 - MEAN) / STD
    with torch.no_grad():
        prob = m(to_tensor(crop)).softmax(1)[0]
    top = prob.topk(5)
    S = 1.25                                    # 1 pixel ảnh = 1.25 px khung

    def show_norm(a):
        # chuẩn hóa xong số nằm quanh 0 (âm và dương); hiển thị bằng cách kéo [-2.2, 2.2] về [0, 255]
        return np.clip((a + 2.2) / 4.4 * 255, 0, 255).astype(np.uint8)

    def draw(theme):
        t = THEMES[theme]
        frames = []
        # 0: ảnh gốc
        cv = canvas(960, 400); paste(cv, src, 20, 20, round(W * S * .62), round(H * S * .62), radius=6); frames.append(arr(cv))
        # 1: resize về cạnh ngắn 256
        cv = canvas(960, 400); paste(cv, rs, 20, 20, round(w2 * S), round(h2 * S) - 2, radius=6); frames.append(arr(cv))
        # 2: khung cắt giữa
        cv = canvas(960, 400); paste(cv, rs, 20, 20, round(w2 * S), round(h2 * S) - 2, radius=6)
        rect(cv, 20 + l * S, 20 + t0 * S, 224 * S, 224 * S, hexrgb(t['clay']), 4, radius=4); frames.append(arr(cv))
        # 3: ảnh 224
        cv = canvas(960, 400); paste(cv, crop, 20, 20, round(224 * S), round(224 * S), radius=6); frames.append(arr(cv))
        # 4: ba kênh sau chuẩn hóa
        cv = canvas(960, 400)
        for c in range(3):
            g = show_norm(norm[..., c])
            paste(cv, np.stack([g] * 3, -1), 20 + c * 300, 20, 280, 280, radius=6)
        frames.append(arr(cv))
        # 5: top-5 xác suất
        fig = fig_frame(960, 400)
        ax = fig.add_axes((.52, .12, .4, .8)); ax.patch.set_alpha(0)
        names = [cats[int(i)] for i in top.indices][::-1]
        vals = top.values.numpy()[::-1]
        ax.barh(range(5), vals, color=[t['blue']] * 4 + [t['clay']], height=.62)
        for k, v in enumerate(vals):
            ax.text(v + .01, k, f'{v:.3f}', va='center', color=t['muted'], fontsize=11)
        ax.set_yticks(range(5)); ax.set_yticklabels(names, color=t['text'], fontsize=12)
        ax.set_xlim(0, 1); ax.set_xticks([])
        for sp in ['bottom', 'left']:
            ax.spines[sp].set_visible(False)
        ax.tick_params(length=0)
        a = grab(fig)
        cv = canvas(960, 400)
        paste(cv, crop, 20, 40, 300, 300, radius=6)
        from PIL import Image as I
        cv.alpha_composite(I.fromarray(a, 'RGBA'))
        frames.append(arr(cv))
        return frames

    labels = [f'ảnh gốc {H} × {W} × 3, giá trị 0–255', f'resize cạnh ngắn về 256: {h2} × {w2}', 'cắt giữa một ô 224 × 224',
              'ảnh vào model: 224 × 224 × 3', 'chia 255, trừ mean, chia std từng kênh R, G, B: số nằm quanh 0',
              f'ResNet-18 trả 1000 xác suất; 5 lớp cao nhất cộng lại {float(top.values.sum()):.3f}']
    return Anim('4-1-pipeline', 'Ảnh mèo thật qua đúng preprocessing của ResNet-18 ImageNet rồi qua model: ba lớp mèo đứng đầu, chia nhau gần hết xác suất.',
                labels, draw, dur=[1500, 1300, 1300, 1300, 1800, 2600], hold=1000, key=[0, 2, 4, 5], themed=True)


# ───────────────────────────── 4.2 ─────────────────────────────

def cifar_feats(n_per=80, classes=(0, 1, 3, 6)):
    """Ảnh CIFAR-10 thật của 4 lớp và vector 512 chiều sau global pooling của ResNet-18 ImageNet (ảnh phóng lên 112)."""
    import torch
    from models import cifar, resnet18, MEAN, STD
    X, y = cifar('test_batch')
    idx = np.concatenate([np.nonzero(y == c)[0][:n_per] for c in classes])
    imgs, lab = X[idx], y[idx]
    m, _ = resnet18()
    body = torch.nn.Sequential(*list(m.children())[:-1]).eval()
    x = torch.tensor(((imgs / 255 - MEAN) / STD).transpose(0, 3, 1, 2), dtype=torch.float32)
    x = torch.nn.functional.interpolate(x, size=112, mode='bilinear', align_corners=False)
    with torch.no_grad():
        F = torch.cat([body(x[k:k + 64]).flatten(1) for k in range(0, len(x), 64)]).numpy()
    return imgs, lab, F


def pca2(A):
    A = A - A.mean(0)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    P = A @ Vt[:2].T
    return P / np.abs(P).max(0)


def a4_2_morph():
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    from models import CIFAR_VI
    classes = (0, 1, 3, 6)
    imgs, lab, F = cifar_feats(classes=classes)
    Praw = pca2(imgs.reshape(len(imgs), -1).astype(float))
    Pfeat = pca2(F)
    acc_raw = cross_val_score(LogisticRegression(max_iter=3000), imgs.reshape(len(imgs), -1) / 255, lab, cv=5).mean()
    acc_feat = cross_val_score(LogisticRegression(max_iter=3000), F, lab, cv=5).mean()
    fs = [0, 0] + [ease(i / 8) for i in range(1, 9)] + [1, 1]

    def draw(theme):
        t = THEMES[theme]
        cols = {0: t['blue'], 1: t['sand'], 3: t['clay'], 6: t['green']}
        frames = []
        for k, f in enumerate(fs):
            P = Praw * (1 - f) + Pfeat * f
            fig = fig_frame(960, 600)
            ax = fig.add_axes((.02, .02, .96, .96)); ax.patch.set_alpha(0)
            for c in classes:
                mk = lab == c
                ax.scatter(P[mk, 0], P[mk, 1], s=26, color=cols[c], linewidths=0, alpha=.85)
            if k in (0, 1, len(fs) - 2, len(fs) - 1):
                # vài ảnh thật đặt đúng vị trí của nó
                rng = np.random.default_rng(42)
                for i in rng.choice(len(imgs), 16, replace=False):
                    ax.imshow(imgs[i], extent=(P[i, 0] - .045, P[i, 0] + .045, P[i, 1] - .07, P[i, 1] + .07), zorder=4)
            ax.set_xlim(-1.08, 1.08); ax.set_ylim(-1.08, 1.08)
            bare(ax)
            for j, c in enumerate(classes):
                fig.text(.985, .95 - j * .055, CIFAR_VI[c], color=cols[c], ha='right', fontsize=12)
            frames.append(grab(fig))
        return frames

    labels = ['PCA của pixel thô (3072 số mỗi ảnh): bốn lớp trộn vào nhau',
              f'linear probe trên pixel thô: accuracy 5-fold {acc_raw:.2f}'] + \
             ['chuyển từ không gian pixel sang không gian đặc trưng'] * 8 + \
             ['PCA của vector ResNet-18 (512 số mỗi ảnh): cùng lớp tụ lại',
              f'linear probe trên vector ResNet-18: accuracy 5-fold {acc_feat:.2f}']
    return Anim('4-2-morph', '320 ảnh CIFAR-10 thật của bốn lớp: đặt theo PCA của pixel thô, rồi trượt sang PCA của vector đặc trưng ResNet-18.',
                labels, draw, dur=[1800, 1800] + [260] * 7 + [600] + [1800, 1800], hold=1200, key=[0, 5, 10, 11],
                photo=True, themed=True, display=600)


# ───────────────────────────── 4.3 ─────────────────────────────

def a4_3_transfer():
    """ResNet-18 học 4 lớp CIFAR-10 trên 800 ảnh: khởi đầu từ trọng số ImageNet so với khởi đầu ngẫu nhiên, cùng số bước."""
    import torch
    from torch import nn
    from torchvision.models import resnet18 as R
    from models import cifar, resnet18, MEAN, STD, CIFAR_VI
    classes = [0, 1, 3, 6]
    X, y = cifar('data_batch_1')
    Xv, yv = cifar('test_batch')
    tr = np.concatenate([np.nonzero(y == c)[0][:200] for c in classes])
    va = np.concatenate([np.nonzero(yv == c)[0][:100] for c in classes])
    remap = {c: i for i, c in enumerate(classes)}

    def tens(a):
        x = torch.tensor(((a / 255 - MEAN) / STD).transpose(0, 3, 1, 2), dtype=torch.float32)
        return nn.functional.interpolate(x, size=64, mode='bilinear', align_corners=False)
    xt, yt = tens(X[tr]), torch.tensor([remap[v] for v in y[tr]])
    xv, yvv = tens(Xv[va]), torch.tensor([remap[v] for v in yv[va]])
    show = np.r_[[np.nonzero(yvv.numpy() == k)[0][j] for j in range(2) for k in range(4)]][:6]
    torch.set_num_threads(4)
    marks = [0, 10, 25, 50, 100, 150]
    runs = {}
    for name in ['pretrained', 'scratch']:
        torch.manual_seed(43)
        if name == 'pretrained':
            net = R(); net.load_state_dict(resnet18()[0].state_dict())
        else:
            net = R()
        net.fc = nn.Linear(512, 4)
        opt = torch.optim.Adam(net.parameters(), 3e-4 if name == 'pretrained' else 1e-3)
        g = torch.Generator().manual_seed(43)
        snaps = []
        for step in range(marks[-1] + 1):
            if step in marks:
                net.eval()
                with torch.no_grad():
                    out = torch.cat([net(xv[k:k + 100]) for k in range(0, len(xv), 100)])
                snaps.append((out.argmax(1).numpy(), float((out.argmax(1) == yvv).float().mean())))
                net.train()
            if step == marks[-1]:
                break
            b = torch.randint(0, len(xt), (32,), generator=g)
            opt.zero_grad()
            nn.functional.cross_entropy(net(xt[b]), yt[b]).backward()
            opt.step()
        runs[name] = snaps
    imgs = Xv[va][show]
    truth = yvv.numpy()[show]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for k in range(len(marks)):
            cv = canvas(960, 400)
            for r, name in enumerate(['pretrained', 'scratch']):
                pred = runs[name][k][0][show]
                for i in range(6):
                    x, yy = 190 + i * 128, 8 + r * 196
                    paste(cv, imgs[i], x, yy, 112, 112, radius=6)
                    if k > 0:
                        ok = pred[i] == truth[i]
                        c = hexrgb(t['green'] if ok else t['clay'])
                        rect(cv, x - 3, yy - 3, 118, 118, c, 3, radius=8)
                        text(cv, x + 56, yy + 136, CIFAR_VI[classes[pred[i]]], c, 21)
                text(cv, 170, yy + 56, 'từ ImageNet' if r == 0 else 'từ ngẫu nhiên', hexrgb(t['text']), 21, anchor='rm')
            frames.append(arr(cv))
        return frames

    labels = [f'bước {s}: accuracy validation (400 ảnh) từ ImageNet {runs["pretrained"][k][1]:.2f}, từ ngẫu nhiên {runs["scratch"][k][1]:.2f}'
              for k, s in enumerate(marks)]
    labels[0] = 'bước 0: cả hai head mới đều ngẫu nhiên'
    return Anim('4-3-transfer', 'ResNet-18 học bốn lớp CIFAR-10 từ 800 ảnh, cùng số bước: bắt đầu từ trọng số ImageNet đoán đúng sớm hơn hẳn bắt đầu từ ngẫu nhiên.',
                labels, draw, dur=[1500, 1200, 1200, 1200, 1200, 1400], hold=2600, key=[0, 1, 3, 5], themed=True)


# ───────────────────────────── 4.4 ─────────────────────────────

def a4_4_heat():
    """Thí nghiệm của bài: phần sửa ΔW (6 × 8) mà full update, LoRA rank 1, rank 2 học được qua 250 bước Adam."""
    import torch
    from torch import nn
    ns = lesson_ns('4.4', upto=4)
    TinyLoRA, W0, Xt, yt, Xv, yv = ns['TinyLoRA'], ns['W0'], ns['X_train'], ns['y_train'], ns['X_valid'], ns['y_valid']
    target = (ns['true_B'] @ ns['true_A']).numpy()
    marks = [0, 5, 10, 20, 40, 70, 110, 160, 250]
    runs = {}
    for kind, rank in [('full', None), ('lora', 1), ('lora', 2)]:
        torch.manual_seed(20)
        if kind == 'full':
            net = nn.Linear(8, 6, bias=False)
            with torch.no_grad():
                net.weight.copy_(W0)
        else:
            net = TinyLoRA(W0, rank=rank, alpha=2 * rank)
        learned = [p for p in net.parameters() if p.requires_grad]
        opt = torch.optim.Adam(learned, lr=.03)
        snaps = []
        for s in range(marks[-1] + 1):
            if s in marks:
                with torch.no_grad():
                    d = (net.weight - W0).numpy() if kind == 'full' else (net.scale * net.B @ net.A).numpy()
                    snaps.append((d.copy(), ((net(Xv) - yv) ** 2).mean().item()))
            if s == marks[-1]:
                break
            opt.zero_grad(set_to_none=True)
            ((net(Xt) - yt) ** 2).mean().backward()
            opt.step()
        runs['full' if kind == 'full' else f'rank {rank}'] = snaps
    vmax = np.abs(target).max()

    def draw(theme):
        t = THEMES[theme]
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list('d', [t['blue'], t['soft'], t['clay']])
        frames = []
        for k in range(len(marks)):
            fig = fig_frame(960, 330)
            mats = [('phần sửa thật', target)] + [(n, runs[n][k][0]) for n in ['full', 'rank 1', 'rank 2']]
            for j, (n, M) in enumerate(mats):
                ax = fig.add_axes((.02 + j * .245, .06, .21, .76))
                ax.imshow(M, cmap=cmap, vmin=-vmax, vmax=vmax, interpolation='nearest')
                bare(ax)
                ax.set_title(n, color=t['text'], fontsize=11.5, pad=6)
            frames.append(grab(fig))
        return frames

    labels = [f'bước {s}: validation MSE full {runs["full"][k][1]:.2g}, rank 1 {runs["rank 1"][k][1]:.2g}, rank 2 {runs["rank 2"][k][1]:.2g}'
              for k, s in enumerate(marks)]
    return Anim('4-4-heat', 'Thí nghiệm của bài: phần sửa ΔW mà full update, LoRA rank 1 và rank 2 học được sau từng số bước; ô cam dương, ô xanh âm.',
                labels, draw, dur=900, hold=2600, key=[0, 3, 5, 8], photo=False, themed=True)


# ───────────────────────────── 4.5 ─────────────────────────────

ZS_IMAGES = [('chelsea', 'ski'), ('coffee', 'ski'), ('rocket', 'ski'), ('china.jpg', 'sk'), ('flower.jpg', 'sk'), ('astronaut', 'ski')]
ZS_LABELS = ['cat', 'dog', 'cup of coffee', 'rocket', 'temple', 'flower', 'astronaut', 'car']


def a4_5_zeroshot():
    from models import clip
    from a_ch5 import square
    model = clip()
    imgs = [square(sample(n) if k == 'sk' else skdata(n)) for n, k in ZS_IMAGES]
    ie = model.encode([Image.fromarray(a) for a in imgs], normalize_embeddings=True)
    prompts = [('a photo of an ' if c[0] in 'aeiou' else 'a photo of a ') + c for c in ZS_LABELS]
    te = model.encode(prompts, normalize_embeddings=True)
    logits = 100 * ie @ te.T                      # CLIP nhân cosine với logit scale 100 trước softmax
    P = np.exp(logits - logits.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
    cos = ie @ te.T

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for i in range(len(imgs)):
            fig = fig_frame(960, 400)
            ax = fig.add_axes((.66, .08, .28, .86)); ax.patch.set_alpha(0)
            order = list(range(len(ZS_LABELS)))[::-1]
            best = int(P[i].argmax())
            ax.barh(range(len(order)), [P[i, j] for j in order], color=[t['clay'] if j == best else t['blue'] for j in order], height=.6)
            ax.set_yticks(range(len(order))); ax.set_yticklabels([prompts[j] for j in order], color=t['text'], fontsize=10.5)
            for k, j in enumerate(order):
                ax.text(P[i, j] + .015, k, f'{P[i, j]:.2f}', va='center', color=t['muted'], fontsize=10)
            ax.set_xlim(0, 1.12); ax.set_xticks([])
            for sp in ['bottom', 'left']:
                ax.spines[sp].set_visible(False)
            ax.tick_params(length=0)
            a = grab(fig)
            cv = canvas(960, 400)
            paste(cv, imgs[i], 20, 40, 320, 320, radius=6)
            cv.alpha_composite(Image.fromarray(a, 'RGBA'))
            frames.append(arr(cv))
        return frames

    labels = [f'ảnh {i + 1}: chọn “{ZS_LABELS[int(P[i].argmax())]}”, cosine {cos[i].max():.3f}, softmax {P[i].max():.2f}' for i in range(len(imgs))]
    return Anim('4-5-zeroshot', 'Zero-shot với CLIP ViT-B/32 trên ảnh thật: mỗi lớp chỉ là một câu “a photo of a …”, ảnh chọn câu có cosine cao nhất; không ảnh nào được dùng để train.',
                labels, draw, dur=2200, hold=1000, key=[0, 1, 3, 5], themed=True, pcols=3)


ANIMS = [a4_1_pipeline, a4_2_morph, a4_3_transfer, a4_4_heat, a4_5_zeroshot]


# ───────────────────────────── kt2 ─────────────────────────────

def a4_kt2_floor():
    """Head 2 → 3 của buổi kiểm tra học trên ba mẫu đầu: loss đúng (logits vào cross-entropy) và loss sai (softmax trước)."""
    import torch
    from torch import nn
    from p8_ch5 import kt_ns
    ns = kt_ns(4, 'kt2', upto=1)
    X, tgt = ns['features'][:3], torch.tensor(ns['targets'][:3])   # ba mẫu đầu, mỗi lớp một mẫu, tách được
    runs = {}
    for kind in ['logits', 'softmax']:
        torch.manual_seed(0)
        head = nn.Linear(2, 3, bias=False)
        opt = torch.optim.SGD(head.parameters(), lr=.5)
        hist = []
        for _ in range(300):
            out = head(X)
            loss = nn.functional.cross_entropy(out if kind == 'logits' else out.softmax(1), tgt)
            hist.append(loss.item())
            opt.zero_grad()
            loss.backward()
            opt.step()
        runs[kind] = hist
    floor = -np.log(np.e / (np.e + 2))
    marks = [1, 5, 10, 20, 40, 70, 110, 160, 230, 300]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for m in marks:
            fig, ax = plain_axes(theme, 960, 420, (.08, .13, .88, .8))
            ax.axhline(floor, color=t['muted'], lw=1.2, ls=(0, (4, 3)))
            ax.plot(range(m), runs['logits'][:m], color=t['blue'], lw=2.2)
            ax.plot(range(m), runs['softmax'][:m], color=t['clay'], lw=2.2)
            ax.set_xlim(0, 300); ax.set_ylim(0, 1.2)
            ax.set_xlabel('bước', color=t['muted'], fontsize=10)
            ax.text(298, floor + .04, f'sàn {floor:.3f}', color=t['muted'], ha='right', fontsize=10)
            ax.text(.98, .95, 'logits vào loss', color=t['blue'], ha='right', transform=ax.transAxes, fontsize=11)
            ax.text(.98, .87, 'softmax rồi mới vào loss', color=t['clay'], ha='right', transform=ax.transAxes, fontsize=11)
            frames.append(grab(fig))
        return frames

    labels = [f'bước {m}: loss đúng {runs["logits"][m - 1]:.3f}, loss khi softmax hai lần {runs["softmax"][m - 1]:.3f}' for m in marks]
    return Anim('4-kt2-floor', 'Head của buổi kiểm tra học ba mẫu đầu (mỗi lớp một mẫu) với hai cách tính loss: đưa logits vào thì loss về gần 0; softmax trước thì loss chỉ tiến sát sàn 0.551.',
                labels, draw, dur=900, hold=2400, key=[1, 4, 9], photo=False, themed=True, pcols=3)


ANIMS.append(a4_kt2_floor)
