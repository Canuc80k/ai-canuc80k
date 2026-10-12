"""Lượt 8 — hình chương 4 (bản gọn). Số liệu lấy từ code bài (lesson_ns) hoặc tính lại đúng như bài.
Ảnh thật: flower.jpg (vultilion / Flickr, CC BY 2.0) và china.jpg (danielbuechele / Flickr, CC BY 2.0) kèm scikit-learn, ghi nguồn ở mục Đọc thêm của bài dùng ảnh.
Chạy riêng: python -B -X utf8 p8_ch4.py [tên ...]"""
import math, sys
import numpy as np
from kit import *
from p8_ch1 import lesson_ns
from p8_ch2 import PAPER, sup, mnum, clip, segline, regions, jit

# ───────────────────────────── 4.1 ─────────────────────────────


def flow41():
    s = Fig(640, 170)
    steps = [('x = (12, 8)', None), ('z = (1, −1)', 'processor'), ('ℓ = (2, −2, 0.25)', 'state_dict'), ('hoat_dong_A', 'labels')]
    xs = [20, 170, 330, 500]
    ws = [116, 116, 140, 120]
    for k, ((txt, part), x, w) in enumerate(zip(steps, xs, ws)):
        col = CLAY if k == 3 else BLUE
        s.box(x, 50, w, 40, 'none', col, r=8, width=0, opacity=.16)
        s.mono(x + w / 2, 70.5, txt, 12.5, 'middle', TEXT, 600 if k == 3 else 400)
        if part:
            s.arrow(xs[k - 1] + ws[k - 1] + 3, 70, x - 3, 70, LINE, 1.3)
            s.label((xs[k - 1] + ws[k - 1] + x) / 2, 30, part, 11.5, color=CLAY, weight=600)
    s.mono(228, 120, '(x − mean) / scale', 11.5, 'middle', MUTED)
    s.mono(400, 120, 'W z + b', 11.5, 'middle', MUTED)
    s.mono(560, 120, 'argmax = 0', 11.5, 'middle', MUTED)
    s.label(320, 156, 'thiếu hay lệch một phần nào, chương trình vẫn chạy mà trả lời sai', 11.5, color=MUTED)
    s.save('4-1-flow', 'Một mẫu đi qua ba phần của gói: processor đổi (12, 8) thành (1, −1), trọng số cho logits (2, −2, 0.25), bảng nhãn đổi chỉ số 0 thành tên.')


def batches41():
    s = Fig(640, 200)
    ids = [101, 102, 103, 104, 105]
    groups = [(0, 2), (2, 4), (4, 5)]
    s.label(20, 30, 'input', 12, 'start', MUTED)
    s.tiles(90, 14, [[str(i) for i in ids]], 70, 32, BLUE, 8, size=13)
    for g, (a, b) in enumerate(groups):
        x0 = 90 + a * 78
        x1 = 90 + b * 78 - 8
        s.path(f'M {x0},{56} L {x0},{62} L {x1},{62} L {x1},{56}', CLAY, 1.3)
        s.mono((x0 + x1) / 2, 78, f'batch {g + 1}', 11.5, 'middle', CLAY)
        s.arrow((x0 + x1) / 2, 86, (x0 + x1) / 2, 112, CLAY, 1.2)
    s.label(20, 132, 'kết quả', 12, 'start', MUTED)
    s.tiles(90, 116, [[str(i) for i in ids]], 70, 32, GREEN, 8, size=13)
    s.label(320, 178, 'batch 2, 2, 1 nối lại đúng thứ tự; giữ id theo từng hàng', 11.5, color=MUTED)
    s.save('4-1-batches', 'Năm mẫu chia batch 2, 2, 1: batch cuối thiếu mẫu vẫn phải chạy, và kết quả nối lại theo đúng thứ tự id ban đầu.')


def transfer41():
    s = Fig(640, 200)
    layers = ['cạnh', 'kết cấu', 'hình dạng', 'bộ phận']
    for k, nm in enumerate(layers):
        x = 30 + k * 105
        s.box(x, 60, 90, 50, 'none', BLUE, r=8, width=0, opacity=.12 + .05 * k)
        s.label(x + 45, 85, nm, 12.5, color=TEXT)
        if k:
            s.arrow(x - 13, 85, x - 2, 85, LINE, 1.2)
    s.arrow(452, 85, 470, 85, LINE, 1.2)
    s.box(472, 60, 140, 50, 'none', CLAY, r=8, width=0, opacity=.2)
    s.label(542, 78, 'head', 12.5, color=TEXT, weight=600)
    s.mono(542, 96, '1000 lớp ImageNet', 11, 'middle', MUTED)
    s.line(30, 130, 440, 130, BLUE, 1.6)
    s.label(235, 148, 'dùng lại được cho ảnh câu lạc bộ', 12, color=BLUE, weight=600)
    s.line(472, 130, 612, 130, CLAY, 1.6)
    s.label(542, 148, 'phải thay', 12, color=CLAY, weight=600)
    s.label(235, 34, 'tầng nông → tầng sâu', 11.5, color=MUTED)
    s.save('4-1-transfer', 'Các tầng của mạng ImageNet học đặc trưng chung (cạnh, kết cấu, hình dạng, bộ phận) dùng lại được; chỉ head cuối gắn với 1000 lớp cũ.')


def processor41():
    from sklearn.datasets import load_sample_image
    im = load_sample_image('flower.jpg')
    crop = im[60:380, 120:520]
    bgr = crop[..., ::-1]
    twice = (crop / 255.0)                                    # sau khi đã chia 255 một lần, processor chia thêm
    seen = np.clip(twice / 255.0 * 255.0, 0, 255)             # pixel mà processor "thấy": tất cả trong [0, 1]
    dark = np.full_like(crop, 0) + (seen).astype('uint8')
    s = Fig(640, 230)
    w, h = 190, 152
    for k, (img, title, col) in enumerate([(crop, 'RGB đúng', GREEN), (bgr, 'đọc bằng cv2 (BGR)', CLAY), (dark, 'chia 255 hai lần', CLAY)]):
        x = 20 + k * 207
        s.photo(x, 34, w, h, img, max_px=420, radius=8)
        s.label(x + w / 2, 18, title, 12.5, color=col, weight=600)
    s.mono(434 + w / 2, 34 + h / 2, 'mọi giá trị ≤ 1/255', 11.5, 'middle', '#d8d4c8')
    s.label(320, 206, 'shape, dtype đều đúng: không có lỗi nào báo ra', 11.5, color=MUTED)
    s.save('4-1-processor', 'Cùng một ảnh thật đưa vào processor RGB: đọc bằng cv2 thì đỏ và lam bị đảo; chia 255 trước khi processor chia lần nữa thì mọi pixel gần 0, mạng thấy gần như một màu.')


def memory41():
    s = Fig(640, 200)
    rows = [('trọng số 100 triệu, FP32', 381.47, BLUE), ('trọng số 100 triệu, FP16', 190.73, BLUE),
            ('input 16 × 3 × 224²', 9.19, CLAY), ('input 32 × 3 × 448²', 73.5, CLAY)]
    for r, (nm, v, col) in enumerate(rows):
        y = 26 + r * 40
        w = v / 381.47 * 330
        s.rect(220, y, max(w, 2), 26, 'none', col, 3, .7, 0)
        s.label(210, y + 13, nm, 12, 'end', TEXT)
        s.mono(220 + max(w, 2) + 8, y + 13, f'{v:g} MiB', 12, 'start', TEXT, 600)
    s.label(320, 188, 'chưa tính activation, gradient, optimizer và bộ nhớ dự trữ', 11.5, color=MUTED)
    s.save('4-1-memory', 'Bộ nhớ thô của trọng số và của tensor input: gấp đôi batch và gấp đôi cạnh ảnh làm input gấp 8, từ 9.19 lên 73.5 MiB.')


FIGS41 = {'4-1-flow': flow41, '4-1-batches': batches41, '4-1-transfer': transfer41, '4-1-processor': processor41, '4-1-memory': memory41}

# ───────────────────────────── 4.2 ─────────────────────────────

