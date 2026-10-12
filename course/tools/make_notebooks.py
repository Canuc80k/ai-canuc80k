"""Xuất mỗi bài lý thuyết có code thành notebook (.ipynb) để học sinh mở trên Colab/Kaggle và chạy cùng.

- Văn bản thành ô Markdown (giữ công thức $...$), khối ```python thành ô code, khối ```output thành kết quả mẫu.
- Câu hỏi nhanh thành câu hỏi kèm đáp án gấp lại; hình SVG bỏ đi (notebook không mở được tệp cục bộ).

Chạy: python make_notebooks.py <thư-mục-content> <thư-mục-ra>
"""
import json, re, sys
from pathlib import Path

CONTENT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'content'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / 'notebooks'
FENCE = re.compile(r'^```(python|output)[ \t]*\n(.*?)^```[ \t]*$\n?', re.S | re.M)
CONTAINER = re.compile(r'^:::[ \t]*(\w+)[ \t]*(.*?)\n(.*?)^:::[ \t]*$', re.S | re.M)
OPTION = re.compile(r'^- \[( |x)\] (.*)$')
TITLES = {'goal': 'Mục tiêu', 'trap': 'Bẫy', 'tip': 'Mẹo', 'note': 'Ghi chú'}


def container(m):
    kind, title, body = m.group(1), m.group(2).strip(), m.group(3).strip('\n')
    if kind == 'quiz':
        lines = body.split('\n')
        opt = [i for i, l in enumerate(lines) if OPTION.match(l)]
        q = '\n'.join(lines[:opt[0]]).strip()
        why = '\n'.join(lines[opt[-1] + 1:]).strip()
        opts, ans = [], ''
        for k, i in enumerate(opt):
            mark, label = OPTION.match(lines[i]).groups()
            opts.append(f'{"ABCDEF"[k]}. {label}')
            if mark == 'x':
                ans = f'{"ABCDEF"[k]}. {label}'
        return (f'**{title or "Hỏi nhanh"}.** {q}\n\n' + '\n'.join(f'- {o}' for o in opts) +
                f'\n\n<details><summary>Đáp án</summary>\n\n{ans}\n\n{why}\n\n</details>')
    quoted = '\n'.join('> ' + l if l else '>' for l in body.split('\n'))
    return f'> **{title or TITLES.get(kind, kind)}**\n>\n{quoted}'


def md_cell(text):
    text = re.sub(r'^!\[[^\]]*\]\([^)]+\)\s*$', '', text, flags=re.M)
    text = CONTAINER.sub(container, text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return {'cell_type': 'markdown', 'metadata': {}, 'source': text.splitlines(keepends=True)} if text else None


def notebook(path):
    text = path.read_text(encoding='utf-8')
    cells, pos = [], 0
    for m in FENCE.finditer(text):
        between = text[pos:m.start()]
        if m.group(1) == 'output' and between.strip() == '' and cells and cells[-1]['cell_type'] == 'code':
            cells[-1]['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': m.group(2).splitlines(keepends=True)}]
        else:
            c = md_cell(between)
            if c:
                cells.append(c)
            if m.group(1) == 'python':
                cells.append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [],
                              'source': m.group(2).rstrip('\n').splitlines(keepends=True)})
        pos = m.end()
    c = md_cell(text[pos:])
    if c:
        cells.append(c)
    return {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                                         'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 5}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for path in sorted(CONTENT.glob('phase-*/*.md')):
        if path.stem.startswith('_') or '```python' not in path.read_text(encoding='utf-8'):
            continue
        nb = notebook(path)
        (OUT / f'{path.stem}.ipynb').write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
        made.append(path.stem)
    print('notebook:', ' '.join(made))


if __name__ == '__main__':
    main()
