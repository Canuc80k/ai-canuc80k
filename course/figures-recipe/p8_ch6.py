"""Lượt 8 — hình chương 6 (bản gọn). Số liệu lấy từ code bài (lesson_ns) hoặc tính lại đúng như bài.
Chạy riêng: python -B -X utf8 p8_ch6.py [tên ...]"""
import math, sys
import numpy as np
from kit import *
from p8_ch1 import lesson_ns
from p8_ch2 import PAPER, sup, mnum, clip, segline, regions, jit


def chips(s, x, y, toks, col=BLUE, h=28, gap=6, size=12.5, op=.16, font_w=7.6, pad=14, mono=True):
    """Dãy token dạng ô bo góc; trả vị trí x kết thúc."""
    for t in toks:
        w = max(26, font_w * len(t) + pad)
        s.box(x, y, w, h, 'none', col, r=6, width=0, opacity=op)
        if mono:
            s.mono(x + w / 2, y + h / 2 + .5, t, size, 'middle', TEXT)
        else:
            s.label(x + w / 2, y + h / 2, t, size, color=TEXT)
        x += w + gap
    return x


# ───────────────────────────── 6.1 ─────────────────────────────


def levels61():
    s = Fig(640, 230)
    rows = [('ký tự', list('học sinh'), FAINT), ('âm tiết', ['học', 'sinh', 'học', 'máy'], BLUE),
            ('từ', ['học_sinh', 'học_máy'], GREEN), ('subword', ['học', '##sinh', 'học', '##máy'], CLAY)]
    s.label(330, 20, '“học sinh học máy”', 13, color=TEXT, weight=600)
    for r, (nm, toks, col) in enumerate(rows):
        y = 40 + r * 44
        s.label(120, y + 8, nm, 12.5, 'end', MUTED)
        s.mono(120, y + 23, f'{len(toks) if r else 16} token', 10.5, 'end', FAINT)
        if r == 0:
            toks = list('học sinh học máy')
            toks = ['␣' if c == ' ' else c for c in toks]
            end = chips(s, 134, y, toks, col, gap=3, font_w=7, pad=10, op=.2)
        else:
            end = chips(s, 134, y, toks, col, op=.2 if col != FAINT else .2)
    s.label(330, 220, 'cùng một câu, số token tùy đơn vị tokenizer chọn', 11.5, color=MUTED)
    s.save('6-1-token-levels', 'Cùng một câu tách theo ký tự, âm tiết, từ hay subword cho số token khác nhau.')


def nfc61():
    s = Fig(640, 190)
    rows = [('gõ sẵn', ['h', 'ọ', 'c'], ['0x68', '0x1ecd', '0x63']),
            ('dấu rời', ['h', 'o', '◌̣', 'c'], ['0x68', '0x6f', '0x323', '0x63'])]
    for r, (nm, chars, codes) in enumerate(rows):
        y = 34 + r * 66
        s.label(120, y + 16, nm, 12.5, 'end', TEXT)
        x = 134
        for ch, cd in zip(chars, codes):
            col = CLAY if cd in ('0x1ecd', '0x323') else BLUE
            s.box(x, y, 60, 32, 'none', col, r=6, width=0, opacity=.18)
            s.label(x + 30, y + 16, ch, 14, color=TEXT)
            s.mono(x + 30, y + 46, cd, 10.5, 'middle', MUTED)
            x += 66
    s.arrow(400, 116, 470, 60, GREEN, 1.4)
    s.label(500, 50, 'NFC gộp lại', 12, 'start', GREEN, 600)
    s.label(500, 70, 'vẫn giữ dấu', 12, 'start', MUTED)
    s.save('6-1-nfc', 'Hai chuỗi cùng hiện là “học” nhưng khác số ký tự; NFC đưa về một dạng.')


def bpe61():
    s = Fig(640, 240)
    words = [('low', 3), ('lower', 2), ('new', 1)]
    steps = [('ký tự', lambda w: list(w)), ('gộp l,o (5 lần)', None), ('gộp lo,w (5 lần)', None)]
    seqs = {w: list(w) for w, _ in words}
    hist = [dict(seqs)]

    def merge(t, a, b):
        out, i = [], 0
        while i < len(t):
            if i + 1 < len(t) and t[i] == a and t[i + 1] == b:
                out.append(a + b)
                i += 2
            else:
                out.append(t[i])
                i += 1
        return out
    for a, b in [('l', 'o'), ('lo', 'w')]:
        seqs = {w: merge(t, a, b) for w, t in seqs.items()}
        hist.append(dict(seqs))
    for c, (title, _) in enumerate(steps):
        x0 = 120 + c * 176
        s.label(x0 + 70, 24, title, 12, color=TEXT if c == 0 else CLAY, weight=600)
        for r, (w, n) in enumerate(words):
            y = 40 + r * 44
            chips(s, x0, y, hist[c][w], BLUE if c == 0 else CLAY, h=26, gap=3, font_w=8, pad=10, size=12, op=.15 + .07 * c)
    for r, (w, n) in enumerate(words):
        s.label(108, 40 + r * 44 + 13, f'{w} × {n}', 12, 'end', MUTED)
    s.label(330, 200, 'tần suất có trọng số: l,o có trong low (3) và lower (2), cộng 5', 11.5, color=MUTED)
    s.save('6-1-bpe', 'BPE gộp dần cặp hay gặp nhất: l,o rồi lo,w, nên “low” thành một token.')


def wordpiece61():
    s = Fig(640, 200)
    s.label(80, 30, 'từ vựng', 12, 'start', MUTED)
    chips(s, 140, 16, ['un', 'una', '##able', '[UNK]'], FAINT, op=.2)
    s.mono(80, 84, 'unable', 14, 'start', TEXT, 600)
    chips(s, 180, 70, ['una'], GREEN, op=.25)
    s.mono(246, 84.5, '+ ble ?', 12.5, 'start', CLAY)
    s.label(340, 84, '##ble, ##bl, ##b đều không có', 12, 'start', MUTED)
    s.mono(80, 140, '→', 14, 'start', MUTED)
    chips(s, 106, 126, ['[UNK]'], CLAY, op=.3)
    s.label(200, 140, 'tham lam lấy mảnh dài nhất, không quay lui thử un + ##able', 12, 'start', MUTED)
    s.save('6-1-wordpiece', 'WordPiece lấy mảnh dài nhất trước; phần còn lại không khớp nên cả từ thành UNK.')


def pipeline61():
    s = Fig(640, 210)
    s.box(20, 40, 140, 40, 'none', FAINT, r=8, width=0, opacity=.18)
    s.label(90, 60, '“bài học hay”', 12.5, color=TEXT)
    s.arrow(164, 60, 196, 60, LINE, 1.2)
    s.box(200, 40, 120, 40, 'none', BLUE, r=8, width=0, opacity=.16)
    s.label(260, 60, 'NFC, viết thường', 12, color=TEXT)
    s.arrow(324, 60, 356, 60, LINE, 1.2)
    s.box(360, 40, 120, 40, 'none', BLUE, r=8, width=0, opacity=.22)
    s.label(420, 54, 'TF-IDF', 12.5, color=TEXT, weight=600)
    s.mono(420, 70, '69 cột', 10.5, 'middle', MUTED)
    s.arrow(484, 60, 516, 60, LINE, 1.2)
    s.box(520, 40, 100, 40, 'none', CLAY, r=8, width=0, opacity=.22)
    s.label(570, 54, 'logistic', 12.5, color=TEXT, weight=600)
    s.mono(570, 70, 'p(tích cực)', 10.5, 'middle', MUTED)
    s.path('M 420,84 L 420,120 L 260,120', GREEN, 1.4, dash='4 3')
    s.label(330, 140, 'vocabulary và IDF chỉ fit trên 12 câu train', 12, color=GREEN)
    s.label(330, 168, 'validation chỉ transform; từ chưa gặp như “không” bị bỏ', 11.5, color=MUTED)
    s.save('6-1-text-pipeline', 'Chuẩn hóa văn bản, TF-IDF fit trên train, rồi logistic regression.')


def coef61():
    ns = lesson_ns('6.1', upto=3)
    tf, clf = ns['baseline']['tfidf'], ns['baseline']['classifier']
    names = tf.get_feature_names_out()
    w = clf.coef_[0]
    order = np.argsort(w)
    pick = list(order[:6]) + list(order[-6:])
    s = Fig(640, 280)
    mx = np.abs(w[pick]).max()
    for k, i in enumerate(pick):
        y = 20 + k * 20
        v = w[i]
        x0 = 320
        L = v / mx * 200
        s.rect(min(x0, x0 + L), y, abs(L), 15, 'none', GREEN if v > 0 else CLAY, 2, .55, 0)
        s.label(x0 - 8 if v > 0 else x0 + 8, y + 8, names[i], 11.5, 'end' if v > 0 else 'start', TEXT)
    s.line(320, 16, 320, 262, LINE, 1)
    s.label(200, 272, '← kéo về tiêu cực', 11.5, color=CLAY)
    s.label(440, 272, 'kéo về tích cực →', 11.5, color=GREEN)
    s.save('6-1-coef', 'Các từ có trọng số lớn nhất đều là từ khen, chê trực tiếp; không có cột nào cho “không”.')