def digit(s, x, y, img, c=6, col=TEXT):
    """Ảnh chữ số 8×8 (giá trị 0..1 hoặc 0..16) vẽ bằng ô xám đậm nhạt."""
    img = np.asarray(img, float).reshape(8, 8)
    vmax = 16 if img.max() > 1.5 else 1
    for i in range(8):
        for j in range(8):
            v = img[i, j] / vmax
            if v > .04:
                s.rect(x + j * c, y + i * c, c + .2, c + .2, 'none', col, 0, min(.95, v), 0)
    s.box(x, y, 8 * c, 8 * c, SOFT_LINE, 'none', r=2, width=.8)


def reuse42():
    ns = lesson_ns('4.2', upto=1)
    X, Z = ns['X_train'], ns['Z_train']
    s = Fig(640, 230)
    digit(s, 20, 80, X[0], 8)
    s.label(52, 160, 'ảnh 8 × 8', 11.5, color=MUTED)
    s.arrow(92, 112, 132, 112, LINE, 1.3)
    s.box(136, 88, 92, 48, 'none', BLUE, r=10, width=0, opacity=.16)
    s.label(182, 106, 'encoder', 12.5, color=TEXT, weight=600)
    s.mono(182, 124, 'PCA, đứng yên', 11, 'middle', MUTED)
    s.arrow(232, 112, 262, 112, LINE, 1.3)
    z = Z[0]
    vmax = np.abs(z).max()
    for k in range(16):
        v = z[k] / vmax
        s.rect(268 + k * 9, 100, 8, 24, 'none', BLUE if v > 0 else CLAY, 1, abs(v) * .9 + .05, 0)
    s.label(340, 144, 'z: 16 số', 11.5, color=MUTED)
    uses = [('linear probe', '0.957'), ('kNN', '0.987'), ('tìm kiếm cosine', 'top-5'), ('KMeans', 'ARI 0.64')]
    for k, (nm, v) in enumerate(uses):
        y = 30 + k * 46
        s.curve(416, 112, 462, y + 14, .0, LINE, 1.1)
        s.box(466, y, 154, 28, 'none', GREEN, r=6, width=0, opacity=.14)
        s.label(474, y + 14, nm, 12, 'start', TEXT)
        s.mono(612, y + 14, v, 11, 'end', MUTED)
    s.save('4-2-reuse', 'Encoder PCA đứng yên biến mỗi ảnh 8 × 8 thành 16 số; cùng ma trận ấy dùng cho linear probe, kNN, tìm kiếm và phân cụm (số từ code bài).')


def scatter42():
    ns = lesson_ns('4.2', upto=1)
    Z, y = ns['Z_valid'], ns['y_valid']
    s = Fig(640, 280)
    lo, hi = Z[:, :2].min(0), Z[:, :2].max(0)
    ax = s.axes(150, 14, 340, 250, (lo[0] - .2, hi[0] + .2), (lo[1] - .2, hi[1] + .2), frame=False, grid=False)
    pal = ['#2f6587', '#c2603e', '#4d7337', '#b8892b', '#7a5aa6', '#3a8f8a', '#a0485e', '#6b6b6b', '#8a6d3b', '#4f79c2']
    for d in range(10):
        k = y == d
        ax.dots(Z[k, 0], Z[k, 1], pal[d], 2.2, opacity=.6)
    for d in range(10):
        m = np.median(Z[y == d, :2], 0)
        s.circle(ax.X(m[0]), ax.Y(m[1]), 10, pal[d], PAPER, 1.6)
        s.mono(ax.X(m[0]), ax.Y(m[1]) + .5, str(d), 12, 'middle', pal[d], 600)
    s.label(520, 120, 'hai tọa độ đầu', 12, 'start', MUTED)
    s.label(520, 138, 'trong 16 của z', 12, 'start', MUTED)
    s.save('4-2-scatter', '540 ảnh validation theo hai tọa độ đầu của embedding PCA (số là trung vị từng chữ số): cùng chữ số tụ lại gần nhau, dù chỉ nhìn 2 trên 16 chiều.')


def cosine42():
    s = Fig(640, 230)
    ax = s.axes(60, 20, 200, 190, (-.5, 7), (-.5, 9), frame=False, grid=False)
    s.line(ax.X(-.5), ax.Y(0), ax.X(7), ax.Y(0), SOFT_LINE, 1)
    s.line(ax.X(0), ax.Y(-.5), ax.X(0), ax.Y(9), SOFT_LINE, 1)
    s.arrow(ax.X(0), ax.Y(0), ax.X(6), ax.Y(8), CLAY, 2)
    s.arrow(ax.X(0), ax.Y(0), ax.X(3), ax.Y(4), BLUE, 2.4)
    s.mono(ax.X(3) + 8, ax.Y(4) + 6, '(3, 4)', 11.5, 'start', BLUE)
    s.mono(ax.X(6) + 8, ax.Y(8) + 4, '(6, 8)', 11.5, 'start', CLAY)
    s.label(160, 14, 'cùng hướng, khác độ dài', 12.5, color=TEXT, weight=600)
    ax2 = s.axes(330, 20, 190, 190, (-1.2, 1.2), (-1.2, 1.2), frame=False, grid=False)
    r = ax2.X(1) - ax2.X(0)
    s.circle(ax2.X(0), ax2.Y(0), r, LINE, 'none', 1)
    s.arrow(ax2.X(0), ax2.Y(0), ax2.X(.6), ax2.Y(.8), TEXT, 2)
    s.circle(ax2.X(.6), ax2.Y(.8), 5, CLAY)
    s.mono(ax2.X(.6) + 10, ax2.Y(.8) - 4, '(0.6, 0.8)', 11.5, 'start', TEXT)
    s.label(425, 14, 'sau chuẩn hóa: trùng nhau', 12.5, color=TEXT, weight=600)
    s.mono(560, 110, 'cos = 1', 13, 'start', GREEN, 600)
    s.mono(560, 132, 'Euclid = 5', 13, 'start', MUTED)
    s.save('4-2-cosine', 'Hai vector (3, 4) và (6, 8) cùng hướng: cosine bằng 1 dù Euclid bằng 5; chuẩn hóa về độ dài 1 thì cả hai thành (0.6, 0.8).')


def results42():
    ns = lesson_ns('4.2', upto=7)
    Xv, Xt = ns['X_valid'], ns['X_train']
    nearest, sim = ns['nearest'], ns['similarity']
    s = Fig(640, 170)
    digit(s, 30, 40, Xv[0], 9)
    s.label(66, 26, 'truy vấn', 12, color=CLAY, weight=600)
    s.arrow(118, 76, 150, 76, LINE, 1.3)
    for k, idx in enumerate(nearest):
        x = 166 + k * 92
        digit(s, x, 40, Xt[idx], 9)
        s.mono(x + 36, 132, f'{sim[idx]:.3f}', 11.5, 'middle', TEXT)
    s.label(400, 26, '5 ảnh train gần nhất theo cosine', 12, color=MUTED)
    s.label(400, 156, 'đều là chữ số 0', 11.5, color=GREEN)
    s.save('4-2-results', 'Ảnh validation đầu tiên (chữ số 0) và 5 ảnh train gần nhất theo cosine trên embedding 16 chiều: cả năm đều là chữ số 0, cosine từ 0.972 giảm dần.')


def scores42():
    rows = [('linear probe (embedding 16)', .9574, BLUE), ('kNN (embedding 16)', .987, GREEN), ('kNN (pixel 64)', .9889, MUTED)]
    s = Fig(640, 160)
    lo = .94
    for r, (nm, v, col) in enumerate(rows):
        y = 26 + r * 38
        w = (v - lo) / (1 - lo) * 300
        s.rect(250, y, w, 26, 'none', col, 3, .7, 0)
        s.label(240, y + 13, nm, 12, 'end', TEXT)
        s.mono(250 + w + 8, y + 13, f'{v:.4f}', 12, 'start', TEXT, 600)
    s.label(320, 146, 'trục bắt đầu từ 0.94; 0.0019 ≈ đúng một ảnh trên 540', 11.5, color=MUTED)
    s.save('4-2-scores', 'Accuracy trên cùng 540 ảnh validation: kNN trên 16 tọa độ PCA gần bằng kNN trên đủ 64 pixel (chênh một ảnh); linear probe thấp hơn.')


