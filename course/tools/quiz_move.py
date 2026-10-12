import re, sys
from pathlib import Path
C = Path(__file__).resolve().parents[1] / 'content'
# usage: quiz_move.py phase-N/<id>.md 'chuỗi trong đáp án đúng' A-D ...
# Chuỗi bắt đầu bằng '=' khớp nguyên văn cả đáp án (cho đáp án ngắn như '=6').
rel = sys.argv[1]; p = C / rel; t = p.read_text(encoding='utf-8')
args = sys.argv[2:]
for key, tgt in zip(args[::2], args[1::2]):
    pattern = r'^- \[x\] ' + re.escape(key[1:]) + r'$' if key.startswith('=') else r'^- \[x\] .*' + re.escape(key)
    blocks = [m for m in re.finditer(r'^::: quiz.*?\n(.*?)^:::', t, re.S | re.M) if re.search(pattern, m.group(1), re.M)]
    assert len(blocks) == 1, (key, len(blocks))
    m = blocks[0]; blk = m.group(1); lines = blk.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('- [')]
    opts = [lines[i] for i in idx]
    k = [j for j, o in enumerate(opts) if o.startswith('- [x]')][0]
    o = opts.pop(k); opts.insert('ABCDE'.index(tgt), o)
    for i, new in zip(idx, opts): lines[i] = new
    nb = '\n'.join(lines)
    t = t[:m.start(1)] + nb + t[m.end(1):]
    print(rel, key[:30], '->', tgt); print('   ' + '\n   '.join(opts))
p.write_text(t, encoding='utf-8')
