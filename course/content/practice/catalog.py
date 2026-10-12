"""Danh mục nhánh Thực hành (clone bài kiểu Kaggle/Nitro về LQDOJ).

Mỗi bài: (mã, tên, nguồn, url gốc, nhãn, chương, ghi chú).
Mã LQDOJ: aicanuc80k + chữ mức + số thứ tự 2 chữ số (l Light, m Medium, h High, e Extra, x Max, u Ultra).
Contest của mỗi mức: aicanuc80k<chữ mức>00.
Nhãn (cách có đáp án ẩn):
  co_san    đáp án chính thức đã công bố (IOAI trên Hugging Face)
  bo_goc    lấy từ bộ dữ liệu công khai mà bài gốc dựng lên
  tinh_lai  đáp án suy ra đúng từ đề (tự viết lời giải)
  dung_lai  dữ liệu tổng hợp, tự viết bộ sinh theo đề gốc
  chia_lai  chia lại tập train có nhãn của bài gốc
  link      không đưa lên LQDOJ; trang Thực hành trỏ tới nơi nộp gốc
Ghi chú "kiểm" = nguồn gốc mới suy ra từ cột dữ liệu, phải mở bộ gốc khẳng định trước khi dựng.
"""

N = 'https://judge.nitro-ai.org/competitions/'
K = 'https://www.kaggle.com/competitions/'
IOAI25 = 'https://github.com/IOAI-official/IOAI-2025'
IOAI26 = 'https://github.com/IOAI-official/IOAI-2026'

TIERS = [
    ('l', 'Light', 'Bài bảng đầu tiên, baseline sklearn là thấy đường. Sau chương 1–2.'),
    ('m', 'Medium', 'Làm sạch dữ liệu, tạo đặc trưng, kỷ luật CV, lớp lệch. Sau chương 2.'),
    ('h', 'High', 'Mạng nơ-ron, TF-IDF hoặc model pretrained trên dữ liệu vừa. Sau chương 3–6.'),
    ('e', 'Extra', 'Phân đoạn, phát hiện, truy hồi, lệch phân phối, pipeline nhiều bước.'),
    ('x', 'Max', 'Mức bài thi cá nhân IOAI.'),
    ('u', 'Ultra', 'Bài khó nhất IOAI/CEOAI; nộp tại nơi gốc.'),
]

