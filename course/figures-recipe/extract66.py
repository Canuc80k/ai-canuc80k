"""Bài 6.6: bảng chấm regex baseline trên bốn thông báo dev, lấy từ đúng validator và baseline của bài."""
from pathlib import Path
import re, io, contextlib, json
from svg import SVG, BLUE, CLAY, INK, LINE

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-6/6.6.md'
ns = {'__name__': 'extraction_grid_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
dev, baseline, validate = ns['dev_examples'], ns['regex_baseline'], ns['validate_answer']
rows = []
for notice, gold in dev:
    ok, _, answer = validate(baseline(notice))
    rows.append((ok, answer, gold))
assert len(rows) == 4 and all(ok for ok, _, _ in rows)
assert ns['schema_valid'] == 4 and ns['exact_correct'] == 2 and ns['field_correct'] == {'date': 3, 'students': 2}
assert [a == g for _, a, g in rows] == [True, True, False, False]
assert rows[2][1] == {'date': '15/10', 'students': None} and rows[3][1] == {'date': '20/10', 'students': 25}

labels = ['12/10 · 18 học sinh', 'chưa có ngày · 20 học sinh', '15/10 · 7 em', 'kế hoạch 20/10 → thực tế 21/10']
assert '7 em' in dev[2][0] and 'thực tế chuyển sang ngày 21/10' in dev[3][0]

s = SVG(640, 290)
cols = {'schema': 318, 'date': 410, 'students': 502, 'exact': 590}
width, top, step = 84, 50, 46
for name, x in cols.items():
    s.text(x, 26, name, 16)
for i, (label, (ok, answer, gold)) in enumerate(zip(labels, rows)):
    y = top + i * step
    s.line(12, y, 632, y, LINE, 0.8)
    s.text(16, y + step / 2, label, 17, anchor='start')
    cells = [('schema', 'hợp lệ', True)]
    for field in ('date', 'students'):
        value = answer[field]
        cells.append((field, 'null' if value is None else str(value), value == gold[field]))
    cells.append(('exact', 'đúng' if answer == gold else 'sai', answer == gold))
    for name, text, right in cells:
        x = cols[name]
        if not right:
            s.rect(x - width / 2 + 4, y + 6, width - 8, step - 12, CLAY, CLAY, radius=4, opacity=.12)
        s.text(x, y + step / 2, text, 17, color=INK if right else CLAY)
y = top + 4 * step
s.line(12, y, 632, y, INK, 1.2)
totals = {'schema': ns['schema_valid'], 'date': ns['field_correct']['date'],
          'students': ns['field_correct']['students'], 'exact': ns['exact_correct']}
s.text(16, y + 28, 'số ca đúng', 17, anchor='start')
for name, x in cols.items():
    s.text(x, y + 28, f'{totals[name]}/4', 17, color=BLUE, weight=600)
s.save('6-6-extraction-grid', 'Regex hợp schema ở cả bốn ca nhưng sai nội dung ở ca “7 em” và ca kế hoạch bị đổi.')
print('extraction grid verified', flush=True)
