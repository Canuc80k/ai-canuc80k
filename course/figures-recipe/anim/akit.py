"""Bộ dựng hình động (lượt 9): mỗi hình là một chuỗi khung ảnh, đóng thành một sprite WebP + tệp mô tả JSON.

Trang bài và slide phát bằng ui/anim.js: tự chạy lặp khi cuộn tới, bấm để dừng, kéo thanh để xem từng khung;
bản in (PDF) hiện các khung chính cạnh nhau. Nhãn từng khung là chữ HTML (đổi màu theo nền), nên trong ảnh
không đặt chữ trừ khi thật cần; khung nào có nét vẽ theo màu chữ thì dựng hai bản sáng/tối.

Quy ước kích thước: khung rộng W px (mặc định 960) hiển thị ở W/1.5 px CSS (640, vừa cột chữ của bài).
"""
from pathlib import Path
import io, json, math, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image

HERE = Path(__file__).resolve().parent
RECIPE = HERE.parent
for f in ['Lora.ttf', 'Inter-Regular.ttf', 'Inter-Semibold.ttf']:
    font_manager.fontManager.addfont(str(RECIPE / f))
LORA = font_manager.FontProperties(fname=str(RECIPE / 'Lora.ttf')).get_name()
INTER = font_manager.FontProperties(fname=str(RECIPE / 'Inter-Regular.ttf')).get_name()
plt.rcParams.update({'font.family': [LORA, 'DejaVu Serif'], 'mathtext.fontset': 'stix',
                     'axes.spines.top': False, 'axes.spines.right': False})

# Màu theo đúng biến CSS của website (portal.css): sáng / tối.
THEMES = {
    'light': dict(bg='#faf9f5', text='#1f1e1c', text2='#3d3c38', muted='#73716a', faint='#a19e94', line='#d3cebf',
                  soft='#e6e2d6', clay='#c2603e', blue='#2f6587', green='#4d7337', sand='#b8892b', surface='#ffffff'),
    'dark': dict(bg='#262624', text='#f2f0e9', text2='#d8d5cb', muted='#a5a299', faint='#7c7970', line='#4a4944',
                 soft='#3a3935', clay='#d97757', blue='#8fbad8', green='#a9c48f', sand='#d4a64a', surface='#30302e'),
}
SAMPLE_CREDIT = {
    'china.jpg': 'scikit-learn sample image china.jpg (danielbuechele / Flickr, CC BY 2.0)',
    'flower.jpg': 'scikit-learn sample image flower.jpg (vultilion / Flickr, CC BY 2.0)',
}


def sample(name):
    """Ảnh mẫu kèm scikit-learn (uint8 HxWx3)."""
    from sklearn.datasets import load_sample_image
    return load_sample_image(name)


def skdata(name):
    """Ảnh mẫu kèm scikit-image (đọc thẳng tệp, không tải mạng)."""
    import skimage.data as d
    return getattr(d, name)()


def fig_frame(w=960, h=540, dpi=150):
    """Figure matplotlib nền trong suốt, kích thước đúng w x h px."""
    fig = plt.figure(figsize=(w / dpi, h / dpi), dpi=dpi)
    fig.patch.set_alpha(0)
    return fig


def grab(fig):
    """Figure -> mảng RGBA uint8, rồi đóng figure."""
    fig.canvas.draw()
    a = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    return a


def to_rgba(img):
    a = np.asarray(img)
    if a.dtype != np.uint8:
        a = np.clip(a, 0, 255).astype(np.uint8)
    if a.ndim == 2:
        a = np.stack([a] * 3, -1)
    if a.shape[2] == 3:
        a = np.concatenate([a, np.full(a.shape[:2] + (1,), 255, np.uint8)], -1)
    return a


def resize(img, w, h=None, resample=Image.LANCZOS):
    im = Image.fromarray(np.asarray(img).astype(np.uint8))
    if h is None:
        h = round(im.size[1] * w / im.size[0])
    return np.asarray(im.resize((w, h), resample))