def valid61():
    ns = lesson_ns('6.1', upto=4)
    T, y, pred, p = ns['valid_texts'], ns['valid_labels'], ns['valid_pred'], ns['positive_prob']
    s = Fig(640, 250)
    ax = s.axes(200, 20, 290, 190, (0, 1), (6, 0), xticks=[0, 1], yticks=[], grid=False, frame=True)
    for i, (t, yy, pp, pr) in enumerate(zip(T, y, pred, p)):
        cy = ax.Y(i + .5)
        wrong = yy != pp
        col = GREEN if yy == 1 else CLAY
        s.rect(ax.X(0), cy - 9, ax.X(pr) - ax.X(0), 18, 'none', col, 3, .55 if not wrong else .25, 0)
        if wrong:
            s.rect(ax.X(0), cy - 9, ax.X(pr) - ax.X(0), 18, col, 'none', 3, 1, 1.6)
        s.label(200, cy, t, 12, 'end', TEXT, 600 if wrong else 400)
        s.mono(ax.X(1) + 8, cy, f'{pr:.3f}', 11, 'start', MUTED)
    s.label(ax.X(.5), 232, 'p(tích cực)', 11.5, color=FAINT)
    s.label(572, 70, 'tích cực thật', 11.5, 'start', GREEN)
    s.label(572, 90, 'tiêu cực thật', 11.5, 'start', CLAY)
    s.label(572, 120, 'viền: sai', 11.5, 'start', MUTED)
    s.save('6-1-valid', 'Hai câu sai chứa “không”, từ chưa có trong vocabulary.')


def confusion61():
    s = Fig(640, 200)
    s.tiles(250, 50, [['2', '1'], ['1', '2']], 70, 50, BLUE, 6, {(0, 0): (GREEN, .3), (1, 1): (GREEN, .3), (0, 1): (CLAY, .25), (1, 0): (CLAY, .25)}, size=16)
    s.label(285, 36, 'đoán 0', 12, color=MUTED)
    s.label(361, 36, 'đoán 1', 12, color=MUTED)
    s.label(240, 75, 'thật 0', 12, 'end', MUTED)
    s.label(240, 131, 'thật 1', 12, 'end', MUTED)
    s.label(470, 70, '“bài giảng không hay”', 11.5, 'start', CLAY)
    s.label(470, 126, '“khóa học không tệ”', 11.5, 'start', CLAY)
    s.line(396, 75, 466, 70, FAINT, 1, '3 3')
    s.line(396, 131, 466, 126, FAINT, 1, '3 3')
    s.label(320, 186, 'accuracy 4/6 = 0.667, macro-F1 0.667', 11.5, color=MUTED)
    s.save('6-1-confusion', 'Hai câu đoán sai đều chứa “không”.')


def pattern61():
    s = Fig(640, 200)
    rows = [('bài C++ khó', [('bài', 1), ('c', 0), ('khó', 1)]), ('bài R dễ', [('bài', 1), ('r', 0), ('dễ', 1)]),
            ('bài Go hay', [('bài', 1), ('go', 1), ('hay', 1)])]
    for r, (txt, toks) in enumerate(rows):
        y = 30 + r * 46
        s.label(150, y + 14, txt, 12.5, 'end', TEXT)
        x = 170
        for t, keep in toks:
            w = 16 + 8 * len(t)
            s.box(x, y, w, 28, 'none', GREEN if keep else CLAY, r=6, width=0, opacity=.25 if keep else .12)
            s.mono(x + w / 2, y + 14.5, t, 12, 'middle', TEXT if keep else FAINT)
            x += w + 6
    s.mono(420, 60, r'token_pattern mặc định', 11.5, 'start', MUTED)
    s.mono(420, 80, r'(?u)\b\w\w+\b', 12, 'start', TEXT)
    s.label(420, 110, 'bỏ mọi token một ký tự (ô mờ)', 12, 'start', CLAY)
    s.save('6-1-pattern', 'TfidfVectorizer mặc định chỉ giữ token từ hai ký tự chữ hoặc số trở lên: “C++” chỉ còn “c” rồi bị bỏ, “R” cũng bị bỏ, chỉ “go” ở lại.')


FIGS61 = {'6-1-token-levels': levels61, '6-1-nfc': nfc61, '6-1-bpe': bpe61, '6-1-wordpiece': wordpiece61,
          '6-1-text-pipeline': pipeline61, '6-1-coef': coef61, '6-1-valid': valid61, '6-1-confusion': confusion61,
          '6-1-pattern': pattern61}

# ───────────────────────────── 6.2 ─────────────────────────────


def vec_panel(s, O, R, vecs, labels, cols, scale=1):
    for (vx, vy), lab, col in zip(vecs, labels, cols):
        ex, ey = O[0] + R * vx * scale, O[1] - R * vy * scale
        s.arrow(O[0], O[1], ex, ey, col, 2)
        s.label(ex + (8 if vx >= 0 else -8), ey - 6 if vy >= 0 else ey + 14, lab, 11.5, 'start' if vx >= 0 else 'end', col, 600)


def cosine62():
    s = Fig(640, 240)
    O, R = (180, 130), 44
    s.line(O[0] - 110, O[1], O[0] + 130, O[1], SOFT_LINE, 1)
    s.line(O[0], O[1] - 110, O[0], O[1] + 100, SOFT_LINE, 1)
    vec_panel(s, O, R, [(2, 2), (1, 0), (-1, -1)], ['tài liệu 1 (2, 2)', 'tài liệu 2 (1, 0)', 'tài liệu 3 (−1, −1)'], [GREEN, SAND, CLAY])
    s.arrow(O[0], O[1], O[0] + R, O[1] - R, BLUE, 3)
    s.label(40, 30, 'mũi tên đậm: query (1, 1)', 11.5, 'start', BLUE, 600)
    rows = [('tài liệu 1', '1', GREEN), ('tài liệu 2', '0.707', SAND), ('tài liệu 3', '−1', CLAY)]
    s.label(470, 60, 'cosine với query (1, 1)', 12, color=MUTED)
    for r, (nm, v, col) in enumerate(rows):
        y = 90 + r * 30
        s.label(450, y, nm, 12, 'end', TEXT)
        s.mono(480, y, v, 12.5, 'start', col, 600)
    s.label(470, 196, 'cosine chỉ nhìn hướng, không nhìn độ dài', 11.5, color=MUTED)
    s.save('6-2-cosine', 'Cùng hướng cho cosine 1 dù dài gấp đôi; lệch 45° cho 0.707; ngược hướng cho −1.')


def dotcos62():
    s = Fig(640, 220)
    O, R = (140, 170), 40
    s.line(O[0] - 20, O[1], O[0] + 150, O[1], SOFT_LINE, 1)
    s.line(O[0], O[1] + 20, O[0], O[1] - 140, SOFT_LINE, 1)
    s.arrow(O[0], O[1], O[0] + 3 * R, O[1], CLAY, 2)
    s.label(O[0] + 3 * R, O[1] + 16, 'A (3, 0)', 11.5, 'middle', CLAY, 600)
    s.arrow(O[0], O[1], O[0] + R, O[1] - R, GREEN, 2)
    s.label(O[0] + R + 8, O[1] - R - 4, 'B = q (1, 1)', 11.5, 'start', GREEN, 600)
    hx = [360, 450, 570]
    s.label(hx[1], 50, 'tích vô hướng', 12, color=MUTED)
    s.label(hx[2], 50, 'cosine', 12, color=MUTED)
    for r, (nm, d, c, col) in enumerate([('A', '3', '0.707', CLAY), ('B', '2', '1', GREEN)]):
        y = 82 + r * 30
        s.label(hx[0], y, nm, 12.5, color=col, weight=600)
        s.mono(hx[1], y, d, 12.5, 'middle', TEXT, 600 if nm == 'A' else 400)
        s.mono(hx[2], y, c, 12.5, 'middle', TEXT, 600 if nm == 'B' else 400)
    s.label(hx[1], 150, 'A thắng: dài', 11.5, color=CLAY)
    s.label(hx[2], 150, 'B thắng: cùng hướng', 11.5, color=GREEN)
    s.save('6-2-dotcos', 'Tích vô hướng ưu ái vector dài; cosine chỉ xét hướng.')


def pooling62():
    s = Fig(640, 220)
    toks = [('(2, 0)', 1), ('(0, 2)', 1), ('(9, 9)', 0), ('(9, 9)', 0)]
    for k, (v, m) in enumerate(toks):
        x = 30 + k * 90
        s.box(x, 40, 80, 34, 'none', BLUE if m else FAINT, r=6, width=0, opacity=.2 if m else .1)
        s.mono(x + 40, 57.5, v, 12.5, 'middle', TEXT if m else FAINT)
        s.mono(x + 40, 94, f'mask {m}', 11, 'middle', GREEN if m else MUTED)
    s.label(205, 24, 'hidden state của 4 vị trí', 12, color=MUTED)
    s.label(540, 52, 'mean cả 4:', 12, 'end', MUTED)
    s.mono(548, 52, '(5, 5)', 13, 'start', CLAY, 600)
    s.label(540, 84, 'mean có mask:', 12, 'end', MUTED)
    s.mono(548, 84, '(1, 1)', 13, 'start', GREEN, 600)
    s.mono(320, 150, 'Σ mᵢ hᵢ / Σ mᵢ = ((2, 0) + (0, 2)) / 2', 12.5, 'middle', TEXT)
    s.label(320, 182, 'padding không được giả định bằng 0: hidden state ở đó có thể là bất cứ gì', 11.5, color=MUTED)
    s.save('6-2-masked-pooling', 'Có mask ra (1, 1); lấy trung bình cả PAD bị kéo về (5, 5).')


