from svg import SVG,BLUE,CLAY,LINE

def backprop():
    s=SVG(640,370)
    # Forward values and their local operations; no paragraphs inside cards.
    for x,label,col in [(60,'x',BLUE),(225,'h',BLUE),(390,'p',CLAY),(560,'J',CLAY)]:
        s.text(x,40,label,20);s.node(x,110,{60:'2',225:'1',390:'2',560:'4'}[x],29,col,23)
    s.arrow(92,110,193,110);s.text(142,78,'× 0.5',17)
    s.arrow(257,110,358,110);s.text(308,78,'× 2',17)
    s.arrow(422,110,528,110);s.text(475,78,'(p − 0)²',17)
    s.text(320,181,'Forward →',16,color=BLUE)
    s.text(320,225,'← Backward',16,color=CLAY)
    for x,label,val in [(60,'∂J/∂w₁','16'),(225,'∂J/∂h','8'),(390,'∂J/∂p','4')]:
        s.node(x,285,val,29,CLAY,23);s.text(x,340,label,18)
    s.arrow(358,285,257,285,CLAY);s.text(308,257,'× 2',17)
    s.arrow(193,285,92,285,CLAY);s.text(142,257,'× x',17)
    s.path('M 560,140 C 560,240 470,285 422,285',CLAY)
    s.save('3-2-hand-backprop','Một lượt forward và backprop với x = 2, y = 0.')

def convolution():
    s=SVG(640,300)
    s.text(115,35,'Ảnh X',20);s.text(330,35,'Kernel',20);s.text(540,35,'Đầu ra',20)
    vals=[[1,2,0],[0,1,3],[2,1,0]]
    s.matrix(40,75,vals,50,BLUE,highlights={(i,j):BLUE for i in range(2) for j in range(2)})
    s.text(240,140,'∗',30)
    s.matrix(280,75,[[1,0],[0,2]],50,CLAY)
    s.arrow(420,140,463,140)
    s.matrix(490,75,[[3,8],[2,1]],50,BLUE,highlights={(0,0):CLAY})
    s.text(320,263,'1·1 + 2·0 + 0·0 + 1·2 = 3',22)
    s.save('5-1-window','Cửa sổ 2 × 2 tạo phần tử đầu tiên của đầu ra.')

def masks():
    s=SVG(640,330)
    s.text(165,35,'Padding mask',20);s.text(480,35,'Causal mask',20)
    for start,mode in [(65,'padding'),(380,'causal')]:
        fill={(i,j):BLUE for i in range(4) for j in range(4) if (j<3 if mode=='padding' else j<=i)}
        s.matrix(start,85,[['' for j in range(4)]for i in range(4)],50,BLUE,fill,labels=False)
        for i,t in enumerate(['1','2','3','PAD'] if mode=='padding' else ['1','2','3','4']):
            s.text(start+(i+.5)*50,307,t,16)
            s.text(start-18,110+i*50,str(i+1),16,anchor='end')
    s.save('3-9-masks','Vùng tô màu là các key mà mỗi query được phép đọc.')

backprop();convolution();masks()