TASKS = {
    'l': [
        ('l01', 'Hình chữ nhật ẩn', 'ROAI 2025, Practice Session', N + 'roai-2025/practice-session/1/view', 'tinh_lai', [1, 2], ''),
        ('l02', 'Đốt calo', 'OJIA 2025', N + 'roai-2025/ojia/2/view', 'bo_goc', [2], 'Kaggle calories (exercise.csv + calories.csv)'),
        ('l03', 'Điểm thi', 'Thi thử OJIA 3, 2025', N + 'roai-2025/simulare-ojia-3/2/view', 'bo_goc', [2], 'Student Performance Factors, kiểm'),
        ('l04', 'Giá nhà', 'Thi thử OJIA 2, 2025', N + 'roai-2025/simulare-ojia-2/2/view', 'chia_lai', [2], 'Price là biến đổi riêng, chia lại train'),
        ('l05', 'Giá nhà theo khu vực', 'AIIS 2025', N + 'aiis/aiis-contest/3/view', 'chia_lai', [2], 'California Housing tổng hợp, chia lại train'),
        ('l06', 'Tiểu hành tinh', 'ROAI 2026, vòng tỉnh IX–X', N + 'roai-2025/etapa-judeteana-ix-x/1/view', 'dung_lai', [2], ''),
        ('l07', 'Chất lượng đất', 'ROAI 2026, vòng cơ sở', N + 'roai-2025/oaia/2/view', 'chia_lai', [1, 2], ''),
        ('l08', 'Hạt đậu', 'Slovak OAI 2026', N + 'slovenska-olympiada/slovak-aoi-2026/1/view', 'bo_goc', [2], 'UCI Dry Bean'),
        ('l09', 'Titanic', 'Kaggle', K + 'titanic', 'bo_goc', [1, 2], 'titanic3; xáo id, đổi tên cột'),
        ('l10', 'Rừng Roosevelt', 'Kaggle', K + 'forest-cover-type-prediction', 'bo_goc', [2], 'UCI Covertype'),
        ('l11', 'Xe đạp thuê', 'Kaggle', K + 'bike-sharing-demand', 'bo_goc', [1, 2, 8], 'UCI Bike Sharing'),
        ('l12', 'Chữ số viết tay', 'Kaggle', K + 'digit-recognizer', 'bo_goc', [2, 3, 5], 'MNIST'),
        ('l13', 'Tìm đường', 'Cram School Christmas 2025', N + 'cram-school/christmas-special-2025/2/view', 'tinh_lai', [9], ''),
    ],
    'm': [
        ('m01', 'Credit Score', 'Thi thử OJIA 1, 2025', N + 'roai-2025/simulare-ojia/2/view', 'bo_goc', [2], 'Kaggle Credit score classification; nhãn trùng dataset_eval_t của editorial'),
        ('m02', 'Tình trạng bệnh nhân', 'Thi thử OJIA 2, 2025', N + 'roai-2025/simulare-ojia-2/1/view', 'chia_lai', [1, 2], 'SEER Breast Cancer bị làm nhiễu; khớp ngược chỉ 90% nên chia lại train'),
        ('m03', 'Nhịp tim', 'Algolymp Challenge 2025', N + 'algolymp/algolymp-challenge/1/view', 'chia_lai', [2], 'BRFSS 2022; lấy mẫu 100k/20k từ train gốc 244k'),
        ('m04', 'Nhà ở Ames', 'Kaggle', K + 'house-prices-advanced-regression-techniques', 'bo_goc', [2], 'Ames Housing'),
        ('m05', 'Y tá và kẻ phá hoại', 'ROAI 2026, vòng tỉnh XI–XII', N + 'roai-2025/etapa-judeteana-xi-xii/1/view', 'bo_goc', [1, 2], 'MIMIC-II IAC (PhysioNet)'),
        ('m06', 'Nhật ký phòng thí nghiệm', 'Cram School PreONIA 2026', N + 'cram-school/preonia-2026/3/view', 'chia_lai', [2], ''),
        ('m07', 'Nhiễu giấu mặt', 'PreIAIO 2026', N + 'nitro/pre-iaio-2026/1/view', 'tinh_lai', [2], ''),
        ('m08', 'Tranh cổ', 'IOAI 2025, ngày 2', IOAI25, 'co_san', [2, 8], ''),
        ('m09', 'Bình luận độc hại', 'ROAI 2025, Lot Baraj 2', N + 'roai-2025/lot-baraj-2/1/view', 'bo_goc', [6], 'Jigsaw Toxic, cấm transformer'),
        ('m10', 'Xứ Lonpestia bốn thứ tiếng', 'Cram School PreONIA 2025', N + 'cram-school/cram-school-preonia-2025/2/view', 'dung_lai', [6], ''),
        ('m11', 'Cô Tấm nhặt chữ', 'Slovak OAI 2026', N + 'slovenska-olympiada/slovak-aoi-2026/3/view', 'dung_lai', [5], 'MNIST + EMNIST letters'),
        ('m12', 'Mê cung Markov', 'Algolymp PreONIA XI–XII 2026', N + 'algolymp/preonia-xi-xii-2026/1/view', 'tinh_lai', [9], ''),
        ('m13', 'Qua sông có đảo', 'ROAI 2026, vòng cơ sở', N + 'roai-2025/oaia/3/view', 'tinh_lai', [9], ''),
    ],
    'h': [
        ('h01', 'Rừng Codru thì thầm', 'Moldova 2026, Simulation 1', N + 'rm-olimpiada-ai/simulation-1/1/view', 'bo_goc', [6], 'Jigsaw Toxic, test_labels.csv'),
        ('h02', 'Người hay máy', 'ONIA 2025', N + 'roai-2025/onia/1/view', 'chia_lai', [6, 4], ''),
        ('h03', 'Phân loại rác', 'Cram School Intermediate 1, 2025', N + 'cram-school/cram-school-training-1/2/view', 'bo_goc', [4, 5], 'TrashNet, kiểm'),
        ('h04', 'Mickey và Donald', 'Nitro NLP Hackathon 2025', N + 'nitro-2025/nitro-nlp/2/view', 'bo_goc', [6], 'MOROCO, kiểm'),
        ('h05', 'Dấu vết trí nhớ', 'Georgian AI League I, 2026', N + 'gaia/ai-league-i/1/view', 'dung_lai', [2, 8], ''),
        ('h06', 'Hành tinh X', 'Georgian AI League I, 2026', N + 'gaia/ai-league-i/2/view', 'dung_lai', [2, 8], ''),
        ('h07', 'Ý nghĩa cuộc sống', 'PreIAIO 2026', N + 'nitro/pre-iaio-2026/3/view', 'tinh_lai', [2], ''),
        ('h08', 'Cuộc chiến vectơ', 'PreIAIO 2026', N + 'nitro/pre-iaio-2026/2/view', 'tinh_lai', [9], ''),
        ('h09', 'Đài thiên văn', 'CEOAI 2026, Practice 1', N + 'ceoai/ceoai-2026-practice-1/3/view', 'dung_lai', [5], ''),
        ('h10', 'Tách từ ghép tiếng Đức', 'IOAI 2025, GAITE', IOAI25, 'co_san', [6], ''),
        ('h11', 'Giọng thật hay giọng máy', 'IOAI 2025, GAITE', IOAI25, 'co_san', [7], ''),
        ('h12', 'Biển nhà vệ sinh', 'IOAI 2025, ngày 2', IOAI25, 'co_san', [4, 5], ''),
        ('h13', 'Cảm xúc phê bình phim', 'Kaggle', K + 'sentiment-analysis-on-movie-reviews', 'bo_goc', [6, 4], 'SST'),
        ('h14', 'Tweet thảm họa', 'Kaggle', K + 'nlp-getting-started', 'bo_goc', [6], 'Figure Eight Disasters on Social Media, kiểm'),
        ('h15', 'Nhận lệnh bằng giọng nói', 'Kaggle', K + 'tensorflow-speech-recognition-challenge', 'bo_goc', [7], 'Speech Commands v0.02, test 4.890 có nhãn'),
        ('h16', 'Giống chó', 'Kaggle', K + 'dog-breed-identification', 'bo_goc', [4, 5], 'Stanford Dogs'),
    ],
    'e': [
        ('e01', 'Radar', 'IOAI 2025, bài ở nhà và ngày 1', IOAI25, 'co_san', [3, 5], '1,4 GB; cắt tập test cho vừa LQDOJ'),
        ('e02', 'Bóng ma trong cỗ máy', 'IOAI 2026', IOAI26, 'co_san', [6], ''),
        ('e03', 'Gấu trúc MNIST', 'CEOAI 2026, Practice 2', N + 'ceoai/ceoai-2026-practice-2/1/view', 'chia_lai', [5], 'từ MNIST'),
        ('e04', 'Thầy Grammar và trận lở hộp', 'ROAI 2026, chọn đội', N + 'roai-2025/baraj-nationala-2026/1/view', 'bo_goc', [5], 'bộ pedestrian, kiểm'),
        ('e05', 'Người gác máy chủ', 'RISE 2026, chung kết', N + 'nitro/rise-2026-final/3/view', 'bo_goc', [8], 'Server Machine Dataset, kiểm'),
        ('e06', 'Thẻ vàng xứ Codru', 'Moldova 2026, Simulation 1', N + 'rm-olimpiada-ai/simulation-1/2/view', 'chia_lai', [2, 8], 'Elo Merchant (Kaggle)'),
        ('e07', 'Ít dữ liệu thôi', 'Georgian AI League I, 2026', N + 'gaia/ai-league-i/3/view', 'bo_goc', [2, 8], 'UCI APS Failure'),
        ('e08', 'Săn ma', 'AIIS Winter 2026', N + 'aiis/aiis-winter-contest/2/view', 'dung_lai', [4, 5], ''),
        ('e09', 'Nhãn chữ số', 'RISE 2026, vòng loại 2', N + 'nitro/rise-2026-open-qualifier-2/2/view', 'dung_lai', [7], 'Free Spoken Digit'),
        ('e10', 'Chụp chữ', 'CEOAI 2026, ngày 1', N + 'ceoai/ceoai-2026-day-1/4/view', 'dung_lai', [5, 7], ''),
        ('e11', 'Hai đoạn văn trộn lẫn', 'CEOAI 2026, ngày 2', N + 'ceoai/ceoai-2026-day-2/2/view', 'chia_lai', [6], ''),
        ('e12', 'Bạn giả', 'RISE 2026, chung kết', N + 'nitro/rise-2026-final/1/view', 'chia_lai', [6], ''),
    ],
    'x': [
        ('x01', 'Rượt đuổi robot', 'IOAI 2026', IOAI26, 'co_san', [9, 6], ''),
        ('x02', 'Sắp lại cuộc trò chuyện', 'IOAI 2026', IOAI26, 'co_san', [7], 'MP3 16 kHz cho vừa LQDOJ'),
        ('x03', 'Trường IOAI', 'IOAI 2026', IOAI26, 'link', [3], 'chấm bằng cách chạy lại notebook với cấu hình ẩn; hàm sinh bị mã hoá'),
        ('x04', 'Đếm gà', 'IOAI 2025, ngày 1', IOAI25, 'link', [5], 'dữ liệu chính thức chưa công khai'),
        ('x05', 'Lời khai trung thực', 'CEOAI 2026, ngày 1', N + 'ceoai/ceoai-2026-day-1/3/view', 'tinh_lai', [5, 6], 'đáp án tính trước bằng chính model'),
        ('x06', 'Người đa ngữ', 'ROAI 2026, chọn đội (CPU)', N + 'roai-2025/lot-2-2026/1/view', 'co_san', [6, 2], 'AG News; khớp ngược đáp án gốc'),
        ('x07', 'Trợ lý bác sĩ X-quang', 'RISE 2026, chung kết', N + 'nitro/rise-2026-final/2/view', 'bo_goc', [7], 'VQA-RAD, kiểm'),
        ('x08', 'Thẻ của người lưu trữ', 'AICC vòng 8', N + 'aicc/aicc-round-8/3/view', 'chia_lai', [7], 'chia lại 500 thẻ train có đáp án; ảnh gallery gốc làm ảnh gây nhiễu; chỉ CLIP ViT-B/16'),
        ('x09', 'Đếm xúc xắc', 'AICC vòng 8', N + 'aicc/aicc-round-8/1/view', 'co_san', [5], 'Kaggle d6-dice, ảnh 640 px'),
        ('x10', 'Nhãn bị bỏ quên', 'Kazakhstan 2026, vòng 2', N + 'cpfed/ai-olymp-2026-second-round/2/view', 'bo_goc', [5], 'ảnh COCO train2017, nhãn test từ chú thích COCO; mAP như COCOeval'),
    ],
    'u': [
        ('u01', 'Kẻ đi lậu', 'CEOAI 2026, ngày 2', N + 'ceoai/ceoai-2026-day-2/1/view', 'dung_lai', [3], 'phỏng theo: trọng số nộp dạng CSV, người kiểm là phép biến đổi checker C++ làm được (lượng tử hóa, nhiễu, cắt tỉa); bỏ người kiểm fine-tune'),
        ('u02', 'Double Agent Dilemma', 'IOAI 2026', IOAI26, 'link', [5, 4], 'checker phải chạy ResNet18 và ViT-Tiny'),
        ('u03', 'Potato', 'IOAI 2026', IOAI26, 'link', [9, 6], 'tương tác, bộ trả lời cần embedding model'),
        ('u04', 'Corrupt Decoder', 'ROAI 2026, chọn đội (GPU)', N + 'roai-2025/lot-1-2026/2/view', 'link', [5], 'checker phải chạy InceptionV3'),
        ('u05', 'Project KRAKEN', 'CEOAI 2026, Practice 1', N + 'ceoai/ceoai-2026-practice-1/2/view', 'link', [3], 'dữ liệu 1,6 GB số thực nhiễu, không vừa tệp đính kèm LQDOJ'),
        ('u06', 'Robot lạc trong thế giới điểm ảnh', 'AICC vòng 8', N + 'aicc/aicc-round-8/2/view', 'dung_lai', [5, 9], 'môi trường pixelnav của kit gốc: cặp ảnh và màn test sinh mới, checker phát lại dãy hành động'),
        ('u07', 'Hình lạc loài', 'CEOAI 2026, ngày 2', N + 'ceoai/ceoai-2026-day-2/3/view', 'dung_lai', [5], 'ghép bộ ba mới từ 300 ảnh train gốc có chú thích vật'),
    ],
}

