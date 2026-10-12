"""Hình động chương 5 (thị giác máy tính).
Ảnh thật: china.jpg, flower.jpg (scikit-learn, CC BY 2.0); coins, coffee, chelsea, astronaut, rocket, horse, camera,
hubble_deep_field, page, brick (scikit-image, public domain/CC0). Model: ResNet-18 ImageNet (torchvision), CLIP ViT-B/32."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, sample, skdata,  # noqa: E402
                  plain_axes, grab, to_rgba, round_corners)
from p8_ch5 import gray, correlate, ink, rgb, SOBEL_X  # noqa: E402

TOWER_BOX = (40, 20, 400, 380)   # vùng cắt tháp dùng chung với các hình 5-1, 5-2 của lượt 8


def tower224():
    return np.asarray(Image.fromarray(sample('china.jpg')).crop(TOWER_BOX).resize((224, 224), Image.LANCZOS))


# ───────────────────────────── 5.1 ─────────────────────────────

def a5_1_scan():
    """Kernel nét dọc trượt qua ảnh tháp thật, bảng đầu ra lấp dần theo thứ tự quét."""
    g = gray(size=72)                      # cùng vùng cắt với hình 5-1-edges, thu nhỏ để thấy từng điểm ảnh
    out = correlate(g, SOBEL_X)            # 70 x 70
    H, W = out.shape
    full = ink(out)
    steps = [0, 70 * 2 + 5, 70 * 2 + 40] + [round(H * W * f) for f in np.linspace(.08, 1, 15)]
    S, X0, X1, Y0 = 420, 40, 500, 30       # cạnh mỗi bảng (px), vị trí trái/phải, mép trên
    px = S / g.shape[0]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for done in steps:
            cv = canvas(960, 480)
            paste(cv, rgb(g), X0, Y0, S, S, nearest=True, radius=6)
            mask = (np.arange(H * W) < done).reshape(H, W)
            img = np.concatenate([full, np.full(full.shape[:2] + (1,), 255, np.uint8)], -1)
            img[~mask] = hexrgb(t['soft'])
            q = S * W / g.shape[1]          # bảng đầu ra 70 điểm vẽ cùng cỡ điểm ảnh với ảnh vào
            off = (S - q) / 2
            paste(cv, img, X1 + off, Y0 + off, round(q), round(q), nearest=True, radius=6)
            if done < H * W:
                i, j = divmod(done, W)
                rect(cv, X0 + j * px - 2, Y0 + i * px - 2, 3 * px + 4, 3 * px + 4, hexrgb(t['clay']), 3, radius=3)
                rect(cv, X1 + off + j * px - 1, Y0 + off + i * px - 1, px + 2, px + 2, hexrgb(t['clay']), 3, radius=2)
            frames.append(arr(cv))
        return frames

    labels = []
    for done in steps:
        if done >= H * W:
            labels.append('xong: 70 × 70 ô, mỗi ô dùng cùng 9 trọng số')
        else:
            i, j = divmod(done, W)
            labels.append(f'cửa sổ ở hàng {i + 1}, cột {j + 1}')
    dur = [900, 900, 900] + [380] * 15
    return Anim('5-1-scan', 'Kernel nét dọc trượt qua ảnh tháp; mỗi vị trí cho một ô của bảng đầu ra.',
                labels, draw, dur=dur, hold=2600, key=[1, 6, 11, 17], themed=True)


# ───────────────────────────── 5.2 ─────────────────────────────

def a5_2_stages():
    """Feature map thật của ResNet-18 ImageNet trên ảnh tháp, qua từng stage."""
    import torch
    from models import resnet18, to_tensor
    m, cats = resnet18()
    img = tower224()
    acts = {}
    names = ['relu', 'layer1', 'layer2', 'layer3', 'layer4']
    hooks = [getattr(m, n).register_forward_hook(lambda mod, i, o, n=n: acts.__setitem__(n, o[0].detach().numpy())) for n in names]
    with torch.no_grad():
        prob = m(to_tensor(img)).softmax(1)[0]
    for h in hooks:
        h.remove()
    top = int(prob.argmax())
    maps = {}
    for n in names:
        a = acts[n]
        order = np.argsort(-a.reshape(a.shape[0], -1).std(1))[:9]   # 9 kênh biến thiên mạnh nhất trên ảnh này
        maps[n] = [a[c] for c in order]

    def tile(a):
        a = a / (np.percentile(a, 99.5) + 1e-9)
        v = (255 - 225 * np.clip(a, 0, 1)).astype(np.uint8)
        return np.repeat(v[..., None], 3, 2)

    def draw(theme):
        frames = []
        for k in range(len(names) + 1):
            cv = canvas(960, 480)
            paste(cv, img, 20, 20, 440, 440, radius=6)
            if k > 0:
                n = names[k - 1]
                for q, a in enumerate(maps[n]):
                    r, c = divmod(q, 3)
                    paste(cv, tile(a), 500 + c * 150, 20 + r * 150, 140, 140, nearest=True, radius=4)
            frames.append(arr(cv))
        return frames

    shapes = [(acts[n].shape[0], acts[n].shape[1]) for n in names]
    labels = ['ảnh vào 224 × 224 × 3'] + [f'`{n}` · {c} kênh · {s} × {s} (9 kênh mạnh nhất)' for n, (c, s) in zip(['conv1'] + names[1:], shapes)]
    labels[-1] += f'; dự đoán “{cats[top]}” {prob[top]:.2f}'
    return Anim('5-2-stages', 'Feature map thật của ResNet-18 trên ảnh tháp: càng sâu, bảng càng nhỏ và nét càng trừu tượng.',
                labels, draw, dur=1500, hold=2400, key=[1, 2, 3, 5], themed=False)


# ───────────────────────────── 5.3 ─────────────────────────────

def a5_3_epochs():
    """Mỗi epoch, cùng một ảnh hoa qua augmentation ngẫu nhiên khác nhau; khung cam là vùng crop trên ảnh gốc."""
    src = sample('flower.jpg')                     # 427 x 640
    H, W = src.shape[:2]
    rng = np.random.default_rng(53)
    views = []
    for e in range(10):
        if e == 0:
            p = dict(s=1.0, cx=W / 2, cy=H / 2, rot=0.0, flip=False, b=1.0, c=1.0)
            p['side'] = H
        else:
            area = rng.uniform(.2, .6)
            side = np.sqrt(area) * H
            rot = float(rng.uniform(-15, 15))
            m = side / 2 * (abs(np.cos(np.deg2rad(rot))) + abs(np.sin(np.deg2rad(rot)))) + 1   # khung xoay nằm trọn trong ảnh
            p = dict(side=side, cx=rng.uniform(m, W - m), cy=rng.uniform(m, H - m), rot=rot,
                     flip=bool(rng.random() < .5), b=float(rng.uniform(.75, 1.25)), c=float(rng.uniform(.75, 1.25)))
            p['s'] = area
        views.append(p)

    def quad(p):
        a = np.deg2rad(p['rot'])
        u = np.array([np.cos(a), np.sin(a)]) * p['side'] / 2
        v = np.array([-np.sin(a), np.cos(a)]) * p['side'] / 2
        c = np.array([p['cx'], p['cy']])
        return [c - u - v, c - u + v, c + u + v, c + u - v]   # trên-trái, dưới-trái, dưới-phải, trên-phải

    def view(p):
        q = quad(p)
        im = Image.fromarray(src).transform((360, 360), Image.QUAD, data=tuple(np.concatenate(q)), resample=Image.BICUBIC)
        a = np.asarray(im, float)
        if p['flip']:
            a = a[:, ::-1]
        mean = a.mean()
        a = (a - mean) * p['c'] + mean
        a = a * p['b']
        return np.clip(a, 0, 255).astype(np.uint8)

    from PIL import ImageDraw

    def draw(theme):
        t = THEMES[theme]
        frames = []
        sx = 520 / W
        for p in views:
            cv = canvas(960, 400)
            paste(cv, src, 20, (400 - H * sx) / 2, 520, round(H * sx), radius=6)
            q = [(20 + x * sx, (400 - H * sx) / 2 + y * sx) for x, y in quad(p)]
            if p['s'] < 1:
                d = ImageDraw.Draw(cv, 'RGBA')
                d.polygon(q, outline=hexrgb(t['clay']), width=4)
            paste(cv, view(p), 580, 20, 360, 360, radius=6)
            frames.append(arr(cv))
        return frames

    labels = ['ảnh gốc']
    for e, p in enumerate(views[1:], 1):
        bits = [f'crop {p["s"]:.0%} diện tích', f'xoay {p["rot"]:+.0f}°'.replace('-', '−')]
        if p['flip']:
            bits.append('lật ngang')
        bits.append(f'sáng ×{p["b"]:.2f}')
        labels.append(f'epoch {e}: ' + ', '.join(bits))
    return Anim('5-3-epochs', 'Mỗi epoch, cùng một ảnh hoa được crop, xoay, lật và đổi sáng ngẫu nhiên; nhãn vẫn là hoa.',
                labels, draw, dur=1300, hold=1600, key=[0, 2, 5, 8], themed=True)


# ───────────────────────────── 5.4 ─────────────────────────────

def a5_4_tokens():
    """Ảnh tháp chia 16 patch 56×56; các hàng patch lần lượt trải thành một chuỗi (hàng dưới đi trước để không
    chồng nhau), cuối cùng ghép CLS ở đầu."""
    img = tower224()
    P = 56
    patches = [img[r * P:(r + 1) * P, c * P:(c + 1) * P] for r in range(4) for c in range(4)]
    cell, gap0 = 56, 8                        # ô trên lưới; khoảng hở khi tách rời
    tok, gap, ty = 50, 4, 330                 # chuỗi: 17 ô (CLS + 16)
    x_start = (960 - (17 * tok + 16 * gap)) / 2
    W0 = 4 * cell + 3 * gap0

    def grid_pos(k, spread):
        r, c = divmod(k, 4)
        g = gap0 * spread
        x = 480 - (4 * cell + 3 * g) / 2 + c * (cell + g)
        y = 20 + r * (cell + g)
        return x + cell / 2, y + cell / 2, cell

    def strip_pos(k):
        return x_start + (k + 1) * (tok + gap) + tok / 2, ty, tok

    # khung: ảnh nguyên, lưới, tách rời, rồi hàng 4, 3, 2, 1 lần lượt trượt xuống (3 khung mỗi hàng), số thứ tự, CLS
    plan = [('whole', None, 0), ('grid', None, 0), ('apart', None, 0)]
    for r in [3, 2, 1, 0]:
        plan += [('move', r, f) for f in (1 / 3, 2 / 3, 1)]
    plan += [('index', None, 1), ('cls', None, 1)]

    def where(k, kind, row, f, moved):
        r = k // 4
        if kind in ('whole', 'grid'):
            return grid_pos(k, 0)
        if kind == 'apart':
            return grid_pos(k, 1)
        if r in moved:
            return strip_pos(k)
        if kind == 'move' and r == row:
            e = ease(f)
            (sx, sy, ss), (ex, ey, es) = grid_pos(k, 1), strip_pos(k)
            return lerp(sx, ex, e), lerp(sy, ey, e), lerp(ss, es, e)
        return grid_pos(k, 1)

    def draw(theme):
        t = THEMES[theme]
        frames = []
        moved = set()
        for kind, row, f in plan:
            cv = canvas(960, 390)
            if kind == 'whole':
                paste(cv, img, 480 - 2 * cell, 20, 4 * cell, 4 * cell, radius=5)
            else:
                for k in range(16):
                    if kind == 'grid':
                        x, y, s = grid_pos(k, 0)
                        s = s - 3
                    else:
                        x, y, s = where(k, kind, row, f, moved if kind == 'move' else {0, 1, 2, 3} if kind in ('index', 'cls') else set())
                    paste(cv, patches[k], x - s / 2, y - s / 2, round(s), round(s), radius=4)
                    if kind in ('index', 'cls'):
                        text(cv, x, y + s / 2 + 18, k + (1 if kind == 'cls' else 0), hexrgb(t['muted']), 17)
                if kind == 'cls':
                    cx = x_start + tok / 2
                    rect(cv, cx - tok / 2, ty - tok / 2, tok, tok, hexrgb(t['sand']), 3, fill=hexrgb(t['sand'], 60), radius=6)
                    text(cv, cx, ty, 'CLS', hexrgb(t['text']), 15, bold=True)
                    text(cv, cx, ty + tok / 2 + 18, 0, hexrgb(t['muted']), 17)
            if kind == 'move' and f == 1:
                moved.add(row)
            frames.append(arr(cv))
        return frames

    labels = ['ảnh 224 × 224', 'chia lưới 4 × 4, mỗi patch 56 × 56 × 3', 'các patch tách rời, chưa trộn thông tin']
    for r in [3, 2, 1, 0]:
        labels += [f'hàng {r + 1} vào vị trí {4 * r}–{4 * r + 3} của chuỗi'] * 3
    labels += ['16 token; thứ tự chỉ còn nằm ở vị trí trong chuỗi', 'ghép CLS vào đầu: chuỗi 17 token']
    dur = [1300, 1300, 1100] + [180, 180, 700] * 4 + [1800, 1800]
    return Anim('5-4-tokens', 'Ảnh tháp chia lưới 4 × 4 (patch 56 × 56 cho dễ nhìn); các hàng patch trải thành chuỗi token, rồi ghép CLS ở đầu.',
                labels, draw, dur=dur, hold=2200, key=[1, 2, 8, 16], themed=True)


# ───────────────────────────── 5.5 ─────────────────────────────

def coin_candidates():
    """Ứng viên box thật trên ảnh đồng xu: detector vòng tròn Hough (cạnh Canny, bán kính 16–38 px).
    Lấy mọi đỉnh của bảng tích lũy trên 33% đỉnh cao nhất, chưa NMS, nên mỗi đồng xu có nhiều box gần nhau."""
    from skimage.feature import canny
    from skimage.transform import hough_circle, hough_circle_peaks
    im = skdata('coins').astype(float) / 255          # 303 x 384, ảnh xám
    edges = canny(im, sigma=2.5, low_threshold=.1, high_threshold=.2)
    radii = np.arange(16, 40, 2)
    acc = hough_circle(edges, radii)
    score, cx, cy, r = hough_circle_peaks(acc, radii, min_xdistance=2, min_ydistance=2,
                                          threshold=.33 * acc.max(), total_num_peaks=400)
    b = np.c_[cx - r, cy - r, cx + r, cy + r, score / score.max()]
    return im, b[np.argsort(-b[:, 4], kind='stable')]


def iou(a, b):
    x1, y1 = np.maximum(a[0], b[:, 0]), np.maximum(a[1], b[:, 1])
    x2, y2 = np.minimum(a[2], b[:, 2]), np.minimum(a[3], b[:, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1]) - inter)


def a5_5_nms():
    from PIL import ImageDraw
    im, B = coin_candidates()
    thr = .3
    alive = np.ones(len(B), bool)
    steps = []
    for i in range(len(B)):
        if not alive[i]:
            continue
        o = iou(B[i], B)
        drop = alive & (o > thr)
        drop[i] = False
        alive &= ~drop
        steps.append((i, np.nonzero(drop)[0]))
    K = len(steps)
    sc = 540 / im.shape[0]
    CW = round(im.shape[1] * sc)
    # 3 lượt đầu chia hai khung (chọn, rồi bỏ); sau đó mỗi khung xử lý gọn 4 lượt
    seq = [('start', 0)]
    for k in range(3):
        seq += [('pick', k), ('done', k + 1)]
    for k in range(3, K, 4):
        seq.append(('done', min(K, k + 4)))
    seq.append(('end', K))
    BLUE, CLAY, SAND = hexrgb('#4fa3e0'), hexrgb('#e07a52'), hexrgb('#f2c14e')

    def box(b):
        return [b[0] * sc, b[1] * sc, b[2] * sc - 1, b[3] * sc - 1]

    def draw(theme):
        frames = []
        for kind, k in seq:
            cv = canvas(CW, 540)
            paste(cv, (im * 255).astype(np.uint8), 0, 0, CW, 540, radius=6)
            d = ImageDraw.Draw(cv, 'RGBA')
            done = [steps[j][0] for j in range(k)]
            removed = set(i for j in range(k) for i in steps[j][1].tolist())
            cur = set([steps[k][0]] + steps[k][1].tolist()) if kind == 'pick' else set()
            for i in range(len(B)):
                if i not in removed and i not in done and i not in cur:
                    d.rectangle(box(B[i]), outline=(255, 255, 255, 110), width=1)
            for i in done:
                d.rectangle(box(B[i]), outline=BLUE, width=3)
            if kind == 'pick':
                for i in steps[k][1]:
                    d.rectangle(box(B[i]), outline=SAND, width=2)
                d.rectangle(box(B[steps[k][0]]), outline=CLAY, width=4)
            frames.append(arr(cv))
        return frames

    labels = []
    for kind, k in seq:
        left = len(B) - sum(len(steps[j][1]) for j in range(k))
        if kind == 'start':
            labels.append(f'{len(B)} box ứng viên của detector, chưa NMS')
        elif kind == 'pick':
            labels.append(f'box score cao nhất còn lại ({B[steps[k][0], 4]:.2f}) và {len(steps[k][1])} box chồng lên nó với IoU > {thr}')
        elif kind == 'done':
            labels.append(f'đã giữ {k} box; còn {left - k} box chưa xét')
        else:
            labels.append(f'NMS xong: {K} box cho 24 đồng xu; 2 box nhỏ nằm trong box lớn có IoU ≤ {thr} nên vẫn sót')
    dur = [1800] + [1400, 1000] * 3 + [450] * (len(seq) - 8) + [600]
    return Anim('5-5-nms', 'NMS trên ảnh đồng xu thật: giữ box score cao nhất, bỏ các box chồng lên nó quá ngưỡng IoU, lặp lại.',
                labels, draw, dur=dur, hold=3200, key=[0, 1, 2, len(seq) - 1], themed=False, quality=80, display=480)


# ───────────────────────────── 5.6 ─────────────────────────────

def a5_6_unet():
    """U-Net nhỏ học mask hoa trên ảnh thật; khung là dự đoán trên cả ảnh sau từng số bước."""
    import torch
    import torch.nn as nn
    from p8_ch5 import flower_masks
    F_ = flower_masks()
    im, target = F_['im'], (F_['inst'] > 0)
    H, W = target.shape
    torch.manual_seed(56)
    x_full = torch.tensor(im.transpose(2, 0, 1)[None] / 255, dtype=torch.float32)
    y_full = torch.tensor(target[None, None], dtype=torch.float32)

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            c = lambda i, o: nn.Sequential(nn.Conv2d(i, o, 3, padding=1), nn.ReLU(), nn.Conv2d(o, o, 3, padding=1), nn.ReLU())
            self.e1, self.e2, self.mid = c(3, 12), c(12, 24), c(24, 32)
            self.d2, self.d1 = c(32 + 24, 24), c(24 + 12, 12)
            self.out = nn.Conv2d(12, 1, 1)
            self.pool = nn.MaxPool2d(2)
            self.up = nn.Upsample(scale_factor=2)

        def forward(self, x):
            a = self.e1(x)
            b = self.e2(self.pool(a))
            m = self.mid(self.pool(b))
            u = self.d2(torch.cat([self.up(m), b], 1))
            return self.out(self.d1(torch.cat([self.up(u), a], 1)))

    net = Net()
    opt = torch.optim.Adam(net.parameters(), 3e-3)
    snaps = [0, 4, 8, 12, 16, 20, 30, 45, 70, 120, 200, 320]
    preds, ious = [], []
    Hc, Wc = H // 4 * 4, W // 4 * 4

    def predict():
        with torch.no_grad():
            p = torch.sigmoid(net(x_full[..., :Hc, :Wc]))[0, 0].numpy()
        m = p > .5
        tg = target[:Hc, :Wc]
        ious.append((m & tg).sum() / max(1, (m | tg).sum()))
        preds.append(p)

    rng = np.random.default_rng(56)
    for step in range(snaps[-1] + 1):
        if step in snaps:
            predict()
        if step == snaps[-1]:
            break
        ys, xs = rng.integers(0, H - 96, 8), rng.integers(0, W - 96, 8)
        xb = torch.cat([x_full[..., y:y + 96, x:x + 96] for y, x in zip(ys, xs)])
        yb = torch.cat([y_full[..., y:y + 96, x:x + 96] for y, x in zip(ys, xs)])
        opt.zero_grad()
        loss = nn.functional.binary_cross_entropy_with_logits(net(xb), yb)
        loss.backward()
        opt.step()

    from skimage.segmentation import find_boundaries
    from scipy.ndimage import binary_dilation
    edge = binary_dilation(find_boundaries(target[:Hc, :Wc], mode='inner'), iterations=1)   # viền dày 3 px để thấy được
    pw = 455
    ph = round(Hc * pw / Wc)

    def draw(theme):
        t = THEMES[theme]
        lo, hi = np.array(hexrgb(t['soft'])[:3], float), np.array(hexrgb(t['blue'])[:3], float)
        frames = []
        for p in preds:
            cv = canvas(960, ph + 20)
            paste(cv, im[:Hc, :Wc], 10, 10, pw, ph, radius=6)
            m = lo + (hi - lo) * p[..., None]          # xanh: xác suất model cho là hoa
            m[edge] = hexrgb(t['clay'])[:3]            # viền cam: mask thật (ngưỡng màu)
            from PIL import Image as _I
            big = np.asarray(_I.fromarray(m.astype(np.uint8)).resize((pw, ph), _I.NEAREST))
            paste(cv, big, 495, 10, pw, ph, radius=6)
            frames.append(arr(cv))
        return frames

    labels = [f'bước {s}: IoU với mask thật {v:.2f}' for s, v in zip(snaps, ious)]
    return Anim('5-6-unet', 'U-Net nhỏ học mask hoa trên ảnh thật: màu xanh là xác suất model cho là hoa, viền cam là mask đặt bằng ngưỡng màu.',
                labels, draw, dur=800, hold=2400, key=[2, 4, 6, 11], themed=True)


# ───────────────────────────── 5.7 ─────────────────────────────

CLIP_POOL = [('china.jpg', 'sk'), ('flower.jpg', 'sk'), ('chelsea', 'ski'), ('coffee', 'ski'), ('astronaut', 'ski'),
             ('rocket', 'ski'), ('horse', 'ski'), ('coins', 'ski'), ('camera', 'ski'), ('hubble_deep_field', 'ski'),
             ('page', 'ski'), ('stereo_motorcycle', 'ski')]
CLIP_QUERIES = ['a photo of a cat', 'a cup of coffee', 'a rocket launch', 'an old pagoda', 'galaxies in deep space',
                'a motorcycle']


def square(a, n=224):
    a = np.asarray(a)
    if a.ndim == 2:
        a = np.stack([a] * 3, -1)
    a = a[..., :3]
    h, w = a.shape[:2]
    s = min(h, w)
    a = a[(h - s) // 2:(h - s) // 2 + s, (w - s) // 2:(w - s) // 2 + s]
    return np.asarray(Image.fromarray(a.astype(np.uint8)).resize((n, n), Image.LANCZOS))


def a5_7_search():
    from models import clip
    model = clip()
    imgs = []
    for name, kind in CLIP_POOL:
        a = sample(name) if kind == 'sk' else skdata(name)
        if name == 'horse':
            a = (np.asarray(a) * 255).astype(np.uint8) if np.asarray(a).dtype == bool else a
        if name == 'stereo_motorcycle':
            a = a[0]
        imgs.append(square(a))
    ie = model.encode([Image.fromarray(a) for a in imgs], normalize_embeddings=True)
    te = model.encode(CLIP_QUERIES, normalize_embeddings=True)
    S = te @ ie.T
    ranks = [np.argsort(-s) for s in S]
    cell, gap = 140, 14
    cols = 6
    x0 = (960 - (cols * cell + (cols - 1) * gap)) / 2

    def pos(r):
        rr, cc = divmod(r, cols)
        return x0 + cc * (cell + gap), 20 + rr * (cell + gap + 20)

    seq = []
    for q in range(len(CLIP_QUERIES)):
        prev = ranks[q - 1] if q else ranks[0]
        for f in [i / 3 for i in range(1, 4)] if q else [1]:
            seq.append((q, prev, ranks[q], f))
        seq.append((q, ranks[q], ranks[q], 1))

    CL, BL, TR = hexrgb('#d0693f'), hexrgb('#4f86c6'), (128, 128, 128, 70)   # nằm trên nền sáng lẫn tối

    def draw(theme):
        frames = []
        for q, a_rank, b_rank, f in seq:
            cv = canvas(960, 360)
            pa = {int(i): r for r, i in enumerate(a_rank)}
            pb = {int(i): r for r, i in enumerate(b_rank)}
            e = ease(f)
            for i in sorted(range(len(imgs)), key=lambda i: -pb[i]):
                (xa, ya), (xb, yb) = pos(pa[i]), pos(pb[i])
                x, y = lerp(xa, xb, e), lerp(ya, yb, e)
                paste(cv, imgs[i], x, y, cell, cell, radius=6)
                if f == 1:
                    s = S[q, i]
                    w = cell * np.clip((s - .1) / .25, 0, 1)
                    rect(cv, x, y + cell + 6, cell, 6, TR, 0, fill=TR, radius=3)
                    rect(cv, x, y + cell + 6, max(6, w), 6, CL if pb[i] == 0 else BL, 0, fill=CL if pb[i] == 0 else BL, radius=3)
                    if pb[i] == 0:
                        rect(cv, x - 4, y - 4, cell + 8, cell + 8, CL, 4, radius=9)
            frames.append(arr(cv))
        return frames

    labels = []
    for q, a_rank, b_rank, f in seq:
        top = int(b_rank[0])
        labels.append(f'“{CLIP_QUERIES[q]}”' + (f' · hạng 1 cosine {S[q, top]:.3f}' if f == 1 else ''))
    dur = [2000 if a is b else 130 for q, a, b, f in seq]
    return Anim('5-7-search', 'CLIP ViT-B/32 xếp 12 ảnh thật theo cosine với từng câu truy vấn; vạch dưới ảnh là cosine.',
                labels, draw, dur=dur, hold=1200, key=[1, 5, 13, 21], themed=False, display=640, quality=82)


# ───────────────────────────── 5.8 ─────────────────────────────

def a5_8_sampling():
    """Sampler DDPM dùng đúng noise predictor bài đã train: 4000 điểm từ N(0, 1) tách dần về hai cụm ±2."""
    import torch
    from p8_ch1 import lesson_ns
    ns = lesson_ns('5.8')
    net, betas, abar = ns['denoiser'], ns['betas'], ns['alpha_bars']
    T = len(betas)
    g = torch.Generator().manual_seed(58)
    x = torch.randn(4000, 1, generator=g)
    hist = {T: x.numpy().ravel().copy()}
    with torch.no_grad():
        for t in range(T - 1, -1, -1):
            eps = net(torch.cat([x, torch.full_like(x, t / (T - 1))], 1))
            a = 1 - betas[t]
            x = (x - betas[t] / (1 - abar[t]).sqrt() * eps) / a.sqrt()
            if t > 0:
                x = x + betas[t].sqrt() * torch.randn(x.shape, generator=g)
            hist[t] = x.numpy().ravel().copy()
    shown = [T, 36, 32, 28, 24, 20, 16, 12, 8, 4, 0]
    bins = np.linspace(-4.5, 4.5, 73)

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for k in shown:
            fig, ax = plain_axes(theme, 960, 420, (.05, .14, .9, .82))
            h, _ = np.histogram(hist[k], bins, density=True)
            ax.bar(bins[:-1], h, width=bins[1] - bins[0], align='edge', color=t['blue'], alpha=.85, linewidth=0)
            for c in (-2, 2):
                ax.axvline(c, color=t['clay'], lw=1.2, ls=(0, (4, 3)))
            ax.set_xlim(-4.5, 4.5)
            ax.set_ylim(0, 1.05)
            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            ax.set_xticks([-4, -2, 0, 2, 4])
            ax.set_xticklabels(['−4', '−2', '0', '2', '4'], color=t['muted'], fontsize=10)
            frames.append(grab(fig))
        return frames

    labels = ['mức 40: điểm xuất phát lấy từ N(0, 1)'] + [f'sau {T - k} bước khử nhiễu, còn mức {k}' for k in shown[1:-1]] + \
             ['mức 0: hai cụm quanh −2 và +2, như dữ liệu train']
    return Anim('5-8-sampling', 'Sampler DDPM dùng noise predictor đã train của bài: 4000 điểm từ noise chuẩn dần tách về hai cụm ±2.',
                labels, draw, dur=650, hold=2600, key=[0, 3, 6, 10], photo=False, themed=True)


# ───────────────────────────── 5.9 ─────────────────────────────

def a5_9_occlusion():
    """Che từng vùng ảnh thật bằng màu trung bình ImageNet, đo xác suất lớp của ResNet-18 giảm bao nhiêu."""
    import torch
    from models import resnet18, to_tensor, center224, MEAN
    m, cats = resnet18()
    img = center224(skdata('coffee'))
    x = to_tensor(img)
    with torch.no_grad():
        p0 = m(x).softmax(1)[0]
    c = int(p0.argmax())
    P, S = 56, 14
    n = (224 - P) // S + 1               # 13 vị trí mỗi chiều
    batch, where = [], []
    for i in range(n):
        for j in range(n):
            z = x.clone()
            z[..., i * S:i * S + P, j * S:j * S + P] = 0      # 0 sau Normalize = màu trung bình ImageNet
            batch.append(z)
            where.append((i, j))
    with torch.no_grad():
        ps = torch.cat([m(torch.cat(batch[k:k + 32])).softmax(1)[:, c] for k in range(0, len(batch), 32)]).numpy()
    drop = (p0[c].item() - ps).reshape(n, n)
    mean_rgb = (MEAN * 255).astype(np.uint8)
    sc = 420 / 224
    rows = list(range(0, n, 1))

    def heat(upto_row, upto_col, theme):
        t = THEMES[theme]
        v = np.clip(drop / max(drop.max(), 1e-6), 0, 1)
        lo, hi = np.array(hexrgb(t['soft'])[:3], float), np.array(hexrgb(t['clay'])[:3], float)
        rgbm = lo + (hi - lo) * v[..., None]
        a = np.full((n, n, 4), 0, np.uint8)
        a[..., :3] = rgbm.astype(np.uint8)
        a[..., 3] = 255
        idx = np.arange(n * n).reshape(n, n)
        a[idx > upto_row * n + upto_col, 3] = 0
        return a

    seq = [(i, j) for i in range(n) for j in range(0, n, 4)] + [(n - 1, n - 1)]
    seq = [(0, 0), (0, 4), (0, 8), (0, 12)] + [(i, n - 1) for i in range(1, n)] + ['overlay']

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for s in seq:
            cv = canvas(960, 460)
            if s == 'overlay':
                v = np.clip(drop / drop.max(), 0, 1)
                up = np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((224, 224), Image.BICUBIC), float) / 255
                o = img * (.22 + .78 * up[..., None])     # giữ sáng vùng quan trọng, làm tối phần còn lại
                paste(cv, o, 30, 20, 420, 420, radius=6)
                paste(cv, heat(n - 1, n - 1, theme), 510, 20, 420, 420, nearest=True, radius=6)
            else:
                i, j = s
                z = img.copy()
                z[i * S:i * S + P, j * S:j * S + P] = mean_rgb
                paste(cv, z, 30, 20, 420, 420, radius=6)
                rect(cv, 30 + j * S * sc, 20 + i * S * sc, P * sc, P * sc, hexrgb(t['clay']), 3)
                rect(cv, 510, 20, 420, 420, hexrgb(t['line']), 2, radius=6)
                paste(cv, heat(i, j, theme), 510, 20, 420, 420, nearest=True, radius=6)
            frames.append(arr(cv))
        return frames

    name = cats[c]
    labels = []
    for s in seq:
        if s == 'overlay':
            labels.append(f'vùng che làm p(“{name}”) giảm mạnh nhất được giữ sáng: mặt tách cà phê')
        else:
            i, j = s
            labels.append(f'che ô hàng {i + 1}, cột {j + 1}: p(“{name}”) = {ps[i * n + j]:.2f} (gốc {p0[c]:.2f})')
    dur = [900] * 4 + [450] * (n - 1) + [600]
    return Anim('5-9-occlusion', 'Occlusion trên ảnh thật với ResNet-18: che từng vùng bằng màu trung bình; che ô nào làm xác suất lớp giảm càng nhiều thì ô đó càng cam.',
                labels, draw, dur=dur, hold=3000, key=[1, 6, 12, len(seq) - 1], themed=True)


ANIMS = [a5_1_scan, a5_2_stages, a5_3_epochs, a5_4_tokens, a5_5_nms, a5_6_unet, a5_7_search, a5_8_sampling, a5_9_occlusion]


# ───────────────────────────── kt3 ─────────────────────────────

def a5_kt3_sweep():
    """Tám xác suất validation của buổi kiểm tra: kéo threshold, accuracy và F1 đổi theo những bậc khác nhau."""
    from p8_ch5 import kt_ns
    ns = kt_ns(5, 'kt3', upto=1)
    p, lab, metric = ns['probabilities'], ns['labels'], ns['binary_metrics']
    grid = np.linspace(0, 1, 401)
    acc = np.array([metric(p >= g, lab)[0] for g in grid])
    f1 = np.array([metric(p >= g, lab)[1] for g in grid])
    ths = [.95, .85, .75, .65, .58, .5, .4, .3, .15, .02]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for th in ths:
            k = int(round(th * 400))
            fig, ax = plain_axes(theme, 960, 440, (.07, .14, .88, .8))
            ax.plot(grid[k:], acc[k:], color=t['blue'], lw=2.2)
            ax.plot(grid[k:], f1[k:], color=t['clay'], lw=2.2)
            ax.plot(grid[:k], acc[:k], color=t['blue'], lw=1, alpha=.25)
            ax.plot(grid[:k], f1[:k], color=t['clay'], lw=1, alpha=.25)
            ax.axvline(th, color=t['text'], lw=1.6)
            for pi, li in zip(p, lab):
                ax.scatter(pi, -.06, s=90, color=t['clay'] if li else t['blue'], edgecolors=t['text'] if pi >= th else 'none',
                           linewidths=1.4, zorder=4, clip_on=False)
            ax.set_xlim(0, 1); ax.set_ylim(-.12, 1.05)
            ax.set_xlabel('threshold', color=t['muted'], fontsize=10)
            ax.text(.02, .96, 'accuracy', color=t['blue'], transform=ax.transAxes, fontsize=11)
            ax.text(.02, .88, 'F1', color=t['clay'], transform=ax.transAxes, fontsize=11)
            frames.append(grab(fig))
        return frames

    labels = [f'threshold {th:g}: accuracy {metric(p >= th, lab)[0]:.3f}, F1 {metric(p >= th, lab)[1]:.3f}' for th in ths]
    return Anim('5-kt3-sweep', 'Tám xác suất validation của buổi kiểm tra (chấm cam là ảnh dương, viền đậm là đoán dương): kéo threshold từ phải sang trái, accuracy và F1 không đạt đỉnh ở cùng chỗ.',
                labels, draw, dur=1200, hold=2200, key=[3, 5, 7, 9], photo=False, themed=True)


ANIMS.append(a5_kt3_sweep)
