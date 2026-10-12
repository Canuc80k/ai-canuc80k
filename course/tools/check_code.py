"""Chạy code trong bài lý thuyết như một notebook và đối chiếu với các khối ```output.

- Mọi khối ```python trong một bài chạy nối tiếp, dùng chung biến (giống chạy lần lượt các ô trên Colab).
- Khối ```output ngay sau một khối python là kết quả in ra của khối đó.

Chạy:
  python check_code.py content/phase-2/2.1.md            # kiểm: báo khối nào in ra khác bài
  python check_code.py content/phase-2/2.1.md --write    # ghi lại các khối output theo kết quả thật
"""
import contextlib, io, re, sys, warnings
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

BLOCK = re.compile(r'^```(python|output)[ \t]*\n(.*?)^```[ \t]*$\n?', re.S | re.M)


def blocks(text):
    return [(m.group(1), m.group(2), m.start(), m.end()) for m in BLOCK.finditer(text)]


def run(path, write=False):
    text = Path(path).read_text(encoding='utf-8')
    found = blocks(text)
    env = {'__name__': '__main__'}
    edits, bad, ran = [], [], 0
    for i, (kind, code, start, end) in enumerate(found):
        if kind != 'python':
            continue
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter('ignore')
            exec(compile(code, f'{path}#khối{ran + 1}', 'exec'), env)
        ran += 1
        got = buf.getvalue().rstrip('\n')
        nxt = found[i + 1] if i + 1 < len(found) else None
        has_out = nxt and nxt[0] == 'output' and text[end:nxt[2]].strip() == ''
        if has_out:
            if nxt[1].rstrip('\n') != got:
                bad.append((ran, nxt[1].rstrip('\n'), got))
                edits.append((nxt[2], nxt[3], f'```output\n{got}\n```\n' if got else ''))
        elif got:
            bad.append((ran, '(chưa có khối output)', got))
            edits.append((end, end, f'\n```output\n{got}\n```\n'))
    if write and edits:
        for s, e, new in sorted(edits, reverse=True):
            text = text[:s] + new + text[e:]
        Path(path).write_text(text, encoding='utf-8')
    for n, want, got in bad:
        print(f'--- khối {n}: trong bài\n{want}\n--- chạy thật\n{got}\n')
    print(f'{path}: {ran} khối code, {len(bad)} khối output {"đã ghi lại" if write else "khác"}')
    return not bad or write


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    ok = all([run(p, '--write' in sys.argv) for p in args])
    sys.exit(0 if ok else 1)
