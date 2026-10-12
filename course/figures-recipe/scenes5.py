import numpy as np
from svg import SVG,BLUE,CLAY,SAND,LINE,INK
from scenes34 import connect,net

def stripe(horizontal=False,n=12,corner=0):
    a=np.zeros((n,n));a[3:5,:]=1 if horizontal else 0
    if not horizontal:a[:,3:5]=1
    a[0:2,0:2]=corner
    return a.tolist()

def stack(s,x,y,nrow,ncol,count,w=88,c=BLUE):
    for k in range(min(count,3)-1,-1,-1):
        s.rect(x+k*6,y-k*6,w,w,c,c,opacity=.04)
    s.rect(x,y,w,w,c)
    for j in range(1,ncol):s.line(x+j*w/ncol,y,x+j*w/ncol,y+w,LINE,.45)
    for i in range(1,nrow):s.line(x,y+i*w/nrow,x+w,y+i*w/nrow,LINE,.45)
    s.text(x+w/2,y+w+23,f'{count} × {nrow} × {ncol}',17)

def receptive():
    s=SVG(640,355);xs=[120,220,320,420,520]
    for i,x in enumerate(xs):s.node(x,65,i,18,BLUE,18)
    for j,x in enumerate([220,320,420]):
        for i in range(j,j+3):connect(s,(xs[i],65),(x,174),BLUE,1,.27,21,11)
        s.circle(x,174,9,BLUE,'none')
        connect(s,(x,174),(320,289),CLAY,1.3,.65,11,12)
    s.circle(320,289,10,CLAY,'none')
    s.text(40,65,'x',21);s.text(40,174,'L₁',21);s.text(40,289,'L₂',21)
    s.path('M 99,30 L 99,16 L 541,16 L 541,30',CLAY)
    s.save('5-1-receptive','Hai lớp cửa sổ ba ô cho receptive field gồm năm ô đầu vào.')

def pool():
    s=SVG(640,285)
    for start,vals,out,title in [(40,[0,4,0,0],[4,0],'Ban đầu'),(376,[0,0,4,0],[0,4],'Dịch một ô')]:
        s.text(start+88,28,title,20)
        s.matrix(start,66,[vals],44,BLUE,{(0,vals.index(4)):CLAY})
        for j in range(2):
            s.path(f'M {start+j*88},120 L {start+j*88},133 L {start+(j+1)*88},133 L {start+(j+1)*88},120',CLAY)
            s.arrow(start+44+j*88,145,start+44+j*88,183,CLAY)
        s.matrix(start+44,196,[out],44,BLUE)
    s.save('5-1-pool-shift','Dịch đỉnh qua ranh giới cửa sổ làm vị trí kết quả MaxPool đổi.')

def cnn():
    s=SVG(640,420)
    s.image(32,81,91,91,stripe(),hi=1);s.text(78,33,'Ảnh',21);s.text(78,202,'1 × 12 × 12',17)
    stack(s,245,81,12,12,8);stack(s,470,81,6,6,8,w=80)
    s.arrow(140,126,218,126);s.text(181,97,'Conv',18)
    s.arrow(355,126,441,126);s.text(397,97,'Pool',18)
    s.path('M 510,206 C 510,257 452,297 412,297',BLUE);s.arrow(429,297,412,297)
    s.text(439,230,'Mean',18)
    s.matrix(231,278,[['h₁','h₂','…','h₈']],40,BLUE,fs=18)
    s.arrow(213,299,161,299);s.matrix(38,278,[['z₀','z₁']],47,CLAY,fs=20)
    s.text(103,362,'Linear head',18)
    s.save('5-2-cnn','Các feature map được pooling rồi gom thành vector để phân lớp.')

def residual():
    s=SVG(640,245)
    s.node(74,167,'x',24,BLUE,24);s.node(319,167,'F',31,BLUE,25);s.node(499,167,'+',24,CLAY,27);s.node(600,167,'y',21,BLUE,22)
    s.arrow(106,167,280,167);s.arrow(359,167,467,167);s.arrow(531,167,571,167)
    s.path('M 74,139 L 74,60 L 499,60 L 499,132',BLUE,1.4);s.arrow(499,119,499,132,BLUE)
    s.text(319,31,'Identity',18)
    s.save('5-2-residual','Nhánh identity cộng trực tiếp x vào F(x).')