def clusters42():
    ns = lesson_ns('4.2', upto=9)
    y, c = ns['y_valid'], ns['valid_clusters']
    M = np.zeros((10, 10), int)
    for a, b in zip(y, c):
        M[a, b] += 1
    order = np.argsort(np.argmax(M, axis=0) + .01 * np.arange(10))
    M = M[:, order]
    s = Fig(640, 280)
    cw = 22
    x0, y0 = 220, 30
    vmax = M.max()
    for i in range(10):
        s.mono(x0 - 10, y0 + i * cw + 11, str(i), 11, 'end', MUTED)
        for j in range(10):
            v = M[i, j]
            if v:
                s.rect(x0 + j * cw, y0 + i * cw, cw - 2, cw - 2, 'none', BLUE, 2, .1 + .85 * v / vmax, 0)
    s.box(x0 - 1, y0 - 1, 10 * cw, 10 * cw, SOFT_LINE, 'none', r=2, width=.8)
    s.label(x0 - 34, y0 + 110, 'chữ số thật', 11.5, 'end', MUTED)
    s.label(x0 + 110, y0 + 10 * cw + 16, 'cụm KMeans (đã xếp lại)', 11.5, color=MUTED)
    s.label(470, 90, 'ARI 0.636', 13, 'start', TEXT, 600)
    s.label(470, 112, 'số cụm ≠ chữ số:', 11.5, 'start', MUTED)
    s.label(470, 128, 'so thẳng chỉ 0.107', 11.5, 'start', MUTED)
    s.save('4-2-clusters', 'Bảng đếm chữ số thật × cụm KMeans trên validation (cột đã xếp lại): phần lớn khối nằm trên đường chéo, nhưng vài chữ số tách đôi hoặc dồn chung một cụm.')


FIGS42 = {'4-2-reuse': reuse42, '4-2-scatter': scatter42, '4-2-cosine': cosine42, '4-2-results': results42,
          '4-2-scores': scores42, '4-2-clusters': clusters42}

# ───────────────────────────── 4.3 ─────────────────────────────

_T43 = {}


def transfer_runs():
    if not _T43:
        ns = lesson_ns('4.3', upto=4)
        for opened in (False, True):
            _, hist, ep, best, acc, cnt = ns['run_transfer'](opened)
            _T43[opened] = (np.array(hist), ep, best, acc, cnt)
    return _T43


def unfreeze43():
    s = Fig(640, 210)
    blocks = ['block 1', 'block 2', 'block 3', 'head']
    rows = [('head-only', 3), ('mở block cuối', 2), ('mở toàn bộ', 0)]
    for r, (nm, first_open) in enumerate(rows):
        y = 30 + r * 52
        s.label(140, y + 16, nm, 12.5, 'end', TEXT, 600)
        for k, b in enumerate(blocks):
            open_ = k >= first_open
            x = 160 + k * 112
            s.box(x, y, 100, 32, 'none', CLAY if open_ else BLUE, r=7, width=0, opacity=.3 if open_ else .1)
            s.label(x + 50, y + 16, b, 12, color=TEXT)
    s.box(240, 186, 14, 12, 'none', BLUE, r=3, width=0, opacity=.1)
    s.label(260, 192, 'đóng băng', 11.5, 'start', MUTED)
    s.box(340, 186, 14, 12, 'none', CLAY, r=3, width=0, opacity=.3)
    s.label(360, 192, 'được học', 11.5, 'start', MUTED)
    s.save('4-3-unfreeze', 'Ba mức mở tham số, thử theo thứ tự: chỉ head, thêm block cuối, rồi toàn bộ encoder.')


def validation43():
    T = transfer_runs()
    h, ep, best, acc, cnt = T[False]
    e = np.arange(1, len(h) + 1)
    s = Fig(640, 220)
    ax = s.axes(70, 20, 440, 160, (1, 60), (0, 1.9), xticks=[1, 20, 36, 60], yticks=[0, .5, 1, 1.5], xlabel='epoch')
    ax.line(e, h[:, 0], BLUE, 2).line(e, h[:, 1], CLAY, 2.2)
    s.line(ax.X(ep), ax.y, ax.X(ep), ax.y + ax.h, FAINT, 1, '3 3')
    s.circle(ax.X(ep), ax.Y(best), 4.5, CLAY, PAPER, 2)
    s.mono(ax.X(ep) + 6, ax.Y(best) + 16, f'{best:.4f}', 11.5, 'start', CLAY)
    s.label(ax.X(60) + 8, ax.Y(h[-1, 0]) + 6, 'train', 12, 'start', BLUE, 600)
    s.label(ax.X(60) + 8, ax.Y(h[-1, 1]) - 6, 'validation', 12, 'start', CLAY, 600)
    s.label(ax.x - 8, ax.y - 10, 'loss', 11.5, 'start', FAINT)
    s.save('4-3-validation', 'Head-only (số từ code bài): train loss giảm tới epoch 60, validation thấp nhất 0.2247 ở epoch 36 rồi nhích lên, nên checkpoint giữ epoch 36.')


def transfer43():
    T = transfer_runs()
    s = Fig(640, 220)
    ax = s.axes(70, 20, 440, 160, (1, 60), (0, 1.9), xticks=[1, 20, 40, 60], yticks=[0, .5, 1, 1.5], xlabel='epoch')
    for opened, col, nm in [(False, BLUE, 'head-only'), (True, CLAY, 'mở encoder')]:
        h, ep, best, acc, cnt = T[opened]
        e = np.arange(1, len(h) + 1)
        ax.line(e, h[:, 1], col, 2.2)
        s.circle(ax.X(ep), ax.Y(best), 4.5, col, PAPER, 2)
        s.label(ax.X(60) + 8, ax.Y(h[-1, 1]) + (8 if opened else -8), nm, 12, 'start', col, 600)
    s.label(ax.x - 8, ax.y - 10, 'validation loss', 11.5, 'start', FAINT)
    s.save('4-3-transfer', 'Validation loss của hai cách (số từ code bài, chấm tròn là checkpoint): mở encoder với learning rate nhỏ xuống 0.157 và còn đang giảm ở epoch 60; head-only dừng ở 0.2247.')


def hand43():
    s = Fig(640, 190)
    s.box(40, 60, 90, 44, 'none', BLUE, r=8, width=0, opacity=.16)
    s.mono(85, 82.5, 'w = 2', 13, 'middle', TEXT)
    s.label(85, 46, 'encoder', 11.5, color=MUTED)
    s.box(250, 60, 90, 44, 'none', CLAY, r=8, width=0, opacity=.2)
    s.mono(295, 82.5, 'a = 1', 13, 'middle', TEXT)
    s.label(295, 46, 'head', 11.5, color=MUTED)
    s.arrow(134, 82, 246, 82, LINE, 1.3)
    s.mono(190, 72, 'wx = 2', 11, 'middle', MUTED)
    s.arrow(344, 82, 420, 82, LINE, 1.3)
    s.mono(470, 82.5, 'ŷ = 2, y = 3', 12.5, 'middle', TEXT)
    s.arrow(420, 132, 344, 132, CLAY, 1.5)
    s.mono(382, 148, 'r = −1', 11.5, 'middle', CLAY)
    s.arrow(246, 132, 134, 132, CLAY, 1.5)
    s.mono(190, 148, '× a', 11.5, 'middle', CLAY)
    s.mono(40, 172, '∂L/∂w = −2, η 0.01 → w = 2.02', 11.5, 'start', BLUE)
    s.mono(330, 172, '∂L/∂a = −4, η 0.1 → a = 1.4', 11.5, 'start', CLAY)
    s.save('4-3-hand', 'Ví dụ tính tay ŷ = a(wx): gradient về encoder phải nhân qua a của head; với learning rate 0.1 cho head và 0.01 cho encoder, a lên 1.4 còn w chỉ nhích tới 2.02.')


def params43():
    T = transfer_runs()
    s = Fig(640, 170)
    rows = [('head-only', T[False][4], T[False][3], BLUE), ('mở encoder', T[True][4], T[True][3], CLAY)]
    for r, (nm, cnt, acc, col) in enumerate(rows):
        y = 30 + r * 50
        w = cnt / 2146 * 240
        s.rect(170, y, max(w, 3), 30, 'none', col, 4, .7, 0)
        s.label(160, y + 15, nm, 12.5, 'end', TEXT)
        s.mono(170 + max(w, 3) + 8, y + 15, f'{cnt} tham số · val acc {acc:.3f}', 12, 'start', TEXT)
    s.label(320, 150, 'đúng thêm 11 trên 306 ảnh validation; mỗi tham số mở kèm gradient và hai moment Adam', 11.5, color=MUTED)
    s.save('4-3-params', 'Số tham số được học và accuracy validation ở checkpoint (số từ code bài): mở encoder tăng từ 66 lên 2146 tham số, accuracy từ 0.902 lên 0.938.')


