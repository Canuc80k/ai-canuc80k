"""Dựng slide trình chiếu (HTML) và bản PDF từ Markdown.

Nguồn: content/phase-N/slides/<id>.md, các slide cách nhau bởi dòng `---`.
Dòng đầu của một slide có thể là chú thích chọn bố cục:
  <!-- title -->        trang bìa
  <!-- section 3 -->    trang mở phần, kèm số thứ tự
  <!-- split -->        hai cột, ngăn bởi dòng `|||`
  <!-- figure -->       một hình lớn
  <!-- center -->       nội dung căn giữa (công thức lớn)
  <!-- quiz -->         câu hỏi nhanh, bấm để hiện đáp án
Không ghi gì là slide thường. Hình viết ../fig/x.svg (tính từ thư mục slides/).

Chạy: python render_slides.py <thư-mục-content> <thư-mục-ra> [--pdf]
Đầu ra: <thư-mục-ra>/<id>.html (dùng ../../ui/ cho CSS, phông, KaTeX) và <id>.pdf nếu có --pdf.
"""
from pathlib import Path
import html, re, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_theory as rt  # noqa: E402

CONTENT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'content'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / 'slides_out'
LAYOUT = re.compile(r'^\s*<!--\s*(title|section|split|figure|center|quiz)\s*(\d*)\s*-->\s*\n')
KW = r'\b(?:def|return|import|from|for|in|if|else|elif|class|True|False|None|with|as|lambda|and|or|not|is|while|break|continue)\b'
TOKEN = re.compile(r'(#[^\n]*)|("(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')|' + f'({KW})' + r'|(\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b)')


def highlight(code):
    out, pos = '', 0
    for m in TOKEN.finditer(code):
        out += html.escape(code[pos:m.start()])
        kind = 'c' if m.group(1) else 's' if m.group(2) else 'k' if m.group(3) else 'n'
        out += f'<span class="t-{kind}">{html.escape(m.group(0))}</span>'
        pos = m.end()
    return out + html.escape(code[pos:])


def polish(frag):
    """Tô màu code Python, đánh dấu khối kết quả."""
    def code(m):
        return f'<pre class="code"><code>{highlight(html.unescape(m.group(1)))}</code></pre>'
    frag = re.sub(r'<pre><code class="language-(?:python|py)">(.*?)</code></pre>', code, frag, flags=re.S)
    frag = re.sub(r'<pre><code class="language-output">(.*?)</code></pre>',
                  r'<pre class="out"><span class="out-label">Kết quả</span><code>\1</code></pre>', frag, flags=re.S)
    frag = re.sub(r'<div class="table-wrap">|</div><!--tw-->', '', frag)
    return frag


def slide_html(chunk, base, path, section, number):
    m = LAYOUT.match(chunk)
    layout, arg = (m.group(1), m.group(2)) if m else ('plain', '')
    body = chunk[m.end():] if m else chunk
    if layout == 'title':
        h = re.search(r'^#\s+(.+)$', body, re.M)
        rest = body[h.end():].strip().split('\n\n')
        sub = rt.md_to_html(rest[0], base, path)[0] if rest and rest[0] else ''
        meta = html.escape(rest[1].strip()) if len(rest) > 1 else ''
        return (f'<section class="slide s-title"><div class="s-mark"></div><h1>{html.escape(h.group(1))}</h1>'
                f'<div class="s-sub">{sub}</div><p class="s-meta">{meta}</p></section>'), section
    if layout == 'section':
        h = re.search(r'^#\s+(.+)$', body, re.M).group(1).strip()
        return (f'<section class="slide s-section"><span class="s-no">{int(arg):02d}</span>'
                f'<h1>{html.escape(h)}</h1></section>'), h
    title = ''
    h = re.match(r'\s*##\s+(.+)\n', body)
    if h:
        title, body = h.group(1).strip(), body[h.end():]
    cols = [c for c in re.split(r'^\|\|\|\s*$', body, flags=re.M)]
    inner = ''.join(f'<div class="s-col">{polish(rt.md_to_html(c, base, path)[0])}</div>' for c in cols)
    head = (f'<div class="s-head"><span class="s-kicker">{html.escape(section)}</span>'
            f'<span class="s-num">{number}</span></div>')
    t = f'<h2 class="s-heading">{rt.md_to_html(title, base, path)[0][3:-4]}</h2>' if title else ''
    return f'<section class="slide s-{layout}">{head}{t}<div class="s-body">{inner}</div></section>', section


