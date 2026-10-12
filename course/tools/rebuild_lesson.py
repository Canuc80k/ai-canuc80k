"""Dựng lại một bài vào website, đúng logic từng bài của build/integrate.py.

python -B -X utf8 tools/rebuild_lesson.py 2.2 --check   # chỉ so, không ghi
python -B -X utf8 tools/rebuild_lesson.py 2.2           # ghi output của riêng bài này

Chỉ thay mục 2.2 trong theory.js/course-data.js; các bài khác phải giữ nguyên.
"""
from pathlib import Path
import hashlib, io, json, re, shutil, sys, tempfile, zipfile

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC / 'build'))
import integrate as ig  # noqa: E402  (main() không chạy khi import)

OUT, CONTENT = ig.OUT, ig.CONTENT
THEORY_PREFIX, COURSE_PREFIX = 'window.THEORY = ', 'window.COURSE_DATA = '


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dump(prefix, data, newline):
    return (prefix + json.dumps(data, ensure_ascii=False) + ';' + newline).encode('utf-8')


def newline_of(path):
    # course-data.js hiện kết thúc bằng CRLF, theory.js bằng LF; giữ đúng như tệp đang có.
    return '\r\n' if path.read_bytes().endswith(b'\r\n') else '\n'


HW_FILE_LABEL = {'.py': 'Code khởi đầu', '.ipynb': 'Notebook', '.in': 'Input mẫu', '.out': 'Output mẫu',
                 '.csv': 'Dữ liệu', '.zip': 'Dữ liệu'}
IO_PAIR = re.compile(r'<pre><code class="language-input">(.*?)</code></pre>\s*<pre><code class="language-output">(.*?)</code></pre>', re.S)


def build_homework(lesson_id, phase_dir, files):
    """Bài tập soạn mới: content/phase-N/homework/<id>/bai-K.md (+ bai-K.py, bai-K.in, bai-K.out, ...).
    Hướng dẫn soạn ở content/HOMEWORK.md. Tệp bắt đầu bằng '_' bị bỏ qua (bản nháp, mẫu)."""
    folder = phase_dir / 'homework' / lesson_id
    sources = sorted((p for p in folder.glob('bai-*.md') if re.fullmatch(r'bai-\d+', p.stem)),
                     key=lambda p: int(p.stem.split('-')[1])) if folder.is_dir() else []
    out_rel = f'giao_trinh/homework/{lesson_id}'
    tasks = []
    for k, md in enumerate(sources, 1):
        assert md.stem == f'bai-{k}', f'đánh số bài tập phải liên tục từ 1: {md.name}'
        text = md.read_text(encoding='utf-8')
        head = re.match(r'#\s+(.+)\n', text)
        assert head, f'{md}: dòng đầu phải là "# Tên bài"'
        html = ig.asset_links(ig.rt.md_to_html(text[head.end():], folder, md)[0], folder)
        # ```input + ```output liền nhau thành hai cột "Input mẫu / Output mẫu"; mục "Tự kiểm tra" thành checklist.
        html = IO_PAIR.sub(lambda m: f'<div class="hw-io"><div><p class="hw-io-label">Input mẫu</p><pre>{m.group(1)}</pre></div>'
                                     f'<div><p class="hw-io-label">Output mẫu</p><pre>{m.group(2)}</pre></div></div>', html)
        html = re.sub(r'(<h2>Tự kiểm tra</h2>\s*)<ul>', r'\1<ul class="hw-check">', html)
        downloads = [{'label': 'Đề bài', 'path': f'{out_rel}/{md.name}'}]
        files[f'{out_rel}/{md.name}'] = md.read_bytes()
        starter = starter_name = None
        order = list(HW_FILE_LABEL)  # Code khởi đầu, Notebook, Input mẫu, Output mẫu, Dữ liệu, rồi tệp khác
        for f in sorted(folder.glob(f'{md.stem}.*'), key=lambda f: (order.index(f.suffix) if f.suffix in order else len(order), f.name)):
            if f.suffix == '.md':
                continue
            files[f'{out_rel}/{f.name}'] = f.read_bytes()
            downloads.append({'label': HW_FILE_LABEL.get(f.suffix, 'Tệp kèm'), 'path': f'{out_rel}/{f.name}'})
            if f.suffix == '.py':
                starter, starter_name = f.read_text(encoding='utf-8'), f.name
        tasks.append({'number': k, 'title': head.group(1).strip(), 'html': html, 'files': downloads,
                      'folder': out_rel, 'starter': starter, 'starterFile': starter_name})
    return tasks


