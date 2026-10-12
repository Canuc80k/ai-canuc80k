from svg import SVG,BLUE,CLAY,SAND,LINE,INK

def alias():
    s=SVG(640,280)
    s.text(155,25,'Gán',20);s.text(485,25,'Copy',20)
    for x,label in [(40,'a'),(40,'b'),(370,'a'),(370,'c')]:
        y=100 if label=='a' else 220;s.node(x,y,label,19,BLUE if label=='a' else CLAY)
    s.matrix(140,80,[[1,2,3]],42);s.arrow(62,100,127,100,BLUE);s.arrow(60,210,128,108,CLAY)
    s.matrix(470,80,[[1,2,3]],42);s.matrix(470,200,[[1,2,3]],42,CLAY)
    s.arrow(392,100,457,100,BLUE);s.arrow(392,220,457,220,CLAY)
    s.save('0-1-names','Gán hai tên vào cùng một list; copy tạo list riêng.')

def notebook():
    s=SVG(640,230)
    s.text(105,30,'n',20);s.text(500,30,'total',20)
    s.node(105,90,'3',25,BLUE);s.node(500,90,'6',25,BLUE)
    s.arrow(140,90,463,90,BLUE);s.text(305,67,'sum(range(n + 1))',18)
    s.node(105,180,'5',25,CLAY);s.node(500,180,'6',25,SAND)
    s.arrow(140,180,463,180,LINE,dash='4 5');s.text(500,220,'cũ',16)
    s.save('0-1-notebook','Đổi n mà chưa chạy lại ô tính total để lại kết quả cũ.')

def axis():
    s=SVG(640,390);values=[[9,8,7],[5,6,4],[3,4,6],[9,8,10],[8,8,9]]
    for j,label in enumerate(['Toán','Lý','Tin']):s.text(185+j*48,25,label,17)
    s.matrix(161,55,values,48)
    for i,val in enumerate(['8','5','4.33','9','8.33']):
        s.arrow(320,79+i*48,420,79+i*48,CLAY);s.text(454,79+i*48,val,20)
    s.text(493,25,'axis = 1',18)
    for j,val in enumerate(['6.8','6.8','7.2']):
        s.arrow(185+j*48,308,185+j*48,340,BLUE);s.text(185+j*48,369,val,20)
    s.text(61,369,'axis = 0',18)
    s.save('0-2-axis','Trung bình theo hàng và theo cột của cùng ma trận.')

def broadcast():
    s=SVG(640,330)
    s.text(66,25,'(4, 1)',18);s.text(255,25,'(3,)',18);s.text(487,25,'(4, 3)',18)
    s.matrix(45,80,[[0],[10],[20],[30]],42,CLAY)
    s.text(145,160,'+',30);s.matrix(193,80,[[1,2,3]],42,BLUE)
    s.text(358,160,'=',30);s.matrix(422,80,[[1,2,3],[11,12,13],[21,22,23],[31,32,33]],42)
    s.path('M 89,103 L 132,103 M 89,145 L 132,145 M 89,187 L 132,187 M 89,229 L 132,229',CLAY,1,dash='3 4')
    for j in range(3):s.arrow(214+j*42,130,214+j*42,206,BLUE,dash='3 4')
    s.save('0-2-broadcast','Một cột cộng một hàng được broadcast thành ma trận 4 × 3.')

def shape():
    s=SVG(640,365)
    s.text(100,25,'ŷ: (3, 1)',19);s.text(310,25,'y: (3,)',19)
    s.matrix(79,70,[[1],[2],[3]],42,CLAY);s.text(192,130,'−',30)
    s.matrix(247,70,[[1,2,3]],42,BLUE);s.arrow(418,130,475,130)
    s.matrix(493,70,[[0,-1,-2],[1,0,-1],[2,1,0]],42,CLAY)
    s.text(552,230,'(3, 3)',19);s.text(552,276,'MSE = 1.333',19,color=CLAY)
    s.line(35,313,605,313,LINE)
    s.text(320,342,'(3,) − (3,)  →  (3,)     MSE = 0',20,color=BLUE)
    s.save('0-2-shape-mismatch','Sai shape tạo chín hiệu thay vì ba phần dư cần tính.')