def scores62():
    ns = lesson_ns('6.2', upto=6)
    L, E = ns['lexical_scores'], ns['learned_scores']
    q = ['quên truy_cập', 'mượn sách', 'lịch học']
    d = ['mật khẩu', 'mượn sách', 'thời khóa biểu']
    s = Fig(640, 230)
    for k, (M, title) in enumerate([(L, 'TF-IDF'), (E, 'embedding nhỏ')]):
        x0 = 160 + k * 250
        s.label(x0 + 100, 22, title, 12.5, color=TEXT, weight=600)
        vals = [[mnum(v, '{:.2f}') for v in r] for r in M]
        fills = {(i, j): ((GREEN if i == j else CLAY), .08 + .45 * max(M[i, j], 0)) for i in range(3) for j in range(3)}
        s.tiles(x0, 56, vals, 64, 34, BLUE, 4, fills, size=12)
        for j, nm in enumerate(d):
            s.label(x0 + j * 68 + 32, 44, nm, 10.5, color=MUTED)
        if k == 0:
            for i, nm in enumerate(q):
                s.label(x0 - 10, 56 + i * 38 + 17, nm, 11.5, 'end', MUTED)
    s.label(400, 206, 'hàng: query; cột: tài liệu; đường chéo là gold', 11.5, color=MUTED)
    s.save('6-2-scores', 'TF-IDF chỉ khớp được câu trùng từ; embedding tìm đúng cả câu khác từ.')


def words62():
    ns = lesson_ns('6.2', upto=7)
    f, p = ns['forget'], ns['password']
    s = Fig(640, 220)
    rows = [('quên', f, BLUE), ('mật_khẩu', p, CLAY), ('trung bình', (f + p) / 2, GREEN)]
    ax = s.axes(170, 30, 300, 150, (-.8, 1.2), (0, 3), xticks=[-.5, 0, .5, 1], yticks=[], grid=False, frame=False)
    s.line(ax.X(0), 26, ax.X(0), 186, LINE, 1)
    for r, (nm, v, col) in enumerate(rows):
        for c in range(3):
            y = 30 + r * 52 + c * 14
            s.rect(min(ax.X(0), ax.X(v[c])), y, abs(ax.X(v[c]) - ax.X(0)), 11, 'none', col, 2, .6, 0)
        s.label(160, 30 + r * 52 + 20, nm, 12.5, 'end', TEXT, 600 if r == 2 else 400)
    s.label(500, 70, 'ba chiều: tài khoản,', 11.5, 'start', MUTED)
    s.label(500, 88, 'thư viện, lịch học', 11.5, 'start', MUTED)
    s.label(500, 130, 'phần dư triệt tiêu', 11.5, 'start', GREEN)
    s.label(500, 148, 'trong câu train', 11.5, 'start', GREEN)
    s.save('6-2-words', 'Hai vector từ đối dấu nhau ở hai chiều nên trung bình rơi đúng (1, 0, 0).')


def ranks62():
    s = Fig(640, 200)
    rows = [('TF-IDF', [1, 1, 3], '0.667', '0.778', CLAY), ('embedding nhỏ', [1, 1, 1], '1.0', '1.0', GREEN)]
    qs = ['quên truy_cập', 'mượn sách', 'lịch học']
    for j, q in enumerate(qs):
        s.label(210 + j * 90, 30, q, 11, color=MUTED)
    s.label(500, 30, 'R@1', 11.5, color=MUTED)
    s.label(570, 30, 'MRR', 11.5, color=MUTED)
    for r, (nm, rk, r1, mrr, col) in enumerate(rows):
        y = 50 + r * 46
        s.label(150, y + 16, nm, 12.5, 'end', TEXT)
        for j, v in enumerate(rk):
            hit = v == 1
            s.box(180 + j * 90, y, 60, 32, 'none', GREEN if hit else CLAY, r=6, width=0, opacity=.25)
            s.mono(210 + j * 90, y + 16.5, f'hạng {v}', 11.5, 'middle', TEXT)
        s.mono(500, y + 16.5, r1, 12.5, 'middle', col, 600)
        s.mono(570, y + 16.5, mrr, 12.5, 'middle', col, 600)
    s.label(320, 166, 'hạng 1 của TF-IDF ở “quên truy_cập” chỉ nhờ phá hòa khi cả hàng bằng 0', 11.5, color=CLAY)
    s.save('6-2-ranks', 'Hạng của tài liệu đúng: TF-IDF 1, 1, 3; embedding 1 cả ba.')


def inbatch62():
    s = Fig(640, 250)
    B = 4
    c = 46
    vals = [['' for _ in range(B + 1)] for _ in range(B)]
    fills = {}
    for i in range(B):
        for j in range(B + 1):
            if j == i:
                fills[(i, j)] = (GREEN, .4)
            elif j == B:
                fills[(i, j)] = (CLAY, .35)
            else:
                fills[(i, j)] = (BLUE, .1)
    s.tiles(170, 50, vals, c, 36, BLUE, 4, fills)
    for j in range(B):
        s.mono(170 + j * (c + 4) + c / 2, 40, f'p{j + 1}', 11.5, 'middle', MUTED)
    s.mono(170 + B * (c + 4) + c / 2, 40, 'hard', 11.5, 'middle', CLAY)
    for i in range(B):
        s.mono(160, 50 + i * 40 + 18, f'q{i + 1}', 11.5, 'end', MUTED)
    s.label(440, 80, 'đường chéo: cặp đúng', 12, 'start', GREEN)
    s.label(440, 104, 'ô khác: in-batch negative', 12, 'start', BLUE)
    s.label(440, 128, 'cột thêm: hard negative', 12, 'start', CLAY)
    s.label(440, 160, 'mỗi hàng là softmax B + 1 lớp', 11.5, 'start', MUTED)
    s.save('6-2-inbatch', 'Mỗi query phải chấm tài liệu của cặp mình cao hơn tài liệu của các cặp khác trong batch.')


def chunks62():
    rng = np.random.default_rng(3)
    sc = np.clip(rng.normal(.25, .06, 40), .05, .45)
    sc[16] = .82
    s = Fig(640, 220)
    ax = s.axes(70, 30, 440, 140, (0, 41), (0, 1), xticks=[1, 17, 40], yticks=[0, .5, 1], xlabel='đoạn')
    for k, v in enumerate(sc, 1):
        s.rect(ax.X(k) - 4, ax.Y(v), 8, ax.Y(0) - ax.Y(v), 'none', CLAY if k == 17 else BLUE, 1, .7 if k == 17 else .3, 0)
    ax.hline(sc.mean(), FAINT, 1.2, '4 3')
    s.label(ax.X(41) + 8, ax.Y(sc.mean()), f'trung bình {sc.mean():.2f}', 11.5, 'start', MUTED)
    s.label(ax.X(41) + 8, ax.Y(.82), 'max 0.82', 11.5, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'cosine với query', 11.5, 'start', FAINT)
    s.save('6-2-chunks', 'Lấy điểm lớn nhất giữ được đoạn trả lời; lấy trung bình bị 39 đoạn khác pha loãng.')


def guess62():
    s = Fig(640, 210)
    ax = s.axes(120, 30, 420, 130, (0, 1), (0, 4), xticks=[0, .25, .5, .75, 1], yticks=[], grid=False)
    rows = [('G1', [.5, .5, .5]), ('G2', [.9, .88, .2]), ('G3', [.8, .45, .1]), ('G4', [.95, .94, .93])]
    cols = [BLUE, GREEN, CLAY]
    for r, (nm, vals) in enumerate(rows):
        y = ax.Y(3.5 - r)
        s.label(110, y, nm, 12, 'end', TEXT, 600 if nm == 'G3' else 400)
        for v, col in zip(vals, cols):
            s.rect(ax.X(v - .05), y - 6, ax.X(v + .05) - ax.X(v - .05), 12, 'none', col, 3, .35, 0)
    for k, (nm, col) in enumerate(zip('ABC', cols)):
        s.box(560, 50 + k * 22, 12, 12, 'none', col, r=2, width=0, opacity=.5)
        s.label(578, 56 + k * 22, nm, 11.5, 'start', MUTED)
    s.label(330, 196, 'mỗi thanh: cosine dự đoán ± 0.05; chỉ G3 có ba khoảng rời nhau', 11.5, color=MUTED)
    s.save('6-2-guess', 'Chỉ với G3, ba khoảng cosine rời nhau.')


FIGS62 = {'6-2-cosine': cosine62, '6-2-dotcos': dotcos62, '6-2-masked-pooling': pooling62, '6-2-scores': scores62,
          '6-2-words': words62, '6-2-ranks': ranks62, '6-2-inbatch': inbatch62, '6-2-chunks': chunks62, '6-2-guess': guess62}

# ───────────────────────────── 6.3 ─────────────────────────────

_T63 = {}


def run63():
    if not _T63:
        _T63['ns'] = lesson_ns('6.3', upto=3)
    return _T63['ns']


def masks63():
    s = Fig(640, 250)
    toks = ['t1', 't2', 't3', 'PAD', 'PAD']
    c = 30
    for k, (title, allow) in enumerate([('encoder BERT: chặn PAD', lambda i, j: j < 3),
                                        ('decoder causal: chặn PAD và tương lai', lambda i, j: j < 3 and j <= i)]):
        x0 = 80 + k * 290
        fills = {}
        for i in range(5):
            for j in range(5):
                ok = allow(i, j) and i < 3
                fills[(i, j)] = (GREEN, .4) if ok else (FAINT, .08)
        fills.update({(1, j): ((GREEN, .75) if allow(1, j) else (FAINT, .08)) for j in range(5)})
        s.tiles(x0, 50, [[''] * 5] * 5, c, c, FAINT, 3, fills, r=3)
        s.label(x0 + 80, 24, title, 12, color=TEXT, weight=600)
        for j, t in enumerate(toks):
            s.mono(x0 + j * (c + 3) + c / 2, 42, t, 9.5, 'middle', MUTED)
        if k == 0:
            for i, t in enumerate(toks):
                s.mono(x0 - 6, 50 + i * (c + 3) + c / 2, t, 9.5, 'end', MUTED)
        n = sum(allow(1, j) for j in range(5))
        s.mono(x0 + 80, 230, f'hàng t2: {n} key', 11.5, 'middle', GREEN)
    s.save('6-3-attention-masks', 'Encoder chỉ chặn cột PAD; causal mask còn chặn key tương lai.')


