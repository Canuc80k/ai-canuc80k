"""Redraw scientific figures from captured numerical artists, with no added notes."""
from pathlib import Path
import re,pickle,json,io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.text import Text,Annotation
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

R=Path(__file__).resolve().parent;C=R.parent
p=R/'Lora.ttf'
if not p.exists():
    f=TTFont(C/'output/ui/fonts/lora.woff');f.flavor=None
    if 'fvar' in f:f=instantiateVariableFont(f,{'wght':400},inplace=True)
    f.save(p)
font_manager.fontManager.addfont(str(p))
for p0 in R.glob('Inter-*.ttf'):
    font_manager.fontManager.addfont(str(p0))
FONT=font_manager.FontProperties(fname=str(p)).get_name()
plt.rcParams.update({'font.family':[FONT,'DejaVu Serif','DejaVu Sans'],'mathtext.fontset':'stix','svg.fonttype':'none','svg.hashsalt':'canuc80k-redraw-20261003','axes.spines.top':False,'axes.spines.right':False})
INK='#1f1e1c'
inv=json.loads((R/'capture-inventory.json').read_text(encoding='utf-8'))
CAPTIONS={}
SHORT_TITLES={
 '3-3-activation':['ReLU','tanh','sigmoid'],
 '1-2-fits':['k = 1','k = 10','k = 80'],
 '0-3-bar':['Trục từ 0','Trục từ 5.5'],
 '2-7-fit-stages':['1 cây','10 cây','100 cây'],
 '3-5-paths':['SGD','Momentum'],
 '7-2-order':['Thấp → cao','Cao → thấp'],
 '7-2-confusion':['Mean pooling','CNN'],
 '1-3-groups':['Random split','Group split'],
 '7-1-mel':['6 trong 20 bộ lọc tam giác','20 band log-mel'],  # lượt 7: trước là '6 / 20 bộ lọc tam giác'
 '2-10-kmeans-assign':['Trước cập nhật','Sau cập nhật'],  # lượt 7: trước là 'trước update', 'sau update'
}
RELABEL={
 '8-4-correlation':{'ylabel':'Phương sai so với một model'},
 '8-4-voting':{'texts':{'Hard vote: lớp 1':'Hard voting: lớp 1','Soft vote: lớp 0':'Soft voting: lớp 0'},'xticks':{'Mean':'Trung bình'}},
}
def write(fig,name):
    for t in fig.findobj(match=Text):
        if str(t.get_color()).lower() in {'black','#000000','k'}:t.set_color(INK)
    out=R/'staged'/f'phase-{name.split("-")[0]}'/'fig'/f'{name}.svg';out.parent.mkdir(parents=True,exist_ok=True)
    buf=io.StringIO();fig.savefig(buf,format='svg',transparent=True,bbox_inches='tight',pad_inches=.07,metadata={'Date':None})
    svg=buf.getvalue();svg=re.sub(r'<\?xml.*?\?>\s*|<!DOCTYPE.*?>\s*','',svg,flags=re.S)
    svg=re.sub(r'<metadata>.*?</metadata>','',svg,flags=re.S)
    svg=svg.replace(INK,'currentColor').replace('#000000','currentColor')
    svg=svg.replace('#c2603e','var(--accent, #c2603e)').replace('#3b6ea8','var(--t-n, #3b6ea8)')
    svg=svg.replace('<svg ', '<svg style="font-family:var(--serif,Lora,Georgia,serif);color:var(--text,#1f1e1c)" ',1)
    out.write_text(svg,encoding='utf-8');plt.close(fig)
    return out