def view():
    s=SVG(640,285);s.text(55,60,'a',20)
    s.matrix(97,40,[[0,1,2,3,4,5]],60,BLUE,{(0,j):CLAY for j in [1,2,3]})
    s.path('M 158,120 L 158,132 L 336,132 L 336,120',CLAY)
    s.text(247,165,'a[1:4] · view',19)
    s.matrix(378,207,[[1,2,3]],48,BLUE);s.text(218,231,'a[[1, 2, 3]] · copy',19)
    s.arrow(298,213,362,230,BLUE)
    s.save('0-2-view','Slice chia sẻ bộ nhớ; advanced indexing tạo bản sao.')

def groupby():
    s=SVG(640,365)
    s.text(115,25,'Dữ liệu',20);s.text(345,25,'mean',20);s.text(535,25,'transform',20)
    rows=[['10A4','6.72'],['10A3','6.84'],['10A3','4.79']]
    s.matrix(35,80,rows,68,BLUE,fs=17);s.text(105,324,'400 dòng',18)
    s.matrix(270,60,[['10A1','6.79'],['10A2','6.41'],['10A3','5.96'],['10A4','6.58']],62,CLAY,fs=17)
    s.text(331,324,'4 nhóm',18)
    s.matrix(497,80,[['6.58'],['5.96'],['5.96']],68,BLUE,fs=19);s.text(534,324,'400 dòng',18)
    s.arrow(180,181,252,181,CLAY);s.arrow(405,181,477,181,BLUE)
    s.save('0-3-groupby','Mean thu về từng nhóm; transform trả lại từng dòng.')

def merge():
    s=SVG(640,380)
    s.text(95,25,'Học sinh',20);s.text(320,25,'Lớp',20);s.text(550,25,'left join',20)
    s.matrix(35,85,[[1,'A'],[2,'A'],[3,'B']],52,BLUE)
    s.matrix(260,85,[['A',38],['A',38],['B',42]],52,CLAY)
    s.matrix(468,59,[[1,'A',38],[1,'A',38],[2,'A',38],[2,'A',38],[3,'B',42]],50,BLUE,fs=17)
    s.arrow(159,160,234,160);s.arrow(383,160,444,160)
    s.text(94,313,'3 dòng',18);s.text(318,313,'A lặp',18);s.text(543,337,'5 dòng',18)
    s.save('0-3-merge','Khóa A lặp trong bảng lớp làm left join tăng số dòng.')

def submission():
    s=SVG(640,265);s.text(160,25,'Thứ tự dự đoán',20);s.text(485,25,'Thứ tự ID',20)
    left=[['403','6.414'],['401','5.964'],['402','6.579']];right=[['401','5.964'],['402','6.579'],['403','6.414']]
    s.matrix(60,65,left,64,BLUE,fs=17);s.matrix(405,65,right,64,CLAY,fs=17)
    for i,j,col in [(0,2,SAND),(1,0,BLUE),(2,1,CLAY)]:
        y1=97+i*64;y2=97+j*64;s.path(f'M 199,{y1} C 290,{y1} 313,{y2} 393,{y2}',col)
        s.arrow(386,y2,399,y2,col)
    s.save('0-3-submission','Ghép dự đoán bằng ID thay vì vị trí trong bảng.')

def timeline():
    s=SVG(640,185)
    for x,w,label,n,col in [(50,352,'Train',80,BLUE),(402,88,'Valid',20,CLAY),(490,88,'Test',20,SAND)]:
        s.rect(x,55,w,55,col,col,opacity=.12);s.text(x+w/2,83,label,18);s.text(x+w/2,125,n,18)
    s.arrow(50,155,594,155)
    for x,t in [(50,0),(402,80),(490,100),(578,120)]:s.text(x,174,t,15)
    s.save('1-1-timeline','Tách train, validation và test theo thứ tự thời gian.')