def mlm63():
    s = Fig(640, 230)
    s.label(320, 22, '15% vị trí được chọn để chấm loss', 12.5, color=TEXT, weight=600)
    parts = [('80%: thay [MASK]', ['An', '[MASK]', 'sách'], CLAY), ('10%: token ngẫu nhiên', ['An', 'bàn', 'sách'], SAND),
             ('10%: giữ nguyên', ['An', 'đọc', 'sách'], BLUE)]
    for r, (nm, toks, col) in enumerate(parts):
        y = 44 + r * 46
        s.label(190, y + 14, nm, 12, 'end', TEXT)
        x = 210
        for k, t in enumerate(toks):
            w = 18 + 8.5 * len(t)
            s.box(x, y, w, 28, 'none', col if k == 1 else FAINT, r=6, width=0, opacity=.3 if k == 1 else .12)
            s.mono(x + w / 2, y + 14.5, t, 12, 'middle', TEXT)
            x += w + 6
        s.mono(x + 14, y + 14.5, '→ đoán “đọc”', 12, 'start', GREEN)
    s.label(320, 200, 'nhãn luôn là token gốc; vị trí không được chọn mang -100', 11.5, color=MUTED)
    s.save('6-3-mlm', 'BERT chọn 15% vị trí: 80% thay MASK, 10% thay token ngẫu nhiên, 10% giữ nguyên.'.replace('[MASK]', 'token MASK'))


def heads63():
    s = Fig(640, 260)
    toks = ['CLS', 'An', 'đến', 'Hà', 'Nội', 'SEP']
    for k, t in enumerate(toks):
        x = 60 + k * 62
        s.box(x, 150, 52, 28, 'none', FAINT, r=5, width=0, opacity=.18)
        s.mono(x + 26, 164.5, t, 11, 'middle', TEXT)
        s.box(x, 104, 52, 28, 'none', BLUE, r=5, width=0, opacity=.2)
        s.mono(x + 26, 118.5, f'h{k}', 11, 'middle', TEXT)
        s.arrow(x + 26, 148, x + 26, 134, LINE, 1)
    s.label(240, 196, 'encoder · (B, L, d)', 11.5, color=MUTED)
    s.arrow(86, 102, 86, 66, CLAY, 1.4)
    s.box(40, 34, 100, 30, 'none', CLAY, r=6, width=0, opacity=.25)
    s.mono(90, 49.5, '(B, C)', 11.5, 'middle', TEXT)
    s.label(90, 22, 'head câu: đọc CLS', 11.5, color=CLAY, weight=600)
    for k in range(1, 6):
        x = 60 + k * 62 + 26
        s.arrow(x, 102, x, 80, GREEN, 1.1)
    s.box(166, 50, 300, 28, 'none', GREEN, r=6, width=0, opacity=.22)
    s.mono(316, 64.5, '(B, L, C): một nhãn mỗi vị trí', 11.5, 'middle', TEXT)
    s.label(316, 38, 'head token (NER)', 11.5, color=GREEN, weight=600)
    s.box(480, 100, 140, 70, 'none', SAND, r=8, width=0, opacity=.25)
    s.label(550, 120, 'head trích đoạn', 11.5, color=TEXT, weight=600)
    s.mono(550, 140, '(B, L, 2)', 11.5, 'middle', TEXT)
    s.label(550, 158, 'softmax theo L', 11, color=MUTED)
    s.save('6-3-two-heads', 'Ba cách đặt head: đọc CLS cho cả câu, mỗi token một nhãn, hoặc điểm đầu và cuối của đoạn.')


def attn63():
    import torch
    ns = run63()
    m = ns['model']
    sents = ['bài không hay', 'bài không tệ']
    ids = ns['make_batch'](sents)
    pos = torch.arange(ids.shape[1]).unsqueeze(0)
    with torch.no_grad():
        x = m.token_embedding(ids) + m.position_embedding(pos)
        _, w = m.encoder.layers[0].self_attn(x, x, x, key_padding_mask=ids.eq(0), need_weights=True, average_attn_weights=False)
    w = w.numpy()
    s = Fig(640, 270)
    c = 28
    for si, sent in enumerate(sents):
        toks = ['CLS'] + sent.split()
        for h in range(2):
            x0 = 64 + si * 316 + h * 128
            vals = [[f'{v:.2f}'.lstrip('0') if v >= .05 else '' for v in row] for row in w[si, h]]
            fills = {(i, j): (CLAY, .06 + .7 * w[si, h, i, j]) for i in range(4) for j in range(4)}
            s.tiles(x0, 64, vals, c, c, CLAY, 2, fills, size=9.5, r=2)
            s.label(x0 + 62, 50, f'head {h + 1}', 11, color=MUTED)
            for j, t in enumerate(toks):
                s.mono(x0 + j * (c + 2) + c / 2, 200 + (j % 2) * 11, t, 8.5, 'middle', MUTED)
            if h == 0:
                for i, t in enumerate(toks):
                    s.mono(x0 - 4, 64 + i * (c + 2) + c / 2, t, 8.5, 'end', MUTED)
        s.label(64 + si * 316 + 124, 24, f'“{sent}”', 12.5, color=TEXT, weight=600)
    s.label(320, 242, 'hàng CLS của hai câu gần như trùng nhau: head đọc CLS không thấy khác biệt hay/tệ', 11.5, color=MUTED)
    s.save('6-3-attn', 'Hàng CLS gần như giống hệt ở hai câu khác nhãn.')


def probs63():
    ns = run63()
    T, y, p = ns['train_texts'], ns['train_labels'].tolist(), ns['train_prob'].tolist()
    s = Fig(640, 280)
    ax = s.axes(200, 20, 320, 220, (0, 1), (10, 0), xticks=[0, .5, 1], yticks=[], grid=False)
    s.line(ax.X(.5), ax.y, ax.X(.5), ax.y + ax.h, FAINT, 1, '3 3')
    for i, (t, lab, pr) in enumerate(zip(T, y, p)):
        cy = ax.Y(i + .5)
        stuck = abs(pr - .5) < .05
        col = GREEN if lab == 1 else CLAY
        s.rect(ax.X(0), cy - 8, ax.X(pr) - ax.X(0), 16, 'none', col, 3, .55, 0)
        s.label(190, cy, t, 11.5, 'end', TEXT, 600 if stuck else 400)
        s.mono(ax.X(1) + 8, cy, f'{pr:.4f}', 10.5, 'start', CLAY if stuck else MUTED)
    s.label(ax.X(.5), 262, 'P(nhãn 1)', 11.5, color=FAINT)
    s.label(600, 100, 'nhãn 1', 11.5, 'start', GREEN)
    s.label(600, 120, 'nhãn 0', 11.5, 'start', CLAY)
    s.save('6-3-probs', 'Sau 100 bước, bốn câu “không hay”, “không tệ” vẫn đứng ở 0.5.')


def seeds63():
    rows = [('63', '0.2777', '0.8', '0/2'), ('1', '0.2781', '0.8', '0/2'), ('2', '0.0000', '1.0', '2/2'),
            ('3', '0.0001', '1.0', '0/2'), ('4', '0.0000', '1.0', '2/2'), ('5', '0.0001', '1.0', '1/2')]
    s = Fig(640, 250)
    hx = [180, 270, 370, 470]
    for x, h in zip(hx, ['seed', 'loss cuối', 'train', 'validation']):
        s.label(x, 24, h, 12, color=MUTED)
    for r, row in enumerate(rows):
        y = 50 + r * 30
        stuck = row[2] == '0.8'
        s.box(140, y - 12, 380, 26, 'none', CLAY if stuck else FAINT, r=5, width=0, opacity=.14 if stuck else .06)
        for x, v in zip(hx, row):
            s.mono(x, y + 1, v, 12, 'middle', TEXT)
    s.label(330, 236, 'kẹt ở 0.4 ln 2 hoặc học thuộc train; validation chỉ là may rủi trên hai câu', 11.5, color=MUTED)
    s.save('6-3-seeds', 'Cùng cách train, sáu seed cho kết quả rất khác nhau.')


def ner63():
    ns = lesson_ns('6.3', upto=5)
    toks, al = ns['tokens'], ns['aligned']
    names = {0: 'O', 1: 'B-PER', 2: 'B-LOC', -100: '-100'}
    wid = ns['word_ids']
    s = Fig(640, 220)
    x = 90
    for k, (t, a, w) in enumerate(zip(toks, al, wid)):
        wd = 26 + 8 * len(t)
        s.box(x, 60, wd, 32, 'none', FAINT if a == -100 else BLUE, r=6, width=0, opacity=.12 if a == -100 else .22)
        s.mono(x + wd / 2, 76.5, t, 12, 'middle', TEXT)
        s.mono(x + wd / 2, 46, 'None' if w is None else str(w), 10.5, 'middle', FAINT)
        s.mono(x + wd / 2, 114, names[a], 11.5, 'middle', MUTED if a == -100 else CLAY)
        x += wd + 8
    s.label(80, 46, 'word_id', 10.5, 'end', FAINT)
    s.label(80, 114, 'nhãn', 10.5, 'end', FAINT)
    s.label(320, 160, '4 vị trí góp loss; ##Nội cùng word_id 2 với Hà nên nhận -100', 11.5, color=MUTED)
    s.save('6-3-ner-alignment', 'Chỉ subword đầu của mỗi từ mang nhãn; CLS, SEP và subword tiếp nối nhận −100.')


