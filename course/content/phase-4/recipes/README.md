# Recipe thực hành với model pretrained thật

Recipe này đưa các bước của bài 4.1–4.5 từ model nhỏ trong bài sang model công bố thật: tải đúng revision, kiểm hash, nạp lại offline, rồi trích embedding, fine-tune, LoRA hoặc chấm zero-shot trên dữ liệu của mình. Mọi con số chỉ đến từ `RESULT.json` của chính lần chạy; recipe không kèm sẵn điểm của model nào.

Các tệp thực hành: [download_assets.py](download_assets.py), [text_experiment.py](text_experiment.py), [zero_shot.py](zero_shot.py), cùng [common.py](common.py). Chúng cần đi cùng nhau khi tải bộ recipe.

## Môi trường và quyền dùng dữ liệu

Chạy trong môi trường project riêng, không cài thư viện toàn máy. Script cần PyTorch, Transformers, Hugging Face Hub, Safetensors, NumPy, scikit-learn; nhánh LoRA cần thêm PEFT, nhánh ảnh cần Pillow. Cú pháp, CLI và các hàm kiểm của script đã được chạy với torch 2.9.1 (CPU), torchvision 0.24.1, transformers 5.12.1, NumPy 2.2.6 và scikit-learn 1.7.2; đó là một môi trường tham khảo, không phải yêu cầu của cuộc thi. Khi thực hành, dùng phiên bản tương thích trong virtual environment; `RESULT.json` ghi lại môi trường thực chạy.

Trước khi dùng, đọc thông báo môi trường của bài/thi và model card. License của model, license dữ liệu và việc cuộc thi cho dùng asset là ba điều cần kiểm riêng. Tạo một note UTF-8 ghi URL nguồn, revision dự kiến, điều khoản/license đã đọc, mục đích dùng và nguồn/giấy phép của dữ liệu. Script lưu nội dung/hash của note ấy; đây là dấu vết việc review, không phải một chứng nhận pháp lý tự động.

Asset của recipe:

