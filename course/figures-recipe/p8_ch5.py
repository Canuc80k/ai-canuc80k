"""Lượt 8 — hình chương 5 (bản gọn). Số liệu lấy từ code bài (lesson_ns) hoặc tính lại đúng như bài.
Ảnh thật: china.jpg (danielbuechele / Flickr, CC BY 2.0) và flower.jpg (vultilion / Flickr, CC BY 2.0) kèm scikit-learn,
ghi nguồn ở mục Đọc thêm của bài dùng ảnh.
Chạy riêng: python -B -X utf8 p8_ch5.py [tên ...]"""
import math, sys
import numpy as np
from kit import *
from p8_ch1 import lesson_ns
from p8_ch2 import PAPER, sup, mnum, clip, segline, regions, jit
from p8_ch4 import digit

SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float)


def gray(name='china.jpg', box=(40, 20, 400, 380), size=180):
    """Ảnh mẫu scikit-learn, cắt vùng box (trái, trên, phải, dưới), đổi xám, thu về size×size; giá trị 0..1."""
    from sklearn.datasets import load_sample_image
    from PIL import Image
    im = Image.fromarray(load_sample_image(name)).crop(box).convert('L').resize((size, size), Image.LANCZOS)
    return np.asarray(im, float) / 255


def correlate(img, k):
    """Cross-correlation 'valid' như Conv2d của PyTorch (không lật kernel)."""
    kh, kw = k.shape
    H, W = img.shape[0] - kh + 1, img.shape[1] - kw + 1
    out = np.zeros((H, W))
    for u in range(kh):
        for v in range(kw):
            out += k[u, v] * img[u:u + H, v:v + W]
    return out


def ink(m, q=99):
    """Feature map → ảnh RGB kiểu nét mực: |giá trị| lớn thì tối, nền trắng."""
    a = np.clip(np.abs(m) / np.percentile(np.abs(m), q), 0, 1)
    v = (255 - 225 * a).astype('uint8')
    return np.repeat(v[..., None], 3, 2)


def rgb(g):
    v = (np.clip(g, 0, 1) * 255).astype('uint8')
    return np.repeat(v[..., None], 3, 2)


