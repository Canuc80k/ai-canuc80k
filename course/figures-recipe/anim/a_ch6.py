"""Hình động chương 6 (ngôn ngữ). Văn bản thật: chính lời giảng của giáo trình (content/phase-*/*.md).
Model thật: paraphrase-multilingual-MiniLM-L12-v2, Qwen2.5-0.5B, whisper-base.en (cache Hugging Face trên máy)."""
import os
import re
import sys
import unicodedata
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

os.environ.setdefault('HF_HUB_OFFLINE', '1')
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, font,  # noqa: E402
                  plain_axes, fig_frame, grab)
from a_ch2 import bare  # noqa: E402

CONTENT = Path(__file__).resolve().parents[2] / 'content'
DATA = Path(__file__).resolve().parent / 'data'


def course_text():
    """Lời giảng của mọi bài (bỏ code, công thức, cú pháp Markdown), chữ thường, chuẩn NFC."""
    parts = []
    for p in sorted(CONTENT.glob('phase-*/*.md')):
        t = p.read_text(encoding='utf-8')
        t = re.sub(r'```.*?```', ' ', t, flags=re.S)
        t = re.sub(r'\$\$.*?\$\$|\$[^$\n]*\$|`[^`]*`|!\[[^\]]*\]\([^)]*\)|\]\([^)]*\)|https?://\S+', ' ', t, flags=re.S)
        t = re.sub(r'^:::.*$|^[-*#>|].*?(?=\w)', ' ', t, flags=re.M)
        parts.append(t)
    return unicodedata.normalize('NFC', ' '.join(parts).lower())


def chips(cv, pieces, x0, y0, w, theme, size=26, gap=6, line=50, start_word=None):
    """Vẽ chuỗi token thành các ô màu xen kẽ; trả về y cuối. pieces: [(chữ, bắt đầu từ mới?)]."""
    t = THEMES[theme]
    d = ImageDraw.Draw(cv, 'RGBA')
    f = font(size)
    x, y = x0, y0
    k = 0
    for s, new_word in pieces:
        tw = d.textlength(s, font=f)
        if new_word and x > x0:
            x += 12
        if x + tw + 14 > x0 + w:
            x, y = x0, y + line
        c = (t['blue'], t['clay'])[k % 2]
        d.rounded_rectangle([x, y, x + tw + 14, y + size + 14], radius=7, fill=hexrgb(c, 46), outline=hexrgb(c, 150), width=2)
        d.text((x + 7, y + 7 + size * .5), s, fill=hexrgb(t['text']), font=f, anchor='lm')
        x += tw + 14 + gap
        k += 1
    return y + line


# ───────────────────────────── 6.1 ─────────────────────────────

SENT61 = 'Học sinh luyện tokenization và overfitting trước kỳ thi IOAI.'


def a6_1_bpe():
    """BPE học trên chính lời giảng của giáo trình: tăng cỡ từ vựng thì cùng một câu được cắt thành ít mảnh hơn."""
    from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers
    corpus = course_text()
    lines = [l for l in corpus.split('\n') if l.strip()]
    sizes = [0, 150, 300, 600, 1200, 2400, 4000]
    res = []
    for vs in sizes:
        tk = Tokenizer(models.BPE(unk_token='[UNK]'))
        tk.normalizer = normalizers.Sequence([normalizers.NFC(), normalizers.Lowercase()])
        tk.pre_tokenizer = pre_tokenizers.Sequence([pre_tokenizers.WhitespaceSplit(), pre_tokenizers.Punctuation()])
        alphabet = sorted({c for c in corpus if not c.isspace()})
        tr = trainers.BpeTrainer(vocab_size=max(vs, len(alphabet) + 2), special_tokens=['[UNK]'], initial_alphabet=alphabet,
                                 show_progress=False, min_frequency=2)
        tk.train_from_iterator(lines, tr)
        enc = tk.encode(SENT61)
        words = enc.word_ids
        pieces = [(s, i == 0 or words[i] != words[i - 1]) for i, s in enumerate(enc.tokens)]
        res.append((tk.get_vocab_size(), pieces))
    n_words = len(re.findall(r'\w+', corpus))

    def draw(theme):
        frames = []
        for _, pieces in res:
            cv = canvas(960, 330)
            chips(cv, pieces, 20, 20, 920, theme)
            frames.append(arr(cv))
        return frames

    labels = [f'từ vựng {v} mảnh{" (chỉ có ký tự)" if k == 0 else ""}: câu thành {len(p)} token' for k, (v, p) in enumerate(res)]
    return Anim('6-1-bpe', f'BPE học trên chính lời giảng của giáo trình (khoảng {n_words // 1000} nghìn từ): từ vựng càng lớn, câu càng ít token; từ hiếm như “tokenization” vẫn ghép được từ mảnh quen.',
                labels, draw, dur=1500, hold=2000, key=[0, 2, 4, 6], photo=False, themed=True)


