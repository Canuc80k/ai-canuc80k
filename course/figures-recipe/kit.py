"""Bộ vẽ hình lượt 8: mở rộng SVG với chữ code đơn cách có tô màu cú pháp, ô notebook, khung, nhãn ghi chú,
mũi tên cong và ảnh thật nhúng base64. Mọi màu đi qua biến CSS của website nên hình tự đổi theo nền sáng/tối.

Quy ước: viewBox rộng 640 (1 đơn vị = 1 px khi hiển thị trên trang bài); chữ nhãn 15–18, chữ code 13–15,
ghi chú phụ 13–14 màu muted. Không đặt câu dài trong hình: ý giải thích nằm ở caption và lời giảng.
"""
import base64, html, io, math, re
from pathlib import Path
from svg import SVG, R

TEXT = 'currentColor'
MUTED = 'var(--muted, #73716a)'
FAINT = 'var(--faint, #a19e94)'
LINE = 'var(--line-strong, #d3cebf)'
SOFT_LINE = 'var(--line, #e6e2d6)'
BLUE = 'var(--t-n, #2f6587)'
CLAY = 'var(--accent, #c2603e)'
GREEN = 'var(--t-s, #4d7337)'
SAND = '#b8892b'
CODE_BG = 'var(--code-bg, #f3f0e7)'
CODE_HEAD = 'var(--code-head, #ebe7dc)'
SURFACE = 'var(--surface, #ffffff)'
ACCENT_SOFT = 'var(--accent-soft, #f5e6dd)'
FONTS = {
    'serif': 'var(--serif, Lora, Georgia, serif)',
    'mono': 'var(--mono, "JetBrains Mono", Consolas, monospace)',
    'sans': 'var(--sans, Inter, "Segoe UI", sans-serif)',
}
KEYWORDS = {'def', 'return', 'for', 'in', 'if', 'elif', 'else', 'while', 'import', 'from', 'as', 'with', 'lambda',
            'is', 'not', 'and', 'or', 'del', 'try', 'except', 'raise', 'None', 'True', 'False', 'class', 'assert'}
TOKEN = re.compile(r'(?P<com>#.*)|(?P<str>"[^"]*"|\'[^\']*\')|(?P<num>\b\d+(?:\.\d+)?(?:e-?\d+)?\b)|(?P<word>[A-Za-z_]\w*)|(?P<other>.)')
MONO_W = 0.6  # bề rộng một ký tự JetBrains Mono theo cỡ chữ


def esc(s):
    return html.escape(str(s), quote=False)


