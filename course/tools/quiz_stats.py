import re, sys
from pathlib import Path
from collections import Counter
C = Path(__file__).resolve().parents[1] / 'content'
tot = Counter()
for rel in sys.argv[1:]:
    t = (C / rel).read_text(encoding='utf-8')
    pos = Counter(); uniq = tie = n = 0
    for blk in re.findall(r'^::: quiz.*?\n(.*?)^:::', t, re.S | re.M):
        opts = re.findall(r'^- \[( |x)\] (.*)$', blk, re.M)
        if not opts: continue
        n += 1
        k = [i for i, (m, _) in enumerate(opts) if m == 'x'][0]
        pos['ABCDE'[k]] += 1
        L = [len(o) for _, o in opts]; mx = max(L)
        if L[k] == mx:
            if L.count(mx) == 1: uniq += 1
            else: tie += 1
    print(rel, n, 'quiz | vị trí', dict(sorted(pos.items())), '| đúng dài nhất riêng', uniq, '| hòa', tie)
    tot['n'] += n; tot['u'] += uniq; tot['t'] += tie
print('TỔNG', tot['n'], 'riêng dài nhất', tot['u'], f"({tot['u']/tot['n']:.0%})", 'hòa', tot['t'])