# ───────────────────────────── 6.2 ─────────────────────────────

def minilm():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device='cpu')


DOCS62 = ['Hạn nộp bài tập về nhà là tối Chủ nhật.', 'Phòng thi mở cửa lúc bảy giờ sáng.', 'Mỗi đội được nộp tối đa năm lần một ngày.',
          'Thư viện cho mượn sách trong hai tuần.', 'Căng tin bán cơm trưa từ mười một giờ.', 'Máy tính phòng lab đã cài sẵn PyTorch.',
          'Học sinh cần mang thẻ khi vào phòng thi.', 'Điểm kiểm tra được công bố sau ba ngày.']
QUERIES62 = ['Mấy giờ thì được vào phòng thi?', 'Khi nào biết điểm?', 'Ăn trưa ở đâu?', 'Máy ở phòng thực hành có thư viện học sâu không?']


def a6_2_search():
    model = minilm()
    D = model.encode(DOCS62, normalize_embeddings=True)
    Q = model.encode(QUERIES62, normalize_embeddings=True)
    S = Q @ D.T
    ranks = [np.argsort(-s) for s in S]
    seq = []
    for q in range(len(QUERIES62)):
        prev = ranks[q - 1] if q else ranks[0]
        if q:
            seq += [(q, prev, ranks[q], f) for f in (1 / 3, 2 / 3)]
        seq += [(q, ranks[q], ranks[q], 1)] * 2

    def draw(theme):
        t = THEMES[theme]
        frames = []
        f = font(21)
        for q, ra, rb, fr in seq:
            cv = canvas(960, 470)
            d = ImageDraw.Draw(cv, 'RGBA')
            pa = {int(i): r for r, i in enumerate(ra)}
            pb = {int(i): r for r, i in enumerate(rb)}
            e = ease(fr)
            for i in range(len(DOCS62)):
                y = 14 + lerp(pa[i], pb[i], e) * 56
                top = pb[i] == 0 and fr == 1
                col = t['clay'] if top else t['blue']
                w = 240 * max(0, S[q, i]) / S.max()
                d.rounded_rectangle([20, y, 20 + 240, y + 12], radius=6, fill=hexrgb(t['soft']))
                d.rounded_rectangle([20, y, 20 + max(12, w), y + 12], radius=6, fill=hexrgb(col))
                d.text((280, y + 6), DOCS62[i], fill=hexrgb(t['clay'] if top else t['text']), font=f, anchor='lm')
                if fr == 1:
                    d.text((20, y + 30), f'{S[q, i]:.2f}', fill=hexrgb(t['muted']), font=font(16), anchor='lm')
            frames.append(arr(cv))
        return frames

    labels = [f'câu hỏi: “{QUERIES62[q]}”' for q, _, _, _ in seq]
    dur = [2200 if fr == 1 else 160 for _, _, _, fr in seq]
    return Anim('6-2-search', 'Model câu đa ngôn ngữ xếp tám câu thông báo theo cosine với từng câu hỏi: ba câu hỏi sau tìm đúng câu trả lời dù gần như không trùng từ; câu hỏi đầu bị kéo về câu cũng nói “vào phòng thi”.',
                labels, draw, dur=dur, hold=800, key=[0, 4, 8, 12], photo=False, themed=True)


# ───────────────────────────── 6.3 ─────────────────────────────

ROAD = ['Con đường này rất đông xe vào giờ tan học.', 'Bố đi đường tắt qua cánh đồng.', 'Đường lên núi trơn vì mưa.',
        'Hai bên đường trồng nhiều cây phượng.', 'Xe buýt rẽ vào đường lớn.', 'Đường về nhà em có một cây cầu.']
SUGAR = ['Mẹ cho thêm một thìa đường vào cốc sữa.', 'Bánh này ít đường nên không ngọt lắm.', 'Đường trắng tan nhanh trong nước nóng.',
         'Bà nấu chè với đường phèn.', 'Uống nhiều nước có đường không tốt cho răng.', 'Kẹo được làm từ đường và bơ.']


