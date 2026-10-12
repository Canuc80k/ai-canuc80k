"""Small, geometry-first SVG authoring primitives. No automatic prose boxes."""
from pathlib import Path
import html,math,json
R=Path(__file__).resolve().parent
INK='currentColor'; BLUE='var(--t-n, #3b6ea8)'; CLAY='var(--accent, #c2603e)'; SAND='#b8892b'
LINE='var(--line-strong, #d3cebf)'
class SVG:
    def __init__(self,w=640,h=360):
        self.w=w;self.h=h;self.parts=[];self.labels=[];self.caption=''
    def text(self,x,y,value,size=18,anchor='middle',color=INK,weight=400,math=False):
        lines=str(value).split('\n'); step=size*1.35
        for i,line in enumerate(lines):
            y0=y+i*step
            self.parts.append(f'<text x="{x:g}" y="{y0:g}" fill="{color}" text-anchor="{anchor}" dominant-baseline="middle" font-size="{size:g}" font-weight="{weight}">{html.escape(line)}</text>')
            self.labels.append({'x':x,'y':y0,'text':line,'size':size,'anchor':anchor})
        return self
    def line(self,x1,y1,x2,y2,color=INK,width=1.4,dash=None):
        extra=f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<path d="M {x1:g},{y1:g} L {x2:g},{y2:g}" fill="none" stroke="{color}" stroke-width="{width:g}" stroke-linecap="round"{extra}/>');return self
    def path(self,d,color=INK,width=1.4,fill='none',opacity=1,dash=None):
        extra=f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width:g}" opacity="{opacity:g}" stroke-linecap="round" stroke-linejoin="round"{extra}/>');return self
    def arrow(self,x1,y1,x2,y2,color=INK,width=1.4,dash=None):
        self.line(x1,y1,x2,y2,color,width,dash)
        a=math.atan2(y2-y1,x2-x1);l=8
        p=[(x2-l*math.cos(a-s),y2-l*math.sin(a-s)) for s in [.42,-.42]]
        self.path(f'M {p[0][0]:g},{p[0][1]:g} L {x2:g},{y2:g} L {p[1][0]:g},{p[1][1]:g}',color,width)
        return self
    def rect(self,x,y,w,h,color=LINE,fill='none',radius=0,opacity=1,width=1.2):
        self.parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{radius:g}" fill="{fill}" fill-opacity="{opacity:g}" stroke="{color}" stroke-width="{width:g}"/>');return self
    def circle(self,x,y,r=5,color=BLUE,fill=None,width=1.4,opacity=1):
        self.parts.append(f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill or color}" fill-opacity="{opacity:g}" stroke="{color}" stroke-width="{width:g}"/>');return self
    def matrix(self,x,y,values,cell=40,color=BLUE,highlights=None,labels=True,fs=18):
        nr=len(values);nc=len(values[0]);highlights=highlights or {}
        for i,row in enumerate(values):
            for j,v in enumerate(row):
                fill=highlights.get((i,j),'none')
                self.rect(x+j*cell,y+i*cell,cell,cell,LINE,fill,opacity=.14 if fill!='none' else 1,width=.8)
                if labels:self.text(x+(j+.5)*cell,y+(i+.5)*cell,v,fs)
        # Only the perimeter uses the semantic color; keep inner grid quiet.
        self.rect(x,y,nc*cell,nr*cell,color,width=1.3)
        return self
    def node(self,x,y,label,r=25,color=BLUE,size=18):
        self.circle(x,y,r,color,'none');self.text(x,y,label,size);return self
    def card(self,x,y,w,h,title,value=None,color=BLUE):
        self.rect(x,y,w,h,color,radius=5)
        if value is None:self.text(x+w/2,y+h/2,title)
        else:
            self.text(x+w/2,y+h*.33,title,16)
            self.text(x+w/2,y+h*.7,value,20)
        return self
    def image(self,x,y,w,h,values,lo=0,hi=None,color=BLUE):
        hi=max(max(v) for v in values) if hi is None else hi
        nr=len(values);nc=len(values[0]);cw=w/nc;ch=h/nr
        for i,row in enumerate(values):
            for j,v in enumerate(row):
                alpha=max(.03,min(.95,.06+.85*(float(v)-lo)/(hi-lo or 1)))
                self.rect(x+j*cw,y+i*ch,cw+.1,ch+.1,'none',color,opacity=alpha,width=0)
        self.rect(x,y,w,h,LINE,width=.8);return self
    def save(self,name,caption):
        self.caption=caption
        text=''.join(self.parts)
        out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="640" role="img" aria-label="{html.escape(caption,quote=True)}" style="font-family:var(--serif, Lora, Georgia, serif);color:var(--text, #1f1e1c)"><title>{html.escape(caption)}</title>{text}</svg>'
        p=R/'staged'/f'phase-{name.split("-")[0]}'/'fig'/f'{name}.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(out,encoding='utf-8')
        meta=R/'labels';meta.mkdir(exist_ok=True);(meta/f'{name}.json').write_text(json.dumps(self.labels,ensure_ascii=False),encoding='utf-8')
        return p
