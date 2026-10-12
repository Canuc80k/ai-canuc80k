"""Stage the new Code mẫu material without modifying the existing course."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, base64, hashlib, html, importlib.util, json, re, sys

WORK = Path(__file__).resolve().parent
PROJECT = WORK.parent.parent
COURSE = WORK.parent
OUT = COURSE / 'output'
STAGE = WORK / 'build/stage'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load_json_js(path, prefix):
    text = path.read_text(encoding='utf-8')
    assert text.startswith(prefix)
    return json.loads(text[len(prefix):].strip().removesuffix(';'))

spec = importlib.util.spec_from_file_location('example_controller', WORK / 'tools/run_examples.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
sys.path.insert(0, str(COURSE / 'tools'))
import render_theory as rt
import make_notebooks as nb

# Preserve long fences as well as ordinary three-backtick fences.
rt.FENCE = re.compile(r'(^(`{3,})[^\n]*\n.*?^\2[ \t]*$)', re.S | re.M)
IMAGE = re.compile(r'!\[([^\]]*)\]\((fig/[^)]+\.svg)\)')

def emit(relative, data):
    target = STAGE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {'path': relative, 'sha256': digest(data), 'bytes': len(data)}

def execution_proof(path):
    data = path.read_bytes()
    parsed = runner.parse_module(data)
    receipt_path = WORK / 'verification' / (path.stem + '.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    assert receipt['status'] == 'passed' and not receipt['issues'], 'execution not passed'
    by_id = {b['id']: b for b in receipt['blocks']}
    assert len(by_id) == len(parsed['blocks']), 'code block count changed'
    for block in parsed['blocks']:
        prior = by_id[block['id']]
        assert block['code_sha256'] == prior['code_sha256'], f"code changed at block {block['id']}"
        assert block['example'] == prior['example'] and block['example_block'] == prior['example_block'], 'example grouping changed'
        ast.parse(block['code'])
    suite = receipt.get('after_write_execution', receipt['initial_execution'])
    suite['block_outputs'] = {int(k): v for k, v in suite['block_outputs'].items()}
    assert suite['status'] == 'passed' and not suite['issues']
    assert not runner.output_issues(parsed, suite), 'output differs from actual execution'
    assert suite['whole_lesson']['status'] == 'passed'
    assert all(x['status'] == 'passed' for x in suite['isolated'])
    assert len(parsed['examples']) >= 2, 'need distinct examples'
    assert not re.search(r'^::: quiz', parsed['text'], re.M), 'quiz outside new code scope'
    for match in IMAGE.finditer(parsed['text']):
        assert (path.parent / match.group(2)).is_file(), 'missing generated figure'
    return parsed, receipt, suite

def adaptive_svg(fragment):
    # Only neutral ink in newly rendered figures adapts to the page theme.
    def adapt(match):
        svg = match.group()
        # Matplotlib's figure/axes/legend backing patches must not stay white
        # while their ink inherits the dark page's text color.
        def backing(group):
            return re.sub(r'(?i)fill:\s*#(?:ffffff|fff)(?![0-9a-f])', 'fill: none', group.group())
        svg = re.sub(r'<g id="patch_\d+">.*?</g>', backing, svg, flags=re.S)
        svg = re.sub(r'(?i)#(?:000000|1f1e1c|222222)(?![0-9a-f])', 'currentColor', svg)
        svg = svg.replace('<svg ', '<svg fill="currentColor" ', 1)
        width = re.search(r'\bwidth="([0-9.]+)pt"', svg)
        if width:
            cap = float(width.group(1)) * 4 / 3
            svg = svg.replace('<svg ', f'<svg style="max-width:min(100%,{cap:g}px);height:auto;margin-inline:auto" ', 1)
        return svg
    return re.sub(r'<svg\b.*?</svg>', adapt, fragment, flags=re.S)

def notebook(path, parsed, suite):
    text = parsed['text']
    cells, position = [], 0
    block_outputs = suite['block_outputs']
    image_count = 0
    def markdown(raw):
        nonlocal image_count
        attachments = {}
        def attach(m):
            nonlocal image_count
            name = f'figure-{image_count}.svg'
            image_count += 1
            attachments[name] = {'image/svg+xml': base64.b64encode((path.parent / m.group(2)).read_bytes()).decode('ascii')}
            return f'![{m.group(1)}](attachment:{name})'
        raw = IMAGE.sub(attach, raw)
        raw = nb.CONTAINER.sub(nb.container, raw).strip()
        if not raw:
            return
        cell = {'cell_type': 'markdown', 'metadata': {}, 'source': raw.replace('\r\n', '\n').splitlines(keepends=True)}
        if attachments:
            cell['attachments'] = attachments
        cells.append(cell)
    for block in parsed['blocks']:
        fence = block['fence']
        markdown(text[position:fence['start']])
        stdout = block_outputs[block['id']]['stdout'].replace('\r\n', '\n')
        code = block['code'].replace('\r\n', '\n').rstrip('\n')
        cells.append({'cell_type': 'code', 'execution_count': None, 'metadata': {},
                      'source': code.splitlines(keepends=True),
                      'outputs': [{'output_type': 'stream', 'name': 'stdout', 'text': stdout.splitlines(keepends=True)}] if stdout else []})
        position = block['output']['end'] if block['output'] else fence['end']
    markdown(text[position:])
    for i, cell in enumerate(cells):
        cell['id'] = digest(f'{path.stem}/{i}'.encode())[:12]
    book = {'cells': cells, 'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python'},
    }, 'nbformat': 4, 'nbformat_minor': 5}
    return book, image_count

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--partial', action='store_true', help='Stage only modules whose current execution proof is valid.')
    args = parser.parse_args()
    course = load_json_js(OUT / 'ui/course-data.js', 'window.COURSE_DATA = ')
    known = {item['id']: item for item in course['lessons']}
    payload = {'version': '2026-10-03-code-examples', 'lessons': {}}
    records, artifacts, pending = [], [], []
    candidates = sorted(p for p in (WORK / 'content').glob('phase-*/*.md') if re.fullmatch(r'phase-[0-9]', p.parent.name))
    assert all(p.stem in known or p.stem.startswith('controller-') for p in candidates), 'unknown lesson ID'
    sources = [p for p in candidates if p.stem in known]
    for path in sources:
        try:
            parsed, receipt, suite = execution_proof(path)
        except (AssertionError, FileNotFoundError, KeyError, ValueError) as ex:
            pending.append({'id': path.stem, 'reason': str(ex)})
            if args.partial:
                continue
            raise
        source_hash = digest(path.read_bytes())
        item = rt.render(path)
        item['html'] = adaptive_svg(item['html'])
        assert not re.search(r'href="(?!https?:|#|mailto:|data:image/)', item['html']), 'new examples need a planned local linked asset'
        assert not re.search(r'<script|javascript:', item['html'], re.I), 'unexpected executable markup'
        prefix = 'giao_trinh/code-examples'
        code_file = f'{prefix}/code/{path.stem}.py'
        notebook_file = f'{prefix}/notebook/{path.stem}.ipynb'
        source_file = f'{prefix}/source/{path.parent.name}/{path.name}'
        heading = '# -*- coding: utf-8 -*-\n# Code mẫu — ' + known[path.stem]['title'] + '\n'
        script = heading
        prior_example = None
        for block in parsed['blocks']:
            if block['example'] != prior_example:
                example = parsed['examples'][block['example'] - 1]
                script += '\n# Ví dụ ' + str(example['number']) + ': ' + example['title'] + '\n'
                prior_example = block['example']
            script += block['code'].replace('\r\n', '\n').rstrip('\n') + '\n\n'
        compile(script, code_file, 'exec')
        book, figures = notebook(path, parsed, suite)
        assert len([c for c in book['cells'] if c['cell_type'] == 'code']) == len(parsed['blocks'])
        artifacts += [emit(code_file, script.encode('utf-8')),
                      emit(notebook_file, json.dumps(book, ensure_ascii=False, indent=1).encode('utf-8')),
                      emit(source_file, path.read_bytes())]
        for match in IMAGE.finditer(parsed['text']):
            relative = f'{prefix}/source/{path.parent.name}/' + match.group(2)
            artifacts.append(emit(relative, (path.parent / match.group(2)).read_bytes()))
        payload['lessons'][path.stem] = {'html': item['html'], 'headings': item['headings'],
            'codeFile': code_file, 'notebook': notebook_file, 'sourceFile': source_file,
            'examples': len(parsed['examples'])}
        assert digest(path.read_bytes()) == source_hash, 'source changed while staging'
        records.append({'id': path.stem, 'phase': path.parent.name, 'source_sha256': source_hash,
                        'examples': len(parsed['examples']), 'python_blocks': len(parsed['blocks']),
                        'figures': figures, 'formulas': item['formulas'],
                        'execution_receipt_sha256': digest((WORK / 'verification' / (path.stem + '.json')).read_bytes()),
                        'code_sha256': digest(script.encode('utf-8')),
                        'notebook': notebook_file, 'codeFile': code_file,
                        'actual_stdout': {str(b['id']): suite['block_outputs'][b['id']]['stdout_sha256'] for b in parsed['blocks']}})
    missing = sorted(set(known) - set(payload['lessons']))
    if not args.partial:
        assert not missing, ('missing modules', missing)
        assert len(records) == 67
    artifacts.append(emit('ui/code-examples.js', ('window.CODE_EXAMPLES = ' + json.dumps(payload, ensure_ascii=False) + ';\n').encode('utf-8')))
    report = {'time_utc': datetime.now(timezone.utc).isoformat(), 'pass': True,
              'partial': args.partial, 'modules': len(records), 'missing': missing, 'pending': pending,
              'examples': sum(x['examples'] for x in records), 'python_blocks': sum(x['python_blocks'] for x in records),
              'figures': sum(x['figures'] for x in records), 'records': records,
              'artifacts': artifacts, 'stage': str(STAGE), 'original_course_written': False}
    (WORK / 'build/staging.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ['records', 'artifacts', 'pending']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
