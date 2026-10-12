#!/usr/bin/env python3
"""Tìm câu trùng hoặc gần trùng giữa các bộ trắc nghiệm.

Chạy trong thư mục course:  python -B -X utf8 tools/quiz_overlap.py <bộ> [--all] [--ratio 0.6]
So mỗi câu của <bộ> với mọi câu của các bộ khác (và trong chính nó): báo khái niệm trùng tên,
câu hỏi giống nhau theo tỉ lệ ký tự (difflib) và đề thi gốc dùng lại (cùng nhãn nguồn).
--all in cả khái niệm trùng tên; mặc định chỉ in khi câu hỏi cũng giống nhau.
"""
import difflib
import importlib.util
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / 'content' / 'quizzes'


def cards(name):
    spec = importlib.util.spec_from_file_location(f'q_{name}', SRC / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = []
    for group, items in mod.GROUPS.items():
        for c in items:
            if not isinstance(c, dict):
                c = dict(zip(['topic', 'q', 'a', 'd', 'why', 'src'], c))
            out.append({'set': name, 'group': group, **c})
    return out


def norm(text):
    return re.sub(r'\s+', ' ', re.sub(r'[`“”"(),.?:;]', ' ', text.lower())).strip()


def main():
    args = sys.argv[1:]
    target = args[0]
    ratio = float(args[args.index('--ratio') + 1]) if '--ratio' in args else 0.6
    names = sorted(p.stem for p in SRC.glob('*.py') if not p.stem.startswith('_'))
    mine = cards(target)
    others = [c for n in names for c in cards(n) if n != target]
    seen_src = {}
    for c in others:
        if c.get('src'):
            seen_src.setdefault(c['src'][1], []).append(c['set'])
    hits = 0
    for i, c in enumerate(mine):
        pool = others + mine[i + 1:]
        if c.get('src') and c['src'][1] in seen_src:
            print(f"NGUỒN  {c['topic']} | {c['src'][1]} đã dùng ở {seen_src[c['src'][1]]}")
            hits += 1
        for o in pool:
            r = difflib.SequenceMatcher(None, norm(c['q']), norm(o['q'])).ratio()
            same_topic = norm(c['topic']) == norm(o['topic'])
            same_answer = norm(c['a']) == norm(o['a']) and len(c['a']) > 12
            if r >= ratio or (same_topic and ('--all' in args or r >= 0.45)) or (same_answer and r >= 0.4):
                print(f"{r:.2f} {'KN ' if same_topic else ''}{c['topic']} ↔ {o['set']}/{o['topic']}\n   {c['q'][:110]}\n   {o['q'][:110]}")
                hits += 1
    print(f'{target}: {len(mine)} câu, {hits} cảnh báo')


if __name__ == '__main__':
    main()
