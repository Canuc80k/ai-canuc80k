"""Lượt 8 — hình chương 7 (bản gọn). Số liệu lấy từ code bài (lesson_ns) hoặc tính lại đúng như bài.
Chạy riêng: python -B -X utf8 p8_ch7.py [tên ...]"""
import math, sys
import numpy as np
from kit import *
from p8_ch1 import lesson_ns
from p8_ch2 import PAPER, sup, mnum, clip, segline, regions, jit
from p8_ch5 import kt_ns


def heat(s, ax, M, x0, x1, y0, y1, lo=-80, hi=0, col=CLAY):
    """Vẽ ma trận M (hàng = trục y từ y0 tới y1, cột = trục x) bằng ô màu, độ đậm theo (M - lo)/(hi - lo)."""
    R, C = M.shape
    dx, dy = (x1 - x0) / C, (y1 - y0) / R
    for i in range(R):
        for j in range(C):
            v = (min(max(M[i, j], lo), hi) - lo) / (hi - lo)
            if v > .02:
                s.rect(ax.X(x0 + j * dx), ax.Y(y0 + (i + 1) * dy), ax.X(x0 + (j + 1) * dx) - ax.X(x0 + j * dx) + .3,
                       ax.Y(y0 + i * dy) - ax.Y(y0 + (i + 1) * dy) + .3, 'none', col, 0, .05 + .9 * v, 0)


def wave_axes(s, x, y, w, h, t0, t1, ylim=(-1, 1), xlabel=None, xticks=None):
    return s.axes(x, y, w, h, (t0, t1), ylim, xticks=xticks, yticks=[ylim[0], 0, ylim[1]], xlabel=xlabel, grid=False)


# ───────────────────────────── 7.1 ─────────────────────────────

_T71 = {}


def ns71():
    if not _T71:
        _T71['ns'] = lesson_ns('7.1', upto=7)
    return _T71['ns']


def sampling71():
    ns = ns71()
    fs = ns['sample_rate']
    s = Fig(640, 230)
    for k, (t0, f, a, col) in enumerate([(0.0, 200, .7, BLUE), (0.5, 600, .4, CLAY)]):
        x0 = 60 + k * 300
        ax = s.axes(x0, 34, 250, 140, (0, 10), (-.8, .8), xticks=[0, 5, 10], yticks=[-.7, 0, .7] if k == 0 else [], grid=False,
                    xlabel='ms sau ' + ('0 s' if k == 0 else '0.5 s'))
        tt = np.linspace(0, .01, 400)
        ax.line(tt * 1000, a * np.sin(2 * np.pi * f * (t0 + tt)), col, 1.4)
        n = np.arange(int(t0 * fs), int(t0 * fs) + 21)
        ax.dots((n / fs - t0) * 1000, ns['waveform'][n], col, 3.2, col)
        s.label(x0 + 125, 20, f'{f} Hz: {fs // f if fs % f == 0 else round(fs / f, 2)} mẫu mỗi chu kỳ', 12, color=TEXT, weight=600)
    s.label(320, 220, 'mỗi chấm là một mẫu, cách nhau 0.5 ms (sample rate 2000 Hz)', 11.5, color=MUTED)
    s.save('7-1-sampling', 'Ở 2000 Hz, âm 200 Hz có 10 mẫu mỗi chu kỳ, âm 600 Hz chỉ khoảng 3.3 mẫu.')


def alias71():
    s = Fig(640, 225)
    ax = s.axes(60, 24, 470, 140, (0, 10), (-1.1, 1.1), xticks=[0, 2, 4, 6, 8, 10], yticks=[-1, 0, 1], xlabel='ms', grid=False)
    tt = np.linspace(0, .01, 800)
    ax.line(tt * 1000, np.cos(2 * np.pi * 350 * tt), BLUE, 1.6).line(tt * 1000, np.cos(2 * np.pi * 650 * tt), CLAY, 1.2)
    n = np.arange(11)
    ax.dots(n, np.cos(2 * np.pi * 350 * n / 1000), TEXT, 4, TEXT)
    s.label(ax.X(10) + 10, ax.Y(.4), '350 Hz', 12, 'start', BLUE, 600)
    s.label(ax.X(10) + 10, ax.Y(-.4), '650 Hz', 12, 'start', CLAY, 600)
    s.label(320, 214, 'lấy mẫu 1000 Hz: hai cosine đi qua đúng cùng các chấm, 650 = 1000 − 350', 11.5, color=MUTED)
    s.save('7-1-alias', 'Lấy mẫu 1000 Hz: cosine 350 Hz và 650 Hz đi qua đúng cùng các điểm mẫu.')