def bn43():
    s = Fig(640, 190)
    s.label(40, 30, 'batch', 12, 'start', MUTED)
    s.tiles(40, 42, [['2', '4'], ['4', '8']], 44, 30, BLUE, 4, size=13)
    s.mono(86, 120, 'mean (3, 6)', 11.5, 'middle', MUTED)
    s.arrow(140, 72, 200, 72, LINE, 1.3)
    s.label(260, 30, 'running_mean', 12, 'middle', MUTED)
    s.tiles(214, 42, [['0', '0']], 44, 30, FAINT, 4, size=13)
    s.mono(260, 92, 'trước', 11, 'middle', MUTED)
    s.arrow(312, 57, 372, 57, CLAY, 1.4)
    s.mono(342, 44, 'train()', 11, 'middle', CLAY)
    s.tiles(380, 42, [['1.5', '3']], 50, 30, CLAY, 4, size=13, opacity=.25)
    s.mono(430, 92, 'sau 0.5·(3, 6)', 11, 'middle', MUTED)
    s.arrow(486, 57, 530, 57, GREEN, 1.4)
    s.mono(508, 44, 'eval()', 11, 'middle', GREEN)
    s.mono(538, 57.5, 'giữ nguyên', 12, 'start', GREEN)
    s.label(320, 160, 'mọi tham số đã requires_grad=False, đang trong no_grad(), mà buffer vẫn đổi', 11.5, color=MUTED)
    s.save('4-3-bn', 'BatchNorm đã đóng băng hết tham số vẫn cập nhật running_mean khi chạy ở train(): từ (0, 0) thành (1.5, 3); chỉ eval() giữ buffer đứng yên.')


FIGS43 = {'4-3-unfreeze': unfreeze43, '4-3-validation': validation43, '4-3-transfer': transfer43, '4-3-hand': hand43,
          '4-3-params': params43, '4-3-bn': bn43}

# ───────────────────────────── 4.4 ─────────────────────────────

_T44 = {}


def lora44(key):
    """Số liệu 4.4 chạy lại từ code bài (float64 như bài; trả lại float32 mặc định sau khi chạy)."""
    if not _T44:
        import torch
        from torch import nn
        n3 = lesson_ns('4.4', upto=3)
        _T44['g0'] = (n3['adapter'].A.grad.numpy().copy(), n3['adapter'].B.grad.numpy().copy())
        n4 = lesson_ns('4.4', upto=4)
        _T44['g1'] = (n4['adapter'].A.grad.numpy().copy(), n4['adapter'].B.grad.numpy().copy())
        W0, Xt, yt, Xv, yv, TL = (n4[k] for k in ['W0', 'X_train', 'y_train', 'X_valid', 'y_valid', 'TinyLoRA'])

        def run(kind, rank=2, steps=250):  # đúng train_small của bài, thêm ghi validation MSE mỗi bước
            torch.manual_seed(20)
            if kind == 'full':
                c = nn.Linear(8, 6, bias=False)
                with torch.no_grad():
                    c.weight.copy_(W0)
            else:
                c = TL(W0, rank=rank, alpha=2 * rank)
            opt = torch.optim.Adam([q for q in c.parameters() if q.requires_grad], lr=0.03)
            hist = []
            for k in range(steps + 1):
                with torch.no_grad():
                    hist.append(((c(Xv) - yv) ** 2).mean().item())
                if k == steps:
                    break
                opt.zero_grad(set_to_none=True)
                ((c(Xt) - yt) ** 2).mean().backward()
                opt.step()
            return np.array(hist)
        _T44['curves'] = {'full': run('full'), 'rank 1': run('lora', 1), 'rank 2': run('lora', 2)}
        _T44['sv'] = np.linalg.svd((n4['true_B'] @ n4['true_A']).numpy(), compute_uv=False)
        torch.set_default_dtype(torch.float32)
    return _T44[key]


def path44():
    s = Fig(640, 200)
    c, g = 16, 2
    s.tiles(120, 50, [[''] * 8] * 6, c, c, BLUE, g, opacity=.14, r=2)
    s.mono(190, 34, 'W₀ · 6×8', 13, 'middle', TEXT)
    s.label(285, 104, '+', 18, color=MUTED)
    s.mono(318, 104, 'α/r', 13, 'middle', MUTED)
    s.tiles(345, 50, [[''] * 2] * 6, c, c, CLAY, g, opacity=.32, r=2)
    s.mono(362, 34, 'B · 6×2', 13, 'middle', TEXT)
    s.tiles(391, 86, [[''] * 8] * 2, c, c, CLAY, g, opacity=.32, r=2)
    s.mono(462, 70, 'A · 2×8', 13, 'middle', TEXT)
    s.label(190, 180, 'cố định · 48 số', 12, color=BLUE)
    s.label(439, 180, 'được học · 12 + 16 = 28 số', 12, color=CLAY)
    s.save('4-4-path', 'LoRA giữ W₀ cố định và học phần sửa (α/r)·BA từ hai ma trận mỏng: với lớp 6×8 và r = 2, B có 12 số, A có 16 số.')


def rank44():
    s = Fig(640, 240)
    th = math.radians(18)
    u, n = (math.cos(th), -math.sin(th)), (-math.sin(th), -math.cos(th))
    O, L = (150, 135), 46
    P = lambda a, b: (O[0] + L * (a * u[0] + b * n[0]), O[1] + L * (a * u[1] + b * n[1]))
    s.line(*P(-2.4, 0), *P(2.8, 0), SOFT_LINE, 1)
    s.arrow(*O, *P(1, 0), BLUE, 2)
    s.label(P(1, 0)[0] + 2, P(1, 0)[1] + 18, 'a', 13, color=BLUE, weight=600)
    for a, b, v, side in [(1.8, 1.0, '1.8', 1), (0, 1.5, '0', -1), (-1.4, -1.0, '−1.4', 1)]:
        x, y = P(a, b)
        s.line(x, y, *P(a, 0), FAINT, 1, '3 3')
        s.circle(x, y, 4.5, TEXT, PAPER, 1.6)
        i = '₁₂₃'[['1.8', '0', '−1.4'].index(v)]
        s.mono(x + 9 * side, y - 7, f'aᵀx{i} = {v}', 11.5, 'start' if side > 0 else 'end', GREEN if v == '0' else TEXT)
    s.label(150, 226, 'input: chỉ nhìn một hướng a', 12, color=MUTED)
    bv = (math.cos(math.radians(62)), -math.sin(math.radians(62)))
    s.arrow(352, 200, 352 + 34 * bv[0], 200 + 34 * bv[1], CLAY, 2)
    s.label(352 + 34 * bv[0] + 8, 200 + 34 * bv[1] + 4, 'b', 13, 'start', CLAY, 600)
    for (x, y), v, i in [((420, 100), 1.8, '₁'), ((470, 160), 0, '₂'), ((560, 96), -1.4, '₃')]:
        s.circle(x, y, 4.5, TEXT, PAPER, 1.6)
        if v:
            d, k = math.copysign(5, v), 26 * v
            s.arrow(x + d * bv[0], y + d * bv[1], x + k * bv[0], y + k * bv[1], CLAY, 1.6)
            s.mono(x - 9, y + 4, f'W₀x{i}', 11.5, 'end', TEXT)
        else:
            s.mono(x + 10, y + 4, f'W₀x{i} không đổi', 11.5, 'start', GREEN)
    s.label(480, 226, 'output: chỉ sửa dọc hướng b', 12, color=MUTED)
    s.save('4-4-rank1', 'LoRA rank 1: adapter đo aᵀx rồi đẩy output dọc đúng một hướng b, tỉ lệ với con số ấy; input vuông góc với a đi qua như model gốc.')


