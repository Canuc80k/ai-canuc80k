"""Use the lesson's actual models/data to draw mechanisms, not score-only bars."""
from pathlib import Path
import re,io,contextlib,os,json
import numpy as np
from svg import SVG,BLUE,CLAY,LINE
from plots import plt,write,FONT
R=Path(__file__).resolve().parent;C=R.parent
def run_lesson(id):
    p=next((C/'content').glob('phase-*/'+id+'.md'));text=p.read_text(encoding='utf-8')
    ns={'__name__':'figure_experiment'}
    with contextlib.redirect_stdout(io.StringIO()):
        for code in re.findall(r'^```python\r?\n(.*?)^```',text,re.M|re.S):exec(compile(code,str(p),'exec'),ns)
    return ns
os.chdir(R)
# Existing PCA encoder, held-out query and its actual cosine neighbours.
ns=run_lesson('4.2');digits=ns['digits'];q_id=int(ns['valid_id'][0]);near=ns['nearest'][:3]
s=SVG(640,260);s.text(102,28,'Query',20)
s.image(57,67,89,89,digits.images[q_id].tolist(),hi=16)
for j,i in enumerate(near):
    x=257+j*124;s.image(x,67,89,89,digits.images[int(ns['train_id'][i])].tolist(),hi=16)
    s.text(x+44,187,f'{ns["similarity"][i]:.3f}',19)
s.arrow(174,111,228,111)
s.save('4-2-results','Ảnh truy vấn và ba ảnh train gần nhất theo cosine trong embedding 16 chiều.')
assert ns['y_valid'][0]==0 and np.round(ns['similarity'][near],3).tolist()==[.972,.934,.931]
retrieval_ids=ns['train_id'][near].tolist()
print('retrieval verified',flush=True)

# Actual fine-tuning histories; replacing the generic illustrative curves.
ns=run_lesson('4.3');curves=[]
with contextlib.redirect_stdout(io.StringIO()):
    for opened in [False,True]:
        model,history,epoch,loss,accuracy,count=ns['run_transfer'](opened)
        curves.append({'open':opened,'history':history,'epoch':epoch,'loss':loss,'accuracy':accuracy,'parameters':count})
assert [c['epoch'] for c in curves]==[36,60]
fig,axes=plt.subplots(1,2,figsize=(6.6,3.1))
for ax,c,title in zip(axes,curves,['Head','Encoder + head']):
    h=np.asarray(c['history']);ax.plot(np.arange(1,61),h[:,0],color='#3b6ea8',lw=1.5,label='train')
    ax.plot(np.arange(1,61),h[:,1],color='#c2603e',lw=1.5,label='valid')
    ax.scatter([c['epoch']],[c['loss']],color='#c2603e',s=24,zorder=4)
    ax.set(xlabel='epoch',ylabel='loss',title=title);ax.legend(frameon=False,fontsize=9)
fig.tight_layout(w_pad=1.8);write(fig,'4-3-transfer')
c=curves[0];h=np.asarray(c['history']);fig,ax=plt.subplots(figsize=(6.3,3.0))
ax.plot(np.arange(1,61),h[:,0],color='#3b6ea8',lw=1.5,label='train')
ax.plot(np.arange(1,61),h[:,1],color='#c2603e',lw=1.5,label='valid')
ax.axvline(c['epoch'],color='#c2603e',ls='--',lw=.8,alpha=.6);ax.scatter([c['epoch']],[c['loss']],color='#c2603e',s=24,zorder=4)
ax.set(xlabel='epoch',ylabel='loss');ax.legend(frameon=False,fontsize=10);fig.tight_layout();write(fig,'4-3-validation')
print('fine tuning histories verified',flush=True)

# Feature maps from the TinyCNN that the lesson actually trains.
ns=run_lesson('5.2');torch=ns['torch'];model=ns['model'];model.eval();maps=[]
conv=next(m for m in model.modules() if isinstance(m,torch.nn.Conv2d))
handle=conv.register_forward_hook(lambda module,args,out:maps.append(out.detach().cpu()))
with torch.no_grad():pred=model(ns['valid_images'][:1]).argmax(dim=1).item()
handle.remove();h=maps[0][0].clamp(min=0).numpy();order=np.argsort(-h.var(axis=(1,2)))[:3]
s=SVG(640,240);s.image(30,62,103,103,ns['valid_images'][0,0].numpy().tolist(),hi=1);s.text(82,27,'Input',20)
lim=float(h[order].max())
for j,k in enumerate(order):
    x=236+j*130;s.image(x,62,103,103,h[k].tolist(),hi=lim);s.text(x+51,27,f'K{k+1}',20)
s.arrow(153,113,213,113)
s.save('5-2-metrics','Ảnh validation và ba feature map thật sau Conv + ReLU của TinyCNN đã train.')
assert pred==int(ns['valid_labels'][0])
(R/'experiment-results.json').write_text(json.dumps({'retrieval_query_id':q_id,'retrieval_ids':retrieval_ids,'fine_tuning':curves,'cnn_pred':pred,'cnn_label':int(ns['valid_labels'][0]),'cnn_channels':order.tolist()},ensure_ascii=False,indent=2),encoding='utf-8')
print('CNN activations verified',flush=True)
