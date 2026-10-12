import math
from svg import SVG,BLUE,CLAY,SAND,LINE,INK

def connect(s,a,b,c=BLUE,w=1,opacity=.32,start_r=9,end_r=9):
    dx=b[0]-a[0];dy=b[1]-a[1];d=math.hypot(dx,dy)
    s.path(f'M {a[0]+start_r*dx/d:g},{a[1]+start_r*dy/d:g} L {b[0]-end_r*dx/d:g},{b[1]-end_r*dy/d:g}',c,w,opacity=opacity)

def net(s,xs,counts,y=140,span=130,colors=None):
    layers=[]
    for x,n in zip(xs,counts):
        ys=[y] if n==1 else [y-span/2+i*span/(n-1) for i in range(n)]
        layers.append([(x,q) for q in ys])
    for i,(a,b) in enumerate(zip(layers,layers[1:])):
        for p in a:
            for q in b:connect(s,p,q,(colors or [BLUE]*len(xs))[i])
    for i,layer in enumerate(layers):
        color=(LINE if i==0 else colors[min(i-1,len(colors)-1)]) if colors else BLUE
        for x,q in layer:s.circle(x,q,7,color,'none',1.5)

def shapes():
    s=SVG(640,300)
    s.text(101,33,'X (2, 3)',20);s.text(321,33,'W (3, 2)',20);s.text(542,33,'XW (2, 2)',20)
    s.matrix(38,99,[[1,2,3],[4,5,6]],42,BLUE)
    s.text(220,141,'@',27)
    s.matrix(279,78,[[1,0],[0,1],[1,1]],42,CLAY)
    s.arrow(403,140,457,140)
    s.matrix(500,99,[[4,5],[10,11]],42,BLUE)
    s.save('3-1-shapes','Chiều trong bằng 3; phép nhân giữ hai mẫu và tạo hai đầu ra.')

def graph():
    s=SVG(640,290)
    for x,k,v,c in [(80,'w','2',BLUE),(310,'u = 3w','6',BLUE),(560,'J = (u−1)²','25',CLAY)]:
        s.text(x,34,k,20);s.node(x,108,v,29,c,23)
    s.arrow(115,108,273,108);s.text(196,80,'× 3',18)
    s.arrow(345,108,523,108)
    s.arrow(523,225,345,225,CLAY);s.text(430,198,'∂J/∂u = 10',18)
    s.arrow(273,225,115,225,CLAY);s.text(195,198,'× 3',18)
    s.text(80,225,'30',24);s.text(560,225,'10',24)
    s.save('3-1-graph','Chain rule nhân các đạo hàm cục bộ trên đường từ J về w.')

def accumulate():
    s=SVG(640,285)
    s.text(320,28,'.grad',22)
    for x,v in [(70,'30'),(235,'60'),(400,'None'),(565,'30')]:s.node(x,130,v,31,CLAY,22 if v!='None' else 17)
    for a,b,t,c in [(108,196,'+ 30',CLAY),(273,361,'clear',BLUE),(438,526,'+ 30',CLAY)]:
        s.arrow(a,130,b,130,c);s.text((a+b)/2,95,t,19)
    s.save('3-1-autograd-sum','Hai lần backward cộng gradient; xóa trước lượt mới để tránh cộng dồn.')

def backprop():
    s=SVG(640,355);net(s,[80,315,545],[2,3,1],140,130)
    for x,t,d in [(80,'X','(B, 2)'),(315,'H','(B, 3)'),(545,'p','(B, 1)')]:
        s.text(x,32,t,22);s.text(x,235,d,18)
    s.node(597,217,'J',20,CLAY,21);s.arrow(554,157,581,197,CLAY)
    s.path('M 597,240 C 597,299 417,309 338,307',CLAY,1.6);s.arrow(345,307,325,307,CLAY)
    s.path('M 299,307 C 208,307 141,307 98,277',CLAY,1.6);s.arrow(101,279,90,269,CLAY)
    s.text(447,335,'G₂W₂ᵀ',20);s.text(180,335,'ReLU′',20)
    s.save('3-2-backprop','Luồng gradient của mạng 2 → 3 → 1 trong ví dụ PyTorch.')

