# Kho câu chính thức theo bài

Mã: `P<n>` = NOAI 2026 Vòng sơ loại, số mục trên bản in Google Forms (mục 12–311 là 300 câu thi), kèm trang PDF. Mức: **G** câu tình huống/vận dụng tốt, R câu nhớ định nghĩa (chỉ hợp làm hỏi nhanh), A nâng cao/lạc đề.
Mọi câu dùng phải tự giải lại và diễn đạt lại bằng lời mình (không có giấy phép dùng nguyên văn); ghi `Đề thi:` khi giữ đúng ý và đáp án của câu gốc, `Phỏng theo:` khi đổi dữ kiện hoặc nguồn là tài liệu luyện tập của trường.

Link: NOAI 2026 sơ loại `https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=<trang>`.

| Bài | NOAI 2026 sơ loại |
|---|---|
| 0.1 | P94 p38 sửa list trong hàm **G** · P95 `is`/`==` **G** · P91 p37 `[1,2]+[3,4]` R · P93 list comprehension R · P99 p39 zip R · P98 generator R · P88 p36 mutable R · P137 p52 IndexError R |
| 0.2 | P113 p44 `np.dot` vs `*` **G** · P104 p41 nhân từng phần tử cần cùng shape/broadcast · P105 arange R · P106 p42 hàng đầu R · P107 broadcasting R · P109 p43 vectorisation R · P115 p45 vì sao NumPy nhanh R · P116 stride A · P12 p8, P16 p10, P20 p11 shape nhân ma trận R · P13 p9 chuẩn L2 R |
| 0.3 | P110 p43 cột tên có dấu cách **G** · P111 groupby mean R · P112 p44 thiếu dữ liệu R · P69 p27 lệch phải mean>median **G** · P57–P59 p23–24 thống kê R · P64–P65 p26 std, z-score R · P70 p28 CLT |
| 1.1 | P147 p55, P148–P150 p56 loại bài R · P302 p115 thứ tự pipeline R · P236 p85, P281 p106 generative/discriminative |
| 1.2 | P272 p98 LSTM 5K review train 98.5/val 72.3 **G** · P277 p104 ba mô hình chẩn đoán **G** · P158 p59 bias–variance R · P153 p57 overfitting R · P286 p108 test 2025 tụt (drift) **G** |
| 1.3 | P303 p116 Protocol A (chọn trên test 50 lần) vs B **G** · P279 p105 CV hay split R · P154–P155 p58 R |
| 1.4 | P304 p117 pipeline tiền xử lý credit **G** · P305 p117 vì sao chuẩn hóa giúp logistic **G** |
| 1.5 | P276 p103 TP180 FP294 đánh giá fraud **G** (đề ghi accuracy 98.7% nhưng số trong đề cho 96.9%; đáp án gốc mơ hồ giữa C và D → dùng bản có chi phí) · P275 p101 class weight vs oversample/SMOTE/undersample **G** · P274 p100 accuracy gây hiểu nhầm R · P66–P68 p26–27 precision/recall/F1 R · P168 p62 ROC R |
| 1.7 | P303 p116 **G** |
| 2.1 | P34 p16 pseudoinverse cần full column rank **G** · P35 condition number **G** · P46 p20 ∂L/∂w R · P86 p35 hội tụ lồi |
| 2.2 | P269 p96 50 bệnh nhân × 100 biomarker, train 98% val 62% **G** · P159 p59, P160 p60 R |
| 2.3 | P273 p99 BCE vs MSE vs hinge vs MAE cho logit **G** · P305 p117 **G** · P45 p19 đạo hàm sigmoid R · P72 p28 BCE R · P75 p29 MLE R · P193–P194 p71 R · P169 p63 Naive Bayes |
| 2.4 | P151 p57 R |
| 2.5 | P270 p97 bốn cách xử lý thiếu dữ liệu **G** · P152 p57 R |
| 2.6 | P232 p84 OOB R · P162 p60 R · P165 p61 bagging giảm variance R |
| 2.7 | P267 p95 20 feature × 5000 mẫu chọn GBDT **G** · P163 p61, P166 p62 R |
| 2.8 | P171 p63 soft margin/C R · P170 one-class SVM · P161 p60 kernel trick R |
| 2.9 | P156 p58, P25 p13 PCA R · P24 p12 hiệp phương sai đối xứng · P28 p14 SVD · P164 p61 curse of dimensionality R |
| 2.10 | P271 p97 mật độ thay đổi → DBSCAN R · P157 p59 chọn K R · P36 p16 spectral clustering A |
| 2.11 | P304 p117 **G** · P270 p97 **G** · P275 p101 **G** · P167 p62 scaling R |
| 3.1 | P118 p46 requires_grad R · P120 backward R · P145 p55 `.item()`/`.detach()` **G** · P129 p49 Tensor/tensor · P54 p22 computational graph R |
| 3.2 | P39 p17 chain rule R · P176 p65 backprop R · P172 p64 perceptron R |
| 3.3 | P273 p99 **G** · P188 p69 khởi tạo nhỏ cho 10 lớp ReLU, He init **G** · P55 p23 vanishing sigmoid R · P183 p67, P191–P192 p70 ReLU/dying/leaky R · P47 p20 ReLU tại 0 · P173–P175 p64–65 R |
| 3.4 | P126 p48 backward hai lần không zero_grad **G** · P121 p47 zero_grad R · P284 p107 val đứng 10% → nhãn lệch **G** · P288 p109 gradient lớp cuối bằng 0 **G** · P141 p53 NaN R · P124 p48 train/eval R · P127 p49 no_grad R · P178–P179 p66 epoch/batch R · P280 p105 loss dao động R |
| 3.5 | P83 p33 warmup BERT **G** · P84 p34 constant/cosine/step **G** · P85 p35 Newton chậm do nghịch đảo Hessian **G** · P297 p114 plateau cần step decay **G** · P294 p112 warmup Adam **G** · P293 1cycle · P298, P301 p114–115 Adam vs SGD R · P51 p21 momentum R · P52 p22 annealing R · P78–P82 p30–32 GD variants R |
| 3.6 | P188 p69 **G** · P195 p71 BN và dropout xung đột · P196 p72 LayerNorm R · P189 p69 early stopping R · P180–P181 p66–67 R · P184–P186 p68 R · P233 p84 clipping R |
| 3.7 | P296 p113 gradient accumulation 8×4 **G** · P285 p108 OOM ResNet-50 **G** · P295 p113 batch lớn và độ chính xác **G** · P144 p54 GPU chậm hơn CPU R · P139 p53 OOM R · P135 p51, P300 p115 mixed precision R · P287 p109 lỗi shape CPU vs GPU A |
| 3.8 | P217–P219 p79 embedding/word2vec/RNN R · P220 p80 LSTM R |
| 3.9 | P230 p83 O(n²) R · P225 p81 positional encoding R · P221–P222 p80 R · P247 p89 ngữ cảnh dài R |
| 3.10 | P76 p30 KL bất đối xứng R |
| 4.1 | P213 p77 vì sao pretrain ImageNet hiệu quả R · P134 p51 lưu state_dict R |
| 4.3 | P132 p50 freeze R · P228 p82, P245 p88 fine-tune R |
| 4.4 | P246 p88 LoRA R |
| 4.5 | P243–P244 p87–88 zero/few-shot R · P261 p93 CLIP zero-shot R |
| 5.1 | P215 p78 3×3 xếp chồng **G** · P214 p78 receptive field R · P199–P202 p73–74 pooling/stride/padding R · P204 p74 feature map R |
| 5.2 | P216 p78 ResNet R · P206 p75 CNN sâu R |
| 5.3 | P307 p119 ba cách chuẩn hóa X-quang **G** · P212 p77, P299 p114 augmentation R · P205 p75 transfer R |
| 5.4 | P260 p93 ViT = chuỗi patch R |
| 5.5 | P268 p96 YOLO cho thời gian thực R (đã dùng ở kt3) · P207–P209 p75–76 R |
| 5.6 | P234 p84 skip của U-Net R · P210–P211 p76–77 semantic/instance R |
| 5.7 | P259 p93 contrastive R · P258 p92, P262 p94 R |
| 5.8 | P255 p91 diffusion chậm hơn GAN R · P254 CFG R · P251 p90 latent diffusion R · P252 p90, P253 p91, P256 p92 R |
| 6.1 | P235 p85 subword **G** · P227 p82 R |
| 6.3 | P224 p81 BERT vs GPT R · P226 p82 MLM R · P229 p83 CLS R |
| 6.4 | P231 p83 causal mask R · P240 p86 temperature R · P241 p87 top-k R · P239 p86 autoregressive R |
| 6.6 | P248 p89 RAG R · P242 p87 prompt R · P238 p86 R |
| 7.4 | P265 p95 cross-attention R · P266 thách thức đa phương thức R · P257 p92 R |
| 8.1–8.3 | P267 p95 **G** · P310 p122 giám sát approval rate **G** · P311 p123 drift tín dụng **G** · P286 p108 **G** · P308 p120 cần version gì để tái tạo model **G** |
| 8.4 | P165 p61, P166 p62 bagging/boosting R |

