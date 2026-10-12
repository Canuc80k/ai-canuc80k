# Recipe âm thanh với asset local

Đây là phần thực hành tiếp theo cho 7.2 và 7.3: đưa quy trình của bài từ tín hiệu tổng hợp sang bản ghi thật với checkpoint có sẵn trên máy. Mọi điểm số và thời gian chạy đến từ `receipt.json` của chính lần chạy; recipe không kèm sẵn kết quả của Whisper, HuBERT hay wav2vec2. `--self-check` kiểm phần toán không cần asset: phép đổi PCM, độ dài sau convolution và scorer.

## Phạm vi đã có adapter

- `local_audio.py --task asr`: checkpoint **Whisper** local, WAV ngắn không quá 30 giây, chép lời cùng ngôn ngữ (`task=transcribe`). CPU, mỗi lần một clip, corpus WER tách theo khoảng trắng và lowercase.
- `--task embedding`: checkpoint **HuBERT hoặc wav2vec2** local, lấy encoder hidden states, mean pooling đúng chiều sau convolution, StandardScaler→LogisticRegression fit trên train, accuracy/macro-F1 trên validation theo group đã chia trong manifest.

Adapter không dùng `Model(config)` để thay weights thiếu. Loader kiểm missing/mismatched keys và dừng khi cần random replacement. Một checkpoint ASR có head dư có thể nạp base encoder nếu các weights của encoder đầy đủ; weights không dùng không đồng nghĩa missing weights. Recipe dùng safetensors local để hợp đồng weights rõ ràng.

## Asset và manifest

Chuẩn bị một task virtual environment nếu thư viện thiếu; không cài toàn máy. Script in phiên bản Python/NumPy/SciPy/torch/Transformers/sklearn/safetensors. WAV dùng `scipy.io.wavfile`, không cần torchaudio/soundfile/FFmpeg. File compressed cần được chuyển đổi bằng quy trình riêng được kiểm, không sửa extension thành WAV.

Checkpoint cần `config.json`, `preprocessor_config.json`, weights safetensors đầy đủ, tokenizer/generation files cho Whisper. Nguồn checkpoint phải được cho phép theo nhiệm vụ và có provenance/revision riêng; manifest lưu các hash thực tế. ASR theo recipe phù hợp thử một checkpoint nhỏ như Whisper tiny trước, rồi đo thời gian/bộ nhớ thực trên thiết bị. Không giả định checkpoint lớn vừa GPU/CPU chỉ từ tên.

Manifest ASR:

```json
{
  "data_root": "audio",
  "normalization": "lowercase_whitespace",
  "records": [
    {
      "id": "clip-001",
      "path": "clip-001.wav",
      "reference": "em học ai hôm nay",
      "group": "speaker-01-session-01",
      "split": "validation"
    }
  ]
}
```

`data_root` được giải theo thư mục manifest; đường dẫn từng WAV phải ở trong root ấy. `id` duy nhất; `group` không được có ở cả train/validation. Group phải theo điều cần tổng quát hóa: nếu cần người nói mới, dùng speaker ID, không dùng session ID cho phép cùng người xuất hiện hai phía. Với ASR, chấm các record validation và giữ cả reference rỗng trong tính số lỗi; tổng token reference toàn corpus phải dương.

Manifest embedding thêm `class_names` theo thứ tự cột output, dùng `label` integer thay cho `reference`, và cần cả train/validation. Train phải chứa mọi lớp. Ví dụ record: `{"id":"clip-002","path":"clip-002.wav","label":0,"group":"session-02","split":"train"}`. Không tạo augmentation/crop rồi mới chia group.

## Lệnh tái tạo

Từ thư mục workspace, kiểm phần toán không cần asset:

```powershell
python -B -X utf8 content/phase-7/recipes/local_audio.py --self-check
```

Kiểm assets trước khi nạp model; thay đường dẫn bằng asset thật của task:

```powershell
python -B -X utf8 content/phase-7/recipes/local_audio.py --task asr --checkpoint "D:/task-assets/whisper-tiny" --manifest "D:/task-data/asr-validation.json" --check
```

Chạy sau preflight thành công:

