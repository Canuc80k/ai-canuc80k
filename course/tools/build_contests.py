"""Dựng mục "Các cuộc thi" của website từ content/contests/.

python -B -X utf8 tools/build_contests.py          # ghi output/ui/contests.js
python -B -X utf8 tools/build_contests.py --check  # chỉ kiểm, không ghi

Nguồn:
- content/contests/contests.json: danh sách cuộc thi theo thứ tự hiện, mỗi mục có id, tên, tên ngắn, cấp, một câu
  tóm tắt, trang chính thức, dòng "kỳ tới", và bảng so sánh (`compare`: các cột của bảng tổng).
- content/contests/<id>.md: trang riêng của từng cuộc thi, Markdown như bài học (bảng, link, khối :::).
  Dòng đầu là "# Tên"; các mục `##` thành mục lục bên phải.
Link tới bài học viết `[Bài 1.3](#/lesson/1.3)`, tới Thực hành `[...](#/practice/bai/1.5)`, tới trắc nghiệm `[...](#/quiz/...)`.
"""
import json, re, sys
from pathlib import Path

C = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C / 'build'))
import integrate as ig  # noqa: E402

SRC = C / 'content' / 'contests'
OUT = C / 'output' / 'ui' / 'contests.js'


def build():
    meta = json.loads((SRC / 'contests.json').read_text(encoding='utf-8'))
    pages, problems = {}, []
    for c in meta['contests']:
        path = SRC / f"{c['id']}.md"
        text = path.read_text(encoding='utf-8')
        head = re.match(r'#\s+(.+)\n', text)
        if not head:
            problems.append(f'{path.name}: dòng đầu phải là "# Tên"')
            continue
        html, *_ = ig.rt.md_to_html(text[head.end():], SRC, path)
        # Link nội bộ (#/...) mở trong trang; link ngoài mở tab mới.
        html = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', html)
        heads = re.findall(r'^## (.+)$', text, re.M)
        pages[c['id']] = {'html': html, 'headings': heads}
        for lid in re.findall(r'\(#/lesson/([\d.]+|kt\d)\)', text):
            if not list((C / 'content').glob(f'phase-*/{lid}.md')):
                problems.append(f'{path.name}: link tới bài không có: {lid}')
    data = {'intro': meta.get('intro', ''), 'columns': meta.get('columns', []), 'contests': meta['contests'], 'pages': pages}
    return data, problems


if __name__ == '__main__':
    data, problems = build()
    if problems:
        sys.exit('\n'.join(problems))
    js = 'window.CONTESTS = ' + json.dumps(data, ensure_ascii=False) + ';\n'
    if '--check' not in sys.argv:
        OUT.write_text(js, encoding='utf-8', newline='\n')
    print(json.dumps({'contests': [c['id'] for c in data['contests']], 'kb': round(len(js.encode()) / 1024)}, ensure_ascii=False))
