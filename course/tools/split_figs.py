"""Tìm và tách slide 'split' có hình nằm trong một cột (hình bị co nhỏ còn nửa trang).

python -B -X utf8 tools/split_figs.py list [id ...]        liệt kê (mặc định mọi bài)
python -B -X utf8 tools/split_figs.py fix <id> [số trang ...]  tách: trang hình riêng (<!-- figure -->, cùng tiêu đề)
                                                             đặt ngay sau trang chữ; trang chữ bỏ cột hình.
Trang chữ còn một cột thì bỏ luôn '<!-- split -->' và '|||'. Số trang tính như shot_slides (đếm '---' + 1).
"""
import re
import sys
from pathlib import Path

C = Path(__file__).resolve().parents[1] / 'content'
FIG = re.compile(r'^!\[[^\]]*\]\(\.\./fig/[^)]+\.svg\)\s*$', re.M)


def deck(lesson):
    return next(C.glob(f'phase-*/slides/{lesson}.md'))


def slides(text):
    return text.split('\n---\n')


def is_split_fig(s):
    return '<!-- split -->' in s and FIG.search(s)


def fix_one(s):
    head = re.search(r'^## .+$', s, re.M).group(0)
    figs = FIG.findall(s)
    body = FIG.sub('', s)
    cols = body.split('|||')
    nonempty = [c for c in cols if re.sub(r'<!--.*?-->|^## .+$', '', c, flags=re.M | re.S).strip()]
    if len(nonempty) <= 1:
        body = body.replace('<!-- split -->\n', '').replace('\n|||\n', '\n')
    body = re.sub(r'\n{3,}', '\n\n', body).rstrip() + '\n'
    fig_slide = '\n<!-- figure -->\n' + head + '\n\n' + '\n\n'.join(f.strip() for f in figs) + '\n'
    return [body, fig_slide]


def main():
    cmd, *rest = sys.argv[1:]
    if cmd == 'list':
        ids = rest or sorted(p.stem for p in C.glob('phase-*/slides/*.md'))
        total = 0
        for i in ids:
            parts = slides(deck(i).read_text(encoding='utf-8'))
            hits = [k + 1 for k, s in enumerate(parts) if is_split_fig(s)]
            if hits:
                total += len(hits)
                print(i, hits)
        print('tổng', total)
    elif cmd == 'fix':
        lesson, *pages = rest
        p = deck(lesson)
        parts = slides(p.read_text(encoding='utf-8'))
        want = {int(x) for x in pages} if pages else {k + 1 for k, s in enumerate(parts) if is_split_fig(s)}
        out = []
        for k, s in enumerate(parts):
            if k + 1 in want and is_split_fig(s):
                out.extend(fix_one(s))
            else:
                out.append(s)
        p.write_text('\n---\n'.join(out), encoding='utf-8')
        print(lesson, 'tách', len(want), 'trang')


if __name__ == '__main__':
    main()