| Tên CLI | Repository | Nguồn đọc license và giới hạn |
|---|---|---|
| `distilbert` | `distilbert/distilbert-base-uncased` | [Model card](https://huggingface.co/distilbert/distilbert-base-uncased), metadata Apache-2.0; model chủ yếu cho tiếng Anh |
| `clip` | `openai/clip-vit-base-patch32` | [Model card](https://huggingface.co/openai/clip-vit-base-patch32) và [repository gốc](https://github.com/openai/CLIP), MIT của repository; cần đọc nguồn/điều kiện của trọng số cụ thể, Hub card có thể thiếu tag license |
| `gpt2` | `openai-community/gpt2` | [Model card](https://huggingface.co/openai-community/gpt2), metadata MIT; causal model tiếng Anh |

Bảng trên lấy từ model card và repository nguồn; script kiểm lại metadata ở revision được chọn và từ chối khi tag có giá trị khác. Với CLIP thiếu tag, note review nguồn là bắt buộc. Không suy license weights chỉ từ license một thư viện. Đối với dữ liệu tự tạo, cũng ghi ai tạo và quyền dùng; đối với dữ liệu ngoài, ghi nguồn và điều kiện riêng.

## Chuẩn bị online rồi thử offline

`download_assets.py` chỉ gọi mạng khi có `--download`. Lấy **commit 40 ký tự hex** của revision định dùng trong repository; thay chuỗi `REPLACE_WITH_40_HEX_COMMIT` dưới đây bằng giá trị thật. Không để `main`. Dùng một thư mục asset mới để tránh trộn phiên bản. Ví dụ từ root bản sao:

```powershell
python -B -X utf8 content/phase-4/recipes/download_assets.py --model distilbert --revision REPLACE_WITH_40_HEX_COMMIT --license-review receipts/phase-4/license-distilbert.txt --dest content/phase-4/recipes/assets/distilbert --download
```

Các tệp safetensors, config, tokenizer và model card được chọn từ revision đó. `ASSET.json` ghi SHA-256 và kích thước từng tệp, revision, model ID và note review. Trạng thái sau tải là `DOWNLOADED_NOT_YET_VALIDATED_OFFLINE`. Đọc [download guide](https://huggingface.co/docs/huggingface_hub/guides/download) nếu layout checkpoint thay đổi; script từ chối khi thiếu config hoặc Safetensors cần thiết, không thay bằng model ngẫu nhiên.

Các script inference/training kiểm lại mọi hash, đặt `HF_HUB_OFFLINE=1` và nạp bằng local path với `local_files_only=True`, `trust_remote_code=False`. Chạy trong một lượt đã ngắt mạng nếu muốn kiểm cả môi trường offline; biến của Hub không ngăn mọi HTTP của code khác trong cả hệ thống. Script không gọi dịch vụ suy luận, không upload và không tự cài gói.

## Feature extraction, head-only, full và LoRA

Chuẩn bị `train.csv` và `valid.csv` với cột `id,text,label,group`. `group` là đơn vị chia cần giữ riêng, như nguồn tài liệu hoặc buổi hoạt động. Không để rỗng, không dùng một ID ở hai tập, không dùng một group ở hai tập. Script còn bắt trùng văn bản chuẩn hóa chính xác. Kiểm này chưa tìm được mọi paraphrase/near-duplicate; cần rà split theo kiến thức dữ liệu.

Tên lớp là chuỗi, được ánh xạ cố định từ tập train. Các nhãn validation phải có trong train. Recipe giới hạn 2000 hàng tổng và 1–80 bước cho một trial nhỏ; mở rộng dữ liệu/training chỉ sau khi đã đánh giá tài nguyên và nhu cầu. Không đọc hidden test để chọn cấu hình. DistilBERT này không phải sentence embedding model chuyên cho mọi nhiệm vụ tương đồng; masked mean là một baseline phải được validation kiểm.

Ví dụ, thay đường dẫn CSV/note review bằng dữ liệu của mình, rồi chạy mỗi mode trong process riêng:

```powershell
python -B -X utf8 content/phase-4/recipes/text_experiment.py --asset content/phase-4/recipes/assets/distilbert --train content/phase-4/recipes/data/train.csv --valid content/phase-4/recipes/data/valid.csv --data-review receipts/phase-4/data-review.txt --mode features --out receipts/phase-4/real-features
python -B -X utf8 content/phase-4/recipes/text_experiment.py --asset content/phase-4/recipes/assets/distilbert --train content/phase-4/recipes/data/train.csv --valid content/phase-4/recipes/data/valid.csv --data-review receipts/phase-4/data-review.txt --mode head --max-steps 20 --out receipts/phase-4/real-head
python -B -X utf8 content/phase-4/recipes/text_experiment.py --asset content/phase-4/recipes/assets/distilbert --train content/phase-4/recipes/data/train.csv --valid content/phase-4/recipes/data/valid.csv --data-review receipts/phase-4/data-review.txt --mode full --max-steps 20 --out receipts/phase-4/real-full
python -B -X utf8 content/phase-4/recipes/text_experiment.py --asset content/phase-4/recipes/assets/distilbert --train content/phase-4/recipes/data/train.csv --valid content/phase-4/recipes/data/valid.csv --data-review receipts/phase-4/data-review.txt --mode lora --rank 4 --max-steps 20 --out receipts/phase-4/real-lora
```

Default là CPU; dùng `--device cuda` chỉ khi môi trường thực có CUDA và được phép. `features` trích masked mean một lần rồi học logistic regression. `head` freeze backbone và đặt backbone eval trong train; head gồm `pre_classifier` và `classifier`. `full` học backbone/head với learning rate riêng. `lora` kiểm đúng các Linear `q_lin`,`v_lin`, giữ base cố định, học adapter và lưu head mới qua `modules_to_save`. PEFT thiếu thì script dừng trước khi nạp asset, không cài tự động.

Các mode training chọn checkpoint có macro-F1 validation lớn nhất, hòa thì chọn loss nhỏ nhất, chỉ trong những bước được chấm. Mode `features` dùng một cấu hình head cố định. Ghi khác biệt giữa cả ngân sách step và loại head; so 20 bước chưa khẳng định mỗi phương pháp đã đạt mức tối ưu. Muốn so kết luận chất lượng cần ngân sách hợp lý, nhiều seed/split nếu phù hợp và test cuối kín.

`RESULT.json` ghi environment, hash CSV và asset, seed, batch/length, history, số tham số được học, validation metric, thời gian có đồng bộ CUDA và peak CUDA allocation nếu có. Đây là allocator peak, chưa phải toàn bộ device memory; CPU peak memory không được đo. `train_plus_validation_seconds` bao gồm các lần validation và chọn checkpoint. Cần đọc cùng định nghĩa khi so. Mode training lưu rồi tải lại model/adapter và đối chiếu logits; model LoRA cần base cùng revision. Feature mode lưu embedding, ID, hệ số head và ánh xạ nhãn trong NPZ; không dùng file này như checkpoint neural độc lập.

## CLIP zero-shot trên ảnh local

Tải CLIP bằng quy trình asset trên. Tạo JSON ánh xạ tên lớp đến **một prompt cố định**, ví dụ `{"desk":"a photo of a desk", "board":"a photo of a classroom board"}`. Tạo CSV `id,image,label` (nhãn có thể bỏ toàn bộ để chỉ inference). Image path tính từ `--image-root`; script từ chối path ra ngoài gốc ấy. Mỗi hàng giữ ID. Prompt vượt context bị từ chối, không cắt âm thầm.

```powershell
python -B -X utf8 content/phase-4/recipes/zero_shot.py --mode clip --asset content/phase-4/recipes/assets/clip --input content/phase-4/recipes/data/images.csv --image-root content/phase-4/recipes/data/images --classes content/phase-4/recipes/data/classes.json --data-review receipts/phase-4/images-review.txt --out receipts/phase-4/real-clip
```

Recipe dùng logits API của checkpoint, có scale đã học, không thay bằng scale 5 của demo. Nếu có nhãn, receipt chấm accuracy và macro-F1 của các prompt khai báo; không có nhãn thì `evaluation` là null. Không dò template bằng hidden test. Không kết luận confidence thế giới mở chỉ từ softmax. Recipe này dùng một prompt/lớp, chưa triển khai ensemble template.

## GPT-2: chấm continuation ngắn

JSON input có `prompt` và `candidates`; tự ghi chính xác khoảng trắng đầu ứng viên. Ví dụ `{"prompt":"The algorithm uses", "candidates":[" dynamic programming", " a greedy strategy"]}`. Recipe tokenizes prompt và candidate **riêng**, rồi ghép explicit token IDs; vì BPE có thể khác ở biên chuỗi, giao thức này được ghi trong receipt và không tuyên bố tương đương mọi cách tokenizing nguyên chuỗi. Không trộn hai giao thức để so điểm.

```powershell
python -B -X utf8 content/phase-4/recipes/zero_shot.py --mode gpt2 --asset content/phase-4/recipes/assets/gpt2 --input content/phase-4/recipes/data/completions.json --data-review receipts/phase-4/text-review.txt --out receipts/phase-4/real-gpt2
```

Recipe không truncation, từ chối khi quá context. Nó shift logits với token kế tiếp, chỉ chấm continuation, kiểm mean negative log khớp loss của masked labels, và lưu log-prob từng token, sum, mean, continuation PPL. Đây không phải PPL corpus dài, cũng không phải accuracy lời giải thuật toán. Không dùng DistilBERT MLM thay model causal trong công thức. Đọc [hướng dẫn PPL](https://huggingface.co/docs/transformers/perplexity) trước khi mở rộng sang cửa sổ trượt của tài liệu dài.

## Lần chạy đầu với asset thật

Chạy từng recipe một, theo thứ tự tải → kiểm offline → thực nghiệm. Sau mỗi lần chạy, đọc `RESULT.json`: môi trường, hash, ID của từng dự đoán và kết quả đối chiếu logits sau khi tải lại. Nếu phiên bản thư viện đổi API hoặc tên module (ví dụ `q_lin`, `v_lin` của DistilBERT), script dừng kèm thông báo; giữ log lỗi ấy, sửa trong một lần chạy có ghi log, và chỉ dùng kết quả của lần chạy đã qua mọi phép kiểm.
