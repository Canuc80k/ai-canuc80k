from pathlib import Path
import re,io,contextlib,json
import numpy as np
from svg import SVG,BLUE,CLAY
from plots import plt,write
R=Path(__file__).resolve().parent;C=R.parent

# Same samples and exact counts as the lesson, represented as individuals.
s=SVG(640,320)
for start,n,hit,title in [(66,90,81,'Cũ · 81/90'),(396,10,2,'Mới · 2/10')]:
    s.text(start+89,27,title,21)
    rows=(n+9)//10;y0=230-rows*18
    for i in range(n):
        row,col=divmod(i,10);color=BLUE if i<hit else CLAY
        s.rect(start+col*18,y0+row*18,13,13,color,color,opacity=.29)
s.circle(229,289,4,BLUE);s.text(271,289,'Đúng',18);s.circle(364,289,4,CLAY);s.text(401,289,'Sai',18)
s.save('8-2-validation-slices','Hai nhóm dùng cùng đơn vị một mẫu: 81/90 đúng ở camera cũ, 2/10 ở camera mới.')

p=C/'content/phase-8/8.4.md';ns={'__name__':'mixture_figure'}
with contextlib.redirect_stdout(io.StringIO()):
    for code in re.findall(r'^```python\r?\n(.*?)^```',p.read_text(encoding='utf-8'),re.M|re.S):exec(compile(code,str(p),'exec'),ns)
weights=np.asarray(ns['weight_grid']);tp=np.asarray(ns['tune_probs']);y=np.asarray(ns['y_tune']);chosen=ns['chosen_weights']
assert np.allclose(chosen,[0,.25,.75])
grid=np.linspace(0,1,61);x,yy=np.meshgrid(grid,grid);z=np.full(x.shape,np.nan)
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        a,b=x[i,j],yy[i,j]
        if a+b<=1+1e-9:
            probs=np.tensordot([max(0,1-a-b),a,b],tp,axes=(0,0))
            z[i,j]=-np.log(np.maximum(1e-15,probs[np.arange(len(y)),y])).mean()
fig,ax=plt.subplots(figsize=(5.4,4.1));cs=ax.contourf(x,yy,z,levels=12,cmap='YlGnBu',alpha=.35)
ax.contour(x,yy,z,levels=6,colors='#1f1e1c',linewidths=.5,alpha=.24)
ax.scatter(weights[:,1],weights[:,2],color='#1f1e1c',s=12,zorder=3)
ax.scatter([chosen[1]],[chosen[2]],color='#c2603e',s=62,marker='*',zorder=4)
ax.set(xlabel='Trọng số forest',ylabel='Trọng số kNN',xlim=(-.03,1.03),ylim=(-.03,1.03));ax.set_aspect('equal')
fig.colorbar(cs,ax=ax,shrink=.72,pad=.07,label='Log loss trên tune')
fig.tight_layout();write(fig,'8-4-tune-audit')
(R/'mixture-loss-data.json').write_text(json.dumps({'chosen':chosen.tolist(),'candidate_weights':weights.tolist(),'candidate_losses':ns['losses'],'models':list(ns['models']),'best_index':ns['best_index'],'weights_constraint':'w_linear=1-w_forest-w_knn'},ensure_ascii=False,indent=2),encoding='utf-8')
print('15 candidate mixtures, chosen (0,.25,.75), exact tune loss surface verified')