def round_corners(rgba, r=10):
    """Bo góc ảnh (alpha), giống ảnh thật trong SVG lượt 8."""
    a = rgba.copy()
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cx = np.clip(xx, r, w - 1 - r)
    cy = np.clip(yy, r, h - 1 - r)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    alpha = np.clip(r + .5 - d, 0, 1)
    a[..., 3] = (a[..., 3] * alpha).astype(np.uint8)
    return a


class Anim:
    """Một hình động. frames(theme) trả danh sách mảng RGBA cùng kích thước.

    labels: nhãn từng khung (chuỗi ngắn; `code` hiện bằng phông đơn cách).
    dur: ms mỗi khung (số hoặc danh sách); hold: ms dừng ở khung cuối trước khi lặp.
    key: chỉ số khung in ra PDF. photo=True: nén lossy (ảnh thật); False: lossless (nét vẽ).
    themed=True: dựng thêm bản tối (khi khung có nét màu chữ).
    """

    def __init__(self, name, caption, labels, draw, dur=700, hold=1800, key=None, photo=True, themed=False,
                 display=None, pcols=None, quality=86):
        self.name, self.caption, self.labels, self.draw = name, caption, list(labels), draw
        self.dur, self.hold, self.key, self.photo, self.themed = dur, hold, key, photo, themed
        self.display, self.pcols, self.quality = display, pcols, quality


def default_keys(n, k=4):
    if n <= k:
        return list(range(n))
    return sorted({round(i * (n - 1) / (k - 1)) for i in range(k)})


def sprite(frames):
    h, w = frames[0].shape[:2]
    n = len(frames)
    cols = max(1, min(n, math.ceil(math.sqrt(n * h / w))))
    while cols * w > 16000:
        cols -= 1
    rows = math.ceil(n / cols)
    assert rows * h <= 16000, 'sprite quá cao'
    s = np.zeros((rows * h, cols * w, 4), np.uint8)
    for i, f in enumerate(frames):
        assert f.shape[:2] == (h, w), (i, f.shape)
        r, c = divmod(i, cols)
        s[r * h:(r + 1) * h, c * w:(c + 1) * w] = to_rgba(f)
    return s, cols


def encode(s, photo, quality):
    im = Image.fromarray(s, 'RGBA')
    opaque = bool((s[..., 3] == 255).all())
    if opaque:
        im = im.convert('RGB')
    buf = io.BytesIO()
    if photo:
        im.save(buf, 'WEBP', quality=quality, method=6, alpha_quality=100)
    else:
        im.save(buf, 'WEBP', lossless=True, quality=100, method=6)
    return buf.getvalue()


