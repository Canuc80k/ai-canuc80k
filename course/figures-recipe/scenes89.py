import math
from svg import SVG,BLUE,CLAY,SAND,LINE,INK
from scenes34 import net
from scenes5 import experiment

def clock():
    s=SVG(640,330);cx=320;cy=169;r=110
    s.circle(cx,cy,r,LINE,'none',1)
    for h in range(24):
        a=2*math.pi*h/24;x=cx+r*math.sin(a);y=cy-r*math.cos(a)
        s.circle(x,y,3.5,CLAY if h in [0,23] else BLUE)
        if h in [0,6,12,18,23]:
            rr=r+23;s.text(cx+rr*math.sin(a),cy-rr*math.cos(a),str(h),18)
    s.path(f'M {cx-28},{cy-r-9} Q {cx-10},{cy-r-23} {cx},{cy-r-9}',CLAY,1.4)
    s.save('2-11-cyclic','Giờ 23 và giờ 0 nằm cạnh nhau trên mã hóa tuần hoàn.')

def groups():
    s=SVG(640,300)
    for base,grouped,title in [(60,False,'Chia dòng'),(395,True,'Chia nguồn')]:
        s.text(base+82,27,title,20)
        for i in range(3):
            s.text(base-25,91+i*58,chr(65+i),20)
            for j in range(4):
                c=CLAY if (i==2 if grouped else j==3) else BLUE
                s.rect(base+j*49,73+i*58,33,33,c,c,opacity=.17)
                s.text(base+j*49+16,90+i*58,str(j+1),17)
    s.circle(239,270,4,BLUE);s.text(284,270,'Train',18)
    s.circle(362,270,4,CLAY);s.text(407,270,'Valid',18)
    s.save('8-2-groups','Chia theo nguồn giữ các đoạn của cùng tài liệu ở cùng phía.')

def partition():
    s=SVG(640,230)
    s.rect(41,54,225,101,'none',BLUE,opacity=.06);s.rect(329,54,268,101,'none',CLAY,opacity=.06)
    for i in range(8):
        x=62+i*74;c=BLUE if i<3 else (SAND if i==3 else CLAY)
        s.circle(x,102,5,c);s.text(x,139,i,18)
    s.line(284,44,284,169,SAND,.9,dash='4 5')
    s.text(62,197,'A',22);s.text(506,197,'B',22)
    s.save('8-3-partition','Đường phân chia nằm giữa hai mốc A tại 0 và B tại 6.')

def mismatch():
    s=SVG(640,235)
    s.text(154,28,'Public',21);s.text(481,28,'Judge',21)  # lượt 7: trước 'Local'
    for base,seq in [(51,['B','A']),(383,['A','B'])]:
        for j,t in enumerate(seq):
            s.text(base+21,91+j*78,j+1,18);s.node(base+102,91+j*78,t,27,BLUE if j==0 else LINE,24)
    s.arrow(245,125,345,125,CLAY)
    s.save('8-3-mismatch','Đổi evaluator có thể đảo thứ hạng của hai phương án.')

def reproduce():
    s=SVG(640,285)
    s.matrix(45,91,[['x₁','x₂'],['x₃','x₄']],38,BLUE,fs=18);s.text(83,34,'X',23)
    for x,t in [(255,'fθ'),(550,'fθ')]:s.node(x,130,t,28,BLUE,22)
    s.arrow(140,130,214,130);s.arrow(296,130,350,130)
    s.rect(373,82,80,96,LINE,radius=3);s.text(413,130,'θ',24)
    s.arrow(468,130,510,130)
    s.text(255,227,'fit',19);s.text(550,227,'predict',19)
    s.save('8-5-reproduce','Khôi phục cùng tham số và preprocessing để tái tạo dự đoán.')

def rl():
    s=SVG(640,315);s.node(99,139,'π',32,BLUE,26)
    s.matrix(409,64,[['']*4 for _ in range(3)],40,BLUE,{(2,0):CLAY},labels=False)
    s.arrow(140,139,377,139,BLUE);s.text(258,104,'aₜ',23)
    s.path('M 491,208 L 491,264 L 99,264 L 99,181',CLAY,1.4);s.arrow(99,200,99,181,CLAY)
    s.text(291,297,'sₜ₊₁, rₜ₊₁',23)
    s.save('9-1-loop','Policy chọn hành động rồi nhận trạng thái mới và phần thưởng.')

