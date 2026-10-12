# Recipe với checkpoint pretrained

Các notebook bài học chạy offline bằng CPU và không cần thư mục này. Recipe dưới đây đưa quy trình của bài 6.2, 6.3, 6.5, 6.6 sang checkpoint công bố: nạp snapshot đã chuẩn bị sẵn trên máy, kiểm hash và license, rồi chạy trên dữ liệu của mình. Cú pháp, import và các cửa chặn asset của script đã được kiểm; điểm số và thời gian chỉ đến từ lần chạy của bạn.

| Bài | Recipe | Repo ID | License theo model card đã đọc |
|---|---|---|---|
| 6.2 | `sentence_embedding.py` | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | Apache-2.0 |
| 6.3 | `bert_finetune.py` | distilbert/distilbert-base-multilingual-cased | Apache-2.0 |
| 6.5 | `seq2seq_pretrained.py` | google/flan-t5-small | Apache-2.0 |
| 6.6 | `llm_inference.py` | Qwen/Qwen2.5-0.5B-Instruct | Apache-2.0 |

Chuẩn bị snapshot và môi trường theo quyền của nơi chạy. Recipe không download, không tự cài package, không dùng remote code. `asset_utils.py` bật chế độ offline, yêu cầu `config.json`, weights safetensors, file license và manifest có commit SHA 40 hex. Manifest đặt **ngoài** thư mục snapshot; `files` phải chứa SHA-256 của toàn bộ file trong snapshot, không giữ cache hub lẫn vào đó. Các file đường dẫn tương đối phải resolve trong asset root. Xác nhận license trong manifest chỉ ghi nhận người chuẩn bị đã đọc điều kiện; hash không tự chứng minh nguồn gốc nếu manifest không được lưu từ nguồn tin cậy.

`assets.example.json` cố ý có placeholder và `license_reviewed: false`, nên bị từ chối khi chạy. Thay bằng receipt thật của snapshot đã chuẩn bị; không chép tên repo rồi tự coi file ngẫu nhiên là pretrained. Các repo ID chỉ nơi đọc model card; việc tải snapshot làm riêng, theo quy định của nơi chạy.

Từ thư mục recipe, ví dụ lệnh khi asset đã sẵn sàng:

```powershell
python -B -X utf8 sentence_embedding.py --asset ABS_SNAPSHOT --manifest ABS_RECEIPT --device cpu
python -B -X utf8 seq2seq_pretrained.py --asset ABS_SNAPSHOT --manifest ABS_RECEIPT --device cpu
python -B -X utf8 llm_inference.py --asset ABS_SNAPSHOT --manifest ABS_RECEIPT --device cuda
python -B -X utf8 bert_finetune.py --asset ABS_SNAPSHOT --manifest ABS_RECEIPT --data ABS_DATA_JSON --task token --device cuda --output ABS_NEW_RUN
```

Fine-tuning dataset JSON có `label_names`, `train`, `validation`. Sequence rows có `text`, `label`; token rows có `tokens` và `labels` cùng độ dài theo từ. Có thể thêm `group`; nhóm train/validation không được trùng. Token recipe yêu cầu fast tokenizer, chỉ gán nhãn subword đầu, không cắt dài âm thầm; evaluation dùng span BIO tại word-level, I không nối đúng mở span mới. Nếu đề có metric chính thức khác, thay evaluator cho đúng đề và ghi receipt. Dataset ví dụ để đọc hợp đồng, không phải benchmark:

```json
{
  "label_names": ["O", "B-PER", "I-PER", "B-LOC", "I-LOC"],
  "train": [{"tokens": ["An", "đến", "Hà", "Nội"], "labels": ["B-PER", "O", "B-LOC", "I-LOC"], "group": "doc-train"}],
  "validation": [{"tokens": ["Bình", "ở", "Huế"], "labels": ["B-PER", "O", "B-LOC"], "group": "doc-valid"}]
}
```

Đọc nguồn: [MiniLM sentence model](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2), [DistilmBERT](https://huggingface.co/distilbert/distilbert-base-multilingual-cased), [FLAN-T5](https://huggingface.co/google/flan-t5-small), [Qwen instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct). Kiểm lại license/revision khi chuẩn bị, lưu môi trường và raw output. Trên T4, inference dùng CUDA float16 nếu môi trường hỗ trợ; thời gian và peak memory phải đo trên chính máy ấy, không suy từ dung lượng danh nghĩa của GPU.
