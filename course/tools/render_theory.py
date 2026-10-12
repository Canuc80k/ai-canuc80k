"""Chuyển bài lý thuyết Markdown (có công thức LaTeX) thành HTML để đưa lên website.

- Công thức: $...$ (trong dòng) và $$...$$ (riêng dòng), render sẵn bằng KaTeX qua Node.
- Hình: ![Chú thích](fig/ten.svg) được nhúng thẳng SVG để đổi màu theo nền sáng/tối.
- Đầu ra: theory.json = {"lessons": {id: {"title", "html", "headings"}}, "phases": {id: {"html"}}}

Chạy: python render_theory.py <thư-mục-content> <tệp-ra.json>
Quy ước tên tệp: phase-2/2.1.md cho bài 2.1; phase-2/_intro.md cho phần mở chương.
"""
from pathlib import Path
import html, json, re, subprocess, sys
import markdown

ROOT = Path(__file__).resolve().parent
CONTENT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'content'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT.parent / 'theory.json'

FENCE = re.compile(r'(^```.*?^```[ \t]*$)', re.S | re.M)
DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$(?!\d)')
INLINE_CODE = re.compile(r'`[^`\n]+`')
QUOTE = re.compile(r'"([^"\n]+)"')
CONTAINER = re.compile(r'^:::[ \t]*(\w+)[ \t]*(.*?)\n(.*?)^:::[ \t]*$', re.S | re.M)
OPTION = re.compile(r'^- \[( |x)\] (.*)$')
SOURCE = re.compile(r'^(Đề thi|Phỏng theo):\s*(.+)$')
SOURCE_KIND = {'Đề thi': 'exam', 'Phỏng theo': 'adapted'}
CALLOUT = {'goal': 'Mục tiêu', 'trap': 'Bẫy', 'tip': 'Mẹo', 'note': 'Ghi chú'}
SPECIAL = {'Ví dụ tính tay': 'is-example', 'Khi đi thi': 'is-exam', 'Tóm tắt': 'is-summary', 'Kiểm tra cuối bài': 'is-check', 'Đọc thêm': 'is-read'}
FIGURE = re.compile(r'^!\[([^\]]*)\]\(((?:\.\./)?fig/[^)]+\.svg)\)\s*$', re.M)
ANIM = re.compile(r'^!\[([^\]]*)\]\(((?:\.\./)?fig/[^)]+)\.anim\.webp\)\s*$', re.M)


def katex(items):
    if not items:
        return []
    r = subprocess.run(['node', str(ROOT / 'katex_render.js')], input=json.dumps(items), capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stderr)
    return json.loads(r.stdout)


def svg_inline(path, caption):
    svg = path.read_text(encoding='utf-8')
    svg = svg[svg.index('<svg'):]
    svg = re.sub(r'<metadata>.*?</metadata>', '', svg, flags=re.S)
    # style toàn cục của matplotlib (*{stroke-linecap:butt}) sẽ lan ra cả trang; CSS .fig svg thay thế
    svg = re.sub(r'<style[^>]*>.*?</style>', '', svg, flags=re.S)
    svg = svg.replace('<svg ', f'<svg role="img" aria-label="{html.escape(caption, quote=True)}" ', 1)
    return f'<figure class="fig">{svg}<figcaption>{caption}</figcaption></figure>'


def anim_html(base, stem, caption):
    """Hình động (lượt 9): sprite WebP + mô tả JSON do figures-recipe/anim dựng; ui/anim.js phát.
    Đường dẫn sprite để trong thẻ a ẩn để bộ dựng chép asset và đổi href như mọi tệp kèm."""
    meta = json.loads((base / f'{stem}.anim.json').read_text(encoding='utf-8'))
    links = f'<a class="anim-src" data-v="light" href="{stem}.anim.webp" hidden></a>'
    if meta.get('dark'):
        assert (base / f'{stem}.anim.dark.webp').is_file(), stem
        links += f'<a class="anim-src" data-v="dark" href="{stem}.anim.dark.webp" hidden></a>'
    data = html.escape(json.dumps(meta, ensure_ascii=False, separators=(',', ':')), quote=True)
    label = html.escape(caption, quote=True)
    return (f'<figure class="fig anim" data-anim="{data}">{links}<div class="anim-live">'
            f'<canvas class="anim-stage" width="{meta["w"]}" height="{meta["h"]}" role="img" aria-label="{label}"></canvas>'
            f'<div class="anim-bar"></div></div><div class="anim-keys" aria-hidden="true"></div>'
            f'<figcaption>{caption}</figcaption></figure>')


