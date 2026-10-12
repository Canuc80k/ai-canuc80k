'''Author native slide Markdown from curated sequences and exact lesson excerpts.
This is a Phase 1 source recipe, not the website/PDF builder.
Run after check_code --write: python -B -X utf8 content/phase-1/build_slides.py
'''
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
OUT = HERE / 'slides'
OUT.mkdir(parents=True, exist_ok=True)

def source(lesson):
    return (HERE / f'{lesson}.md').read_text(encoding='utf-8')

def slide(marker, body):
    return f'<!-- {marker} -->\n{body.strip()}'

def title(lesson, name, subtitle):
    return slide('title', f'# {name}\n\n{subtitle}\n\nPhase 1 · Bài {lesson}')

def section(number, name):
    return slide(f'section {number}', f'# {name}')

def split(name, left, right):
    return slide('split', f'## {name}\n\n{left}\n\n|||\n\n{right}')

def center(name, body):
    return slide('center', f'## {name}\n\n{body}')

def figure(name, filename, caption):
    return slide('figure', f'## {name}\n\n![{caption}](../fig/{filename}.svg)')

def quick(lesson, index):
    text = source(lesson).split('## Kiểm tra cuối bài')[0]
    quizzes = re.findall(r'^::: quiz[^\n]*\n.*?^:::', text, re.S | re.M)
    return slide('quiz', quizzes[index-1])

def cell(lesson, index, start=None, end=None, out_start=None, out_end=None, output_only=False):
    cells = re.findall(r'^```python\n(.*?)^```\s*\n\s*```output\n(.*?)^```', source(lesson), re.M | re.S)
    code, output = cells[index-1]
    code = '\n'.join(code.rstrip().splitlines()[slice(start, end)])
    output = '\n'.join(output.rstrip().splitlines()[slice(out_start, out_end)])
    code_block = '' if output_only else f'```python\n{code}\n```\n\n'
    return code_block + f'```output\n{output}\n```'

def save(lesson, slides):
    assert 16 <= len(slides) <= 28
    (OUT / f'{lesson}.md').write_text('\n\n---\n\n'.join(slides)+'\n', encoding='utf-8')
    print(f'{lesson}: {len(slides)} slides')

def lesson_11():
    save('1.1', [
        title('1.1', 'Bài toán học máy', 'Đặt ghế cho buổi sinh hoạt thứ Bảy'),
        split('Ta đang dự đoán điều gì?',
              'Chiều thứ Sáu: biết số đăng ký và dự báo mưa.\n\nThứ Bảy: mới biết số người thật sự đến.',
              'Mỗi hàng = một buổi.\n\nMột dự đoán = một con số người.\n\nThông tin đầu vào phải có đúng lúc sử dụng.'),
        center('Sau buổi này', 'Viết hợp đồng bài toán · dựng baseline · đọc MAE · kiểm bảng theo ID'),
        section(1, 'Dữ liệu và đầu ra'),
        figure('Feature, target và ID', '1-1-contract', 'ID dùng để ghép kết quả; target chỉ dùng khi học hoặc chấm.'),
        split('Classification hay regression?',
              'Có ít nhất 30 người không?\n\n**Classification:** một nhãn.',
              'Có bao nhiêu người?\n\n**Regression:** một giá trị số.\n\nMã lớp bằng số không tự biến classification thành regression.'),
        quick('1.1', 1),
        center('Shape trước model', cell('1.1', 1, start=-4)+'\n\nX: (120,2) · y: (120,) · hàng là buổi, cột là feature.'),
        section(2, 'Học, chọn và chấm'),
        figure('Ba phần, ba công việc', '1-1-timeline', 'Chốt phương án trước khi mở test.'),
        quick('1.1', 3),
        center('MAE có đơn vị người', r'$$\operatorname{MAE}=\frac1m\sum_i|\hat y_i-y_i|.$$'+'\n\nCàng nhỏ càng tốt; không phải mọi buổi đều sai bằng nhau.'),
        split('Ví dụ tay', 'Thật: (20, 30, 40)\n\nĐoán: (18, 33, 39)',
              r'$$\operatorname{MAE}=(2+3+1)/3=2.$$'+'\n\nSai cao và sai thấp không triệt tiêu nhau.'),
        center('Baseline hằng số và linear', cell('1.1', 3, start=9, end=16)+'\n\nCùng 20 buổi validation · chọn theo MAE nhỏ hơn.'),
        center('Chốt rồi chấm', cell('1.1', 4)+'\n\nFit lại train + validation; test MAE 1.317 người.\n\nSau khi xem test, không chỉnh rồi gọi cùng điểm là độc lập.'),
        section(3, 'Đường dự đoán thật'),
        split('Kiểm bảng CSV', 'Một hàng cho mỗi ID.\n\nĐúng tên cột, đúng thứ tự, số hữu hạn.\n\nDùng `index=False`.',
              cell('1.1', 5, output_only=True)),
        quick('1.1', 4),
        split('Bẫy và cách kiểm', 'Nhãn `(n,1)` trừ dự đoán `(n,)` có thể tạo `(n,n)`.\n\nKiểm shape trước khi chấm.',
              '`model.score` không luôn là metric đề.\n\nGọi MAE tường minh.\n\nKhông đưa target hậu nghiệm vào feature.'),
        center('Khi đi thi', 'Đọc input/output và metric → baseline → kiểm ví dụ tay → kiểm ID → nộp theo môi trường được phép.'),
        center('Chốt ý', 'Train học · validation chọn · test báo cáo.\n\nLàm 10 câu cuối bài và chạy lại notebook.'),
    ])