def downsample71():
    from scipy.signal import resample_poly
    ns = ns71()
    w = ns['waveform']
    half = ns['sample_rate'] // 2
    s = Fig(640, 220)
    for k, (nm, sig, col) in enumerate([('bỏ mẫu waveform[::2]', w[::2], CLAY), ('resample_poly (có lọc)', resample_poly(w, 1, 2), GREEN)]):
        tail = sig[len(sig) // 2:]
        amp = np.abs(np.fft.rfft(tail)) * 2 / len(tail)
        fr = np.fft.rfftfreq(len(tail), d=1 / half)
        x0 = 60 + k * 300
        ax = s.axes(x0, 40, 240, 120, (0, 500), (0, .45), xticks=[0, 200, 400], yticks=[0, .2, .4] if k == 0 else [], grid=False, xlabel='Hz')
        for f_, a_ in zip(fr, amp):
            if a_ > .005:
                s.line(ax.X(f_), ax.Y(0), ax.X(f_), ax.Y(a_), col, 2.4)
        s.label(x0 + 120, 24, nm, 12, color=TEXT, weight=600)
        v = amp[fr == 400][0]
        s.mono(ax.X(400), ax.Y(max(v, .02)) - 10, f'400 Hz: {v:.3f}', 11, 'middle', col)
    s.label(320, 206, 'nửa sau chỉ có âm 600 Hz; ở 1000 Hz, Nyquist còn 500 Hz', 11.5, color=MUTED)
    s.save('7-1-downsample', 'Bỏ mẫu sinh âm giả 400 Hz; resample_poly lọc trước nên không có.')


def frames71():
    ns = ns71()
    w = ns['waveform']
    fs = ns['sample_rate']
    s = Fig(640, 230)
    ax = s.axes(40, 60, 560, 90, (0, .4), (-.8, .8), xticks=[0, .1, .2, .3, .4], yticks=[], grid=False, xlabel='giây')
    n = np.arange(int(.4 * fs))
    ax.line(n / fs, w[n], FAINT, 1)
    from scipy.signal.windows import hann
    hw = hann(200, sym=False)
    for j, col in enumerate([BLUE, CLAY, GREEN]):
        st = j * 100
        tt = (st + np.arange(200)) / fs
        ax.line(tt, .75 * hw, col, 1.8)
        s.box(ax.X(st / fs), 14 + j * 14, ax.X((st + 200) / fs) - ax.X(st / fs), 8, 'none', col, r=2, width=0, opacity=.5)
        s.mono(ax.X((st + 200) / fs) + 6, 18.5 + j * 14, f'frame {j}', 10.5, 'start', col)
    s.label(320, 214, 'window 200 mẫu (100 ms), hop 100 mẫu (50 ms): mỗi frame chồng nửa frame trước; đường cong là Hann', 11.5, color=MUTED)
    s.save('7-1-frames', 'STFT chia waveform thành các frame chồng nửa nhau, nhân cửa sổ Hann.')


def spectrogram71():
    ns = ns71()
    P, fr, ce = ns['power'], ns['frequencies'], ns['centers']
    db = 10 * np.log10(np.maximum(P, 1e-12) / P.max())
    s = Fig(640, 250)
    ax = s.axes(70, 20, 470, 180, (0, 1), (0, 1000), xticks=[0, .25, .5, .75, 1], yticks=[0, 200, 600, 1000], xlabel='giây', grid=False)
    heat(s, ax, db, 0, 1, 0 - 5, 1000 + 5, lo=-80)
    s.label(ax.X(.25), ax.Y(200) - 12, '200 Hz', 11.5, color=TEXT)
    s.label(ax.X(.75), ax.Y(600) - 12, '600 Hz', 11.5, color=TEXT)
    s.label(ax.X(1) + 10, ax.Y(1000), 'Hz theo trục dọc', 11, 'start', FAINT)
    s.label(ax.X(1) + 10, ax.Y(900), '0 dB', 11, 'start', CLAY)
    s.label(ax.X(1) + 10, ax.Y(100), '−80 dB', 11, 'start', FAINT)
    s.save('7-1-spectrogram', 'Spectrogram: 200 Hz ở nửa giây đầu, 600 Hz ở nửa giây sau.')


def tradeoff71():
    from scipy.signal.windows import hann
    fs = 2000
    t = np.arange(fs) / fs
    sig = .5 * np.sin(2 * np.pi * 300 * t) + .5 * np.sin(2 * np.pi * 330 * t)
    sig[1000:1006] += 2.0
    s = Fig(640, 265)
    for k, (L, H) in enumerate([(40, 10), (400, 10)]):
        frames = np.lib.stride_tricks.sliding_window_view(sig, L)[::H]
        sp = np.abs(np.fft.rfft(frames * hann(L, sym=False), axis=1)) ** 2
        db = 10 * np.log10(np.maximum(sp.T, 1e-12) / sp.max())
        fr = np.fft.rfftfreq(L, 1 / fs)
        keep = fr <= 600
        x0 = 60 + k * 300
        ax = s.axes(x0, 36, 240, 160, (0, 1), (0, 600), xticks=[0, .5, 1], yticks=[0, 300, 600] if k == 0 else [], xlabel='giây', grid=False)
        heat(s, ax, db[keep], L / 2 / fs, 1 - L / 2 / fs, 0, 600 + fs / L / 2, lo=-40)
        s.label(x0 + 120, 22, f'window {L} mẫu ({L * 1000 // fs} ms)', 12, color=TEXT, weight=600)
    s.label(320, 252, 'tín hiệu: hai âm 300 Hz và 330 Hz, cộng một tiếng gõ ngắn ở 0.5 s', 11.5, color=MUTED)
    s.save('7-1-tradeoff', 'Cửa sổ ngắn định vị tiếng gõ sắc nhưng nhòe tần số; cửa sổ dài thì ngược lại.')


def mel71():
    ns = ns71()
    W, fr = ns['filters'], ns['frequencies']
    s = Fig(640, 210)
    ax = s.axes(60, 24, 520, 140, (0, 1000), (0, 1.1), xticks=[0, 250, 500, 750, 1000], yticks=[0, 1], xlabel='Hz', grid=False)
    for b in range(W.shape[0]):
        ax.line(fr, W[b], CLAY if b % 2 == 0 else BLUE, 1.3)
    s.label(ax.x - 8, ax.y - 8, 'trọng số', 11.5, 'start', FAINT)
    s.label(320, 200, '20 tam giác đều theo mel: hẹp ở tần số thấp, rộng dần ở tần số cao', 11.5, color=MUTED)
    s.save('7-1-mel', 'Bộ lọc mel hẹp ở tần số thấp, rộng dần ở tần số cao.')


def logmel71():
    ns = ns71()
    L = ns['log_mel']
    s = Fig(640, 230)
    ax = s.axes(80, 20, 440, 170, (0, 1), (0, 20), xticks=[0, .5, 1], yticks=[0, 10, 20], xlabel='giây', grid=False)
    heat(s, ax, L, 0, 1, 0, 20, lo=-80)
    s.mono(ax.X(1) + 10, ax.Y(6), 'hàng: mel band', 11, 'start', FAINT)
    s.mono(ax.X(1) + 10, ax.Y(18), 'shape (20, 19)', 11.5, 'start', MUTED)
    s.mono(ax.X(1) + 10, ax.Y(15), 'min −112.1 dB', 11, 'start', FAINT)
    s.mono(ax.X(1) + 10, ax.Y(12), 'max 0 dB', 11, 'start', CLAY)
    s.save('7-1-logmel', 'Log-mel: năng lượng ở band thấp nửa đầu, band cao hơn nửa sau.')


def peaknorm71():
    t = np.arange(400) / 2000
    rng = np.random.default_rng(0)
    base = np.sin(2 * np.pi * 100 * t) + .3 * np.sin(2 * np.pi * 230 * t) + .05 * rng.standard_normal(400)
    normal, jam = .2 * base, .6 * base
    s = Fig(640, 245)
    for k, (title, a, b) in enumerate([('trước', normal, jam), ('sau peak normalize', normal / np.abs(normal).max(), jam / np.abs(jam).max())]):
        x0 = 60 + k * 300
        ax = s.axes(x0, 40, 240, 130, (0, .2), (-1.1, 1.1), xticks=[0, .1, .2], yticks=[-1, 0, 1] if k == 0 else [], grid=False, xlabel='giây')
        ax.line(t, b, CLAY, 1.2).line(t, a, BLUE, 1.2)
        s.label(x0 + 120, 24, title, 12, color=TEXT, weight=600)
    s.label(320, 212, 'cam: máy kẹt · xanh: máy bình thường', 11.5, color=TEXT)
    s.label(320, 232, 'minh họa: hai clip cùng dạng sóng, biên độ gấp 3; chuẩn hóa từng clip làm chúng trùng nhau', 11.5, color=MUTED)
    s.save('7-1-peaknorm', 'Peak normalize từng clip xóa mất khác biệt biên độ giữa máy bơm kẹt và bình thường.')


def specaug71():
    ns = ns71()
    L = ns['log_mel'].copy()
    s = Fig(640, 245)
    for k, title in enumerate(['log-mel', 'sau time mask và frequency mask']):
        M = L.copy()
        if k:
            M[:, 8:11] = -80
            M[12:16, :] = -80
        x0 = 60 + k * 300
        ax = s.axes(x0, 36, 240, 150, (0, 1), (0, 20), xticks=[0, .5, 1], yticks=[0, 10, 20] if k == 0 else [], xlabel='giây', grid=False)
        heat(s, ax, M, 0, 1, 0, 20, lo=-80)
        if k:
            s.box(ax.X(8 / 19), ax.y, ax.X(11 / 19) - ax.X(8 / 19), ax.h, BLUE, 'none', r=0, width=1.4, dash='3 3')
            s.box(ax.x, ax.Y(16), ax.w, ax.Y(12) - ax.Y(16), GREEN, 'none', r=0, width=1.4, dash='3 3')
        s.label(x0 + 120, 22, title, 12, color=TEXT, weight=600)
    s.label(320, 232, 'vùng che được điền một giá trị; điền gì phụ thuộc thang đang dùng (ở đây −80 dB)', 11.5, color=MUTED)
    s.save('7-1-specaug', 'SpecAugment che một dải thời gian và một dải tần khi train.')


FIGS71 = {'7-1-sampling': sampling71, '7-1-alias': alias71, '7-1-downsample': downsample71, '7-1-frames': frames71,
          '7-1-spectrogram': spectrogram71, '7-1-tradeoff': tradeoff71, '7-1-mel': mel71, '7-1-logmel': logmel71,
          '7-1-peaknorm': peaknorm71, '7-1-specaug': specaug71}

# ───────────────────────────── 7.2 ─────────────────────────────

_T72 = {}


def ns72(upto=4):
    if upto not in _T72:
        _T72[upto] = lesson_ns('7.2', upto=upto)
    return _T72[upto]


def task72():
    s = Fig(640, 250)
    rows = [('một nhãn cho clip', '(B, C)', 'softmax, cross-entropy', CLAY), ('nhiều nhãn có/không', '(B, C)', 'sigmoid, BCE', SAND),
            ('nhãn theo thời gian', '(B, T, C)', 'mỗi frame một dự đoán', GREEN)]
    for r, (nm, shp, loss, col) in enumerate(rows):
        y = 26 + r * 74
        s.label(30, y + 6, nm, 12.5, 'start', TEXT, 600)
        s.mono(30, y + 26, shp, 11.5, 'start', MUTED)
        s.label(30, y + 44, loss, 11, 'start', MUTED)
        for j in range(16):
            s.box(240 + j * 22, y, 20, 30, 'none', BLUE, r=2, width=0, opacity=.12 + .1 * ((j * 7) % 5) / 4)
        if r == 0:
            s.box(240, y + 36, 350, 18, 'none', col, r=4, width=0, opacity=.4)
            s.mono(415, y + 45.5, 'chuông', 11, 'middle', TEXT)
        elif r == 1:
            s.box(240, y + 36, 350, 9, 'none', col, r=2, width=0, opacity=.5)
            s.box(240, y + 46, 350, 9, 'none', BLUE, r=2, width=0, opacity=.35)
            s.mono(600, y + 41, 'xe', 10, 'start', TEXT)
            s.mono(600, y + 51, 'nói', 10, 'start', TEXT)
        else:
            on = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
            for j, v in enumerate(on):
                s.box(240 + j * 22, y + 36, 20, 18, 'none', col if v else FAINT, r=2, width=0, opacity=.5 if v else .12)
    s.save('7-2-task', 'Ba dạng bài: một nhãn cho clip, nhiều nhãn độc lập, hoặc nhãn cho từng frame.')


def pair72():
    ns = ns72(1)
    F_, y = ns['features'], ns['labels']
    s = Fig(640, 232)
    for k, idx in enumerate([0, 1]):
        x0 = 70 + k * 290
        ax = s.axes(x0, 34, 220, 150, (0, 8), (0, 24), xticks=[0, 4, 8], yticks=[0, 12, 24] if k == 0 else [], xlabel='frame', grid=False)
        M = F_[idx]
        heat(s, ax, M - M.max(), 0, 8, 0, 24, lo=-40)
        s.line(ax.X(4), ax.y, ax.X(4), ax.y + ax.h, FAINT, 1, '3 3')
        s.label(x0 + 110, 20, f'nhãn {y[idx]}: ' + ('thấp → cao' if y[idx] == 1 else 'cao → thấp'), 12, color=TEXT, weight=600)
    s.save('7-2-pair', 'Hai lớp có cùng tập frame, chỉ khác thứ tự.')


def split72():
    ns = ns72(2)
    g, tr, va = ns['groups'], ns['train_indices'], ns['valid_indices']
    vg = set(g[va])
    s = Fig(640, 170)
    for sess in range(20):
        x = 30 + sess * 29
        col = CLAY if sess in vg else BLUE
        for r in range(4):
            s.box(x, 40 + r * 18, 24, 14, 'none', col, r=2, width=0, opacity=.45 if sess in vg else .2)
        s.mono(x + 12, 124, str(sess), 9.5, 'middle', MUTED)
    s.label(320, 22, 'mỗi cột là một phiên, bốn ô là bốn clip của phiên ấy', 11.5, color=MUTED)
    s.label(320, 152, 'validation (cam): 5 phiên, 20 clip; giao group với train bằng 0', 11.5, color=CLAY)
    s.save('7-2-split', 'Chia theo phiên ghi: mỗi phiên nằm trọn ở train hoặc validation.')


def order72():
    s = Fig(640, 230)
    A = [['3', '0'], ['0', '3']]
    B = [['0', '3'], ['3', '0']]
    for k, (M, nm, mean, delta, col) in enumerate([(A, 'clip A', '(1.5, 1.5)', '(−3, 3)', BLUE), (B, 'clip B', '(1.5, 1.5)', '(3, −3)', CLAY)]):
        x0 = 60 + k * 310
        fills = {(i, j): (col, .4 if M[i][j] == '3' else .06) for i in range(2) for j in range(2)}
        s.tiles(x0, 50, M, 50, 40, col, 4, fills, size=14)
        s.label(x0 + 52, 32, nm, 12.5, color=TEXT, weight=600)
        s.label(x0 - 8, 70, 'band 1', 10.5, 'end', MUTED)
        s.label(x0 - 8, 114, 'band 2', 10.5, 'end', MUTED)
        s.mono(x0 + 120, 64, f'mean  {mean}', 12, 'start', TEXT)
        s.mono(x0 + 120, 92, f'delta {delta}', 12, 'start', col, 600)
    s.label(320, 170, 'mean theo thời gian bằng nhau: không hàm nào của mean tách được hai clip', 11.5, color=MUTED)
    s.label(320, 192, 'delta (frame sau trừ frame trước) đổi dấu khi đảo thứ tự', 11.5, color=MUTED)
    s.save('7-2-order', 'Đổi thứ tự hai frame không đổi trung bình; delta thì đổi dấu.')


def confusion72():
    s = Fig(640, 220)
    for k, (nm, M, acc) in enumerate([('baseline: mean từng band', [[10, 0], [10, 0]], 'acc 0.500 · macro-F1 0.333'),
                                       ('CNN trên log-mel', [[10, 0], [0, 10]], 'acc 1.000 · macro-F1 1.000')]):
        x0 = 110 + k * 280
        fills = {(i, j): ((GREEN if i == j else CLAY), .08 + .045 * M[i][j]) for i in range(2) for j in range(2)}
        s.tiles(x0, 56, [[str(v) for v in r] for r in M], 64, 44, BLUE, 5, fills, size=15)
        s.label(x0 + 66, 28, nm, 12.5, color=TEXT, weight=600)
        s.label(x0 + 32, 46, 'đoán 0', 10.5, color=MUTED)
        s.label(x0 + 101, 46, 'đoán 1', 10.5, color=MUTED)
        if k == 0:
            s.label(x0 - 8, 78, 'thật 0', 10.5, 'end', MUTED)
            s.label(x0 - 8, 127, 'thật 1', 10.5, 'end', MUTED)
        s.mono(x0 + 66, 172, acc, 11.5, 'middle', CLAY if k == 0 else GREEN)
    s.save('7-2-confusion', 'Baseline gộp thời gian đoán một lớp cho mọi clip; CNN đúng cả 20.')


def pooling72():
    s = Fig(640, 240)
    c = 22
    for k, (title, kw, res, col) in enumerate([('kernel 3×3 rồi mean thời gian', 3, 'train 1.000 · valid 0.950', GREEN),
                                                ('kernel 3×1 rồi mean thời gian', 1, 'train 0.500 · valid 0.500', CLAY)]):
        x0 = 70 + k * 290
        fills = {(i, j): ((BLUE, .32) if (j < 4) == (i >= 4) else (FAINT, .08)) for i in range(8) for j in range(8)}
        s.tiles(x0, 46, [[''] * 8] * 8, c, 14, FAINT, 2, fills, r=2)
        jc = 4 if kw == 3 else 3
        s.box(x0 + (jc - (kw // 2)) * (c + 2) - 2, 46 + 3 * 16 - 2, kw * (c + 2) + 2, 3 * 16 + 2, col, 'none', r=3, width=2)
        s.line(x0 + 4 * (c + 2) - 1, 40, x0 + 4 * (c + 2) - 1, 176, FAINT, 1, '3 3')
        s.label(x0 + 95, 26, title, 12, color=TEXT, weight=600)
        s.mono(x0 + 95, 200, res, 11.5, 'middle', col, 600)
    s.label(320, 228, 'kernel phải nhìn qua ranh giới frame 4 | 5 thì thứ tự mới còn sau bước gộp', 11.5, color=MUTED)
    s.save('7-2-pooling', 'Kernel 3×3 nhìn ba frame kề nhau nên thấy chỗ chuyển; kernel 3×1 thì không.')


def windows72():
    p = [.05, .10, .92, .08, .06]
    s = Fig(640, 220)
    ax = s.axes(80, 30, 380, 150, (0, 5), (0, 1), xticks=[], yticks=[0, .5, 1], grid=False)
    for k, v in enumerate(p):
        s.rect(ax.X(k + .15), ax.Y(v), ax.X(.7) - ax.X(0), ax.Y(0) - ax.Y(v), 'none', CLAY if v > .5 else BLUE, 3, .55, 0)
        s.mono(ax.X(k + .5), ax.Y(v) - 8, f'{v:.2f}', 11, 'middle', TEXT)
        s.mono(ax.X(k + .5), ax.y + ax.h + 14, f'cửa sổ {k + 1}', 10.5, 'middle', MUTED)
    ax.hline(.5, FAINT, 1, '3 3')
    s.label(ax.x - 8, ax.y - 12, 'P(có còi)', 11.5, 'start', FAINT)
    s.mono(500, 80, 'mean 0.242', 13, 'start', BLUE, 600)
    s.label(500, 100, 'dưới 0.5: bỏ sót', 11.5, 'start', MUTED)
    s.mono(500, 136, 'max  0.920', 13, 'start', CLAY, 600)
    s.label(500, 156, 'một cửa sổ chắc là đủ', 11.5, 'start', MUTED)
    s.save('7-2-windows', 'Trung bình xác suất các cửa sổ bỏ sót tiếng còi; lấy max thì bắt được.')


def maskpool72():
    s = Fig(640, 210)
    s.label(40, 30, 'clip 1: hai bước thật, hai bước padding', 12, 'start', TEXT, 600)
    vecs = ['(1, 2)', '(3, 4)', '(0, 0)', '(0, 0)']
    for j, v in enumerate(vecs):
        s.box(40 + j * 80, 46, 72, 32, 'none', BLUE if j < 2 else FAINT, r=5, width=0, opacity=.25 if j < 2 else .1)
        s.mono(76 + j * 80, 62.5, v, 11.5, 'middle', TEXT if j < 2 else FAINT)
        s.mono(76 + j * 80, 92, f'a = {1 if j < 2 else 0}', 10.5, 'middle', MUTED)
    s.mono(400, 56, 'chia cho 4:  (1, 1.5)', 12.5, 'start', CLAY)
    s.mono(400, 82, 'chia cho 2:  (2, 3)', 12.5, 'start', GREEN, 600)
    s.label(320, 140, 'chia cho số bước đã pad thì embedding phụ thuộc clip nào được ghép cùng batch', 11.5, color=MUTED)
    s.mono(320, 170, 'z = Σ a_t h_t / Σ a_t', 12.5, 'middle', TEXT)
    s.save('7-2-maskpool', 'Chia cho 2 bước thật ra (2, 3); chia cho cả 4 bước đã pad ra (1, 1.5).')


def timemask72():
    s = Fig(640, 170)
    W = 560
    s.rect(40, 50, W, 30, 'none', FAINT, 3, .12, 0)
    sc = W / 200
    s.rect(40 + 90 * sc, 50, 5 * sc, 30, 'none', CLAY, 1, .8, 0)
    s.label(40 + 92 * sc, 40, 'tiếng gõ 5 frame', 11.5, color=CLAY)
    s.rect(40 + 70 * sc, 46, 40 * sc, 38, BLUE, 'none', 3, 1, 1.6)
    s.label(40 + 90 * sc, 104, 'time mask 40 frame', 11.5, color=BLUE)
    s.mono(40, 104, '0', 10.5, 'start', FAINT)
    s.mono(40 + W, 104, '2 s', 10.5, 'end', FAINT)
    s.label(320, 146, 'mask rộng hơn sự kiện ngắn nhất có thể che trọn bằng chứng mà nhãn vẫn là “gõ cửa”', 11.5, color=MUTED)
    s.save('7-2-timemask', 'Time mask dài hơn sự kiện có thể che trọn tiếng gõ mà nhãn vẫn là “gõ cửa”.')


FIGS72 = {'7-2-task': task72, '7-2-pair': pair72, '7-2-split': split72, '7-2-order': order72, '7-2-confusion': confusion72,
          '7-2-pooling': pooling72, '7-2-windows': windows72, '7-2-maskpool': maskpool72, '7-2-timemask': timemask72}

# ───────────────────────────── 7.3 ─────────────────────────────

_T73 = {}


def ns73():
    if not _T73:
        _T73['ns'] = lesson_ns('7.3', upto=3)
    return _T73['ns']


def asr73():
    s = Fig(640, 220)
    toks = ['em', 'em', '_', '_', 'học', 'học', 'học', '_', 'AI', 'AI', '_', '_']
    x0, w, g = 130, 30, 3
    s.label(20, 44, 'CTC', 12.5, 'start', TEXT, 600)
    for j, t in enumerate(toks):
        blank = t == '_'
        s.box(x0 + j * (w + g), 30, w, 28, 'none', FAINT if blank else BLUE, r=3, width=0, opacity=.1 if blank else .25)
        s.mono(x0 + j * (w + g) + w / 2, 44.5, t, 10, 'middle', FAINT if blank else TEXT)
    xe = x0 + 12 * (w + g)
    s.arrow(xe + 4, 44, xe + 34, 44, MUTED, 1.3)
    s.mono(xe + 42, 44.5, 'em học AI', 12, 'start', CLAY, 600)
    s.label(20, 124, 'encoder–', 12.5, 'start', TEXT, 600)
    s.label(20, 142, 'decoder', 12.5, 'start', TEXT, 600)
    for j in range(12):
        s.box(x0 + j * (w + g), 104, w, 20, 'none', BLUE, r=3, width=0, opacity=.12)
    s.label(x0 + 6 * (w + g), 96, 'hidden của encoder', 10.5, color=FAINT)
    out = ['<sot>', 'em', 'học', 'AI', '<eot>']
    for k, t in enumerate(out):
        cx = x0 + 30 + k * 82
        s.box(cx - 30, 160, 60, 26, 'none', CLAY if 0 < k < 4 else FAINT, r=5, width=0, opacity=.25 if 0 < k < 4 else .12)
        s.mono(cx, 173.5, t, 11, 'middle', TEXT if 0 < k < 4 else MUTED)
        s.line(cx, 156, cx, 128, FAINT, 1, '2 3')
        if k < 4:
            s.arrow(cx + 32, 173, cx + 50, 173, MUTED, 1.2)
    s.save('7-3-asr', 'CTC cho mỗi frame một nhãn rồi gộp; encoder–decoder sinh từng token.')


def align73():
    s = Fig(640, 190)
    x0, sc = 90, 170
    true = [('em', .10, .30), ('học', .30, .75), ('AI', .75, 1.20), ('hôm', 1.80, 2.15), ('nay', 2.15, 2.90)]
    even = [(w, i * .6, (i + 1) * .6) for i, w in enumerate(['em', 'học', 'AI', 'hôm', 'nay'])]
    for row, (nm, spans, col, y) in enumerate([('lời thật', true, BLUE, 34), ('chia đều', even, CLAY, 92)]):
        s.label(x0 - 12, y + 14, nm, 12, 'end', TEXT, 600)
        for w, a, b in spans:
            s.box(x0 + a * sc + 1, y, (b - a) * sc - 2, 28, 'none', col, r=4, width=0, opacity=.28)
            s.mono(x0 + (a + b) / 2 * sc, y + 14.5, w, 11.5, 'middle', TEXT)
    s.label(x0 + 1.5 * sc, 48, 'ngừng', 11, color=FAINT)
    for t in range(4):
        s.line(x0 + t * sc, 132, x0 + t * sc, 137, FAINT, 1)
        s.mono(x0 + t * sc, 150, f'{t} s', 10.5, 'middle', FAINT)
    s.line(x0, 132, x0 + 3 * sc, 132, FAINT, 1)
    s.save('7-3-align', 'Người nói ngừng giữa câu, nên chia đều thời gian cho các từ sẽ lệch.')


def ctc73():
    from itertools import product
    P = np.array([[.6, .4], [.5, .5], [.4, .6]])
    rows = []
    for path in product(range(2), repeat=3):
        p = float(np.prod(P[np.arange(3), path]))
        out = []
        for i, c in enumerate(path):
            if c == 1 and (i == 0 or path[i - 1] != 1):
                out.append('a')
        rows.append((''.join(out), path, p))
    order = {'': 0, 'a': 1, 'aa': 2}
    rows.sort(key=lambda r: (order[r[0]], -r[2]))
    s = Fig(640, 230)
    y0, dy = 22, 25
    groups = {}
    for i, (tr, path, p) in enumerate(rows):
        y = y0 + i * dy
        for j, c in enumerate(path):
            s.box(80 + j * 30, y - 10, 26, 20, 'none', FAINT if c == 0 else BLUE, r=3, width=0, opacity=.1 if c == 0 else .28)
            s.mono(93 + j * 30, y + .5, '_a'[c], 11, 'middle', FAINT if c == 0 else TEXT)
        s.mono(190, y + .5, f'{p:.2f}', 11, 'start', MUTED)
        groups.setdefault(tr, []).append(y)
    cols = {'': FAINT, 'a': CLAY, 'aa': SAND}
    for tr, ys in groups.items():
        cy = sum(ys) / len(ys)
        for y in ys:
            s.line(232, y, 380, cy, SOFT_LINE, 1)
        tot = sum(p for t, _, p in rows if t == tr)
        s.box(384, cy - 14, 150, 28, 'none', cols[tr], r=5, width=0, opacity=.3)
        s.mono(396, cy + .5, tr or 'rỗng', 12, 'start', TEXT, 600)
        s.mono(522, cy + .5, f'{tot:.2f}', 12, 'end', TEXT, 600)
    s.save('7-3-ctc', 'Tám path gộp thành ba transcript; “a” gom sáu path, xác suất 0.76.')


def greedy73():
    s = Fig(640, 180)
    fills = {(0, 0): (BLUE, .35), (0, 1): (BLUE, .35), (1, 0): (FAINT, .1), (1, 1): (FAINT, .1)}
    s.tiles(90, 46, [['0.6', '0.6'], ['0.4', '0.4']], 54, 32, BLUE, 4, fills, size=13)
    s.label(80, 63, '_', 13, 'end', MUTED)
    s.label(80, 99, 'a', 13, 'end', MUTED)
    s.label(117, 32, 't = 1', 10.5, color=FAINT)
    s.label(175, 32, 't = 2', 10.5, color=FAINT)
    s.label(146, 140, 'greedy chọn _ ở cả hai frame', 11, color=BLUE)
    s.mono(300, 62, 'rỗng', 12.5, 'start', TEXT)
    s.mono(360, 62, '__', 12, 'start', MUTED)
    s.mono(560, 62, '0.36', 12.5, 'end', BLUE, 600)
    s.mono(300, 102, 'a', 12.5, 'start', TEXT, 600)
    s.mono(360, 102, 'a_ + _a + aa', 12, 'start', MUTED)
    s.mono(560, 102, '0.64', 12.5, 'end', CLAY, 600)
    s.line(300, 82, 560, 82, SOFT_LINE, 1)
    s.save('7-3-greedy', 'Path tốt nhất ra chuỗi rỗng, nhưng transcript “a” có tổng xác suất cao hơn.')


def ctcdp73():
    H = ns73()['history']
    s = Fig(640, 230)
    X = [200, 330, 460]
    Y = [56, 116, 176]
    for t in range(3):
        s.label(X[t], 22, f't = {t + 1}', 11, color=FAINT)
    for k, lab in enumerate('_a_'):
        s.mono(130, Y[k] + .5, lab, 13, 'middle', MUTED)
    for t in range(1, 3):
        for k in range(3):
            for d in (0, 1):
                if k - d >= 0 and H[t - 1][k - d] > 0:
                    s.arrow(X[t - 1] + 32, Y[k - d] + (6 if d else 0), X[t] - 34, Y[k] - (6 if d else 0), SOFT_LINE, 1.1)
    for t in range(3):
        for k in range(3):
            v = H[t][k]
            end = t == 2 and k >= 1
            s.box(X[t] - 30, Y[k] - 14, 60, 28, 'none', CLAY if end else BLUE, r=5, width=0, opacity=.35 if end else (.2 if v > 0 else .06))
            s.mono(X[t], Y[k] + .5, f'{v:.2f}', 12, 'middle', TEXT if v > 0 else FAINT, 600 if end else 400)
    s.mono(510, 146, '0.48 + 0.28', 12, 'start', CLAY)
    s.mono(510, 168, '= 0.76', 12.5, 'start', CLAY, 600)
    s.save('7-3-ctc-dp', 'Quy hoạch động trên lưới α: hai ô cuối cộng ra 0.76.')


def underflow73():
    s = Fig(640, 230)
    ax = s.axes(90, 24, 400, 160, (0, 1000), (-400, 0), xticks=[0, 500, 1000], yticks=[-400, -300, -200, -100, 0], xlabel='số frame', grid=False)
    ax.line([0, 400], [0, -400], CLAY, 2)
    ax.hline(-38, BLUE, 1.2, '4 4')
    ax.hline(-308, BLUE, 1.2, '4 4')
    s.mono(ax.X(1000) + 8, ax.Y(-38), 'float32', 11, 'start', BLUE)
    s.mono(ax.X(1000) + 8, ax.Y(-308), 'float64', 11, 'start', BLUE)
    s.label(ax.x - 8, ax.y - 12, 'log₁₀ của tích', 11, 'start', FAINT)
    s.mono(ax.X(560), ax.Y(-200), 'log α ≈ −2303 ở frame 1000', 11, 'start', MUTED)
    s.mono(ax.X(560), ax.Y(-230), 'vẫn biểu diễn được', 11, 'start', MUTED)
    s.save('7-3-underflow', 'Tích xác suất nhỏ dần về 0 sau vài chục frame; log-space thì không.')


def repeat73():
    ext = ['_', 'a', '_', 'a', '_']
    s = Fig(640, 240)

    def lattice(x0, T, title, path=None):
        reach = np.zeros((T, 5), bool)
        reach[0, :2] = True
        for t in range(1, T):
            for k in range(5):
                ok = reach[t - 1, k] or (k >= 1 and reach[t - 1, k - 1])
                if k >= 2 and ext[k] != '_' and ext[k] != ext[k - 2]:
                    ok = ok or reach[t - 1, k - 2]
                reach[t, k] = ok
        for k in range(5):
            s.mono(x0 - 14, 50 + k * 32 + 13.5, ext[k], 12, 'middle', MUTED)
            for t in range(T):
                on = reach[t, k]
                s.box(x0 + t * 50, 50 + k * 32, 44, 27, 'none', BLUE if on else FAINT, r=4, width=0, opacity=.25 if on else .07)
        for k in (3, 4):
            s.box(x0 + (T - 1) * 50 - 2, 50 + k * 32 - 2, 48, 31, CLAY, 'none', r=5, width=1.4, dash='3 3')
        if path:
            pts = [(x0 + t * 50 + 22, 50 + k * 32 + 13.5) for t, k in enumerate(path)]
            for (a, b), (c, d) in zip(pts, pts[1:]):
                s.line(a, b, c, d, CLAY, 2)
            for a, b in pts:
                s.circle(a, b, 4, CLAY, CLAY)
        s.label(x0 + (T * 50 - 6) / 2, 30, title, 12, color=TEXT, weight=600)

    lattice(150, 2, 'T = 2: không tới ô cuối')
    lattice(400, 3, 'T = 3: a _ a', path=[1, 2, 3])
    s.label(320, 222, 'khung đứt: hai ô path phải dừng ở frame cuối', 11, color=MUTED)
    s.save('7-3-repeat', 'Target “aa” cần blank chen giữa, nên 2 frame không đủ.')


def whisper73():
    s = Fig(640, 210)
    steps = [('audio', '16 kHz'), ('pad / cắt', '30 s'), ('log-mel', '3000 frame'), ('encoder', '1500 vị trí')]
    for i, (a, b) in enumerate(steps):
        x = 30 + i * 150
        s.box(x, 26, 116, 48, 'none', BLUE, r=6, width=0, opacity=.16)
        s.label(x + 58, 42, a, 12, color=TEXT, weight=600)
        s.mono(x + 58, 61, b, 11, 'middle', MUTED)
        if i < 3:
            s.arrow(x + 120, 50, x + 146, 50, MUTED, 1.3)
    toks = ['<|startoftranscript|>', '<|vi|>', '<|transcribe|>']
    x = 30
    for t in toks:
        w = s.mono_width(t, 11) + 18
        s.box(x, 132, w, 28, 'none', SAND, r=5, width=0, opacity=.3)
        s.mono(x + w / 2, 146.5, t, 11, 'middle', TEXT)
        x += w + 8
    s.arrow(x + 2, 146, x + 28, 146, MUTED, 1.3)
    s.mono(x + 36, 146.5, 'em học AI hôm nay', 12, 'start', CLAY, 600)
    s.curve(538, 76, 400, 128, .2, FAINT, 1.1, dash='3 3')
    s.label(320, 186, 'decoder bắt đầu bằng dãy token chọn ngôn ngữ và việc cần làm', 11, color=MUTED)
    s.save('7-3-whisper', 'Whisper đưa audio về 30 giây, 3000 frame log-mel, 1500 vị trí encoder.')


def wer73():
    s = Fig(640, 190)
    ref = ['em', 'học', 'ai', 'hôm', 'nay']
    pred = ['em', 'học', 'toán', None, 'nay']
    ops = ['', '', 'S', 'D', '']
    x0, w = 150, 72
    s.label(x0 - 16, 47, 'reference', 11.5, 'end', MUTED)
    s.label(x0 - 16, 97, 'prediction', 11.5, 'end', MUTED)
    for j in range(5):
        col = CLAY if ops[j] == 'S' else SAND if ops[j] == 'D' else BLUE
        x = x0 + j * (w + 8)
        s.box(x, 32, w, 30, 'none', col, r=5, width=0, opacity=.25)
        s.mono(x + w / 2, 47.5, ref[j], 12, 'middle', TEXT)
        if pred[j]:
            s.box(x, 82, w, 30, 'none', col, r=5, width=0, opacity=.25)
            s.mono(x + w / 2, 97.5, pred[j], 12, 'middle', TEXT)
        else:
            s.box(x, 82, w, 30, col, 'none', r=5, width=1.2, dash='3 3')
        if ops[j]:
            s.mono(x + w / 2, 132, ops[j], 12.5, 'middle', col, 600)
    s.mono(320, 166, 'WER = (S + D + I) / N = (1 + 1 + 0) / 5 = 0.4', 12, 'middle', TEXT)
    s.save('7-3-wer', 'Một thay thế, một xóa trên 5 từ: WER 0.4.')


def werdp73():
    ref = ['em', 'học', 'ai', 'hôm', 'nay']
    pred = ['em', 'học', 'toán', 'nay']
    R, C = len(ref), len(pred)
    D = np.zeros((R + 1, C + 1), int)
    D[:, 0] = range(R + 1)
    D[0, :] = range(C + 1)
    for i in range(1, R + 1):
        for j in range(1, C + 1):
            D[i, j] = min(D[i - 1, j] + 1, D[i, j - 1] + 1, D[i - 1, j - 1] + (ref[i - 1] != pred[j - 1]))
    i, j, path = R, C, {(R, C)}
    while i or j:
        if i and j and D[i, j] == D[i - 1, j - 1] + (ref[i - 1] != pred[j - 1]):
            i, j = i - 1, j - 1
        elif i and D[i, j] == D[i - 1, j] + 1:
            i -= 1
        else:
            j -= 1
        path.add((i, j))
    s = Fig(640, 250)
    cw, ch, g, x0, y0 = 56, 28, 4, 190, 44
    fills = {(a, b): (CLAY, .35) if (a, b) in path else (BLUE, .08) for a in range(R + 1) for b in range(C + 1)}
    s.tiles(x0, y0, [[str(v) for v in r] for r in D], cw, ch, BLUE, g, fills, size=12)
    for b, t in enumerate([''] + pred):
        s.mono(x0 + b * (cw + g) + cw / 2, y0 - 14, t, 11, 'middle', MUTED)
    for a, t in enumerate([''] + ref):
        s.mono(x0 - 12, y0 + a * (ch + g) + ch / 2 + .5, t, 11, 'end', MUTED)
    s.label(x0 + 2.5 * (cw + g), 14, 'prediction', 11, color=FAINT)
    s.label(x0 - 60, y0 - 14, 'reference', 11, 'end', FAINT)
    s.mono(x0 + 5 * (cw + g) + 6, y0 + 5 * (ch + g) + ch / 2, '← distance 2', 11.5, 'start', CLAY)
    s.save('7-3-wer-dp', 'Bảng edit distance; đường tô màu là một cách ghép tối ưu.')


def corpus73():
    s = Fig(640, 170)
    rows = [(['em', 'học', 'AI'], 2), (['mai', 'lớp', 'em', 'học', 'lập', 'trình', 'thi', 'đấu'], None)]
    for r, (toks, bad) in enumerate(rows):
        y = 34 + r * 50
        for j, t in enumerate(toks):
            col = CLAY if j == bad else BLUE
            s.box(24 + j * 44, y, 40, 28, 'none', col, r=4, width=0, opacity=.35 if j == bad else .18)
            s.mono(44 + j * 44, y + 14.5, t, 10.5, 'middle', TEXT)
    s.label(24 + 3 * 44 + 6, 48, 'sai 1 / 3', 11, 'start', CLAY)
    s.label(24 + 8 * 44 + 6, 98, 'đúng 8 / 8', 11, 'start', MUTED)
    s.mono(470, 52, 'corpus', 11.5, 'start', MUTED)
    s.mono(470, 72, '1/11 = 0.091', 12.5, 'start', TEXT, 600)
    s.mono(470, 104, 'trung bình câu', 11.5, 'start', MUTED)
    s.mono(470, 124, '(1/3 + 0)/2 = 0.167', 12.5, 'start', TEXT, 600)
    s.save('7-3-corpus', 'Corpus WER 0.091; trung bình WER từng câu 0.167.')


def pad73():
    s = Fig(640, 170)
    x0, W = 120, 340
    for r, (nm, sec) in enumerate([('clip 30 s', 30), ('clip 3 s', 3)]):
        y = 36 + r * 52
        s.label(x0 - 12, y + 14, nm, 12, 'end', TEXT, 600)
        s.box(x0, y, W * sec / 30, 28, 'none', BLUE, r=4, width=0, opacity=.3)
        if sec < 30:
            s.box(x0 + W * sec / 30 + 2, y, W * (30 - sec) / 30 - 2, 28, 'none', FAINT, r=4, width=0, opacity=.12)
            s.label(x0 + W * .55, y + 14, 'pad 27 s', 11, color=FAINT)
        s.mono(x0 + W + 20, y + 14.5, '1500 vị trí', 12, 'start', MUTED)
    s.label(320, 150, 'encoder làm cùng một lượng tính; chỉ decoder ngắn đi', 11.5, color=MUTED)
    s.save('7-3-pad', 'Clip 3 giây vẫn được pad lên 30 giây, nên thời gian chạy giảm ít.')


def lengths73():
    s = Fig(640, 170)
    x0, W = 110, 360
    for r, (nm, real) in enumerate([('clip 4 s', 100), ('clip 1 s', 25)]):
        y = 34 + r * 50
        s.label(x0 - 12, y + 13, nm, 12, 'end', TEXT, 600)
        s.box(x0, y, W * real / 100, 26, 'none', BLUE, r=4, width=0, opacity=.3)
        if real < 100:
            s.box(x0 + W * real / 100 + 2, y, W * (100 - real) / 100 - 2, 26, 'none', FAINT, r=4, width=0, opacity=.12)
            s.label(x0 + W * .62, y + 13, '75 bước pad', 11, color=FAINT)
        s.mono(x0 + W + 18, y + 13.5, f'{real}', 12.5, 'start', GREEN, 600)
    s.mono(x0 + W + 18, 16, 'input_lengths', 11, 'start', MUTED)
    s.label(320, 150, 'truyền 100 cho clip 1 s thì alignment phải trải qua cả 75 bước pad', 11.5, color=MUTED)
    s.save('7-3-lengths', 'Batch pad về T = 100: clip 1 giây chỉ có 25 bước thật, nên input_lengths đúng là 100 và 25; truyền 100 cho cả hai clip không báo lỗi nhưng bắt CTC giải thích cả phần pad.')


FIGS73 = {'7-3-asr': asr73, '7-3-align': align73, '7-3-ctc': ctc73, '7-3-greedy': greedy73, '7-3-ctc-dp': ctcdp73,
          '7-3-underflow': underflow73, '7-3-repeat': repeat73, '7-3-whisper': whisper73, '7-3-wer': wer73,
          '7-3-wer-dp': werdp73, '7-3-corpus': corpus73, '7-3-pad': pad73, '7-3-lengths': lengths73}

# ───────────────────────────── 7.4 ─────────────────────────────

_T74 = {}


def ns74():
    if not _T74:
        _T74['ns'] = lesson_ns('7.4', upto=5)
    return _T74['ns']


def fusion74():
    s = Fig(640, 240)
    for r, (nm, y) in enumerate([('early', 30), ('late', 140)]):
        s.label(20, y + 34, nm, 12.5, 'start', TEXT, 600)
        s.box(80, y, 70, 26, 'none', BLUE, r=5, width=0, opacity=.25)
        s.label(115, y + 13, 'ảnh v', 11.5, color=TEXT)
        s.box(80, y + 42, 70, 26, 'none', SAND, r=5, width=0, opacity=.3)
        s.label(115, y + 55, 'chữ t', 11.5, color=TEXT)
    # early: nối vector rồi một head
    for j in range(6):
        s.box(200 + j * 18, 51, 16, 22, 'none', BLUE if j < 4 else SAND, r=2, width=0, opacity=.3)
    s.arrow(152, 43, 196, 58, MUTED, 1.2)
    s.arrow(152, 85, 196, 66, MUTED, 1.2)
    s.mono(254, 90, '[v; t]', 11, 'middle', MUTED)
    s.arrow(312, 62, 352, 62, MUTED, 1.2)
    s.box(356, 46, 80, 32, 'none', CLAY, r=6, width=0, opacity=.25)
    s.label(396, 62, 'head', 12, color=TEXT)
    s.arrow(440, 62, 480, 62, MUTED, 1.2)
    s.mono(488, 62.5, 'p', 13, 'start', CLAY, 600)
    # late: mỗi nhánh một head, gộp xác suất
    for k, (yy, col, nm) in enumerate([(153, BLUE, 'p⁽ᵛ⁾'), (195, SAND, 'p⁽ᵗ⁾')]):
        s.arrow(152, yy, 196, yy, MUTED, 1.2)
        s.box(200, yy - 14, 70, 28, 'none', col, r=6, width=0, opacity=.3)
        s.label(235, yy, 'head', 11.5, color=TEXT)
        s.arrow(274, yy, 306, yy, MUTED, 1.2)
        s.mono(312, yy + .5, nm, 12, 'start', TEXT)
        s.arrow(352, yy, 382, 176 + (yy - 174) * .25, MUTED, 1.2)
    s.box(386, 160, 120, 32, 'none', CLAY, r=6, width=0, opacity=.25)
    s.mono(446, 176.5, 'αp⁽ᵛ⁾+(1−α)p⁽ᵗ⁾', 10.5, 'middle', TEXT)
    s.arrow(510, 176, 540, 176, MUTED, 1.2)
    s.mono(548, 176.5, 'p', 13, 'start', CLAY, 600)
    s.save('7-4-fusion', 'Early fusion nối vector hai nguồn; late fusion gộp xác suất của hai head.')


def join74():
    s = Fig(640, 210)
    ids = [1, 2, 3, 4, 5]
    caps = [1, 2, 4, 5]
    s.label(110, 22, 'ảnh', 12, color=TEXT, weight=600)
    s.label(230, 22, 'caption theo hàng', 12, color=TEXT, weight=600)
    s.label(450, 22, 'join theo id', 12, color=TEXT, weight=600)
    for i, a in enumerate(ids):
        y = 40 + i * 30
        s.box(80, y, 60, 24, 'none', BLUE, r=4, width=0, opacity=.22)
        s.mono(110, y + 12.5, f'id {a}', 11, 'middle', TEXT)
        c = caps[i] if i < len(caps) else None
        ok = c == a
        s.box(200, y, 60, 24, 'none' if c else CLAY, (GREEN if ok else CLAY) if c else 'none', r=4, width=0 if c else 1.2,
              opacity=.25 if c else 1, dash=None if c else '3 3')
        if c:
            s.mono(230, y + 12.5, f'id {c}', 11, 'middle', TEXT)
        s.box(420, y, 60, 24, 'none' if a in caps else CLAY, GREEN if a in caps else 'none', r=4, width=0 if a in caps else 1.2,
              opacity=.25 if a in caps else 1, dash=None if a in caps else '3 3')
        s.mono(450, y + 12.5, f'id {a}' if a in caps else 'thiếu', 11, 'middle', TEXT if a in caps else CLAY)
    s.label(230, 196, 'từ hàng 3 trở đi lệch một bậc', 11, color=CLAY)
    s.label(450, 196, 'id 3 thiếu: đếm được', 11, color=MUTED)
    s.save('7-4-join', 'Ghép theo thứ tự hàng làm lệch cặp; join theo id giữ đúng cặp.')


def sync74():
    s = Fig(640, 190)
    x0, sc = 80, 1200  # px mỗi giây, cửa sổ 4.00–4.44 s
    t0 = 4.0

    def X(t):
        return x0 + (t - t0) * sc
    s.label(x0 - 10, 46, 'âm', 12, 'end', TEXT, 600)
    for k in range(400, 441):
        t = k * .01
        s.line(X(t), 36, X(t), 56, CLAY if k == 430 else SOFT_LINE, 2 if k == 430 else 1)
    s.label(x0 - 10, 106, 'video', 12, 'end', TEXT, 600)
    for f in range(100, 111):
        t = f / 25
        s.box(X(t) + 1, 92, sc / 25 - 2, 28, 'none', CLAY if f == 107 else BLUE, r=3, width=0, opacity=.35 if f == 107 else .15)
    s.line(X(4.3), 30, X(4.3), 126, CLAY, 1, '3 3')
    s.mono(X(4.3), 20, 'frame âm 430 = 4.30 s', 11, 'middle', CLAY)
    s.mono(X(107 / 25) + sc / 50, 138, 'khung 107', 11, 'middle', CLAY)
    s.mono(X(107 / 25) + sc / 50, 154, '4.28–4.32 s', 10.5, 'middle', MUTED)
    for t in (4.0, 4.2, 4.4):
        s.mono(X(t), 176, f'{t:.1f} s', 10, 'middle', FAINT)
    s.save('7-4-sync', 'Âm 100 frame/giây, video 25 khung/giây: frame âm 430 rơi vào khung hình 107.')


def xor74():
    ns = ns74()
    X_, y, va = ns['features'], ns['labels'], ns['valid_indices']
    s = Fig(640, 260)
    g = np.linspace(-.35, 1.35, 46)
    gx, gy = np.meshgrid(g, g)
    grid = np.column_stack([gx.ravel(), gy.ravel()])
    for k, (nm, key, acc) in enumerate([('logistic regression', 'linear_fusion', 'valid 0.470'), ('MLP 8 nút ẩn', 'nonlinear_fusion', 'valid 1.000')]):
        ax = s.axes(70 + k * 300, 34, 190, 170, (-.35, 1.35), (-.35, 1.35), xticks=[0, 1], yticks=[0, 1] if k == 0 else [], grid=False)
        pred = ns[key].predict(grid).reshape(gx.shape)
        d = g[1] - g[0]
        for i in range(len(g)):
            for j in range(len(g)):
                s.rect(ax.X(g[j] - d / 2), ax.Y(g[i] + d / 2), ax.X(d) - ax.X(0) + .3, ax.Y(0) - ax.Y(d) + .3, 'none',
                       CLAY if pred[i, j] else BLUE, 0, .1, 0)
        for c, col in ((0, BLUE), (1, CLAY)):
            m = va[y[va] == c]
            ax.dots(X_[m, 0], X_[m, 1], col, 2.6, col)
        s.label(ax.x + 95, 20, nm, 12, color=TEXT, weight=600)
        s.mono(ax.x + 95, 236, acc, 11.5, 'middle', CLAY if k == 0 else GREEN, 600)
    s.save('7-4-xor', 'Logistic regression không tách được XOR; MLP 8 nút ẩn tách đúng bốn góc.')


def late74():
    ns = ns74()
    y = ns['toy_labels']
    rows = [('ảnh', ns['image_probability']), ('chữ', ns['text_probability']), ('fusion', ns['fused_probability'])]
    s = Fig(640, 200)
    x0, cw, ch, g = 100, 52, 30, 5
    for j in range(8):
        s.mono(x0 + j * (cw + g) + cw / 2, 24, f'y = {y[j]}', 10.5, 'middle', MUTED)
    for r, (nm, p) in enumerate(rows):
        yy = 38 + r * (ch + g)
        s.label(x0 - 12, yy + ch / 2, nm, 12, 'end', TEXT, 600 if r == 2 else 400)
        for j in range(8):
            ok = (p[j] >= .5) == bool(y[j])
            s.box(x0 + j * (cw + g), yy, cw, ch, 'none', GREEN if ok else CLAY, r=4, width=0, opacity=.3 if ok else .35)
            s.mono(x0 + j * (cw + g) + cw / 2, yy + ch / 2 + .5, f'{p[j]:.3g}', 11, 'middle', TEXT)
    for r, a in enumerate(['0.500', '0.500', '1.000']):
        s.mono(x0 + 8 * (cw + g) + 6, 38 + r * (ch + g) + ch / 2 + .5, a, 11.5, 'start', TEXT, 600 if r == 2 else 400)
    s.label(320, 180, 'xanh: đúng phía ngưỡng 0.5, cam: sai; hai nhánh sai ở những mẫu khác nhau', 11, color=MUTED)
    s.save('7-4-late', 'Mỗi nhánh sai bốn mẫu khác nhau; trung bình hai xác suất đúng cả tám.')


def ablation74():
    s = Fig(640, 220)
    items = [('chỉ ảnh', .5, BLUE), ('chỉ chữ', .5, SAND), ('ghép đúng cặp', 1.0, GREEN), ('ghép sai cặp', .5, CLAY)]
    ax = s.axes(90, 26, 440, 150, (0, 4), (0, 1), xticks=[], yticks=[0, .5, 1], grid=False)
    for k, (nm, v, col) in enumerate(items):
        s.rect(ax.X(k + .2), ax.Y(v), ax.X(.6) - ax.X(0), ax.Y(0) - ax.Y(v), 'none', col, 3, .5, 0)
        s.mono(ax.X(k + .5), ax.Y(v) - 9, f'{v:.3f}', 11.5, 'middle', TEXT)
        s.label(ax.X(k + .5), ax.y + ax.h + 16, nm, 11.5, color=TEXT)
    ax.hline(.5, FAINT, 1, '3 3')
    s.label(ax.x - 8, ax.y - 12, 'accuracy', 11, 'start', FAINT)
    s.save('7-4-ablation', 'Mỗi nhánh riêng 0.5, ghép đúng cặp 1.0, ghép lệch cặp lại về 0.5.')


def missing74():
    s = Fig(640, 200)
    items = [('điền 0 rồi chia 2', '(0 + 0.8) / 2', .4, CLAY), ('điền 0.5 cho ảnh', '(0.5 + 0.8) / 2', .65, SAND), ('bỏ nhánh thiếu', '0.8 / 1', .8, GREEN)]
    for k, (nm, f, v, col) in enumerate(items):
        y = 30 + k * 50
        s.label(160, y + 13, nm, 12, 'end', TEXT, 600 if k == 2 else 400)
        s.box(176, y, 300 * v, 26, 'none', col, r=4, width=0, opacity=.4)
        s.mono(176 + 300 * v + 8, y + 13.5, f'{v:g}', 12, 'start', TEXT, 600)
        s.mono(176 + 8, y + 13.5, f, 10.5, 'start', TEXT)
    s.line(176 + 150, 22, 176 + 150, 180, FAINT, 1, '3 3')
    s.mono(176 + 150, 192, '0.5', 10, 'middle', FAINT)
    s.save('7-4-missing', 'Thiếu ảnh: bỏ nhánh thiếu và chuẩn hóa lại trọng số giữ được 0.8.')


def align74():
    ns = ns74()
    u = ns['unit_rows']
    vi, vt = ns['valid_images'], ns['valid_texts']
    mats = [('chưa căn chỉnh', u(vi) @ u(vt).T, '0.05'), ('học W từ cặp đúng', u(vi @ ns['projection']) @ u(vt).T, '0.95'),
            ('học W từ cặp xáo', u(vi @ ns['wrong_projection']) @ u(vt).T, '0.00')]
    s = Fig(640, 240)
    for k, (nm, M, r1) in enumerate(mats):
        ax = s.axes(40 + k * 205, 34, 160, 160, (0, 20), (0, 20), xticks=[], yticks=[], grid=False)
        heat(s, ax, M[::-1], 0, 20, 0, 20, lo=.3, hi=1, col=BLUE)
        s.box(ax.x, ax.y, 160, 160, SOFT_LINE, 'none', r=0, width=1)
        s.label(ax.x + 80, 20, nm, 12, color=TEXT, weight=600)
        s.mono(ax.x + 80, 212, f'recall@1 {r1}', 11.5, 'middle', GREEN if k == 1 else CLAY, 600)
    s.save('7-4-align', 'Chưa căn chỉnh thì không có đường chéo; W học từ cặp đúng thì có.')


def vlm74():
    s = Fig(640, 186)
    s.box(20, 40, 80, 64, 'none', BLUE, r=6, width=0, opacity=.18)
    for i in range(4):
        for j in range(4):
            s.box(26 + j * 17.5, 46 + i * 13.5, 15, 11.5, 'none', BLUE, r=1.5, width=0, opacity=.15 + .07 * ((i * 3 + j) % 4))
    s.label(60, 120, 'ảnh 336 px', 11, color=MUTED)
    s.arrow(104, 72, 132, 72, MUTED, 1.2)
    for k, nm in enumerate(['image encoder', 'projector']):
        x = 136 + k * 118
        s.box(x, 54, 100, 36, 'none', BLUE if k == 0 else SAND, r=6, width=0, opacity=.25)
        s.label(x + 50, 72, nm, 11.5, color=TEXT)
        s.arrow(x + 104, 72, x + 114, 72, MUTED, 1.2)
    for j in range(10):
        s.box(372 + j * 13, 60, 11, 24, 'none', BLUE, r=2, width=0, opacity=.35)
    s.mono(437, 100, '576 visual tokens', 10.5, 'middle', MUTED)
    q = ['có', 'mấy', 'quả', '?']
    for j, t in enumerate(q):
        s.box(372 + j * 44, 124, 40, 24, 'none', SAND, r=3, width=0, opacity=.3)
        s.mono(392 + j * 44, 136.5, t, 10.5, 'middle', TEXT)
    s.mono(437, 162, 'token câu hỏi', 10.5, 'middle', MUTED)
    s.line(512, 72, 540, 72, MUTED, 1.2)
    s.line(552, 136, 540, 136, MUTED, 1.2)
    s.line(540, 72, 540, 136, MUTED, 1.2)
    s.arrow(540, 104, 560, 104, MUTED, 1.2)
    s.box(564, 82, 62, 44, 'none', CLAY, r=6, width=0, opacity=.25)
    s.label(595, 98, 'language', 10.5, color=TEXT)
    s.label(595, 112, 'model', 10.5, color=TEXT)
    s.mono(595, 150, '{"count": 3}', 10.5, 'middle', CLAY, 600)
    s.arrow(595, 128, 595, 140, MUTED, 1.2)
    s.save('7-4-vlm', 'VLM: ảnh thành 576 visual token, nối với token câu hỏi cho language model đọc.')


def crossattn74():
    s = Fig(640, 186)
    s.label(140, 22, 'chèn visual tokens', 12, color=TEXT, weight=600)
    for j in range(24):
        s.box(20 + j * 9, 44, 7.5, 22, 'none', BLUE, r=1.5, width=0, opacity=.3)
    for j in range(4):
        s.box(20 + 24 * 9 + 6 + j * 9, 44, 7.5, 22, 'none', SAND, r=1.5, width=0, opacity=.45)
    s.mono(140, 84, '576 + 40 = 616 token', 11.5, 'middle', TEXT)
    s.mono(140, 104, 'self-attention 616 × 616', 11, 'middle', MUTED)
    s.label(485, 22, 'cross-attention chữ → ảnh', 12, color=TEXT, weight=600)
    x0, y0, W, H = 370, 56, 230, 60
    s.box(x0, y0, W, H, 'none', CLAY, r=3, width=0, opacity=.2)
    for j in range(4):
        s.box(x0 - 16, y0 + j * 15 + 1, 12, 13, 'none', SAND, r=1.5, width=0, opacity=.45)
    for j in range(24):
        s.box(x0 + j * 9.58 + .5, y0 - 16, 8.5, 12, 'none', BLUE, r=1.5, width=0, opacity=.3)
    s.mono(x0 - 22, y0 + H / 2, '40', 11, 'end', MUTED)
    s.mono(x0 + W / 2, y0 + H + 16, '576 key, value từ ảnh', 11, 'middle', MUTED)
    s.mono(x0 + W / 2, y0 + H / 2 + .5, '(40, 576)', 13, 'middle', CLAY, 600)
    s.mono(x0 + W / 2, y0 + H + 40, 'chuỗi chữ vẫn dài 40', 11, 'middle', TEXT)
    s.save('7-4-crossattn', 'Chèn visual token vào chuỗi, hoặc dùng cross-attention từ chữ sang ảnh.')


FIGS74 = {'7-4-fusion': fusion74, '7-4-join': join74, '7-4-sync': sync74, '7-4-xor': xor74, '7-4-late': late74,
          '7-4-ablation': ablation74, '7-4-missing': missing74, '7-4-align': align74, '7-4-vlm': vlm74, '7-4-crossattn': crossattn74}

# ───────────────────────────── kt4 ─────────────────────────────

_TK4 = {}


def nskt4():
    if not _TK4:
        _TK4['ns'] = kt_ns(7, 'kt4')
    return _TK4['ns']


def schedule_kt4():
    s = Fig(640, 170)
    parts = [('đọc', 20, FAINT), ('baseline A', 60, BLUE), ('baseline B', 60, SAND), ('cải tiến A', 80, BLUE),
             ('cải tiến B', 80, SAND), ('khóa', 40, CLAY), ('kiểm', 20, CLAY)]
    x0, sc, t = 30, 580 / 360, 0
    for k, (nm, m, col) in enumerate(parts):
        x = x0 + t * sc
        s.box(x + 1, 50, m * sc - 2, 34, 'none', col, r=4, width=0, opacity=.4 if k in (1, 2, 5, 6) else .18)
        if m >= 40:
            s.label(x + m * sc / 2, 67, nm, 11, color=TEXT)
        s.mono(x, 100, str(t), 10, 'middle', FAINT)
        t += m
    s.mono(x0 + 360 * sc, 100, '360', 10, 'middle', FAINT)
    s.label(x0 + 10 * sc, 34, 'đọc', 10.5, color=MUTED)
    s.label(x0 + 350 * sc, 34, 'kiểm', 10.5, color=MUTED)
    s.label(x0 + 80 * sc, 128, 'hai đường về đích trước', 11, color=MUTED)
    s.line(x0 + 20 * sc, 116, x0 + 140 * sc, 116, MUTED, 1)
    s.label(x0 + 300 * sc, 128, 'phần chốt không bị cắt', 11, color=CLAY)
    s.line(x0 + 300 * sc, 116, x0 + 360 * sc, 116, CLAY, 1)
    s.save('7-kt4-schedule', 'Lịch mẫu 360 phút: đọc hai đề, dựng hai baseline, mỗi bài một khoảng cải tiến, rồi 60 phút cuối khóa model, suy luận và kiểm file. Khi trễ, chỉ phần cải tiến co lại.')


def score_kt4():
    s = Fig(640, 250)

    def panel(x0, title, xlim, base, best, pts, xticks, lower_better):
        ax = s.axes(x0, 34, 220, 150, xlim, (0, 100), xticks=xticks, yticks=[0, 50, 100] if x0 < 200 else [], grid=False,
                    xlabel='WER' if lower_better else 'macro-F1')
        xs = np.linspace(*xlim, 200)
        ys = np.clip((xs - base) / (best - base) * 100, 0, 100)
        ax.line(xs, ys, BLUE, 2)
        s.line(ax.X(base), ax.y, ax.X(base), ax.y + ax.h, FAINT, 1, '4 4')
        for x, sc in pts:
            s.circle(ax.X(x), ax.Y(sc), 4.5, CLAY, CLAY)
            if sc > 0:
                s.mono(ax.X(x) - 10, ax.Y(sc), f'{sc:.0f}', 11, 'end', CLAY, 600)
            else:
                s.mono(ax.X(x), ax.Y(sc) - 14, '0', 11, 'middle', CLAY, 600)
        s.label(ax.x + 110, 18, title, 12, color=TEXT, weight=600)
        s.mono(ax.X(base), ax.y + ax.h + 34, f'baseline {base}', 10, 'middle', FAINT)

    panel(70, 'bài A: càng cao càng tốt', (.4, 1.0), .5, .9, [(.70, 50), (.74, 60)], [.4, .6, .8, 1.0], False)
    panel(370, 'bài B: càng thấp càng tốt', (.5, .1), .4, .15, [(.30, 40), (.45, 0)], [.5, .3, .1], True)
    s.save('7-kt4-score', 'Điểm chuẩn hóa của hai bài trong ví dụ: kém baseline của đề (vạch đứt) thì được 0. Bài A tính theo macro-F1, bài B theo WER nên trục đảo chiều; các chấm là bốn trường hợp trong code.')


def ids_kt4():
    s = Fig(640, 200)
    exp = ['img-a', 'img-b', 'img-c']
    dic = [('img-c', 1), ('img-a', 2), ('img-b', 0)]
    pred = {k: v for k, v in dic}
    ref = {'img-a': 2, 'img-b': 1, 'img-c': 1}
    s.label(130, 24, 'theo insertion order', 12, color=TEXT, weight=600)
    s.label(450, 24, 'theo manifest', 12, color=TEXT, weight=600)
    for r in range(3):
        y = 44 + r * 36
        k, v = dic[r]
        ok = ref[exp[r]] == v
        s.mono(70, y + 14, exp[r], 11, 'end', MUTED)
        s.box(80, y, 110, 28, 'none', GREEN if ok else CLAY, r=4, width=0, opacity=.3)
        s.mono(135, y + 14.5, f'{k}: {v}', 11, 'middle', TEXT)
        e = exp[r]
        ok2 = ref[e] == pred[e]
        s.mono(390, y + 14, e, 11, 'end', MUTED)
        s.box(400, y, 110, 28, 'none', GREEN if ok2 else CLAY, r=4, width=0, opacity=.3)
        s.mono(455, y + 14.5, f'{e}: {pred[e]}', 11, 'middle', TEXT)
    s.label(40, 170, 'hàng nộp', 10.5, 'start', FAINT)
    s.mono(135, 170, 'đúng 0 / 3', 11.5, 'middle', CLAY, 600)
    s.mono(455, 170, 'đúng 2 / 3', 11.5, 'middle', GREEN, 600)
    s.save('7-kt4-ids', 'Cùng dictionary dự đoán theo ID của bài: ghi theo insertion order thì mỗi hàng nộp mang dự đoán của ID khác (đúng 0/3); sắp theo manifest thì đúng 2/3 như code.')


def segments_kt4():
    s = Fig(640, 200)
    P = [[.6, .3, .1], [.2, .7, .1], [.5, .4, .1]]
    m = np.mean(P, axis=0)
    s.label(130, 22, 'ba đoạn 10 s của một ID', 12, color=TEXT, weight=600)
    for r, p in enumerate(P):
        y = 40 + r * 34
        s.mono(56, y + 13, f'đoạn {r + 1}', 10.5, 'end', MUTED)
        for c, v in enumerate(p):
            s.box(66 + c * 56, y, 52, 26, 'none', BLUE, r=3, width=0, opacity=.08 + .5 * v)
            s.mono(92 + c * 56, y + 13.5, f'{v:.1f}', 11, 'middle', TEXT)
    for c in range(3):
        s.mono(92 + c * 56, 156, f'lớp {c}', 10, 'middle', FAINT)
    s.arrow(250, 80, 300, 80, MUTED, 1.3)
    s.label(275, 66, 'trung bình', 10.5, color=MUTED)
    for c, v in enumerate(m):
        s.box(312 + c * 56, 66, 52, 28, 'none', CLAY if c == m.argmax() else BLUE, r=3, width=0, opacity=.4 if c == m.argmax() else .12)
        s.mono(338 + c * 56, 80.5, f'{v:.2f}', 11, 'middle', TEXT)
    s.arrow(484, 80, 520, 80, MUTED, 1.3)
    s.mono(530, 80.5, f'lớp {m.argmax()}', 12.5, 'start', CLAY, 600)
    s.label(420, 124, 'một hàng cho mỗi ID', 11, color=MUTED)
    s.save('7-kt4-segments', 'Một file 30 giây cắt thành ba đoạn 10 giây (xác suất đặt tay): trung bình xác suất ba đoạn theo ID rồi argmax, để file nộp có đúng một hàng cho ID ấy.')


def normalize_kt4():
    s = Fig(640, 180)
    rows = [('reference', ['em', 'học', 'ai'], [None] * 3), ('local: lower', ['em', 'học', 'ai.'], [0, 0, 1]),
            ('đề: lower, bỏ dấu câu', ['em', 'học', 'ai'], [0, 0, 0])]
    for r, (nm, toks, bad) in enumerate(rows):
        y = 26 + r * 40
        s.label(200, y + 13, nm, 11.5, 'end', TEXT if r else MUTED, 600 if r else 400)
        for j, t in enumerate(toks):
            col = FAINT if bad[j] is None else (CLAY if bad[j] else GREEN)
            s.box(214 + j * 70, y, 64, 26, 'none', col, r=4, width=0, opacity=.15 if bad[j] is None else .3)
            s.mono(246 + j * 70, y + 13.5, t, 11.5, 'middle', TEXT)
        if r:
            s.mono(440, y + 13.5, 'WER 1/3' if r == 1 else 'WER 0', 12, 'start', CLAY if r == 1 else GREEN, 600)
    s.label(320, 160, 'transcript Em học AI. sau hai cách chuẩn hóa', 11, color=MUTED)
    s.save('7-kt4-normalize', 'Transcript “Em học AI.” qua hai scorer: scorer local chỉ hạ chữ thường nên còn token “ai.” khác “ai” (WER 1/3); scorer của đề bỏ thêm dấu câu nên khớp hoàn toàn (WER 0).')


def paired_kt4():
    ns = nskt4()
    y = ns['labels']
    rows = [('ảnh', ns['image_ok']), ('chữ', ns['text_ok']), ('fusion', ns['fusion_ok'])]
    fixed = set(np.flatnonzero(~ns['image_ok'] & ns['fusion_ok']))
    broke = set(np.flatnonzero(ns['image_ok'] & ~ns['fusion_ok']))
    allbad = set(np.flatnonzero(~ns['image_ok'] & ~ns['text_ok'] & ~ns['fusion_ok']))
    s = Fig(640, 200)
    x0, w, g = 60, 17, 3
    for j in range(len(y)):
        col = GREEN if j in fixed else CLAY if j in broke else FAINT if j in allbad else None
        if col:
            s.box(x0 + j * (w + g) - 2, 28, w + 4, 3 * 26 + 4, col, 'none', r=4, width=1.4, dash=None if col != FAINT else '3 3')
        if j % 5 == 0 or col:
            s.mono(x0 + j * (w + g) + w / 2, 122, str(j), 9.5, 'middle', col or FAINT)
    for r, (nm, ok) in enumerate(rows):
        yy = 32 + r * 26
        s.label(x0 - 10, yy + 10, nm, 11.5, 'end', TEXT, 600 if r == 2 else 400)
        for j in range(len(y)):
            s.box(x0 + j * (w + g), yy, w, 20, 'none', BLUE if ok[j] else FAINT, r=3, width=0, opacity=.5 if ok[j] else .08)
        s.mono(x0 + len(y) * (w + g) + 8, yy + 10.5, f'{ok.mean():.2f}', 11, 'start', TEXT, 600 if r == 2 else 400)
    s.label(170, 152, 'fusion sửa: 3, 11, 17', 11, color=GREEN)
    s.label(340, 152, 'fusion làm sai: 8, 21', 11, color=CLAY)
    s.label(500, 152, 'cả ba sai: 5, 14', 11, color=MUTED)
    s.save('7-kt4-paired', 'Đúng/sai theo từng ID của ba cấu hình trên 25 mẫu validation (từ code bài), ô đặc là đúng: fusion sửa ba ID nhánh ảnh sai, làm sai thêm hai ID nhánh ảnh đúng; ID 5 và 14 cả ba cùng sai.')


FIGSKT4 = {'7-kt4-schedule': schedule_kt4, '7-kt4-score': score_kt4, '7-kt4-ids': ids_kt4, '7-kt4-segments': segments_kt4,
           '7-kt4-normalize': normalize_kt4, '7-kt4-paired': paired_kt4}

FIGS = {**FIGS71, **FIGS72, **FIGS73, **FIGS74, **FIGSKT4}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
