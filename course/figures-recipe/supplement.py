import math
from svg import SVG,BLUE,CLAY,SAND,LINE,INK

def knn():
    s=SVG(640,430);q=(195,239)
    s.circle(*q,99,LINE,BLUE,0,.04)
    pts={'A':(125,309),'B':(195,309),'C':(335,169),'D':(405,99),'E':(265,239)}
    for k in ['A','B','E']:
        x,y=pts[k];dx=x-q[0];dy=y-q[1];d=math.hypot(dx,dy)
        s.line(q[0]+9*dx/d,q[1]+9*dy/d,x-8*dx/d,y-8*dy/d,CLAY,1.2)
    for k,(x,y) in pts.items():s.circle(x,y,5,CLAY if k in ['A','B'] else BLUE)
    for k,labelpos in {'A':(94,328),'B':(223,321),'C':(358,153),'D':(433,91),'E':(293,229)}.items():s.text(*labelpos,k+(': 0' if k in ['A','B'] else ': 1'),18)
    s.node(*q,'q',14,SAND,18)
    s.arrow(55,379,480,379);s.arrow(55,379,55,38)
    for j in [1,2,3,4,5]:s.text(55+j*70,400,j,17)
    for i in [1,2,3,4]:s.text(35,379-i*70,i,17)
    s.save('2-4-knn-vote','Ba láng giềng B, E, A nằm trong vùng gần query q.')

def tree():
    s=SVG(640,280)
    s.line(27,132,270,132,LINE)
    for i,col in enumerate([BLUE,BLUE,CLAY,CLAY]):s.circle(57+i*62,132,6,col);s.text(57+i*62,169,i+1,18)
    s.line(150,63,150,193,SAND,1.2,dash='3 5');s.text(150,38,'2.5',20)
    s.rect(438,38,119,54,LINE,radius=4);s.text(497,65,'x ≤ 2.5',21)
    s.arrow(470,104,407,197,BLUE);s.arrow(525,104,587,197,CLAY)
    s.node(391,224,'0',22,BLUE,24);s.node(603,224,'1',22,CLAY,24)
    s.save('2-5-stump-tree','Ngưỡng 2.5 chia bốn mẫu thành hai lá thuần.')

def bert_masks():
    s=SVG(640,330)
    for x,title,mode in [(92,'Hai chiều','bidirectional'),(400,'Causal','causal')]:
        s.text(x+88,27,title,21)
        fill={(i,j):BLUE for i in range(4)for j in range(3) if mode=='bidirectional' or j<=i}
        s.matrix(x,67,[['']*4 for _ in range(4)],44,BLUE,fill,labels=False)
        for i,t in enumerate(['CLS','không','hay','PAD']):s.text(x+22+i*44,269,t,14);s.text(x-18,89+i*44,str(i+1),17,anchor='end')
    s.save('6-3-attention-masks','Padding mask chặn cột PAD; causal mask chặn các key tương lai.')

knn();tree();bert_masks()

def confusion():
    s=SVG(640,310)
    s.text(80,125,'Thật 0',19);s.text(80,246,'Thật 1',19)
    for j,t in enumerate(['Đoán 0','Đoán 1']):s.text(241+j*185,28,t,21)
    for i,row in enumerate([['TN = 3','FP = 3'],['FN = 1','TP = 3']]):
        for j,t in enumerate(row):
            c=BLUE if i==j else CLAY;s.rect(152+j*185,61+i*121,178,112,c,c,opacity=.08);s.text(241+j*185,117+i*121,t,23)
    s.save('1-5-confusion','Bốn ô đếm dự đoán đúng và sai theo nhãn thật và dự đoán.')
confusion()

def softmax():
    s=SVG(640,285)
    for x,title in [(74,'z'),(312,'exp(z − max z)'),(549,'p')]:s.text(x,31,title,21 if x!=312 else 18)
    for x,values,c in [(48,[[2],[1],[0]],CLAY),(286,[[1],['0.368'],['0.135']],SAND),(521,[['0.665'],['0.245'],['0.090']],BLUE)]:s.matrix(x,81,values,55,c,fs=19)  # lượt 7: số 0.665 chạm viền ở cỡ 22
    s.arrow(132,164,247,164);s.text(188,126,'exp',18)
    s.arrow(369,164,484,164);s.text(426,126,'÷ 1.503',18)
    s.save('2-3-softmax','Trừ max trước exp rồi chia tổng để thu xác suất có tổng bằng 1.')
softmax()
