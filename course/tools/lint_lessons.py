"""Soát lỗi hình thức lặp lại trong bài học và slide (không sửa gì).

python -B -X utf8 tools/lint_lessons.py [id ...]     (mặc định: mọi bài)

Báo: câu hỏi không đúng 4 phương án (câu 'Đề thi' được giữ 5 như đề gốc) hoặc không đúng 1 đáp án; chữ 'demo' và vài từ cần tránh trong lời giảng
(ngoài khối code); dòng chữ thụt một dấu cách ở slide; hai đoạn slide chỉ gồm $...$ liền nhau; ký tự điều khiển lạ.
"""
import re
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / 'content'
AVOID = [
    (r'\bdemo\b', 'demo'),
    (r'hậu nghiệm', 'hậu nghiệm'),
    (r'\b(các em|em hãy|bạn hãy|thầy|cô giáo)\b', 'xưng hô'),
    (r'## Ví dụ tay\b', 'Ví dụ tay'),
    (r'\blượt soạn\b|\bngười soạn\b', 'giọng người soạn'),
]


def prose_lines(text):
    """(số dòng, dòng) ngoài khối ``` ."""
    inside = False
    for i, line in enumerate(text.split('\n'), 1):
        if line.startswith('```'):
            inside = not inside
            continue
        if not inside:
            yield i, line


def quizzes(text):
    for m in re.finditer(r'^::: quiz[^\n]*\n(.*?)^:::$', text, re.M | re.S):
        body = m.group(1)
        opts = re.findall(r'^- \[( |x)\] ', body, re.M)
        line = text.count('\n', 0, m.start()) + 1
        yield line, len(opts), opts.count('x'), 'Đề thi:' in body


def check(path):
    text = path.read_text(encoding='utf-8')
    rel = path.relative_to(CONTENT)
    out = []
    for line, n, right, exam in quizzes(text):
        if right != 1 or not (n == 4 or (exam and n == 5)):   # câu 'Đề thi' giữ 5 phương án như đề gốc
            out.append(f'{rel}:{line}: quiz {n} phương án, {right} đáp án')
    is_slide = 'slides' in path.parts
    for i, line in prose_lines(text):
        plain = re.sub(r'`[^`]*`', '', line)            # bỏ tên biến, đoạn code trong dòng
        bare = re.sub(r'\$[^$]*\$|!\[[^\]]*\]\([^)]*\)', '', plain)   # bỏ LaTeX và chú thích hình
        bare = re.sub(r'\b(d|c|k)?m²|\bR²(?![=−-])', '', bare)        # đơn vị diện tích, tên R² đứng riêng
        if re.search(r'[₀-₉²³ⁿ]', bare):
            out.append(f'{rel}:{i}: công thức bằng ký tự Unicode (nên dùng LaTeX): {line.strip()[:80]}')
        for pat, name in AVOID:
            if re.search(pat, plain, re.I):
                out.append(f'{rel}:{i}: {name}: {line.strip()[:90]}')
        if is_slide and re.fullmatch(r'\$[^$]+\$[.,]?', line.strip()) and re.search(r'\\(frac|sum|sqrt|int)', line):
            out.append(f'{rel}:{i}: công thức đứng riêng dòng nên dùng $$ (inline bị thu nhỏ): {line.strip()[:70]}')
        if is_slide and re.match(r'^ [^ \-*]', line):
            out.append(f'{rel}:{i}: thụt một dấu cách: {line[:60]}')
        if re.search(r'[\x00-\x08\x0b-\x1f]', line):
            out.append(f'{rel}:{i}: ký tự điều khiển')
    for i, line in enumerate(text.split('\n'), 1):
        # Chú thích hình chứa dấu ngoặc vuông làm bộ dựng không nhận ra hình (trang tải fig/... và báo 404).
        if line.startswith('![') and '.svg)' in line and not re.fullmatch(r'!\[[^\]]*\]\([^)]+\.svg\)\s*', line):
            out.append(f'{rel}:{i}: chú thích hình chứa dấu ngoặc vuông: {line[:70]}')
    if is_slide:
        # Đoạn chỉ gồm đúng một $...$ được dựng không có <p>; hai đoạn như vậy liền nhau hiện thành một dòng.
        lines = text.split('\n')
        alone = lambda s: re.fullmatch(r'\$[^$]+\$', s.strip()) is not None
        for i in range(len(lines) - 2):
            if alone(lines[i]) and not lines[i + 1].strip() and alone(lines[i + 2]):
                out.append(f'{rel}:{i + 1}: hai đoạn chỉ có $...$ liền nhau sẽ dính một dòng (dùng $$ hoặc aligned)')
    return out


def main(ids):
    files = []
    for p in sorted(CONTENT.glob('phase-*/*.md')) + sorted(CONTENT.glob('phase-*/slides/*.md')):
        if ids and p.stem not in ids:
            continue
        files.append(p)
    problems = [msg for p in files for msg in check(p)]
    print('\n'.join(problems))
    print(f'--- {len(files)} tệp, {len(problems)} chỗ cần xem')


if __name__ == '__main__':
    main(sys.argv[1:])
