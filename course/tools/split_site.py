"""Tách dữ liệu website thành bản nhẹ cho trang chủ + từng gói theo bài, để trang mở nhanh.

theory.js (~23 MB), course-data.js (~6 MB) và code-examples.js (~1 MB) vẫn là bản gốc mà các công cụ
khác (rebuild_lesson, check_all_lessons, quiz_learn…) đọc và ghi. Lệnh này chỉ đọc chúng rồi ghi:

- ui/data/index.js  : COURSE_DATA rút gọn (không HTML bài tập), THEORY chỉ có mục lục + phần mở chương,
                      CODE_EXAMPLES chỉ có mục lục, và LESSON_LINKS (vòng học của từng bài).
- ui/data/l/<id>.js : toàn bộ dữ liệu một bài (lý thuyết, bài tập, code mẫu), app.js nạp khi mở bài.

Chạy lại sau mỗi lần dựng bài / dựng trắc nghiệm / dựng thực hành:
    python -B -X utf8 tools/split_site.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UI = ROOT / 'output' / 'ui'
REPO = 'Canuc80k/ai-canuc80k'
SITE_DIR = 'docs'  # thư mục chứa website trong repo GitHub


def load(name, prefix):
    s = (UI / name).read_text(encoding='utf-8')
    assert s.startswith(prefix), name
    return json.loads(s[len(prefix):].rstrip().rstrip(';'))


def dump(prefix, data):
    return prefix + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'


def main():
    course = load('course-data.js', 'window.COURSE_DATA = ')
    theory = load('theory.js', 'window.THEORY = ')
    examples = load('code-examples.js', 'window.CODE_EXAMPLES = ')
    quiz = load('quiz-bank.js', 'window.QUIZ_BANK = ')
    practice = load('practice-bank.js', 'window.PRACTICE_BANK = ')

    # Câu trắc nghiệm (bộ 6 mức, không tính kho ẩn) nhắc tới từng bài qua dòng "Ôn lại".
    quiz_by_lesson = {}
    for s in quiz['sets']:
        if s.get('hidden'):
            continue
        for q in s['questions']:
            for lid in {x[0] for x in q.get('learn') or []}:
                quiz_by_lesson[lid] = quiz_by_lesson.get(lid, 0) + 1

    # Đề thật (Thực hành) theo chương.
    practice_by_phase = {}
    for t in practice['tiers']:
        for x in t['tasks']:
            for ch in x.get('chapters', []):
                practice_by_phase.setdefault(ch, []).append(x['code'])

    # Đề thật luyện đúng từng bài (content/practice/lessons.json), giữ thứ tự Light -> Ultra.
    drill_map = json.loads((ROOT / 'content' / 'practice' / 'lessons.json').read_text(encoding='utf-8'))
    order = [x['code'] for t in practice['tiers'] for x in t['tasks']]
    unknown = [c for c in drill_map if c != '_' and c not in order]
    assert not unknown, f'lessons.json có mã không có trong Thực hành: {unknown}'
    drill_by_lesson = {}
    for code in order:
        for lid in drill_map.get(code, []):
            drill_by_lesson.setdefault(lid, []).append(code)

    out_dir = UI / 'data' / 'l'
    out_dir.mkdir(parents=True, exist_ok=True)
    keep = set()
    lite_lessons, links = [], {}
    for l in course['lessons']:
        lid = l['id']
        th = theory['lessons'].get(lid)
        ce = examples['lessons'].get(lid)
        chunk = {'id': lid, 'lesson': l, 'theory': th, 'examples': ce}
        name = f'{lid}.js'
        (out_dir / name).write_text(dump('window.__lessonChunk(', chunk).replace(';\n', ');\n'), encoding='utf-8')
        keep.add(name)

        lite = {k: v for k, v in l.items() if k not in ('parts', 'homework', 'code', 'codeOutput')}
        lite['homework'] = [{'title': h.get('title', '')} for h in l.get('homework') or []]
        lite['parts'] = [{'title': m.get('title', ''), 'homework': [{'title': h.get('title', '')} for h in m.get('homework') or []]}
                         for m in l.get('parts') or []]
        lite['hasCode'] = bool(l.get('code'))
        lite_lessons.append(lite)

        nb = l.get('notebook')
        nb_path = f'{SITE_DIR}/{nb}' if nb else None
        links[lid] = {
            'quiz': quiz_by_lesson.get(lid, 0),
            'homework': len(l.get('homework') or []) or sum(len(m.get('homework') or []) for m in l.get('parts') or []),
            'practice': practice_by_phase.get(l['phase'], []),
            'drill': drill_by_lesson.get(lid, []),
            'colab': f'https://colab.research.google.com/github/{REPO}/blob/main/{nb_path}' if nb_path else None,
            'kaggle': f'https://www.kaggle.com/kernels/welcome?src=https://github.com/{REPO}/blob/main/{nb_path}' if nb_path else None,
        }

    for old in out_dir.glob('*.js'):
        if old.name not in keep:
            old.unlink()

    cur = json.loads((ROOT / 'curriculum.json').read_text(encoding='utf-8'))
    results = {k['id']: k.get('result', '') for k in cur.get('courses', [])}
    lite_course = {**course, 'lessons': lite_lessons, 'courses': [{**k, 'result': k.get('result') or results.get(k['id'], '')} for k in course['courses']]}
    lite_theory = {'phases': theory['phases'],
                   'lessons': {k: {'headings': v['headings'], 'lazy': True} for k, v in theory['lessons'].items()}}
    lite_examples = {'version': examples.get('version'),
                     'lessons': {k: {'headings': v.get('headings', []), 'notebook': v.get('notebook'), 'codeFile': v.get('codeFile'), 'lazy': True}
                                 for k, v in examples['lessons'].items()}}
    inline = sum((v.get('html') or '').count('<div class="quiz"') + (v.get('html') or '').count('<div class="quiz ') for v in theory['lessons'].values())
    stats = {'lessons': sum(1 for l in course['lessons'] if l.get('kind') != 'checkpoint'),
             'checks': sum(1 for l in course['lessons'] if l.get('kind') == 'checkpoint'),
             'inline': inline,
             'bank': sum(len(s['questions']) for s in quiz['sets'] if not s.get('hidden')),
             'homework': sum(v['homework'] for v in links.values()),
             'practice': sum(len(t['tasks']) for t in practice['tiers'])}
    index = (dump('window.COURSE_DATA = ', lite_course) + dump('window.THEORY = ', lite_theory)
             + dump('window.CODE_EXAMPLES = ', lite_examples) + dump('window.LESSON_LINKS = ', links) + dump('window.SITE_STATS = ', stats))
    (UI / 'data' / 'index.js').write_text(index, encoding='utf-8')
    total = sum((out_dir / n).stat().st_size for n in keep)
    print(json.dumps({'stats': stats, 'index_kb': round(len(index.encode()) / 1024), 'chunks': len(keep), 'chunks_mb': round(total / 2**20, 1)}))


if __name__ == '__main__':
    main()