TAIL = '''<div class="progress"><i id="bar"></i></div></div><div class="bar"><button id="prev" onclick="move(-1)" aria-label="Slide trước">&larr;</button><span class="count" id="count"></span><button id="next" onclick="move(1)" aria-label="Slide sau">&rarr;</button></div><script src="../../ui/anim.js"></script><script>
(function(){var t=new URLSearchParams(location.hash.slice(1)).get('theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);})();
var n=0,s=[].slice.call(document.querySelectorAll('.slide'));
function over(el){var b=el.querySelector('.s-body');return el.scrollHeight>el.clientHeight+1||(b&&b.scrollHeight>b.clientHeight+1);}
function fit(el){el.style.removeProperty('--fs');var f=1;while(over(el)&&f>0.72){f-=0.04;el.style.setProperty('--fs',f.toFixed(2));}}
function show(){s.forEach(function(x,i){x.classList.toggle('active',i===n);});fit(s[n]);
document.getElementById('count').textContent=(n+1)+' / '+s.length;document.getElementById('bar').style.width=((n+1)/s.length*100)+'%';
document.getElementById('prev').disabled=n===0;document.getElementById('next').disabled=n===s.length-1;}
function move(d){n=Math.max(0,Math.min(s.length-1,n+d));show();}
document.addEventListener('keydown',function(e){if(e.target.closest&&e.target.closest('.anim-bar'))return;if(['ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();move(1);}if(['ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();move(-1);}if(e.key==='Home'){n=0;show();}if(e.key==='End'){n=s.length-1;show();}});
document.querySelector('.deck').addEventListener('click',function(e){
var o=e.target.closest('.quiz-opt');if(o){var q=o.closest('.quiz');if(!q.classList.contains('is-answered')){q.classList.add('is-answered');q.querySelectorAll('.quiz-opt').forEach(function(b){if(b.dataset.correct==='1')b.classList.add('is-right');else if(b===o)b.classList.add('is-wrong');});q.querySelector('.quiz-why').hidden=false;fit(s[n]);}return;}
if(e.target.closest('a,pre,button,.quiz,.anim'))return;var r=this.getBoundingClientRect();move(e.clientX<r.left+r.width*0.3?-1:1);});
window.addEventListener('resize',function(){fit(s[n]);});
window.addEventListener('beforeprint',function(){s.forEach(fit);});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){fit(s[n]);});
show();
if(window.Anim)Anim.scan(document);
</script></body></html>'''


def build(path, out_dir):
    text = path.read_text(encoding='utf-8')
    chunks = [c for c in re.split(r'^---\s*$', text, flags=re.M) if c.strip()]
    title = re.search(r'^#\s+(.+)$', chunks[0], re.M).group(1).strip()
    section, slides = '', []
    for i, chunk in enumerate(chunks, 1):
        h, section = slide_html(chunk.strip('\n') + '\n', path.parent, path, section, i)
        slides.append(h)
    page = ('<!doctype html><html lang="vi"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)} — Slide</title><link rel="icon" href="../../ui/favicon.svg">'
            '<link rel="stylesheet" href="../../ui/katex/katex.min.css"><link rel="stylesheet" href="../../ui/slides.css">'
            '</head><body><div class="deck v2">' + ''.join(slides) + TAIL)
    # Slide HTML nằm cùng một thư mục; resource source nằm theo từng phase.
    # Các asset này được bộ dựng bài học lưu tại giao_trinh/assets/.
    content_root = path.parents[2].resolve()
    def asset_href(match):
        url = html.unescape(match.group(1))
        if url.startswith(('http:', 'https:', 'mailto:', '#', 'data:')):
            return match.group(0)
        raw, separator, fragment = url.partition('#')
        asset = (path.parent / raw).resolve()
        if not asset.is_file() or not asset.is_relative_to(content_root):
            return match.group(0)
        relative = asset.relative_to(content_root).as_posix()
        target = '../assets/' + relative + (separator + fragment if separator else '')
        return 'href="' + html.escape(target, quote=True) + '"'
    page = re.sub(r'href="([^"]+)"', asset_href, page)
    out = out_dir / f'{path.stem}.html'
    out.write_text(page, encoding='utf-8')
    return out, len(slides)


def to_pdf(html_path, ui_dir):
    """In ra PDF 16:9 bằng Chromium. ui_dir: thư mục ui/ của website (CSS, phông, KaTeX)."""
    import shutil, tempfile
    from playwright.sync_api import sync_playwright
    tmp = Path(tempfile.mkdtemp())
    (tmp / 'giao_trinh' / 'slides').mkdir(parents=True)
    shutil.copytree(ui_dir, tmp / 'ui')
    page_path = tmp / 'giao_trinh' / 'slides' / html_path.name
    shutil.copy(html_path, page_path)
    pdf = html_path.with_suffix('.pdf')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1600, 'height': 900})
        pg.goto(page_path.as_uri() + '#theme=light')
        pg.wait_for_timeout(800)
        pg.emulate_media(media='print')
        pg.evaluate("document.querySelectorAll('.slide').forEach(fit)")
        pg.pdf(path=str(pdf), width='16in', height='9in', print_background=True, margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        b.close()
    shutil.rmtree(tmp)
    return pdf


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ui = next((Path(a.split('=', 1)[1]) for a in sys.argv if a.startswith('--pdf=')), None)
    for path in sorted(CONTENT.glob('phase-*/slides/*.md')):
        out, n = build(path, OUT)
        msg = f'{out.name}: {n} slide'
        if ui:
            msg += f', {to_pdf(out, ui).name}'
        print(msg)


if __name__ == '__main__':
    main()