def count44():
    s = Fig(640, 220)
    ax = s.axes(70, 20, 420, 160, (0.6, 5.4), (0, 80), xticks=[1, 2, 3, 4, 5], yticks=[0, 20, 40, 60, 80], xlabel='rank r')
    ax.hline(48, BLUE, 1.6, None)
    r = np.arange(1, 6)
    ax.line([0.6, 5.4], [14 * 0.6, 14 * 5.4], CLAY, 2)
    ax.dots(r, 14 * r, CLAY, 4, CLAY)
    s.label(ax.X(5.4) + 8, ax.Y(48), 'full 48', 12, 'start', BLUE, 600)
    s.label(ax.X(5.4) + 8, ax.Y(14 * 5.4), 'LoRA 14r', 12, 'start', CLAY, 600)
    for k in r:
        s.mono(ax.X(k) + (8 if k < 4 else -8), ax.Y(14 * k) + (10 if k < 4 else -15), str(14 * k), 11, 'start' if k < 4 else 'end', CLAY)
    s.label(ax.x - 8, ax.y - 10, 'tham số học', 11.5, 'start', FAINT)
    s.save('4-4-count', 'Lớp 6×8: LoRA học 14r tham số, vượt 48 của full update từ r = 4.')


def grad44():
    s = Fig(640, 210)
    (a0, b0), (a1, b1) = lora44('g0'), lora44('g1')
    ma, mb = np.abs(a1).max(), max(np.abs(b0).max(), np.abs(b1).max())
    c, g = 20, 3

    def heat(x, y, m, mx):
        vals = [[('0' if v == 0 else None) for v in row] for row in m]
        fills = {(i, j): ((CLAY if v > 0 else BLUE), .08 + .62 * abs(v) / mx) if v else (FAINT, .1)
                 for i, row in enumerate(m) for j, v in enumerate(row)}
        s.tiles(x, y, vals, c, c, FAINT, g, fills, size=10, text_color=FAINT, r=3)

    for k, (A, B, title, note) in enumerate([(a0, b0, 'bước đầu: B = 0', 'đúng bằng 0'), (a1, b1, 'sau một bước', 'cỡ 10⁻⁴')]):
        x0 = 40 + k * 300
        s.label(x0 + 125, 22, title, 12.5, color=TEXT, weight=600)
        s.mono(x0, 52, '∂L/∂A', 11.5, 'start', MUTED)
        heat(x0, 60, A, ma)
        s.label(x0 + 91, 124, note, 11.5, color=GREEN if k == 0 else MUTED)
        s.mono(x0 + 200, 52, '∂L/∂B', 11.5, 'start', MUTED)
        heat(x0 + 200, 60, B, mb)
        s.label(x0 + 222, 206, 'cỡ 10⁻²', 11.5, color=MUTED)
    s.save('4-4-grad', 'Gradient ở bước đầu (số từ code bài): ∂L/∂A chứa B = 0 nên bằng 0, ∂L/∂B thì không; sau một bước, A bắt đầu nhận gradient. Màu theo dấu, đậm theo độ lớn trong từng ma trận.')


def curves44():
    C = lora44('curves')
    s = Fig(640, 240)
    ax = s.axes(70, 20, 430, 180, (0, 250), (-14.5, -1.5), xticks=[0, 50, 100, 150, 200, 250],
                yticks=[-14, -10, -6, -2], yfmt='', xlabel='bước Adam')
    for e in [-14, -10, -6, -2]:
        s.label(ax.x - 8, ax.Y(e), f'10{sup(e)}', 11, 'end', FAINT)
    st = np.arange(251)
    for nm, col in [('full', BLUE), ('rank 2', GREEN), ('rank 1', CLAY)]:
        h = np.log10(C[nm])
        ax.line(st, h, col, 2)
        s.label(ax.X(250) + 8, ax.Y(h[-1]), nm, 12, 'start', col, 600)
    s.mono(ax.X(250) + 8, ax.Y(np.log10(C['rank 1'][-1])) + 16, '0.00204', 11, 'start', CLAY)
    s.label(ax.x - 8, ax.y - 10, 'validation MSE', 11.5, 'start', FAINT)
    s.save('4-4-curves', 'Validation MSE theo bước (số từ code bài, trục log): full về 3·10⁻¹⁴; rank 2 có lúc xuống dưới 10⁻⁹ nhưng dao động, dừng ở 5·10⁻⁶; rank 1 nằm ở sàn 0.00204 từ khoảng bước 40.')


def spectrum44():
    sv = lora44('sv')
    s = Fig(640, 200)
    ax = s.axes(80, 24, 300, 130, (0.4, 6.6), (0, 0.18), xticks=[], yticks=[0, .05, .1, .15])
    for k, v in enumerate(sv, 1):
        x = ax.X(k)
        h = max(ax.Y(0) - ax.Y(v), 1.5)
        if k == 1:
            s.rect(x - 16, ax.Y(0) - h, 32, h, 'none', CLAY, 3, .75, 0)
        else:
            s.rect(x - 16, ax.Y(0) - h, 32, h, CLAY, 'none', 3, 1, 1.4)
        s.label(x, ax.Y(0) + 16, f'σ{"₁₂₃₄₅₆"[k - 1]}', 12, color=MUTED)
        if k <= 2:
            s.mono(x, ax.Y(v) - 8, f'{v:.4g}', 11.5, 'middle', TEXT)
    s.label(420, 70, 'rank 1 giữ σ₁, bỏ σ₂', 12.5, 'start', TEXT, 600)
    s.mono(420, 98, 'σ₂² / 6 = 0.108² / 6', 12, 'start', MUTED)
    s.mono(420, 120, '≈ 0.0019', 12, 'start', CLAY)
    s.save('4-4-spectrum', 'Giá trị kỳ dị của phần sửa thật (số từ code bài): chỉ hai giá trị khác 0. Rank 1 giữ σ₁, phần σ₂ bị bỏ góp khoảng 0.108²/6 ≈ 0.0019 vào MSE.')


def adapters44():
    s = Fig(640, 200)
    s.box(40, 64, 120, 70, 'none', BLUE, r=10, width=0, opacity=.16)
    s.label(100, 94, 'base W₀', 13, color=TEXT, weight=600)
    s.label(100, 114, 'giữ nguyên', 11.5, color=MUTED)
    for nm, task, y in [('X', 'chủ đề', 26), ('Y', 'độ khó', 116)]:
        s.curve(164, 99, 236, y + 28, 0, LINE, 1.3)
        s.box(240, y, 170, 56, 'none', CLAY, r=8, width=0, opacity=.22)
        s.label(325, y + 23, f'adapter {nm}', 12.5, color=TEXT, weight=600)
        s.label(325, y + 41, f'A, B và head {nm}', 11.5, color=MUTED)
        s.arrow(414, y + 28, 470, y + 28, LINE, 1.3)
        s.label(478, y + 28, task, 12.5, 'start', TEXT)
    s.save('4-4-adapters', 'Một base, mỗi nhiệm vụ một adapter kèm head riêng: đổi adapter là đổi nhiệm vụ, không merge hai adapter vào cùng một W₀.')


def distil44():
    s = Fig(640, 210)
    total, adapter, head = 67_028_738, 73_728, 592_130
    W, x0 = 520, 60
    tw = W * (adapter + head) / total
    s.rect(x0, 40, W - tw, 30, 'none', BLUE, 4, .16, 0)
    s.rect(x0 + W - tw, 40, tw, 30, 'none', CLAY, 1, .9, 0)
    s.label(x0 + (W - tw) / 2, 55, 'đóng băng · 66 362 880', 12, color=TEXT)
    s.mono(x0 + W + 8, 55, '0.99%', 11.5, 'start', CLAY)
    s.label(x0, 26, 'DistilBERT + LoRA rank 4 · 67 028 738 tham số', 12, 'start', MUTED)
    aw = W * adapter / (adapter + head)
    y = 130
    s.line(x0 + W - tw, 72, x0, y - 2, FAINT, 1, '3 3')
    s.line(x0 + W, 72, x0 + W, y - 2, FAINT, 1, '3 3')
    s.rect(x0, y, aw, 30, 'none', CLAY, 4, .85, 0)
    s.rect(x0 + aw + 2, y, W - aw - 2, 30, 'none', CLAY, 4, .3, 0)
    s.label(x0 + aw / 2, y + 48, 'adapter A, B', 11.5, color=CLAY)
    s.label(x0 + aw / 2, y + 64, '73 728', 11.5, color=CLAY)
    s.label(x0 + aw + (W - aw) / 2, y + 15, 'head mới · 592 130', 12, color=TEXT)
    s.save('4-4-distil', 'Phần được học khi chèn LoRA rank 4 vào q_lin, v_lin của DistilBERT (số từ output bài): khoảng 1% tổng tham số, trong đó head mới gấp tám lần adapter.')


