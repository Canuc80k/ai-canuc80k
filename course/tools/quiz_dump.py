"""In từng câu trắc nghiệm của một tệp: số thứ tự, tiêu đề, câu hỏi rút gọn, các lựa chọn kèm độ dài, đánh dấu đáp án đúng."""
import re, sys
from pathlib import Path
QUIZ = re.compile(r'^::: quiz([^\n]*)\n(.*?)^:::[ \t]*$', re.M | re.S)
for i, (title, body) in enumerate(QUIZ.findall(Path(sys.argv[1]).read_text(encoding='utf-8')), 1):
    lines = body.split('\n')
    opts = [(j, l) for j, l in enumerate(lines) if re.match(r'^- \[[ x]\] ', l)]
    q = ' '.join(lines[:opts[0][0]]).strip()
    L = [len(re.sub(r'[`$*]', '', l[6:])) for _, l in opts]
    k = [l[3] for _, l in opts].index('x')
    flag = 'DÀI NHẤT' if L[k] == max(L) and L.count(max(L)) == 1 else ('=max' if L[k] == max(L) else '')
    print(f'#{i} {title.strip() or "Hỏi nhanh"} {flag}\n  Q: {q[:160]}')
    for (j, l), n in zip(opts, L):
        print(f'  {l[:4]} ({n:3d}) {l[6:][:150]}')