## NOAI 2026 Chung kết, Phần 1 (`F<n>`, mục trên bản in, trang PDF)

Link `https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Final-Assessment-Section-1-MCQs-Google-Forms.pdf#page=<trang>`. Đa số là câu đọc code/gỡ lỗi, chất lượng cao. Câu đánh dấu ⚠ có đáp án mơ hồ: chỉ dùng sau khi tự kiểm, hoặc viết lại thành câu "Phỏng theo" có điều kiện rõ.

| Bài | Câu |
|---|---|
| 1.3/1.4 | F4 p5 chọn đặc trưng trên toàn bộ dữ liệu rồi mới CV (92%) vs trong từng fold (78%) **G** |
| 2.3 | F5 p7 gradient logistic + L2 theo quy ước scikit-learn **G** (đáp án D; câu chữ "C = 1/λm" của đề lệch quy ước, sửa khi phỏng theo) |
| 2.6 | F2 p3 tăng n_estimators 100→1000, val đứng 87.3% **G** |
| 2.7 | F3 p4 boosting chuyển sang loss L1: phần dư thành sign, lá lấy trung vị **G** · F6 p9 AdaBoost ⚠ (B và C đều sửa được) |
| 3.3 | F7 p11 loss đa nhãn: sigmoid+BCE vs softmax **G** |
| 3.5 | F10 p15 learning rate warmup+cosine tại bước 50000 (≈5.0e-4) **G** |
| 3.6 | F8 p12 norm gradient lớp đầu rất nhỏ → vanishing, thêm residual **G** · F9 p13 BatchNorm tự viết ⚠ |
| 3.7 | F11 p16 chia loss khi gradient accumulation **G** · F16 p24 `unscale_` trước khi clip với GradScaler **G** |
| 3.9 | F17 p26 thiếu chia √d_k nên attention quá nhọn **G** |
| 4.3 | F15 p22 fine-tune fc không đổi ⚠ · F21 p34 BERT val loss tăng sau epoch 1 ⚠ |
| 5.3 | F12 p17 augmentation X-quang ⚠ |
| 5.6 | F14 p20 IoU khi union = 0 (bỏ lớp) **G** · F13 p18 U-Net lệch kích thước ⚠ |
| 6.1 | F19 p30 cắt chuỗi làm mất `<EOS>` **G** (dữ kiện gốc lệch: câu 8 từ thêm BOS/EOS vừa đủ 10 token nên không bị cắt; 6.1 dùng `max_len = 8`, câu 9 từ, ghi `Phỏng theo:`) |
| 6.3 | F20 p32 MLM 80/10/10 **G** |
| 6.4 | F18 p28 ba cách tạo causal mask đều tương đương **G** |