def lesson_12():
    save('1.2', [
        title('1.2', 'Generalization', 'Đúng trên dữ liệu đã nhớ có đủ không?'),
        split('Buổi tuần sau là một mẫu mới', 'Lưu nguyên nhãn cũ có thể cho lỗi train bằng 0.',
              'Mục tiêu: dự đoán tốt ở buổi chưa thấy.\n\nCần validation mô phỏng đúng tình huống mới.'),
        section(1, 'Độ linh hoạt và nhiễu'),
        center('Một cơ chế sinh biết trước', r'$$y=\sin(2\pi x)+\varepsilon.$$'+'\n\nMức tham gia chuẩn hóa; nhiễu có std 0.25.\n\nDữ liệu giả để kiểm cơ chế.'),
        figure('Ba đường cùng train', '1-2-fits', 'k=1 bám nhiễu; k=80 san phẳng; k=10 giữ xu hướng.'),
        quick('1.2', 1),
        split('kNN ở mức cần dùng hôm nay', 'Tìm k điểm train gần nhất.\n\nLấy trung bình nhãn.',
              'k nhỏ: linh hoạt hơn.\n\nk lớn: trơn hơn.\n\nTại điểm train, k=1 trả đúng nhãn kể cả nhiễu.'),
        center('Đọc hai cột lỗi', cell('1.2', 1, start=14)+'\n\nk=1 có train 0; k=10 có validation thấp hơn.'),
        quick('1.2', 2),
        split('Underfit và overfit', 'Underfit: thiếu khả năng biểu diễn hoặc học chưa đạt.',
              'Overfit: chi tiết train không ổn định trên mẫu mới.\n\nKiểm split, metric và dữ liệu trước khi đổi model.'),
        section(2, 'Thêm dữ liệu có ích không?'),
        figure('Learning curve', '1-2-learning', 'Trục ngang là số mẫu; mỗi điểm trung bình bốn fold.'),
        split('Đọc learning curve', cell('1.2', 2, output_only=True),
              'Validation giảm từ 0.2187 xuống 0.0748.\n\nTăng mẫu giúp vùng hàng xóm hẹp hơn.\n\nSau đó cải thiện chậm dần.'),
        center('Đừng nhầm hai trục ngang', 'Learning curve: số mẫu train.\n\nĐường tối ưu: epoch / số bước.\n\nMỗi đường trả lời một câu hỏi.'),
        quick('1.2', 3),
        split('Ví dụ tay', 'k=2; nhãn hàng xóm 1 và 3 → đoán 2.\n\nNhãn mới 4 → lỗi bình phương 4.',
              'Thật (1,3,5), đoán (2,3,4):\n\nMSE = (1+0+1)/3 = 2/3.'),
        center('Phần nhiễu còn lại', r'$$\mathbb E[\varepsilon^2]=0.25^2=0.0625.$$'+'\n\nTrong cơ chế giả lập này.\n\nValidation hữu hạn có thể nằm thấp hơn do ngẫu nhiên.'),
        section(3, 'Generalization cho ai?'),
        quick('1.2', 4),
        split('Trở lại câu lạc bộ', 'Tuần tương lai có thể khác mùa, lịch học hoặc quy mô.',
              'Trường mới khác với buổi mới ở cùng trường.\n\nSplit phải mô phỏng nhiệm vụ, không chọn theo điểm đẹp.'),
        center('Chốt ý', 'Đọc train + validation, kiểm điều kiện split, rồi chọn cách xử lý.\n\nLàm 10 câu cuối bài.'),
    ])

