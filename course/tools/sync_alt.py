"""Đồng bộ chú thích hình: alt text trong bài và slide lấy đúng <title> của SVG (một nguồn duy nhất cho caption).

python -B -X utf8 tools/sync_alt.py 0-1-notebook 0-2-image ...     (tên hình)
python -B -X utf8 tools/sync_alt.py --prefix 0-                     (mọi hình bắt đầu bằng 0-)
Chỉ đổi những chỗ đang dẫn hình đó; in số chỗ đã đổi.
"""
import html
import re
import sys
from pathlib import Path

C = Path(__file__).resolve().parents[1] / 'content'
args = sys.argv[1:]
if args and args[0] == '--prefix':
    names = sorted(p.stem for p in C.glob(f'phase-*/fig/{args[1]}*.svg'))
else:
    names = args
titles = {}
for n in names:
    p = next(C.glob(f'phase-*/fig/{n}.svg'))
    m = re.search(r'<title>(.*?)</title>', p.read_text(encoding='utf-8'), re.S)
    if not m:                      # hình matplotlib cũ không có <title>: giữ chú thích đang có
        print('bỏ qua (không có title):', n)
        continue
    t = html.unescape(m.group(1)).strip()
    assert '[' not in t and ']' not in t, (n, t)
    titles[n] = t
total = 0
for md in sorted(C.glob('phase-*/**/*.md')):
    text = md.read_text(encoding='utf-8')
    new = text
    for n, t in titles.items():
        new = re.sub(r'!\[[^\]]*\]\(((?:\.\./)?fig/' + re.escape(n) + r'\.svg)\)', lambda m: f'![{t}]({m.group(1)})', new)
    if new != text:
        k = sum(1 for a, b in zip(text.splitlines(), new.splitlines()) if a != b)
        total += k
        md.write_text(new, encoding='utf-8')
        print(md.relative_to(C).as_posix(), k)
print('đổi', total, 'chỗ')