FIGS44 = {'4-4-path': path44, '4-4-rank1': rank44, '4-4-count': count44, '4-4-grad': grad44, '4-4-curves': curves44,
          '4-4-spectrum': spectrum44, '4-4-adapters': adapters44, '4-4-distil': distil44}

# ───────────────────────────── 4.5 ─────────────────────────────


def contrastive45():
    from sklearn.datasets import load_sample_image, load_digits
    china = load_sample_image('china.jpg')[20:380, 40:400]
    flower = load_sample_image('flower.jpg')[40:400, 140:500]
    three = load_digits().images[3]
    caps = ['a photo of a pagoda', 'a photo of a flower', 'a handwritten 3']
    s = Fig(640, 300)
    x0, y0, cw, ch, g = 150, 46, 150, 64, 8
    for j, c in enumerate(caps):
        s.mono(x0 + j * (cw + g) + cw / 2, y0 - 14, c, 11.5, 'middle', TEXT)
    for i in range(3):
        y = y0 + i * (ch + g)
        if i < 2:
            s.photo(66, y, ch, ch, [china, flower][i], max_px=200, radius=6)
        else:
            s.box(66, y, ch, ch, 'none', PAPER, r=6, width=0)
            digit(s, 66, y, three, 8)
        for j in range(3):
            x = x0 + j * (cw + g)
            if i == j:
                s.box(x, y, cw, ch, 'none', CLAY, r=8, width=0, opacity=.32)
                s.label(x + cw / 2, y + ch / 2, 'kéo lên', 12, color=TEXT, weight=600)
            else:
                s.box(x, y, cw, ch, 'none', BLUE, r=8, width=0, opacity=.08)
                s.label(x + cw / 2, y + ch / 2, 'đẩy xuống', 11.5, color=FAINT)
    s.label(x0 + 1.5 * cw + g, 280, 'mỗi hàng: ảnh chọn đúng caption · mỗi cột: caption chọn đúng ảnh', 11.5, color=MUTED)
    s.save('4-5-contrastive', 'Một batch ba cặp ảnh–caption: pretraining kéo điểm của cặp đúng trên đường chéo lên và đẩy mọi ô khác xuống, theo cả hàng lẫn cột.')


def shots45():
    s = Fig(640, 210)
    cols = [('zero-shot', 'x → ?', BLUE, 'trọng số giữ nguyên', 'không dùng ví dụ có nhãn'),
            ('few-shot', 'x₁→y₁  x₂→y₂  x→?', BLUE, 'trọng số giữ nguyên', 'ví dụ nằm trong prompt'),
            ('fine-tuning', 'x → ?', CLAY, 'trọng số đã cập nhật', 'ví dụ dùng để học trọng số')]
    for k, (title, prompt, col, wlab, note) in enumerate(cols):
        x = 20 + k * 210
        s.label(x + 95, 22, title, 13, color=TEXT, weight=600)
        s.box(x, 40, 190, 36, 'none', FAINT, r=7, width=0, opacity=.12)
        s.mono(x + 95, 58.5, prompt, 12, 'middle', TEXT)
        s.arrow(x + 95, 80, x + 95, 104, LINE, 1.2)
        s.box(x, 108, 190, 40, 'none', col, r=7, width=0, opacity=.16 if col == BLUE else .3)
        s.label(x + 95, 128, wlab, 12, color=TEXT)
        s.label(x + 95, 174, note, 11.5, color=MUTED if k == 0 else (BLUE if k == 1 else CLAY))
    s.save('4-5-shots', 'Ba cách dùng ví dụ có nhãn của nhiệm vụ mới: zero-shot không dùng, few-shot đặt vài ví dụ vào prompt, fine-tuning dùng chúng để cập nhật trọng số.')


def angles45():
    ns = lesson_ns('4.5', upto=1)
    cos, lg, pr = ns['scores'][0], ns['logits'][0], ns['probabilities'][0]
    s = Fig(640, 240)
    O, R = (170, 128), 88
    s.circle(*O, R, SOFT_LINE, 'none', 1)
    names = ['bàn', 'bảng', 'máy tính']
    for (vx, vy), nm in zip(ns['texts'], names):
        s.arrow(*O, O[0] + R * vx, O[1] - R * vy, BLUE, 1.8)
    s.label(O[0] + R + 10, O[1] + 1, 'bàn', 12.5, 'start', BLUE, 600)
    s.label(O[0], O[1] - R - 12, 'bảng', 12.5, color=BLUE, weight=600)
    s.label(O[0] - R - 10, O[1] + 1, 'máy tính', 12.5, 'end', BLUE, 600)
    ux, uy = ns['images'][0]
    s.arrow(*O, O[0] + R * ux, O[1] - R * uy, CLAY, 2.2)
    s.label(O[0] + R * ux + 8, O[1] - R * uy - 8, 'ảnh 1', 12.5, 'start', CLAY, 600)
    hx = [372, 452, 512, 584]
    for x, h in zip(hx, ['', 'cosine', '× 5', 'softmax']):
        s.label(x, 52, h, 11.5, 'end' if x == hx[0] else 'middle', MUTED)
    for r, nm in enumerate(names):
        y = 84 + r * 34
        s.label(hx[0], y, nm, 12.5, 'end', TEXT)
        s.mono(hx[1], y, mnum(cos[r], '{:.1f}'), 12.5, 'middle', TEXT)
        s.mono(hx[2], y, mnum(lg[r], '{:g}'), 12.5, 'middle', TEXT)
        s.mono(hx[3], y, f'{pr[r]:.4f}', 12.5, 'middle', CLAY if r == 0 else TEXT, 600 if r == 0 else 400)
    s.save('4-5-angles', 'Ảnh 1 (0.8, 0.6) so với ba vector lớp dài 1 (số từ code bài): cosine 0.8, 0.6, −0.8; nhân scale 5 rồi softmax cho “bàn” 0.7309.')


def matrix45():
    ns = lesson_ns('4.5', upto=2)
    sm, L = ns['softmax'], ns['logits']
    P_row, P_col = sm(L), sm(L.T).T
    s = Fig(640, 236)
    names = ['bàn', 'bảng', 'máy tính']
    for k, (P, title, loss) in enumerate([(P_row, 'softmax theo hàng: ảnh tìm chữ', ns['image_to_text']),
                                         (P_col, 'softmax theo cột: chữ tìm ảnh', ns['text_to_image'])]):
        x0 = 86 + k * 300
        s.label(x0 + 104, 20, title, 12.5, color=TEXT, weight=600)
        for j, nm in enumerate(names):
            s.label(x0 + j * 70 + 32, 44, nm, 11.5, color=MUTED)
        vals = [[f'{v:.3f}' for v in row] for row in P]
        fills = {(i, j): (CLAY if i == j else BLUE, .06 + .4 * P[i, j]) for i in range(3) for j in range(3)}
        s.tiles(x0, 56, vals, 64, 34, BLUE, 6, fills, size=12)
        if k == 0:
            for i in range(3):
                s.label(x0 - 10, 56 + i * 40 + 17, f'ảnh {i + 1}', 11.5, 'end', MUTED)
        s.mono(x0 + 101, 196, f'loss {loss:.4f}', 12, 'middle', CLAY)
    s.label(320, 224, 'loss = trung bình −log của ba ô đường chéo', 11.5, color=MUTED)
    s.save('4-5-matrix', 'Cùng ma trận logits, softmax theo hàng và theo cột cho hai phân phối khác nhau (số từ code bài): loss ảnh tìm chữ 0.2114, chữ tìm ảnh 0.2135.')