def lesson_13():
    save('1.3', [
        title('1.3', 'Data split và cross-validation', 'Mẫu mới là một hàng, một người hay một thời điểm?'),
        split('Ba bài làm của một học sinh', 'Chia theo hàng có thể đưa cùng người vào train và validation.',
              'Đích: người ở trường mới.\n\nPhải giữ đơn vị chưa thấy ra khỏi train.'),
        section(1, 'Chọn split từ nhiệm vụ'),
        figure('Hàng khác nhưng người trùng', '1-3-groups', 'Group split giữ các bản ghi của một người cùng phía trong từng vòng.'),
        quick('1.3', 1),
        split('Stratified giữ nhãn', cell('1.3', 1, output_only=True),
              '12 mẫu, ba dương.\n\nValid ba mẫu không thể giữ đúng tỷ lệ 25%.\n\nStratified không tự giữ người hoặc thời gian.'),
        quick('1.3', 2),
        split('Kiểm group giao nhau', cell('1.3', 2, output_only=True),
              'Không chỉ kiểm chỉ số hàng.\n\nGroup ở train ∩ group ở valid phải rỗng khi đánh giá group mới.'),
        section(2, 'Dự đoán tương lai'),
        figure('Train đứng trước validation', '1-3-time', 'Train mở rộng, gap theo thời điểm biết nhãn; test cuối giữ riêng.'),
        center('Các chỉ số đã chạy', cell('1.3', 3, output_only=True)+'\n\nSắp theo thời gian trước. Gap=1 là minh họa; gap thật theo thời điểm biết nhãn.'),
        quick('1.3', 3),
        section(3, 'K-fold và OOF'),
        center('Mỗi mẫu được chấm khi nó ở ngoài train', r'$$\bar s=\frac1K\sum_{k=1}^Ks_k.$$'+'\n\nĐiểm trung bình fold và metric gộp không luôn giống nhau.'),
        split('Ghi OOF về vị trí gốc',
              '```python\noof_probability[valid_ids] = probability\ntimes_scored[valid_ids] += 1\n```\n\nTrích hai dòng từ vòng CV trong bài.',
              cell('1.3', 4, output_only=True)),
        split('Kiểm các hàng được chấm', '```python\nassert np.all(times_scored == 1)\nassert np.isfinite(oof_probability).all()\n```',
              'K-fold phân hoạch đầy đủ trong demo.\n\nTimeSeriesSplit có hàng đầu chưa từng làm validation: cần mask, không điền bằng nhãn.'),
        quick('1.3', 4),
        split('Tính tay: validation thiếu lớp', r'$\binom{12}{3}=220$ bộ ba.'+'\n\n'+r'$\binom9{3}=84$ bộ không có dương.',
              'Xác suất 84/220 ≈ 0.382.\n\nKiểm số mẫu lớp trong từng fold.'),
        split('Bẫy', 'OOF không được nối theo thứ tự fold rồi coi là thứ tự gốc.\n\nFeature, nhãn và group dùng cùng chỉ số.',
              'Fit preprocessing trong từng fold.\n\nDùng OOF để chọn nhiều phương án vẫn cần test ngoài hoặc nested CV.'),
        center('Chốt ý', 'Random: độc lập · stratified: lớp · group: đơn vị mới · thời gian: tương lai.\n\nLàm 10 câu cuối bài.'),
    ])