def cup(s,x,y,flip=False,c=BLUE):
    s.path(f'M {x},{y} L {x+75},{y} L {x+69},{y+77} Q {x+35},{y+94} {x+6},{y+77} Z',c,1.5,fill=c,opacity=.08)
    xx=x+75 if flip else x
    d=f'M {xx},{y+15} C {xx+(43 if flip else -43)},{y+8} {xx+(43 if flip else -43)},{y+67} {xx},{y+60}'
    s.path(d,c,1.5)

def labels():
    s=SVG(640,250)
    cup(s,111,73);cup(s,457,73,True)
    s.arrow(259,111,375,111);s.text(318,82,'flip',20)
    s.text(146,220,'trái',20);s.text(491,220,'phải',20)
    s.save('5-3-labels','Lật ngang giữ loại vật thể nhưng đổi nhãn chỉ hướng.')

def split():
    s=SVG(640,345)
    for j,(letter,col) in enumerate([('A',BLUE),('B',BLUE),('C',CLAY)]):
        s.image(46+j*107,37,62,62,stripe(j%2==1),hi=1,color=col);s.text(77+j*107,123,letter,18)
    s.path('M 31,136 L 31,150 L 233,150 L 233,136',BLUE);s.path('M 245,136 L 245,150 L 316,150 L 316,136',CLAY)
    s.arrow(137,164,137,204,BLUE);s.text(137,329,'Train',19)
    s.image(25,227,65,65,stripe(),hi=1);s.image(104,227,65,65,stripe(),hi=1);s.image(183,227,65,65,stripe(True),hi=1)
    s.path('M 281,165 C 365,170 440,188 482,220',CLAY);s.arrow(471,212,482,220,CLAY)
    s.image(472,231,65,65,stripe(False),hi=1,color=CLAY);s.text(505,329,'Valid · C',19)
    s.save('5-3-split','Tách nguồn trước khi sinh các biến thể augmentation.')