def candidates45():
    ns = lesson_ns('4.5', upto=3)
    before, after = ns['probabilities'][0], ns['new_probabilities'][0]
    s = Fig(640, 200)
    W, x0 = 470, 120
    cols = [BLUE, SAND, GREEN, CLAY]
    names = ['bàn', 'bảng', 'máy tính', 'lớp mới']
    for r, (P, lab) in enumerate([(before, '3 lớp'), (after, 'thêm lớp 4')]):
        y = 30 + r * 76
        s.label(x0 - 12, y + 17, lab, 12.5, 'end', TEXT, 600)
        x = x0
        for k, p in enumerate(P):
            w = W * p
            if w > .5:
                s.rect(x, y, max(w - 2, .5), 34, 'none', cols[k], 3, .28 if k < 3 else .45, 0)
            if p > .15:
                s.label(x + w / 2, y + 17, f'{names[k]} {p:.3f}', 12, color=TEXT)
            elif p > .05:
                s.label(x + w / 2, y - 9, f'{names[k]} {p:.3f}', 11.5, color=MUTED)
            x += w
    s.label(x0 + W / 2, 180, 'ảnh và ba vector cũ không đổi; chỉ mẫu số có thêm một ứng viên', 11.5, color=MUTED)
    s.save('4-5-candidates', 'Softmax của ảnh 1 trước và sau khi thêm một lớp trùng hướng ảnh (số từ code bài): “bàn” từ 0.731 xuống 0.245, lớp mới thắng với 0.665.')


def ranking45():
    ns = lesson_ns('4.5', upto=4)
    cond = ns['conditional']
    s = Fig(640, 250)
    ax = s.axes(80, 26, 360, 180, (0, 3.2), (-1.2, 0.05), xticks=[0, 1, 2, 3], yticks=[-1, -.5, 0],
                yfmt='{:g}', xlabel='số token ứng viên')
    res = {}
    for nm, col in [('A', BLUE), ('B', CLAY)]:
        lp = np.r_[0, np.cumsum(np.log(cond[nm]))]
        xs = np.arange(len(lp))
        ax.line(xs, lp, col, 2.2)
        ax.dots(xs, lp, col, 4, col)
        m = len(lp) - 1
        s.line(ax.X(0), ax.Y(0), ax.X(m), ax.Y(lp[-1]), col, 1.2, '4 4')
        s.label(ax.X(m) + 9, ax.Y(lp[-1]) + 14, nm, 13, 'start', col, 600)
        res[nm] = (lp[-1], lp[-1] / m)
    s.label(ax.x - 8, ax.y - 12, 'log p tích lũy', 11.5, 'start', FAINT)
    cx = [478, 540, 606]
    s.label(cx[1], 56, 'tổng', 12, color=MUTED)
    s.label(cx[2], 56, 'mean', 12, color=MUTED)
    for r, (nm, col) in enumerate([('A', BLUE), ('B', CLAY)]):
        y = 82 + r * 24
        s.label(cx[0], y, nm, 12.5, color=col, weight=600)
        s.mono(cx[1], y, mnum(res[nm][0], '{:.3f}'), 12, 'middle', col, 600 if nm == 'A' else 400)
        s.mono(cx[2], y, mnum(res[nm][1], '{:.3f}'), 12, 'middle', col, 600 if nm == 'B' else 400)
    s.label(cx[0], 140, 'chọn', 12, color=MUTED)
    s.label(cx[1], 140, 'A', 12.5, color=BLUE, weight=600)
    s.label(cx[2], 140, 'B', 12.5, color=CLAY, weight=600)
    s.label(cx[1], 172, 'điểm cuối', 11.5, color=MUTED)
    s.label(cx[2], 172, 'độ dốc', 11.5, color=MUTED)
    s.save('4-5-ranking', 'Log-probability tích lũy qua từng token của hai ứng viên (số từ code bài): tổng log là điểm cuối nên chọn A; mean log là độ dốc từ gốc nên chọn B.')


def tokens45():
    s = Fig(640, 170)
    rows = [('model X', ['quy', ' hoạch', ' động'], '−6 / 3', 'e² ≈ 7.39'),
            ('model Y', ['qu', 'y', ' ho', 'ạch', ' độ', 'ng'], '−6 / 6', 'e ≈ 2.72')]
    W, x0 = 260, 100
    for r, (nm, toks, frac, ppl) in enumerate(rows):
        y = 34 + r * 60
        s.label(x0 - 12, y + 16, nm, 12.5, 'end', TEXT, 600)
        w = W / len(toks)
        for k, t in enumerate(toks):
            s.box(x0 + k * w + 1, y, w - 4, 32, 'none', BLUE if r == 0 else CLAY, r=6, width=0, opacity=.16 if r == 0 else .22)
            s.mono(x0 + k * w + w / 2 - 1, y + 16.5, t.strip(), 12, 'middle', TEXT)
        s.mono(x0 + W + 16, y + 16.5, f'mean log {frac}', 12, 'start', MUTED)
        s.mono(x0 + W + 150, y + 16.5, f'PPL {ppl}', 12, 'start', TEXT, 600)
    s.label(320, 156, 'cùng một câu, cùng tổng log −6: chỉ mẫu số khác nhau', 11.5, color=MUTED)
    s.save('4-5-tokens', 'Cùng một câu và cùng tổng log-probability −6, tokenizer tách 3 hay 6 token cho PPL 7.39 hay 2.72: PPL chỉ so được trong cùng một tokenizer.')


def shift45():
    s = Fig(640, 200)
    toks = ['The', ' algorithm', ' uses', ' dynamic', ' programming']
    xs = [70, 170, 280, 395, 530]
    for k, (t, x) in enumerate(zip(toks, xs)):
        cand = k >= 3
        w = 34 + 8.2 * len(t.strip())
        s.box(x - w / 2, 70, w, 34, 'none', CLAY if cand else FAINT, r=7, width=0, opacity=.28 if cand else .12)
        s.mono(x, 87.5, t.strip(), 12.5, 'middle', TEXT)
        s.mono(x, 132, f'ℓ{k}', 11.5, 'middle', MUTED)
        if k < len(toks) - 1:
            scored = k >= 2
            s.curve(x + 6, 122, xs[k + 1] - 6, 108, -.35, CLAY if scored else FAINT, 1.6 if scored else 1.1,
                    dash=None if scored else '3 3')
    s.label(175, 46, 'prompt: không chấm', 12, color=MUTED)
    s.label(462, 46, 'ứng viên: chỉ chấm hai token này', 12, color=CLAY)
    s.label(320, 176, 'logits ở vị trí j dự đoán token j + 1, nên nhãn dịch đi một vị trí', 11.5, color=MUTED)
    s.save('4-5-shift', 'Chấm một ứng viên bằng causal language model: logits ở vị trí j dự đoán token j + 1; chỉ cộng log-prob của các token thuộc ứng viên.')


FIGS45 = {'4-5-contrastive': contrastive45, '4-5-shots': shots45, '4-5-angles': angles45, '4-5-matrix': matrix45,
          '4-5-candidates': candidates45, '4-5-ranking': ranking45, '4-5-tokens': tokens45, '4-5-shift': shift45}

# ───────────────────────────── kt2 ─────────────────────────────


def splitkt2():
    rng = np.random.default_rng(3)
    s = Fig(640, 230)
    nr, nc, c, g = 8, 10, 14, 4
    for k, (title, note) in enumerate([('chia ngẫu nhiên theo ảnh', 'ảnh validation có “anh em” cùng buổi trong train'),
                                       ('chia theo buổi', 'validation gồm buổi mới, như test')]):
        x0 = 60 + k * 300
        s.label(x0 + 90, 20, title, 12.5, color=TEXT, weight=600)
        val = rng.random((nr, nc)) < .2 if k == 0 else np.isin(np.arange(nr), [2, 6])[:, None].repeat(nc, 1)
        fills = {(i, j): (CLAY, .7) if val[i, j] else (BLUE, .16) for i in range(nr) for j in range(nc)}
        s.tiles(x0, 38, [[''] * nc] * nr, c, c, BLUE, g, fills, r=3)
        if k == 0:
            for i in range(nr):
                s.label(x0 - 8, 38 + i * (c + g) + c / 2, f'buổi {i + 1}', 10.5, 'end', FAINT)
        s.label(x0 + 90, 200, note, 11.5, color=MUTED)
    s.box(250, 214, 12, 10, 'none', CLAY, r=2, width=0, opacity=.7)
    s.label(268, 219, 'validation', 11, 'start', MUTED)
    s.box(340, 214, 12, 10, 'none', BLUE, r=2, width=0, opacity=.16)
    s.label(358, 219, 'train', 11, 'start', MUTED)
    s.save('4-kt2-split', 'Hai cách chia cùng 8 buổi ảnh: chia ngẫu nhiên rải ảnh validation vào mọi buổi; chia theo buổi giữ riêng cả buổi, đúng tình huống test là buổi mới.')