def lesson_14():
    save('1.4', [
        title('1.4', 'Pipeline và data leakage', 'Tiền xử lý cũng là một phần được học'),
        split('Một bảng có số, chữ và ô thiếu', 'Điền thiếu, scale và encode trước model.',
              'Nếu xử lý cả bảng rồi mới split, validation đã ảnh hưởng việc học.'),
        section(1, 'Fit ở đâu?'),
        split('Tính tay scaler', 'Train 10, 20 → mean 15, std 5.\n\nValid 30 → (30−15)/5 = 3.',
              cell('1.4', 1, output_only=True)),
        quick('1.4', 1),
        figure('Giữ cùng hệ tọa độ', '1-4-pipeline', 'Train fit; dữ liệu mới chỉ transform rồi predict.'),
        split('Biến đổi cố định và được học', 'Chia cm cho 100 theo schema: cố định.\n\nMedian, mean/std, danh mục: học từ dữ liệu.',
              'Học từ train của mỗi lần đánh giá.\n\nÁp dụng nhất quán cho mẫu mới.'),
        section(2, 'Những đường rò rỉ'),
        figure('Pipeline không hiểu thời điểm cột', '1-4-leakage', 'Chặn preprocessing toàn bảng và kiểm riêng feature hậu nghiệm.'),
        quick('1.4', 2),
        split('Bảng demo', cell('1.4', 2, output_only=True),
              '80 buổi; train 60, valid 20.\n\nMissing không mặc nhiên bằng 0.\n\nSlot sáng/chiều dùng one-hot.'),
        section(3, 'ColumnTransformer + Pipeline'),
        split('Mỗi nhóm cột một nhánh', 'Số: median → StandardScaler.\n\nChữ: most frequent → OneHotEncoder.',
              'ColumnTransformer ghép nhánh.\n\nPipeline ngoài ghép preprocessing → regressor.'),
        center('Fit toàn quy trình', cell('1.4', 3, start=-4)+'\n\n20 hàng, 4 cột; MAE validation 1.707. Tên bước dùng để tra trạng thái.'),
        quick('1.4', 3),
        split('Đọc trạng thái đã học', cell('1.4', 4, output_only=True),
              'Median lưu khớp train.\n\nBuổi tối chưa thấy → one-hot toàn 0.\n\nChạy được chưa bảo đảm model hiểu buổi tối.'),
        split('CV nhận toàn Pipeline', cell('1.4', 5, start=3),
              'Mỗi fold fit lại imputer, scaler, encoder và model.\n\nKhông transform toàn dev trước CV.'),
        quick('1.4', 4),
        center('Điểm hoàn hảo nhưng vô dụng', cell('1.4', 6, output_only=True)+'\n\nCố tình dùng target làm feature. MAE 0 vẫn không hợp lệ:\n\nfeature chưa biết lúc cần dự đoán.'),
        center('Khi đi thi', 'Lập bảng thời điểm feature, giữ split, fit toàn Pipeline, thử mẫu mới không có nhãn.'),
        center('Chốt ý', 'Pipeline giữ nơi fit; con người giữ hợp đồng dữ liệu.\n\nLàm 10 câu cuối bài.'),
    ])