def bio63():
    s = Fig(640, 200)
    rows = [('chép B-LOC cho cả hai', ['B-LOC', 'B-LOC'], 2), ('đổi subword sau thành I-LOC', ['B-LOC', 'I-LOC'], 1)]
    for r, (nm, labs, n) in enumerate(rows):
        y = 40 + r * 64
        s.label(210, y + 16, nm, 12, 'end', TEXT)
        for k, (t, l) in enumerate(zip(['Hà', '##Nội'], labs)):
            x = 230 + k * 96
            s.box(x, y, 86, 32, 'none', GREEN if l.startswith('B') else SAND, r=6, width=0, opacity=.25)
            s.mono(x + 43, y + 11, t, 11.5, 'middle', TEXT)
            s.mono(x + 43, y + 25, l, 10, 'middle', MUTED)
        if n == 2:
            s.box(228, y - 4, 90, 40, CLAY, 'none', r=7, width=1.4)
            s.box(324, y - 4, 90, 40, CLAY, 'none', r=7, width=1.4)
        else:
            s.box(228, y - 4, 186, 40, GREEN, 'none', r=7, width=1.4)
        s.label(440, y + 16, f'{n} thực thể', 12.5, 'start', CLAY if n == 2 else GREEN, 600)
    s.save('6-3-bio', 'Hai B-LOC liền nhau là hai thực thể; subword tiếp nối phải mang I-LOC.')


def window63():
    s = Fig(640, 200)
    W = 560
    sc = W / 700
    s.rect(40, 90, W, 24, 'none', FAINT, 3, .16, 0)
    s.mono(40 + W / 2, 102.5, 'hồ sơ 700 subword', 11.5, 'middle', MUTED)
    wins = [(0, 512, BLUE), (188, 700, CLAY)]
    for k, (a, b, col) in enumerate(wins):
        y = 40 if k == 0 else 130
        s.rect(40 + a * sc, y, (b - a) * sc, 28, 'none', col, 4, .3, 0)
        s.mono(40 + (a + b) / 2 * sc, y + 14.5, f'cửa sổ {k + 1}: {a}–{b}', 11.5, 'middle', TEXT)
    s.rect(40 + 188 * sc, 86, (512 - 188) * sc, 32, GREEN, 'none', 3, 1, 1.4)
    s.label(40 + 350 * sc, 184, 'vùng chồng lấp: giữ dự đoán của cửa sổ mà từ nằm gần giữa hơn', 11.5, color=GREEN)
    s.save('6-3-window', 'Văn bản dài chia thành các cửa sổ chồng lấp; mỗi từ lấy dự đoán từ cửa sổ mà nó gần giữa hơn.')


FIGS63 = {'6-3-attention-masks': masks63, '6-3-mlm': mlm63, '6-3-two-heads': heads63, '6-3-attn': attn63,
          '6-3-probs': probs63, '6-3-seeds': seeds63, '6-3-ner-alignment': ner63, '6-3-bio': bio63, '6-3-window': window63}

# ───────────────────────────── 6.4 ─────────────────────────────


def shift64():
    s = Fig(640, 200)
    seq = ['<bos>', 'em', 'học', 'toán', '<eos>']
    w, g = 86, 14
    for k in range(4):
        x = 70 + k * (w + g)
        s.box(x, 40, w, 30, 'none', BLUE, r=6, width=0, opacity=.18)
        s.mono(x + w / 2, 55.5, seq[k], 12, 'middle', TEXT)
        s.box(x, 120, w, 30, 'none', CLAY, r=6, width=0, opacity=.22)
        s.mono(x + w / 2, 135.5, seq[k + 1], 12, 'middle', TEXT)
        s.arrow(x + w / 2, 74, x + w / 2, 116, LINE, 1.1)
    s.label(60, 55, 'input', 12, 'end', MUTED)
    s.label(60, 135, 'label', 12, 'end', MUTED)
    s.label(500, 55, 'ids[:, :-1]', 11.5, 'start', BLUE)
    s.label(500, 135, 'ids[:, 1:]', 11.5, 'start', CLAY)
    s.label(270, 182, 'vị trí i chỉ đọc tiền tố đến i, dự đoán token i + 1', 11.5, color=MUTED)
    s.save('6-4-causal-shift', 'Input bỏ token cuối, label bỏ token đầu: vị trí i dự đoán token i + 1.')


def counts64():
    ns = lesson_ns('6.4', upto=1)
    bc, vocab = ns['bigram_counts'], ns['target_vocab']
    rows = ['<bos>', 'em', 'bạn', 'học', 'đọc', 'toán']
    cols = [v for v in vocab if v != '<unk>']
    s = Fig(640, 260)
    c = 48
    vals = [[str(bc[r][v]) if bc[r][v] else '' for v in cols] for r in rows]
    fills = {(i, j): (BLUE, .06 + .2 * bc[r][v]) for i, r in enumerate(rows) for j, v in enumerate(cols)}
    s.tiles(140, 50, vals, c, 26, BLUE, 3, fills, size=12)
    for j, v in enumerate(cols):
        s.mono(140 + j * (c + 3) + c / 2, 40, v, 10.5, 'middle', MUTED)
    for i, r in enumerate(rows):
        s.mono(130, 50 + i * 29 + 13, r, 11, 'end', MUTED)
    s.label(330, 244, 'ô trống: chưa gặp, xác suất 0 nếu không làm trơn', 11.5, color=MUTED)
    s.save('6-4-counts', 'Bảng đếm bigram gần như toàn 0.')


def smooth64():
    ns = lesson_ns('6.4', upto=2)
    vocab, bc = ns['target_vocab'], ns['bigram_counts']
    raw = np.array([bc['em'][v] for v in vocab], float)
    raw = raw / raw.sum()
    sm = ns['em_distribution']
    s = Fig(640, 230)
    ax = s.axes(80, 26, 440, 150, (-.5, len(vocab) - .5), (0, .7), xticks=[], yticks=[0, .25, .5], grid=False)
    for k, v in enumerate(vocab):
        s.rect(ax.X(k) - 16, ax.Y(raw[k]), 15, ax.Y(0) - ax.Y(raw[k]), 'none', FAINT, 2, .7, 0)
        s.rect(ax.X(k) + 1, ax.Y(sm[k]), 15, ax.Y(0) - ax.Y(sm[k]), 'none', CLAY, 2, .7, 0)
        s.mono(ax.X(k), ax.y + ax.h + 14, v, 10, 'middle', MUTED)
    s.mono(ax.X(vocab.index('học')) + 6, ax.Y(raw[vocab.index('học')]) - 8, '2/3 → 0.25', 11, 'middle', CLAY)
    s.box(540, 60, 12, 12, 'none', FAINT, r=2, width=0, opacity=.7)
    s.label(558, 66, 'không làm trơn', 11.5, 'start', MUTED)
    s.box(540, 84, 12, 12, 'none', CLAY, r=2, width=0, opacity=.7)
    s.label(558, 90, 'add-1', 11.5, 'start', MUTED)
    s.label(ax.x - 8, ax.y - 12, 'p(· | em)', 11.5, 'start', FAINT)
    s.save('6-4-smooth', 'Không làm trơn, nhiều token có xác suất 0; add-1 chia cho mọi token một phần.')


def nll64():
    ns = lesson_ns('6.4', upto=3)
    nd, vocab, BOS, EOS, UNK = ns['next_distribution'], ns['target_vocab'], ns['BOS'], ns['EOS'], ns['UNK']
    s = Fig(640, 240)
    texts = ['em học toán', 'em sách học', 'robot học toán']
    ax = s.axes(170, 30, 360, 170, (0, 9), (3, 0), xticks=[0, 3, 6, 9], yticks=[], grid=False)
    for r, t in enumerate(texts):
        words = [w if w in vocab else UNK for w in t.split()]
        toks = [BOS] + words + [EOS]
        x0 = 0
        y = ax.Y(r + .5)
        for k, (a, b) in enumerate(zip(toks, toks[1:])):
            v = -np.log(nd(a)[vocab.index(b)])
            s.rect(ax.X(x0) + .5, y - 13, ax.X(x0 + v) - ax.X(x0) - 1, 26, 'none', [BLUE, GREEN, SAND, CLAY][k], 2, .45, 0)
            x0 += v
        nll, cnt = ns['sentence_nll'](t)
        s.label(160, y - 6, t, 12, 'end', TEXT)
        s.mono(160, y + 10, f'PPL {np.exp(nll):.3f}', 10.5, 'end', MUTED)
    s.label(350, 226, 'mỗi đoạn là −log p của một token đích (cả EOS); cả thanh là tổng NLL', 11.5, color=MUTED)
    s.save('6-4-nll', 'Đảo trật tự hay gặp từ lạ đều làm perplexity tăng.')


def temperature64():
    ns = lesson_ns('6.4', upto=5)
    sm = ns['softmax_temperature']
    lg = ns['example_logits']
    s = Fig(640, 220)
    for k, T in enumerate([.5, 1.0, 2.0]):
        p = sm(lg, T)
        x0 = 60 + k * 195
        ax = s.axes(x0, 40, 150, 120, (-.5, 2.5), (0, 1), xticks=[], yticks=[0, .5, 1] if k == 0 else [], grid=False)
        for j, v in enumerate(p):
            s.rect(ax.X(j) - 18, ax.Y(v), 36, ax.Y(0) - ax.Y(v), 'none', CLAY if j == 0 else BLUE, 3, .6, 0)
            s.mono(ax.X(j), ax.Y(v) - 7, f'{v:.3f}'.lstrip('0'), 10.5, 'middle', TEXT)
            s.mono(ax.X(j), ax.y + ax.h + 14, f'z={lg[j]:g}', 10, 'middle', MUTED)
        s.label(x0 + 75, 22, f'T = {T:g}', 12.5, color=TEXT, weight=600)
    s.label(320, 206, 'thứ tự không đổi; T nhỏ làm nhọn, T lớn làm phẳng', 11.5, color=MUTED)
    s.save('6-4-temperature', 'Temperature nhỏ làm phân phối nhọn, lớn làm phẳng; thứ tự giữ nguyên.')