def grid():
    s=SVG(640,370);vals=[['6.200','8.000','10.000','G'],['4.580','', '8.000','10.000'],['3.122','4.580','6.200','8.000']]
    x0=119;y0=45;w=101;h=93
    for i,row in enumerate(vals):
        for j,v in enumerate(row):
            x=x0+j*w;y=y0+i*h
            s.rect(x,y,w,h,LINE,LINE if (i,j)==(1,1) else 'none',opacity=.18)
            if (i,j)==(1,1):
                for d in range(0,100,14):s.line(x+d,y+12,x+min(d+40,94),y+79,LINE,.8)
            else:
                s.text(x+w/2,y+28,v,18)
                if (i,j)!=(0,3):
                    if i==2 and j<3:s.arrow(x+27,y+69,x+75,y+69,CLAY)
                    elif j==3:s.arrow(x+50,y+79,x+50,y+53,CLAY)
                    elif i==0:s.arrow(x+27,y+69,x+75,y+69,CLAY)
                    elif (i,j)==(1,0):s.arrow(x+50,y+79,x+50,y+53,CLAY)
                    elif (i,j)==(1,2):s.arrow(x+27,y+69,x+75,y+69,CLAY)
    s.save('9-1-grid','Giá trị V* của từng ô và hành động tối ưu trong grid world.')

def search():
    s=SVG(640,325);pts={'S':(68,163),'A':(318,61),'B':(318,264),'G':(567,163)}
    for a,b,c,col in [('S','A','2',BLUE),('A','G','2',BLUE),('S','B','1',LINE),('B','G','10',LINE)]:
        p=pts[a];q=pts[b];dx=q[0]-p[0];dy=q[1]-p[1];d=math.hypot(dx,dy)
        s.arrow(p[0]+30*dx/d,p[1]+30*dy/d,q[0]-30*dx/d,q[1]-30*dy/d,col)
        s.text((p[0]+q[0])/2,(p[1]+q[1])/2+(-22 if a=='A' or b=='A' else 22),c,20)
    for t,(x,y) in pts.items():s.node(x,y,t,24,BLUE if t!='B' else LINE,23)
    s.save('9-2-search','Đường S–A–G có chi phí 4, ngắn hơn đường S–B–G có chi phí 11.')

def frontier():
    s=SVG(640,280)
    for x,t in [(99,'Đỉnh'),(240,'g'),(380,'h'),(522,'g+h')]:s.text(x,29,t,20)
    for y,row,c in [(97,['A','2','2','4'],BLUE),(206,['B','1','10','11'],LINE)]:
        s.rect(43,y-37,547,74,c,c,opacity=.07)
        for x,t in zip([99,240,380,522],row):s.text(x,y,t,23)
    s.save('9-2-astar-frontier','A* lấy A trước B vì ưu tiên g+h chứ không chỉ g.')

def minimax():
    s=SVG(640,320);s.text(320,28,'MAX',19);s.node(320,80,'3',24,BLUE,23)
    for x,v,col in [(159,'3',BLUE),(481,'2',LINE)]:
        s.arrow(303 if x==159 else 337,99,x+13 if x==159 else x-13,157,col)
        s.node(x,179,v,22,col,22);s.text(x,137,'MIN',18)
    for x,y,v,col in [(83,289,'3',BLUE),(235,289,'5',LINE),(405,289,'2',CLAY),(557,289,'9',LINE)]:
        p=159 if x<320 else 481;s.arrow(p-10 if x<p else p+10,202,x+7 if x<p else x-7,260,col)
        s.node(x,y,v,21,col,22)
    s.save('9-2-minimax','MIN chọn giá trị nhỏ hơn ở mỗi nhánh, MAX chọn nhánh có giá trị lớn hơn.')

def constraints():
    s=SVG(640,205)
    for x,k,v,c in [(83,'A','0',BLUE),(320,'B','1',CLAY),(557,'C','0',BLUE)]:s.text(x,28,k,22);s.node(x,115,v,32,c,25)
    s.line(125,115,278,115);s.text(201,81,'≠',25)
    s.line(362,115,515,115);s.text(438,81,'≠',25)
    s.save('9-2-constraints','A khác B và B khác C, nhưng A có thể bằng C.')