def lesson_15():
    save('1.5', [
        title('1.5', 'Classification metrics', 'Một cảnh báo đúng nghĩa là gì?'),
        split('Accuracy 97% vẫn bỏ sót mọi buổi cần', '100 buổi: 97 âm, ba dương.\n\nLuôn đoán âm → accuracy 0.97.',
              'Recall 0.\n\nCần đọc loại lỗi, không chỉ một điểm tổng.'),
        section(1, 'Bốn ô và hai mẫu số'),
        figure('Confusion matrix', '1-5-confusion', 'Hàng thật, cột dự đoán; FP báo nhầm, FN bỏ sót.'),
        quick('1.5', 1),
        center('Precision và recall', r'$$P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN}.$$'+'\n\nP: trong những cảnh báo.\n\nR: trong những buổi thật sự cần.'),
        quick('1.5', 2),
        split('Tính tay F1', 'TP=3, FP=3, FN=1.\n\nP=0.5, R=0.75.',
              r'$$F_1=\frac{2TP}{2TP+FP+FN}=0.6.$$'+'\n\nF1 không trực tiếp dùng TN.'),
        split('Đối chiếu code', cell('1.5', 1, output_only=True),
              'Mười score cho sẵn, chưa huấn luyện trong bài.\n\nThreshold 0.5, quy tắc ≥.\n\nKiểm labels và chia 0.'),
        section(2, 'Chọn threshold'),
        figure('Cùng score, đổi quyết định', '1-5-threshold', 'Recall không giảm khi hạ ngưỡng; precision không bắt buộc đơn điệu.'),
        split('Chọn trên validation', cell('1.5', 2, output_only=True),
              'Chọn 0.5 trong bốn ứng viên.\n\nĐây là một hyperparameter.\n\nĐặt quy tắc hòa trước khi xem test.'),
        split('Áp dụng nguyên ngưỡng cho test', '```python\ntest_prediction = p_test >= chosen_threshold\n```\n\n'+cell('1.5', 3, output_only=True),
              'F1 test 0.571.\n\nKhông thử ngưỡng trên test để đổi lựa chọn.'),
        quick('1.5', 3),
        section(3, 'Score, thứ tự và xác suất'),
        figure('ROC-AUC', '1-5-roc', 'Quét threshold tạo ROC; AUC không tự chọn điểm vận hành.'),
        split('Tính AUC theo cặp', 'Bốn dương × sáu âm = 24 cặp.\n\nXếp đúng 6+5+3+1 = 15 cặp.',
              cell('1.5', 4, output_only=True)+'\n\nAUC=15/24=0.625.'),
        quick('1.5', 4),
        split('Log loss phạt sai quá tự tin', cell('1.5', 5, output_only=True),
              'Cùng hai nhãn đều sai ở 0.5.\n\nXác suất sai gần 0/1 bị phạt nặng hơn.\n\nAUC chỉ nhìn thứ tự.'),
        split('Nhiều lớp và lớp hiếm', 'Macro-F1: trung bình đều lớp.\n\nWeighted-F1: trọng số theo số mẫu thật.\n\nMicro: gộp TP/FP/FN trước.',
              'Đúng pos_label, classes_, labels.\n\nResampling chỉ trong train mỗi fold.\n\nKhông đổi metric vì điểm cao hơn.'),
        center('Chốt ý', 'Nhãn → confusion/F1 · thứ tự → AUC/AP · xác suất → log loss.\n\nThreshold chọn từ validation; làm 10 câu cuối bài.'),
    ])

