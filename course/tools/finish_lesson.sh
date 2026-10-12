#!/usr/bin/env bash
# Kiểm và dựng một bài sau khi sửa nguồn:
# chạy code -> kiểm nguồn -> dựng bài -> các trang khác không đổi -> QA Chromium -> ảnh ghép slide.
# bash tools/finish_lesson.sh 0.1        (preview build/serve.py phải đang chạy ở cổng 56872)
# Receipt: receipts/lessons/. Ảnh QA (dựng lại được): 04. Workspace/AI-course-qa/<id>/.
set -euo pipefail
id="$1"
S="$(cd "$(dirname "$0")/.." && pwd)"
QA="$S/../../04. Workspace/AI-course-qa/$id"
src="$(ls "$S"/content/phase-*/"$id".md)"
py() { python -B -X utf8 "$@"; }

py "$S/tools/check_code.py" "$src"
# Hình phải khớp mẫu nhúng của render_theory (vd. chú thích có dấu ] làm hình thành link 404)
py -c "
import re,sys; sys.path.insert(0, sys.argv[2]); import render_theory as R
bad=[l for l in open(sys.argv[1],encoding='utf-8').read().splitlines() if l.startswith('![') and '](' in l and ('fig/' in l) and not (R.FIGURE.match(l) or R.ANIM.match(l))]
if bad: print('Hình không nhúng được (chú thích có [ ] ?):', *bad, sep='\n  '); sys.exit(1)
" "$src" "$S/tools"
py "$S/tools/audit_sources.py" "$id"
py "$S/tools/rebuild_lesson.py" "$id" > "$S/receipts/lessons/rebuild-$id.json"
py -c "import json,sys; r=json.load(open(sys.argv[1],encoding='utf-8')); print({k: v for k, v in r.items() if k != 'files'})" "$S/receipts/lessons/rebuild-$id.json"
py "$S/tools/check_all_lessons.py"
# Link "Ôn lại" trỏ mục theo vị trí <h2>: thêm/bớt mục thì dựng lại quiz-bank cho khớp
(cd "$S" && py tools/build_quizzes.py | tail -1)
py "$S/tools/split_site.py"
mkdir -p "$QA"
rm -f "$QA"/*.png
(cd "$S/tools/qa" && node qa_lesson.cjs "$id" "$QA" > "$QA/qa-summary.json")
py -c "
import json,sys
r=json.load(open(sys.argv[1],encoding='utf-8'))
for k,v in r.items(): print(k, {a:b for a,b in v.items() if b not in ([],0,False)})
" "$QA/qa-summary.json"
py "$S/tools/contact_sheet.py" "$QA"