def a6_3_context():
    import torch
    from transformers import AutoTokenizer, AutoModel
    from huggingface_hub import snapshot_download
    path = snapshot_download('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', local_files_only=True)
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModel.from_pretrained(path).eval()
    sents = ROAD + SUGAR
    lab = np.array([0] * len(ROAD) + [1] * len(SUGAR))
    vecs = []                                      # (câu, lớp, chiều)
    for s in sents:
        enc = tok(s, return_tensors='pt', return_offsets_mapping=True)
        off = enc.pop('offset_mapping')[0].tolist()
        lo = s.lower().index('đường')
        pos = [i for i, (a, b) in enumerate(off) if b > a and a >= lo and b <= lo + len('đường')]
        assert pos, s
        with torch.no_grad():
            hs = model(**enc, output_hidden_states=True).hidden_states
        vecs.append(np.stack([h[0, pos].mean(0).numpy() for h in hs]))
    V = np.stack(vecs)
    L = V.shape[1]
    sep = []
    pts = []
    for l in range(L):
        A = V[:, l] - V[:, l].mean(0)
        U, s_, Vt = np.linalg.svd(A, full_matrices=False)
        P = A @ Vt[:2].T
        if pts:                                     # giữ chiều trục ổn định giữa các lớp (dấu của PCA tùy ý)
            for j in range(2):
                if np.dot(P[:, j], pts[-1][:, j]) < 0:
                    P[:, j] *= -1
        pts.append(P / (np.abs(P).max() + 1e-9))
        Vn = V[:, l] / np.linalg.norm(V[:, l], axis=1, keepdims=True)
        C = Vn @ Vn.T
        same = (C[lab[:, None] == lab[None]].sum() - len(lab)) / ((lab[:, None] == lab[None]).sum() - len(lab))
        diff = C[lab[:, None] != lab[None]].mean()
        sep.append((same, diff))

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for l in range(L):
            fig = fig_frame(960, 470)
            ax = fig.add_axes((.02, .03, .96, .94)); ax.patch.set_alpha(0)
            P = pts[l]
            for k, col in [(0, t['blue']), (1, t['clay'])]:
                m = lab == k
                ax.scatter(P[m, 0], P[m, 1], s=90, color=col, linewidths=0, zorder=3)
            ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25)
            bare(ax)
            fig.text(.985, .93, '“đường” = lối đi', color=t['blue'], ha='right', fontsize=12)
            fig.text(.985, .87, '“đường” = chất ngọt', color=t['clay'], ha='right', fontsize=12)
            frames.append(grab(fig))
        return frames

    labels = [('lớp 0, embedding tra bảng' if l == 0 else f'sau lớp {l}') +
              f': cosine trung bình cùng nghĩa {sep[l][0]:.2f}, khác nghĩa {sep[l][1]:.2f}' for l in range(L)]
    return Anim('6-3-context', 'Vector của chữ “đường” trong 12 câu, qua từng lớp của một encoder kiểu BERT (MiniLM đa ngôn ngữ): càng lên cao, hai nghĩa càng tách xa.',
                labels, draw, dur=[1600] + [800] * (L - 2) + [1200], hold=2600, key=[0, 3, 7, L - 1], photo=False, themed=True)


# ───────────────────────────── 6.4 ─────────────────────────────

PROMPT64 = 'Hà Nội là thủ đô của'


def a6_4_next():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B')
    model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B', dtype=torch.float32).eval()
    ids = tok(PROMPT64, return_tensors='pt').input_ids
    steps = []
    for _ in range(9):
        with torch.no_grad():
            p = model(ids).logits[0, -1].softmax(-1)
        v, i = p.topk(5)
        steps.append((tok.decode(ids[0]), [(tok.decode([int(j)]), float(x)) for x, j in zip(v, i)]))
        ids = torch.cat([ids, i[:1][None]], 1)
    final = tok.decode(ids[0])

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for k, (ctx, top) in enumerate(steps + [(final, None)]):
            cv = canvas(960, 400)
            d = ImageDraw.Draw(cv, 'RGBA')
            f = font(28, 'serif')
            d.text((24, 40), PROMPT64, fill=hexrgb(t['muted']), font=f, anchor='lm')
            x = 24 + d.textlength(PROMPT64, font=f)
            d.text((x, 40), ctx[len(PROMPT64):], fill=hexrgb(t['text']), font=f, anchor='lm')
            if top:
                x2 = x + d.textlength(ctx[len(PROMPT64):], font=f)
                d.rounded_rectangle([x2 + 4, 22, x2 + 20, 58], radius=4, fill=hexrgb(t['clay'], 90))
                for r, (s, pv) in enumerate(top):
                    y = 110 + r * 54
                    shown = s.replace('\n', '↵') if s.strip() else repr(s)
                    d.text((24, y + 10), shown, fill=hexrgb(t['clay'] if r == 0 else t['text']), font=font(24), anchor='lm')
                    d.rounded_rectangle([230, y, 230 + 600, y + 20], radius=10, fill=hexrgb(t['soft']))
                    d.rounded_rectangle([230, y, 230 + max(20, 600 * pv), y + 20], radius=10, fill=hexrgb(t['clay'] if r == 0 else t['blue']))
                    d.text((845, y + 10), f'{pv:.3f}', fill=hexrgb(t['muted']), font=font(20), anchor='lm')
            frames.append(arr(cv))
        return frames

    labels = [f'bước {k + 1}: 5 token có xác suất cao nhất; greedy chọn “{top[0][0].strip()}” ({top[0][1]:.2f})' for k, (_, top) in enumerate(steps)] + \
             ['sau 9 bước greedy']
    return Anim('6-4-next', 'Qwen2.5-0.5B viết tiếp “Hà Nội là thủ đô của” từng token: mỗi bước model trả một phân phối, greedy lấy token cao nhất rồi nối vào.',
                labels, draw, dur=1700, hold=2400, key=[0, 1, 5, 9], photo=False, themed=True)


