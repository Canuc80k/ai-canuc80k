"""Hình động chương 7 (âm thanh, đa phương thức). Âm thanh thật: hai câu tiếng Anh đọc bằng giọng tổng hợp Windows
(data/speech_zira.wav, data/speech_david.wav, 16 kHz). Model thật: wav2vec2-base-960h, CLIP ViT-B/32, ResNet-18, MiniLM."""
import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image

os.environ.setdefault('HF_HUB_OFFLINE', '1')
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))
from akit import (Anim, THEMES, canvas, paste, rect, arr, hexrgb, text, ease, lerp, sample, skdata,  # noqa: E402
                  plain_axes, fig_frame, grab)
from a_ch2 import bare  # noqa: E402

DATA = Path(__file__).resolve().parent / 'data'


def speech(name='speech_zira'):
    import scipy.io.wavfile as wav
    sr, a = wav.read(DATA / f'{name}.wav')
    return sr, a.astype(np.float32) / 32768


def logpower(a, sr, win=400, hop=160):
    from numpy.lib.stride_tricks import sliding_window_view
    fr = sliding_window_view(a, win)[::hop] * np.hanning(win)
    P = np.abs(np.fft.rfft(fr, axis=1)) ** 2
    return 10 * np.log10(P + 1e-10).T, hop          # (tần số, khung)


# ───────────────────────────── 7.1 ─────────────────────────────

def a7_1_stft():
    sr, a = speech()
    S, hop = logpower(a, sr)
    S = np.clip(S, S.max() - 80, None)
    n = S.shape[1]
    stops = [int(round(x)) for x in np.linspace(1, n, 18)]
    win = 400

    MID, BL, CL = '#8f8b81', '#4f86c6', '#d0693f'      # đọc được trên cả nền sáng lẫn tối

    def draw(theme):
        frames = []
        for k in stops:
            fig = fig_frame(960, 500)
            ax = fig.add_axes((.04, .64, .92, .32)); ax.patch.set_alpha(0)
            tt = np.arange(len(a)) / sr
            ax.plot(tt, a, color=BL, lw=.5)
            s0 = (k - 1) * hop / sr
            ax.axvspan(s0, s0 + win / sr, color=CL, alpha=.4, lw=0)
            ax.set_xlim(0, len(a) / sr); ax.set_ylim(-np.abs(a).max(), np.abs(a).max())
            bare(ax)
            ax2 = fig.add_axes((.04, .06, .92, .52))
            shown = np.full_like(S, np.nan)
            shown[:, :k] = S[:, :k]
            ax2.imshow(shown, origin='lower', aspect='auto', cmap='magma', extent=(0, len(a) / sr, 0, sr / 2 / 1000),
                       vmin=S.min(), vmax=S.max(), interpolation='nearest')
            ax2.set_facecolor('none')
            ax2.set_xlim(0, len(a) / sr)
            ax2.set_yticks([0, 2, 4, 6, 8]); ax2.set_yticklabels(['0', '2', '4', '6', '8 kHz'], color=MID, fontsize=9)
            ax2.set_xticks([0, 1, 2, 3]); ax2.set_xticklabels(['0', '1', '2', '3 s'], color=MID, fontsize=9)
            for s_ in ax2.spines.values():
                s_.set_visible(False)
            ax2.tick_params(length=0)
            frames.append(grab(fig))
        return frames

    labels = [f'khung {k}/{n}: cửa sổ 25 ms bắt đầu ở {(k - 1) * hop / sr * 1000:.0f} ms, FFT cho một cột của spectrogram' for k in stops]
    labels[-1] = f'đủ {n} khung, mỗi khung cách nhau 10 ms: câu “Deep learning models learn patterns from data.”'
    return Anim('7-1-stft', 'Một câu đọc thật (16 kHz): cửa sổ 25 ms trượt trên waveform, mỗi vị trí qua FFT thành một cột của spectrogram bên dưới.',
                labels, draw, dur=[700] * 17 + [600], hold=2800, key=[4, 9, 13, 17], themed=False)