def topp64():
    s = Fig(640, 220)
    dists = [('bước nhọn', [.97, .01, .01, .01]), ('bước phẳng', [.3, .3, .2, .2])]
    for k, (nm, p) in enumerate(dists):
        x0 = 70 + k * 290
        cum = np.cumsum(p) - np.array(p)
        keep = cum < .9
        for j, v in enumerate(p):
            y = 50 + j * 32
            s.rect(x0, y, v * 200, 24, 'none', CLAY if keep[j] else FAINT, 3, .55 if keep[j] else .3, 0)
            s.mono(x0 + v * 200 + 8, y + 12, f'{v:g}', 11, 'start', TEXT if keep[j] else FAINT)
        s.label(x0 + 100, 30, f'{nm}: giữ {int(keep.sum())}', 12.5, color=TEXT, weight=600)
    s.label(320, 200, 'top-p 0.9 giữ token cho tới khi tổng dồn đạt 0.9, kể cả token vượt ngưỡng', 11.5, color=MUTED)
    s.save('6-4-topp', 'Top-p 0.9: bước nhọn giữ 1 token, bước phẳng giữ cả 4.')


def greedy64():
    s = Fig(640, 230)
    s.circle(60, 115, 8, TEXT, PAPER, 1.6)
    s.mono(60, 140, 'bắt đầu', 10.5, 'middle', MUTED)
    for (lab, p, pe, y, col) in [('A', .6, .5, 60, BLUE), ('B', .4, .95, 170, CLAY)]:
        s.curve(68, 115, 196, y, 0, col, 1.8)
        s.mono(130, (115 + y) / 2 - 6 if y < 115 else (115 + y) / 2 + 14, f'{p}', 11.5, 'middle', col)
        s.box(200, y - 16, 50, 32, 'none', col, r=6, width=0, opacity=.25)
        s.mono(225, y + .5, lab, 13, 'middle', TEXT, 600)
        s.arrow(254, y, 340, y, col, 1.6)
        s.mono(297, y - 8, f'{pe}', 11.5, 'middle', col)
        s.box(344, y - 16, 60, 32, 'none', FAINT, r=6, width=0, opacity=.2)
        s.mono(374, y + .5, 'EOS', 12, 'middle', TEXT)
        s.mono(420, y + .5, f'= {p * pe:.2f}', 13, 'start', col, 600)
    s.label(486, 60, 'greedy đi nhánh này', 11.5, 'start', BLUE)
    s.label(486, 170, 'chuỗi tốt hơn', 11.5, 'start', CLAY)
    s.label(320, 220, 'beam 2 giữ cả A lẫn B nên tìm ra B EOS', 11.5, color=MUTED)
    s.save('6-4-greedy-paths', 'Greedy chọn A trước nên lỡ chuỗi B EOS có xác suất cao hơn; beam 2 tìm ra nó.')


def beamx64():
    s = Fig(640, 220)
    ax = s.axes(80, 30, 420, 150, (0, 1), (0, .45), xticks=[0, .25, .5, .75, 1], yticks=[0, .2, .4], xlabel='x = p(EOS | B)')
    xs = np.linspace(0, 1, 101)
    ax.line(xs, .4 * xs, CLAY, 2.2)
    ax.hline(.3, BLUE, 2, None)
    s.line(ax.X(.75), ax.y, ax.X(.75), ax.y + ax.h, FAINT, 1, '3 3')
    s.circle(ax.X(.75), ax.Y(.3), 4.5, TEXT, PAPER, 2)
    s.mono(ax.X(.75) - 8, ax.Y(.3) - 10, 'x = 0.75', 11.5, 'end', TEXT)
    s.label(ax.X(1) + 8, ax.Y(.3), 'A EOS: 0.30', 12, 'start', BLUE, 600)
    s.label(ax.X(1) + 8, ax.Y(.4), 'B EOS: 0.4x', 12, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'xác suất cả chuỗi', 11.5, 'start', FAINT)
    s.save('6-4-beamx', 'Greedy chỉ không kém khi x ≤ 0.75.')


FIGS64 = {'6-4-causal-shift': shift64, '6-4-counts': counts64, '6-4-smooth': smooth64, '6-4-nll': nll64,
          '6-4-temperature': temperature64, '6-4-topp': topp64, '6-4-greedy-paths': greedy64, '6-4-beamx': beamx64}

# ───────────────────────────── 6.5 ─────────────────────────────

_T65 = {}


def run65():
    if not _T65:
        _T65['ns'] = lesson_ns('6.5', upto=6)
    return _T65['ns']


def encdec65():
    s = Fig(640, 260)
    src = ['A', 'B', 'PAD']
    tgt = ['BOS', 'B', 'A']
    for k, t in enumerate(src):
        x = 40 + k * 56
        s.box(x, 190, 48, 28, 'none', FAINT if t == 'PAD' else BLUE, r=5, width=0, opacity=.12 if t == 'PAD' else .22)
        s.mono(x + 24, 204.5, t, 11, 'middle', FAINT if t == 'PAD' else TEXT)
    s.box(30, 100, 180, 56, 'none', BLUE, r=8, width=0, opacity=.14)
    s.label(120, 118, 'encoder', 12.5, color=TEXT, weight=600)
    s.label(120, 138, 'self-attention, mask PAD', 11, color=MUTED)
    s.arrow(120, 186, 120, 160, LINE, 1.1)
    s.label(120, 240, 'nguồn: đọc cả câu', 11.5, color=MUTED)
    for k, t in enumerate(tgt):
        x = 420 + k * 64
        s.box(x, 190, 56, 28, 'none', CLAY, r=5, width=0, opacity=.22)
        s.mono(x + 28, 204.5, t, 11, 'middle', TEXT)
    s.box(400, 100, 210, 56, 'none', CLAY, r=8, width=0, opacity=.16)
    s.label(505, 118, 'decoder', 12.5, color=TEXT, weight=600)
    s.label(505, 138, 'self-attention, causal mask', 11, color=MUTED)
    s.arrow(505, 186, 505, 160, LINE, 1.1)
    s.label(505, 240, 'đích: chỉ tiền tố đã có', 11.5, color=MUTED)
    s.arrow(214, 128, 396, 128, GREEN, 1.8)
    s.label(305, 112, 'cross-attention', 12, color=GREEN, weight=600)
    s.label(305, 146, 'query từ đích, key/value từ nguồn', 11, color=MUTED)
    s.label(305, 162, 'vẫn mask PAD nguồn', 11, color=MUTED)
    s.arrow(505, 96, 505, 64, LINE, 1.1)
    s.mono(505, 52, 'p(y_t | y_<t, x)', 12, 'middle', TEXT)
    s.save('6-5-encoder-decoder', 'Ba chỗ dùng attention: self-attention của encoder, self-attention có causal mask của decoder, cross-attention.')


def teacher65():
    ns = lesson_ns('6.5', upto=1)
    src, dec, lab = ns['source_ids'][1].tolist(), ns['decoder_ids'][1].tolist(), ns['target_ids'][1].tolist()
    name = {0: 'PAD', 1: 'BOS', 2: 'EOS', 3: 'A', 4: 'B', 5: 'C'}
    s = Fig(640, 210)
    s.label(110, 30, 'nguồn', 12, 'end', MUTED)
    for k, t in enumerate(src):
        s.box(130 + k * 70, 16, 60, 28, 'none', BLUE, r=5, width=0, opacity=.2)
        s.mono(160 + k * 70, 30.5, f'{name[t]} ({t})', 11, 'middle', TEXT)
    for k, (a, b) in enumerate(zip(dec, lab)):
        x = 130 + k * 110
        s.box(x, 80, 90, 30, 'none', FAINT, r=6, width=0, opacity=.2)
        s.mono(x + 45, 95.5, f'{name[a]} ({a})', 11.5, 'middle', TEXT)
        s.box(x, 150, 90, 30, 'none', CLAY, r=6, width=0, opacity=.25)
        s.mono(x + 45, 165.5, f'{name[b]} ({b})', 11.5, 'middle', TEXT)
        s.arrow(x + 45, 114, x + 45, 146, LINE, 1.1)
        if k < 2:
            s.curve(x + 90, 165, x + 112, 95, -.3, GREEN, 1.2)
    s.label(110, 95, 'decoder input', 12, 'end', MUTED)
    s.label(110, 165, 'label', 12, 'end', MUTED)
    s.label(320, 200, 'label bước trước thành input bước sau', 11.5, color=GREEN)
    s.save('6-5-teacher-forcing', 'Teacher forcing: token đúng của bước trước làm input cho bước sau.')


def loss65():
    ns = run65()
    h = np.array(ns['loss_history'])
    s = Fig(640, 220)
    ax = s.axes(80, 26, 420, 150, (0, 220), (-4, .5), xticks=[0, 50, 100, 150, 220], yticks=[-4, -2, 0], yfmt='', xlabel='bước')
    for e in (-4, -2, 0):
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    ax.line(np.arange(len(h)), np.log10(h), BLUE, 2)
    v = float(ns['valid_loss'])
    ax.hline(np.log10(v), CLAY, 1.6, '5 4')
    s.label(ax.X(220) + 8, ax.Y(np.log10(h[-1])), f'train {h[-1]:.4f}', 11.5, 'start', BLUE, 600)
    s.label(ax.X(220) + 8, ax.Y(np.log10(v)), f'validation {v:.4f}', 11.5, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 12, 'loss (teacher forcing)', 11.5, 'start', FAINT)
    s.save('6-5-loss', 'Train loss xuống gần 0, validation loss vẫn cao.')


