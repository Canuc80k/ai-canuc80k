#!/usr/bin/env python3
"""Nối mỗi câu của mục Trắc nghiệm với bài và mục lý thuyết cần học để trả lời được câu đó.

Đích là một mục h2 (`## …`) của bài học hoặc buổi kiểm tra, trừ bốn mục cuối bài (Khi đi thi, Tóm tắt,
Kiểm tra cuối bài, Đọc thêm). Bảng nối lưu ở content/quizzes/learn.json, khóa là dấu vân tay của câu
(sha1 của câu hỏi và đoạn code), nên đổi thứ tự hay chuyển câu giữa các bộ không làm mất nối; sửa chữ câu hỏi
thì câu đó hiện ra là chưa nối để xem lại. build_quizzes.py đọc bảng này và gắn vào quiz-bank.js.

Chạy trong thư mục course:
  python -B -X utf8 tools/quiz_learn.py outline                 dàn ý: mỗi bài và các mục đích, đánh số §1, §2…
  python -B -X utf8 tools/quiz_learn.py find "<regex>"          mục nào nhắc tới cụm từ, bao nhiêu lần
  python -B -X utf8 tools/quiz_learn.py cands <bộ> [-k 8]       từng câu của bộ kèm các mục gợi ý (BM25), để gán tay
  python -B -X utf8 tools/quiz_learn.py ingest <tệp gán>        đọc dòng "L001: 2.3§8, 2.5§3" (hoặc "L001: -") vào learn.json
  python -B -X utf8 tools/quiz_learn.py check                   mọi câu đã nối, mọi mục đích còn tồn tại
  python -B -X utf8 tools/quiz_learn.py carry [--yes]           câu vừa sửa chữ: chép nối từ dòng cũ cùng bộ, cùng mã câu
  python -B -X utf8 tools/quiz_learn.py audit [--rank 40] [--empty 30]   soát nối yếu (BM25) và câu trống có mục khớp mạnh
Đổi tên một mục `##` trong bài thì sửa tên đó trong learn.json (check báo đúng chỗ).
  python -B -X utf8 tools/quiz_learn.py show <bộ>               in câu và các mục đã nối, để đọc lại
  python -B -X utf8 tools/quiz_learn.py spots <bộ> [--todo]     từng link kèm các câu gợi ý trong mục, nhãn [đoạn.câu]
  python -B -X utf8 tools/quiz_learn.py section <bài> <§|tên>   mọi câu của một mục, nhãn [đoạn.câu]
  python -B -X utf8 tools/quiz_learn.py mark <tệp chọn>         đọc dòng "L001.1: 4.2, 7" (câu cần đọc của link 1) vào learn.json
Câu cần đọc là chữ đúng như trên trang đã dựng (output/ui/theory.js), app.js tìm chuỗi ấy để tô sáng.
Dựng lại một bài thì chạy check: câu nào đã đổi chữ sẽ được báo để chọn lại.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

COURSE = Path(__file__).resolve().parent.parent
CONTENT = COURSE / 'content'
LEARN = CONTENT / 'quizzes' / 'learn.json'
SKIP = {'Khi đi thi', 'Tóm tắt', 'Kiểm tra cuối bài', 'Đọc thêm'}


def lesson_order(path):
    m = re.match(r'(\d+)\.(\d+)$', path.stem)
    return (int(path.parent.name.split('-')[1]), 0 if m else 1, int(m.group(2)) if m else 0, path.stem)


def split_sections(text):
    """[(tên mục, nội dung)] theo các dòng `## ` nằm ngoài khối code; thứ tự trùng thứ tự <h2> trên trang bài."""
    secs, fence = [], False
    for line in text.splitlines():
        if line.startswith('```'):
            fence = not fence
        if not fence and line.startswith('## '):
            secs.append([line[3:].strip(), []])
        elif secs:
            secs[-1][1].append(line)
    return [(h, '\n'.join(body)) for h, body in secs]


_LESSONS = None


def lessons():
    """[(id, tiêu đề, [(tên mục, nội dung)])] theo thứ tự khóa học; chỉ các mục đích."""
    global _LESSONS
    if _LESSONS is None:
        _LESSONS = []
        for path in sorted(CONTENT.glob('phase-*/*.md'), key=lesson_order):
            if path.name.startswith('_'):
                continue
            text = path.read_text(encoding='utf-8')
            title = re.search(r'^# (.+)$', text, re.M).group(1).strip()
            _LESSONS.append((path.stem, title, [(h, b) for h, b in split_sections(text) if h not in SKIP]))
    return _LESSONS


def headings():
    """{id bài: [tên mục đích]}: dùng để kiểm bảng nối."""
    return {lid: [h for h, _ in secs] for lid, _, secs in lessons()}


def targets():
    """{(id bài, tên mục): (vị trí <h2> trên trang, tiêu đề bài)}: build_quizzes.py dùng để dựng link."""
    out = {}
    for path in sorted(CONTENT.glob('phase-*/*.md'), key=lesson_order):
        if path.name.startswith('_'):
            continue
        text = path.read_text(encoding='utf-8')
        title = re.search(r'^# (.+)$', text, re.M).group(1).strip()
        for i, (h, _) in enumerate(split_sections(text)):
            if h not in SKIP:
                out[(path.stem, h)] = (i, title)
    return out


def fingerprint(card):
    return hashlib.sha1((card['q'] + '\n' + card.get('code', '')).encode('utf-8')).hexdigest()[:12]


def load_set(set_id):
    sys.path.insert(0, str(COURSE / 'tools'))
    import build_quizzes as bq
    meta = next(m for m in bq.SETS if m['id'] == set_id)
    cards = bq.load(set_id)
    out, n = [], 0
    for gid, _, _ in meta['groups']:
        for raw in cards[gid]:
            n += 1
            c = bq.normalize(raw)
            out.append((f"{meta['prefix']}{n:03d}", gid, c))
    return out


def all_sets():
    sys.path.insert(0, str(COURSE / 'tools'))
    import build_quizzes as bq
    return [m['id'] for m in bq.SETS if (CONTENT / 'quizzes' / f"{m['id']}.py").exists()]


# ---------- gợi ý bằng BM25 ----------
WORD = re.compile(r"[0-9a-zà-ỹđ_]+", re.I)
STOP = set('là và của các có một cho được không với khi thì này trong để những đó ra vào ta nào gì bao nhiêu '
           'như hay hơn mà từ theo vì nên đã sẽ cũng rồi lại đều chỉ cùng phải bằng sau trước nếu thế còn câu '
           'đúng sai đáp án phương lời giải học sinh người'.split())


def tokens(text):
    text = re.sub(r'```output.*?```', ' ', text, flags=re.S)
    words = [w.lower() for w in WORD.findall(text)]
    words = [w for w in words if w not in STOP and len(w) > 1]
    return words + [a + ' ' + b for a, b in zip(words, words[1:])]


class Index:
    def __init__(self):
        self.docs = []   # (id bài, số mục, tên mục)
        tfs = []
        for lid, title, secs in lessons():
            for k, (h, body) in enumerate(secs, 1):
                self.docs.append((lid, k, h))
                tfs.append(Counter(tokens(f'{h} {h} {title} {body}')))
        self.tfs, n = tfs, len(tfs)
        df = Counter(t for tf in tfs for t in tf)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}
        self.len = [sum(tf.values()) for tf in tfs]
        self.avg = sum(self.len) / n

    def rank(self, text, k=8):
        q = Counter(tokens(text))
        scores = []
        for i, tf in enumerate(self.tfs):
            s = 0.0
            for t, w in q.items():
                f = tf.get(t)
                if f:
                    s += min(w, 3) * self.idf[t] * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * self.len[i] / self.avg))
            scores.append(s)
        best = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [(self.docs[i], scores[i]) for i in best]


# ---------- câu cần đọc: đoạn văn trên trang đã dựng ----------
# Trang bài (output/ui/theory.js) chia thành đoạn: <p>, <li>, <figcaption>, hàng bảng <tr>, trừ phần trắc nghiệm trong bài.
# Chữ của một đoạn lấy như app.js (hàm learnText): công thức KaTeX viết lại thành $mã TeX$, mọi khoảng trắng gộp
# thành một dấu cách. Câu cần đọc lưu đúng chuỗi chữ ấy, nên app.js tìm lại được trên trang và tô sáng.
from html.parser import HTMLParser

THEORY = COURSE / 'output' / 'ui' / 'theory.js'
PASSAGE = {'p', 'li', 'figcaption', 'tr'}
VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'col', 'wbr', 'area', 'base', 'embed', 'track'}
SKIP_TAGS = {'svg', 'button', 'script', 'style'}


class _Node:
    __slots__ = ('tag', 'cls', 'kids', 'parent')

    def __init__(self, tag, cls, parent):
        self.tag, self.cls, self.kids, self.parent = tag, cls, [], parent


class _Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = _Node('#root', set(), None)
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = _Node(tag, set((dict(attrs).get('class') or '').split()), self.cur)
        self.cur.kids.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(_Node(tag, set((dict(attrs).get('class') or '').split()), self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def _walk(node):
    yield node
    for k in node.kids:
        if isinstance(k, _Node):
            yield from _walk(k)


def _raw_text(node):
    return ''.join(k if isinstance(k, str) else _raw_text(k) for k in node.kids)


def learn_text(node):
    """Chữ của một phần tử, đúng như hàm learnText trong app.js."""
    out, space = [], True

    def emit(s, atomic):
        nonlocal space
        for ch in s:
            if not atomic and ch.isspace():
                if not space:
                    out.append(' ')
                space = True
            else:
                out.append(ch)
                space = False

    def go(n):
        for k in n.kids:
            if isinstance(k, str):
                emit(k, False)
            elif 'katex' in k.cls:
                ann = next((x for x in _walk(k) if x.tag == 'annotation'), None)
                emit('$' + (_raw_text(ann) if ann else '') + '$', True)
            elif k.tag not in SKIP_TAGS and 'out-label' not in k.cls:
                go(k)
    go(node)
    if out and out[-1] == ' ':
        out.pop()
    return ''.join(out)


_PAGES = {}


def page_sections(lid):
    """{vị trí <h2> trên trang: (tên mục, [chữ từng đoạn])} của các mục <section class="t-sec">."""
    if not _PAGES:
        s = THEORY.read_text(encoding='utf-8')
        _PAGES.update(json.loads(s[s.index('{'):s.rindex('}') + 1])['lessons'])
    page = _PAGES[lid]
    if isinstance(page, dict) and 'html' in page:
        root = _Tree(page['html']).root
        out = {}
        for k, h2 in enumerate(n for n in _walk(root) if n.tag == 'h2'):
            sec = h2.parent
            if sec.tag != 'section' or 't-sec' not in sec.cls:
                continue
            paras = []
            for n in _walk(sec):
                if n.tag in PASSAGE and not _inside(n, sec, lambda a: 'quiz' in a.cls or a.tag == 'svg'):
                    t = learn_text(n)
                    if t:
                        paras.append(t)
            out[k] = (learn_text(h2), paras)
        _PAGES[lid] = out
    return _PAGES[lid]


def _inside(n, stop, test):
    a = n.parent
    while a is not None and a is not stop:
        if test(a):
            return True
        a = a.parent
    return False


def sentences(text):
    """Tách đoạn thành câu: sau . ! ? … và khoảng trắng, câu sau mở đầu bằng chữ hoa, chữ số, ngoặc hay công thức;
    không cắt bên trong $…$. Ghép các câu liền nhau bằng một dấu cách cho lại đúng chuỗi gốc."""
    out, start, dollars = [], 0, 0
    for i, ch in enumerate(text):
        if ch == '$':
            dollars += 1
        if (ch == ' ' and i > 0 and text[i - 1] in '.!?…' and dollars % 2 == 0 and i + 1 < len(text)
                and (text[i + 1].isupper() or text[i + 1].isdigit() or text[i + 1] in '“"‘([$`')):
            out.append(text[start:i])
            start = i + 1
    out.append(text[start:])
    return [s for s in out if s]


_TARGETS = None


def section_paras(lid, h):
    """Chữ từng đoạn của mục `h` trong bài `lid` trên trang đã dựng."""
    global _TARGETS
    if _TARGETS is None:
        _TARGETS = targets()
    return page_sections(lid)[_TARGETS[(lid, h)][0]][1]


class SentIndex:
    """BM25 trên từng câu của mọi mục đích: xếp hạng câu trong một mục theo độ khớp với câu hỏi."""
    def __init__(self):
        self.tf = {}
        df, n, total = Counter(), 0, 0
        for lid, _, secs in lessons():
            for h, _ in secs:
                for i, para in enumerate(section_paras(lid, h), 1):
                    for j, sent in enumerate(sentences(para), 1):
                        tf = Counter(tokens(sent))
                        self.tf[(lid, h, i, j)] = tf
                        df.update(tf.keys())
                        n += 1
                        total += sum(tf.values())
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}
        self.avg = total / n

    def score(self, key, q):
        tf, ln = self.tf[key], sum(self.tf[key].values())
        return sum(min(w, 3) * self.idf[t] * tf[t] * 2.2 / (tf[t] + 1.2 * (0.25 + 0.75 * ln / self.avg)) for t, w in q.items() if t in tf)


# ---------- bảng nối ----------
def read_learn():
    return json.loads(LEARN.read_text(encoding='utf-8')) if LEARN.exists() else {}


def write_learn(data):
    data = dict(sorted(data.items(), key=lambda kv: (kv[1]['set'], kv[1]['ref'])))
    LEARN.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')


def cmd_outline(_):
    for lid, title, secs in lessons():
        print(f'{lid} {title}')
        print('   ' + ' | '.join(f'§{k} {h}' for k, (h, _) in enumerate(secs, 1)))


def short(s, n):
    s = re.sub(r'\s+', ' ', s)
    return s if len(s) <= n else s[:n - 1] + '…'


def cmd_cands(a):
    idx, done = Index(), read_learn()
    for ref, gid, c in load_set(a.set):
        fp = fingerprint(c)
        if a.todo and fp in done:
            continue
        print(f'{ref} [{gid}] {c["topic"]}')
        print(f'  Q: {short(c["q"], a.width)}')
        if c.get('code'):
            print(f'  CODE: {short(c["code"], 160)}')
        print(f'  A: {short(c["a"], 160)}')
        print(f'  W: {short(c["why"], a.width)}')
        hits = idx.rank(' '.join([c['topic'], c['q'], c['a'], c['why'], c.get('code', '')]), a.k)
        print('  ? ' + ' | '.join(f'{lid}§{k} {short(h, 34)}' for (lid, k, h), _ in hits))


LINE = re.compile(r'^([A-Z]+\d{3})\s*:\s*(.*?)\s*(?:#.*)?$')
REF = re.compile(r'^(kt\d|\d+\.\d+)§(\d+)$')


def cmd_ingest(a):
    outline = {lid: [h for h, _ in secs] for lid, _, secs in lessons()}
    data = read_learn()
    by_set = {}
    errors, n = [], 0
    for line in Path(a.file).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            set_id = line[1:].strip()
            by_set[set_id] = {ref: c for ref, _, c in load_set(set_id)}
            cur = by_set[set_id]
            continue
        m = LINE.match(line)
        if not m:
            errors.append(f'dòng lạ: {line}')
            continue
        ref, rhs = m.groups()
        card = cur.get(ref)
        if card is None:
            errors.append(f'{set_id}: không có câu {ref}')
            continue
        targets = []
        if rhs != '-':
            for t in [x.strip() for x in rhs.split(',')]:
                r = REF.match(t)
                if not r or r.group(1) not in outline or not 1 <= int(r.group(2)) <= len(outline[r.group(1)]):
                    errors.append(f'{set_id}/{ref}: mục không có: {t}')
                    continue
                targets.append([r.group(1), outline[r.group(1)][int(r.group(2)) - 1]])
        assert len({tuple(t) for t in targets}) == len(targets), f'{ref}: trùng mục'
        kept = {(t[0], t[1]): t[2:] for t in data.get(fingerprint(card), {}).get('to', [])}
        targets = [t + kept.get(tuple(t), []) for t in targets]
        data[fingerprint(card)] = {'set': set_id, 'ref': ref, 'q': short(card['q'], 70), 'to': targets}
        n += 1
    if errors:
        sys.exit('\n'.join(errors))
    write_learn(data)
    print(f'Đã ghi {n} câu vào {LEARN.relative_to(COURSE)} (tổng {len(data)})')


def cmd_check(_):
    outline = headings()
    data, seen, bad = read_learn(), set(), []
    stats, nospot = Counter(), 0
    for set_id in all_sets():
        for ref, _, c in load_set(set_id):
            fp = fingerprint(c)
            seen.add(fp)
            e = data.get(fp)
            if e is None:
                bad.append(f'{set_id}/{ref}: chưa nối')
                continue
            stats[len(e['to'])] += 1
            for lid, h, *spots in e['to']:
                if h not in outline.get(lid, []):
                    bad.append(f'{set_id}/{ref}: mục không còn: {lid} · {h}')
                    continue
                if not spots:
                    nospot += 1
                for quote in (spots[0] if spots else []):
                    if not any(quote in t for t in section_paras(lid, h)):
                        bad.append(f'{set_id}/{ref}: câu cần đọc không còn trong {lid} · {h}: {short(quote, 60)}')
    stale = [e['ref'] for fp, e in data.items() if fp not in seen]
    print(f'Số mục mỗi câu: {dict(sorted(stats.items()))}; mục trong bảng không còn câu: {len(stale)}; link chưa chọn câu cần đọc: {nospot}')
    if bad:
        sys.exit('\n'.join(bad[:40]) + (f'\n… và {len(bad) - 40} lỗi khác' if len(bad) > 40 else ''))
    print('PASS: mọi câu đã nối, mọi mục đích và câu cần đọc còn tồn tại')


def cmd_carry(a):
    """Câu vừa sửa chữ có dấu vân tay mới: tìm dòng cũ cùng bộ, cùng mã câu, đã mồ côi; in cũ/mới, --yes thì chép nối sang."""
    data = read_learn()
    cards = {s: load_set(s) for s in all_sets()}
    live = {fingerprint(c) for rows in cards.values() for _, _, c in rows}
    orphans = {(e['set'], e['ref']): fp for fp, e in data.items() if fp not in live}
    moved = 0
    for set_id, rows in cards.items():
        for ref, _, c in rows:
            fp = fingerprint(c)
            old = orphans.get((set_id, ref))
            if fp in data or old is None:
                continue
            print(f'{set_id}/{ref}\n  cũ: {data[old]["q"]}\n  mới: {short(c["q"], 70)}\n  nối: {data[old]["to"]}')
            if a.yes:
                data[fp] = {**data.pop(old), 'q': short(c['q'], 70)}
                moved += 1
    if a.yes:
        write_learn(data)
        print(f'Đã chép {moved} câu')


def cmd_show(a):
    data = read_learn()
    for ref, gid, c in load_set(a.set):
        e = data.get(fingerprint(c))
        to = ' ; '.join(f'{lid} {h}' + ''.join(f'\n          « {q} »' for q in (sp[0] if sp else [])) for lid, h, *sp in e['to']) if e else 'CHƯA NỐI'
        print(f'{ref} {short(c["q"], 90)}\n      → {to or "(không có mục phù hợp)"}')


def cmd_audit(a):
    """Soát lại bảng nối bằng BM25: mục đã nối xếp hạng quá thấp (dễ là gõ nhầm số mục),
    và câu không nối nhưng có mục khớp mạnh (dễ là bỏ sót)."""
    idx, data = Index(), read_learn()
    pos = {(lid, h): i for i, (lid, _, h) in enumerate(idx.docs)}
    for set_id in all_sets():
        for ref, _, c in load_set(set_id):
            e = data.get(fingerprint(c))
            if e is None:
                continue
            q = Counter(tokens(' '.join([c['topic'], c['q'], c['a'], c['why'], c.get('code', '')])))
            scores = [sum(min(w, 3) * idx.idf[t] * tf[t] * 2.2 / (tf[t] + 1.2 * (0.25 + 0.75 * idx.len[i] / idx.avg))
                          for t, w in q.items() if t in tf) for i, tf in enumerate(idx.tfs)]
            order = sorted(range(len(scores)), key=lambda i: -scores[i])
            rank = {i: r for r, i in enumerate(order, 1)}
            top = idx.docs[order[0]]
            if e['to']:
                weak = [(lid, h, rank[pos[(lid, h)]]) for lid, h, *_ in e['to'] if rank[pos[(lid, h)]] > a.rank]
                if weak and len(weak) == len(e['to']):
                    print(f'YẾU {set_id}/{ref} {short(c["q"], 80)}\n     nối: ' + ' ; '.join(f'{l} {short(h, 40)} (hạng {r})' for l, h, r in weak)
                          + f'\n     BM25 đứng đầu: {top[0]}§{top[1]} {short(top[2], 40)}')
            elif a.empty and scores[order[0]] >= a.empty:
                print(f'TRỐNG {set_id}/{ref} {short(c["q"], 80)} → gợi ý {top[0]}§{top[1]} {short(top[2], 40)} ({scores[order[0]]:.0f})')


def cmd_coverage(_):
    """Mục nào được nhiều câu trỏ tới, mục nào chưa câu nào trỏ tới."""
    hits = Counter()
    for e in read_learn().values():
        for lid, h, *_ in e['to']:
            hits[(lid, h)] += 1
    per = defaultdict(int)
    for lid, _, secs in lessons():
        for h, _ in secs:
            per[lid] += hits[(lid, h)]
    print(' '.join(f'{lid}:{n}' for lid, n in per.items()))


def cmd_find(a):
    """Mục nào nhắc tới cụm từ (không phân biệt hoa thường), kèm số lần và câu đầu tiên chứa nó."""
    pat = re.compile(a.term, re.I)
    for lid, _, secs in lessons():
        for k, (h, body) in enumerate(secs, 1):
            hits = pat.findall(h + '\n' + body)
            if len(hits) >= a.min:
                first = next((s for s in re.split(r'(?<=[.!?])\s+|\n', body) if pat.search(s)), h)
                print(f'{lid}§{k} {h} ×{len(hits)}  | {short(first.strip(), 140)}')


def cmd_spots(a):
    """Từng link của bộ kèm các câu trong mục xếp theo độ khớp, để chọn câu cần đọc. Nhãn [đoạn.câu] dùng cho `mark`."""
    idx, data = SentIndex(), read_learn()
    for ref, _, c in load_set(a.set):
        e = data.get(fingerprint(c))
        if not e or not e['to'] or (a.todo and all(len(t) > 2 for t in e['to'])):
            continue
        right = c['options'][c['answer']] if 'options' in c else c.get('a', '')
        print(f'{ref} Q: {short(c["q"], a.width)}' + (f'\n   CODE: {short(c["code"], 140)}' if c.get('code') else ''))
        print(f'   A: {short(right, 160)}\n   W: {short(c["why"], a.width)}')
        q = Counter(tokens(' '.join([c['q'], right, right, c['why'], c.get('code', '')])))
        for n, (lid, h, *sp) in enumerate(e['to'], 1):
            paras = section_paras(lid, h)
            keys = [(lid, h, i, j) for i, para in enumerate(paras, 1) for j, _ in enumerate(sentences(para), 1)]
            best = sorted(keys, key=lambda k: -idx.score(k, q))[:a.k]
            print(f' .{n} → {lid} · {h} ({len(paras)} đoạn, {len(keys)} câu)' + (f'  ĐÃ CHỌN {len(sp[0])}' if sp else ''))
            for key in sorted(best, key=lambda k: k[2:]):
                print(f'   [{key[2]}.{key[3]}] {short(sentences(paras[key[2] - 1])[key[3] - 1], a.swidth)}')


def cmd_section(a):
    """In mọi câu của một mục, đánh nhãn [đoạn.câu]: id bài và số thứ tự mục (§) như `outline`, hoặc tên mục."""
    secs = dict((lid, s) for lid, _, s in lessons())[a.lid]
    h = secs[int(a.sec) - 1][0] if a.sec.isdigit() else a.sec
    print(f'{a.lid} · {h}')
    for i, para in enumerate(section_paras(a.lid, h), 1):
        for j, sent in enumerate(sentences(para), 1):
            print(f'[{i}.{j}] {short(sent, a.swidth)}')


SPOT_LINE = re.compile(r'^([A-Z]+\d{3})(?:\.(\d))?\s*:\s*(.*?)\s*(?:#.*)?$')
SPOT = re.compile(r'^(\d+)(?:\.(\d+)(?:-(\d+))?)?$')


def cmd_mark(a):
    """Đọc tệp chọn câu: dòng "@bộ", rồi "L001.1: 4.2" (câu 2 đoạn 4), "4.2-3" (câu 2 tới 3), "4" (cả đoạn),
    nhiều chỗ cách nhau dấu phẩy; câu chỉ có một link thì viết "L001: 4.2"."""
    data = read_learn()
    errors, n = [], 0
    for line in Path(a.file).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            set_id = line[1:].strip()
            cur = {ref: c for ref, _, c in load_set(set_id)}
            continue
        m = SPOT_LINE.match(line)
        if not m:
            errors.append(f'dòng lạ: {line}')
            continue
        ref, k, rhs = m.groups()
        e = data.get(fingerprint(cur[ref])) if ref in cur else None
        if not e or not e['to']:
            errors.append(f'{set_id}/{ref}: không có link')
            continue
        if k is None and len(e['to']) > 1:
            errors.append(f'{set_id}/{ref}: có {len(e["to"])} link, phải ghi .1/.2')
            continue
        k = int(k or 1)
        if not 1 <= k <= len(e['to']):
            errors.append(f'{set_id}/{ref}: không có link .{k}')
            continue
        lid, h = e['to'][k - 1][:2]
        paras, quotes = section_paras(lid, h), []
        for spot in [x.strip() for x in rhs.split(',')]:
            r = SPOT.match(spot)
            if not r or not 1 <= int(r.group(1)) <= len(paras):
                errors.append(f'{set_id}/{ref}.{k}: không có đoạn {spot}')
                continue
            para = paras[int(r.group(1)) - 1]
            if r.group(2) is None:
                quotes.append(para)
                continue
            sents = sentences(para)
            lo = int(r.group(2))
            hi = int(r.group(3) or lo)
            if not 1 <= lo <= hi <= len(sents):
                errors.append(f'{set_id}/{ref}.{k}: không có câu {spot}')
                continue
            quote = ' '.join(sents[lo - 1:hi])
            assert quote in para
            quotes.append(quote)
        e['to'][k - 1] = [lid, h, quotes]
        n += 1
    if errors:
        sys.exit('\n'.join(errors))
    write_learn(data)
    print(f'Đã ghi câu cần đọc cho {n} link')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('outline')
    p = sub.add_parser('find')
    p.add_argument('term')
    p.add_argument('--min', type=int, default=1)
    p = sub.add_parser('cands')
    p.add_argument('set')
    p.add_argument('-k', type=int, default=8)
    p.add_argument('--width', type=int, default=260)
    p.add_argument('--todo', action='store_true', help='chỉ câu chưa nối')
    p = sub.add_parser('ingest')
    p.add_argument('file')
    sub.add_parser('check')
    p = sub.add_parser('carry')
    p.add_argument('--yes', action='store_true')
    p = sub.add_parser('show')
    p.add_argument('set')
    sub.add_parser('coverage')
    p = sub.add_parser('spots')
    p.add_argument('set')
    p.add_argument('-k', type=int, default=6)
    p.add_argument('--width', type=int, default=240)
    p.add_argument('--swidth', type=int, default=230)
    p.add_argument('--todo', action='store_true', help='chỉ câu còn link chưa chọn câu cần đọc')
    p = sub.add_parser('section')
    p.add_argument('lid')
    p.add_argument('sec')
    p.add_argument('--swidth', type=int, default=400)
    p = sub.add_parser('mark')
    p.add_argument('file')
    p = sub.add_parser('audit')
    p.add_argument('--rank', type=int, default=40, help='báo khi mọi mục đã nối xếp sau hạng này')
    p.add_argument('--empty', type=float, default=0, help='báo câu không nối mà mục đứng đầu đạt điểm này')
    a = ap.parse_args()
    {'outline': cmd_outline, 'find': cmd_find, 'cands': cmd_cands, 'ingest': cmd_ingest, 'check': cmd_check, 'carry': cmd_carry, 'show': cmd_show,
     'coverage': cmd_coverage, 'audit': cmd_audit, 'spots': cmd_spots, 'section': cmd_section, 'mark': cmd_mark}[a.cmd](a)


if __name__ == '__main__':
    main()