def patches():
    s=SVG(640,320);s.text(127,29,'4 × 4',21);s.text(479,29,'4 patch',21)
    vals=np.arange(16).reshape(4,4).tolist();colors=[BLUE,CLAY,SAND,LINE]
    hi={(i,j):colors[(i//2)*2+j//2] for i in range(4) for j in range(4)}
    s.matrix(55,83,vals,36,BLUE,hi,fs=18)
    patches=[[0,1,4,5],[2,3,6,7],[8,9,12,13],[10,11,14,15]]
    s.matrix(407,83,patches,36,BLUE,{(i,j):colors[i] for i in range(4)for j in range(4)},fs=18)
    s.arrow(245,155,358,155)
    s.save('5-4-patches','Bốn cửa sổ 2 × 2 trở thành bốn token của ảnh.')

def position():
    s=SVG(640,330)
    patterns=[stripe(False,6),stripe(True,6),np.eye(6).tolist(),np.fliplr(np.eye(6)).tolist()]
    for row,order in enumerate([[0,1,2,3],[2,0,3,1]]):
        y=38+row*173
        for j,i in enumerate(order):
            x=58+j*150;s.image(x,y,66,66,patterns[i],hi=1)
            s.text(x+33,y+95,f'p{j}',19)
    for j in range(4):s.arrow(91+j*150,143,91+j*150,188,LINE)
    s.save('5-4-position','Đảo nội dung patch trong khi vị trí token vẫn giữ nguyên.')

def iou():
    s=SVG(640,330);x,y,scale=182,35,45
    s.rect(x,y,4*scale,4*scale,BLUE,BLUE,opacity=.08)
    s.rect(x+scale,y+scale,4*scale,4*scale,CLAY,CLAY,opacity=.08)
    s.rect(x+scale,y+scale,3*scale,3*scale,SAND,SAND,opacity=.12)
    s.text(x-30,y+80,'A',22,color=BLUE);s.text(x+5*scale+30,y+scale+90,'B',22,color=CLAY)
    s.text(x+2.5*scale,y+2.5*scale,'9',26)
    s.text(320,300,'IoU = 9 / (16 + 16 − 9) = 9/23',22)
    s.save('5-5-iou','IoU là diện tích giao chia diện tích hợp của hai box.')

def nms():
    s=SVG(640,260);s.text(153,27,'Trước NMS',20);s.text(493,27,'Sau NMS',20)
    for base,keep in [(30,[0,1,2]),(370,[0,2])]:
        for i,(x,y,w,h,col) in enumerate([(0,0,4,4,BLUE),(.5,.5,4,4,CLAY),(6,0,4,4,SAND)]):
            if i not in keep:continue
            s.rect(base+x*22,72+y*22,w*22,h*22,col)
            if i==0:s.text(base-10,122,'0',18,anchor='end',color=BLUE)
            elif i==1:s.text(base+110,183,'1',18,color=CLAY)
            else:s.text(base+176,122,'2',18,color=SAND)
    s.arrow(284,122,341,122)
    s.save('5-5-nms','NMS giữ box 0 và 2, bỏ box 1 chồng lấn với box điểm cao hơn.')

def masks():
    s=SVG(640,290);s.text(156,27,'Semantic',21);s.text(484,27,'Instance',21)
    for base,inst in [(52,False),(380,True)]:
        fill={(i,j):(BLUE if not inst or j<3 else CLAY) for i in [2,3]for j in [1,2,3,4]}
        s.matrix(base,70,[['']*6 for _ in range(6)],35,BLUE,fill,labels=False)
        if inst:s.text(base+70,175,'1',22);s.text(base+140,175,'2',22)
    s.save('5-6-masks','Semantic gộp cùng lớp; instance tách từng vật thể bằng ID riêng.')

def maskmetrics():
    s=SVG(640,325)
    s.text(52,59,'G',23);s.text(52,156,'P',23)
    s.matrix(91,31,[[1,1,1,0]],49,BLUE,{(0,j):BLUE for j in [0,1,2]})
    s.matrix(91,128,[[1,1,0,1]],49,CLAY,{(0,j):CLAY for j in [0,1,3]})
    for i,t in enumerate(['TP','TP','FN','FP']):s.text(115+i*49,221,t,18)
    s.text(478,87,'IoU = 2/4',23);s.text(478,137,'= 0.5',23)
    s.text(478,234,'Dice = 4/6',23);s.text(478,279,'≈ 0.667',23)
    s.save('5-6-mask-metrics','So mask từng pixel để đếm TP, FP, FN và tính IoU, Dice.')

def unet():
    s=SVG(640,355)
    stack(s,69,63,12,12,4,82);stack(s,469,63,12,12,4,82);stack(s,266,241,6,6,8,69)
    s.arrow(167,99,441,99,CLAY);s.text(308,63,'Skip · concat',19)
    s.arrow(154,177,249,263,BLUE);s.text(164,226,'Pool',18)
    s.arrow(359,263,454,177,BLUE);s.text(462,226,'Up',18)
    s.save('5-6-unet','Nhánh skip đưa chi tiết độ phân giải cao vào decoder.')

def pairs():
    s=SVG(640,300)
    a=np.zeros((8,8));a[1:7,3:5]=1;b=np.roll(a,1,axis=1);c=np.zeros((8,8));c[3:5,1:7]=1
    for x,im,t in [(70,a,'A'),(283,b,'A′'),(497,c,'B')]:s.image(x,57,74,74,im.tolist(),hi=1);s.text(x+37,26,t,21)
    s.path('M 107,148 L 107,179 L 320,179 L 320,148',BLUE);s.text(214,213,'+',25,color=BLUE)
    s.path('M 320,148 L 320,243 L 534,243 L 534,148',CLAY);s.text(427,273,'−',25,color=CLAY)
    s.save('5-7-pairs','Hai view cùng nguồn là cặp positive; view khác nguồn tạo cặp negative.')

def similarity():
    s=SVG(640,275);vals=[[.99,.11,-.99],[.11,.99,.11],[-.99,.11,.99]]
    for i,t in enumerate(['A','B','C']):s.text(234+i*57,28,t,21);s.text(174,84+i*57,t,21)
    s.matrix(206,55,vals,57,BLUE,{(i,i):BLUE for i in range(3)},fs=19)
    s.save('5-7-matrix','Mỗi hàng ảnh được so với từng caption theo cột.')

def diffusion():
    s=SVG(640,235);rng=np.random.default_rng(16);a=np.zeros((8,8));a[1:7,3:5]=1
    for i,(level,t) in enumerate([(0,'x₀'),(.3,'xₜ'),(1,'ε')]):
        noisy=np.clip(a*(1-level)+rng.normal(.5,.28,a.shape)*level,0,1)
        s.image(64+i*213,58,85,85,noisy.tolist(),hi=1);s.text(107+i*213,25,t,23)
    s.arrow(168,99,256,99,BLUE);s.arrow(381,99,469,99,BLUE)
    s.arrow(469,182,168,182,CLAY);s.text(320,216,'Reverse',18)
    s.save('5-8-diffusion','Forward thêm nhiễu; quá trình sinh học đi ngược từng bước.')

def gan():
    s=SVG(640,330)
    s.matrix(27,59,[['z₁'],['z₂'],['…']],27,BLUE,fs=16);s.node(190,99,'G',29,BLUE,25);s.arrow(75,99,151,99)
    s.image(281,67,65,65,stripe(False,8),hi=1);s.arrow(228,99,262,99)
    s.image(281,239,65,65,stripe(True,8),hi=1,color=CLAY)
    s.node(498,185,'D',32,CLAY,26)
    s.path('M 365,99 L 455,165',BLUE);s.arrow(442,155,455,165,BLUE)
    s.path('M 365,271 L 455,205',CLAY);s.arrow(442,215,455,205,CLAY)
    s.arrow(541,185,603,185);s.text(596,217,'p',22)
    s.path('M 485,145 C 460,22 251,19 208,65',CLAY,1.3);s.arrow(215,58,208,65,CLAY)
    s.save('5-8-gan','Gradient từ discriminator đi qua ảnh sinh để cập nhật generator.')

def occlusion():
    s=SVG(640,265)
    for i,(hide,title) in enumerate([('none','Gốc'),('corner','Che góc'),('stroke','Che nét')]):
        im=np.array(stripe(False,8,1));x=63+i*211
        s.image(x,69,84,84,im.tolist(),hi=1);s.text(x+42,30,title,19)
        if hide=='corner':s.rect(x,y=69,w=22,h=22,color=CLAY,fill='var(--bg,#faf9f5)')
        if hide=='stroke':s.rect(x+31,69,22,84,CLAY,'var(--bg,#faf9f5)')
    s.save('5-9-occlusion','Che từng vùng ảnh để kiểm phần nào ảnh hưởng dự đoán.')

def shortcut():
    s=SVG(640,280)
    for i,(horizontal,mark) in enumerate([(False,0),(True,1),(False,1),(True,0)]):
        x=39+i*153;s.image(x,57,78,78,stripe(horizontal,8,mark),hi=1)
        s.rect(x,57,20,20,CLAY,width=1.3)
        s.text(x+39,29,'V' if not horizontal else 'H',21)
        s.text(x+39,169,str(mark),21,color=CLAY)
    s.path('M 39,207 L 39,218 L 270,218 L 270,207',BLUE)
    s.path('M 345,207 L 345,218 L 576,218 L 576,207',CLAY)
    s.save('5-9-shortcut','Đổi tương quan giữa dấu góc và hướng nét để kiểm shortcut.')

def contracts():
    # Mỗi cột: tên bài toán ở trên, dạng đầu ra ở dưới (lượt 7: trước đây cột phân đoạn không có nhãn).
    s=SVG(640,225)
    for x,title in [(98,'Phân loại'),(266,'Phát hiện'),(434,'Phân đoạn'),(581,'Truy xuất')]:s.text(x,26,title,19)
    s.image(57,52,82,82,stripe(),hi=1);s.text(98,178,'y = 0',21)
    s.image(225,52,82,82,stripe(),hi=1);s.rect(240,56,30,71,CLAY,width=1.7);s.text(266,178,'box',21)
    s.image(393,52,82,82,stripe(),hi=1,color=CLAY);s.text(434,178,'mask',21)
    s.image(566,52,38,38,stripe(),hi=1);s.image(566,96,38,38,stripe(True),hi=1)
    s.text(550,77,'1',17);s.text(550,121,'2',17);s.text(581,178,'thứ hạng',21)
    s.save('5-kt3-contract','Classification, detection, segmentation và retrieval có dạng đầu ra khác nhau.')

def experiment(name='5-kt3-loop'):
    s=SVG(640,230)
    s.text(142,28,'A',22);s.text(482,28,'B',22)
    for start in [60,401]:
        s.matrix(start,65,[['x₁'],['x₂'],['x₃']],34,BLUE,fs=18)
        net(s,[start+80,start+133,start+185],[2,3,1],119,70)
    s.arrow(260,120,355,120,CLAY);s.text(308,86,'Δθ',21)
    s.save(name,'Giữ cùng validation khi so sánh một thay đổi của mô hình.')

for f in [receptive,pool,cnn,residual,labels,split,patches,position,iou,nms,masks,maskmetrics,unet,pairs,similarity,diffusion,gan,occlusion,shortcut,contracts,experiment]:f()