def train_loop():
    s=SVG(640,355)
    s.matrix(35,100,[[1,2],[2,-1]],34,BLUE,fs=18);s.text(70,48,'Batch',20)
    net(s,[230,320,407],[2,3,1],140,92)
    s.text(320,48,'fθ',22);s.text(409,199,'ŷ',22)
    s.arrow(128,140,198,140,BLUE);s.arrow(427,140,505,140)
    s.node(556,140,'J',28,CLAY,24)
    s.path('M 556,174 C 556,286 326,295 281,234',CLAY,1.6)
    s.arrow(286,241,276,224,CLAY);s.text(470,285,'∇θJ',23)
    s.text(260,322,'θ ← θ − η∇θJ',23)
    s.save('3-4-loop','Mỗi batch tạo loss, gradient rồi một bước cập nhật tham số.')

def checkpoint():
    s=SVG(640,255)
    for x,label in [(50,'θ'),(480,'θ')]:
        s.matrix(x,85,[['w₁','w₂'],['b₁','b₂']],48,BLUE,fs=20);s.text(x+48,38,label,23)
    s.rect(276,62,87,129,LINE,fill='none',radius=3)
    s.path('M 343,62 L 343,87 L 363,87',LINE)
    s.text(319,139,'best.pt',18)
    s.arrow(166,132,255,132,BLUE);s.text(210,105,'save',18)
    s.arrow(384,132,458,132,BLUE);s.text(421,105,'load',18)
    s.save('3-4-checkpoint','Lưu và khôi phục cùng bộ tham số đã chọn trên validation.')

def dropout():
    s=SVG(640,325)
    s.text(126,30,'h',23);s.text(360,30,'Train · p = 0.5',19)
    s.matrix(42,81,[[1,2,3,4]],42,BLUE)
    s.matrix(310,81,[[2,0,6,0]],42,CLAY,{(0,1):LINE,(0,3):LINE})
    s.arrow(229,102,286,102,CLAY);s.text(257,72,'× 2',19)
    s.text(126,220,'h',23);s.text(360,220,'Eval',19)
    s.matrix(42,250,[[1,2,3,4]],42,BLUE);s.matrix(310,250,[[1,2,3,4]],42,BLUE);s.arrow(229,271,286,271)
    s.save('3-6-dropout','Train bỏ ngẫu nhiên neuron và scale; eval dùng toàn bộ giá trị.')

def memory():
    s=SVG(640,205);s.text(320,26,'FP32 · Adam',20)
    for i,label in enumerate(['θ','∇θ','m','v']):
        x=50+i*135;c=[BLUE,CLAY,SAND,BLUE][i]
        s.rect(x,72,135,72,c,c,opacity=.10);s.text(x+67,91,label,22);s.text(x+67,124,'4 B',18)
    s.line(50,172,590,172);s.text(320,195,'16 byte / tham số',20)
    s.save('3-7-memory','Trọng số, gradient và hai moment của Adam đều chiếm bộ nhớ.')

def device():
    s=SVG(640,275)
    for y,c1,c2,mark,col in [(75,'CPU','GPU','✕',CLAY),(205,'GPU','GPU','✓',BLUE)]:
        s.card(52,y-38,127,75,'X',c1,BLUE);s.card(395,y-38,127,75,'θ',c2,BLUE)
        s.arrow(205,y,360,y,col);s.text(288,y-30,mark,26,color=col)
    s.save('3-7-debug','Đầu vào và tham số phải nằm trên cùng thiết bị.')

def padding():
    s=SVG(640,255);s.text(155,25,'Token IDs',20);s.text(500,25,'Mask',20)
    ids=[[2,3,4,0],[5,6,0,0]];mask=[[1,1,1,0],[1,1,0,0]]
    hi={(i,j):LINE for i in range(2) for j in range(4) if not mask[i][j]}
    s.matrix(54,79,ids,45,BLUE,hi);s.matrix(407,79,mask,45,CLAY,hi)
    s.arrow(270,124,370,124);s.text(500,213,'PAD = 0',18)
    s.save('3-8-padding','Padding tạo tensor cùng chiều dài; mask đánh dấu vị trí có thông tin.')

