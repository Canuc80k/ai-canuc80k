#!/usr/bin/env python3
"""Dựng mục Thực hành thành output/ui/practice-bank.js.

Nguồn: content/practice/catalog.py (TIERS, TASKS, LIVE). Bài trong LIVE đã lên LQDOJ; bài "link" trỏ tới nơi nộp gốc;
bài còn lại hiện "Sắp có". Công cụ cũng bảo đảm START_HERE.html nạp practice-bank.js.
Chạy trong thư mục course:  python -B -X utf8 tools/build_practice.py [--check]
--check chỉ kiểm, không ghi tệp; báo lỗi nếu practice-bank.js đang lệch nguồn.
"""
import importlib.util
import json
import sys
from pathlib import Path

COURSE = Path(__file__).resolve().parent.parent
SRC = COURSE / 'content' / 'practice' / 'catalog.py'
OUT = COURSE / 'output' / 'ui' / 'practice-bank.js'
HTML = COURSE / 'output' / 'START_HERE.html'
TAG = '<script defer src="ui/practice-bank.js"></script>'
LANES = {'co_san', 'bo_goc', 'tinh_lai', 'dung_lai', 'chia_lai', 'link'}


def load():
    spec = importlib.util.spec_from_file_location('practice_catalog', SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build():
    cat = load()
    seen, tiers = set(), []
    for tid, title, _ in cat.TIERS:
        tasks = []
        for k, (code, name, source, url, lane, chapters, _note) in enumerate(cat.TASKS[tid], 1):
            assert code == f'{tid}{k:02d}', f'mã {code} phải là {tid}{k:02d}'
            assert code not in seen and lane in LANES, code
            seen.add(code)
            item = {'code': code, 'name': name, 'source': source, 'chapters': sorted(chapters)}
            if lane == 'link':
                item.update(status='link', url=url)
            elif code in cat.LIVE:
                live = cat.LIVE[code]
                item.update(status='live', url=cat.LQDOJ + code)
                if live.get('data'):
                    item['data'] = live['data']
            else:
                item['status'] = 'soon'
            tasks.append(item)
        tiers.append({'id': tid, 'title': title, 'tasks': tasks})
    unknown = set(cat.LIVE) - seen
    assert not unknown, f'LIVE có mã lạ: {sorted(unknown)}'
    return 'window.PRACTICE_BANK = ' + json.dumps({'tiers': tiers}, ensure_ascii=False, separators=(',', ':')) + ';\n'


def main():
    text = build()
    html = HTML.read_text(encoding='utf-8')
    if '--check' in sys.argv:
        ok = OUT.exists() and OUT.read_text(encoding='utf-8') == text and TAG in html
        print('PASS: practice-bank.js khớp nguồn' if ok else 'FAIL: practice-bank.js lệch nguồn hoặc START_HERE.html chưa nạp')
        sys.exit(0 if ok else 1)
    OUT.write_text(text, encoding='utf-8')
    if TAG not in html:
        anchor = '<script defer src="ui/app.js"></script>'
        assert anchor in html
        HTML.write_text(html.replace(anchor, TAG + anchor), encoding='utf-8')
    data = json.loads(text[len('window.PRACTICE_BANK = '):-2])
    n = [len(t['tasks']) for t in data['tiers']]
    live = sum(x['status'] == 'live' for t in data['tiers'] for x in t['tasks'])
    print(f'Đã ghi {OUT.name}: {sum(n)} bài ({", ".join(f"{t["title"]} {len(t["tasks"])}" for t in data["tiers"])}), {live} bài đã lên LQDOJ')


if __name__ == '__main__':
    main()
