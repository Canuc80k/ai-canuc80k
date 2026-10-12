"""Dựng lại phần mở chương (content/phase-N/_intro.md) vào theory.js, đúng cách integrate.py làm.

python -B -X utf8 tools/rebuild_intro.py 0          # phase-0
Chỉ thay mục phases[N]; mọi bài và chương khác phải giữ nguyên.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rebuild_lesson as rb  # noqa: E402

ig = rb.ig
phase = sys.argv[1]
path = rb.CONTENT / f'phase-{phase}' / '_intro.md'
target = rb.OUT / 'ui/theory.js'
nl = rb.newline_of(target)
theory = ig.json_js(target, rb.THEORY_PREFIX)
assert rb.dump(rb.THEORY_PREFIX, theory, nl) == target.read_bytes(), 'theory.js không dump lại đúng bytes'
item = ig.rt.render(path)
html = ig.asset_links(item['html'], path.parent)
old = theory['phases'][phase]['html']
theory['phases'][phase] = {'html': html}
target.write_bytes(rb.dump(rb.THEORY_PREFIX, theory, nl))
print(f'phase-{phase}/_intro:', 'đổi' if html != old else 'không đổi')