def lesson_16():
    save('1.6', [
        title('1.6', 'Regression và ranking metrics', 'Đo sai số một con số và chấm một danh sách'),
        split('Hai công việc của câu lạc bộ', 'Đặt ghế: sai bao nhiêu người?',
              'Gợi ý ba bài: bài phù hợp đứng gần đầu không?\n\nKhoảng cách giữa mã bài không phải lỗi số học.'),
        section(1, 'Regression'),
        figure('Lỗi lớn bị phạt thế nào?', '1-6-losses', 'Trị tuyệt đối tăng đều; bình phương tăng nhanh.'),
        center('Đọc cả công thức và đơn vị', r'$$\operatorname{MAE}=\frac1n\sum_i|r_i|.$$'+'\n\n'+r'$$\operatorname{RMSE}=\sqrt{\frac1n\sum_i r_i^2}.$$'+'\n\nMAE/RMSE cùng đơn vị target.'),
        quick('1.6', 1),
        split('Tính tay ba buổi', 'Thật (10,20,30), đoán (12,18,27).\n\nSai số (2,−2,−3).',
              cell('1.6', 1, output_only=True)),
        center('R² và mốc trung bình tập chấm', r'$$R^2=1-\frac{\sum_i(y_i-\hat y_i)^2}{\sum_i(y_i-\bar y)^2}.$$'+'\n\nCó thể âm. Không phải tỷ lệ mẫu đoán đúng.'),
        quick('1.6', 2),
        figure('Cùng lỗi tuyệt đối, tỷ lệ khác nhau', '1-6-relative', 'MAPE đặt trọng số lớn lên target nhỏ.'),
        split('MAPE và target 0', cell('1.6', 2, output_only=True),
              '0.1333 = 13.33%.\n\nTarget 0 gây mẫu số nguy hiểm.\n\nTheo đúng công thức scorer, không tự cộng 1.'),
        quick('1.6', 3),
        split('Chọn metric đổi người thắng', cell('1.6', 3, output_only=True),
              'MAE chọn A.\n\nMAPE chọn B.\n\nHai metric đặt trọng số khác nhau.'),
        split('Loss học khác metric chấm', cell('1.6', 4, output_only=True),
              'Hằng số tối ưu MSE: mean.\n\nHằng số tối ưu MAE: median.\n\nChọn thực tế bằng validation theo metric đề.'),
        section(2, 'Ranking theo query'),
        figure('Đặt bài relevant gần đầu', '1-6-ranking', 'Cùng Precision@3, AP@3 khác do thứ tự.'),
        center('Một quy ước AP@k', r'$$\operatorname{AP@}k=\frac{\sum_{r=1}^kP@r\,\operatorname{rel}(r)}{\min(R,k)}.$$'+'\n\nĐọc mẫu số, duplicate, query rỗng và tie của scorer thật.'),
        split('Chỉ cộng tại vị trí relevant', '```python\nhits = 0\ntotal = 0.0\nfor rank, item in enumerate(top, start=1):\n    if item in relevant:\n        hits += 1\n        total += hits / rank\n```',
              'Trích vòng lặp trong `ap_at_k`.\n\nTử số cộng precision tại từng vị trí đúng.\n\nSau đó chia mẫu số của scorer.'),
        quick('1.6', 4),
        split('Ví dụ tay và code', 'Query 1: AP=5/9.\n\nQuery 2: relevant ở hạng 2 → AP=1/2.',
              cell('1.6', 5, output_only=True)+'\n\nMAP=(5/9+1/2)/2=19/36.'),
        split('Bẫy của phép gộp', 'RMSE gộp không mặc nhiên là trung bình RMSE fold.\n\nGiữ shape nhãn và prediction.',
              'Không nối query để tính AP một lần.\n\nKhông thay AP@k bằng AP classification.\n\nSplit vẫn phải đúng.'),
        center('Chốt ý', 'Regression: đơn vị, outlier, mẫu số.\n\nRanking: query, relevance, thứ tự và quy ước.\n\nLàm 10 câu cuối bài.'),
    ])