def build(anim, out_dir):
    """Dựng một hình động vào out_dir: <name>.anim.webp, [.anim.dark.webp], .anim.json. Trả về báo cáo."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    light = [to_rgba(f) for f in anim.draw('light')]
    n = len(light)
    assert n == len(anim.labels), (anim.name, n, len(anim.labels))
    dark = [to_rgba(f) for f in anim.draw('dark')] if anim.themed else None
    if dark is not None and all(np.array_equal(a, b) for a, b in zip(light, dark)):
        dark = None
    h, w = light[0].shape[:2]
    files = {}
    s, cols = sprite(light)
    files[f'{anim.name}.anim.webp'] = encode(s, anim.photo, anim.quality)
    if dark is not None:
        files[f'{anim.name}.anim.dark.webp'] = encode(sprite(dark)[0], anim.photo, anim.quality)
    dur = anim.dur if isinstance(anim.dur, (int, float)) else list(anim.dur)
    if isinstance(dur, list):
        assert len(dur) == n, (anim.name, 'dur')
    key = anim.key if anim.key is not None else default_keys(n)
    meta = {'w': w, 'h': h, 'n': n, 'cols': cols, 'dur': dur, 'hold': anim.hold, 'labels': anim.labels,
            'key': key, 'dark': dark is not None, 'dw': anim.display or round(w / 1.5),
            'pcols': anim.pcols or (min(len(key), 4) if anim.photo else 2)}   # nét vẽ có chữ: in 2 cột cho đọc được
    files[f'{anim.name}.anim.json'] = (json.dumps(meta, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    for k, v in files.items():
        (out_dir / k).write_bytes(v)
    sizes = {k: len(v) for k, v in files.items()}
    return {'name': anim.name, 'caption': anim.caption, 'frames': n, 'size': [w, h], 'bytes': sizes,
            'sha256': {k: hashlib.sha256(v).hexdigest() for k, v in files.items()}}, light, dark


def contact(light, dark, labels, path, cols=None, scale=.5):
    """Ảnh ghép mọi khung trên nền trang sáng (và tối nếu có) để duyệt bằng mắt."""
    from PIL import ImageDraw, ImageFont
    n = len(light)
    h, w = light[0].shape[:2]
    cols = cols or min(n, 4)
    tw, th = int(w * scale), int(h * scale)
    rows = math.ceil(n / cols)
    themes = [('light', light)] + ([('dark', dark)] if dark is not None else [('dark', light)])
    pad, lab = 12, 26
    sheet = Image.new('RGB', (len(themes) * (cols * (tw + pad) + pad), rows * (th + lab + pad) + pad), '#888')
    font = ImageFont.truetype(str(RECIPE / 'Inter-Regular.ttf'), 15)
    for t, (theme, frames) in enumerate(themes):
        bg = THEMES[theme]['bg']
        x0 = t * (cols * (tw + pad) + pad)
        panel = Image.new('RGB', (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad), bg)
        d = ImageDraw.Draw(panel)
        for i, f in enumerate(frames):
            r, c = divmod(i, cols)
            im = Image.fromarray(to_rgba(f), 'RGBA').resize((tw, th), Image.LANCZOS)
            x, y = pad + c * (tw + pad), pad + r * (th + lab + pad)
            panel.paste(im, (x, y), im)
            d.text((x, y + th + 4), f'{i}: {labels[i]}'[:70], fill=THEMES[theme]['muted'], font=font)
        sheet.paste(panel, (x0, 0))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


# ───────────── vẽ trực tiếp bằng PIL (ảnh thật + khung, không chữ) ─────────────
from PIL import ImageDraw  # noqa: E402


def hexrgb(c, a=255):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def canvas(w, h):
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def paste(cv, arr, x, y, w, h, nearest=False, radius=8):
    """Dán ảnh (mảng HxW[x3/4]) vào canvas tại (x, y), co giãn về w x h, bo góc."""
    im = Image.fromarray(to_rgba(arr), 'RGBA').resize((w, h), Image.NEAREST if nearest else Image.LANCZOS)
    a = round_corners(np.asarray(im), radius) if radius else np.asarray(im)
    im = Image.fromarray(a, 'RGBA')
    cv.alpha_composite(im, (int(x), int(y)))
    return cv


def rect(cv, x, y, w, h, color, width=3, fill=None, radius=0):
    d = ImageDraw.Draw(cv, 'RGBA')
    d.rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=radius, outline=color, width=width, fill=fill)
    return cv


def arr(cv):
    return np.asarray(cv).copy()


def font(size, kind='sans', bold=False):
    from PIL import ImageFont
    f = {'sans': 'Inter-Semibold.ttf' if bold else 'Inter-Regular.ttf', 'serif': 'Lora.ttf'}[kind]
    return ImageFont.truetype(str(RECIPE / f), size)


def text(cv, x, y, s, color, size=22, anchor='mm', kind='sans', bold=False):
    ImageDraw.Draw(cv, 'RGBA').text((x, y), str(s), fill=color, font=font(size, kind, bold), anchor=anchor)
    return cv


def ease(t):
    """Chuyển động mượt 0..1 (nhanh dần rồi chậm dần)."""
    t = min(1, max(0, t))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def plain_axes(theme, w=960, h=480, rect=(.06, .12, .9, .84), dpi=150):
    """Figure trong suốt với một axes gọn: trục dưới/trái màu line, không lưới."""
    t = THEMES[theme]
    fig = fig_frame(w, h, dpi)
    ax = fig.add_axes(rect)
    ax.patch.set_alpha(0)
    for s in ['left', 'bottom']:
        ax.spines[s].set_color(t['line'])
    ax.tick_params(colors=t['muted'], labelsize=9, length=3)
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_color(t['muted'])
    return fig, ax