## NOAI 2025 Phần 1 (`N25-<n>`, có đáp án trong PDF; 4 trang)

Link `https://learn.aisingapore.org/wp-content/uploads/2025/10/NOAI-2025-MCQ-Assessment-Questions.pdf#page=<trang>`. Đều là câu định nghĩa (R).
1 PCA không giám sát (1.1/2.9) · 2 bagging giảm variance (2.6) · 3 RL = thưởng/phạt (9.1) · 4 underfitting (1.2) · 5 boosting tuần tự (2.7) · 6 Adam (3.5) · 7 vanishing (3.3) · 8 early stopping (3.6) · 9 residual (5.2) · 10 lr schedule (3.5) · 11 pooling (5.1) · 12 YOLO một bước (5.5) · 13 RPN (5.5) · 14 depthwise separable (5.2) · 15 Mask R-CNN (5.6) · 16 attention (3.9) · 17 BERT transfer (6.3) · 18 beam search (6.5) · 19 CLS (6.3) · 20 causal mask (6.4).

## USA-NA-AIO 2026

Vòng 1 (`https://www.usaaio.org/attachments/past-problems/2026/usaaio-2026-round-1-problems.pdf#page=<trang>`):
P1.1 p1 không giám sát (1.1) · P1.2 p1–2 L1 vs L2 (2.2, đã dùng) · P1.3 p2 bias–variance theo độ phức tạp (1.2) · P1.4 p2–3 F1 khi lệch lớp (1.5) · P1.5 p3 UMAP giữ cấu trúc lân cận (2.9) · P2.1–2.3 p4–6 chiếu lên thành phần chính, phần dư (2.9, câu tính có 5 lựa chọn) **G** · P3 p7 ma trận từ ánh xạ, phân tích tổng tích ngoài (0.2, tự luận → phỏng theo) · P4.1 p8 đạo hàm tanh (3.3) · P4.2 p8–9 gradient MSE không vòng lặp (2.1) · P5 p10–15 ma trận tương đồng cosine S = WWᵀ, hạng ≤ 100 nên không khả nghịch, xấp xỉ hạng thấp bằng SVD (6.2/2.9) **G** · P6 p16 sắp feature map theo độ sâu (5.1/5.9) · P7.2 p18 chọn σ_w để giữ phương sai (3.3/3.6) **G** · P7.4 p19 MLP ngưỡng nhận diện tam giác (3.2) **G** · P8 p20–21 ResNet-50: số tham số, shape layer2, đóng băng backbone (5.2/4.2) **G** · P9 p22–24 kNN trên dữ liệu bảng (2.4).

Vòng 2 Ngày 1 (`…/usaaio-2026-round-2-day-1-problems.pdf`): P1.1 p2–4 độ phức tạp attention O(T²d), linear attention qua feature map (3.9) **G** · P1.2 p4–5 relative positional encoding, miền j−i (3.9).
Vòng 2 Ngày 2 (`…/usaaio-2026-round-2-day-2-problems.pdf`): P3.1 p2–4 x_t | x_0 trong forward diffusion, giới hạn t→∞ (5.8) **G** · P3.2 p4–6 KL giữa hai Gaussian (3.10/5.8) · P3.3 p6 đưa bước t vào mạng (5.8) · P4 p7–9 phân loại hình, 200 nhãn + 800 không nhãn, cấm pretrained (5.7/8.3).

## Tài liệu luyện tập của trường (luôn ghi `Phỏng theo:`)

CMU 10-601 Practice Exam 1/2/3, MIT 6.036 Final Spring 2022 — tra bằng `tools/exam_find.py <từ khóa>` theo từng bài.