def nll65():
    s = Fig(640, 210)
    rows = [('C B', [0.027, 0.729, 0.003]), ('C C', [0.002, 6.804, 0.003])]
    hdr = ['vị trí 1', 'vị trí 2', 'EOS']
    for j, h in enumerate(hdr):
        s.label(200 + j * 90 + 40, 30, h, 11.5, color=MUTED)
    for r, (nm, vals) in enumerate(rows):
        y = 44 + r * 50
        s.label(190, y + 20, nm, 12.5, 'end', TEXT)
        for j, v in enumerate(vals):
            s.box(200 + j * 90, y, 80, 40, 'none', CLAY, r=6, width=0, opacity=.08 + .6 * min(v / 6.8, 1))
            s.mono(240 + j * 90, y + 20.5, f'{v:g}', 12.5, 'middle', TEXT)
    s.label(500, 70, 'C C, bước 2 sau BOS C:', 11.5, 'start', MUTED)
    s.mono(500, 92, 'A 0.994  C 0.001', 12, 'start', CLAY)
    s.label(500, 120, 'tiền tố đúng vẫn chọn A', 11.5, 'start', MUTED)
    s.label(320, 190, 'trung bình sáu ô bằng 1.2613; riêng 6.804 chiếm gần 90% tổng', 11.5, color=MUTED)
    s.save('6-5-nll', 'Lỗi dồn vào vị trí thứ hai của C C.')


def beam65():
    rows = [('C B', [('B C', -.759), ('B A', -1.153), ('B B', -2.047)]), ('C C', [('C A', -.009), ('C', -5.279), ('A C', -6.142)])]
    s = Fig(640, 220)
    for r, (src, cands) in enumerate(rows):
        x0 = 60 + r * 300
        s.label(x0 + 120, 24, f'nguồn {src} · beam 3', 12, color=TEXT, weight=600)
        for k, (c, v) in enumerate(cands):
            y = 44 + k * 40
            w = (7 + v) / 7 * 160
            gold = (src == 'C B' and c == 'B C') or (src == 'C C' and c == 'C C')
            s.rect(x0 + 60, y, w, 28, 'none', GREEN if gold else (CLAY if k == 0 else BLUE), 3, .5 if k == 0 else .25, 0)
            s.mono(x0 + 50, y + 14.5, c, 12, 'end', TEXT)
            s.mono(x0 + 64 + w, y + 14.5, f'{v:g}', 11, 'start', MUTED)
    s.label(320, 196, 'tổng log-prob; C C không có trong top 3: beam chỉ tìm lỗi model tin chắc', 11.5, color=MUTED)
    s.save('6-5-beam', 'Beam 3: C B ra đúng B C; C C ra C A, đáp án đúng không lọt vào top 3.')


def crossattn65():
    s = Fig(640, 220)
    O, R = (130, 150), 60
    s.line(O[0] - 20, O[1], O[0] + 150, O[1], SOFT_LINE, 1)
    s.line(O[0], O[1] + 20, O[0], O[1] - 130, SOFT_LINE, 1)
    s.arrow(*O, O[0] + R, O[1], BLUE, 2.4)
    s.label(O[0] + R + 6, O[1] + 16, 'q = k₁', 11.5, 'start', BLUE, 600)
    s.arrow(*O, O[0], O[1] - R, FAINT, 1.6)
    s.label(O[0] + 8, O[1] - R, 'k₂', 11.5, 'start', MUTED)
    s.mono(300, 60, 'điểm  (0.707, 0)', 12.5, 'start', TEXT)
    s.mono(300, 88, 'softmax (0.67, 0.33)', 12.5, 'start', TEXT)
    s.mono(300, 116, '0.67·(2, 0) + 0.33·(0, 2)', 12.5, 'start', MUTED)
    s.mono(300, 144, 'context (1.34, 0.66)', 13, 'start', CLAY, 600)
    s.label(400, 186, 'vector đọc được là tổ hợp có trọng số của các value', 11.5, color=MUTED)
    s.save('6-5-cross-attention', 'Trọng số 0.67 và 0.33 trộn hai value thành context (1.34, 0.66).')


def padctx65():
    s = Fig(640, 200)
    rows = [('có mask', [.25, .75, 0], '(1, 4.5)', GREEN), ('quên mask', [1 / 7, 3 / 7, 3 / 7], '≈ (4.43, 6.43)', CLAY)]
    vals = ['(4, 0)', '(0, 6)', 'PAD (9, 9)']
    for j, v in enumerate(vals):
        s.mono(200 + j * 100 + 45, 30, v, 11, 'middle', MUTED)
    for r, (nm, w, ctx, col) in enumerate(rows):
        y = 44 + r * 56
        s.label(190, y + 20, nm, 12.5, 'end', TEXT)
        for j, v in enumerate(w):
            s.box(200 + j * 100, y, 90, 40, 'none', col, r=6, width=0, opacity=.08 + .6 * v)
            s.mono(245 + j * 100, y + 20.5, f'{v:.2f}', 12, 'middle', TEXT)
        s.mono(510, y + 20.5, ctx, 12.5, 'start', col, 600)
    s.label(320, 180, 'value của PAD kéo context đi xa khi mask bị quên', 11.5, color=MUTED)
    s.save('6-5-padctx', 'Quên mask PAD thì context bị kéo lệch.')


def bleu65():
    rows = [('họp họp họp họp', .25, 0, .472, 0), ('câu lạc bộ họp thứ sáu', 1, .8, .846, .757),
            ('câu lạc bộ họp vào thứ bảy', .857, .833, 1, .845)]
    s = Fig(640, 220)
    hx = [330, 400, 470, 550]
    for x, h in zip(hx, ['p1', 'p2', 'BP', 'BLEU-2']):
        s.label(x, 34, h, 12, color=MUTED)
    s.label(320, 14, 'tham chiếu: câu lạc bộ họp vào thứ sáu', 11.5, color=MUTED)
    for r, (c, p1, p2, bp, b) in enumerate(rows):
        y = 64 + r * 40
        s.label(300, y, c, 12, 'end', TEXT)
        for x, v in zip(hx, (p1, p2, bp, b)):
            s.mono(x, y, f'{v:.3f}', 12, 'middle', CLAY if x == hx[3] else TEXT, 600 if x == hx[3] else 400)
    s.box(530, 136, 42, 22, CLAY, 'none', r=5, width=1.4)
    s.label(320, 200, 'câu sai thứ bảy được điểm cao hơn câu đúng: overlap n-gram không kiểm sự thật', 11.5, color=MUTED)
    s.save('6-5-bleu', 'Câu lặp từ bị clipping về 0; câu đúng mà ngắn bị phạt; câu sai vẫn có thể được điểm cao.')


def t5shift65():
    s = Fig(640, 230)
    rows = [('labels', ['4', '3', '1', '-100'], CLAY), ('decoder input', ['0', '4', '3', '1'], BLUE),
            ('labels có sẵn 0', ['0', '4', '3', '1'], SAND), ('dịch hai lần', ['0', '0', '4', '3'], CLAY)]
    for r, (nm, toks, col) in enumerate(rows):
        y = 30 + r * 46 + (12 if r >= 2 else 0)
        s.label(170, y + 14, nm, 12, 'end', TEXT)
        for k, t in enumerate(toks):
            s.box(184 + k * 60, y, 52, 28, 'none', FAINT if t == '-100' else col, r=5, width=0, opacity=.12 if t == '-100' else .25)
            s.mono(210 + k * 60, y + 14.5, t, 12, 'middle', TEXT)
    s.label(480, 60, 'đúng: thư viện tự dịch', 12, 'start', GREEN)
    s.label(480, 160, 'sai: vị trí đầu bị dạy', 12, 'start', CLAY)
    s.label(480, 178, 'đoán PAD', 12, 'start', CLAY)
    s.save('6-5-t5shift', 'T5 tự dịch labels thành decoder input (số từ code bài): labels 4 3 1 cho input 0 4 3 1; nếu labels đã có sẵn token mở đầu 0 thì bị dịch hai lần thành 0 0 4 3.')


FIGS65 = {'6-5-encoder-decoder': encdec65, '6-5-teacher-forcing': teacher65, '6-5-loss': loss65, '6-5-nll': nll65,
          '6-5-beam': beam65, '6-5-cross-attention': crossattn65, '6-5-padctx': padctx65, '6-5-bleu': bleu65,
          '6-5-t5shift': t5shift65}

# ───────────────────────────── 6.6 ─────────────────────────────


def stages66():
    s = Fig(640, 200)
    boxes = [('pretraining', 'đoán token kế\ntrên kho văn bản lớn', BLUE), ('base model', 'biết viết tiếp', FAINT),
             ('SFT', 'chỉ dẫn và' + chr(10) + 'trả lời mẫu', CLAY), ('RLHF / DPO', 'tối ưu theo' + chr(10) + 'ưu tiên', CLAY), ('instruct model', 'làm theo chỉ dẫn', GREEN)]
    w, g = 106, 18
    for k, (nm, sub, col) in enumerate(boxes):
        x = 20 + k * (w + g)
        model = k in (1, 4)
        s.box(x, 60, w, 56, 'none', col, r=8 if model else 4, width=0, opacity=.28 if model else .16)
        s.label(x + w / 2, 80, nm, 12, color=TEXT, weight=600)
        for j, line in enumerate(sub.split('\n')):
            s.label(x + w / 2, 98 + j * 14, line, 10.5, color=MUTED)
        if k:
            s.arrow(x - g + 2, 88, x - 2, 88, LINE, 1.1)
    s.label(330, 160, 'post-training', 12, color=CLAY, weight=600)
    s.path('M 268,140 L 268,148 L 494,148 L 494,140', CLAY, 1.2)
    s.save('6-6-stages', 'Base model học đoán token; post-training (SFT, RLHF, DPO) biến nó thành instruct model.')


