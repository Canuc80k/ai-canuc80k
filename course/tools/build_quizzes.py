#!/usr/bin/env python3
"""Dựng mục Trắc nghiệm thành output/ui/quiz-bank.js.

Nguồn: content/quizzes/<bộ>.py (light…, medium…, high…, extra…, max…, ultra…), mỗi tệp có GROUPS = {mã nhóm: [câu, ...]}.
Bộ có 'pool' trỏ tới một kho ẩn ('hidden'): kho không hiện để luyện, chế độ kiểm tra bốc câu từ cả bộ lẫn kho.
Tệp bắt đầu bằng '_' là tệp phụ (nguồn gộp, danh sách chọn), không phải bộ câu hỏi.
Một câu là tuple (khái niệm, câu hỏi, đáp án đúng, [ba phương án nhiễu], lời giải[, nguồn])
hoặc dict cùng các khóa topic, q, a, d, why, thêm code (đoạn Python hiện dưới câu hỏi) và src.
Nguồn là (loại, nhãn, url); url có thể rỗng khi đề gốc không có bản công khai.
Mỗi câu còn được nối với các mục lý thuyết cần học (content/quizzes/learn.json, xem tools/quiz_learn.py);
câu chưa nối, hay câu cần đọc không còn trên trang bài, làm lệnh dừng, trừ khi thêm --allow-missing lúc đang gán dở.
Chạy trong thư mục course:  python -B -X utf8 tools/build_quizzes.py [--check] [--allow-missing]
--check chỉ kiểm, không ghi tệp; báo lỗi nếu quiz-bank.js đang lệch nguồn.
"""
import importlib.util
import json
import random
import sys
from collections import Counter
from pathlib import Path

import quiz_learn

COURSE = Path(__file__).resolve().parent.parent
SRC = COURSE / 'content' / 'quizzes'
OUT = COURSE / 'output' / 'ui' / 'quiz-bank.js'

INTRO = [('ml', 'Học máy và dữ liệu', 35), ('deep', 'Mạng nơ-ron và học sâu', 15), ('cv', 'Thị giác máy tính', 25),
         ('nlp', 'Ngôn ngữ tự nhiên', 20), ('audio', 'Âm thanh', 5)]
EXAM = [('ml', 'Học máy và dữ liệu', 25), ('deep', 'Học sâu và huấn luyện', 25), ('cv', 'Thị giác máy tính', 20),
        ('nlp', 'Ngôn ngữ và mô hình ngôn ngữ lớn', 20), ('gen', 'Mô hình sinh và đa phương thức', 10)]
SETS = [
    {'id': 'light', 'title': 'Light', 'prefix': 'L', 'seed': 20261008, 'groups': INTRO},
    {'id': 'light2', 'title': 'Light 2', 'prefix': 'LB', 'seed': 20261014, 'groups': INTRO},
    {'id': 'light3', 'title': 'Light 3', 'prefix': 'LC', 'seed': 20261015, 'groups': INTRO},
    {'id': 'light4', 'title': 'Light 4', 'prefix': 'LD', 'seed': 20261016, 'groups': INTRO},
    {'id': 'light5', 'title': 'Light 5', 'prefix': 'LE', 'seed': 20261017, 'groups': INTRO},
    {'id': 'medium', 'title': 'Medium', 'prefix': 'M', 'seed': 20261009, 'groups': INTRO},
    {'id': 'medium2', 'title': 'Medium 2', 'prefix': 'MB', 'seed': 20261018, 'groups': INTRO},
    {'id': 'medium3', 'title': 'Medium 3', 'prefix': 'MC', 'seed': 20261019, 'groups': INTRO},
    {'id': 'high', 'title': 'High', 'prefix': 'H', 'seed': 20261010, 'groups': EXAM},
    {'id': 'high2', 'title': 'High 2', 'prefix': 'HB', 'seed': 20261020, 'groups': EXAM},
    {'id': 'extra', 'title': 'Extra', 'prefix': 'E', 'seed': 20261011, 'groups': EXAM},
    {'id': 'extra2', 'title': 'Extra 2', 'prefix': 'EB', 'seed': 20261021, 'groups': EXAM},
    {'id': 'max', 'title': 'Max', 'prefix': 'MXC', 'seed': 20261024, 'groups': EXAM, 'pool': 'max_kho'},
    {'id': 'max_kho', 'title': 'Max', 'prefix': 'MXK', 'seed': 20261025, 'groups': EXAM, 'hidden': True},
    {'id': 'ultra', 'title': 'Ultra', 'prefix': 'UC', 'seed': 20261026, 'groups': EXAM, 'pool': 'ultra_kho'},
    {'id': 'ultra_kho', 'title': 'Ultra', 'prefix': 'UK', 'seed': 20261027, 'groups': EXAM, 'hidden': True},
]
SOURCE_KINDS = {'Đề thi', 'Phỏng theo'}
LEARN, TARGETS, MISSING, STALE = quiz_learn.read_learn(), quiz_learn.targets(), [], []