def contract():
    s=SVG(640,310)
    s.matrix(35,78,[['x₁₁','x₁₂'],['x₂₁','x₂₂'],['x₃₁','x₃₂']],42,BLUE,fs=17);s.text(77,37,'X',22)
    s.rect(262,81,116,82,LINE,BLUE,5,.06);s.text(320,122,'fθ',26)
    s.matrix(515,82,[['ŷ₁'],['ŷ₂'],['ŷ₃']],42,CLAY);s.text(536,37,'ŷ',22)
    s.arrow(131,121,242,121,BLUE);s.arrow(398,121,495,121,CLAY)
    s.matrix(280,227,[['y₁','y₂','y₃']],38,BLUE);s.text(253,247,'y',22)
    s.path('M 337,213 L 337,188',BLUE);s.arrow(337,194,337,174,BLUE)
    s.save('1-1-contract','Dữ liệu X tạo dự đoán ŷ; nhãn y dùng để học tham số.')

def tasks():
    s=SVG(640,280)
    for x,label in [(105,'Classification'),(320,'Regression'),(535,'Clustering')]:s.text(x,27,label,18)
    # Regions, a fitted line and unlabeled clusters encode different outputs.
    s.rect(35,76,140,145,LINE);s.rect(35,76,70,145,'none',BLUE,opacity=.08);s.rect(105,76,70,145,'none',CLAY,opacity=.08)
    for x,y,c in [(61,107,BLUE),(68,150,BLUE),(140,173,CLAY),(143,98,CLAY)]:s.circle(x,y,5,c)
    s.text(70,251,'0',20);s.text(140,251,'1',20)
    s.line(250,217,391,76,BLUE,1.6)
    for x,y in [(273,196),(317,145),(369,111)]:s.circle(x,y,5,CLAY)
    s.text(320,251,'ŷ ∈ ℝ',20)
    for cx,cy,c in [(502,111,BLUE),(568,185,CLAY)]:
        s.circle(cx,cy,38,c,'none',opacity=.5)
        for dx,dy in [(-10,-11),(15,-6),(-3,13)]:s.circle(cx+dx,cy+dy,5,c)
    s.text(535,251,'Không có y',18)
    s.save('1-1-task-types','Ba loại bài toán khác nhau ở dạng đầu ra và sự có mặt của nhãn.')

def oof():
    s=SVG(640,350)
    starts=[100,280,460]
    for x,label in zip(starts,['0–31','32–63','64–95']):s.text(x+70,28,label,18)
    for i in range(3):
        s.text(65,87+i*63,f'Fold {i+1}',17,anchor='end')
        for j,x in enumerate(starts):
            c=CLAY if i==j else BLUE;s.rect(x,61+i*63,140,48,c,c,opacity=.10)
            s.text(x+70,85+i*63,'valid' if i==j else 'train',18)
    for j,x in enumerate(starts):s.arrow(x+70,238,x+70,275,CLAY)
    for j,x in enumerate(starts):s.rect(x,283,140,42,CLAY,CLAY,opacity=.12)
    s.text(63,304,'OOF',18,anchor='end');s.text(350,342,'96 dự đoán',18)
    s.save('1-3-oof-mapping','Mỗi mẫu nhận một dự đoán từ fold không dùng mẫu đó để fit.')

