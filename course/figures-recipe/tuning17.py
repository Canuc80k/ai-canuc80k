"""Bài 1.7: F1 train và CV theo k, lấy từ đúng GridSearchCV mà bài chạy."""
from pathlib import Path
import re, io, contextlib
import pandas as pd
from plots import plt, write

R = Path(__file__).resolve().parent
C = R.parent
p = C / 'content/phase-1/1.7.md'
ns = {'__name__': 'tuning_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
        exec(compile(code, str(p), 'exec'), ns)
log = pd.DataFrame(ns['grid'].cv_results_)
fig, ax = plt.subplots(figsize=(6.3, 3.1))
for weights, color in [('uniform', '#3b6ea8'), ('distance', '#c2603e')]:
    rows = log[log['param_knn__weights'] == weights].sort_values('param_knn__n_neighbors')
    k = rows['param_knn__n_neighbors'].astype(int).to_numpy()
    ax.plot(k, rows['mean_train_score'], color=color, ls='--', lw=1.2, marker='o', ms=3, label=f'{weights}, train')
    ax.plot(k, rows['mean_test_score'], color=color, lw=1.7, marker='o', ms=4, label=f'{weights}, CV')
best = log.loc[log['rank_test_score'] == 1].iloc[0]
assert (int(best['param_knn__n_neighbors']), best['param_knn__weights']) == (9, 'distance')
assert round(best['mean_test_score'], 3) == 0.685
ax.scatter([9], [best['mean_test_score']], s=110, facecolors='none', edgecolors='#c2603e', linewidths=1.2, zorder=5)
ax.set(xlabel='k (số hàng xóm)', ylabel='F1', xticks=[3, 9, 21], ylim=(0.55, 1.04))
ax.legend(frameon=False, fontsize=9, ncol=2, loc='upper right', bbox_to_anchor=(1.0, 0.88))
fig.tight_layout()
write(fig, '1-7-grid-log')
print('grid log figure verified', flush=True)