# ───────────────────────────── 7.2 ─────────────────────────────

def mel_filter(sr, n_fft, n_mels=64):
    def hz2mel(f):
        return 2595 * np.log10(1 + f / 700)

    def mel2hz(m):
        return 700 * (10 ** (m / 2595) - 1)
    pts = mel2hz(np.linspace(hz2mel(0), hz2mel(sr / 2), n_mels + 2))
    bins = np.floor((n_fft + 1) * pts / sr).astype(int)
    F = np.zeros((n_mels, n_fft // 2 + 1))
    for m in range(1, n_mels + 1):
        l, c, r = bins[m - 1], bins[m], bins[m + 1]
        for k in range(l, c):
            F[m - 1, k] = (k - l) / max(1, c - l)
        for k in range(c, r):
            F[m - 1, k] = (r - k) / max(1, r - c)
    return F


def logmel(a, sr, win=400, hop=160):
    from numpy.lib.stride_tricks import sliding_window_view
    fr = sliding_window_view(a, win)[::hop] * np.hanning(win)
    P = np.abs(np.fft.rfft(fr, n=512, axis=1)) ** 2
    M = mel_filter(sr, 512) @ P.T
    return 10 * np.log10(M + 1e-10)


def a7_2_specaug():
    """SpecAugment trên log-mel của một câu thật: mỗi epoch che ngẫu nhiên vài dải thời gian và tần số."""
    sr, a = speech('speech_david')
    M = logmel(a, sr)
    M = np.clip(M, M.max() - 70, None)
    T, Fq = M.shape[1], M.shape[0]
    rng = np.random.default_rng(72)
    masks = [([], [])]
    for _ in range(9):
        tm = [(int(s), int(w)) for s, w in zip(rng.integers(0, T - 30, 2), rng.integers(8, 30, 2))]
        fm = [(int(s), int(w)) for s, w in zip(rng.integers(0, Fq - 12, 2), rng.integers(4, 12, 2))]
        masks.append((tm, fm))

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for tm, fm in masks:
            X = M.copy()
            for s, w in tm:
                X[:, s:s + w] = M.mean()
            for s, w in fm:
                X[s:s + w, :] = M.mean()
            fig = fig_frame(960, 380)
            ax = fig.add_axes((.02, .04, .96, .92))
            ax.imshow(X, origin='lower', aspect='auto', cmap='magma', vmin=M.min(), vmax=M.max(), interpolation='nearest')
            for s, w in tm:
                ax.add_patch(__import__('matplotlib.patches', fromlist=['x']).Rectangle((s - .5, -.5), w, Fq, fill=False, ec=t['clay'], lw=1.6))
            for s, w in fm:
                ax.add_patch(__import__('matplotlib.patches', fromlist=['x']).Rectangle((-.5, s - .5), T, w, fill=False, ec=t['blue'], lw=1.6))
            bare(ax)
            frames.append(grab(fig))
        return frames

    labels = ['log-mel gốc: 64 dải mel × 1 khung mỗi 10 ms'] + \
             [f'epoch {e}: che {sum(w for _, w in tm) * 10} ms thời gian (khung cam), {sum(w for _, w in fm)} dải mel (khung xanh)'
              for e, (tm, fm) in enumerate(masks[1:], 1)]
    return Anim('7-2-specaug', 'SpecAugment trên log-mel của một câu đọc thật: mỗi epoch che ngẫu nhiên vài đoạn thời gian và vài dải tần, nhãn giữ nguyên.',
                labels, draw, dur=1300, hold=1300, key=[0, 1, 2, 3], themed=True)


# ───────────────────────────── 7.3 ─────────────────────────────

W2V_VOCAB = ['<pad>', '<s>', '</s>', '<unk>', '|', 'E', 'T', 'A', 'O', 'N', 'I', 'H', 'S', 'R', 'D', 'L', 'U', 'M', 'W', 'C',
             'F', 'G', 'Y', 'P', 'B', 'V', 'K', "'", 'X', 'J', 'Q', 'Z']   # bảng 32 ký tự của wav2vec2-base-960h


def a7_3_ctc():
    """wav2vec2 đọc câu thật: mỗi khung 20 ms một phân phối trên 32 ký tự; greedy CTC gộp lặp rồi bỏ blank."""
    import torch
    from transformers import Wav2Vec2FeatureExtractor, AutoModelForCTC
    sr, a = speech()
    fe = Wav2Vec2FeatureExtractor.from_pretrained('facebook/wav2vec2-base-960h')
    model = AutoModelForCTC.from_pretrained('facebook/wav2vec2-base-960h').eval()
    with torch.no_grad():
        lg = model(fe(a, sampling_rate=16000, return_tensors='pt').input_values).logits[0]
    P = lg.softmax(-1).numpy()
    ids = P.argmax(1)
    n = len(ids)
    chars = ['·' if i == 0 else ('␣' if i == 4 else W2V_VOCAB[i]) for i in ids]
    collapsed = []
    prev = None
    for i in ids:
        if i != prev and i != 0:
            collapsed.append(' ' if i == 4 else W2V_VOCAB[i])
        prev = i
    text_out = ''.join(collapsed).strip()
    S, hop = logpower(a, sr)
    S = np.clip(S, S.max() - 80, None)
    NV = 36                                   # phóng to 0.72 s đầu (“deep learning”): mỗi khung 20 ms đủ rộng để đọc
    stops = [4, 8, 12, 16, 20, 24, 28, 32]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        for k in stops + [NV]:
            fig = fig_frame(960, 470)
            ax = fig.add_axes((.02, .55, .96, .42))
            ax.imshow(S[:, :2 * NV], origin='lower', aspect='auto', cmap='magma', extent=(0, NV, 0, 1))
            ax.axvspan(k, NV, color=t['bg'], alpha=.72, lw=0)
            bare(ax)
            ax2 = fig.add_axes((.02, .3, .96, .2)); ax2.patch.set_alpha(0)
            ax2.set_xlim(0, NV); ax2.set_ylim(0, 1)
            for j in range(k):
                c = chars[j]
                if c == '·':
                    ax2.text(j + .5, .5, '·', ha='center', va='center', color=t['faint'], fontsize=16)
                else:
                    ax2.text(j + .5, .5, c, ha='center', va='center', color=t['clay'], fontsize=14, fontweight='bold')
            bare(ax2)
            done = []
            prev = None
            for i in ids[:k]:
                if i != prev and i != 0:
                    done.append(' ' if i == 4 else W2V_VOCAB[i])
                prev = i
            fig.text(.02, .14, ''.join(done), color=t['text'], fontsize=17, ha='left', va='center', family='monospace')
            frames.append(grab(fig))
        return frames

    blanks = int((ids == 0).sum())
    blanks = int((ids[:NV] == 0).sum())
    labels = [f'{k}/{NV} khung (đầu câu) đã đọc: hàng giữa là ký tự argmax của mỗi khung 20 ms, chấm là blank; dòng dưới là kết quả sau khi gộp' for k in stops] +              [f'{NV} khung đầu, {blanks} khung là blank. Cả câu {n} khung cho: “{text_out}”']
    return Anim('7-3-ctc', 'wav2vec2 đọc một câu thật (phóng to hai từ đầu): mỗi khung 20 ms cho một ký tự hoặc blank; gộp ký tự lặp liền nhau rồi bỏ blank là được transcript.',
                labels, draw, dur=[900] * len(stops) + [1600], hold=2400, key=[1, 3, 5, len(stops)], themed=True)


# ───────────────────────────── 7.4 ─────────────────────────────

PAIRS74 = [('chelsea', 'ski', 'a cat looking at the camera'), ('coffee', 'ski', 'a cup of coffee on a saucer'),
           ('rocket', 'ski', 'a rocket on the launch pad'), ('china.jpg', 'sk', 'an old pagoda by the lake'),
           ('flower.jpg', 'sk', 'an orange flower'), ('astronaut', 'ski', 'an astronaut in a white suit'),
           ('horse', 'ski', 'the silhouette of a horse'), ('coins', 'ski', 'rows of old coins')]


def a7_4_align():
    """Cosine ảnh–caption: hai encoder học riêng (ResNet-18 + MiniLM, chiếu ngẫu nhiên về cùng 512 chiều) so với CLIP học chung."""
    import torch
    from models import clip, resnet18, center224, to_tensor
    from a_ch5 import square
    from sentence_transformers import SentenceTransformer
    imgs = []
    for n, k, _ in PAIRS74:
        x = sample(n) if k == 'sk' else skdata(n)
        if n == 'horse':
            x = (np.asarray(x) * 255).astype(np.uint8) if np.asarray(x).dtype == bool else x
        imgs.append(square(x))
    caps = [c for _, _, c in PAIRS74]
    cm = clip()
    Ci = cm.encode([Image.fromarray(a) for a in imgs], normalize_embeddings=True)
    Ct = cm.encode(caps, normalize_embeddings=True)
    C_clip = Ci @ Ct.T
    r18, _ = resnet18()
    body = torch.nn.Sequential(*list(r18.children())[:-1]).eval()
    with torch.no_grad():
        Fi = torch.cat([body(to_tensor(center224(np.stack([a] * 3, -1) if a.ndim == 2 else a[..., :3]))).flatten(1) for a in imgs]).numpy()
    st = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')
    Ft = st.encode(caps)                          # 384 chiều
    rng = np.random.default_rng(74)
    Pt = rng.normal(size=(384, 512)) / np.sqrt(384)   # chiếu chữ lên 512 chiều cho cùng chiều với ảnh, không học gì
    Fi = Fi / np.linalg.norm(Fi, axis=1, keepdims=True)
    Gt = Ft @ Pt
    Gt = Gt / np.linalg.norm(Gt, axis=1, keepdims=True)
    C_sep = Fi @ Gt.T
    n = len(imgs)

    def draw(theme):
        t = THEMES[theme]
        from matplotlib.colors import LinearSegmentedColormap
        frames = []
        for k in range(n + 1):
            fig = fig_frame(960, 480)
            for j, (C, title) in enumerate([(C_sep, 'hai encoder học riêng'), (C_clip, 'CLIP, học chung')]):
                ax = fig.add_axes((.1 + j * .47, .05, .36, .76))
                Z = (C - C.min()) / (C.max() - C.min())
                shown = np.full_like(Z, np.nan)
                shown[:k] = Z[:k]
                cmap = LinearSegmentedColormap.from_list('c', [t['soft'], t['clay']])
                ax.imshow(shown, cmap=cmap, vmin=0, vmax=1, interpolation='nearest')
                for i in range(k):
                    jj = int(C[i].argmax())
                    ax.add_patch(__import__('matplotlib.patches', fromlist=['x']).Rectangle((jj - .5, i - .5), 1, 1, fill=False, ec=t['text'], lw=1.6))
                ax.set_xlim(-.5, n - .5); ax.set_ylim(n - .5, -.5)
                bare(ax)
                ax.set_title(title, color=t['text'], fontsize=11.5, pad=6)
                for i in range(n):
                    ax.imshow(imgs[i], extent=(-1.45, -.6, i + .42, i - .42))
                ax.set_xlim(-1.5, n - .5)
            frames.append(grab(fig))
        return frames

    acc_sep = float((C_sep.argmax(1) == np.arange(n)).mean())
    acc_clip = float((C_clip.argmax(1) == np.arange(n)).mean())
    labels = ['8 ảnh thật (hàng) và 8 caption (cột, cùng thứ tự): ô đúng nằm trên đường chéo'] + \
             [f'ảnh {k}: ô viền đậm là caption có cosine cao nhất trong hàng' for k in range(1, n)] + \
             [f'caption cao nhất đúng cặp: học riêng {acc_sep * n:.0f}/{n}, CLIP {acc_clip * n:.0f}/{n}']
    return Anim('7-4-align', 'Cosine giữa 8 ảnh thật và 8 caption: hai encoder học riêng, chỉ ép về cùng số chiều, không có đường chéo; CLIP học chung từ cặp ảnh–chữ nên đúng cặp sáng nhất.',
                labels, draw, dur=[1800] + [600] * (n - 1) + [2400], hold=1200, key=[0, 3, 6, n], themed=True)


ANIMS = [a7_1_stft, a7_2_specaug, a7_3_ctc, a7_4_align]


# ───────────────────────────── kt4 ─────────────────────────────

def a7_kt4_ids():
    """25 ID validation của buổi kiểm tra: đúng/sai của nhánh ảnh, nhánh chữ, fusion, rồi khoanh các nhóm ID cần đọc."""
    from p8_ch5 import kt_ns
    from PIL import ImageDraw
    ns = kt_ns(7, 'kt4', upto=4)
    oks = [ns['image_ok'], ns['text_ok'], ns['fusion_ok']]
    names = ['ảnh', 'chữ', 'fusion']
    groups = [('fusion sửa', ~oks[0] & oks[2]), ('fusion làm sai', oks[0] & ~oks[2]), ('cả ba cùng sai', ~oks[0] & ~oks[1] & ~oks[2])]
    seq = [('row', 1), ('row', 2), ('row', 3)] + [('group', g) for g in range(3)]

    def draw(theme):
        t = THEMES[theme]
        frames = []
        cs = 32
        cols = [t['blue'], t['green'], t['clay']]
        for kind, v in seq:
            cv = canvas(960, 200)
            d = ImageDraw.Draw(cv, 'RGBA')
            shown = 3 if kind == 'group' else v
            for r in range(shown):
                text(cv, 110, 34 + r * 46 + cs / 2, names[r], hexrgb(t['text']), 18, anchor='rm')
                for i in range(25):
                    x, y = 124 + i * cs, 34 + r * 46
                    d.rounded_rectangle([x, y, x + cs - 6, y + cs - 6], radius=5,
                                        fill=hexrgb(cols[r]) if oks[r][i] else None, outline=hexrgb(cols[r]), width=2)
            if kind == 'group':
                for i in np.flatnonzero(groups[v][1]):
                    x = 124 + i * cs
                    d.rounded_rectangle([x - 4, 28, x + cs - 2, 34 + 2 * 46 + cs], radius=7, outline=hexrgb(t['text']), width=3)
            for i in range(25):
                text(cv, 124 + i * cs + (cs - 6) / 2, 14, str(i), hexrgb(t['faint']), 12)
            frames.append(arr(cv))
        return frames

    labels = [f'nhánh {names[v - 1]}: đúng {oks[v - 1].sum()}/25 (ô đặc)' for _, v in seq[:3]] + \
             [f'{groups[g][0]}: ID {np.flatnonzero(groups[g][1]).tolist()}' for _, g in seq[3:]]
    return Anim('7-kt4-ids', 'Đúng/sai theo từng ID của ba cấu hình trên 25 mẫu validation của buổi kiểm tra, rồi khoanh các nhóm ID cần đọc: fusion sửa, fusion làm sai, cả ba cùng sai.',
                labels, draw, dur=1600, hold=1800, key=[2, 3, 4, 5], photo=False, themed=True, pcols=1)


ANIMS.append(a7_kt4_ids)