def checks66():
    ns = lesson_ns('6.6', upto=1)
    cases = ns['validator_cases']
    va = ns['validate_answer']
    s = Fig(640, 240)
    for r, raw in enumerate(cases):
        y = 36 + r * 36
        ok, reason, _ = va(raw)
        disp = raw if len(raw) < 46 else raw[:43] + '…'
        s.mono(30, y + 14, disp, 11, 'start', TEXT)
        s.box(380, y, 24, 26, 'none', GREEN if ok else CLAY, r=5, width=0, opacity=.35)
        s.mono(392, y + 13.5, '✓' if ok else '✗', 12, 'middle', TEXT, 600)
        s.label(414, y + 13, reason.replace('Students phải là số nguyên không âm hoặc null', 'students sai kiểu'), 11.5, 'start', GREEN if ok else CLAY)
    s.label(30, 20, 'chuỗi model trả về', 11.5, 'start', MUTED)
    s.label(414, 20, 'validate_answer', 11.5, 'start', MUTED)
    s.save('6-6-checks', 'Validator chỉ nhận chuỗi đầu; bốn chuỗi còn lại bị từ chối.')


def levels66():
    s = Fig(640, 220)
    lv = [('1. cú pháp', 'json.loads đọc được', 'Đây là kết quả: {…}', BLUE), ('2. schema', 'đúng khóa, kiểu, miền', '{"students": "18", …}', SAND),
          ('3. nội dung', 'khớp gold từ nguồn', '{"date": "20/10", …} (kế hoạch cũ)', CLAY)]
    for r, (nm, check, fail, col) in enumerate(lv):
        y = 30 + r * 58
        s.box(40 + r * 30, y, 220 - r * 30, 44, 'none', col, r=7, width=0, opacity=.22)
        s.label(50 + r * 30, y + 15, nm, 12.5, 'start', TEXT, 600)
        s.label(50 + r * 30, y + 32, check, 11, 'start', MUTED)
        s.mono(290, y + 22, fail, 11, 'start', MUTED)
    s.label(290, 16, 'ví dụ trượt ở mức này', 11.5, 'start', FAINT)
    s.label(320, 206, 'qua mức trên chưa chắc qua mức dưới: prompt injection qua được cả hai mức đầu', 11.5, color=MUTED)
    s.save('6-6-levels', 'Ba mức kiểm output: cú pháp JSON, schema, nội dung.')


def messages66():
    ns = lesson_ns('6.6', upto=2)
    msgs = ns['messages']
    col = {'system': SAND, 'user': BLUE, 'assistant': GREEN}
    s = Fig(640, 280)
    for k, m in enumerate(msgs):
        y = 20 + k * 40
        c = m['content']
        if m['role'] == 'system':
            c = 'Trích ngày/tháng tổ chức và số học sinh… chỉ trả JSON…'
        c = c if len(c) <= 62 else c[:59] + '…'
        s.box(30, y, 100, 30, 'none', col[m['role']], r=6, width=0, opacity=.3)
        s.mono(80, y + 15.5, m['role'], 11.5, 'middle', TEXT)
        s.mono(142, y + 15.5, c, 10.5, 'start', TEXT)
    s.path('M 620,64 L 626,64 L 626,182 L 620,182', MUTED, 1.2)
    s.label(600, 270, 'hai cặp few-shot rồi thông báo cần trích', 11.5, 'end', MUTED)
    s.save('6-6-messages', 'Prompt gồm một system, hai cặp ví dụ, rồi thông báo cần trích.')


def grid66():
    ns = lesson_ns('6.6', upto=3)
    dev, rb, va = ns['dev_examples'], ns['regex_baseline'], ns['validate_answer']
    s = Fig(640, 250)
    hx = [70, 300, 400, 500]
    for x, h in zip(hx, ['thông báo', 'schema', 'date', 'students']):
        s.label(x, 26, h, 12, 'start' if x == hx[0] else 'middle', MUTED)
    short = ['Ngày 12/10 … 18 học sinh', 'chưa thông báo ngày, 20 học sinh', 'Ngày 15/10, có 7 em', 'Kế hoạch 20/10, thực tế 21/10']
    for r, (notice, gold) in enumerate(dev):
        ok, _, ans = va(rb(notice))
        y = 46 + r * 44
        s.label(hx[0], y + 15, short[r], 11.5, 'start', TEXT)
        for x, good in [(hx[1], ok), (hx[2], ans['date'] == gold['date']), (hx[3], ans['students'] == gold['students'])]:
            s.box(x - 30, y, 60, 30, 'none', GREEN if good else CLAY, r=6, width=0, opacity=.3)
            val = '✓' if x == hx[1] else str(ans['date' if x == hx[2] else 'students'])
            s.mono(x, y + 15.5, '✓' if (x == hx[1] and ok) else (val if good or x != hx[1] else '✗'), 11, 'middle', TEXT)
    s.label(320, 236, 'hợp schema 4/4, exact 2/4: lỗi nội dung, không phải lỗi JSON', 11.5, color=MUTED)
    s.save('6-6-extraction-grid', 'Regex hợp schema cả bốn ca nhưng sai nội dung ở hai ca.')


def rag66():
    s = Fig(640, 210)
    s.rect(60, 40, 520, 34, 'none', FAINT, 4, .14, 0)
    s.rect(60, 40, 520 * .6, 34, 'none', BLUE, 4, .3, 0)
    s.label(60 + 260 * .6, 57, 'đoạn đúng trong top-3: 60', 12, color=TEXT)
    s.label(60 + 520 * .8, 57, 'thiếu đoạn đúng: 40', 12, color=CLAY)
    s.rect(60, 100, 520 * .57, 34, 'none', GREEN, 4, .4, 0)
    s.rect(60 + 520 * .57, 100, 520 * .03, 34, 'none', CLAY, 1, .5, 0)
    s.label(60 + 260 * .57, 117, 'LLM trả đúng: 57', 12, color=TEXT)
    s.mono(60 + 520 * .6 + 6, 117, '3 sai', 11, 'start', CLAY)
    s.label(50, 57, 'retriever', 11.5, 'end', MUTED)
    s.label(50, 117, 'đọc', 11.5, 'end', MUTED)
    s.label(320, 170, 'recall@3 = 0.6 là trần của cả hệ; tầng đọc đúng 57/60', 12, color=TEXT)
    s.label(320, 192, 'sửa retriever trước', 11.5, color=CLAY, weight=600)
    s.save('6-6-rag', 'Nút thắt là retriever: chỉ 60/100 câu có đoạn đúng trong top-3.')


def memory66():
    s = Fig(640, 180)
    B, L, n, h, dh, b = 1, 1024, 24, 2, 64, 2
    base = 2 * B * L * n * h * dh * b / 2 ** 20
    rows = [('B=1, L=1024, h=2', base, GREEN), ('B=4, L=2048, h=2', base * 8, BLUE)]
    for r, (nm, v, col) in enumerate(rows):
        y = 40 + r * 46
        s.label(210, y + 14, nm, 12, 'end', TEXT)
        s.rect(220, y, v / 100 * 340, 28, 'none', col, 3, .55, 0)
        s.mono(226 + v / 100 * 340, y + 14.5, f'{v:g} MiB', 12, 'start', col, 600)
    s.mono(320, 150, 'KV bytes ≈ 2·B·L·n·h·d_h·b  (n = 24, d_h = 64, b = 2)', 12, 'middle', MUTED)
    s.save('6-6-memory-budget', 'KV cache tăng tuyến tính theo batch và độ dài: 12 MiB thành 96 MiB.')


def leftpad66():
    s = Fig(640, 220)
    for k, (title, left) in enumerate([('pad phải', False), ('pad trái', True)]):
        x0 = 40 + k * 300
        s.label(x0 + 130, 24, title, 12.5, color=TEXT, weight=600)
        for r, n in enumerate([30, 22]):
            y = 44 + r * 50
            cells = 15
            real = n // 2
            pad = cells - real
            for j in range(cells):
                is_pad = (j < pad) if left else (j >= real)
                s.box(x0 + j * 16, y, 14, 26, 'none', FAINT if is_pad else BLUE, r=2, width=0, opacity=.14 if is_pad else .32)
            s.box(x0 + cells * 16, y, 22, 26, 'none', CLAY, r=3, width=0, opacity=.5)
            s.mono(x0 + cells * 16 + 11, y + 13.5, '+', 12, 'middle', TEXT)
        s.label(x0 + 130, 160, 'token mới nối sau pad' if not left else 'token mới nối ngay sau token thật', 11.5, color=CLAY if not left else GREEN)
    s.label(320, 200, 'ô xanh: token thật; ô mờ: pad; ô cam: token generate nối vào cuối hàng', 11.5, color=MUTED)
    s.save('6-6-leftpad', 'Sinh theo batch với decoder-only: generate nối token mới vào cuối mỗi hàng; pad phải làm prompt ngắn có token mới đứng sau pad, pad trái để token mới nối ngay sau token thật.')


FIGS66 = {'6-6-stages': stages66, '6-6-checks': checks66, '6-6-levels': levels66, '6-6-messages': messages66,
          '6-6-extraction-grid': grid66, '6-6-rag': rag66, '6-6-memory-budget': memory66, '6-6-leftpad': leftpad66}

FIGS = {**FIGS61, **FIGS62, **FIGS63, **FIGS64, **FIGS65, **FIGS66}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
