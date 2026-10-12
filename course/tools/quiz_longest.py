#!/usr/bin/env python3
"""Liệt kê câu có đáp án đúng dài hẳn nhất (dễ lộ đáp án). Chạy trong course: python -B -X utf8 tools/quiz_longest.py <bộ> [ngưỡng ký tự]"""
import importlib.util
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / 'content' / 'quizzes'
name, gap = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0
spec = importlib.util.spec_from_file_location(name, SRC / f'{name}.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
n = 0
for group, items in mod.GROUPS.items():
    for c in items:
        c = c if isinstance(c, dict) else dict(zip(['topic', 'q', 'a', 'd'], c))
        m = max(len(x) for x in c['d'])
        if len(c['a']) > m + gap:
            n += 1
            print(f"{group:5} {len(c['a']):3} > {m:3}  {c['topic']}\n      A: {c['a']}\n      D: {c['d']}")
print(n, 'câu')
