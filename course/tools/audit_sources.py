from pathlib import Path
import ast,json,re,sys
R=Path(__file__).resolve().parents[1];CONTENT=R/'content'
# Bản sao từ build/audit_sources.py: ghi receipt vào receipts/lessons, nhận ID bài từ argv,
# và cho phép 5 lựa chọn khi câu ghi rõ là đề thi thật (giữ nguyên đề gốc).
ONLY=set(sys.argv[1:]);OUTDIR=R/'receipts'/'lessons'
REG=json.loads((R/'curriculum.json').read_text(encoding='utf-8'))
known={v['id']:v for v in REG['lessons']};problems=[];records=[]
for path in sorted(CONTENT.glob('phase-*/*.md')):
    if path.stem.startswith('_') or (ONLY and path.stem not in ONLY):continue
    t=path.read_text(encoding='utf-8');final=t.split('## Kiểm tra cuối bài',1)[-1] if '## Kiểm tra cuối bài' in t else ''
    quizzes=re.findall(r'^::: quiz([^\n]*)\n(.*?)^:::[ \t]*$',t,re.M|re.S)
    endq=re.findall(r'^::: quiz Câu (\d+)\n(.*?)^:::[ \t]*$',final,re.M|re.S)
    errors=[]
    if len(endq)!=10 or sorted(int(v[0]) for v in endq)!=list(range(1,11)):errors.append('final questions')
    positions=[]
    for label,body in quizzes:
        choices=re.findall(r'^- \[([ x])\] (.*)$',body,re.M)
        if len(choices) not in ([3,4,5] if re.search(r'^Đề thi:',body,re.M) else [3,4]) or sum(x=='x' for x,v in choices)!=1:errors.append('quiz options '+label)
        lines=body.splitlines();indexes=[i for i,l in enumerate(lines) if re.match(r'^- \[[ x]\]',l)]
        if indexes and not '\n'.join(lines[indexes[-1]+1:]).strip():errors.append('missing explanation')
    for label,body in endq:
        positions.append(next((i for i,(mark,value) in enumerate(re.findall(r'^- \[([ x])\] (.*)$',body,re.M)) if mark=='x'),-1))
    figures=re.findall(r'!\[[^\]]*\]\(([^)]+\.svg)\)',t)
    for ref in figures:
        if not (path.parent/ref).is_file():errors.append('missing figure '+ref)
    for i,code in enumerate(re.findall(r'^```python\n(.*?)^```',t,re.M|re.S)):
        try:ast.parse(code)
        except SyntaxError:errors.append(f'code syntax {i+1}')
    deck=path.parent/'slides'/path.name
    wide=[]
    if deck.exists():
        for i,chunk in enumerate(re.split(r'^---\s*$',deck.read_text(encoding='utf-8'),flags=re.M),1):
            narrow='<!-- split -->' in chunk
            for lang,code in re.findall(r'^```(python|output)\n(.*?)^```',chunk,re.M|re.S):
                for line in code.splitlines():
                    if len(line)>(52 if narrow else 104):wide.append({'slide':i,'language':lang,'length':len(line),'line':line})
            for ref in re.findall(r'!\[[^\]]*\]\(([^)]+\.svg)\)',chunk):
                if not (deck.parent/ref).exists():errors.append('deck missing '+ref)
    else:errors.append('missing deck')
    if len(figures)<2:errors.append('fewer than two meaningful figures')
    record={'id':path.stem,'words':len(t.split()),'quizzes':len(quizzes),'end_quizzes':len(endq),'answer_positions':positions,
            'figures':len(figures),'code_blocks':t.count('```python'),'wide_code':wide,'errors':errors}
    records.append(record)
    if errors:problems.append({'id':path.stem,'errors':errors})
missing=(set(known)&ONLY if ONLY else set(known))-{x['id'] for x in records}
receipt={'missing':sorted(missing),'problems':problems,'records':records}
OUTDIR.mkdir(exist_ok=True);(OUTDIR/('source-audit-'+'-'.join(sorted(ONLY))+'.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'missing':sorted(missing),'problems':problems,'overwide':sum(len(x['wide_code']) for x in records),'count':len(records)},ensure_ascii=False))
sys.exit(bool(missing or problems))