```powershell
python -B -X utf8 content/phase-7/recipes/local_audio.py --task asr --checkpoint "D:/task-assets/whisper-tiny" --manifest "D:/task-data/asr-validation.json" --language vietnamese --run --out "receipts/phase-7/asr-real"
python -B -X utf8 content/phase-7/recipes/local_audio.py --task embedding --checkpoint "D:/task-assets/hubert-base" --manifest "D:/task-data/classification.json" --run --out "receipts/phase-7/embedding-real"
```

Các đường dẫn `D:/task-assets` và `D:/task-data` là **chỗ thay** bằng thư mục checkpoint và dữ liệu thật của task. `--check` không ghi file và không nạp weights; trạng thái là `PREFLIGHT_ONLY_WEIGHTS_NOT_LOADED`. `--run` mới ghi `receipt.json`, transcript/raw scorer hoặc `embedding-probe.npz` chứa vector, ID/split, mapping và tham số linear probe. Nếu thư viện/processor không tương thích, recipe dừng; điều chỉnh trong venv của task và ghi phiên bản mới, không tự tải code/model.

## Hợp đồng và giới hạn cần giữ

PCM signed được chia theo $2^{bits-1}$, unsigned 8-bit trừ 128 rồi chia 128; stereo dùng mean downmix có chủ ý, cần kiểm trái pha. Sample rate lấy từ processor config và đổi bằng `resample_poly` có lọc, không chỉ sửa metadata. Không peak-normalize từng clip ngoài yêu cầu checkpoint. Im lặng được ghi cờ để kiểm hallucination; không âm thầm xóa các clip ấy khỏi validation.

Embedding chạy một clip một lần nên không có batch padding; length mask sau conv được tính từ kernel/stride. Khi mở rộng batch, phải đổi lengths từng clip và dùng attention mask đúng hợp đồng checkpoint, không mặc định mọi wav2vec2 cần mask giống nhau. Linear probe dùng StandardScaler fit train, class mapping rõ, metric trên đúng split. Cache cần đi cùng hash input, checkpoint và processor; thay asset thì dựng lại.

WER của recipe là **lowercase + tách khoảng trắng**, giữ dấu và dấu câu nếu chúng còn trong token. Nó là scorer minh họa có kiểm, không tự tương đương scorer một cuộc thi. Nếu đề chuẩn hóa punctuation/Unicode/số hoặc tách từ khác, thay cùng quy tắc cho reference và prediction, chốt scorer trước chọn model và lưu phiên bản. Có thể bổ sung alignment S/D/I, CER và lỗi tên riêng/số theo mục tiêu.

Chưa có chunking/VAD, timestamps, diarization, beam tuning, fine-tuning, model checkpoint export hoặc smoke load lại linear probe; clip quá 30 giây dừng có giải thích. `embedding-probe.npz` lưu các tham số dùng để tái tạo linear prediction, không là một model encoder mới. Muốn kết luận pipeline nộp tái lập, cần viết inference adapter dùng chính các tham số đã lưu và so predictions ở tiến trình mới trước khi nộp.

## Qwen2-Audio, Voxtral và VLM

Các model này có task/template/API khác Whisper. Recipe trên cố ý dừng với `model_type` ngoài adapter hỗ trợ. Chuẩn bị recipe riêng theo [Qwen2-Audio documentation](https://huggingface.co/docs/transformers/model_doc/qwen2_audio), [Voxtral model card](https://huggingface.co/mistralai/Voxtral-Mini-3B-2507) hoặc [multimodal chat templates](https://huggingface.co/docs/transformers/chat_templating_multimodal): kiểm local weights/processor/version, task transcribe thay vì summarize, input sample rate/resize, token limit, output mới và scorer. Chạy trước một clip/ảnh có reference, ghi thời gian/bộ nhớ rồi mới batch. Recipe này không có adapter cho các model ấy.

Nguồn tham khảo thêm: [Whisper model card](https://huggingface.co/openai/whisper-tiny), [HuBERT documentation](https://huggingface.co/docs/transformers/model_doc/hubert), [wav2vec2 checkpoint card](https://huggingface.co/facebook/wav2vec2-base-960h), [SciPy resample_poly](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.resample_poly.html). Đọc sampling rate, attention mask, language/task và giới hạn theo **checkpoint cụ thể**, không suy từ họ model.