def lesson_17():
    save('1.7', [
        title('1.7', 'Hyperparameter tuning', 'Thử tham số để quyết định, không chỉ để có điểm cao'),
        split('Một lần thử cần một câu hỏi', 'Đổi k có giảm overfit không?\n\nFeature mới có sửa nhóm lỗi không?',
              'Giữ split và metric để biết điểm đổi do điều gì.\n\nGhi recipe, không chỉ score.'),
        section(1, 'Quy trình lựa chọn'),
        figure('Test ngoài toàn bộ tuning', '1-7-workflow', 'Vòng trong chọn; chốt model rồi mới chấm test.'),
        split('Parameter và hyperparameter', 'Hệ số linear được học từ train: parameter.',
              'k, độ sâu, mức phạt, threshold: quyết định cấu hình.\n\nFeature và preprocessing cũng là lựa chọn.'),
        quick('1.7', 1),
        split('Dev và test đã tách', cell('1.7', 1, output_only=True),
              'Mẫu giả độc lập → stratified.\n\nPipeline chứa StandardScaler.\n\nMetric lựa chọn: F1 lớp 1.'),
        split('Mọi fold fit cả Pipeline', '```python\npipeline = Pipeline([\n    (\'scale\', StandardScaler()),\n    (\'knn\', KNeighborsClassifier()),\n])\n```',
              'Trích từ bài học.\n\nScaler được fit riêng trong từng fold.\n\nTham số dùng tên `knn__n_neighbors`.'),
        section(2, 'Ngân sách search'),
        center('Đếm fit trước khi chạy', '3 giá trị k × 2 weights = 6 cấu hình.\n\n3 fold + refit cuối:\n\n6 × 3 + 1 = **19 fit**.'),
        quick('1.7', 2),
        figure('Grid và random', '1-7-search', 'Grid vùng nhỏ thử hết; random lấy mẫu theo ngân sách trong vùng rộng hơn.'),
        center('Grid đã chạy', cell('1.7', 2, output_only=True, out_start=7)+'\n\nk=9, weights=distance; CV F1 0.685.\n\nTên bước: `knn__n_neighbors`.'),
        split('Đọc log train và validation', 'Distance: train score có thể bằng 1 vì điểm là hàng xóm của chính nó.',
              '`mean_test_score` trong CV = validation fold.\n\nKhông phải test ngoài.\n\nXem từng fold khi cải thiện nhỏ.'),
        center('Random đã chạy', cell('1.7', 3, output_only=True)+'\n\n4 ứng viên, 3 fold, refit → 13 fit. Cùng CV và metric.\n\nGhi ngân sách và vùng search.'),
        quick('1.7', 3),
        section(3, 'Chốt và báo cáo'),
        center('Chọn bằng CV, chấm test', cell('1.7', 4, output_only=True)+'\n\nGrid thắng theo CV; `best_estimator_` đã refit toàn dev.\n\nTest F1 0.727, đọc cả confusion matrix.'),
        split('Tính tay khi hòa', 'A: (0.7,0.8,0.9).\n\nB: (0.8,0.8,0.8).\n\nCùng trung bình 0.8.',
              'Quy tắc hòa đặt trước test.\n\nKhông tự suy ra B chắc chắn tổng quát tốt hơn.\n\nCó thể xét chi phí hoặc độ ổn định trên dev.'),
        quick('1.7', 4),
        split('Nested CV khi cần', 'Vòng trong chọn cấu hình.\n\nVòng ngoài chấm toàn quy trình chọn.',
              'Tốn thêm fit.\n\nBest CV score của vòng trong thường lạc quan sau chọn.\n\nTest ngoài là phương án đơn giản nếu có đủ dữ liệu.'),
        split('Log và bước thử tiếp', 'Phiên dữ liệu · split · feature · model · tham số · seed · metric · thời gian.',
              'Chọn một giả thuyết tiếp theo từ lỗi.\n\nKhông tìm seed hoặc leaderboard thuận lợi rồi gọi là đánh giá độc lập.'),
        center('Chốt ý', 'Tuning là một phần của việc học.\n\nGiữ Pipeline + split + metric, chọn bằng dev, báo test sau khi chốt.\n\nLàm 10 câu cuối bài.'),
    ])

if __name__ == '__main__':
    lesson_11()
    lesson_12()
    lesson_13()
    lesson_14()
    lesson_15()
    lesson_16()
    lesson_17()