# Bài đã lên LQDOJ: mã -> {'data': đường dẫn tải dữ liệu (kit LQDOJ hoặc Kaggle Dataset)}.
# Trang Thực hành hiện bài chưa có ở đây là "Sắp có"; bài "link" luôn trỏ tới nơi nộp gốc.
LIVE = {
    'l01': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl01/attachments/1153'},
    'l02': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl02/attachments/1155'},
    'l03': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl03/attachments/1156'},
    'l04': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl04/attachments/1158'},
    'l05': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl05/attachments/1159'},
    'l06': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl06/attachments/1160'},
    'l07': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl07/attachments/1161'},
    'l08': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl08/attachments/1162'},
    'l09': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl09/attachments/1163'},
    'l10': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl10/attachments/1164'},
    'l11': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl11/attachments/1165'},
    'l12': {},  # dữ liệu ba tệp, xem đề
    'l13': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kl13/attachments/1166'},
    'm01': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km01/attachments/1171'},
    'm02': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km02/attachments/1173'},
    'm03': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km03/attachments/1174'},
    'm04': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km04/attachments/1175'},
    'm05': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km05/attachments/1178'},
    'm06': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km06/attachments/1184'},
    'm07': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km07/attachments/1189'},
    'm08': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km08/attachments/1195'},
    'm09': {},  # dữ liệu hai tệp, xem đề
    'm10': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km10/attachments/1216'},
    'm11': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km11/attachments/1231'},
    'm12': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km12/attachments/1236'},
    'm13': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80km13/attachments/1241'},
    'h01': {},  # dữ liệu ba tệp, xem đề
    'h02': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh02/attachments/1270'},
    'h03': {},  # dữ liệu bốn tệp, xem đề
    'h04': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh04/attachments/1280'},
    'h05': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh05/attachments/1310'},
    'h06': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh06/attachments/1311'},
    'h07': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh07/attachments/1323'},
    'h08': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh08/attachments/1324'},
    'h09': {},  # dữ liệu ba tệp, xem đề
    'h10': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh10/attachments/1364'},
    'h11': {},  # dữ liệu bảy tệp, xem đề
    'h12': {},  # dữ liệu ba tệp, xem đề
    'h13': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh13/attachments/1399'},
    'h14': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kh14/attachments/1401'},
    'h15': {},  # dữ liệu bốn tệp, xem đề
    'h16': {},  # dữ liệu bốn tệp, xem đề
    'e03': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke03/attachments/1408'},
    'e04': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke04/attachments/1409'},
    'e05': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke05/attachments/1419'},
    'e06': {},  # dữ liệu ba tệp, xem đề
    'e01': {},  # dữ liệu tám tệp, xem đề
    'e02': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke02/attachments/1467'},
    'e09': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke09/attachments/1468'},
    'e08': {},  # dữ liệu bốn tệp, xem đề
    'e11': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke11/attachments/1473'},
    'x01': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kx01/attachments/1466'},
    'e07': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke07/attachments/1474'},
    'e12': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ke12/attachments/1475'},
    'x05': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kx05/attachments/1476'},
    'e10': {},  # dữ liệu ba tệp, xem đề
    'x06': {},  # dữ liệu ba tệp, xem đề
    'x07': {},  # dữ liệu hai tệp, xem đề
    'u01': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ku01/attachments/1486'},
    'x09': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80kx09/attachments/1487'},
    'u06': {'data': 'https://lqdoj.edu.vn/problem/aicanuc80ku06/attachments/1488'},
    'u07': {},  # dữ liệu hai tệp, xem đề
    'x10': {},  # dữ liệu tám tệp, xem đề
    'x08': {},  # dữ liệu tám tệp, xem đề
    'x02': {},  # dữ liệu sáu tệp, xem đề
}

LQDOJ = 'https://lqdoj.edu.vn/problem/aicanuc80k'

if __name__ == '__main__':
    from collections import Counter
    total = Counter()
    for tier, name, _ in TIERS:
        rows = TASKS[tier]
        lanes = Counter(r[4] for r in rows)
        total.update(lanes)
        print(f'{name:7} {len(rows):3}  ' + ', '.join(f'{k} {v}' for k, v in sorted(lanes.items())))
    print('Tổng', sum(total.values()), dict(total))