def blocky(img, size):
    """Phóng ảnh nhỏ bằng lặp điểm để thấy rõ từng ô."""
    f = max(1, size // img.shape[0])
    return np.repeat(np.repeat(img, f, 0), f, 1)


def maxpool(m, k=2):
    H, W = m.shape[0] // k * k, m.shape[1] // k * k
    return m[:H, :W].reshape(H // k, k, W // k, k).max(axis=(1, 3))


# ───────────────────────────── 5.1 ─────────────────────────────


def window51():
    ns = lesson_ns('5.1', upto=1)
    X, K, Y = ns['image'], ns['kernel'], ns['feature_map']
    s = Fig(640, 210)
    c = 42
    fx = {(i, j): (CLAY, .3) for i in range(2) for j in range(2)}
    s.tiles(40, 46, [[f'{v:g}' for v in r] for r in X], c, c, BLUE, 4, fx, size=15)
    s.label(107, 28, 'ảnh X · 3×3', 12.5, color=TEXT, weight=600)
    s.tiles(250, 69, [[f'{v:g}' for v in r] for r in K], c, c, CLAY, 4, size=15, opacity=.2)
    s.label(294, 51, 'kernel · 2×2', 12.5, color=TEXT, weight=600)
    s.tiles(450, 69, [[f'{v:g}' for v in r] for r in Y], c, c, GREEN, 4, {(0, 0): (CLAY, .3)}, size=15)
    s.label(494, 51, 'đầu ra · 2×2', 12.5, color=TEXT, weight=600)
    s.arrow(184, 115, 238, 115, LINE, 1.3)
    s.arrow(346, 115, 440, 115, LINE, 1.3)
    s.mono(320, 192, '1·1 + 2·0 + 0·0 + 1·2 = 3', 13, 'middle', TEXT)
    s.save('5-1-window', 'Nhân từng ô của cửa sổ với kernel rồi cộng: ô đầu ra đầu tiên bằng 3.')


def edges51():
    g = gray()
    kx, ky = SOBEL_X, SOBEL_X.T
    s = Fig(640, 290)
    w = 176
    xs = [26, 232, 438]
    for x, img, title in [(xs[0], rgb(g), 'ảnh xám'), (xs[1], ink(correlate(g, kx)), 'kernel nét dọc'),
                          (xs[2], ink(correlate(g, ky)), 'kernel nét ngang')]:
        s.photo(x, 34, w, w, img, max_px=360, radius=6)
        s.label(x + w / 2, 20, title, 12.5, color=TEXT, weight=600)
    for x, k in [(xs[1], kx), (xs[2], ky)]:
        fills = {(i, j): ((CLAY if v > 0 else BLUE) if v else FAINT, .1 + .14 * abs(v)) for i, r in enumerate(k) for j, v in enumerate(r)}
        s.tiles(x + w / 2 - 41, 222, [[mnum(v, '{:g}') for v in r] for r in k], 26, 18, FAINT, 2, fills, size=10.5)
    s.label(xs[0] + w / 2, 244, 'cùng 9 trọng số trượt qua mọi vị trí', 11.5, color=MUTED)
    s.save('5-1-edges', 'Kernel nét dọc làm sáng cạnh đứng của tháp; kernel ngang làm sáng mái và lan can.')


def padding51():
    s = Fig(640, 240)
    c, g = 30, 4
    x0 = 120
    s.label(60, 66, 'p = 1, s = 2', 12, 'middle', TEXT, 600)
    fills = {(0, 0): (FAINT, .08), (0, 8): (FAINT, .08)}
    s.tiles(x0, 52, [[''] + [str(i) for i in range(7)] + ['']], c, c, BLUE, g, fills, size=12)
    s.mono(x0 + c / 2, 100, 'vành', 10.5, 'middle', FAINT)
    s.mono(x0 + 8 * (c + g) + c / 2, 100, 'vành', 10.5, 'middle', FAINT)
    for k, st in enumerate([0, 2, 4, 6]):
        y = 42 if k % 2 == 0 else 32
        a, b = x0 + st * (c + g) + 3, x0 + (st + 3) * (c + g) - g - 3
        s.path(f'M {a},{y + 6} L {a},{y} L {b},{y} L {b},{y + 6}', CLAY, 1.3)
    s.arrow(430, 67, 470, 67, LINE, 1.2)
    s.tiles(478, 52, [[''] * 4], c, c, CLAY, g, opacity=.3)
    s.mono(546, 100, '4 ô', 12, 'middle', CLAY)
    s.label(60, 166, 'd = 2', 12, 'middle', TEXT, 600)
    tap = {(0, j): (CLAY, .32) for j in (0, 2, 4)}
    s.tiles(x0 + c + g, 152, [[str(i) for i in range(7)]], c, c, BLUE, g, tap, size=12)
    a, b = x0 + (c + g) + 3, x0 + 6 * (c + g) - g - 3
    s.path(f'M {a},{146} L {a},{140} L {b},{140} L {b},{146}', CLAY, 1.3)
    s.mono((a + b) / 2, 132, 'phủ 5 ô, 3 trọng số', 11.5, 'middle', CLAY)
    s.arrow(430, 167, 470, 167, LINE, 1.2)
    s.tiles(478, 152, [[''] * 3], c, c, CLAY, g, opacity=.3)
    s.mono(529, 200, '3 ô', 12, 'middle', CLAY)
    s.save('5-1-padding', 'Padding thêm vành 0, stride dịch nhiều ô, dilation đọc cách ô.')


def channels51():
    s = Fig(640, 250)

    def stack(x, y, n, size, col, dx=7, op=.16):
        for k in range(n - 1, -1, -1):
            s.box(x + k * dx, y - k * dx, size, size, 'none', col, r=5, width=0, opacity=op)
            s.box(x + k * dx, y - k * dx, size, size, PAPER, 'none', r=5, width=1)
    stack(30, 80, 3, 84, BLUE)
    s.mono(88, 208, '(3, 7, 7)', 12, 'middle', MUTED)
    s.label(88, 30, 'ảnh RGB', 12.5, color=TEXT, weight=600)
    stack(186, 108, 3, 36, CLAY, 6, .3)
    s.mono(212, 208, '(3, 3, 3)', 12, 'middle', MUTED)
    s.label(212, 30, 'một kernel', 12.5, color=TEXT, weight=600)
    s.arrow(250, 122, 300, 122, LINE, 1.2)
    s.mono(275, 112, '+ b', 11.5, 'middle', MUTED)
    s.box(306, 80, 84, 84, 'none', GREEN, r=5, width=0, opacity=.22)
    s.mono(348, 208, '(7, 7)', 12, 'middle', MUTED)
    s.label(348, 30, 'một kênh ra', 12.5, color=TEXT, weight=600)
    s.arrow(400, 122, 446, 122, LINE, 1.2)
    s.mono(423, 112, '× 8', 11.5, 'middle', MUTED)
    stack(452, 108, 8, 84, GREEN, 6, .14)
    s.mono(536, 208, '(8, 7, 7)', 12, 'middle', MUTED)
    s.label(536, 30, 'tám kênh ra', 12.5, color=TEXT, weight=600)
    s.mono(320, 236, '8 · (3·9 + 1) = 224 tham số', 12.5, 'middle', CLAY)
    s.save('5-1-channels', 'Mỗi kernel đọc cả ba kênh RGB; tám kernel cho tám kênh ra, 224 tham số.')


def pool51():
    g = gray(size=128)
    m = np.abs(correlate(np.pad(g, 1, mode='edge'), SOBEL_X)) + np.abs(correlate(np.pad(g, 1, mode='edge'), SOBEL_X.T))
    maps = [m]
    for _ in range(3):
        maps.append(maxpool(maps[-1]))
    s = Fig(640, 210)
    w = 132
    for k, mm in enumerate(maps):
        x = 24 + k * 152
        s.photo(x, 32, w, w, blocky(ink(mm), 256), max_px=264, radius=4)
        s.mono(x + w / 2, 20, f'{mm.shape[0]}×{mm.shape[1]}', 12, 'middle', TEXT)
        if k:
            s.arrow(x - 18, 98, x - 4, 98, CLAY, 1.3)
    s.label(320, 192, 'mỗi lần max pool 2×2 giữ một số trong bốn: nét còn, vị trí chính xác mất dần', 11.5, color=MUTED)
    s.save('5-1-pool', 'Ba lần max pool 2×2: từ 128×128 xuống 16×16, nét còn nhưng chi tiết mất dần.')


def poolshift51():
    s = Fig(640, 200)
    c, g = 40, 4
    for k, (row, out, title) in enumerate([([0, 4, 0, 0], [4, 0], 'ban đầu'), ([0, 0, 4, 0], [0, 4], 'dịch một ô')]):
        x0 = 60 + k * 300
        s.label(x0 + 86, 24, title, 12.5, color=TEXT, weight=600)
        fills = {(0, j): (BLUE if j < 2 else SAND, .16 if v == 0 else .0) for j, v in enumerate(row)}
        fills.update({(0, j): (CLAY, .35) for j, v in enumerate(row) if v})
        s.tiles(x0, 42, [[str(v) for v in row]], c, c, BLUE, g, fills, size=14)
        for w in range(2):
            a, b = x0 + w * 2 * (c + g) + 3, x0 + (w * 2 + 2) * (c + g) - g - 3
            s.path(f'M {a},{88} L {a},{94} L {b},{94} L {b},{88}', MUTED, 1.2)
            s.arrow((a + b) / 2, 98, x0 + 42 + w * (c + g) + c / 2, 128, FAINT, 1.1)
        s.tiles(x0 + 42, 132, [[str(v) for v in out]], c, c, GREEN, g, {(0, j): (CLAY, .35) for j, v in enumerate(out) if v}, size=14)
    s.label(320, 188, 'đỉnh qua ranh giới cửa sổ: kết quả đổi chỗ, pooling không bất biến dịch tuyệt đối', 11.5, color=MUTED)
    s.save('5-1-pool-shift', 'Đỉnh dịch một ô qua ranh giới cửa sổ thì đầu ra max pool đổi từ (4, 0) thành (0, 4).'.replace('[', '(').replace(']', ')'))


def receptive51():
    s = Fig(640, 230)
    c, g = 40, 8
    x0 = 320 - (7 * (c + g) - g) / 2
    X = lambda j: x0 + j * (c + g) + c / 2
    for j in range(7):
        inside = 1 <= j <= 5
        s.box(X(j) - c / 2, 160, c, 30, 'none', CLAY if inside else BLUE, r=6, width=0, opacity=.3 if inside else .1)
    for j in (2, 3, 4):
        for d in (-1, 0, 1):
            s.line(X(j), 74, X(j + d), 158, FAINT, 1)
        s.circle(X(j), 72, 7, BLUE, PAPER, 1.6)
    for d in (-1, 0, 1):
        s.line(X(3), 22, X(3 + d), 64, CLAY, 1.4)
    s.circle(X(3), 20, 8, CLAY, CLAY, 0)
    s.label(x0 - 16, 20, 'lớp 2', 12, 'end', MUTED)
    s.label(x0 - 16, 72, 'lớp 1', 12, 'end', MUTED)
    s.label(x0 - 16, 175, 'đầu vào', 12, 'end', MUTED)
    s.mono(320, 214, 'r = 1 + 2 + 2 = 5', 12.5, 'middle', CLAY)
    s.save('5-1-receptive', 'Hai lớp kernel 3: mỗi ô ở lớp 2 nhìn được 5 ô đầu vào.')


def equiv51():
    from sklearn.datasets import load_sample_image
    from PIL import Image
    full = Image.fromarray(load_sample_image('china.jpg')).convert('L')
    sh = 40
    crops = [np.asarray(full.crop((60 + sh, 40, 380 + sh, 360)).resize((160, 160), Image.LANCZOS), float) / 255,
             np.asarray(full.crop((60, 40, 380, 360)).resize((160, 160), Image.LANCZOS), float) / 255]
    maps = [correlate(c_, SOBEL_X) for c_ in crops]
    col = int(np.argmax(np.abs(maps[0]).sum(0)))
    d = sh * 160 / 320
    s = Fig(640, 300)
    w = 120
    xs = [190, 340]
    for r, (img, mm, lab) in enumerate(zip(crops, maps, ['ảnh', 'dịch phải 20 px'])):
        y = 30 + r * 140
        s.photo(xs[0], y, w, w, rgb(img), max_px=240, radius=5)
        s.photo(xs[1], y, w, w, ink(mm), max_px=240, radius=5)
        s.label(xs[0] - 12, y + w / 2, lab, 12, 'end', TEXT)
        cx = xs[1] + (1 + col + r * d) * w / 160
        s.line(cx, y - 6, cx, y + 4, CLAY, 2)
    s.label(xs[0] + w / 2, 20, 'đầu vào', 12, color=MUTED)
    s.label(xs[1] + w / 2, 20, 'feature map nét dọc', 12, color=MUTED)
    s.label(480, 160, 'cạnh mạnh nhất', 12, 'start', CLAY)
    s.label(480, 178, 'dịch đúng 20 px', 12, 'start', CLAY)
    s.save('5-1-equiv', 'Dịch ảnh 20 px thì feature map dịch theo đúng 20 px.')


FIGS51 = {'5-1-window': window51, '5-1-edges': edges51, '5-1-padding': padding51, '5-1-channels': channels51,
          '5-1-pool': pool51, '5-1-pool-shift': poolshift51, '5-1-receptive': receptive51, '5-1-equiv': equiv51}

# ───────────────────────────── 5.2 ─────────────────────────────

_T52 = {}


def run52():
    """Chạy code bài 5.2 tới hết thí nghiệm 18 lớp; lưu thêm gradient conv đầu của bốn cấu hình (chạy lại đúng seed)."""
    if not _T52:
        ns = lesson_ns('5.2', upto=5)
        _T52['ns'] = ns
        grads = {}
        for name, skip, norm in [('plain', False, False), ('plain + BN', False, True),
                                 ('residual', True, False), ('residual + BN', True, True)]:
            grads[name] = ns['train_deep'](ns['deep_net'](skip, norm), steps=1)[0]
        _T52['grads'] = grads
    return _T52


def samples52():
    ns = lesson_ns('5.2', upto=1)
    X, y = ns['train_images'].numpy(), ns['train_labels'].numpy()
    s = Fig(640, 190)
    w, g = 64, 10
    for k in range(8):
        x = 30 + k * (w + g)
        s.photo(x, 40, w, w, blocky(ink(X[k, 0], 100), 192), max_px=192, radius=4)
        s.label(x + w / 2, 122, 'đứng' if y[k] == 0 else 'ngang', 12, color=BLUE if y[k] == 0 else CLAY)
    s.label(320, 22, '8 ảnh train đầu tiên của make_lines (12×12, nhiễu σ = 0.04)', 12, color=MUTED)
    s.label(320, 166, 'chỉ 5 vị trí × 2 hướng: validation khác train ở nhiễu', 11.5, color=MUTED)
    s.save('5-2-samples', 'Tám ảnh train: nét đứng hoặc nét ngang, ở năm vị trí, cộng nhiễu nhỏ.')


def cnn52():
    s = Fig(640, 210)

    def stack(x, y, n, size, col, dx=5, op=.14):
        for k in range(n - 1, -1, -1):
            s.box(x + k * dx, y - k * dx, size, size, 'none', col, r=4, width=0, opacity=op)
            s.box(x + k * dx, y - k * dx, size, size, PAPER, 'none', r=4, width=1)
    stack(20, 70, 1, 72, BLUE, op=.2)
    s.mono(56, 172, '1×12×12', 11.5, 'middle', MUTED)
    s.label(56, 30, 'ảnh', 12.5, color=TEXT, weight=600)
    stack(130, 84, 4, 72, BLUE)
    s.mono(181, 172, '8×12×12', 11.5, 'middle', MUTED)
    s.label(181, 30, 'conv + ReLU', 12.5, color=TEXT, weight=600)
    stack(270, 102, 4, 36, BLUE)
    s.mono(303, 172, '8×6×6', 11.5, 'middle', MUTED)
    s.label(303, 30, 'max pool', 12.5, color=TEXT, weight=600)
    stack(368, 102, 4, 36, BLUE, op=.22)
    s.mono(401, 172, '8×6×6', 11.5, 'middle', MUTED)
    s.label(401, 30, 'conv + ReLU', 12.5, color=TEXT, weight=600)
    s.tiles(482, 64, [[''] for _ in range(8)], 16, 10, GREEN, 2, opacity=.4, r=2)
    s.mono(490, 172, '8', 11.5, 'middle', MUTED)
    s.label(492, 30, 'trung bình', 12.5, color=TEXT, weight=600)
    s.tiles(560, 92, [['z₀'], ['z₁']], 40, 22, CLAY, 4, size=11.5, opacity=.25)
    s.mono(580, 172, '2 logits', 11.5, 'middle', MUTED)
    s.label(580, 30, 'linear head', 12.5, color=TEXT, weight=600)
    for a, b in [(96, 126), (226, 266), (330, 364), (428, 476), (504, 554)]:
        s.arrow(a, 106, b, 106, LINE, 1.1)
    s.save('5-2-cnn', 'TinyCNN: hai lần conv + ReLU xen max pool, lấy trung bình mỗi kênh, rồi linear ra hai logits.')


def metrics52():
    ns = lesson_ns('5.2', upto=3)
    import torch
    model, V, yv = ns['model'], ns['valid_images'], ns['valid_labels'].numpy()
    pick = [int(np.where(yv == 0)[0][0]), int(np.where(yv == 1)[0][0])]
    with torch.no_grad():
        act = model.features[:2](V[pick]).numpy()
    ch = list(np.argsort(-act.var(axis=(0, 2, 3)))[:3])
    s = Fig(640, 250)
    w = 92
    for r, i in enumerate(pick):
        y = 34 + r * 106
        s.photo(60, y, w, w, blocky(ink(V[i, 0].numpy(), 100), 192), max_px=192, radius=4)
        for k, c_ in enumerate(ch):
            a = act[r, c_]
            img = blocky((255 - 225 * np.clip(a / (act[:, c_].max() + 1e-9), 0, 1)).astype('uint8')[..., None].repeat(3, 2), 192)
            s.photo(220 + k * 118, y, w, w, img, max_px=192, radius=4)
        s.arrow(162, y + w / 2, 208, y + w / 2, LINE, 1.2)
    s.label(106, 22, 'ảnh validation', 12, color=MUTED)
    for k, c_ in enumerate(ch):
        s.label(266 + k * 118, 22, f'kênh {c_}', 12, color=MUTED)
    s.save('5-2-metrics', 'Ba kênh sau lớp conv đầu: mỗi kênh nhấn một phần khác nhau của nét.')


def residual52():
    s = Fig(640, 190)
    s.circle(60, 120, 18, BLUE, PAPER, 1.6)
    s.mono(60, 120.5, 'x', 14, 'middle', TEXT)
    for k, (lab, x) in enumerate([('conv', 130), ('ReLU', 230), ('conv', 330)]):
        s.box(x, 102, 80, 36, 'none', CLAY if lab == 'conv' else FAINT, r=7, width=0, opacity=.22 if lab == 'conv' else .14)
        s.label(x + 40, 120, lab, 12.5, color=TEXT)
    for a, b in [(80, 126), (212, 226), (312, 326), (412, 448)]:
        s.arrow(a, 120, b, 120, LINE, 1.2)
    s.label(270, 158, 'F(x)', 12.5, color=CLAY, weight=600)
    s.circle(466, 120, 16, CLAY, PAPER, 1.6)
    s.mono(466, 120.5, '+', 15, 'middle', CLAY, 600)
    s.path('M 60,100 L 60,46 L 466,46 L 466,100', BLUE, 1.6)
    s.arrow(466, 80, 466, 102, BLUE, 1.6)
    s.label(263, 34, 'đường tắt: x đi thẳng', 12.5, color=BLUE, weight=600)
    s.arrow(484, 120, 524, 120, LINE, 1.2)
    s.box(528, 102, 64, 36, 'none', FAINT, r=7, width=0, opacity=.14)
    s.label(560, 120, 'ReLU', 12.5, color=TEXT)
    s.mono(320, 180, 'y = ReLU(x + F(x))', 12.5, 'middle', TEXT)
    s.save('5-2-residual', 'Residual block: đường tắt cộng thẳng x vào F(x) rồi mới qua ReLU.')


def depth52():
    T = run52()
    C = T['ns']['curves']
    s = Fig(640, 250)
    for k, (title, pair) in enumerate([('không BatchNorm', ('plain', 'residual')), ('có BatchNorm', ('plain + BN', 'residual + BN'))]):
        x0 = 60 + k * 300
        ax = s.axes(x0, 34, 230, 170, (0, 99), (-5, 1.5), xticks=[0, 50, 99], yticks=[-4, -2, 0], yfmt='', xlabel='bước')
        for e in (-4, -2, 0):
            s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
        s.label(x0 + 115, 20, title, 12.5, color=TEXT, weight=600)
        for nm, col in zip(pair, (CLAY, BLUE)):
            h = np.log10(np.maximum(np.array(C[nm]), 1e-5))
            ax.line(np.arange(len(h)), h, col, 1.8)
        if k == 0:
            s.label(ax.X(99) - 2, ax.Y(np.log10(C['plain'][-1])) - 10, 'plain kẹt ở ln 2', 11.5, 'end', CLAY)
            mi = int(np.argmax(C['residual']))
            s.mono(ax.X(mi) + 8, ax.Y(np.log10(C['residual'][mi])) + 4, f'{max(C["residual"]):.1f}', 11, 'start', BLUE)
        else:
            s.label(ax.X(60), ax.Y(np.log10(C['plain + BN'][60])) - 10, 'plain + BN', 11.5, 'middle', CLAY)
            s.label(ax.X(60), ax.Y(np.log10(C['residual + BN'][60])) + 16, 'residual + BN', 11.5, 'middle', BLUE)
    s.label(60 - 8, 24, 'loss train', 11.5, 'start', FAINT)
    s.save('5-2-depth', 'Mạng 18 lớp: không BatchNorm, mạng thẳng kẹt ở ln 2; residual học được.')


def grad52():
    G = run52()['grads']
    s = Fig(640, 200)
    ax = s.axes(170, 20, 380, 140, (-12, 0), (0, 4), xticks=[-12, -9, -6, -3, 0], xfmt='', grid=False, frame=False)
    for e in (-12, -9, -6, -3, 0):
        s.label(ax.X(e), 176, f'10{sup(e)}', 11, color=FAINT)
    for r, nm in enumerate(['plain', 'plain + BN', 'residual', 'residual + BN']):
        y = 26 + r * 34
        v = math.log10(G[nm])
        col = CLAY if nm == 'plain' else BLUE
        s.rect(ax.X(-12), y, ax.X(v) - ax.X(-12), 22, 'none', col, 3, .6, 0)
        s.label(160, y + 11, nm, 12, 'end', TEXT)
        s.mono(ax.X(v) + 8, y + 11, f'{G[nm]:.1e}', 11.5, 'start', col)
    s.label(360, 196, 'norm gradient của conv đầu ở bước 1', 11.5, color=MUTED)
    s.save('5-2-grad', 'Gradient tới lớp conv đầu: mạng thẳng không BatchNorm gần như bằng 0; có đường tắt hoặc BatchNorm thì không.')


def resnet52():
    stages = [('stem', 64, 56), ('layer1', 64, 56), ('layer2', 128, 28), ('layer3', 256, 14), ('layer4', 512, 7)]
    s = Fig(640, 220)
    x = 30
    for k, (nm, c_, hw) in enumerate(stages):
        h = 26 + hw * 2.2
        w = 18 + c_ / 8
        y = 110 - h / 2
        s.box(x, y, w, h, 'none', BLUE if k else FAINT, r=5, width=0, opacity=.12 + .05 * k)
        s.label(x + w / 2, 196, nm, 11.5, color=MUTED)
        s.mono(x + w / 2, 110.5, f'{c_}', 11.5, 'middle', TEXT)
        s.mono(x + w / 2, y - 10, f'{hw}×{hw}', 11, 'middle', MUTED)
        if k:
            s.arrow(x - 22, 110, x - 4, 110, LINE, 1.1)
        x += w + 26
    s.arrow(x - 22, 110, x - 4, 110, LINE, 1.1)
    s.box(x, 92, 60, 36, 'none', CLAY, r=6, width=0, opacity=.22)
    s.label(x + 30, 110, '1000', 12, color=TEXT)
    s.label(x + 30, 196, 'linear', 11.5, color=MUTED)
    s.label(320, 22, 'ảnh 224×224 · số trong khối là số kênh', 11.5, color=MUTED)
    s.save('5-2-resnet', 'ResNet-18: mỗi stage chia đôi cạnh, nhân đôi số kênh, tới 512 kênh 7×7.')


def bottleneck52():
    s = Fig(640, 230)
    for k, (lab, cin, cout) in enumerate([('1×1', 256, 64), ('3×3', 64, 64), ('1×1', 64, 256)]):
        y = 34 + k * 46
        s.box(60, y, 160, 34, 'none', CLAY if lab == '3×3' else BLUE, r=7, width=0, opacity=.24 if lab == '3×3' else .14)
        s.mono(140, y + 17.5, f'{lab}  {cin} → {cout}', 12, 'middle', TEXT)
    s.label(140, 20, 'bottleneck', 12.5, color=TEXT, weight=600)
    s.mono(140, 190, '69 632 tham số', 12.5, 'middle', CLAY, 600)
    for k in range(2):
        y = 57 + k * 46
        s.box(300, y, 160, 34, 'none', CLAY, r=7, width=0, opacity=.24)
        s.mono(380, y + 17.5, '3×3  256 → 256', 12, 'middle', TEXT)
    s.label(380, 20, 'hai conv 3×3 ở 256 kênh', 12.5, color=TEXT, weight=600)
    s.mono(380, 190, '1 179 648 tham số', 12.5, 'middle', MUTED, 600)
    s.label(560, 100, 'ít hơn', 12, color=MUTED)
    s.mono(560, 122, '≈ 17 lần', 13, 'middle', CLAY, 600)
    s.save('5-2-bottleneck', 'Bottleneck: conv 1×1 thu kênh lại, conv 3×3 chạy ở ít kênh, conv 1×1 mở ra; ít tham số hơn 17 lần.')


FIGS52 = {'5-2-samples': samples52, '5-2-cnn': cnn52, '5-2-metrics': metrics52, '5-2-residual': residual52,
          '5-2-depth': depth52, '5-2-grad': grad52, '5-2-resnet': resnet52, '5-2-bottleneck': bottleneck52}

# ───────────────────────────── 5.3 ─────────────────────────────


def sample(name, box, size):
    from sklearn.datasets import load_sample_image
    from PIL import Image
    return Image.fromarray(load_sample_image(name)).crop(box).resize((size, size), Image.LANCZOS)


def output_block(lesson, k):
    """Khối ```output thứ k của bài (đọc đúng số đã in trong bài)."""
    import re
    from p8_ch1 import CONTENT
    text = (CONTENT / f'phase-{lesson.split(".")[0]}' / f'{lesson}.md').read_text(encoding='utf-8')
    return re.findall(r'^```output\n(.*?)^```', text, re.M | re.S)[k]


def labels53():
    from sklearn.datasets import load_digits
    s = Fig(640, 230)
    fl = np.asarray(sample('flower.jpg', (140, 40, 500, 400), 240))
    six = load_digits().images[load_digits().target == 6][0]
    w = 70
    cols = [(24, 'hoa', 'vẫn là hoa', GREEN), (234, 'rẽ trái', 'thành rẽ phải', CLAY), (444, 'số 6', 'thành số 9', CLAY)]
    for x0, a, b, col in cols:
        s.arrow(x0 + w + 6, 80, x0 + w + 34, 80, LINE, 1.2)
        s.label(x0 + w / 2, 140, a, 12, color=TEXT)
        s.label(x0 + w + 40 + w / 2, 140, b, 12, color=col, weight=600)
    s.photo(24, 45, w, w, fl, max_px=200, radius=6)
    s.photo(24 + w + 40, 45, w, w, fl[:, ::-1], max_px=200, radius=6)
    s.mono(24 + w + 20, 64, 'lật', 10.5, 'middle', MUTED)

    def sign(x, d):
        s.box(x, 45, w, w, 'none', SAND, r=12, width=0, opacity=.3)
        cx, cy = x + w / 2, 80
        s.path(f'M {cx + 22 * d},{cy} L {cx - 18 * d},{cy}', TEXT, 5)
        s.path(f'M {cx - 4 * d},{cy - 15} L {cx - 20 * d},{cy} L {cx - 4 * d},{cy + 15}', TEXT, 5)
    sign(234, 1)
    sign(234 + w + 40, -1)
    s.mono(234 + w + 20, 64, 'lật', 10.5, 'middle', MUTED)
    digit(s, 444 + 3, 48, six, 8)
    digit(s, 444 + w + 40 + 3, 48, np.rot90(six, 2), 8)
    s.mono(444 + w + 20, 64, 'xoay', 10.5, 'middle', MUTED)
    s.label(320, 196, 'nhãn giữ hay đổi tùy điều mà nhãn mô tả', 11.5, color=MUTED)
    s.save('5-3-labels', 'Lật hoa vẫn là hoa; lật biển rẽ trái thành rẽ phải; xoay số 6 thành số 9.')


def photoaug53():
    from PIL import Image, ImageEnhance
    from sklearn.datasets import load_sample_image
    full = Image.fromarray(load_sample_image('china.jpg'))
    base = full.crop((40, 20, 400, 380)).resize((240, 240), Image.LANCZOS)
    crop = full.crop((120, 90, 300, 270)).resize((240, 240), Image.LANCZOS)
    rot = full.crop((-20, -40, 460, 440)).rotate(15, resample=Image.BILINEAR, fillcolor=(0, 0, 0)).crop((60, 60, 420, 420)).resize((240, 240))
    light = ImageEnhance.Contrast(ImageEnhance.Brightness(base).enhance(1.45)).enhance(.65)
    cut = np.asarray(base).copy()
    cut[70:150, 120:200] = 0
    tiles = [(base, 'gốc'), (base.transpose(Image.FLIP_LEFT_RIGHT), 'lật ngang'), (crop, 'crop rồi phóng'),
             (rot, 'xoay 15°'), (light, 'sáng hơn, nhạt hơn'), (cut, 'cutout')]
    s = Fig(640, 400)
    w = 150
    for k, (img, lab) in enumerate(tiles):
        x, y = 40 + (k % 3) * 200, 34 + (k // 3) * 186
        s.photo(x, y, w, w, np.asarray(img), max_px=300, radius=6)
        s.label(x + w / 2, y + w + 16, lab, 12, color=TEXT if k else MUTED)
    s.save('5-3-photo-aug', 'Năm phép augmentation trên một ảnh tháp; cả năm đều giữ nhãn.')


def boxflip53():
    ns = lesson_ns('5.3', upto=1)
    s = Fig(640, 200)
    c, g = 22, 2
    for k, (m, b, lab) in enumerate([(ns['mask'], ns['box'], 'trước'), (ns['flipped_mask'], ns['flipped_box'], 'sau khi lật')]):
        x0 = 40 + k * 300
        fills = {(i, j): (CLAY, .45) for i in range(4) for j in range(10) if m[i, j]}
        s.tiles(x0, 50, [[''] * 10] * 4, c, c, BLUE, g, fills, r=2, opacity=.1)
        x1, y1, x2, y2 = b
        s.box(x0 + x1 * (c + g) - 1, 50 + y1 * (c + g) - 1, (x2 - x1) * (c + g), (y2 - y1) * (c + g), BLUE, 'none', r=2, width=2)
        s.label(x0 + 5 * (c + g), 28, lab, 12.5, color=TEXT, weight=600)
        s.mono(x0 + 5 * (c + g), 168, f'box {list(map(int, b))}'.replace('[', '(').replace(']', ')'), 12, 'middle', BLUE)
    s.arrow(292, 98, 328, 98, LINE, 1.3)
    s.save('5-3-boxflip', 'Lật ảnh thì phải lật cả mask và box theo.')


def split53():
    s = Fig(640, 290)
    srcs = [('china.jpg', (40, 20, 400, 380), 'nguồn A'), ('flower.jpg', (140, 40, 500, 400), 'nguồn B'),
            ('china.jpg', (380, 120, 640, 380), 'nguồn C')]
    w = 44
    for k, (nm, (a, b, c_, d), lab) in enumerate(srcs):
        x0 = 30 + k * 200
        for f in range(3):
            img = sample(nm, (a + 12 * f, b + 6 * f, c_ + 12 * f - 30, d + 6 * f - 30), 120)
            s.photo(x0 + f * (w + 6), 40, w, w, np.asarray(img), max_px=100, radius=4)
        s.label(x0 + 75, 26, lab, 12, color=TEXT, weight=600)
    s.path('M 30,96 L 30,104 L 380,104 L 380,96', BLUE, 1.4)
    s.path('M 430,96 L 430,104 L 580,104 L 580,96', CLAY, 1.4)
    s.arrow(205, 108, 205, 140, BLUE, 1.3)
    s.arrow(505, 108, 505, 140, CLAY, 1.3)
    s.label(205, 160, 'train: A, B rồi mới augment', 12, color=BLUE, weight=600)
    s.label(505, 160, 'validation: C, không augment', 12, color=CLAY, weight=600)
    from PIL import Image
    v = sample('china.jpg', (40, 20, 370, 350), 120)
    for k, img in enumerate([v, v.transpose(Image.FLIP_LEFT_RIGHT), v.rotate(12, fillcolor=(0, 0, 0)), v.crop((20, 20, 100, 100)).resize((120, 120))]):
        s.photo(102 + k * 54, 178, w, w, np.asarray(img), max_px=100, radius=4)
    s.photo(483, 178, w, w, np.asarray(sample('china.jpg', (380, 120, 610, 350), 120)), max_px=100, radius=4)
    s.label(320, 262, 'các frame của một nguồn gần như trùng nhau: chia theo nguồn, không chia theo ảnh', 11.5, color=MUTED)
    s.save('5-3-split', 'Chia theo nguồn trước khi augment; augmentation chỉ sinh từ ảnh train.')


def digitaug53():
    ns = lesson_ns('5.3', upto=2)
    tx, ty = ns['train_x'], ns['train_y']
    i = int((ty == 2).nonzero()[0][0])
    shift = ns['shift']
    img = tx[i]
    tiles = [(img, 'gốc'), (shift(img, 0, 1), 'dời phải'), (shift(img, 1, 0), 'dời xuống'), (img.flip(-1), 'lật ngang')]
    s = Fig(640, 200)
    for k, (im, lab) in enumerate(tiles):
        x = 60 + k * 140
        s.box(x, 34, 96, 96, 'none', PAPER, r=6, width=0)
        digit(s, x, 34, im[0].numpy(), 12, CLAY if k == 3 else TEXT)
        s.label(x + 48, 150, lab, 12, color=CLAY if k == 3 else TEXT)
        s.label(x + 48, 170, 'nhãn 2', 11.5, color=MUTED)
    s.save('5-3-digit-aug', 'Dời một pixel vẫn là chữ 2; lật ngang thì không còn là chữ 2.')


def ablation53():
    rows = [l.split() for l in output_block('5.3', 2).strip().splitlines()[1:]]
    data = [(' '.join(r[:-2]), float(r[-2]), float(r[-1])) for r in rows]
    s = Fig(640, 240)
    ax = s.axes(80, 26, 440, 160, (0, 4), (0.5, 0.95), xticks=[], yticks=[.5, .6, .7, .8, .9], yfmt='{:.1f}', grid=False)
    for k, (nm, o, sh) in enumerate(data):
        x = ax.X(k + .5)
        for j, (v, col) in enumerate([(o, BLUE), (sh, CLAY)]):
            xx = x - 30 + j * 32
            s.rect(xx, ax.Y(v), 28, ax.Y(.5) - ax.Y(v), 'none', col, 3, .7, 0)
            s.mono(xx + 14, ax.Y(v) + 11, f'{v:.3f}'.lstrip('0'), 10, 'middle', PAPER)
        s.label(x, ax.y + ax.h + 16, nm, 12, color=TEXT)
    s.box(540, 60, 12, 12, 'none', BLUE, r=2, width=0, opacity=.7)
    s.label(558, 66, 'ảnh gốc', 12, 'start', MUTED)
    s.box(540, 84, 12, 12, 'none', CLAY, r=2, width=0, opacity=.7)
    s.label(558, 90, 'ảnh dời 1 px', 12, 'start', MUTED)
    s.label(ax.x - 8, ax.y - 12, 'accuracy validation', 11.5, 'start', FAINT)
    s.save('5-3-ablation', 'Phép dời giúp model đoán đúng ảnh bị dời; phép lật làm hại cả hai.')


def crop53():
    import torch
    from torchvision.transforms import RandomResizedCrop
    from PIL import Image
    from sklearn.datasets import load_sample_image
    im = Image.fromarray(load_sample_image('china.jpg'))
    W, H = im.size
    ob = (505, 150, 633, 235)                      # khoảng 4% diện tích ảnh
    oa = (ob[2] - ob[0]) * (ob[3] - ob[1])
    torch.manual_seed(0)
    crops = [RandomResizedCrop.get_params(im, (0.08, 1.0), (3 / 4, 4 / 3)) for _ in range(2000)]

    def has(c_):
        i, j, h, w = c_
        ix = max(0, min(j + w, ob[2]) - max(j, ob[0]))
        iy = max(0, min(i + h, ob[3]) - max(i, ob[1]))
        return ix * iy >= .5 * oa
    miss = 1 - np.mean([has(c_) for c_ in crops])
    s = Fig(640, 260)
    sc = 360 / W
    X0, Y0 = 30, 20
    s.photo(X0, Y0, W * sc, H * sc, np.asarray(im), max_px=520, radius=6)
    s.box(X0 + ob[0] * sc, Y0 + ob[1] * sc, (ob[2] - ob[0]) * sc, (ob[3] - ob[1]) * sc, '#ffffff', 'none', r=2, width=2)
    for c_ in crops[:6]:
        i, j, h, w = c_
        s.box(X0 + j * sc, Y0 + i * sc, w * sc, h * sc, '#7fd18b' if has(c_) else '#ff8a65', 'none', r=2, width=1.8)
    s.label(420, 60, 'vật cần nhận: khung trắng, 4% ảnh', 12, 'start', TEXT)
    s.label(420, 90, 'sáu crop ngẫu nhiên đầu tiên', 12, 'start', MUTED)
    s.label(420, 132, 'trên 2000 crop', 12, 'start', MUTED)
    s.mono(420, 158, f'{miss:.0%} không chứa', 13, 'start', CLAY, 600)
    s.mono(420, 178, 'nửa vật mà vẫn', 12, 'start', MUTED)
    s.mono(420, 196, 'mang nhãn “có vật”', 12, 'start', MUTED)
    s.save('5-3-crop', f'RandomResizedCrop mặc định (scale 0.08–1) trên ảnh thật với một vật chiếm 4% ở góc: trên 2000 crop, khoảng {miss:.0%} không chứa nổi nửa vật mà vẫn giữ nhãn.')


def gray53():
    s = Fig(640, 210)
    s.box(40, 70, 56, 56, 'none', FAINT, r=6, width=0, opacity=.3)
    s.mono(68, 98.5, 'x', 14, 'middle', TEXT)
    s.label(68, 146, '1 kênh', 11.5, color=MUTED)
    s.arrow(102, 80, 160, 52, LINE, 1.2)
    s.arrow(102, 116, 160, 146, LINE, 1.2)
    for k in range(3):
        s.box(160 + k * 6, 32 - k * 6, 60, 46, 'none', FAINT, r=5, width=0, opacity=.25)
    s.mono(202, 56, 'x x x', 11, 'middle', TEXT)
    s.arrow(236, 52, 290, 52, LINE, 1.2)
    s.box(296, 34, 130, 36, 'none', BLUE, r=7, width=0, opacity=.16)
    s.mono(361, 52.5, 'W₁ W₂ W₃', 12.5, 'middle', TEXT)
    s.box(166, 128, 48, 48, 'none', FAINT, r=5, width=0, opacity=.3)
    s.mono(190, 152.5, 'x', 12.5, 'middle', TEXT)
    s.arrow(220, 152, 290, 152, LINE, 1.2)
    s.box(296, 134, 130, 36, 'none', BLUE, r=7, width=0, opacity=.16)
    s.mono(361, 152.5, 'W₁ + W₂ + W₃', 12.5, 'middle', TEXT)
    s.arrow(432, 52, 486, 92, LINE, 1.2)
    s.arrow(432, 152, 486, 112, LINE, 1.2)
    s.label(536, 102, 'cùng đầu ra', 12.5, color=GREEN, weight=600)
    s.label(361, 20, 'chép thành ba kênh', 11.5, color=MUTED)
    s.label(361, 192, 'một kênh, gộp weight', 11.5, color=MUTED)
    s.save('5-3-gray', 'Ảnh xám chép thành ba kênh cho cùng đầu ra với conv một kênh có weight là tổng ba lát.')


FIGS53 = {'5-3-labels': labels53, '5-3-photo-aug': photoaug53, '5-3-boxflip': boxflip53, '5-3-split': split53,
          '5-3-digit-aug': digitaug53, '5-3-ablation': ablation53, '5-3-crop': crop53, '5-3-gray': gray53}

# ───────────────────────────── 5.4 ─────────────────────────────


def tower(size=224):
    return np.asarray(sample('china.jpg', (40, 20, 400, 380), size))


def patches54():
    img = tower(224)
    s = Fig(640, 250)
    W = 196
    s.photo(24, 30, W, W, img, max_px=448, radius=4)
    st = W / 14
    for k in range(1, 14):
        s.line(24 + k * st, 30, 24 + k * st, 30 + W, '#ffffff', .6)
        s.line(24, 30 + k * st, 24 + W, 30 + k * st, '#ffffff', .6)
    s.box(24 + 3 * st, 30 + 7 * st, 6 * st, st, CLAY, 'none', r=0, width=2)
    s.label(24 + W / 2, 18, '224×224 · patch 16 → lưới 14×14', 11.5, color=MUTED)
    s.arrow(236, 128, 270, 128, LINE, 1.2)
    w = 40
    for k in range(6):
        idx = 7 * 14 + 3 + k
        r, c_ = divmod(idx, 14)
        crop = img[16 * r:16 * r + 16, 16 * c_:16 * c_ + 16]
        x = 282 + k * (w + 8)
        s.photo(x, 104, w, w, blocky(crop, 160), max_px=160, radius=3)
        s.mono(x + w / 2, 160, str(idx), 11, 'middle', MUTED)
    s.mono(282 + 6 * (w + 8) + 2, 126, '…', 12, 'start', MUTED)
    s.label(440, 196, '196 token, mỗi token 3·16·16 = 768 số thô', 12, color=TEXT)
    s.label(424, 84, 'patch 101–106 của hàng 7', 11.5, color=MUTED)
    s.save('5-4-patches', 'Ảnh 224×224 chia patch 16×16 thành 196 token.')


def unfold54():
    ns = lesson_ns('5.4', upto=1)
    P = ns['patches'][0].to(int).numpy()
    s = Fig(640, 210)
    img = [[str(4 * i + j) for j in range(4)] for i in range(4)]
    cols = [BLUE, CLAY, GREEN, SAND]
    fills = {(i, j): (cols[(i // 2) * 2 + j // 2], .22) for i in range(4) for j in range(4)}
    s.tiles(40, 40, img, 34, 30, BLUE, 4, fills, size=12.5)
    s.label(108, 24, 'ảnh 4×4', 12, color=MUTED)
    s.arrow(196, 98, 236, 98, LINE, 1.2)
    s.label(216, 86, 'unfold', 11, color=MUTED)
    pf = {(i, j): (cols[i], .22) for i in range(4) for j in range(4)}
    s.tiles(250, 40, [[str(v) for v in r] for r in P], 34, 30, BLUE, 4, pf, size=12.5)
    s.label(318, 24, 'patch đúng', 12, color=GREEN, weight=600)
    wrong = [[str(4 * i + j) for j in range(4)] for i in range(4)]
    s.tiles(450, 40, wrong, 34, 30, FAINT, 4, size=12.5, opacity=.12)
    s.label(518, 24, 'cắt mỗi 4 số', 12, color=CLAY, weight=600)
    s.label(518, 186, 'mỗi “patch” là một hàng ảnh', 11.5, color=CLAY)
    s.label(318, 186, 'mỗi hàng là một ô 2×2', 11.5, color=GREEN)
    s.save('5-4-unfold', 'unfold rồi permute cho patch đúng; flatten rồi cắt chỉ lấy một hàng ảnh.')


def sequence54():
    s = Fig(640, 210)
    s.box(30, 40, 54, 40, 'none', CLAY, r=6, width=0, opacity=.3)
    s.mono(57, 60.5, 'CLS', 12, 'middle', TEXT, 600)
    for k in range(5):
        s.box(92 + k * 46, 40, 40, 40, 'none', BLUE, r=6, width=0, opacity=.16)
        s.mono(112 + k * 46, 60.5, str(k), 11.5, 'middle', TEXT)
    s.mono(334, 60.5, '…', 13, 'middle', MUTED)
    s.box(352, 40, 40, 40, 'none', BLUE, r=6, width=0, opacity=.16)
    s.mono(372, 60.5, '195', 11, 'middle', TEXT)
    for k in range(8):
        x = [57, 112, 158, 204, 250, 296, 334, 372][k]
        if k != 6:
            s.mono(x, 100, '+', 12, 'middle', GREEN)
    s.label(214, 118, 'position embedding (1, 197, 768), học được', 11.5, color=GREEN)
    s.arrow(214, 132, 214, 152, LINE, 1.2)
    s.box(40, 156, 350, 34, 'none', FAINT, r=7, width=0, opacity=.16)
    s.label(215, 173, 'Transformer encoder · (B, 197, 768)', 12, color=TEXT)
    s.arrow(392, 173, 440, 173, CLAY, 1.4)
    s.label(500, 173, 'output CLS → head', 12, color=CLAY, weight=600)
    s.label(214, 24, '1 class token + 196 patch token', 12, color=MUTED)
    s.save('5-4-sequence', 'Chuỗi vào ViT: token CLS và 196 patch token, cộng mã vị trí, shape (B, 197, 768).')


def reach54():
    s = Fig(640, 250)
    n, c, g = 14, 11, 1
    for k, (title, r) in enumerate([('conv 3×3, 4 lớp', 4), ('conv 3×3, 13 lớp', 13), ('attention, 1 lớp', 99)]):
        x0 = 30 + k * 205
        fills = {(i, j): ((CLAY, .55) if i == j == 0 else (BLUE if r < 99 else GREEN, .3)) for i in range(n) for j in range(n)
                 if max(i, j) <= r}
        s.tiles(x0, 40, [[''] * n] * n, c, c, FAINT, g, fills, r=1, opacity=.08)
        s.label(x0 + 84, 24, title, 12, color=TEXT, weight=600)
    s.label(320, 228, 'vùng ô (0, 0) đọc được trên lưới 14×14 patch', 11.5, color=MUTED)
    s.save('5-4-reach', 'Conv 3×3 cần 13 lớp mới nối hai góc ảnh; một lớp attention đã nối mọi patch.')


def cost54():
    s = Fig(640, 230)
    sizes = [224, 384, 448]
    ax = s.axes(150, 24, 380, 150, (0, 700000), (0, 3), xticks=[], yticks=[], grid=False, frame=False)
    for r, hw in enumerate(sizes):
        L = (hw // 16) ** 2
        y = 34 + r * 50
        cells = (L + 1) ** 2
        s.rect(150, y, cells / 700000 * 380, 30, 'none', CLAY if r else BLUE, 3, .6, 0)
        s.label(140, y + 15, f'{hw}×{hw}', 12.5, 'end', TEXT)
        s.mono(150 + cells / 700000 * 380 + 8, y + 15, f'{L + 1} token · {cells:,} ô'.replace(',', ' '), 11.5, 'start', TEXT)
    s.label(340, 200, 'ô attention mỗi head, mỗi lớp = (L + 1)²; cạnh ảnh gấp đôi thì gấp khoảng 16', 11.5, color=MUTED)
    s.save('5-4-cost', 'Gấp đôi cạnh ảnh thì ma trận attention gấp khoảng 16 lần.')


def shuffle54():
    img = tower(192)
    g = 4
    p = img.shape[0] // g
    tiles = [img[p * i:p * i + p, p * j:p * j + p] for i in range(g) for j in range(g)]
    rng = np.random.default_rng(3)
    perm = rng.permutation(g * g)
    sh = np.zeros_like(img)
    for k, t in enumerate(perm):
        i, j = divmod(k, g)
        sh[p * i:p * i + p, p * j:p * j + p] = tiles[t]
    s = Fig(640, 250)
    w = 170
    for k, (im, lab) in enumerate([(img, 'ảnh gốc'), (sh, 'cùng 16 patch, đổi chỗ')]):
        x = 40 + k * 220
        s.photo(x, 34, w, w, im, max_px=340, radius=4)
        for q in range(1, g):
            s.line(x + q * w / g, 34, x + q * w / g, 34 + w, '#ffffff', 1)
            s.line(x, 34 + q * w / g, x + w, 34 + q * w / g, '#ffffff', 1)
        s.label(x + w / 2, 22, lab, 12, color=TEXT, weight=600)
    s.label(530, 90, 'không có vị trí:', 12, color=MUTED)
    s.label(530, 110, 'mean pooling bằng nhau', 12, color=CLAY, weight=600)
    s.label(530, 150, 'cộng mã vị trí cố định:', 12, color=MUTED)
    s.label(530, 170, 'output khác nhau', 12, color=GREEN, weight=600)
    s.save('5-4-position', 'Thiếu mã vị trí, hai ảnh cùng tập patch khác bố cục cho cùng kết quả.')


def posinterp54():
    ns = lesson_ns('5.4', upto=5)
    old = ns['table'][0, 1:].numpy()
    new = ns['resized'][0, 1:].numpy()
    s = Fig(640, 230)
    for k, (tab, n, title) in enumerate([(old, 4, 'lưới 4×4 · 16 vector'), (new, 7, 'lưới 7×7 · 49 vector')]):
        x0, side = 70 + k * 270, 150
        st = side / (n - 1)
        for idx, (r, c_) in enumerate(tab):
            i, j = divmod(idx, n)
            col = BLUE if (r + c_) / 6 < .5 else CLAY
            s.circle(x0 + j * st, 44 + i * st, 7 if n == 4 else 5.5, col, col, 0, .25 + .6 * (r + c_) / 6)
        s.label(x0 + side / 2, 24, title, 12, color=TEXT, weight=600)
    s.arrow(244, 119, 316, 119, LINE, 1.3)
    s.label(280, 106, 'nội suy 2D', 11.5, color=MUTED)
    s.label(320, 220, 'màu theo hàng + cột của vector; CLS (−1, −1) tách riêng, giữ nguyên', 11.5, color=MUTED)
    s.save('5-4-posinterp', 'Nội suy bảng vị trí từ lưới 4×4 sang 7×7; CLS tách ra rồi ghép lại.')


FIGS54 = {'5-4-patches': patches54, '5-4-unfold': unfold54, '5-4-sequence': sequence54, '5-4-reach': reach54,
          '5-4-cost': cost54, '5-4-position': shuffle54, '5-4-posinterp': posinterp54}

# ───────────────────────────── 5.5 ─────────────────────────────


def boxes_on(s, ax, boxes, cols, labels=None, width=1.8, fill=.12):
    """Vẽ box xyxy theo hệ trục ax (y hướng xuống như ảnh: ylim đảo)."""
    for k, (b, col) in enumerate(zip(boxes, cols)):
        x1, y1, x2, y2 = b
        s.box(ax.X(x1), ax.Y(y1), ax.X(x2) - ax.X(x1), ax.Y(y2) - ax.Y(y1), col, col if fill else 'none', r=1,
              width=width, opacity=fill if fill else 1)
        if labels:
            s.label(ax.X(x1) + 6, ax.Y(y1) + 13, labels[k], 11.5, 'start', col, 600)


def formats55():
    from sklearn.datasets import load_sample_image
    im = load_sample_image('china.jpg')
    H, W = im.shape[:2]
    b = (60, 25, 355, 400)
    s = Fig(640, 250)
    sc = 300 / W
    X0, Y0 = 20, 20
    s.photo(X0, Y0, W * sc, H * sc, im, max_px=600, radius=6)
    s.box(X0 + b[0] * sc, Y0 + b[1] * sc, (b[2] - b[0]) * sc, (b[3] - b[1]) * sc, '#ffd166', 'none', r=1, width=2.2)
    cx, cy, w, h = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, b[2] - b[0], b[3] - b[1]
    s.circle(X0 + cx * sc, Y0 + cy * sc, 3.5, '#ffd166', '#ffd166', 0)
    rows = [('xyxy · pixel', f'({b[0]}, {b[1]}, {b[2]}, {b[3]})', 'TorchVision'),
            ('xywh · pixel', f'({b[0]}, {b[1]}, {w}, {h})', 'COCO JSON'),
            ('cxcywh · 0–1', f'({cx / W:.3f}, {cy / H:.3f}, {w / W:.3f}, {h / H:.3f})', 'nhãn YOLO')]
    for k, (a, v, src) in enumerate(rows):
        y = 50 + k * 56
        s.label(346, y, a, 12, 'start', TEXT, 600)
        s.label(626, y, src, 11.5, 'end', MUTED)
        s.mono(346, y + 22, v, 12, 'start', CLAY)
    s.label(170, 236, f'ảnh {W}×{H}, box đặt tay quanh tháp', 11.5, color=MUTED)
    s.save('5-5-formats', 'Cùng một box ghi theo ba quy ước: xyxy, xywh của COCO, cxcywh chuẩn hóa của YOLO.')


def iou55():
    s = Fig(640, 230)
    ax = s.axes(70, 20, 170, 170, (-.5, 5.5), (5.5, -.5), grid=False, frame=False)
    boxes_on(s, ax, [(0, 0, 4, 4), (1, 1, 5, 5)], [BLUE, CLAY], ['A', 'B'])
    s.box(ax.X(1), ax.Y(1), ax.X(4) - ax.X(1), ax.Y(4) - ax.Y(1), 'none', GREEN, r=0, width=0, opacity=.3)
    s.mono(ax.X(2.5), ax.Y(2.5), '9', 15, 'middle', TEXT, 600)
    s.mono(310, 70, 'giao  = 3·3 = 9', 13, 'start', TEXT)
    s.mono(310, 100, 'hợp   = 16 + 16 − 9 = 23', 13, 'start', TEXT)
    s.mono(310, 140, 'IoU   = 9/23 ≈ 0.391', 13.5, 'start', CLAY, 600)
    s.label(310, 176, 'chưa đạt ngưỡng 0.5', 12, 'start', MUTED)
    s.save('5-5-iou', 'IoU = 9 / (16 + 16 − 9) ≈ 0.39.')


def shift55():
    s = Fig(640, 230)
    ax = s.axes(80, 20, 400, 160, (0, 4), (0, 1), xticks=[0, 1, 2, 3, 4], yticks=[0, .5, 1], xlabel='lệch ngang (pixel)')
    d = np.linspace(0, 4, 81)
    ax.hline(.5, FAINT, 1, '4 4')
    for side, col in [(4, CLAY), (16, SAND), (40, BLUE)]:
        iou = np.clip((side - d) / (side + d), 0, 1)
        ax.line(d, iou, col, 2.2)
        s.label(ax.X(4) + 8, ax.Y(iou[-1]), f'box {side}×{side}', 12, 'start', col, 600)
    s.circle(ax.X(1), ax.Y(.6), 4.5, CLAY, PAPER, 2)
    s.mono(ax.X(1) + 8, ax.Y(.6) - 8, '0.6', 11.5, 'start', CLAY)
    s.circle(ax.X(1), ax.Y(39 / 41), 4.5, BLUE, PAPER, 2)
    s.mono(ax.X(1), ax.Y(39 / 41) - 10, '0.95', 11.5, 'middle', BLUE)
    s.label(ax.x - 8, ax.y - 10, 'IoU', 11.5, 'start', FAINT)
    s.save('5-5-shift', 'Lệch 1 pixel: box 40×40 còn IoU 0.95, box 4×4 chỉ còn 0.6.')


def nms55():
    ns = lesson_ns('5.5', upto=2)
    B, S, kept = ns['boxes'], ns['scores'], ns['kept']
    s = Fig(640, 210)
    for k, (title, show) in enumerate([('trước NMS', [0, 1, 2]), ('sau NMS', kept)]):
        ax = s.axes(40 + k * 310, 44, 260, 106, (-.5, 10.5), (5, -.5), grid=False, frame=False)
        cols = {0: BLUE, 1: CLAY, 2: GREEN}
        boxes_on(s, ax, [B[i] for i in show], [cols[i] for i in show], fill=.08)
        for i in show:
            x1, y1, x2, y2 = B[i]
            yy = ax.Y(y2) + 14 if i == 1 else ax.Y(y1) - 7
            s.mono(ax.X(x1) + (ax.X(x2) - ax.X(x1)) / 2 + (8 if i == 1 else 0), yy, f'{i} · {S[i]:g}', 11.5, 'middle', cols[i])
        s.label(40 + k * 310 + 130, 22, title, 12.5, color=TEXT, weight=600)
    s.arrow(296, 95, 334, 95, LINE, 1.3)
    s.label(320, 190, 'box 1 chồng box 0 với IoU ≈ 0.62 > 0.5 nên bị loại; box 2 ở xa nên giữ', 11.5, color=MUTED)
    s.save('5-5-nms', 'NMS giữ box 0 và box 2, bỏ box 1 vì chồng box 0 quá ngưỡng.')


def classnms55():
    s = Fig(640, 230)
    rider = [(0, 0, 4, 8), (0, 2, 4, 9)]
    for k, (title, keep) in enumerate([('trộn lớp: nms', [0]), ('theo lớp: batched_nms', [0, 1])]):
        ax = s.axes(90 + k * 280, 36, 120, 150, (-1, 5), (9.5, -.5), grid=False, frame=False)
        boxes_on(s, ax, [rider[i] for i in keep], [[BLUE, CLAY][i] for i in keep], [['người 0.9', 'xe đạp 0.8'][i] for i in keep], fill=.1)
        if 1 not in keep:
            x1, y1, x2, y2 = rider[1]
            s.box(ax.X(x1), ax.Y(y1), ax.X(x2) - ax.X(x1), ax.Y(y2) - ax.Y(y1), FAINT, 'none', r=1, width=1.2, dash=None)
            s.mono(ax.X(2), ax.Y(9) + 14, 'xe đạp bị xóa', 11.5, 'middle', CLAY)
        s.label(90 + k * 280 + 60, 20, title, 12.5, color=TEXT, weight=600)
    s.mono(560, 100, 'IoU 0.667', 12.5, 'middle', MUTED)
    s.save('5-5-classnms', 'NMS trộn lớp xóa nhầm box xe đạp; batched_nms chỉ so box cùng lớp.')


def match55():
    s = Fig(640, 220)
    ax = s.axes(40, 40, 300, 130, (-.5, 10.5), (4.8, -.5), grid=False, frame=False)
    boxes_on(s, ax, [(0, 0, 4, 4), (6, 0, 10, 4)], [GREEN, GREEN], ['chai A', 'chai B'], fill=.14)
    rows = [('1', 'A', 'TP', '1', '1/2'), ('2', 'A lần nữa', 'FP', '1/2', '1/2'), ('3', 'B', 'TP', '2/3', '1')]
    hx = [380, 430, 520, 570, 616]
    for x, h in zip(hx, ['thứ tự', 'khoanh', '', 'P', 'R']):
        s.label(x, 48, h, 11.5, color=MUTED)
    for r, (i, w, f, p, rc) in enumerate(rows):
        y = 78 + r * 30
        s.mono(hx[0], y, i, 12, 'middle', TEXT)
        s.label(hx[1], y, w, 12, color=TEXT)
        s.label(hx[2], y, f, 12, color=GREEN if f == 'TP' else CLAY, weight=600)
        s.mono(hx[3], y, p, 12, 'middle', TEXT)
        s.mono(hx[4], y, rc, 12, 'middle', TEXT)
    s.label(190, 196, 'mỗi ground truth chỉ được ghép một lần', 11.5, color=MUTED)
    s.save('5-5-match', 'Box thứ hai trên cùng chai A là FP vì chai A đã được ghép.')


def pr55():
    s = Fig(640, 230)
    ax = s.axes(80, 20, 380, 170, (0, 1.05), (0, 1.1), xticks=[0, .5, 1], yticks=[0, 2 / 3, 1], yfmt='{:.2g}', xlabel='recall')
    s.rect(ax.X(0), ax.Y(1), ax.X(.5) - ax.X(0), ax.Y(0) - ax.Y(1), 'none', BLUE, 0, .16, 0)
    s.rect(ax.X(.5), ax.Y(2 / 3), ax.X(1) - ax.X(.5), ax.Y(0) - ax.Y(2 / 3), 'none', CLAY, 0, .18, 0)
    ax.line([0, .5, .5, 1], [1, 1, 2 / 3, 2 / 3], TEXT, 2)
    ax.dots([.5, .5, 1], [1, .5, 2 / 3], CLAY, 4.5, CLAY)
    s.mono(ax.X(.25), ax.Y(.5), '1/2', 14, 'middle', TEXT)
    s.mono(ax.X(.75), ax.Y(.33), '1/3', 14, 'middle', TEXT)
    s.label(ax.X(.5) + 8, ax.Y(.5) + 4, 'FP: (0.5, 1/2)', 11, 'start', CLAY)
    s.label(ax.x - 8, ax.y - 10, 'precision', 11.5, 'start', FAINT)
    s.mono(540, 100, 'AP = 1/2 + 1/3', 13, 'middle', TEXT)
    s.mono(540, 126, '= 5/6', 14, 'middle', CLAY, 600)
    s.save('5-5-pr', 'AP là diện tích dưới đường bao precision: 5/6.')


def yolo55():
    s = Fig(640, 220)
    n, c = 13, 9
    s.tiles(40, 30, [[''] * n] * n, c, c, BLUE, 1, {(6, 6): (CLAY, .6)}, r=1, opacity=.12)
    s.label(104, 172, 'lưới 13×13', 12, color=MUTED)
    for a in range(3):
        y = 34 + a * 46
        parts = [('4', 'box', BLUE), ('1', 'obj', GREEN), ('80', 'lớp', CLAY)]
        x = 230
        for v, lab, col in parts:
            w = 30 if v != '80' else 150
            s.box(x, y, w, 30, 'none', col, r=5, width=0, opacity=.22)
            s.mono(x + w / 2, y + 15.5, v, 11.5, 'middle', TEXT)
            x += w + 4
        s.label(222, y + 15, f'anchor {a + 1}', 11, 'end', MUTED)
    s.label(330, 178, 'mỗi ô: 3 × (4 + 1 + 80) = 255 số', 12, color=TEXT)
    s.mono(540, 90, '169 · 255', 13, 'middle', MUTED)
    s.mono(540, 114, '= 43 095', 14, 'middle', CLAY, 600)
    s.save('5-5-yolo', 'Head YOLO trên lưới 13×13: mỗi ô 3 anchor, mỗi anchor 85 số.')


def letterbox55():
    s = Fig(640, 240)
    sc = .12
    s.box(30, 50, 1280 * sc, 720 * sc, 'none', BLUE, r=3, width=0, opacity=.16)
    s.box(30 + 200 * sc, 50 + 200 * sc, 400 * sc, 200 * sc, CLAY, 'none', r=1, width=2)
    s.label(30 + 640 * sc, 36, 'ảnh gốc 1280×720', 12, color=TEXT, weight=600)
    s.mono(30 + 640 * sc, 50 + 720 * sc + 18, '(200, 200, 600, 400)', 11.5, 'middle', CLAY)
    s.arrow(206, 94, 252, 94, LINE, 1.2)
    s.label(229, 82, '× 0.5', 11, color=MUTED)
    t = .2
    x0, y0 = 262, 20
    s.box(x0, y0, 640 * t, 640 * t, 'none', FAINT, r=3, width=0, opacity=.16)
    s.box(x0, y0 + 140 * t, 640 * t, 360 * t, 'none', BLUE, r=0, width=0, opacity=.16)
    s.box(x0 + 100 * t, y0 + 240 * t, 200 * t, 100 * t, CLAY, 'none', r=1, width=2)
    s.mono(x0 + 64, y0 + 14, 'đệm 140', 10.5, 'middle', MUTED)
    s.mono(x0 + 64, y0 + 640 * t - 8, 'đệm 140', 10.5, 'middle', MUTED)
    s.label(x0 + 64, y0 + 640 * t + 18, 'vào model 640×640', 12, color=TEXT, weight=600)
    s.mono(x0 + 64, y0 + 640 * t + 38, '(100, 240, 300, 340)', 11.5, 'middle', CLAY)
    s.label(420, 80, 'đổi về ảnh gốc:', 12, 'start', TEXT, 600)
    s.mono(420, 106, '1. trừ đệm: y − 140', 12, 'start', TEXT)
    s.mono(420, 130, '2. chia s = 0.5', 12, 'start', TEXT)
    s.label(420, 164, 'làm ngược thứ tự là lệch box', 11.5, 'start', CLAY)
    s.save('5-5-letterbox', 'Letterbox: ảnh 1280×720 thu về 640×360 rồi đệm 140 pixel trên và dưới; box trên ảnh vuông phải trừ đệm trước, chia hệ số 0.5 sau mới về đúng ảnh gốc.')


FIGS55 = {'5-5-formats': formats55, '5-5-iou': iou55, '5-5-shift': shift55, '5-5-nms': nms55, '5-5-classnms': classnms55,
          '5-5-match': match55, '5-5-pr': pr55, '5-5-yolo': yolo55, '5-5-letterbox': letterbox55}

# ───────────────────────────── 5.6 ─────────────────────────────

_F56 = {}


def flower_masks():
    """Mask hoa trên flower.jpg bằng ngưỡng màu + mở/đóng hình thái; hai thành phần lớn nhất là hai bông hoa."""
    if not _F56:
        from sklearn.datasets import load_sample_image
        from scipy import ndimage
        im = load_sample_image('flower.jpg')
        r, g, b = (im[..., k].astype(int) for k in range(3))
        m = (r > 140) & (r - b > 60) & (r - g > 20)
        m = ndimage.binary_fill_holes(ndimage.binary_opening(m, iterations=2))
        lab, n = ndimage.label(m)
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        order = np.argsort(-sizes)[:2] + 1
        inst = np.zeros(m.shape, int)
        for k, l in enumerate(order, 1):
            inst[lab == l] = k
        _F56.update(im=im, inst=inst)
    return _F56


def tint(im, mask_rgb, alpha=.55):
    out = im.astype(float).copy()
    sel = mask_rgb.sum(-1) > 0
    out[sel] = (1 - alpha) * out[sel] + alpha * mask_rgb[sel]
    return out.astype('uint8')


def masks56():
    F_ = flower_masks()
    im, inst = F_['im'], F_['inst']
    sem = np.full_like(im, 236)
    sem[inst > 0] = (217, 119, 87)
    ins = np.full_like(im, 236)
    ins[inst == 1] = (217, 119, 87)
    ins[inst == 2] = (70, 120, 170)
    s = Fig(640, 210)
    w, h = 190, 127
    for k, (img, title) in enumerate([(im, 'ảnh'), (sem, 'semantic: một lớp “hoa”'), (ins, 'instance: hoa 1, hoa 2')]):
        x = 20 + k * 207
        s.photo(x, 34, w, h, img, max_px=420, radius=6)
        s.label(x + w / 2, 22, title, 12, color=TEXT, weight=600)
    s.label(320, 190, 'mask đặt tay bằng ngưỡng màu; bông dưới bị khung ảnh cắt mất một phần', 11.5, color=MUTED)
    s.save('5-6-masks', 'Semantic mask gán cùng lớp “hoa”; instance mask tách từng bông.')


def area56():
    F_ = flower_masks()
    im, inst = F_['im'], F_['inst']
    m = inst == 1
    ys, xs = np.nonzero(m)
    x1, x2, y1, y2 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    frac = m.sum() / ((x2 - x1) * (y2 - y1))
    crop = im[y1:y2, x1:x2]
    s = Fig(640, 230)
    sz = 170
    s.photo(40, 30, sz, sz, crop, max_px=340, radius=4)
    s.box(40, 30, sz, sz, '#ffd166', 'none', r=4, width=2)
    mk = np.full_like(crop, 236)
    mk[m[y1:y2, x1:x2]] = (217, 119, 87)
    s.photo(260, 30, sz, sz, mk, max_px=340, radius=4)
    s.box(260, 30, sz, sz, '#ffd166', 'none', r=4, width=2)
    s.label(125, 18, 'box quanh bông hoa', 12, color=TEXT, weight=600)
    s.label(345, 18, 'mask của bông hoa', 12, color=TEXT, weight=600)
    s.label(470, 90, 'pixel hoa chiếm', 12, 'start', MUTED)
    s.mono(470, 116, f'{frac:.0%} của box', 14, 'start', CLAY, 600)
    s.label(470, 150, 'phần còn lại là nền', 12, 'start', MUTED)
    s.save('5-6-area', 'Hoa chỉ chiếm khoảng 75% diện tích box.')


def maskmetrics56():
    s = Fig(640, 200)
    g = [1, 1, 1, 0]
    p = [1, 1, 0, 1]
    c = 46
    s.tiles(150, 40, [[str(v) for v in g]], c, 34, GREEN, 6, {(0, j): (GREEN, .3 if v else .06) for j, v in enumerate(g)}, size=13)
    s.tiles(150, 86, [[str(v) for v in p]], c, 34, BLUE, 6, {(0, j): (BLUE, .3 if v else .06) for j, v in enumerate(p)}, size=13)
    s.label(140, 57, 'ground truth', 12, 'end', MUTED)
    s.label(140, 103, 'dự đoán', 12, 'end', MUTED)
    tags = [('TP', GREEN), ('TP', GREEN), ('FN', CLAY), ('FP', CLAY)]
    for j, (t, col) in enumerate(tags):
        s.label(150 + j * (c + 6) + c / 2, 140, t, 12, color=col, weight=600)
    s.mono(390, 70, 'IoU  = 2 / 4 = 0.5', 13, 'start', TEXT)
    s.mono(390, 100, 'Dice = 4 / 6 ≈ 0.667', 13, 'start', TEXT)
    s.label(390, 134, 'TN không có trong công thức', 11.5, 'start', MUTED)
    s.save('5-6-mask-metrics', 'TP = 2, FN = 1, FP = 1: IoU = 0.5, Dice ≈ 0.667.')


def aggregate56():
    s = Fig(640, 210)
    rows = [('ảnh A, vật lớn', 180 / 190), ('ảnh B, vật nhỏ', 2 / 11), ('trung bình theo ảnh', (180 / 190 + 2 / 11) / 2), ('gộp pixel', 182 / 201)]
    for r, (nm, v) in enumerate(rows):
        y = 26 + r * 40
        col = CLAY if r == 2 else (BLUE if r == 3 else FAINT)
        s.rect(200, y, v * 340, 26, 'none', col, 3, .55 if r >= 2 else .35, 0)
        s.label(190, y + 13, nm, 12, 'end', TEXT, 600 if r >= 2 else 400)
        s.mono(200 + v * 340 + 8, y + 13, f'{v:.3f}', 12, 'start', col if r >= 2 else MUTED)
    s.label(370, 196, 'vật lớn chiếm gần hết pixel nên cách gộp che lỗi bỏ sót vật nhỏ', 11.5, color=MUTED)
    s.save('5-6-aggregate', 'Trung bình Dice theo ảnh 0.565; gộp pixel thì 0.905.')


def unet56():
    s = Fig(640, 250)

    def blk(x, y, w, h, ch, hw, col, op=.18):
        s.box(x, y, w, h, 'none', col, r=5, width=0, opacity=op)
        s.mono(x + w / 2, y + h / 2 + .5, str(ch), 11.5, 'middle', TEXT)
        s.mono(x + w / 2, y + h + 12, hw, 10.5, 'middle', MUTED)
    blk(30, 50, 26, 80, 1, '12×12', FAINT, .3)
    s.label(43, 34, 'ảnh', 11.5, color=MUTED)
    blk(96, 50, 34, 80, 4, '12×12', BLUE)
    blk(150, 160, 34, 40, 4, '6×6', BLUE, .12)
    blk(216, 160, 50, 40, 8, '6×6', BLUE, .28)
    s.label(241, 230, 'middle', 11.5, color=MUTED)
    blk(300, 50, 50, 80, 8, '12×12', BLUE, .28)
    s.label(325, 34, 'phóng to', 11.5, color=MUTED)
    blk(380, 50, 76, 80, 12, '12×12', GREEN, .25)
    blk(486, 50, 34, 80, 4, '12×12', BLUE)
    s.label(503, 34, 'decode', 11.5, color=MUTED)
    blk(560, 50, 26, 80, 1, '12×12', CLAY, .35)
    s.label(573, 34, 'logits', 11.5, color=MUTED)
    for a, b in [(58, 94), (352, 378), (458, 484), (522, 558)]:
        s.arrow(a, 90, b, 90, LINE, 1.2)
    s.arrow(113, 146, 150, 168, LINE, 1.2)
    s.label(110, 176, 'pool', 11, 'end', MUTED)
    s.arrow(186, 180, 214, 180, LINE, 1.2)
    s.arrow(268, 170, 304, 146, LINE, 1.2)
    s.path('M 113,50 L 113,22 L 395,22 L 395,46', GREEN, 1.6)
    s.arrow(395, 36, 395, 48, GREEN, 1.6)
    s.label(254, 14, 'skip: encode (4 kênh) nối với 8 kênh phóng to', 11.5, color=GREEN, weight=600)
    s.save('5-6-unet', 'TinyUNet: thu nhỏ, phóng to, nối với nhánh skip, ra một logit mỗi pixel.')


def rects56():
    ns = lesson_ns('5.6', upto=3)
    import torch
    V, Y = ns['valid_x'], ns['valid_y']
    with torch.no_grad():
        P = (ns['model'](V).sigmoid() >= .5).float()
    s = Fig(640, 260)
    w = 78
    for i in range(5):
        x = 120 + i * (w + 22)
        for r, (arr, col) in enumerate([(V[i, 0].numpy(), None), (Y[i, 0].numpy(), GREEN), (P[i, 0].numpy(), BLUE)]):
            y = 20 + r * (w + 4)
            if col is None:
                img = blocky(ink(arr, 100), 156)
            else:
                rgb_ = {GREEN: (110, 160, 110), BLUE: (70, 120, 170)}[col]
                img = np.full((12, 12, 3), 250, 'uint8')
                img[arr > .5] = rgb_
                img = blocky(img, 156)
            s.photo(x, y, w, w, img, max_px=160, radius=3)
    for r, lab in enumerate(['ảnh', 'mask thật', 'dự đoán']):
        s.label(108, 20 + r * (w + 4) + w / 2, lab, 12, 'end', MUTED)
    s.save('5-6-rects', 'Mask thật và mask TinyUNet dự đoán gần như trùng nhau.')


def rle56():
    s = Fig(640, 210)
    m = [[0, 1, 0], [1, 1, 0]]
    c = 40
    for k, (title, order, runs) in enumerate([('trải theo hàng', 'C', '(2, 1, 4, 2)'), ('trải theo cột', 'F', '(2, 3)')]):
        x0 = 60 + k * 300
        fills = {(i, j): (CLAY, .35) for i in range(2) for j in range(3) if m[i][j]}
        num = np.arange(1, 7).reshape(2, 3, order=order)
        s.tiles(x0, 44, [[str(num[i, j]) for j in range(3)] for i in range(2)], c, c, BLUE, 4, fills, size=12.5, opacity=.08)
        s.label(x0 + 62, 28, title, 12.5, color=TEXT, weight=600)
        s.mono(x0 + 62, 150, f'RLE {runs}', 13, 'middle', CLAY, 600)
        seq = np.array(m).ravel(order=order)
        s.mono(x0 + 62, 176, ' '.join(map(str, seq)), 12, 'middle', MUTED)
    s.label(320, 200, 'cùng một mask, hai chuỗi khác nhau: số trong ô là chỉ số khi trải', 11.5, color=MUTED)
    s.save('5-6-rle', 'Trải theo hàng hay theo cột cho hai chuỗi RLE khác nhau.')


def resize56():
    s = Fig(640, 200)
    c = 44
    src = ['0', '0', '2', '2']
    s.tiles(60, 30, [src], c, 30, BLUE, 4, {(0, j): (CLAY if v == '2' else BLUE, .3 if v == '2' else .1) for j, v in enumerate(src)}, size=12.5)
    s.label(50, 45, 'mask', 12, 'end', MUTED)
    bil = ['0', '0', '0', '0.5', '1.5', '2', '2', '2']
    bl = ['0', '0', '0', '0', '1', '2', '2', '2']
    nn_ = ['0', '0', '0', '0', '2', '2', '2', '2']
    for r, (row, lab) in enumerate([(bil, 'bilinear'), (bl, 'rồi .long()'), (nn_, 'nearest')]):
        y = 76 + r * 40
        fills = {(0, j): ((CLAY, .3) if v == '2' else (SAND, .45) if v not in ('0', '2') else (BLUE, .1)) for j, v in enumerate(row)}
        s.tiles(260, y, [row], 40, 30, BLUE, 3, fills, size=11.5)
        s.label(250, y + 15, lab, 12, 'end', MUTED if r < 2 else GREEN)
    s.label(436, 64, '8 cột', 11.5, color=MUTED)
    s.label(108, 100, '0 nền, 1 giấy, 2 mực', 11.5, color=MUTED)
    s.save('5-6-resize', 'Phóng mask bằng bilinear sinh nhãn không có; nearest chỉ chép nhãn sẵn có.')


FIGS56 = {'5-6-masks': masks56, '5-6-area': area56, '5-6-mask-metrics': maskmetrics56, '5-6-aggregate': aggregate56,
          '5-6-unet': unet56, '5-6-rects': rects56, '5-6-rle': rle56, '5-6-resize': resize56}

# ───────────────────────────── 5.7 ─────────────────────────────

_T57 = {}


def run57():
    """Chạy code bài 5.7 tới linear probe (khoảng 20 giây trên CPU); trả không gian tên."""
    if not _T57:
        _T57['ns'] = lesson_ns('5.7', upto=7)
    return _T57['ns']


def pairs57():
    from PIL import Image, ImageEnhance
    from sklearn.datasets import load_sample_image
    srcs = [Image.fromarray(load_sample_image('china.jpg')), Image.fromarray(load_sample_image('flower.jpg'))]
    views = [
        [srcs[0].crop((40, 20, 400, 380)), ImageEnhance.Color(srcs[0].crop((150, 120, 360, 330)).rotate(-12, fillcolor=(0, 0, 0))).enhance(.3)],
        [srcs[1].crop((120, 30, 480, 390)), ImageEnhance.Brightness(srcs[1].crop((200, 80, 420, 300)).transpose(Image.FLIP_LEFT_RIGHT)).enhance(1.35)],
    ]
    s = Fig(640, 280)
    w = 100
    for r, (a_, b_) in enumerate(views):
        y = 34 + r * 130
        s.photo(40, y, w, w, np.asarray(a_.resize((200, 200))), max_px=200, radius=6)
        s.photo(200, y, w, w, np.asarray(b_.resize((200, 200))), max_px=200, radius=6)
        s.line(144, y + w / 2, 196, y + w / 2, GREEN, 2.2)
        s.label(170, y + w / 2 - 9, 'positive', 11.5, color=GREEN, weight=600)
    s.line(250, 138, 90, 160, CLAY, 1.4, '4 3')
    s.label(170, 140, 'negative', 11.5, color=CLAY, weight=600)
    s.label(350, 96, 'positive: hai view của một ảnh', 12, 'start', GREEN)
    s.label(350, 116, 'crop, xoay, đổi màu, lật, đổi sáng', 11.5, 'start', MUTED)
    s.label(350, 170, 'negative: view của ảnh khác', 12, 'start', CLAY)
    s.label(350, 190, 'trong cùng batch', 11.5, 'start', MUTED)
    s.save('5-7-pairs', 'Hai view của cùng một ảnh là cặp positive; ảnh khác trong batch là negative.')


def matrix57():
    ns = lesson_ns('5.7', upto=2)
    L = ns['logits'].detach().numpy()
    G = ns['logits'].grad.numpy()
    s = Fig(640, 220)
    caps = ['caption 0', 'caption 1', 'caption 2']
    fills = {(i, j): (GREEN if i == j else BLUE, .3 if i == j else .08) for i in range(3) for j in range(3)}
    s.tiles(110, 44, [[mnum(v, '{:g}') for v in r] for r in L], 62, 34, BLUE, 6, fills, size=12.5)
    for j, c_ in enumerate(caps):
        s.label(110 + j * 68 + 31, 32, c_, 11, color=MUTED)
    for i in range(3):
        s.label(100, 44 + i * 40 + 17, f'ảnh {i}', 11.5, 'end', MUTED)
    s.label(208, 178, 'logits', 12, color=TEXT, weight=600)
    gf = {(i, j): ((GREEN, .3) if G[i, j] < 0 else (CLAY, .2)) for i in range(3) for j in range(3)}
    s.tiles(380, 44, [[mnum(v, '{:+.3f}') for v in r] for r in G], 72, 34, BLUE, 6, gf, size=11.5)
    s.label(490, 178, 'gradient của loss đối xứng', 12, color=TEXT, weight=600)
    s.label(490, 200, 'âm trên đường chéo: tăng; dương ngoài: giảm', 11.5, color=MUTED)
    s.save('5-7-matrix', 'Gradient kéo ô đường chéo lên, đẩy các ô khác xuống.')


def tau57():
    ns = lesson_ns('5.7', upto=3)
    import torch
    row = ns['row_scores']
    s = Fig(640, 210)
    W, x0 = 400, 150
    for r, tau in enumerate([1.0, 0.5, 0.1]):
        p = (row / tau).softmax(0)
        push = (p[1:] / tau).numpy()
        share = push / push.sum()
        y = 36 + r * 50
        s.label(x0 - 12, y + 15, f'τ = {tau:g}', 12.5, 'end', TEXT)
        x = x0
        for k, v in enumerate(share):
            w = W * v
            s.rect(x, y, max(w - 1.5, .5), 30, 'none', CLAY if k == 0 else BLUE, 2, .65 if k == 0 else .2, 0)
            x += w
        s.mono(x0 + W + 10, y + 15, f'{share[0]:.3f}', 12, 'start', CLAY)
    s.label(x0, 22, 'negative khó (cosine 0.7)', 11.5, 'start', CLAY)
    s.label(x0 + W, 22, 'sáu negative dễ (cosine 0)', 11.5, 'end', BLUE)
    s.label(350, 196, 'phần lực đẩy của loss dồn vào từng negative', 11.5, color=MUTED)
    s.save('5-7-tau', 'Temperature càng nhỏ, lực đẩy càng dồn vào negative khó.')


def chance57():
    s = Fig(640, 220)
    ax = s.axes(80, 20, 400, 160, (np.log2(16), np.log2(2048)), (0, 8), xticks=[4, 6, 8, 10], xfmt='', yticks=[0, 2, 4, 6, 8],
                xlabel='số ứng viên K', grid=False)
    for e in (4, 6, 8, 10):
        s.label(ax.X(e), ax.y + ax.h + 14, str(2 ** e), 11, color=FAINT)
    k = np.linspace(4, 11, 100)
    ax.line(k, np.log(2 ** k), FAINT, 2)
    s.label(ax.X(11) + 8, ax.Y(np.log(2048)), 'log K', 12, 'start', MUTED)
    for K, L, nm, col in [(1024, 2.9, 'A', BLUE), (64, 2.1, 'B', CLAY)]:
        x = ax.X(np.log2(K))
        s.line(x, ax.Y(L), x, ax.Y(np.log(K)), col, 1.4, '3 3')
        s.circle(x, ax.Y(L), 5, col, col, 0)
        s.mono(x + 9, ax.Y(L) + 16, f'{nm}: {L}', 12, 'start', col, 600)
        s.mono(x + 9, ax.Y((L + np.log(K)) / 2) + 4, f'cách mốc {np.log(K) - L:.2f}', 11, 'start', col)
    s.label(ax.x - 8, ax.y - 10, 'loss', 11.5, 'start', FAINT)
    s.save('5-7-chance', 'Mốc đoán mò log K phụ thuộc batch, nên loss của hai batch khác nhau không so được.')


def shapes57():
    ns = lesson_ns('5.7', upto=5)
    import torch
    X, y = ns['train_images'], ns['train_labels']
    gen = torch.Generator().manual_seed(1)
    v1 = ns['augment'](X[:6], gen)
    v2 = ns['augment'](X[:6], gen)
    s = Fig(640, 270)
    w = 66
    names = ['tròn', 'tam giác', 'chữ nhật']
    for k in range(6):
        x = 112 + k * 86
        for r, img in enumerate([X[k, 0], v1[k, 0], v2[k, 0]]):
            a = np.clip(img.numpy(), 0, 1)
            s.photo(x, 24 + r * 76, w, w, blocky(rgb(a), 132), max_px=132, radius=3)
        s.label(x + w / 2, 256, names[y[k]], 11.5, color=MUTED)
    for r, lab in enumerate(['ảnh', 'view 1', 'view 2']):
        s.label(100, 24 + r * 76 + w / 2, lab, 12, 'end', MUTED)
    s.save('5-7-shapes', 'Sáu ảnh hình học và hai view của mỗi ảnh; hình giữ nguyên qua mọi view.')


def probe57():
    rows = [l.split() for l in output_block('5.7', 5).strip().splitlines()[1:]]
    data = [(' '.join(r[:-2]), float(r[-2]), float(r[-1])) for r in rows]
    names = {'pixels': 'pixel thô', 'random encoder': 'encoder chưa train', 'contrastive': 'sau contrastive'}
    s = Fig(640, 220)
    for r, (nm, f1, nb) in enumerate(data):
        y = 34 + r * 54
        s.label(150, y + 18, names[nm], 12.5, 'end', TEXT, 600 if r == 2 else 400)
        s.rect(160, y, f1 * 300, 18, 'none', BLUE, 3, .6, 0)
        s.rect(160, y + 20, nb * 300, 18, 'none', CLAY, 3, .5, 0)
        s.mono(160 + f1 * 300 + 8, y + 9, f'{f1:.3f}', 11.5, 'start', BLUE)
        s.mono(160 + nb * 300 + 8, y + 29, f'{nb:.3f}', 11.5, 'start', CLAY)
    s.box(520, 60, 12, 12, 'none', BLUE, r=2, width=0, opacity=.6)
    s.label(538, 66, 'probe F1', 11.5, 'start', MUTED)
    s.box(520, 84, 12, 12, 'none', CLAY, r=2, width=0, opacity=.5)
    s.label(538, 90, 'cùng hình @5', 11.5, 'start', MUTED)
    s.label(320, 206, 'cùng probe, 200 ảnh có nhãn; nhãn không dùng khi train contrastive', 11.5, color=MUTED)
    s.save('5-7-probe', 'Linear probe: pixel thô 0.536, encoder chưa train 0.764, sau contrastive 0.968.')


def neighbors57():
    import torch
    import torch.nn.functional as F_
    ns = run57()
    tl = ns['test_labels']
    rates = {}
    for nm, (_, b) in ns['feature_sets'].items():
        u = F_.normalize(torch.tensor(b), dim=1)
        sc = u @ u.T
        sc.fill_diagonal_(float('-inf'))
        nb = sc.topk(5, dim=1).indices.numpy()
        same = (tl[nb] == tl[:, None]).mean(1)
        rates[nm] = [float(same[tl == c].mean()) for c in range(3)]
    s = Fig(640, 230)
    ax = s.axes(80, 26, 420, 150, (0, 3), (0, 1), xticks=[], yticks=[0, .5, 1], grid=False)
    cols = {'pixels': FAINT, 'random encoder': BLUE, 'contrastive': CLAY}
    labs = {'pixels': 'pixel thô', 'random encoder': 'encoder chưa train', 'contrastive': 'contrastive'}
    for c, cls in enumerate(['tròn', 'tam giác', 'chữ nhật']):
        for k, nm in enumerate(rates):
            v = rates[nm][c]
            x = ax.X(c + .5) - 48 + k * 33
            s.rect(x, ax.Y(v), 30, ax.Y(0) - ax.Y(v), 'none', cols[nm], 3, .6 if nm != 'pixels' else .35, 0)
            s.mono(x + 15, ax.Y(v) - 7, f'{v:.2f}'.lstrip('0'), 10.5, 'middle', TEXT)
        s.label(ax.X(c + .5), ax.y + ax.h + 16, cls, 12, color=TEXT)
    for k, nm in enumerate(rates):
        s.box(520, 50 + k * 24, 12, 12, 'none', cols[nm], r=2, width=0, opacity=.6)
        s.label(538, 56 + k * 24, labs[nm], 11.5, 'start', MUTED)
    s.label(ax.x - 8, ax.y - 12, 'cùng hình trong 5 láng giềng', 11.5, 'start', FAINT)
    s.save('5-7-neighbors', 'Tỉ lệ láng giềng cùng hình: contrastive cao nhất ở cả ba lớp.')


def recall57():
    ranks = [1, 3, 7, 2]
    s = Fig(640, 210)
    ax = s.axes(80, 26, 360, 140, (.5, 8.5), (0, 1.05), xticks=[1, 2, 3, 4, 5, 6, 7, 8], yticks=[0, .25, .5, .75, 1], xlabel='k')
    ks = np.arange(1, 9)
    rec = [np.mean([r <= k for r in ranks]) for k in ks]
    ax.step(np.r_[.5, ks + .5], np.r_[rec[0], rec], CLAY, 2.2)
    for k in (1, 5):
        s.circle(ax.X(k), ax.Y(rec[k - 1]), 4.5, CLAY, PAPER, 2)
        s.mono(ax.X(k), ax.Y(rec[k - 1]) - 10, f'{rec[k - 1]:.2f}', 11.5, 'middle', CLAY)
    s.label(ax.x - 8, ax.y - 12, 'recall@k', 11.5, 'start', FAINT)
    s.label(470, 70, 'hạng ảnh đúng của 4 query', 12, 'start', MUTED)
    s.mono(470, 96, '1, 3, 7, 2', 13, 'start', TEXT)
    s.save('5-7-recall', 'Ảnh đúng ở hạng 1, 3, 7, 2: recall@1 = 0.25, recall@5 = 0.75.')


FIGS57 = {'5-7-pairs': pairs57, '5-7-matrix': matrix57, '5-7-tau': tau57, '5-7-chance': chance57, '5-7-shapes': shapes57,
          '5-7-probe': probe57, '5-7-neighbors': neighbors57, '5-7-recall': recall57}

# ───────────────────────────── 5.8 ─────────────────────────────


def gan58():
    s = Fig(640, 230)

    def node(x, y, w, txt, col, op=.2):
        s.box(x, y, w, 36, 'none', col, r=8, width=0, opacity=op)
        s.label(x + w / 2, y + 18, txt, 12.5, color=TEXT, weight=600)
    s.mono(40, 82, 'z', 14, 'middle', TEXT)
    node(70, 64, 80, 'G', CLAY, .28)
    s.arrow(54, 82, 66, 82, LINE, 1.2)
    s.arrow(152, 82, 196, 82, LINE, 1.2)
    s.label(240, 82, 'ảnh giả', 12, color=TEXT)
    s.arrow(284, 82, 346, 106, LINE, 1.2)
    s.label(240, 150, 'ảnh thật', 12, color=TEXT)
    s.arrow(284, 150, 346, 126, LINE, 1.2)
    node(350, 98, 80, 'D', BLUE, .22)
    s.arrow(432, 116, 470, 116, LINE, 1.2)
    s.mono(476, 116.5, 'thật / giả', 12, 'start', MUTED)
    s.path('M 390,96 L 390,44 L 110,44', CLAY, 1.6, dash='4 3')
    s.arrow(110, 44, 110, 60, CLAY, 1.6)
    s.label(250, 30, 'bước G: gradient đi qua D (D đóng băng) về G', 11.5, color=CLAY)
    s.label(320, 200, 'bước D: detach ảnh giả, chỉ cập nhật D', 11.5, color=BLUE)
    s.save('5-8-gan', 'D học phân biệt ảnh thật với ảnh giả; G học qua gradient đi xuyên D.')


def saturate58():
    s = Fig(640, 230)
    ax = s.axes(80, 24, 380, 160, (0, 1), (0, 1), xticks=[0, .25, .5, .75, 1], yticks=[0, .5, 1], xlabel='D(G(z)) = σ(a)')
    p = np.linspace(0, 1, 101)
    ax.line(p, p, BLUE, 2.2).line(p, 1 - p, CLAY, 2.2)
    s.label(ax.X(1) + 8, ax.Y(1), 'minimax: σ(a)', 12, 'start', BLUE, 600)
    s.label(ax.X(1) + 8, ax.Y(0), 'non-saturating: 1 − σ(a)', 12, 'start', CLAY, 600)
    s.circle(ax.X(.01), ax.Y(.01), 4.5, BLUE, PAPER, 2)
    s.circle(ax.X(.01), ax.Y(.99), 4.5, CLAY, PAPER, 2)
    s.label(ax.X(1) + 8, ax.Y(.62), 'tại D(G(z)) = 0.01:', 11.5, 'start', MUTED)
    s.mono(ax.X(1) + 8, ax.Y(.5), 'minimax 0.01', 11.5, 'start', BLUE)
    s.mono(ax.X(1) + 8, ax.Y(.38), 'non-saturating 0.99', 11.5, 'start', CLAY)
    s.label(ax.x - 8, ax.y - 10, '|gradient theo logit a|', 11.5, 'start', FAINT)
    s.save('5-8-saturate', 'Khi D bắt được ảnh giả, loss minimax gần như hết gradient; non-saturating thì không.')


def schedule58():
    import torch
    steps = 40
    betas = torch.linspace(0.01, 0.15, steps)
    return torch.cumprod(1 - betas, dim=0).numpy().astype(float)


def diffusion58():
    ab = schedule58()
    g = gray('china.jpg', (40, 20, 400, 380), 160) * 2 - 1
    rng = np.random.default_rng(5)
    eps = rng.standard_normal(g.shape)
    s = Fig(640, 200)
    ts = [None, 2, 6, 12, 20, 39]
    w = 92
    for k, t in enumerate(ts):
        x = 20 + k * 102
        if t is None:
            img, lab, sub = g, 'x₀', 'ảnh sạch'
        else:
            img = np.sqrt(ab[t]) * g + np.sqrt(1 - ab[t]) * eps
            lab, sub = f't = {t}', f'ᾱ = {ab[t]:.2f}'
        s.photo(x, 30, w, w, rgb((np.clip(img, -2, 2) + 2) / 4 if t is not None else (img + 1) / 2), max_px=184, radius=4)
        s.mono(x + w / 2, 20, lab, 11.5, 'middle', TEXT)
        s.mono(x + w / 2, 138, sub, 11, 'middle', MUTED)
    s.arrow(40, 162, 600, 162, CLAY, 1.4)
    s.label(320, 180, 'forward: thêm nhiễu theo lịch β của bài; sinh ảnh là học đi ngược chiều này', 11.5, color=MUTED)
    s.save('5-8-diffusion', 'Thêm nhiễu dần qua 40 mức, đến cuối ảnh gần như chỉ còn nhiễu.')


def alphabar58():
    ab = schedule58()
    s = Fig(640, 220)
    ax = s.axes(80, 24, 400, 150, (0, 39), (0, 1), xticks=[0, 10, 20, 30, 39], yticks=[0, .5, 1], xlabel='mức nhiễu t')
    t = np.arange(40)
    ax.line(t, np.sqrt(ab), BLUE, 2.2).line(t, np.sqrt(1 - ab), CLAY, 2.2)
    s.label(ax.X(39) + 8, ax.Y(np.sqrt(ab[-1])), '√ᾱ: tín hiệu', 12, 'start', BLUE, 600)
    s.label(ax.X(39) + 8, ax.Y(np.sqrt(1 - ab[-1])), '√(1 − ᾱ): nhiễu', 12, 'start', CLAY, 600)
    s.mono(ax.X(39) - 4, ax.Y(np.sqrt(ab[-1])) - 10, f'{np.sqrt(ab[-1]):.2f}', 11, 'end', BLUE)
    s.label(ax.x - 8, ax.y - 10, 'hệ số trong x_t', 11.5, 'start', FAINT)
    s.save('5-8-alphabar', 'Hệ số tín hiệu giảm dần, hệ số nhiễu tăng dần theo mức nhiễu.')


def hist58():
    import torch
    ab = schedule58()
    rng = np.random.default_rng(0)
    x0 = rng.integers(0, 2, 20000) * 4 - 2 + .2 * rng.standard_normal(20000)
    eps = rng.standard_normal(20000)
    s = Fig(640, 200)
    bins = np.linspace(-4, 4, 61)
    for k, t in enumerate([None, 8, 20, 39]):
        x = 30 + k * 152
        xt = x0 if t is None else np.sqrt(ab[t]) * x0 + np.sqrt(1 - ab[t]) * eps
        h, _ = np.histogram(xt, bins)
        h = h / h.max()
        ax = s.axes(x, 40, 130, 100, (-4, 4), (0, 1.05), xticks=[-2, 0, 2], yticks=[], grid=False)
        for i in range(60):
            s.rect(ax.X(bins[i]), ax.Y(h[i]), ax.X(bins[i + 1]) - ax.X(bins[i]) - .3, ax.Y(0) - ax.Y(h[i]), 'none',
                   CLAY if t is None else BLUE, 0, .55, 0)
        s.mono(x + 65, 26, 'x₀' if t is None else f't = {t}', 12, 'middle', TEXT)
    s.label(320, 192, 'hai cụm quanh ±2 nhòe dần thành một phân phối chuẩn', 11.5, color=MUTED)
    s.save('5-8-hist', 'Hai cụm dữ liệu nhòe dần thành một phân phối chuẩn.')


def mse58():
    import torch
    ns = lesson_ns('5.8', upto=5)
    den, ab_t = ns['denoiser'], ns['alpha_bars']
    torch.manual_seed(1)
    n = 4000
    out = []
    for t in range(40):
        clean = (torch.randint(0, 2, (n, 1)) * 4 - 2).float() + .2 * torch.randn(n, 1)
        eps = torch.randn(n, 1)
        kept = ab_t[t]
        noisy = kept.sqrt() * clean + (1 - kept).sqrt() * eps
        inp = torch.cat([noisy, torch.full((n, 1), t / 39)], 1)
        with torch.no_grad():
            out.append(torch.nn.functional.mse_loss(den(inp), eps).item())
    out = np.array(out)
    s = Fig(640, 220)
    ax = s.axes(80, 24, 400, 150, (0, 39), (0, 1.1), xticks=[0, 10, 20, 30, 39], yticks=[0, .5, 1], xlabel='mức nhiễu t')
    ax.hline(1, FAINT, 1, '4 4')
    ax.line(np.arange(40), out, CLAY, 2.2)
    s.label(ax.X(39) + 8, ax.Y(1), 'luôn đoán 0', 11.5, 'start', MUTED)
    s.label(ax.X(39) + 8, ax.Y(out[-1]), 'denoiser đã train', 12, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 10, 'MSE trên noise', 11.5, 'start', FAINT)
    s.save('5-8-mse', 'Sai số đoán nhiễu theo từng mức: khó ở mức thấp và mức giữa, dễ ở mức cao.')


def cfg58():
    s = Fig(640, 230)
    O = (90, 190)
    u = (120, -50)
    c = (150, -95)
    s.arrow(*O, O[0] + u[0], O[1] + u[1], BLUE, 2)
    s.label(O[0] + u[0] + 8, O[1] + u[1] + 12, 'không prompt', 11.5, 'start', BLUE, 600)
    s.arrow(*O, O[0] + c[0], O[1] + c[1], GREEN, 2)
    s.label(O[0] + c[0] + 18, O[1] + c[1] + 16, 'có prompt (w = 1)', 11.5, 'start', GREEN, 600)
    w = 2
    e = (u[0] + w * (c[0] - u[0]), u[1] + w * (c[1] - u[1]))
    s.line(O[0] + u[0], O[1] + u[1], O[0] + e[0], O[1] + e[1], FAINT, 1.2, '4 3')
    s.arrow(*O, O[0] + e[0], O[1] + e[1], CLAY, 2.2)
    s.label(O[0] + e[0] + 8, O[1] + e[1] + 4, f'w = {w:g}', 12, 'start', CLAY, 600)
    s.mono(440, 120, 'ε̂ = ε∅ + w (ε_c − ε∅)', 12.5, 'start', TEXT)
    s.label(440, 150, 'w lớn: bám prompt hơn,', 12, 'start', MUTED)
    s.label(440, 170, 'kém đa dạng, tốn gấp đôi', 12, 'start', MUTED)
    s.save('5-8-cfg', 'Guidance đi tiếp w lần theo hướng từ dự đoán không prompt sang có prompt.')


def latent58():
    s = Fig(640, 210)
    s.box(40, 30, 150, 150, 'none', BLUE, r=6, width=0, opacity=.16)
    s.mono(115, 105, '512×512×3', 12.5, 'middle', TEXT)
    s.mono(115, 196, '786 432 số', 12, 'middle', MUTED)
    s.arrow(206, 105, 256, 105, LINE, 1.3)
    s.label(231, 92, 'encoder', 11, color=MUTED)
    s.box(270, 86, 19, 19, 'none', CLAY, r=3, width=0, opacity=.35)
    s.box(274, 82, 19, 19, 'none', CLAY, r=3, width=0, opacity=.3)
    s.box(278, 78, 19, 19, 'none', CLAY, r=3, width=0, opacity=.25)
    s.box(282, 74, 19, 19, 'none', CLAY, r=3, width=0, opacity=.2)
    s.mono(286, 130, '64×64×4', 12.5, 'middle', TEXT)
    s.mono(286, 196, '16 384 số', 12, 'middle', MUTED)
    s.label(470, 90, 'mỗi lần gọi denoiser', 12, color=MUTED)
    s.mono(470, 118, 'ít hơn 48 lần', 14, 'middle', CLAY, 600)
    s.save('5-8-latent', 'Khử nhiễu trên latent ít hơn 48 lần số so với ảnh gốc.')


FIGS58 = {'5-8-gan': gan58, '5-8-saturate': saturate58, '5-8-diffusion': diffusion58, '5-8-alphabar': alphabar58,
          '5-8-hist': hist58, '5-8-mse': mse58, '5-8-cfg': cfg58, '5-8-latent': latent58}

# ───────────────────────────── 5.9 ─────────────────────────────


def pix8(s, x, y, img, c=10, col=TEXT):
    """Ảnh 8×8 giá trị 0..1 vẽ bằng ô xám (nền sáng, nét đậm)."""
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            v = float(np.clip(img[i, j], 0, 1))
            if v > .04:
                s.rect(x + j * c, y + i * c, c + .2, c + .2, 'none', col, 0, min(.95, v), 0)
    s.box(x, y, img.shape[1] * c, img.shape[0] * c, SOFT_LINE, 'none', r=2, width=.8)


def heat8(s, x, y, m, c=10, col=CLAY):
    mx = float(np.max(np.abs(m))) or 1
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            v = abs(float(m[i, j])) / mx
            if v > .02:
                s.rect(x + j * c, y + i * c, c + .2, c + .2, 'none', col, 0, .1 + .8 * v, 0)
    s.box(x, y, m.shape[1] * c, m.shape[0] * c, SOFT_LINE, 'none', r=2, width=.8)


def crosstab59():
    s = Fig(640, 210)
    cells = [['84', '6'], ['6', '4']]
    fills = {(0, 0): (GREEN, .25), (0, 1): (SAND, .35), (1, 0): (SAND, .35), (1, 1): (CLAY, .3)}
    s.tiles(250, 50, cells, 90, 50, BLUE, 6, fills, size=16)
    s.label(295, 36, 'B đúng', 12, color=MUTED)
    s.label(391, 36, 'B sai', 12, color=MUTED)
    s.label(240, 75, 'A đúng', 12, 'end', MUTED)
    s.label(240, 131, 'A sai', 12, 'end', MUTED)
    s.label(500, 92, 'hai ô giữa phân biệt', 12, 'start', SAND)
    s.label(500, 110, 'hai model', 12, 'start', SAND)
    s.label(500, 140, 'ô cả hai sai: xem ảnh', 12, 'start', CLAY)
    s.label(500, 158, 'trước', 12, 'start', CLAY)
    s.label(343, 190, 'A và B cùng đúng 90 trên 100 ảnh', 11.5, color=MUTED)
    s.save('5-9-crosstab', 'A và B cùng đúng 90 ảnh, nhưng mỗi model đúng riêng 6 ảnh.')


def shortcut59():
    ns = lesson_ns('5.9', upto=1)
    N, C = ns['normal_images'], ns['changed_images']
    s = Fig(640, 230)
    c = 11
    for r, (imgs, title) in enumerate([(N, 'nguồn: góc sáng đi với nét ngang'), (C, 'đổi góc: nhãn giữ nguyên')]):
        x0 = 40 + r * 300
        s.label(x0 + 120, 22, title, 12, color=TEXT, weight=600)
        for k, i in enumerate([0, 1]):
            x = x0 + k * 130
            pix8(s, x + 20, 40, imgs[i], c)
            s.box(x + 20 - 2, 40 - 2, 2 * c + 4, 2 * c + 4, CLAY, 'none', r=2, width=1.6)
            s.label(x + 20 + 4 * c, 40 + 8 * c + 18, 'đứng' if i == 0 else 'ngang', 12, color=MUTED)
    s.label(320, 196, 'khung cam: ô góc 2×2 mà model A đọc; model B chỉ đọc vùng nét ở giữa', 11.5, color=MUTED)
    s.save('5-9-shortcut', 'Ở tập nguồn, ô góc sáng luôn đi với nét ngang; tập kiểm đảo ô góc.')


def filter59():
    ns = lesson_ns('5.9', upto=1)
    Fm = ns['orientation_filter']
    s = Fig(640, 220)
    vals = [[('+¼' if v > 0 else '−¼' if v < 0 else '') for v in row] for row in Fm]
    fills = {(i, j): ((CLAY, .35) if Fm[i, j] > 0 else (BLUE, .3) if Fm[i, j] < 0 else (FAINT, .06)) for i in range(8) for j in range(8)}
    s.tiles(200, 20, vals, 20, 20, FAINT, 2, fills, size=9.5, r=2)
    s.label(186, 108, '(H − V)/4', 12.5, 'end', TEXT, 600)
    s.label(400, 70, '+¼: chỉ thuộc nét ngang', 12, 'start', CLAY)
    s.label(400, 94, '−¼: chỉ thuộc nét đứng', 12, 'start', BLUE)
    s.label(400, 130, 'ngang sạch: score +1', 12, 'start', TEXT)
    s.label(400, 150, 'đứng sạch: score −1', 12, 'start', TEXT)
    s.label(400, 170, 'ô góc nằm ngoài filter', 12, 'start', MUTED)
    s.save('5-9-filter', 'Filter của model B chỉ có trọng số trên vùng nét, không có ở ô góc.')


def occscores59():
    ns = lesson_ns('5.9', upto=3)
    a, b = ns['score_a'], ns['score_b']
    s = Fig(640, 220)
    labs = ['ảnh gốc', 'che góc', 'che nét']
    for k, lab in enumerate(labs):
        y = 34 + k * 50
        s.label(130, y + 18, lab, 12.5, 'end', TEXT)
        for j, (v, col) in enumerate([(a[k], BLUE), (b[k], CLAY)]):
            yy = y + j * 19
            s.rect(140, yy, v * 360, 16, 'none', col, 3, .6, 0)
            s.mono(140 + v * 360 + 8, yy + 8, f'{v:.4f}', 11, 'start', col)
    s.line(140 + .5 * 360, 28, 140 + .5 * 360, 186, FAINT, 1, '3 3')
    s.box(560, 60, 12, 12, 'none', BLUE, r=2, width=0, opacity=.6)
    s.label(578, 66, 'A', 12, 'start', MUTED)
    s.box(560, 84, 12, 12, 'none', CLAY, r=2, width=0, opacity=.6)
    s.label(578, 90, 'B', 12, 'start', MUTED)
    s.label(320, 206, 'xác suất lớp 1 (ngang) trước và sau khi che', 11.5, color=MUTED)
    s.save('5-9-occlusion-scores', 'Che góc làm A đổi hẳn dự đoán; che nét làm B đổi dự đoán.')


def occmap59():
    ns = lesson_ns('5.9', upto=3)
    ex = ns['example']
    feats, ma, mb = ns['features'], ns['model_a'], ns['model_b']
    pos = [(i, j) for i in range(7) for j in range(7)]
    batch = []
    for i, j in pos:
        e = ex.copy()
        e[i:i + 2, j:j + 2] = 0
        batch.append(e)
    batch = np.stack(batch)
    corner, shape = feats(np.stack([ex]))
    base_a, base_b = ma.predict_proba(corner)[0, 1], mb.predict_proba(shape)[0, 1]
    corner, shape = feats(batch)
    da = (base_a - ma.predict_proba(corner)[:, 1]).reshape(7, 7)
    db = (base_b - mb.predict_proba(shape)[:, 1]).reshape(7, 7)
    s = Fig(640, 230)
    c = 16
    pix8(s, 60, 40, ex, c)
    s.label(124, 26, 'ảnh ngang', 12, color=MUTED)
    for k, (d, nm) in enumerate([(da, 'model A'), (db, 'model B')]):
        x = 260 + k * 190
        heat8(s, x, 48, np.clip(d, 0, None), c, CLAY)
        s.label(x + 56, 26, nm, 12, color=TEXT, weight=600)
        s.mono(x + 56, 180, f'giảm tối đa {d.max():.2f}', 11, 'middle', MUTED)
    s.label(320, 214, 'mỗi ô: score lớp 1 giảm bao nhiêu khi che cửa sổ 2×2 bắt đầu ở đó', 11.5, color=MUTED)
    s.save('5-9-occmap', 'Bản đồ occlusion: A chỉ nhạy với ô góc, B nhạy với vùng nét.')


def saliency59():
    ns = lesson_ns('5.9', upto=4)
    sal = ns['saliency']
    N = ns['normal_images']
    s = Fig(640, 220)
    c = 14
    for k, (nm, col) in enumerate([('A', BLUE), ('B', CLAY)]):
        for r, i in enumerate([1, 0]):
            x = 80 + k * 280 + r * 130
            m = sal(nm, N[i])
            heat8(s, x, 44, m, c, col)
            s.label(x + 56, 172, 'ảnh ngang' if i == 1 else 'ảnh đứng', 11.5, color=MUTED)
        s.label(80 + k * 280 + 121, 26, f'saliency của {nm}', 12.5, color=TEXT, weight=600)
    s.label(320, 204, 'model tuyến tính: gradient chính là trọng số, giống nhau trên mọi ảnh', 11.5, color=MUTED)
    s.save('5-9-saliency', 'Saliency: A dồn vào ô góc, B dồn vào vùng nét.')


def gradcam59():
    s = Fig(640, 220)
    A1 = [['1', '0'], ['2', '1']]
    A2 = [['0', '3'], ['1', '0']]
    M = [['0.5', '0'], ['0.5', '0.5']]
    s.tiles(40, 60, A1, 40, 34, BLUE, 4, size=13, opacity=.18)
    s.label(84, 44, 'A¹ · α₁ = 0.5', 12, color=TEXT, weight=600)
    s.tiles(190, 60, A2, 40, 34, CLAY, 4, size=13, opacity=.2)
    s.label(234, 44, 'A² · α₂ = −0.5', 12, color=TEXT, weight=600)
    s.arrow(296, 94, 336, 94, LINE, 1.2)
    s.mono(316, 82, 'ReLU', 10.5, 'middle', MUTED)
    s.tiles(350, 60, M, 50, 34, GREEN, 4, {(0, 1): (FAINT, .08)}, size=13, opacity=.28)
    s.label(404, 44, 'M_c', 12, color=TEXT, weight=600)
    s.mono(40, 160, 'α = trung bình gradient theo không gian', 12, 'start', MUTED)
    s.mono(40, 184, '0.5·A¹ − 0.5·A² = (0.5, −1.5; 0.5, 0.5) → ReLU', 12, 'start', MUTED)
    s.save('5-9-gradcam', 'Grad-CAM tính tay: ô góc trên phải ra −1.5, ReLU đưa về 0.')


def matrix59():
    rows = [l.split() for l in output_block('5.9', 4).strip().splitlines()[1:]]
    data = [(' '.join(r[:-2]), float(r[-2]), float(r[-1])) for r in rows]
    s = Fig(640, 230)
    for r, (nm, a, b) in enumerate(data):
        y = 40 + r * 40
        s.label(200, y + 17, nm, 12.5, 'end', TEXT)
        for j, v in enumerate((a, b)):
            col = GREEN if v >= .95 else (CLAY if v <= .55 else SAND)
            s.box(220 + j * 110, y, 100, 34, 'none', col, r=6, width=0, opacity=.3)
            s.mono(270 + j * 110, y + 17.5, f'{v:.3f}', 12.5, 'middle', TEXT)
    s.label(270, 24, 'A (đọc góc)', 12, color=MUTED)
    s.label(380, 24, 'B (đọc nét)', 12, color=MUTED)
    s.label(480, 90, 'mỗi model thắng', 12, 'start', MUTED)
    s.label(480, 110, 'ở một hàng khác', 12, 'start', MUTED)
    s.save('5-9-matrix', 'A sụp khi đổi ô góc; B giữ được nhưng tụt khi nét dịch chỗ.')


def baseline59():
    from sklearn.datasets import load_sample_image
    im = np.asarray(sample('china.jpg', (40, 20, 400, 380), 240)).copy()
    mean = np.array([0.485, 0.456, 0.406])
    a = im.copy()
    a[80:160, 70:170] = 0
    b = im.copy()
    b[80:160, 70:170] = (mean * 255).astype('uint8')
    s = Fig(640, 230)
    w = 170
    for k, (img, lab) in enumerate([(a, 'gán 0 trước Normalize'), (b, 'gán 0 sau Normalize')]):
        x = 60 + k * 210
        s.photo(x, 30, w, w, img, max_px=340, radius=5)
        s.label(x + w / 2, 18, lab, 12, color=TEXT, weight=600)
    s.label(460, 90, 'sau Normalize, 0 ứng với', 12, 'start', MUTED)
    s.label(460, 110, 'mean ImageNet:', 12, 'start', MUTED)
    s.mono(460, 134, '(124, 116, 104)', 12, 'start', CLAY)
    s.label(460, 160, 'che đen phải gán ≈ −2.1', 12, 'start', MUTED)
    s.label(460, 178, 'ở kênh R', 12, 'start', MUTED)
    s.save('5-9-baseline', 'Gán 0 trước Normalize cho ô đen; gán 0 sau Normalize cho ô màu trung bình.')


FIGS59 = {'5-9-crosstab': crosstab59, '5-9-shortcut': shortcut59, '5-9-filter': filter59, '5-9-occlusion-scores': occscores59,
          '5-9-occmap': occmap59, '5-9-saliency': saliency59, '5-9-gradcam': gradcam59, '5-9-matrix': matrix59,
          '5-9-baseline': baseline59}

# ───────────────────────────── kt3 ─────────────────────────────


def contractkt3():
    F_ = flower_masks()
    im, inst = F_['im'], F_['inst']
    m = inst == 1
    ys, xs = np.nonzero(m)
    x1, x2, y1, y2 = xs.min(), xs.max(), ys.min(), ys.max()
    H, W = im.shape[:2]
    s = Fig(640, 220)
    w, h = 132, 88
    sc = w / W
    titles = ['phân loại', 'phát hiện', 'phân đoạn', 'truy xuất']
    outs = ['nhãn: hoa', 'lớp, box, score', 'mask / RLE', 'thứ hạng ảnh']
    for k in range(4):
        x = 24 + k * 152
        s.label(x + w / 2, 22, titles[k], 12.5, color=TEXT, weight=600)
        s.label(x + w / 2, 196, outs[k], 12, color=CLAY)
        if k == 0:
            s.photo(x, 40, w, h, im, max_px=300, radius=5)
        elif k == 1:
            s.photo(x, 40, w, h, im, max_px=300, radius=5)
            s.box(x + x1 * sc, 40 + y1 * sc, (x2 - x1) * sc, (y2 - y1) * sc, '#ffd166', 'none', r=1, width=2)
        elif k == 2:
            mk = np.full_like(im, 236)
            mk[inst > 0] = (217, 119, 87)
            s.photo(x, 40, w, h, mk, max_px=300, radius=5)
    from sklearn.datasets import load_sample_image
    x = 24 + 3 * 152
    s.mono(x + w / 2, 52, '“a flower”', 11.5, 'middle', MUTED)
    china = load_sample_image('china.jpg')
    for r, (img, rank) in enumerate([(im, 1), (china, 2)]):
        y = 66 + r * 60
        s.photo(x + 30, y, 80, 52, img, max_px=200, radius=4)
        s.mono(x + 18, y + 26, str(rank), 12, 'middle', TEXT)
    s.save('5-kt3-contract', 'Cùng ảnh thật, bốn dạng đầu ra: phân loại nộp nhãn, phát hiện nộp lớp kèm box và score, phân đoạn nộp mask, truy xuất nộp thứ hạng ảnh cho một câu truy vấn.')


def logloss_kt3():
    s = Fig(640, 210)
    rows = [('nộp one-hot, đúng 90%', 3.45, CLAY), ('đoán đều ba lớp', np.log(3), FAINT), ('nộp xác suất, p đúng ≈ 0.9', -np.log(.9), GREEN)]
    for r, (nm, v, col) in enumerate(rows):
        y = 36 + r * 46
        s.label(210, y + 15, nm, 12.5, 'end', TEXT)
        s.rect(220, y, v / 3.6 * 330, 30, 'none', col, 3, .55, 0)
        s.mono(220 + v / 3.6 * 330 + 8, y + 15, f'{v:.2f}', 12, 'start', col if col != FAINT else MUTED)
    s.label(390, 190, 'log loss, thấp là tốt; mỗi ảnh sai với p = 10⁻¹⁵ góp 34.5', 11.5, color=MUTED)
    s.save('5-kt3-logloss', 'Log loss của câu hỏi: nộp one-hot dù đúng 90% cho khoảng 3.45, tệ hơn cả đoán đều ba lớp (1.10); nộp xác suất với p đúng khoảng 0.9 chỉ khoảng 0.11.')


def budgetkt3():
    s = Fig(640, 170)
    parts = [('train 15 epoch', 180, BLUE), ('test', 20, GREEN), ('nạp lại', 10, SAND), ('dự phòng', 30, CLAY)]
    x = 30
    W = 580
    for k, (nm, mins, col) in enumerate(parts):
        w = W * mins / 240
        s.rect(x, 50, w - 2, 40, 'none', col, 4, .35, 0)
        if k == 0:
            s.label(x + w / 2, 70, nm, 12, color=TEXT)
            s.mono(x + w / 2, 108, f'{mins} phút', 11, 'middle', MUTED)
        else:
            s.mono(x + w / 2, 70.5, str(mins), 11, 'middle', TEXT)
            s.label(x + w / 2, 108 + (k - 1) * 0, nm, 11, color=MUTED) if k != 2 else s.label(x + w / 2, 124, nm, 11, color=MUTED)
        x += w
    s.label(320, 32, '4 giờ = 240 phút', 12, color=TEXT, weight=600)
    s.mono(320, 146, '(240 − 20 − 10 − 30) / 12 = 15 epoch', 12.5, 'middle', CLAY)
    s.save('5-kt3-budget', 'Ngân sách 4 giờ của câu hỏi: trừ 20 phút chạy test, 10 phút nạp lại và kiểm file, 30 phút dự phòng; còn 180 phút cho 15 epoch, mỗi epoch 12 phút.')


def kt_ns(phase, name, upto=None):
    """Như lesson_ns cho bài kiểm tra (tên tệp không chứa số chương)."""
    import re, io, contextlib
    from p8_ch1 import CONTENT
    text = (CONTENT / f'phase-{phase}' / f'{name}.md').read_text(encoding='utf-8')
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for b in re.findall(r'^```python\n(.*?)^```', text, re.M | re.S)[:upto]:
            exec(compile(b, name, 'exec'), ns)
    return ns


def thresholdkt3():
    ns = kt_ns(5, 'kt3', upto=1)
    p, y, bm = ns['probabilities'], ns['labels'], ns['binary_metrics']
    s = Fig(640, 270)
    ax = s.axes(80, 90, 420, 140, (0, 1), (0, 1.05), xticks=[0, .2, .4, .6, .8, 1], yticks=[0, .5, 1], xlabel='threshold')
    for v, lab in zip(p, y):
        s.circle(ax.X(v), 54 if lab else 72, 5, CLAY if lab else FAINT, CLAY if lab else PAPER, 1.6)
    s.label(ax.x - 8, 54, 'dương', 11, 'end', CLAY)
    s.label(ax.x - 8, 72, 'âm', 11, 'end', MUTED)
    ts = np.linspace(0, 1, 401)
    acc = [bm(p >= t, y)[0] for t in ts]
    f1 = [bm(p >= t, y)[1] for t in ts]
    ax.line(ts, acc, BLUE, 2).line(ts, f1, CLAY, 2)
    for t in (.5, .65):
        s.line(ax.X(t), 40, ax.X(t), ax.y + ax.h, FAINT, 1, '3 3')
        s.circle(ax.X(t), ax.Y(bm(p >= t, y)[1]), 4.5, CLAY, PAPER, 2)
        s.mono(ax.X(t), 30, f'{t:g}', 11, 'middle', MUTED)
    s.label(ax.X(1) + 8, ax.Y(acc[-1]), 'accuracy', 12, 'start', BLUE, 600)
    s.label(ax.X(1) + 8, ax.Y(f1[-1]), 'F1', 12, 'start', CLAY, 600)
    s.save('5-kt3-threshold', 'Tám xác suất validation (chấm đặc là ảnh dương) và accuracy, F1 theo threshold, tính từ code bài: tại 0.5 và 0.65 accuracy cùng 0.875 nhưng F1 là 0.857 và 0.8.')


def mergekt3():
    s = Fig(640, 200)
    s.label(110, 26, 'prediction', 12, color=TEXT, weight=600)
    s.tiles(60, 40, [['c', '1'], ['a', '0'], ['b', '1']], 48, 30, BLUE, 4, size=13)
    s.label(320, 26, 'sample', 12, color=TEXT, weight=600)
    s.tiles(296, 40, [['a'], ['b'], ['c']], 48, 30, FAINT, 4, size=13, opacity=.15)
    s.label(530, 26, 'ghép theo ID', 12, color=GREEN, weight=600)
    s.tiles(480, 40, [['a', '0'], ['b', '1'], ['c', '1']], 48, 30, GREEN, 4, size=13)
    for i, j in [(0, 2), (1, 0), (2, 1)]:
        s.curve(162, 55 + i * 34, 290, 55 + j * 34, 0, FAINT, 1.1)
    s.arrow(350, 89, 470, 89, LINE, 1.2)
    s.label(320, 168, 'chép theo vị trí hàng sẽ gán nhãn của c cho a', 11.5, color=CLAY)
    s.save('5-kt3-merge', 'Prediction có thứ tự c, a, b; ghép theo ID với sample a, b, c (số từ code bài) cho đúng nhãn 0, 1, 1; chép theo vị trí hàng sẽ gán nhầm nhãn của c cho a.')


def leaderboardkt3():
    s = Fig(640, 220)
    ax = s.axes(70, 30, 330, 140, (.8, .88), (0, 3), xticks=[.8, .82, .84, .86, .88], xfmt='{:.2f}', yticks=[], grid=False)
    for r, (nm, v, sd, pub, col) in enumerate([('A', .842, .006, .83, BLUE), ('B', .838, .007, .85, CLAY)]):
        y = ax.Y(2 - r)
        s.line(ax.X(v - sd), y, ax.X(v + sd), y, col, 3)
        s.circle(ax.X(v), y, 5, col, col, 0)
        s.line(ax.X(pub - 1 / 60), y + 24, ax.X(pub + 1 / 60), y + 24, col, 1.4, '3 3')
        s.circle(ax.X(pub), y + 24, 4.5, col, PAPER, 1.8)
        s.label(ax.x - 10, y + 12, nm, 13, 'end', col, 600)
    s.line(430, 70, 456, 70, TEXT, 3)
    s.label(464, 70, 'validation 5-fold ± độ lệch fold', 11.5, 'start', MUTED)
    s.line(430, 96, 456, 96, TEXT, 1.4, '3 3')
    s.label(464, 96, 'public 60 ảnh ± một ảnh', 11.5, 'start', MUTED)
    s.save('5-kt3-leaderboard', 'Hai cấu hình của câu hỏi: khoảng dao động validation chồng nhau, và trên 60 ảnh public mỗi ảnh đổi điểm khoảng 0.017, nên chênh 0.02 chỉ cỡ một ảnh: coi như ngang nhau.')


FIGSKT3 = {'5-kt3-contract': contractkt3, '5-kt3-logloss': logloss_kt3, '5-kt3-budget': budgetkt3,
           '5-kt3-threshold': thresholdkt3, '5-kt3-merge': mergekt3, '5-kt3-leaderboard': leaderboardkt3}

FIGS = {**FIGS51, **FIGS52, **FIGS53, **FIGS54, **FIGS55, **FIGS56, **FIGS57, **FIGS58, **FIGS59, **FIGSKT3}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