def bayes():
    s=SVG(640,335);s.node(69,149,'1000',38,BLUE,20)
    for y,v,p,out,col in [(68,'20','2%','18',BLUE),(237,'980','98%','98',CLAY)]:
        s.node(320,y,v,32,col,23);s.node(562,y,out,29,col,23)
        s.arrow(110,133 if y==68 else 165,280,y,col);s.text(193,82 if y==68 else 247,p,20)
        s.arrow(363,y,523,y,col);s.text(444,y-31,'90%' if y==68 else '10%',20)
    s.text(320,310,'P = 18 / (18 + 98) ≈ 15.5%',23)
    s.save('9-3-bayes','Số cảnh báo thật và cảnh báo nhầm cùng quyết định precision.')

def alerts():
    s=SVG(640,270)
    for i in range(116):
        row,col=divmod(i,20);c=BLUE if i<18 else CLAY;s.rect(134+col*18,58+row*18,13,13,c,c,opacity=.32)
    s.circle(181,210,4,BLUE);s.text(239,210,'18 đúng',19)
    s.circle(363,210,4,CLAY);s.text(428,210,'98 nhầm',19)
    s.save('9-3-confusion-metrics','Trong 116 cảnh báo, chỉ 18 là dương tính thật.')

def gradient():
    s=SVG(640,330)
    for x,k,v,c in [(90,'x','(1, 2)',BLUE),(305,'z','0',BLUE),(520,'p','0.5',CLAY)]:s.text(x,26,k,23);s.node(x,97,v,31,c,21)
    s.arrow(130,97,265,97);s.text(198,67,'w·x+b',18);s.arrow(345,97,480,97);s.text(409,67,'σ',22)
    s.node(520,259,'−0.5',31,CLAY,20);s.text(520,309,'∂L/∂z',20)
    s.path('M 555,109 C 612,160 612,212 555,247',CLAY)
    s.arrow(480,259,180,259,CLAY);s.text(320,221,'× x',22)
    s.text(90,259,'(−0.5, −1)',21);s.text(90,309,'∇wL',20)
    s.save('9-3-gradient','Với y=1, BCE cho gradient logit p−y rồi nhân với từng feature.')

def squared():
    s=SVG(640,290)
    for x,side,label,value,col in [(80,16,'1','1',BLUE),(260,32,'2','4',BLUE),(436,160,'10','100',CLAY)]:
        s.text(x+side/2,28,'|r| = '+label,20)
        s.rect(x,220-side,side,side,col,col,opacity=.12)
        s.text(x+side/2,259,value,22)
    s.save('3-3-loss-metrics','Bình phương phần dư biến độ dài 1, 2, 10 thành diện tích 1, 4, 100.')

def pr():
    s=SVG(640,345);x=116;y=291;w=442;h=215
    s.rect(x,y-h,w/2,h,'none',BLUE,opacity=.09)
    s.rect(x+w/2,y-h*2/3,w/2,h*2/3,'none',CLAY,opacity=.09)
    s.line(x,y,x+w,y);s.line(x,y,x,y-h-13)
    s.path(f'M {x},{y-h} H {x+w/2} V {y-h*2/3} H {x+w}',BLUE,1.5)
    for xx,t in [(x,'0'),(x+w/2,'0.5'),(x+w,'1')]:s.text(xx,y+26,t,18)
    s.text(x-29,y-h,'1',18);s.text(x-36,y-h*2/3,'2/3',18)
    s.text(x+w/4,y-h/2,'1/2',23);s.text(x+w*3/4,y-h/3,'1/3',23)
    s.text(61,36,'P',22);s.text(602,291,'R',22)
    s.save('5-5-pr','Diện tích dưới đường precision nội suy là 1/2 + 1/3 = 5/6.')

def ranking():
    s=SVG(640,325)
    for y,label,values in [(82,'A',[.6,.8]),(239,'B',[.4,.95,.95])]:
        s.text(49,y,label,24)
        for j,v in enumerate(values):
            x=129+j*117;s.node(x,y,str(v),27,BLUE if label=='A' else CLAY,20)
            if j<len(values)-1:s.arrow(x+34,y,x+83,y)
        s.text(552,y,'0.48' if label=='A' else '0.361',23)
        s.text(552,y+43,'√0.48 ≈ 0.693' if label=='A' else '∛0.361 ≈ 0.712',19)
    s.save('4-5-ranking','Xác suất chuỗi nhân các bước; chuẩn hóa độ dài đổi cách so sánh hai ứng viên.')

for f in [clock,groups,partition,mismatch,reproduce,rl,grid,search,frontier,minimax,constraints,bayes,alerts,gradient,squared,pr,ranking]:f()