class Fig(SVG):
    """SVG với các nét vẽ của lượt 8. Toạ độ chữ: (x, y) là đường giữa dòng (dominant-baseline middle)."""

    def t(self, x, y, value, size=16, anchor='middle', color=TEXT, weight=400, font='serif', italic=False, opacity=1):
        lines = str(value).split('\n')
        step = size * 1.35
        for i, line in enumerate(lines):
            y0 = y + i * step
            style = ' font-style="italic"' if italic else ''
            op = f' opacity="{opacity:g}"' if opacity != 1 else ''
            keep = ' xml:space="preserve" style="font-variant-ligatures:none"' if font == 'mono' else ''
            self.parts.append(f'<text{keep} x="{x:g}" y="{y0:g}" fill="{color}" text-anchor="{anchor}" dominant-baseline="middle" '
                              f'font-family=\'{FONTS[font]}\' font-size="{size:g}" font-weight="{weight}"{style}{op}>{esc(line)}</text>')
            self.labels.append({'x': x, 'y': y0, 'text': line, 'size': size, 'anchor': anchor})
        return self

    def mono(self, x, y, value, size=14, anchor='start', color=TEXT, weight=400):
        return self.t(x, y, value, size, anchor, color, weight, font='mono')

    def code(self, x, y, line, size=14, color=TEXT, plain=False):
        """Một dòng code Python có tô màu cú pháp (từ khóa, chuỗi, số, chú thích)."""
        spans = []
        if plain:
            spans.append(f'<tspan>{esc(line)}</tspan>')
        else:
            for m in TOKEN.finditer(line):
                kind = m.lastgroup
                s = m.group()
                c = {'com': 'var(--t-c, #8d8a80)', 'str': 'var(--t-s, #4d7337)', 'num': 'var(--t-n, #2f6587)'}.get(kind)
                if kind == 'word' and s in KEYWORDS:
                    c = 'var(--t-k, #9a4528)'
                spans.append(f'<tspan fill="{c}">{esc(s)}</tspan>' if c else esc(s))
        self.parts.append(f'<text x="{x:g}" y="{y:g}" fill="{color}" dominant-baseline="middle" xml:space="preserve" style="font-variant-ligatures:none" '
                          f'font-family=\'{FONTS["mono"]}\' font-size="{size:g}">{"".join(spans)}</text>')
        self.labels.append({'x': x, 'y': y, 'text': line, 'size': size, 'anchor': 'start', 'mono': True})
        return self

    def mono_width(self, text, size=14):
        return len(text) * size * MONO_W

    def box(self, x, y, w, h, color=LINE, fill='none', r=6, width=1.2, opacity=1, dash=None):
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}" fill-opacity="{opacity:g}" '
                          f'stroke="{color}" stroke-width="{width:g}"{extra}/>')
        return self

    def cell(self, x, y, w, lines, prompt='', size=14, out=None, out_color=TEXT, stale=False, accent=None, line_h=None):
        """Ô notebook kiểu Jupyter: nhãn [n] bên trái, khung code nền code-bg, phần output bên dưới (nếu có).
        Trả về chiều cao đã dùng."""
        line_h = line_h or size * 1.6
        w = max(w, max(self.mono_width(l, size) for l in lines) + 26)   # ô luôn đủ rộng cho dòng dài nhất
        h = len(lines) * line_h + 14
        border = accent or LINE
        self.box(x, y, w, h, border, CODE_BG, r=6, width=1.6 if accent else 1.1)
        if prompt:
            self.mono(x - 10, y + 7 + line_h / 2, prompt, size - 1, 'end', MUTED)
        for i, line in enumerate(lines):
            self.code(x + 12, y + 7 + line_h * (i + .5), line, size)
        used = h
        if out is not None:
            oy = y + h + 6
            for i, line in enumerate(str(out).split('\n')):
                self.mono(x + 12, oy + line_h * (i + .5), line, size, color=out_color)
            used += 6 + line_h * len(str(out).split('\n'))
            if stale:
                self.box(x + 4, oy - 2, self.mono_width(max(str(out).split('\n'), key=len), size) + 16, line_h * len(str(out).split('\n')) + 4,
                         SAND, 'none', r=4, width=1.3, dash='4 3')
        return used

    def pill(self, x, y, text, color=BLUE, size=13, anchor='middle', font='sans', fill_opacity=.12):
        w = len(text) * size * (.62 if font == 'mono' else .55) + 16
        h = size + 10
        x0 = x - w / 2 if anchor == 'middle' else (x if anchor == 'start' else x - w)
        self.box(x0, y - h / 2, w, h, color, color, r=h / 2, width=1, opacity=fill_opacity)
        self.t(x0 + w / 2, y + .5, text, size, 'middle', color, 500, font=font)
        return w

    def note(self, x, y, text, size=13.5, anchor='start', color=MUTED, italic=False):
        return self.t(x, y, text, size, anchor, color, 400, font='serif', italic=italic)

    def curve(self, x1, y1, x2, y2, bend=.25, color=TEXT, width=1.4, head=True, dash=None):
        """Mũi tên cong: bend > 0 cong sang trái theo chiều đi."""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx - dy * bend, my + dx * bend
        self.path(f'M {x1:g},{y1:g} Q {cx:g},{cy:g} {x2:g},{y2:g}', color, width, dash=dash)
        if head:
            a = math.atan2(y2 - cy, x2 - cx)
            l = 8
            p = [(x2 - l * math.cos(a - s), y2 - l * math.sin(a - s)) for s in [.42, -.42]]
            self.path(f'M {p[0][0]:g},{p[0][1]:g} L {x2:g},{y2:g} L {p[1][0]:g},{p[1][1]:g}', color, width)
        return self

    def photo(self, x, y, w, h, source, quality=82, max_px=900, crop=None, radius=6, border=True):
        """Nhúng ảnh thật (JPEG/PNG trên đĩa hoặc mảng numpy HxWx3 0..255) dạng base64, bo góc."""
        from PIL import Image
        import numpy as np
        if isinstance(source, (str, Path)):
            im = Image.open(source).convert('RGB')
        else:
            im = Image.fromarray(np.asarray(source).astype('uint8')).convert('RGB')
        if crop:
            im = im.crop(crop)
        scale = min(1, max_px / max(im.size))
        if scale < 1:
            im = im.resize((round(im.size[0] * scale), round(im.size[1] * scale)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=quality, optimize=True)
        data = base64.b64encode(buf.getvalue()).decode()
        cid = f'clip{len(self.parts)}'
        self.parts.append(f'<clipPath id="{cid}"><rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{radius:g}"/></clipPath>'
                          f'<image x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})" '
                          f'href="data:image/jpeg;base64,{data}"/>')
        if border:
            self.box(x, y, w, h, LINE, 'none', r=radius, width=1)
        return self

    def grid(self, x, y, values, cw=40, ch=32, color=BLUE, fill=None, size=15, font='serif', head_color=LINE, inner=SOFT_LINE):
        """Bảng giá trị với viền ngoài màu ngữ nghĩa, lưới trong nhạt; fill: dict (i,j) -> (màu, độ đậm)."""
        fill = fill or {}
        nr, nc = len(values), len(values[0])
        for (i, j), (c, op) in fill.items():
            self.box(x + j * cw, y + i * ch, cw, ch, 'none', c, r=0, width=0, opacity=op)
        for i in range(1, nr):
            self.line(x, y + i * ch, x + nc * cw, y + i * ch, inner, .9)
        for j in range(1, nc):
            self.line(x + j * cw, y, x + j * cw, y + nr * ch, inner, .9)
        for i, row in enumerate(values):
            for j, v in enumerate(row):
                if v is not None and v != '':
                    self.t(x + (j + .5) * cw, y + (i + .5) * ch, v, size, font=font)
        self.box(x, y, nc * cw, nr * ch, color, 'none', r=3, width=1.4)
        return self


def _tiles(self, x, y, values, cw=34, ch=30, color=BLUE, gap=3, fills=None, size=14, font='mono', opacity=.13,
           r=4, text_color=TEXT, colors=None):
    """Ô bo góc nền nhạt, không kẻ lưới (phong cách gọn của lượt 8). fills: {(i, j): (màu, độ đậm)};
    colors: {(i, j): màu chữ}. values có thể chứa None để bỏ trống ô."""
    fills = fills or {}
    colors = colors or {}
    for i, row in enumerate(values):
        for j, v in enumerate(row):
            c, op = fills.get((i, j), (color, opacity))
            cx, cy = x + j * (cw + gap), y + i * (ch + gap)
            self.box(cx, cy, cw, ch, 'none', c, r=r, width=0, opacity=op)
            if v is not None and v != '':
                self.t(cx + cw / 2, cy + ch / 2 + .5, v, size, color=colors.get((i, j), text_color), font=font)
    return (len(values[0]) * (cw + gap) - gap, len(values) * (ch + gap) - gap)


def _label(self, x, y, text, size=13, anchor='middle', color=MUTED, weight=400):
    return self.t(x, y, text, size, anchor, color, weight, font='sans')


Fig.tiles = _tiles
Fig.label = _label


class Axes:
    """Khung biểu đồ gọn trong một Fig: lưới ngang nhạt, nhãn trục nhỏ, không viền trên/phải.
    x, y, w, h: vùng vẽ (không gồm nhãn). xlim/ylim: miền dữ liệu."""

    def __init__(self, fig, x, y, w, h, xlim, ylim, xticks=None, yticks=None, xfmt='{:g}', yfmt='{:g}',
                 xlabel=None, ylabel=None, grid=True, frame=True):
        self.f, self.x, self.y, self.w, self.h = fig, x, y, w, h
        self.xlim, self.ylim = xlim, ylim
        if grid and yticks:
            for v in yticks:
                fig.line(x, self.Y(v), x + w, self.Y(v), SOFT_LINE, .8)
        if frame:
            fig.line(x, y + h, x + w, y + h, LINE, 1)
        for v in yticks or []:
            fig.label(x - 8, self.Y(v), yfmt.format(v), 11, 'end', FAINT)
        for v in xticks or []:
            fig.label(self.X(v), y + h + 14, xfmt.format(v), 11, 'middle', FAINT)
        if xlabel:
            fig.label(x + w, y + h + 30, xlabel, 11.5, 'end', FAINT)
        if ylabel:
            fig.label(x - 8, y - 14, ylabel, 11.5, 'start', FAINT)

    def X(self, v):
        a, b = self.xlim
        return self.x + (v - a) / (b - a) * self.w

    def Y(self, v):
        a, b = self.ylim
        return self.y + self.h - (v - a) / (b - a) * self.h

    def line(self, xs, ys, color=BLUE, width=1.8, dash=None, clip=True):
        pts = []
        for a, b in zip(xs, ys):
            if clip:
                b = min(max(b, self.ylim[0]), self.ylim[1])
            pts.append(f'{self.X(a):.1f},{self.Y(b):.1f}')
        self.f.path('M ' + ' L '.join(pts), color, width, dash=dash)
        return self

    def step(self, xs, ys, color=BLUE, width=1.6):
        """Đường bậc thang tại các điểm chuyển (cho kNN)."""
        pts = []
        for i, (a, b) in enumerate(zip(xs, ys)):
            if i:
                pts.append(f'{self.X(a):.1f},{self.Y(ys[i - 1]):.1f}')
            pts.append(f'{self.X(a):.1f},{self.Y(b):.1f}')
        self.f.path('M ' + ' L '.join(pts), color, width)
        return self

    def dots(self, xs, ys, color=FAINT, r=2.6, fill=None, opacity=1):
        for a, b in zip(xs, ys):
            self.f.circle(self.X(a), self.Y(b), r, color, fill, 0, opacity)
        return self

    def hline(self, v, color=SAND, width=1.4, dash='5 4'):
        self.f.line(self.x, self.Y(v), self.x + self.w, self.Y(v), color, width, dash)
        return self


Fig.axes = lambda self, *a, **k: Axes(self, *a, **k)
