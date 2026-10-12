"""Regenerate the reviewed vector sources. Run --apply only after visual QA."""
from pathlib import Path
import subprocess,sys,json,hashlib,xml.etree.ElementTree as ET,re,shutil
R=Path(__file__).resolve().parent;C=R.parent
EXPECTED=502  # số hình sau lượt 8; thêm hình mới thì tăng số này
PRUNED={'1-7-workflow','4-1-package','5-kt3-loop','6-6-llm-pipeline','7-kt4-loop','7-kt4-time','8-1-budget','8-5-reproduce','8-5-timeline','5-9-occlusion','2-7-boosting'}
CAP={
'0-2-speed':'Hai cách tính sigmoid cho cùng dãy đầu vào.',
'0-3-eda':'Phân bố điểm và quan hệ giữa giờ tự học với điểm.',
'0-3-bar':'Cùng trung bình, cắt trục y làm chênh lệch trông lớn hơn.',
'1-2-fits':'k nhỏ bám nhiễu; k quá lớn bỏ mất xu hướng.',
'1-2-learning':'Thêm dữ liệu làm train và validation tiến gần nhau.',
'1-3-groups':'Tách theo người giữ các mẫu cùng nguồn ở cùng phía.',
'1-3-time':'Validation nằm sau train và cách bởi một khoảng thời gian.',
'1-5-confusion':'Đối chiếu nhãn thật theo hàng với dự đoán theo cột.',
'1-5-roc':'Đổi threshold tạo các cặp FPR, TPR trên ROC.',
'1-5-threshold':'Precision và recall đổi theo threshold.',
'1-6-losses':'Lỗi bình phương tăng nhanh hơn lỗi tuyệt đối.',
'1-6-relative':'Cùng lỗi tuyệt đối, lỗi tương đối phụ thuộc độ lớn target.',
'1-7-search':'Grid search và random search phân bố lượt thử khác nhau.',
'1-7-grid-log':'F1 trên train (nét đứt) và trên CV (nét liền) theo k, cho hai kiểu weights.',
'2-1-residuals':'Phần dư giữa điểm dữ liệu và đường dự đoán.',
'2-1-projection':'Least squares chiếu y lên không gian cột của X.',
'2-1-gd1d':'Learning rate quyết định tiến gần đáy hay vượt đáy.',
'2-1-lr':'Learning rate ảnh hưởng tốc độ giảm và tính ổn định của loss.',
'2-1-scaling':'Chuẩn hóa đổi hình thung lũng và đường đi gradient descent.',
'2-1-residual-plots':'Phần dư ngẫu nhiên, uốn cong và loe dần cho các cấu trúc lỗi khác nhau.',
'2-1-loglog':'Độ dốc trên log–log biểu diễn tốc độ tăng của thời gian theo n.',
'2-2-geometry':'Vùng L1 và L2 chạm các đường đồng mức ở vị trí khác nhau.',
'2-2-path':'Hệ số Lasso thay đổi khi mức phạt tăng.',
'2-2-shrink':'Ridge co hệ số; Lasso có vùng đưa hệ số về 0.',
'2-2-validation':'Regularization ảnh hưởng khác nhau lên train và tập giữ lại.',
'2-3-boundary':'Các mức xác suất logistic tạo những đường song song.',
'2-3-linfail':'Thêm điểm xa kéo đường linear regression trên nhãn 0/1.',
'2-3-loss':'Loss và gradient của cross-entropy so với lỗi bình phương.',
'2-3-sigmoid':'Sigmoid chuyển logit thành xác suất.',
'2-3-softmax':'Softmax chuẩn hóa ba logits thành phân phối có tổng bằng 1.',
'2-3-weights':'Dấu của hệ số cho biết nét mực làm tăng hay giảm score từng lớp.',
'2-4-k':'k thay đổi độ gấp khúc của ranh giới kNN.',
'2-4-units':'Đổi đơn vị một feature làm đổi khoảng cách Euclid.',
'2-5-partition':'Các phép chia của decision tree tạo những vùng hình chữ nhật.',
'2-5-stump':'So ba ngưỡng chia trên cùng bốn mẫu.',
'2-6-variance':'Tương quan giữa các cây giới hạn mức giảm phương sai.',
'2-7-boosting':'Theo dõi train và validation khi tăng số cây.',
'2-7-early-stop':'MSE train giảm mãi; MSE validation thấp nhất ở vòng 31 rồi tăng lại.',
'2-7-fit-stages':'Tổng các cây nông dần xấp xỉ đường cong.',
'2-7-stages':'Boosting cộng các bước sửa phần dư vào dự đoán.',
'2-8-hinge':'Hinge loss bằng 0 khi signed margin ít nhất bằng 1.',
'2-8-margin':'Support vectors nằm trên hai đường lề của SVM.',
'2-9-label':'PCA có thể bỏ hướng biến thiên nhỏ nhưng mang nhãn.',
'2-9-pca':'PC1 theo hướng dữ liệu trải dài nhất; PC2 vuông góc PC1.',
'2-10-kmeans-assign':'Gán cụm rồi lấy trung bình tạo các tâm mới.',
'2-10-moons':'K-Means và DBSCAN tạo hình cụm khác nhau trên dữ liệu trăng khuyết.',
'2-11-time':'Feature tại thời điểm dự đoán chỉ lấy các giá trị đã có trong quá khứ.',
'3-2-xor':'Hai lớp XOR ở những góc đối diện không tách bằng một đường thẳng.',
'3-3-activation':'Hình dạng của ReLU, tanh và sigmoid.',
'3-3-residual-loss':'So độ phạt của MSE và MAE theo phần dư.',
'3-3-depth-scale':'Độ lệch chuẩn pre-activation qua 10 lớp ReLU (trục log): khởi tạo N(0, 0.01²) co khoảng 9 lần mỗi lớp, He giữ quanh 1.4.',
'3-5-budget':'Loss theo bước (thang log) trên J=w₁²+8w₂²: SGD giảm đều, Adam và momentum vừa giảm vừa dao động.',
'3-6-early-stop':'Validation MSE dao động mạnh, chạm một đáy hẹp ở epoch 26 rồi nhích dần lên tới epoch 160; train loss xuống dưới MSE của nhiễu và gần như đi ngang.',
'3-8-rnn-pad':'Câu “dp” dài 1: trạng thái cần đọc là h₁; cột cuối h₃ đã đi qua hai PAD.',
'3-10-errors':'Lỗi tái tạo của 48 mẫu test trên thang log; vạch đứt là ngưỡng. Nhóm bất thường nằm cách ngưỡng hơn một bậc độ lớn, hai mẫu bình thường vượt ngưỡng là hai FP.',
'3-5-paths':'Cùng η=0.09 từ (−2, 1): SGD zigzag theo w₂ rồi về đáy; momentum μ=0.8 vượt qua đáy rồi vòng lại.',
'3-5-schedule':'StepLR giảm learning rate theo các mốc epoch.',
'3-6-capacity':'Tăng độ phức tạp làm train loss và validation loss tách nhau.',
'3-9-masks':'Vùng màu là các key mà query được phép đọc.',
'3-10-reconstruction':'Điểm lệch khỏi quan hệ đã học có lỗi tái tạo lớn hơn.',
'4-2-cosine':'Chuẩn hóa giữ hướng và bỏ ảnh hưởng của độ dài vector.',
'4-3-transfer':'Learning curve thực tế khi chỉ học head và khi mở cả encoder.',
'4-3-validation':'Checkpoint head-only được chọn tại validation loss thấp nhất.',
'4-4-count':'Với lớp 6×8, LoRA học 14r tham số; từ r = 4 đã vượt 48 của full update.',
'4-5-contrastive':'Score trên đường chéo ứng với các cặp ảnh–caption đúng.',
'6-2-cosine':'Góc giữa các vector quyết định cosine similarity.',
'6-3-attention-masks':'Padding mask chặn cột PAD; causal mask chặn key tương lai.',
'6-4-temperature':'Temperature đổi độ tập trung của phân phối sampling.',
'7-1-sampling':'Các mẫu rời rạc lấy từ cùng tín hiệu liên tục.',
'7-1-spectrogram':'Tần số đổi từ 200 Hz sang 600 Hz được nhìn theo thời gian.',
'7-1-mel':'Các bộ lọc tam giác gom phổ thành các mel band.',
'7-2-order':'Đảo thứ tự thời gian giữ mean nhưng đổi cấu trúc chuỗi.',
'7-2-confusion':'CNN giữ vị trí phân biệt được hai thứ tự mà mean pooling bỏ mất.',
'7-kt4-time':'Lịch phân bổ thời gian của buổi luyện.',
'8-1-budget':'Phân bổ thời gian của buổi luyện.',
'8-5-timeline':'Các mốc thời gian trong buổi thi thử.',
'8-1-priority':'So mức tăng điểm kỳ vọng trên mỗi phút của các phương án.',
'8-2-shift':'Shortcut bị đảo làm hai cách chọn feature có kết quả khác nhau.',
'8-2-validation-slices':'Cùng một ô là một mẫu: camera mới có ít mẫu và tỉ lệ lỗi cao hơn.',
'8-4-correlation':'Các lỗi tương quan cao làm lợi ích ensemble chạm một giới hạn.',
'8-4-tune-audit':'Lưới 15 bộ trọng số; tổng trọng số của forest và kNN không quá 1, phần còn lại thuộc linear. Màu là log loss trên tune.',
'8-4-voting':'Hard voting và trung bình xác suất có thể chọn hai lớp khác nhau.',
'9-3-attention':'Causal mask đưa trọng số của key tương lai về 0.',
'4-1-flow':'Một mẫu đi qua ba phần của gói: processor, trọng số trong state_dict, rồi bảng nhãn.',
'4-kt2-regions':'Ba vùng quyết định của head đặt tay. Mẫu (1.5, 0) có nhãn 1 (vòng rỗng) nằm trong vùng của lớp 0.',
'5-kt3-threshold':'Hàng trên: tám xác suất validation, chấm đặc là ảnh dương. Hàng dưới: accuracy và F1 theo threshold. Tại 0.5 và 0.65 accuracy cùng 0.875, còn F1 là 0.857 và 0.8.',
'5-9-occlusion-scores':'Che góc kéo xác suất lớp 1 của A xuống; che nét kéo xác suất của B xuống.',
'5-2-depth':'Loss train theo bước của bốn mạng 18 lớp: không BatchNorm, plain kẹt ở ln 2 còn residual học nhưng có lúc vọt lên; có BatchNorm, residual hội tụ nhanh hơn plain.',
'5-3-digit-aug':'Dời một pixel vẫn là chữ 2; lật ngang tạo một hình không còn là chữ 2 nhưng vẫn mang nhãn 2.',
'5-7-neighbors':'Tỉ lệ ảnh cùng hình trong 5 láng giềng cosine của mỗi ảnh test, tách theo lớp. Contrastive cao nhất ở cả ba lớp; chữ nhật vẫn khó nhất.',
'6-6-extraction-grid':'Regex hợp schema ở cả bốn ca nhưng sai nội dung ở ca “7 em” và ca kế hoạch bị đổi.',
'7-kt4-score':'Điểm chuẩn hóa theo metric của hai bài; vạch đứt là baseline của đề. Macro-F1 càng cao càng tốt, WER càng thấp càng tốt, kém baseline thì điểm bằng 0. Các chấm là bốn trường hợp trong code.',
'7-kt4-paired':'Mỗi ô là một mẫu validation, ô đặc là dự đoán đúng. Fusion sửa ba ID mà nhánh ảnh sai (xanh) và làm sai thêm hai ID mà nhánh ảnh đúng (đỏ); ID 5 và 14 cả ba cùng sai.',
'7-3-ctc-dp':'Lưới α của target `a`: mỗi ô cộng các ô được phép đi tới ở frame trước rồi nhân xác suất frame; hai ô cuối cộng ra 0.76.',
'8-1-plans':'Mỗi chấm là một kế hoạch; đường bậc thang là điểm tối đa trong từng ngân sách. Ở 130 phút, duyệt hết đạt 40 điểm, tham lam dừng ở 30.',
'8-1-noise':'Chênh lệch accuracy public của B so với A qua 5000 lần rút. Đường đứng sẫm là 0, đường nét đứt là chênh lệch thật 0.01.',
'8-3-ablation':'Lọc cứng mất ba hidden dù số lượt trung bình trên ván giải được thấp nhất; tính cả ván thất bại, lọc mềm cân đối đứng đầu.',
'8-5-column-order':'Accuracy validation của cùng một model theo sáu thứ tự cột: chỉ thứ tự x0, x1, x2 lúc fit cho 0.933, thứ tự x2, x0, x1 tụt xuống 0.700.',
'8-5-sessions':'Ba lịch 360 phút; tam giác đánh dấu phút đóng thí nghiệm. Buổi 2 đóng ở phút 275 để chừa 70 phút chạy lại; buổi 1 chưa chạy lại và dùng 35 phút cuối để sửa file.',
}
def regenerate():
    scripts=['plots.py','scenes01.py','scenes34.py','scenes5.py','scenes67.py','scenes89.py','canary.py','supplement.py','experiments.py','extra8.py','tuning17.py','boost27.py','depth33.py','optim35.py','regul36.py','rnn38.py','ae310.py','pretrained41.py','kt2regions.py','kt3threshold.py','occlusion59.py','depth52.py','augment53.py','neighbors57.py','extract66.py','kt4score.py','kt4paired.py','ctcdp73.py','plans81.py','noise81.py','open83.py','mock85.py','p8_ch0.py','p8_ch1.py','p8_ch2.py','p8_ch3.py','p8_ch4.py','p8_ch5.py','p8_ch6.py','p8_ch7.py','p8_ch8.py','p8_ch9.py']  # lượt 8: hình vẽ lại hoặc thêm mới, chạy sau cùng để thay bản cũ
    for name in scripts:
        r=subprocess.run([sys.executable,'-B','-X','utf8',str(R/name)],capture_output=True,text=True,encoding='utf-8')
        if r.returncode:raise RuntimeError(name+'\n'+r.stdout+'\n'+r.stderr)
        print(name,'OK',flush=True)
