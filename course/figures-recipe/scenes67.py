import numpy as np,math
from svg import SVG,BLUE,CLAY,SAND,LINE,INK
from scenes34 import pooling,attention
from scenes5 import stripe,experiment

def tokens():
    s=SVG(640,330)
    for y,label,items in [(62,'Âm tiết',['học','sinh','học','máy']),(172,'Từ',['học sinh','học máy']),(282,'BPE',['lo','w','e','r'])]:
        s.text(77,y if y!=282 else y-10,label,19,anchor='end')
        w=110 if len(items)==4 else 235
        for i,t in enumerate(items):s.rect(120+i*(w+12),y-25,w,50,BLUE if y!=172 else CLAY,radius=4);s.text(120+i*(w+12)+w/2,y,t,19)
    # Lượt 7: chữ 'lower' trước đây lơ lửng giữa hàng Từ và hàng BPE; nay ghi ngay dưới nhãn BPE.
    s.text(77,294,'từ lower',14,anchor='end')
    s.save('6-1-token-levels','Token có thể là âm tiết, từ hoặc mảnh subword.')

def tfidf():
    s=SVG(640,295)
    docs=['học máy','máy học','học sinh'];counts=np.array([[1,1,0],[1,1,0],[1,0,1]])
    idf=np.log(4/(counts.astype(bool).sum(axis=0)+1))+1;v=counts*idf;v=v/np.linalg.norm(v,axis=1,keepdims=True)
    s.text(110,30,'Text',21);s.text(410,30,'TF-IDF',21)
    for i,t in enumerate(docs):s.text(107,104+i*49,t,20)
    for j,t in enumerate(['học','máy','sinh']):s.text(343+j*65,67,t,18)
    s.matrix(311,83,[[f'{z:.2f}' for z in row] for row in v],65,BLUE,fs=18)
    s.arrow(193,157,280,157)
    s.save('6-1-text-pipeline','Văn bản trở thành vector TF-IDF theo vocabulary đã fit.')

def heads():
    s=SVG(640,370)
    s.text(120,27,'H',22);s.matrix(60,72,[['h₀₁','h₀₂'],['h₁₁','h₁₂'],['h₂₁','h₂₂'],['h₃₁','h₃₂']],57,BLUE,{(0,0):CLAY,(0,1):CLAY},fs=19)
    s.text(50,100,'CLS',16,anchor='end')
    s.path('M 195,99 C 274,99 280,80 367,80',CLAY);s.arrow(352,80,367,80,CLAY)
    s.path('M 195,186 C 274,186 280,252 367,252',BLUE);s.arrow(352,252,367,252,BLUE)
    s.matrix(399,51,[['y₀','y₁','…']],44,CLAY,fs=21);s.text(465,115,'(B, C)',20)
    s.matrix(422,168,[['']*2 for _ in range(4)],34,BLUE,{(i,j):BLUE for i in range(4)for j in range(2)},labels=False);s.text(456,342,'(B, L, C)',20)
    s.save('6-3-two-heads','Head câu lấy CLS; head token tạo logits tại từng vị trí.')

def ner():
    s=SVG(640,315);tokens=['CLS','An','đến','Hà','##Nội','sớm','SEP'];wid=['—','0','1','2','2','3','—'];lab=['−100','B-PER','O','B-LOC','−100','O','−100']
    for y,title,values in [(67,'Token',tokens),(162,'word_id',wid),(257,'Label',lab)]:
        s.text(76,y,title,17,anchor='end')
        for i,t in enumerate(values):
            c=LINE if i in [0,4,6] else (CLAY if i==3 else BLUE)
            s.rect(102+i*72,y-26,64,52,c,c,opacity=.08)
            s.text(134+i*72,y,t,16 if y==257 else 18)
    s.path('M 322,103 L 322,115 L 454,115 L 454,103',CLAY)
    s.save('6-3-ner-alignment','Hà và ##Nội cùng word_id; nhãn chỉ gắn vào subword đầu.')

def shift(name='6-4-causal-shift',xs=None,ys=None):
    xs=xs or ['BOS','em','học','toán'];ys=ys or ['em','học','toán','EOS'];n=len(xs)
    s=SVG(640,270);cell=95;start=(640-n*cell)/2
    for j,(a,b) in enumerate(zip(xs,ys)):
        x=start+j*cell;s.rect(x,52,75,48,BLUE);s.text(x+37,76,a,20)
        s.rect(x,186,75,48,CLAY);s.text(x+37,210,b,20)
        s.arrow(x+37,113,x+37,170,CLAY)
    s.text(37,76,'x',22);s.text(37,210,'y',22)
    s.save(name,'Target dịch một token so với input được đưa vào decoder.')

def greedy():
    s=SVG(640,340);s.node(55,169,'S',22,BLUE,22)
    for y,letter,p,p_end,result,col in [(78,'A','0.6','0.5','0.30',CLAY),(263,'B','0.4','0.95','0.38',BLUE)]:  # lượt 7: bỏ dạng '.60'
        s.node(270,y,letter,23,col,22);s.node(486,y,'EOS',31,col,18)
        s.arrow(83,154 if y==78 else 184,237,y,col);s.text(153,75 if y==78 else 263,p,19)
        s.arrow(307,y,445,y,col);s.text(375,y-29,p_end,19)
        s.text(587,y,result,23,color=col)
    s.save('6-4-greedy-paths','Greedy chọn A ở bước đầu, nhưng xác suất cả chuỗi B–EOS cao hơn.')

