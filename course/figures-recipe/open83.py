"""Bài 8.3: tỉ lệ giải được theo hidden và điểm của bốn chiến lược, lấy từ đúng thí nghiệm ablation của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-8/8.3.md'
ns = {'__name__': 'ablation_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
results, budget = ns['results'], ns['budget']
names = ['scan 0..7 (baseline)', 'hard + balanced', 'soft + balanced', 'soft + scan']


def solved_rate(games):
    return np.array([np.mean([games[j * 8 + h] is not None for j in range(300)]) for h in range(8)])


def summary(games):
    done = [g for g in games if g is not None]
    return float(np.mean(done)), float(np.mean([g if g is not None else budget + 1 for g in games]))


hard, soft = solved_rate(results['hard + balanced']), solved_rate(results['soft + balanced'])
stats = [summary(results[n]) for n in names]
assert round(stats[1][0], 2) == 2.20 and round(stats[1][1], 2) == 4.92
assert round(stats[2][1], 2) == 2.84 and round(stats[0][1], 2) == 4.50 and round(stats[3][1], 2) == 4.50
assert np.allclose(soft, 1.0) and abs(hard.mean() - 0.6) < 1e-9
assert np.allclose(hard[[1, 3, 5]], 0.0)

fig, (a, b) = plt.subplots(1, 2, figsize=(6.6, 2.9), gridspec_kw={'width_ratios': [1.15, 1]})
x = np.arange(8)
a.bar(x - 0.19, hard, 0.36, color='#c2603e', label='lọc cứng')
a.bar(x + 0.19, soft, 0.36, color='#3b6ea8', label='lọc mềm')
a.set(xlabel='hidden', ylabel='tỉ lệ ván giải được', ylim=(0, 1.12), xticks=x)
a.legend(frameon=False, fontsize=9, loc='lower left', bbox_to_anchor=(-0.02, 1.0), ncol=2)

labels = ['quét', 'cứng + cân đối', 'mềm + cân đối', 'mềm + quét']
y = np.arange(len(names))[::-1]
for yi, (only, score) in zip(y, stats):
    b.plot([only, score], [yi, yi], color='#b8b3a6', lw=1.4, zorder=1)
b.scatter([s[0] for s in stats], y, s=90, facecolor='none', edgecolor='#3b6ea8', lw=1.5, zorder=3, label='chỉ ván giải được')
b.scatter([s[1] for s in stats], y, s=26, color='#c2603e', zorder=4, label='tính cả ván thất bại')
b.set(xlabel='số lượt trung bình', yticks=y, yticklabels=labels, xlim=(1.5, 5.4))
b.legend(frameon=False, fontsize=9, loc='lower left', bbox_to_anchor=(-0.02, 1.0), ncol=1)
fig.tight_layout()
write(fig, '8-3-ablation')
print('ablation figure verified', flush=True)
