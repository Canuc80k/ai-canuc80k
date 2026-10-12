"""Bài 5.7: tỉ lệ láng giềng cùng hình (5 láng giềng cosine trong tập test), tách theo lớp,
cho pixel thô, encoder chưa train và encoder contrastive; lấy từ đúng thí nghiệm của bài."""
from pathlib import Path
import re, io, contextlib
import numpy as np
import torch
import torch.nn.functional as F
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-5/5.7.md'
ns = {'__name__': 'neighbors_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)

labels = ns['test_labels']
features = {
    'pixel thô': ns['test_images'].flatten(1).numpy(),
    'encoder chưa train': ns['embed'](ns['random_encoder'], ns['test_images']),
    'contrastive': ns['embed'](ns['encoder'], ns['test_images']),
}


def same_by_class(x, k=5):
    unit = F.normalize(torch.tensor(x), dim=1)
    scores = unit @ unit.T
    scores.fill_diagonal_(float('-inf'))
    near = scores.topk(k, dim=1).indices.numpy()
    same = labels[near] == labels[:, None]
    return same.mean(), [same[labels == c].mean() for c in range(3)]


rates = {}
for name, x in features.items():
    overall, per_class = same_by_class(x)
    rates[name] = per_class
    print(name, round(float(overall), 3), [round(float(v), 3) for v in per_class], flush=True)
# Khớp cột "same shape@5" của bài.
assert [round(float(same_by_class(x)[0]), 3) for x in features.values()] == [0.510, 0.551, 0.812]

fig, ax = plt.subplots(figsize=(6.3, 2.8))
x = np.arange(3)
width = 0.26
for i, (name, color) in enumerate(zip(rates, ['#b8892b', '#3b6ea8', '#c2603e'])):
    ax.bar(x + (i - 1) * width, rates[name], width, color=color, label=name)
ax.set(xticks=x, ylim=(0, 1), ylabel='láng giềng cùng hình')
ax.set_xticklabels(['tròn', 'tam giác', 'chữ nhật'])
ax.legend(frameon=False, fontsize=9, loc='upper right', ncol=3, bbox_to_anchor=(1, 1.12))
fig.tight_layout()
write(fig, '5-7-neighbors')
print('neighbors figure verified', flush=True)