# ───────────────────────────── 6.5 ─────────────────────────────

def a6_5_xattn():
    """Whisper (encoder–decoder) chép giọng đọc thật: mỗi token sinh ra, cross-attention đặt trọng số lên đoạn âm thanh nào."""
    import torch
    import scipy.io.wavfile as wav
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    proc = WhisperProcessor.from_pretrained('openai/whisper-base.en')
    model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-base.en', attn_implementation='eager').eval()
    sr, a = wav.read(DATA / 'speech_zira.wav')
    a = a.astype(np.float32) / 32768
    feats = proc(a, sampling_rate=16000, return_tensors='pt').input_features
    with torch.no_grad():
        gen = model.generate(feats)
        out = model(input_features=feats, decoder_input_ids=gen, output_attentions=True)
    LAYER, HEAD = 2, 0      # head có trọng số đi đều theo thời gian nhất trên câu này (đã kiểm argmax từng token)
    A = out.cross_attentions[LAYER][0, HEAD].numpy()      # (token, 1500 khung 20 ms)
    toks = [proc.tokenizer.decode([int(i)]) for i in gen[0]]
    keep = [k for k, s in enumerate(toks) if not s.startswith('<|')]
    n_frames = int(len(a) / sr / .02) + 4
    A = A[:, :n_frames]
    mel = feats[0, :, :n_frames * 2].numpy()
    text_all = proc.batch_decode(gen, skip_special_tokens=True)[0].strip()

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for j in range(len(keep) + 1):
            fig = fig_frame(960, 470)
            ax = fig.add_axes((.03, .44, .94, .5))
            ax.imshow(mel, origin='lower', aspect='auto', cmap='magma', extent=(0, n_frames, 0, 80))
            bare(ax)
            if j < len(keep):
                w = A[keep[j]]
                ax2 = fig.add_axes((.03, .3, .94, .12)); ax2.patch.set_alpha(0)
                ax2.fill_between(np.arange(len(w)) + .5, 0, w / w.max(), color=t['clay'], alpha=.85, lw=0)
                ax2.set_xlim(0, n_frames); ax2.set_ylim(0, 1.05)
                bare(ax2)
                c = (w * np.arange(len(w))).sum() / w.sum()
                ax.axvline(c, color='#ffffff', lw=1.2, alpha=.8)
            said = ''.join(toks[k] for k in keep[:j + 1]) if j < len(keep) else text_all
            fig.text(.03, .14, said.strip(), color=t['text'], fontsize=17, ha='left', va='center')
            if j < len(keep):
                fig.text(.03, .05, f'token đang sinh: “{toks[keep[j]].strip()}”', color=t['clay'], fontsize=12, ha='left')
            frames.append(grab(fig))
        return frames

    labels = [f'token {j + 1}/{len(keep)}: “{toks[k].strip()}”, trọng số lớn nhất ở {A[k].argmax() * .02:.2f} s'
              for j, k in enumerate(keep)] + [f'transcript: “{text_all}”']
    return Anim('6-5-xattn', f'Whisper chép một câu đọc thật: encoder đọc phổ âm thanh; mỗi token decoder sinh ra, một head cross-attention (lớp {LAYER + 1}, head {HEAD + 1}) dồn trọng số vào đoạn âm của từ ấy.',
                labels, draw, dur=[900] * len(keep) + [1800], hold=1600, key=[1, 3, 5, len(keep)], photo=True, themed=True)