def load(name):
    spec = importlib.util.spec_from_file_location(f'quiz_{name}', SRC / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.GROUPS


def normalize(card):
    if isinstance(card, dict):
        assert set(card) <= {'topic', 'q', 'a', 'd', 'why', 'code', 'src'}, set(card)
        return card
    assert len(card) in (5, 6), card[1]
    out = dict(zip(['topic', 'q', 'a', 'd', 'why'], card[:5]))
    if len(card) == 6:
        out['src'] = card[5]
    return out


def build_set(meta):
    cards, groups = load(meta['id']), meta['groups']
    assert list(cards) == [g for g, _, _ in groups], f"{meta['id']}: thứ tự nhóm phải là {[g for g, _, _ in groups]}"
    total = sum(n for _, _, n in groups)
    assert total % 4 == 0
    positions = [p for p in range(4) for _ in range(total // 4)]
    random.Random(meta['seed']).shuffle(positions)
    questions, seen = [], set()
    for gid, _, expected in groups:
        assert len(cards[gid]) == expected, f"{meta['id']}/{gid}: cần {expected} câu, có {len(cards[gid])}"
        for raw in cards[gid]:
            c = normalize(raw)
            texts = [c['topic'], c['q'], c['a'], *c['d'], c['why']]
            key = (c['q'], c.get('code', ''))
            assert key not in seen, f"trùng câu hỏi: {c['q']}"
            seen.add(key)
            assert len(c['d']) == 3 and len({c['a'], *c['d']}) == 4, f"cần 4 phương án khác nhau: {c['q']}"
            assert all(isinstance(s, str) and s and s.strip() == s for s in texts), f"khoảng trắng thừa: {c['q']}"
            assert all(s.count('`') % 2 == 0 for s in texts), f"dấu ` lẻ: {c['q']}"
            pos = positions[len(questions)]
            item = {'id': f"{meta['prefix']}{len(questions) + 1:03d}", 'group': gid, 'topic': c['topic'], 'q': c['q'],
                    'options': c['d'][:pos] + [c['a']] + c['d'][pos:], 'answer': pos, 'why': c['why']}
            if c.get('code'):
                item['code'] = c['code'].strip('\n')
            if c.get('src'):
                kind, label, url = c['src']
                assert kind in SOURCE_KINDS and label and (url == '' or url.startswith('https://')), c['src']
                item['src'] = {'kind': kind, 'label': label, **({'url': url} if url else {})}
            entry = LEARN.get(quiz_learn.fingerprint(c))
            if entry is None:
                MISSING.append(f"{meta['id']}/{item['id']}")
            elif entry['to']:
                # [id bài, vị trí <h2> trên trang, tên mục, [câu cần đọc]]; tên mục bỏ dấu $ của công thức.
                # Câu cần đọc là chữ đúng như trên trang (quiz_learn.learn_text); app.js tìm và tô sáng.
                item['learn'] = [[lid, TARGETS[(lid, h)][0], h.replace('$', '')] + ([spots[0]] if spots and spots[0] else [])
                                 for lid, h, *spots in entry['to']]
                STALE.extend(f"{meta['id']}/{item['id']} → {lid} · {h}" for lid, h, *spots in entry['to'] for quote in (spots[0] if spots else [])
                             if not any(quote in t for t in quiz_learn.section_paras(lid, h)))
            questions.append(item)
    extra = {k: meta[k] for k in ('pool', 'hidden') if k in meta}
    return {'id': meta['id'], 'title': meta['title'], **extra,
            'groups': [{'id': gid, 'name': name, 'count': n} for gid, name, n in groups], 'questions': questions}


def main():
    present = [m for m in SETS if (SRC / f"{m['id']}.py").exists()]
    bank = {'sets': [build_set(meta) for meta in present]}
    for s in bank['sets']:
        qs = s['questions']
        strict = sum(len(q['options'][q['answer']]) > max(len(o) for i, o in enumerate(q['options']) if i != q['answer']) for q in qs)
        sources = Counter(q['src']['kind'] for q in qs if 'src' in q)
        print(f"{s['title']}: {len(qs)} câu, vị trí {dict(sorted(Counter(q['answer'] for q in qs).items()))}, "
              f"đáp án dài hẳn nhất {strict}, có code {sum('code' in q for q in qs)}, nguồn {dict(sources)}")
    if STALE:
        # bài đã dựng lại và câu cần đọc đổi chữ: trang bài không tô được câu đó
        msg = (f'{len(STALE)} câu cần đọc không còn trên trang bài ({"; ".join(STALE[:4])}…): '
               'chạy tools/quiz_learn.py check, chọn lại bằng spots/section rồi mark')
        if '--allow-missing' not in sys.argv:
            sys.exit(msg)
        print('CẢNH BÁO: ' + msg)
    if MISSING:
        msg = (f'{len(MISSING)} câu chưa nối với mục lý thuyết ({", ".join(MISSING[:8])}…): '
               'chạy tools/quiz_learn.py carry hoặc cands <bộ> --todo rồi ingest')
        if '--allow-missing' not in sys.argv:
            sys.exit(msg)
        print('CẢNH BÁO: ' + msg)
    text = 'window.QUIZ_BANK = ' + json.dumps(bank, ensure_ascii=False, separators=(',', ':')) + ';\n'
    if '--check' in sys.argv:
        current = OUT.read_text(encoding='utf-8') if OUT.exists() else ''
        if current != text:
            sys.exit(f'LỆCH: {OUT.relative_to(COURSE)} chưa khớp nguồn, chạy lại không có --check')
        print('PASS: quiz-bank.js khớp nguồn')
        return
    OUT.write_text(text, encoding='utf-8', newline='\n')
    print(f'Đã ghi {OUT.relative_to(COURSE)} ({len(text.encode())} byte)')


if __name__ == '__main__':
    main()