def pooling(name='3-8-pooling',vals=None,mask=None):
    vals=vals or [[2,0],[0,4],[0,0]];mask=mask or [1,1,0]
    s=SVG(640,305);s.text(135,30,'Vector token',20)  # lượt 7: trước là 'Token vectors'
    hi={(i,j):LINE for i in range(len(vals)) for j in range(2) if not mask[i]}
    s.matrix(88,73,vals,42,BLUE,hi)
    for i,m in enumerate(mask):
        s.rect(33,73+i*42,31,42,LINE)
        s.text(48,94+i*42,m,17)
    s.text(48,30,'m',20)
    total=[sum(row[j]*m for row,m in zip(vals,mask)) for j in range(2)];n=sum(mask)
    s.arrow(198,138,290,138);s.text(239,102,'Σ',24)
    s.matrix(313,116,[total],42,CLAY);s.arrow(422,138,473,138);s.text(448,102,'÷ '+str(n),20)
    s.matrix(499,116,[[round(t/n,3) for t in total]],42,BLUE)
    s.save(name,'Mean pooling cộng và đếm chỉ những token được mask giữ lại.')

def attention(name='3-9-attention',weights=(.731,.269),values=((2,0),(0,4)),out=(1.462,1.076)):
    s=SVG(640,290)
    s.matrix(46,45,[values[0]],53,BLUE,fs=20);s.matrix(46,202,[values[1]],53,CLAY,fs=20)
    s.path('M 174,71 C 245,71 243,129 284,132',BLUE,2.2);s.arrow(269,131,284,132,BLUE)
    s.path('M 174,228 C 245,228 243,169 284,158',CLAY,1.2);s.arrow(269,162,284,158,CLAY)
    s.text(220,47,f'× {weights[0]:.3f}',18,color=BLUE);s.text(220,256,f'× {weights[1]:.3f}',18,color=CLAY)
    s.node(317,145,'+',27,BLUE,28);s.arrow(354,145,413,145)
    s.matrix(442,118,[out],69,BLUE,fs=18)
    s.save(name,'Attention tạo tổ hợp có trọng số của các value.')

def maskflow():
    s=SVG(640,290)
    for i,(v,x) in enumerate(zip([1,0,2],[90,145,200])):
        s.rect(x,211-v*68,29,max(2,v*68),BLUE if i<2 else LINE,BLUE if i<2 else LINE,opacity=.25)
        s.text(x+14,244,str(i+1),17)
    s.line(190,52,235,201,CLAY,1.6);s.line(235,52,190,201,CLAY,1.6)
    s.text(150,27,'Score',20);s.arrow(266,150,368,150);s.text(316,119,'mask',18)
    for v,x in zip([.731,.269,0],[411,466,521]):
        s.rect(x,211-v*170,29,max(2,v*170),BLUE,BLUE,opacity=.22);s.text(x+14,227,f'{v:.3f}'.rstrip('0').rstrip('.'),16)
    s.text(476,27,'Softmax',20)
    s.save('3-9-mask-flow','Loại key tương lai trước softmax để trọng số của nó bằng 0.')

def bottleneck():
    s=SVG(640,285);net(s,[90,320,550],[2,1,2],143,108)
    for x,t in [(90,'x'),(320,'z'),(550,'x̂')]:s.text(x,31,t,24)
    s.text(90,243,'2 chiều',19);s.text(320,243,'1 chiều',19);s.text(550,243,'2 chiều',19)
    s.save('3-10-bottleneck','Minh họa nút thắt 2 → 1 → 2: nén rồi tái tạo hai chiều đầu vào.')

def package():
    s=SVG(640,300)
    for x,t in [(72,'Processor'),(293,'Weights'),(490,'Labels')]:s.text(x+40,33,t,18)
    s.matrix(33,87,[['x₁','x₂'],['x₃','x₄']],39,BLUE,fs=19)
    s.arrow(140,128,230,128)
    net(s,[270,330,390],[2,3,2],125,87)
    s.arrow(409,128,465,128)
    s.rect(486,77,118,102,LINE,radius=4);s.text(545,108,'0 → A',20);s.text(545,148,'1 → B',20)
    s.text(331,245,'Config',18);s.path('M 299,206 L 299,269 L 358,269 L 358,206 Z',LINE);s.line(309,222,349,222,LINE);s.line(309,233,343,233,LINE)
    s.save('4-1-package','Processor, kiến trúc, weights và labels cùng xác định phép dự đoán.')