def finalize():
    manifest={};captions={};ns={'s':'http://www.w3.org/2000/svg'}
    for p in sorted((R/'staged').glob('phase-*/fig/*.svg')):
        raw=p.read_text(encoding='utf-8');stem=p.stem
        tree=ET.fromstring(raw);title=tree.find('s:title',ns)
        caption=CAP.get(stem) or (title.text if title is not None else None)
        assert caption,(stem,'missing meaningful caption')
        # No SVG id may collide with another inline figure's clip paths.
        ids=re.findall(r'\bid="([^"]+)"',raw);prefix='fig-'+stem+'-'
        for id in ids:
            if id.startswith(prefix):continue
            raw=raw.replace('id="'+id+'"','id="'+prefix+id+'"').replace('#'+id+'"','#'+prefix+id+'"').replace('#'+id+')','#'+prefix+id+')')
        raw=re.sub(r'aria-label="[^"]*"|role="img"','',raw)
        if stem in {'2-1-loglog','2-1-scaling','2-2-geometry'}:
            def pad(m):
                x,y,w,h=map(float,m.group(1).split())
                if x<0:return m.group(0)
                return f'viewBox="{x-8:g} {y-8:g} {w+16:g} {h+16:g}"'
            raw=re.sub(r'viewBox="([^"]+)"',pad,raw)
        p.write_text(raw,encoding='utf-8')
        captions[stem]=caption;manifest[stem]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'caption':caption,'retain':stem not in PRUNED}
    assert len(manifest)==EXPECTED,len(manifest)
    (R/'captions.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2),encoding='utf-8')
    (R/'staged-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (R/'pruned.json').write_text(json.dumps(sorted(PRUNED),ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
    if '--finalize-only' not in sys.argv:regenerate()
    finalize();print(f'{EXPECTED} figures staged; {len(PRUNED)} figures no lesson cites are marked for removal.')
    if '--apply' in sys.argv:
        phase=sys.argv[sys.argv.index('--phase')+1] if '--phase' in sys.argv else None
        for p in (R/'staged').glob('phase-*/fig/*.svg'):
            if phase is None or p.parent.parent.name=='phase-'+phase:shutil.copy2(p,C/'content'/p.relative_to(R/'staged'))