def encoder_decoder():
    s=SVG(640,350)
    for j,t in enumerate(['x₁','x₂','x₃']):s.node(145+j*178,58,t,20,BLUE,20)
    s.path('M 110,91 L 110,124 L 535,124 L 535,91',BLUE)
    s.text(320,158,'Encoder · H',21)
    for j,t in enumerate(['y₁','y₂','y₃']):
        x=145+j*178;s.node(x,272,t,20,CLAY,20);s.arrow(x,184,x,240,BLUE)
        if j<2:s.arrow(x+29,272,x+147,272,CLAY)
    s.text(320,330,'Decoder',21)
    s.save('6-5-encoder-decoder','Decoder đọc memory nguồn và các token đích đã có.')

def extraction():
    s=SVG(640,235)
    s.text(128,56,'Lan · 08:30',22)
    s.arrow(249,113,357,113)
    s.text(466,76,'name: Lan',21);s.text(466,151,'time: 08:30',21)
    s.path('M 390,50 L 373,50 L 373,177 L 390,177',LINE)
    s.path('M 548,50 L 565,50 L 565,177 L 548,177',LINE)
    s.save('6-6-llm-pipeline','Trích thông tin trong văn bản vào các trường schema.')

def cache():
    s=SVG(640,300)
    for x,title in [(67,'K'),(380,'V')]:
        s.text(x+95,27,title,23)
        s.matrix(x,68,[['']*6 for _ in range(4)],31,BLUE,{(i,j):BLUE for i in range(4)for j in range(5)},labels=False)
        s.rect(x+5*31,68,31,124,CLAY,CLAY,opacity=.12)
        s.path(f'M {x},214 L {x},224 L {x+5*31},224 L {x+5*31},214',BLUE)
        s.text(x+77,250,'L',21);s.text(x+170,250,'+1',21,color=CLAY)
    s.save('6-6-memory-budget','Mỗi token mới thêm một vị trí vào cả key cache và value cache.')

def wave(s,x,y,w=150,h=56):
    pts=[]
    for t in np.linspace(0,1,90):pts.append((x+t*w,y+math.sin(8*math.pi*t)*h/2))
    s.path('M '+' L '.join(f'{a:g},{b:g}' for a,b in pts),BLUE,1.25)

def audio_task():
    s=SVG(640,310);wave(s,26,151,140,63)
    s.path('M 185,151 C 258,151 271,65 352,65',BLUE);s.arrow(336,65,352,65)
    s.path('M 185,151 C 258,151 271,238 352,238',CLAY);s.arrow(336,238,352,238,CLAY)
    s.node(489,65,'y',32,BLUE,25)
    s.matrix(391,213,[['y₁','y₂','y₃','…']],45,CLAY,fs=21)
    s.save('7-2-task','Một nhãn cho cả clip hoặc một dãy nhãn theo thời gian.')

def asr():
    s=SVG(640,320);wave(s,22,156,118,54)
    s.path('M 161,156 C 196,156 229,61 266,61',BLUE);s.arrow(254,61,266,61)
    s.path('M 161,156 C 196,156 210,257 241,257',CLAY);s.arrow(229,257,241,257,CLAY)
    s.text(333,32,'CTC',21);s.matrix(281,50,[['a','—','a']],37,BLUE,fs=21);s.arrow(417,68,499,68)
    s.text(555,68,'aa',24)
    s.text(407,191,'Encoder–decoder',21)  # lượt 7: trước là 'Autoregressive'
    for j,t in enumerate(['BOS','y₁','y₂']):
        x=278+j*115;s.node(x,258,t,27,CLAY,17)
        if j<2:s.arrow(x+34,258,x+81,258,CLAY)
    s.save('7-3-asr','CTC gộp nhãn frame; decoder sinh token lần lượt.')

def ctc():
    s=SVG(640,335)
    for j,probs in enumerate([(.6,.4),(.5,.5),(.4,.6)]):
        x=71+j*166;s.text(x,27,f't{j+1}',20)
        for y,t,p in [(101,'_',probs[0]),(235,'a',probs[1])]:
            s.node(x,y,t,22,BLUE if t=='a' else LINE,20);s.text(x,62 if t=='_' else 283,f'{p:.1f}',17)
        if j<2:
            for y1 in [101,235]:
                for y2 in [101,235]:s.line(x+26,y1,x+140,y2,LINE,.8)
    s.arrow(444,168,476,168)
    for y,t,p in [(78,'""','0.12'),(170,'a','0.76'),(263,'aa','0.12')]:s.text(520,y,t,22);s.text(591,y,p,20)
    s.save('7-3-ctc','Tám path theo frame được gộp thành ba transcript.')