def recipe_zip(folder, copy_asset):
    """Gói recipes.zip của một chương, đúng cách integrate.py đóng (cùng thứ tự, tên và mtime tệp)."""
    sources = sorted(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    assert sources, f'{folder} không có tệp recipe'
    for p in sources:
        copy_asset(p)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sources:
            z.write(p, Path('recipes') / p.relative_to(folder))
    with zipfile.ZipFile(io.BytesIO(buf.getvalue())) as z:
        assert z.testzip() is None
    return f'giao_trinh/assets/{folder.parent.name}/recipes.zip', buf.getvalue()


def build(lesson_id, write):
    path = next(CONTENT.glob(f'phase-*/{lesson_id}.md'))
    text = path.read_text(encoding='utf-8')
    theory = ig.json_js(OUT / 'ui/theory.js', THEORY_PREFIX)
    course = ig.json_js(OUT / 'ui/course-data.js', COURSE_PREFIX)
    # Bản đọc vào phải dump lại đúng bytes, nếu không thì cách vá từng mục không an toàn.
    nl = {name: newline_of(OUT / 'ui' / name) for name in ['theory.js', 'course-data.js']}
    for name, prefix, data in [('theory.js', THEORY_PREFIX, theory), ('course-data.js', COURSE_PREFIX, course)]:
        assert dump(prefix, data, nl[name]) == (OUT / 'ui' / name).read_bytes(), f'{name} không dump lại đúng bytes'
    lesson = next(l for l in course['lessons'] if l['id'] == lesson_id)

    copied_assets = []
    real_copy = ig.copy_asset
    def copy_asset(source):
        target = OUT / 'giao_trinh/assets' / source.resolve().relative_to(CONTENT.resolve())
        copied_assets.append((source, target))
        return real_copy(source) if write else target.relative_to(OUT).as_posix()
    ig.copy_asset = copy_asset

    item = ig.rt.render(path)
    item['html'] = ig.asset_links(item['html'], path.parent)
    files = {}  # đường dẫn trong output -> bytes mới
    if 'recipes/' in text:
        # Như integrate.py: chép mọi tệp recipe của chương làm asset, đóng recipes.zip, thêm link tải cuối bài.
        url, data = recipe_zip(path.parent / 'recipes', copy_asset)
        files[url] = data
        item['html'] += f'<p><a href="{url}" download>Tải gói recipe của chương</a> — gồm các module phụ và hướng dẫn chuẩn bị asset.</p>'
    final = text.split('## Kiểm tra cuối bài', 1)[-1]
    assert len(re.findall(r'^::: quiz Câu \d+\s*$', final, re.M)) == 10, 'cần đúng 10 câu cuối bài'

    new_theory = json.loads(json.dumps(theory))
    new_theory['lessons'][lesson_id] = {'html': item['html'], 'headings': item['headings']}
    new_course = json.loads(json.dumps(course))
    new_lesson = next(l for l in new_course['lessons'] if l['id'] == lesson_id)
    new_lesson['theory'] = True

    files[f'giao_trinh/source/{path.parent.name}/{path.name}'] = path.read_bytes()
    found = ig.nb.FENCE.findall(text)
    codes = [v for kind, v in found if kind == 'python']
    outputs = [v for kind, v in found if kind == 'output']
    if codes:
        combined = '# -*- coding: utf-8 -*-\n# ' + new_lesson['title'] + ' — chạy các bước như notebook từ trên xuống.\n\n'
        combined += '\n\n'.join(f'# Bước {i}\n{v.rstrip()}' for i, v in enumerate(codes, 1)) + '\n'
        files[f'giao_trinh/code/{lesson_id}.py'] = combined.encode('utf-8')
        new_lesson.update(code=combined, codeOutput='\n\n'.join(v.rstrip() for v in outputs) + '\n',
                          codeFile=f'giao_trinh/code/{lesson_id}.py')
        book = ig.notebook_with_figures(path)
        files[f'giao_trinh/notebook/{lesson_id}.ipynb'] = json.dumps(book, ensure_ascii=False, indent=1).encode('utf-8')
        new_lesson['notebook'] = f'giao_trinh/notebook/{lesson_id}.ipynb'
    deck_source = path.parent / 'slides' / path.name
    with tempfile.TemporaryDirectory() as tmp:
        deck, n_slides = ig.rs.build(deck_source, Path(tmp))
        files[f'giao_trinh/slides/{lesson_id}.html'] = deck.read_bytes()
    new_lesson['deck'] = f'giao_trinh/slides/{lesson_id}.html'
    # PDF do tools/qa/make_pdfs.cjs dựng từ website; chỉ gắn nút khi tệp đã có.
    # Không dùng giao_trinh/slides/<id>.pdf: đó là PDF đời cũ chỉ để tham chiếu.
    for key, rel in [('deckPdf', f'giao_trinh/pdf/slide-{lesson_id}.pdf'), ('lessonPdf', f'giao_trinh/pdf/bai-{lesson_id}.pdf')]:
        if (OUT / rel).is_file():
            new_lesson[key] = rel
        else:
            new_lesson.pop(key, None)
    homework = build_homework(lesson_id, path.parent, files)
    if homework:
        new_lesson['homework'] = homework
    else:
        new_lesson.pop('homework', None)
    files['ui/theory.js'] = dump(THEORY_PREFIX, new_theory, nl['theory.js'])
    files['ui/course-data.js'] = dump(COURSE_PREFIX, new_course, nl['course-data.js'])

    # Các bài khác không được đổi.
    others_same = all(new_theory['lessons'][k] == v for k, v in theory['lessons'].items() if k != lesson_id)
    others_same &= new_theory['phases'] == theory['phases']
    others_same &= [l for l in new_course['lessons'] if l['id'] != lesson_id] == [l for l in course['lessons'] if l['id'] != lesson_id]
    others_same &= {k: v for k, v in new_course.items() if k != 'lessons'} == {k: v for k, v in course.items() if k != 'lessons'}
    assert others_same, 'bài khác bị đổi'

    report = {'lesson': lesson_id, 'slides': n_slides, 'code_blocks': len(codes),
              'quizzes': text.count('::: quiz'), 'figures': len(ig.rt.FIGURE.findall(text)),
              'formulas': item['formulas'], 'words': len(text.split()), 'files': {}}
    for rel, data in files.items():
        old = (OUT / rel).read_bytes() if (OUT / rel).is_file() else None
        if rel.startswith('giao_trinh/code/') and old is not None and b'\r\n' in old:
            data = data.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')   # integrate.py ghi code bằng write_text trên Windows
        report['files'][rel] = {'changed': old != data, 'sha256': sha(data)}
        if write and old != data:
            (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
            (OUT / rel).write_bytes(data)
    for source, target in copied_assets:
        same = target.is_file() and target.read_bytes() == source.read_bytes()
        report['files'][target.relative_to(OUT).as_posix()] = {'changed': not same, 'sha256': sha(source.read_bytes())}
    ig.copy_asset = real_copy
    return report


if __name__ == '__main__':
    lesson_id, write = sys.argv[1], '--check' not in sys.argv
    print(json.dumps(build(lesson_id, write), ensure_ascii=False, indent=1))
