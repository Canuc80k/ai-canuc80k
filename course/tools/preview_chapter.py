"""Xuất một chương lý thuyết thành MỘT tệp HTML tự chứa (phông, KaTeX, hình nhúng sẵn) để đọc duyệt.

Chạy: python preview_chapter.py <phase> <tệp-ra.html> [thư-mục-ui-src]
Cần theory.json đã render (render_theory.py).
"""
import base64, json, re, sys
from pathlib import Path

CUR = Path(__file__).resolve().parent.parent
PHASE = sys.argv[1] if len(sys.argv) > 1 else '2'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else CUR / f'preview-phase-{PHASE}.html'
UI_SRC = Path(sys.argv[3]) if len(sys.argv) > 3 else CUR.parent / 'AI-course-ui-redesign-20261002' / 'src'

th = json.loads((CUR / 'theory.json').read_text(encoding='utf-8'))
cur = json.loads((CUR / 'curriculum.json').read_text(encoding='utf-8'))
meta = {l['id']: l for l in cur['lessons']}
phase = next(p for p in cur['phases'] if str(p['id']) == PHASE)
order = sorted((k for k in th['lessons'] if meta[k]['phase'] == phase['id']), key=lambda x: int(x.split('.')[1]))

css = (CUR / 'tools' / 'katex' / 'katex.min.css').read_text(encoding='utf-8')
css = re.sub(r'url\((fonts/[^)]+\.woff2)\) format\("woff2"\)(,url\([^)]+\) format\("woff"\),url\([^)]+\) format\("truetype"\))?',
             lambda m: 'url(data:font/woff2;base64,' + base64.b64encode((CUR / 'tools' / 'katex' / m.group(1)).read_bytes()).decode() + ') format("woff2")', css)
font = lambda n: 'data:font/woff;base64,' + base64.b64encode((UI_SRC / 'fonts' / n).read_bytes()).decode()
portal = (UI_SRC / 'portal.css').read_text(encoding='utf-8')
theory_css = '\n'.join(l for l in portal.splitlines() if l.startswith(('.theory', '.fig', '.prose', '.table-wrap')) and 'prose.md' not in l)

toc = ''.join(f'<a href="#b{k}"><span>{k}</span>{meta[k]["title"]}</a>' for k in order)
intro = th['phases'].get(PHASE, {}).get('html', '')
body = f'<section id="intro"><p class="kicker">Phase {PHASE}</p><h1>{phase["title"]}</h1><nav class="chap-toc">{toc}</nav><article class="prose theory">{intro}</article></section>'
for k in order:
    body += (f'<section id="b{k}"><p class="kicker">Bài {k}</p><h1>{meta[k]["title"]}</h1><p class="lead">{meta[k]["summary"]}</p>'
             f'<article class="prose theory">{th["lessons"][k]["html"]}</article></section>')
page = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{phase["title"]} — AI Canuc80k</title>
<style>{css}
@font-face{{font-family:"Lora";src:url({font("lora.woff")}) format("woff");font-weight:400 700}}
@font-face{{font-family:"Lora";src:url({font("lora-italic.woff")}) format("woff");font-weight:400 700;font-style:italic}}
@font-face{{font-family:"Inter";src:url({font("inter-400.woff")}) format("woff");font-weight:400}}
@font-face{{font-family:"Inter";src:url({font("inter-600.woff")}) format("woff");font-weight:500 700}}
@font-face{{font-family:"JetBrains Mono";src:url({font("jetbrains-mono.woff")}) format("woff")}}
:root{{--serif:"Lora",Georgia,serif;--sans:"Inter",system-ui,sans-serif;--mono:"JetBrains Mono",Consolas,monospace;--bg:#faf9f5;--bg-side:#f4f2ea;--line:#e6e2d6;--line-strong:#d3cebf;--text:#1f1e1c;--text-2:#3d3c38;--muted:#73716a;--faint:#a19e94;--accent:#c2603e;--accent-ink:#9a4528;--code-bg:#f3f0e7;--code-text:#2b2a27}}
@media (prefers-color-scheme:dark){{:root{{--bg:#262624;--bg-side:#1f1e1d;--line:#3a3935;--line-strong:#4a4944;--text:#f2f0e9;--text-2:#d8d5cb;--muted:#a5a299;--faint:#7c7970;--accent:#d97757;--accent-ink:#eb9a7e;--code-bg:#1f1e1d;--code-text:#e6e3da}}}}
body{{margin:0;background:var(--bg);color:var(--text)}}main{{max-width:760px;margin:0 auto;padding:48px 20px 96px}}
section{{padding:24px 0 56px;border-bottom:1px solid var(--line)}}h1{{font:500 40px/1.15 var(--serif);margin:0 0 10px;letter-spacing:-.01em}}
.kicker{{font:500 13px var(--sans);color:var(--accent-ink);margin:0 0 8px}}.lead{{font:16px/1.5 var(--sans);color:var(--muted);margin:0 0 32px}}
.chap-toc{{display:grid;gap:2px;margin:24px 0 36px;font:15px var(--sans)}}.chap-toc a{{color:var(--text);text-decoration:none;padding:6px 0}}.chap-toc a:hover{{color:var(--accent-ink)}}.chap-toc span{{display:inline-block;width:3em;color:var(--faint)}}
.prose table{{display:block;overflow-x:auto}}.katex-display{{overflow-x:auto;overflow-y:hidden}}
{theory_css}
</style></head><body><main>{body}</main></body></html>'''
OUT.write_text(page, encoding='utf-8')
print(OUT, f'{len(page) / 1e6:.2f} MB', len(order), 'bài')
