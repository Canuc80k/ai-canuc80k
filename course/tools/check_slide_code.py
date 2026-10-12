"""Dò code trên slide lệch với code của bài học (không sửa gì).

python -B -X utf8 tools/check_slide_code.py [id ...]     (mặc định: mọi bài)

Mỗi dòng trong khối ```python của slide (bỏ chú thích, bỏ mọi khoảng trắng) phải là một đoạn con của code bài học
(các khối ```python của bài, cũng bỏ chú thích và khoảng trắng). Dòng chỉ gồm dấu ngoặc bị bỏ qua.
Khối ```py trong câu hỏi không được kiểm (code minh họa riêng của câu hỏi).
"""
import re
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / 'content'


def blocks(text, lang='python'):
    return re.findall(r'^```' + lang + r'[ \t]*\n(.*?)^```', text, re.M | re.S)


def strip_comment(line):
    out, quote = [], None
    for ch in line:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
        elif ch in '\'"':
            quote = ch
            out.append(ch)
        elif ch == '#':
            break
        else:
            out.append(ch)
    return ''.join(out)


def norm(s):
    return re.sub(r'\s+', '', s)


def check(lesson_path):
    slide_path = lesson_path.parent / 'slides' / lesson_path.name
    if not slide_path.exists():
        return []
    lesson_code = norm(''.join(strip_comment(l) for b in blocks(lesson_path.read_text(encoding='utf-8')) for l in b.split('\n')))
    out = []
    for b in blocks(slide_path.read_text(encoding='utf-8')):
        for line in b.split('\n'):
            piece = norm(strip_comment(line))
            piece = re.sub(r'^[)\]}]+', '', re.sub(r'[,(\[{\\]+$', '', piece))   # bẻ dòng: bỏ ngoặc/phẩy ở mép
            if len(piece) < 4 or re.fullmatch(r'[()\[\]{},:]+', piece):
                continue
            if piece not in lesson_code:
                out.append(f'{slide_path.relative_to(CONTENT)}: {line.strip()[:100]}')
    return out


def main(ids):
    files = [p for p in sorted(CONTENT.glob('phase-*/*.md')) if not p.name.startswith('_') and (not ids or p.stem in ids)]
    problems = [m for p in files for m in check(p)]
    print('\n'.join(problems))
    print(f'--- {len(files)} bài, {len(problems)} dòng code slide không thấy trong bài học')


if __name__ == '__main__':
    main(sys.argv[1:])