def redraw(name,record):
    with (R/'capture'/f'{name}.pickle').open('rb') as f:fig=pickle.load(f)
    if name=='3-3-residual-loss' and len(fig.axes)==2:
        data=[(line.get_xdata().copy(),line.get_ydata().copy()) for line in fig.axes[0].lines[:2]]
        plt.close(fig);fig,a=plt.subplots(figsize=(6.3,3.1))
        for (x,y),label,color in zip(data,['MSE','MAE'],['#c2603e','#3b6ea8']):a.plot(x,y,color=color,lw=1.5,label=label)
        a.set(xlabel='|r|',ylabel='loss');a.legend(frameon=False)
    if name=='3-6-capacity':
        for i,line in enumerate(fig.axes[0].lines[:2]):line.set_label(['train','validation'][i])
        for t in list(fig.axes[0].texts):t.remove()
        fig.axes[0].legend(frameon=False)
    if name=='8-2-shift':
        for line,label in zip(fig.axes[0].lines[:2],['signal + shortcut','signal']):line.set_label(label)
        fig.axes[0].legend(frameon=False)
    if name=='1-3-groups':
        from matplotlib.patches import Patch
        fig.legend(handles=[Patch(facecolor='#3b6ea8',label='Train'),Patch(facecolor='#c2603e',label='Valid')],loc='lower center',bbox_to_anchor=(.5,-.18),ncol=2,frameon=False,prop={'family':FONT,'size':10})
    for t in list(fig.texts):t.remove()
    fig._suptitle=None;fig._supxlabel=None;fig._supylabel=None
    for i,a in enumerate(fig.axes):
        original_title=a.get_title() or a.get_title(loc='left')
        a.set_title('',loc='left');a.set_title('',loc='right');a.set_title('',loc='center')
        # Long notes, panel letters and decorative prose have no place inside a plot.
        for t in list(a.texts):
            text=t.get_text().strip();keep=False
            if isinstance(t,Annotation) and not text:keep=True
            # Heatmap/count labels and terse geometric labels are useful data.
            if re.fullmatch(r'[-+−]?\d+(?:\.\d+)?(?:%| ms)?',text):keep=True
            if text in {'PC1','PC2','OLS','train','validation','ReLU','tanh','sigmoid','MSE','MAE','P','R'}:keep=True
            if len(text)<=24 and text.count(' ')<=4 and any(c.isdigit() for c in text):keep=True
            if len(text)==1 and text.isupper() and t.get_transform()!=a.transAxes:keep=True
            if name=='7-1-spectrogram' and text in {'200 Hz','600 Hz'}:keep=True
            if name=='3-3-activation' and text in {'ReLU','tanh','sigmoid'}:keep=False
            if not keep:t.remove()
            # Lượt 7: nhãn ranh giới đè lên vạch đứt và dải sáng; đặt lệch sang phải vạch.
            elif name=='7-1-spectrogram' and text.startswith('ranh giới'):t.set_ha('left');t.set_x(t.get_position()[0]+.03)
        title=SHORT_TITLES.get(name,[])
        if title and i<len(title):a.set_title(title[i],fontfamily=FONT,fontsize=11,pad=10)
        elif len(fig.axes)>1:
            old=original_title;a.set_title(old if len(old)<27 and '\n' not in old else '',fontfamily=FONT,fontsize=11,pad=10)
        else:a.set_title('')
        a.set_facecolor('none');a.set_axisbelow(True)
        a.tick_params(labelsize=9.5,width=.65,length=3,pad=4)
        a.spines['top'].set_visible(False);a.spines['right'].set_visible(False)
        for spine in a.spines.values():spine.set_color(INK);spine.set_linewidth(.7)
        a.xaxis.label.set_fontfamily(FONT);a.yaxis.label.set_fontfamily(FONT)
        a.xaxis.label.set_fontsize(11);a.yaxis.label.set_fontsize(11)
        a.xaxis.labelpad=8;a.yaxis.labelpad=8
        if name=='2-3-sigmoid':a.set_xlabel('z',fontfamily=FONT,fontsize=11,labelpad=8)
        # Lượt 7: nhãn tiếng Anh trong hình đổi sang thuật ngữ của bài.
        fix=RELABEL.get(name,{})
        if 'ylabel' in fix:a.set_ylabel(fix['ylabel'],fontfamily=FONT,fontsize=11,labelpad=8)
        for t in a.texts:
            if t.get_text() in fix.get('texts',{}):t.set_text(fix['texts'][t.get_text()])
        if fix.get('xticks'):
            labels=[t.get_text() for t in a.get_xticklabels()];a.set_xticks(a.get_xticks());a.set_xticklabels([fix['xticks'].get(l,l) for l in labels])
        for t in a.get_xticklabels()+a.get_yticklabels():t.set_fontfamily(FONT)
        leg=a.get_legend()
        if leg:
            if len(fig.axes)==1:
                handles,labels=a.get_legend_handles_labels()
                leg=a.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,1.03),ncol=min(3,len(labels)),frameon=False)
            leg.get_frame().set_visible(False)
            for t in leg.get_texts():t.set_fontfamily(FONT);t.set_fontsize(9.5)
        for t in a.texts:t.set_fontfamily(FONT);t.set_fontsize(10.5)
    for t in fig.findobj(match=Text):
        if t.get_text():
            t.set_fontfamily([FONT,'DejaVu Serif','DejaVu Sans'])
            if str(t.get_color()).lower() not in {'white','#ffffff','#fff'}:t.set_color(INK)
    # Keep the old Linear regression reference geometry, not the rejected layout.
    try:fig.tight_layout(pad=.65,w_pad=1.65,h_pad=1.35)
    except (ValueError,RuntimeError):pass
    return write(fig,name)

if __name__=='__main__':
    for name,record in inv.items():
        if any(a['on'] for a in record['axes']):redraw(name,record)
    # Exact recovered reference figures are the control for this redesign.
    for p in (R/'reference').glob('*.svg'):
        out=R/'staged/phase-2/fig'/p.name;out.parent.mkdir(parents=True,exist_ok=True)
        svg=p.read_text(encoding='utf-8').replace("'Inter'","'Lora'").replace("'DejaVu Sans'","'Lora'")
        svg=svg.replace('#c2603e','var(--accent, #c2603e)').replace('#3b6ea8','var(--t-n, #3b6ea8)')
        out.write_text(svg,encoding='utf-8')
    print('Scientific plots staged; original seven Linear regression figures restored.')