def md_to_html(text, base, path):
    """Markdown (có công thức, hình, khối :::) thành HTML. base: thư mục chứa fig/."""
    store, math = {}, []

    def keep(value):
        key = f'@@K{len(store)}@@'
        store[key] = value
        return key

    # 1. tách code block để công thức trong code không bị đụng tới
    text = FENCE.sub(lambda m: keep(('code', m.group(1))), text)
    # 2. hình
    text = FIGURE.sub(lambda m: '\n\n' + keep(('raw', svg_inline(base / m.group(2), m.group(1)))) + '\n\n', text)
    text = ANIM.sub(lambda m: '\n\n' + keep(('raw', anim_html(base, m.group(2), m.group(1)))) + '\n\n', text)
    # 3. công thức
    def math_key(tex, display):
        math.append({'tex': tex.strip(), 'display': display})
        return keep(('math', len(math) - 1))
    text = DISPLAY.sub(lambda m: '\n\n' + math_key(m.group(1), True) + '\n\n', text)
    text = INLINE.sub(lambda m: math_key(m.group(1), False), text)
    # 3b. inline code giữ nguyên; ngoặc kép thẳng trong văn bản thành ngoặc kép cong
    text = INLINE_CODE.sub(lambda m: keep(('code', m.group(0))), text)
    text = QUOTE.sub(r'“\1”', text)
    MD_EXT = ['tables', 'fenced_code', 'sane_lists']

    def restore_code(t):
        for key, (kind, value) in store.items():
            if kind == 'code':
                t = t.replace(key, value)
        return t

    def md(t):
        return markdown.markdown(restore_code(t.strip()), extensions=MD_EXT, output_format='html')

    def md_inline(t):
        return re.sub(r'^<p>(.*)</p>$', r'\1', md(t), flags=re.S)

    # 4. khối đặc biệt ::: quiz / goal / trap / tip / note
    def container(m):
        kind, title, body = m.group(1), m.group(2).strip(), m.group(3)
        if kind == 'quiz':
            lines = body.strip('\n').split('\n')
            opt = [i for i, l in enumerate(lines) if OPTION.match(l)]
            assert opt, (path, 'quiz không có lựa chọn')
            question = '\n'.join(lines[:opt[0]])
            # Dòng "Đề thi: ..." / "Phỏng theo: ..." sau các lựa chọn là ghi chú nguồn, luôn hiện ở chân câu hỏi.
            tail = lines[opt[-1] + 1:]
            sources = [SOURCE.match(l) for l in tail if SOURCE.match(l)]
            why = '\n'.join(l for l in tail if not SOURCE.match(l))
            items = []
            for k, i in enumerate(opt):
                mark, label = OPTION.match(lines[i]).groups()
                items.append(f'<li><button type="button" class="quiz-opt" data-action="quiz" data-correct="{int(mark == "x")}">'
                             f'<span class="quiz-key">{"ABCDEF"[k]}</span><span class="quiz-text">{md_inline(label)}</span></button></li>')
            assert sum(OPTION.match(lines[i]).group(1) == 'x' for i in opt) == 1, (path, 'quiz cần đúng một đáp án')
            html_ = (f'<div class="quiz"><p class="quiz-label">{title or "Hỏi nhanh"}</p><div class="quiz-q">{md(question)}</div>'
                     f'<ol class="quiz-opts">{"".join(items)}</ol><div class="quiz-why" hidden>{md(why)}</div>'
                     + ''.join(f'<p class="quiz-src quiz-src-{SOURCE_KIND[s.group(1)]}"><span class="quiz-src-kind">{s.group(1)}</span>'
                               f'{md_inline(s.group(2))}</p>' for s in sources)
                     + '</div>')
        else:
            assert kind in CALLOUT, (path, kind)
            html_ = (f'<aside class="callout callout-{kind}"><p class="callout-title">{title or CALLOUT[kind]}</p>'
                     f'{md(body)}</aside>')
        return '\n\n' + keep(('raw', html_)) + '\n\n'
    text = CONTAINER.sub(container, text)
    rendered = katex(math)
    out = md(text)
    for _ in range(4):   # khối lồng nhau: thay đến khi hết khóa
        for key, (kind, value) in store.items():
            if kind == 'raw':
                out = out.replace(f'<p>{key}</p>', value).replace(key, value)
            elif kind == 'math':
                frag = rendered[value]
                out = out.replace(f'<p>{key}</p>', frag).replace(key, frag)
            elif kind == 'code':
                out = out.replace(key, html.escape(value))
    leftover = re.findall(r'@@K\d+@@', out)
    assert not leftover, (path, leftover[:3])
    return out, len(math)


def render(path):
    out, n_math = md_to_html(path.read_text(encoding='utf-8'), path.parent, path)
    title = re.search(r'<h1>(.*?)</h1>', out)
    out = re.sub(r'<h1>.*?</h1>\s*', '', out, count=1)
    if not path.name.startswith('_') and out.startswith('<p>'):
        out = '<p class="hook">' + out[3:]   # đoạn mở bài
    headings = [re.sub('<[^>]+>', '', h) for h in re.findall(r'<h2>(.*?)</h2>', out)]
    # mỗi mục h2 là một <section>; vài mục cuối có kiểu riêng
    parts = re.split(r'(?=<h2>)', out)
    sections = []
    for part in parts[1:]:
        name = re.sub('<[^>]+>', '', re.match(r'<h2>(.*?)</h2>', part).group(1))
        cls = ' '.join(['t-sec', SPECIAL.get(name, '')]).strip()
        sections.append(f'<section class="{cls}">{part.rstrip()}</section>')
    out = parts[0] + ''.join(sections)
    return {'title': re.sub('<[^>]+>', '', title.group(1)) if title else '', 'html': out, 'headings': headings, 'formulas': n_math}


def main():
    data = {'lessons': {}, 'phases': {}}
    for path in sorted(CONTENT.glob('phase-*/*.md')):  # slide nằm ở phase-*/slides/, không lẫn vào đây
        item = render(path)
        if path.stem == '_intro':
            data['phases'][path.parent.name.split('-')[1]] = item
        else:
            data['lessons'][path.stem] = item
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: {i: v.get('formulas') for i, v in d.items()} for k, d in data.items()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