def batches():
    s=SVG(640,275);s.text(320,25,'B = 2',21)
    for i in range(5):s.rect(80+i*100,62,74,50,BLUE);s.text(117+i*100,87,i,23)
    for x,w in [(69,193),(269,193),(469,93)]:
        s.path(f'M {x},121 L {x},133 L {x+w},133 L {x+w},121',CLAY)
    s.rect(78,196,474,53,BLUE)
    for i in range(5):s.text(125+i*95,222,i,22)
    for x in [165,365,510]:s.arrow(x,146,x,181,CLAY)
    s.save('4-1-batches','Chia batch rồi ghép kết quả theo đúng thứ tự input.')

def reuse():
    s=SVG(640,345);s.image(23,132,82,82,[[0,0,0,1,0,0],[0,0,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,1,1,1,0]],hi=1)
    s.arrow(124,174,180,174);s.node(221,174,'fθ',31,BLUE,23);s.arrow(263,174,309,174)
    s.matrix(321,138,[['z₁'],['z₂']],36,BLUE,fs=19)
    for y,t in [(55,'Probe'),(173,'kNN'),(292,'Cluster')]:
        s.path(f'M 376,174 C 423,174 423,{y} 466,{y}',BLUE);s.arrow(454,y,470,y)
        s.text(547,y-21,t,19)
        if t=='Probe':s.line(498,y+34,589,y-1,CLAY);s.circle(522,y+20,3,BLUE);s.circle(560,y+21,3,CLAY)
        elif t=='kNN':
            for x0,y0,c in [(513,14,BLUE),(537,28,BLUE),(564,14,CLAY)]:s.circle(x0,y+y0,4,c)
            s.circle(545,y+12,7,SAND,'none')
        else:
            s.circle(523,y+19,19,BLUE,'none');s.circle(576,y+19,19,CLAY,'none')
    s.save('4-2-reuse','Cùng một embedding có thể dùng cho nhiều bài toán phía sau.')

def unfreeze():
    s=SVG(640,410)
    for j,(label,cols) in enumerate([('Head',[BLUE,BLUE,CLAY]),('Block cuối',[BLUE,CLAY,CLAY]),('Toàn bộ',[CLAY,CLAY,CLAY])]):
        y=70+j*125;s.text(84,y,label,18)
        net(s,[210,323,433,557],[2,2,2,1],y,44,cols+[CLAY])
    s.circle(259,385,4,BLUE);s.text(303,385,'Freeze',17)
    s.circle(403,385,4,CLAY);s.text(447,385,'Learn',17)
    s.save('4-3-unfreeze','Phạm vi mở tham số tăng từ head tới các block encoder.')

def lora():
    s=SVG(640,310);s.text(137,27,'W₀ · 6 × 8',21);s.text(344,27,'B · 6 × 2',21);s.text(510,27,'A · 2 × 8',21)
    s.image(41,70,192,144,[[1]*8 for _ in range(6)],hi=1,color=BLUE)
    s.text(274,137,'+',29);s.image(320,70,48,144,[[1]*2 for _ in range(6)],hi=1,color=CLAY)
    s.text(393,137,'@',23);s.image(416,118,192,48,[[1]*8 for _ in range(2)],hi=1,color=CLAY)
    s.text(320,269,'W = W₀ + (α/r) BA',23)
    s.save('4-4-path','Hai ma trận hạng thấp tạo phần sửa cho weights cố định.')

def candidates():
    s=SVG(640,325);cx,cy=320,165;r=112
    s.circle(cx,cy,r,LINE,'none',1)
    for angle,label in [(0,'C₀'),(math.pi/2,'C₁'),(math.pi,'C₂')]:
        x=cx+r*math.cos(angle);y=cy-r*math.sin(angle);s.arrow(cx,cy,x,y,BLUE);s.text(x+20*math.cos(angle),y-20*math.sin(angle),label,20)
    s.arrow(cx,cy,cx+.8*r,cy-.6*r,CLAY,1.9);s.text(430,88,'Ảnh',20,color=CLAY)
    s.save('4-5-candidates','Zero-shot so hướng embedding ảnh với embedding của các mô tả lớp.')

for f in [shapes,graph,accumulate,backprop,train_loop,checkpoint,dropout,memory,device,padding,pooling,attention,maskflow,bottleneck,package,batches,reuse,unfreeze,lora,candidates]:f()