def floorkt2():
    s = Fig(640, 230)
    ax = s.axes(70, 20, 430, 170, (0, 8), (0, 1.2), xticks=[0, 2, 4, 6, 8], yticks=[0, .4, .8, 1.2],
                xlabel='logit lớp đúng hơn hai lớp kia')
    m = np.linspace(0, 8, 161)
    ce = -np.log(np.exp(m) / (np.exp(m) + 2))
    p = np.exp(m) / (np.exp(m) + 2)
    q = 1 / (np.exp(m) + 2)
    dbl = -np.log(np.exp(p) / (np.exp(p) + 2 * np.exp(q)))
    floor = -np.log(np.e / (np.e + 2))
    ax.hline(floor, FAINT, 1, '4 4')
    ax.line(m, ce, BLUE, 2.2).line(m, dbl, CLAY, 2.2)
    s.label(ax.X(8) + 8, ax.Y(dbl[-1]) - 8, 'softmax rồi loss', 12, 'start', CLAY, 600)
    s.mono(ax.X(8) + 8, ax.Y(dbl[-1]) + 10, f'sàn {floor:.3f}', 11.5, 'start', CLAY)
    s.label(ax.X(8) + 8, ax.Y(ce[-1]), 'logits vào loss', 12, 'start', BLUE, 600)
    s.label(ax.x - 8, ax.y - 10, 'cross-entropy', 11.5, 'start', FAINT)
    s.save('4-kt2-floor', 'Cross-entropy của một mẫu ba lớp khi logit lớp đúng tăng dần: đưa logits vào loss thì về 0; áp softmax trước thì loss kẹt ở sàn −ln(e/(e+2)) ≈ 0.551.')


def probkt2():
    s = Fig(640, 220)
    ax = s.axes(70, 20, 400, 160, (0, 1), (0, 4), xticks=[0, .1, .3, .5, 1], yticks=[0, 1, 2, 3, 4],
                xlabel='xác suất lớp đúng')
    pp = np.linspace(.02, 1, 200)
    ax.line(pp, -np.log(pp), BLUE, 2)
    for v in (.3, .1):
        s.circle(ax.X(v), ax.Y(-np.log(v)), 4.5, CLAY, CLAY, 0)
        s.mono(ax.X(v) + 9, ax.Y(-np.log(v)) - 6, f'{-np.log(v):.2f}', 11.5, 'start', CLAY)
    s.label(ax.x - 8, ax.y - 10, '−ln p', 11.5, 'start', FAINT)
    s.label(560, 70, 'cả hai lúc đều đoán sai', 12, color=TEXT)
    s.label(560, 92, 'accuracy không đổi', 12, color=MUTED)
    s.label(560, 126, 'loss mẫu này', 12, color=TEXT)
    s.mono(560, 148, '1.20 → 2.30', 12, 'middle', CLAY)
    s.save('4-kt2-prob', 'Một mẫu sai có xác suất lớp đúng giảm từ 0.3 xuống 0.1: argmax vẫn sai nên accuracy giữ nguyên, còn loss của mẫu tăng từ 1.20 lên 2.30.')


def regionskt2():
    s = Fig(640, 270)
    lim = (-2.6, 2.6)
    ax = s.axes(90, 16, 220, 220, lim, lim, xticks=[-2, 0, 2], yticks=[-2, 0, 2], grid=False, frame=False)
    xs = ys = np.linspace(-2.6, 2.6, 261)
    X1, X2 = np.meshgrid(xs, ys)
    pred = np.stack([X1, X2, -X1 - X2]).argmax(0)
    cols = [CLAY, BLUE, SAND]
    regions(s, ax, pred, xs, ys, cols, .14)
    for dx, dy in [(1, 1), (1, -2), (-2, 1)]:
        t = 2.6 / max(abs(dx), abs(dy))
        s.line(ax.X(0), ax.Y(0), ax.X(dx * t), ax.Y(dy * t), FAINT, 1)
    for (x, y), c in zip([(2, 0), (0, 2), (-1, -1)], cols):
        s.circle(ax.X(x), ax.Y(y), 5, c, c, 0)
    s.circle(ax.X(1.5), ax.Y(0), 5, BLUE, PAPER, 2)
    s.label(ax.X(1.75), ax.Y(-1.4), 'vùng 0', 12, color=CLAY, weight=600)
    s.label(ax.X(-1.2), ax.Y(2.1), 'vùng 1', 12, color=BLUE, weight=600)
    s.label(ax.X(-1.6), ax.Y(-1.9), 'vùng 2', 12, color=SAND, weight=600)
    s.mono(370, 70, 'x = (1.5, 0)', 12.5, 'start', TEXT)
    s.mono(370, 96, 'logits 1.5, 0, −1.5', 12, 'start', MUTED)
    s.mono(370, 122, 'dự đoán 0, nhãn thật 1', 12, 'start', CLAY)
    s.label(370, 170, 'biên: nơi hai logit bằng nhau', 11.5, 'start', MUTED)
    s.label(370, 190, 'ba tia đi qua gốc', 11.5, 'start', MUTED)
    s.save('4-kt2-regions', 'Ba vùng quyết định của head đặt tay. Mẫu (1.5, 0) có nhãn 1 (vòng rỗng) nằm trong vùng của lớp 0.')


def orderkt2():
    s = Fig(640, 240)
    sub = [(43, 0), (41, 1), (42, 2), (44, 0)]
    truth = [(41, 1), (42, 2), (43, 0), (44, 1)]
    s.label(150, 22, 'file nộp', 12.5, color=TEXT, weight=600)
    s.label(470, 22, 'judge chấm theo hàng', 12.5, color=TEXT, weight=600)
    s.label(110, 44, 'id', 11, color=MUTED)
    s.label(190, 44, 'dự đoán', 11, color=MUTED)
    s.label(430, 44, 'id', 11, color=MUTED)
    s.label(510, 44, 'nhãn thật', 11, color=MUTED)
    for i, ((a, p), (b, t)) in enumerate(zip(sub, truth)):
        y = 56 + i * 38
        s.tiles(80, y, [[str(a), str(p)]], 60, 30, BLUE, 20, size=12.5)
        s.tiles(400, y, [[str(b), str(t)]], 60, 30, GREEN, 20, size=12.5)
        s.arrow(244, y + 15, 392, y + 15, FAINT, 1.1)
        s.mono(318, y + 9, '✗', 13, 'middle', CLAY, 600)
    s.label(320, 222, 'cùng nội dung: chấm theo id được 0.75, chấm theo hàng được 0', 11.5, color=MUTED)
    s.save('4-kt2-order', 'File nộp giữ thứ tự input 43, 41, 42, 44; judge bỏ cột id và chấm theo thứ tự 41, 42, 43, 44 nên cả bốn hàng đều sai.')


def flowkt2():
    s = Fig(640, 120)
    steps = [('đề', 'metric, split'), ('baseline', 'nộp bản đầu'), ('một batch', 'shape, loss, grad'),
             ('thay đổi', 'so cùng split'), ('checkpoint', 'theo tiêu chí'), ('tải lại', 'rồi mới nộp')]
    w, g = 96, 9
    for k, (a, b) in enumerate(steps):
        x = 8 + k * (w + g)
        s.box(x, 30, w, 54, 'none', CLAY if k == 5 else BLUE, r=8, width=0, opacity=.24 if k == 5 else .14)
        s.label(x + w / 2, 50, a, 12.5, color=TEXT, weight=600)
        s.label(x + w / 2, 68, b, 11, color=MUTED)
        if k:
            s.arrow(x - g + 1, 57, x - 1, 57, LINE, 1.1)
    s.save('4-kt2-flow', 'Quy trình ôn khóa 2: đọc đề, nộp baseline, debug một batch, thử từng thay đổi trên cùng split, chọn checkpoint, tải lại rồi nộp.')


FIGSKT2 = {'4-kt2-split': splitkt2, '4-kt2-floor': floorkt2, '4-kt2-prob': probkt2, '4-kt2-regions': regionskt2,
           '4-kt2-order': orderkt2, '4-kt2-flow': flowkt2}

FIGS = {**FIGS41, **FIGS42, **FIGS43, **FIGS44, **FIGS45, **FIGSKT2}

if __name__ == '__main__':
    for n in sys.argv[1:] or list(FIGS):
        FIGS[n]()
        print('ok', n)