# ───────────────────────────── 6.6 ─────────────────────────────

QUERIES66 = ['Khi prompt quá dài so với ngữ cảnh thì làm gì?', 'Kiểm đầu ra JSON có đúng schema bằng cách nào?', 'KV cache tốn bao nhiêu bộ nhớ?']


def a6_6_rag():
    """Truy hồi trên chính bài 6.6: chia lời giảng thành đoạn, tìm 3 đoạn gần câu hỏi nhất bằng embedding câu."""
    model = minilm()
    t66 = (CONTENT / 'phase-6' / '6.6.md').read_text(encoding='utf-8')
    body = t66.split('## Khi đi thi')[0]
    body = re.sub(r'```.*?```', ' ', body, flags=re.S)
    body = re.sub(r':::.*?:::', ' ', body, flags=re.S)
    paras = [re.sub(r'\$[^$]*\$|`[^`]*`|!\[[^\]]*\]\([^)]*\)|\*\*', '', p).strip() for p in body.split('\n\n')]
    paras = [p for p in paras if len(p.split()) > 25 and not p.startswith('#') and not p.startswith('|')]
    chunks = paras[:24]
    E = model.encode(chunks, normalize_embeddings=True)
    Q = model.encode(QUERIES66, normalize_embeddings=True)
    S = Q @ E.T
    cols = 6
    seq = [(q, f) for q in range(len(QUERIES66)) for f in (0, 1)]

    def wrap(d, s, f, width, maxlines):
        words, lines, cur = s.split(), [], ''
        for w_ in words:
            if d.textlength((cur + ' ' + w_).strip(), font=f) > width:
                lines.append(cur)
                cur = w_
                if len(lines) == maxlines:
                    break
            else:
                cur = (cur + ' ' + w_).strip()
        else:
            lines.append(cur)
            return lines
        lines[-1] = lines[-1].rstrip(',.;:') + ' …'
        return lines

    def draw(theme):
        t = THEMES[theme]
        frames = []
        f = font(17)
        for q, stage in seq:
            cv = canvas(960, 440)
            d = ImageDraw.Draw(cv, 'RGBA')
            order = np.argsort(-S[q])
            rank = {int(i): r for r, i in enumerate(order)}
            lo, hi = S[q].min(), S[q].max()
            for i in range(len(chunks)):
                r_, c_ = divmod(i, cols)
                x, y = 14 + c_ * 52, 20 + r_ * 52
                v = (S[q, i] - lo) / (hi - lo)
                hit = stage == 1 and rank[i] < 3
                d.rounded_rectangle([x, y, x + 44, y + 44], radius=7, fill=hexrgb(t['clay'] if hit else t['blue'], int(40 + 170 * v)),
                                    outline=hexrgb(t['text']) if hit else None, width=2)
                if hit:
                    d.text((x + 22, y + 22), str(rank[i] + 1), fill=hexrgb('#ffffff'), font=font(19, bold=True), anchor='mm')
            if stage == 1:
                for r in range(3):
                    i = int(order[r])
                    y = 18 + r * 140
                    d.text((350, y + 4), f'{r + 1}', fill=hexrgb(t['clay']), font=font(22, bold=True), anchor='lt')
                    d.text((376, y + 8), f'cosine {S[q, i]:.2f}', fill=hexrgb(t['muted']), font=font(15), anchor='lt')
                    for k, ln in enumerate(wrap(d, chunks[i], f, 560, 4)):
                        d.text((376, y + 32 + k * 24), ln, fill=hexrgb(t['text']), font=f, anchor='lt')
            frames.append(arr(cv))
        return frames

    labels = []
    for q, stage in seq:
        labels.append(f'câu hỏi: “{QUERIES66[q]}”' + (' · 3 đoạn có cosine cao nhất được đưa vào prompt' if stage else ' · chấm cosine với từng đoạn'))
    return Anim('6-6-rag', f'Truy hồi trên chính lời giảng bài này: {len(chunks)} đoạn văn (mỗi ô một đoạn, càng đậm cosine càng cao); mỗi câu hỏi lấy 3 đoạn gần nhất để ghép vào prompt.',
                labels, draw, dur=[1300, 4200] * len(QUERIES66), hold=600, key=[1, 3, 5], photo=False, themed=True, pcols=1)


ANIMS = [a6_1_bpe, a6_2_search, a6_3_context, a6_4_next, a6_5_xattn, a6_6_rag]