def pipeline(leak=False,name='1-4-pipeline'):
    s=SVG(640,300)
    for y,label,values in [(80,'Train',[[2,4],[3,6]]),(233,'Valid',[[2.5,5],[3.5,7]])]:s.text(48,y,label,18);s.matrix(99,y-29,values,29,BLUE,fs=15)
    s.rect(288,48,95,66,CLAY,CLAY,5,.08);s.text(335,82,'μ, σ',25)
    s.arrow(173,80,267,80,BLUE);s.text(223,56,'fit',17)
    s.rect(288,204,95,66,CLAY,CLAY,5,.08);s.text(335,237,'μ, σ',25)
    s.arrow(335,126,335,192,CLAY)
    s.arrow(174,233,269,233,BLUE);s.text(223,209,'transform',15)
    s.arrow(399,82,469,82);s.arrow(399,237,469,237)
    s.matrix(490,52,[[-1,-1],[1,1]],29,BLUE,fs=15);s.matrix(490,208,[[0,0],[2,2]],29,BLUE,fs=15)
    if leak:
        s.path('M 165,210 C 203,161 247,135 286,99',CLAY,1.7);s.text(224,155,'✕',25,color=CLAY)
    s.save(name,'Validation dùng thống kê đã học từ train.' if not leak else 'Đưa validation vào bước fit làm rò rỉ dữ liệu.')

def ranking():
    s=SVG(640,290)
    for y,tokens in [(85,['A','B','C']),(207,['C','E','B'])]:
        for j,t in enumerate(tokens):
            c=BLUE if t in {'A','C','E'} else LINE;s.rect(70+j*110,y-29,67,57,c,c,opacity=.10);s.text(103+j*110,y,t,22)
        s.arrow(386,y,431,y);s.text(526,y,'AP = 5/9' if y==85 else 'AP = 2/3',21)
    s.text(103,37,'1/1',17,color=BLUE);s.text(323,37,'2/3',17,color=BLUE)
    s.text(103,157,'1/1',17,color=BLUE);s.text(213,157,'2/2',17,color=BLUE)
    s.save('1-6-ranking','Cùng hai kết quả liên quan, thứ tự sớm hơn cho AP cao hơn.')

def workflow():
    s=SVG(640,210)
    for x,t in [(70,'Train'),(305,'Valid'),(545,'Test')]:s.node(x,96,t,36,BLUE,18)
    s.arrow(111,96,263,96);s.text(186,67,'CV',18)
    s.arrow(346,96,503,96);s.text(426,67,'chốt θ',18)
    s.rect(245,154,120,35,CLAY,CLAY,4,.08);s.text(305,171,'chọn θ',18)
    s.arrow(305,137,305,146,CLAY)
    s.save('1-7-workflow','Chọn cấu hình trên validation rồi mới chấm test riêng.')

def bootstrap():
    s=SVG(640,270)
    s.text(78,57,'Gốc',19);s.text(78,152,'Rút',19)
    s.matrix(143,30,[[0,1,2,3,4]],65,BLUE);s.matrix(143,123,[[0,0,2,3,3]],65,CLAY)
    s.text(305,226,'OOB',19);s.rect(365,200,112,51,BLUE,BLUE,3,.08);s.text(421,226,'1, 4',23)
    s.save('2-6-bootstrap','Bootstrap rút có lặp; các mẫu 1 và 4 nằm ngoài lượt rút này.')

def density():
    s=SVG(640,190)
    for x,v,c in [(100,'0',CLAY),(180,'0.1',BLUE),(260,'0.2',BLUE),(380,'0.35',CLAY),(575,'3',SAND)]:
        s.circle(x,88,6,c);s.text(x,132,v,18)
    s.path('M 60,88 A 120,65 0 1 1 300,88 A 120,65 0 1 1 60,88',BLUE,1,dash='4 5')
    s.text(180,50,'core',18);s.text(102,171,'border',18);s.text(575,171,'noise',18)
    s.save('2-10-density','Vùng ε quanh core chứa đủ ba điểm; điểm xa là noise.')

for f in [alias,notebook,axis,broadcast,shape,view,groupby,merge,submission,timeline,contract,tasks,oof,ranking,workflow,bootstrap,density]:f()
pipeline();pipeline(True,'1-4-leakage')