def wer():
    s=SVG(640,270);gold=['em','học','ai','hôm','nay'];pred=['em','học','toán','—','nay']
    # Lượt 7: nhãn hàng viết tiếng Việt (trước là 'Gold'/'Pred'); dời lưới sang phải để đủ chỗ.
    for y,label,row in [(69,'Tham chiếu',gold),(177,'Dự đoán',pred)]:
        s.text(112,y,label,17,anchor='end')
        for j,t in enumerate(row):
            x=124+j*100;c=CLAY if j in [2,3] else BLUE
            s.rect(x,y-27,80,54,c,c,opacity=.08);s.text(x+40,y,t,21)
    for j in range(5):s.line(164+j*100,102,164+j*100,141,CLAY if j in [2,3] else LINE)
    s.text(364,248,'WER = (1 + 1) / 5 = 0.4',22)
    s.save('7-3-wer','Một từ thay thế và một từ bị xóa trên năm từ reference.')

def fusion():
    s=SVG(640,345)
    s.text(115,28,'Early',21);s.text(487,28,'Late',21)
    s.matrix(53,63,[['zᵢ₁','zᵢ₂']],40,BLUE,fs=18);s.matrix(53,157,[['zₜ₁','zₜ₂']],40,CLAY,fs=18)
    s.path('M 153,83 L 200,119 L 221,119',BLUE);s.path('M 153,177 L 200,119',CLAY)
    s.matrix(238,46,[['zᵢ₁'],['zᵢ₂'],['zₜ₁'],['zₜ₂']],40,BLUE,{(i,0):BLUE if i<2 else CLAY for i in range(4)},fs=18)
    s.matrix(422,57,[['p₀','p₁']],40,BLUE,fs=20);s.matrix(422,152,[['q₀','q₁']],40,CLAY,fs=20)
    s.path('M 512,77 C 559,77 559,164 559,203',BLUE);s.arrow(559,190,559,203,BLUE)
    s.path('M 512,172 C 529,181 533,200 540,213',CLAY);s.arrow(534,201,540,213,CLAY)
    s.node(559,230,'+',20,BLUE,23)
    s.arrow(559,260,559,283);s.text(600,275,'÷ 2',18)
    s.text(537,319,'½(p + q)',23)
    s.save('7-4-fusion','Early ghép feature vectors; late ghép xác suất cùng lớp.')

def vlm():
    s=SVG(640,340)
    s.image(30,64,75,75,stripe(False,8),hi=1);s.text(68,27,'Ảnh',20)
    for j in range(4):s.rect(160+j*34,76,26,39,BLUE,BLUE,opacity=.09)
    s.arrow(119,100,144,100,BLUE)
    s.text(242,165,'Visual tokens',18)  # lượt 7: thống nhất với bài (trước 'Image tokens')
    for j,t in enumerate(['Vật','gì','?']):s.rect(162+j*68,219,58,42,CLAY);s.text(191+j*68,240,t,18)
    s.path('M 311,101 C 388,101 398,161 446,161',BLUE);s.arrow(433,159,446,161,BLUE)
    s.path('M 381,241 C 405,241 410,203 446,198',CLAY);s.arrow(432,200,446,198,CLAY)
    s.node(489,178,'LM',29,BLUE,22);s.arrow(530,178,585,178);s.text(608,178,'y',21)
    s.save('7-4-vlm','Các vector ảnh và token câu hỏi cùng đi vào language model.')

def ablation():
    s=SVG(640,345);p=[.90,.80,.40,.30,.10,.20,.60,.70];q=[.40,.35,.85,.90,.55,.65,.25,.20]
    for y,i in zip([74,139,204,269],[0,2,6,4]):
        xa=115+440*p[i];xb=115+440*q[i];xm=(xa+xb)/2
        s.line(115,y,555,y,LINE,.7);s.line(xa,y,xb,y,LINE,1.4)
        s.circle(xa,y,5,BLUE);s.circle(xb,y,5,CLAY);s.circle(xm,y,5,INK)
        s.text(65,y,'y = 1' if i<4 else 'y = 0',18)
    s.line(335,48,335,290,LINE,1,dash='4 5')
    for x,t in [(115,'0'),(335,'0.5'),(555,'1')]:s.text(x,320,t,18)
    s.circle(168,23,4,BLUE);s.text(204,23,'Ảnh',17)
    s.circle(278,23,4,CLAY);s.text(313,23,'Chữ',17)
    s.circle(389,23,4,INK);s.text(448,23,'Trung bình',17)  # lượt 7: trước 'Mean'
    s.save('7-4-ablation','Ghép đúng cặp xác suất giúp hai nguồn bù những lỗi khác nhau.')

for f in [tokens,tfidf,heads,ner,shift,greedy,encoder_decoder,extraction,cache,audio_task,asr,ctc,wer,fusion,vlm,ablation]:f()
pooling('6-2-masked-pooling',[[2,0],[0,2],[9,9],[9,9]],[1,1,0,0])
attention('6-5-cross-attention',(.670,.330),((2,0),(0,2)),(1.340,.660))
shift('6-5-teacher-forcing',['BOS','B','A'],['B','A','EOS'])
experiment('7-kt4-loop')
