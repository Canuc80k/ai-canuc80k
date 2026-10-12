# Recipe ảnh thật với asset cục bộ

Các bài 5.1–5.9 chạy trên CPU với ảnh nhỏ tự tạo. Recipe dưới đây là bước tiếp theo khi đã có ảnh, nhãn và checkpoint trên máy: kiểm hash, nạp offline, chạy thử một ảnh, rồi fine-tune hoặc đánh giá trên validation của chính dữ liệu ấy. Mọi điểm số và thời gian chạy đến từ lần chạy của bạn; recipe không kèm sẵn kết quả nào.

## Kiểm môi trường trước

Chạy từ thư mục workspace:

```powershell
python -B -X utf8 content/phase-5/recipes/local_assets.py
```

Lệnh chỉ đọc khả năng tìm module, không tải model, không cài gói và không chạy GPU. Module được tìm thấy chưa bảo đảm import tương thích; bước chạy thật kiểm import và dừng khi thiếu điều kiện.

## Nạp và chạy một ảnh

[local_assets.py](local_assets.py) có bốn task: classifier, detector, clip, diffusion. Không truyền `--run` thì chỉ preflight. Các đường dẫn bên dưới là chỗ thay bằng asset thực sự đã có; chúng không là tên tệp được cung cấp sẵn.

Classifier dùng **ResNet-18 ImageNet V1 state dict**, detector dùng **Faster R-CNN ResNet-50 FPN COCO V1 state dict**. Trọng số và kiến trúc khác phải viết adapter riêng, không đổi tên để ép nạp. Constructor đặt `weights=None` và `weights_backbone=None` khi phù hợp để không tự tải. Metadata JSON có `sha256` của file, `kind` tương ứng và `class_names` đúng thứ tự output. Hàm kiểm hash trước khi nạp.

```powershell
python -B -X utf8 content/phase-5/recipes/local_assets.py --task classifier --checkpoint <state.pth> --metadata <asset.json> --image <image.png>
python -B -X utf8 content/phase-5/recipes/local_assets.py --task classifier --checkpoint <state.pth> --metadata <asset.json> --image <image.png> --run
```

Metadata classifier dùng `kind=resnet18_imagenet_v1` và 1000 class names. Đầu ra là top class index, tên và xác suất giữa 1000 lớp đó; chưa phải head nhãn mới của lớp học. Để transfer: nạp encoder, thay `fc` theo số lớp đích, đóng băng encoder, train head bằng split nhóm đúng, rồi thử mở block cuối với learning rate riêng. Preprocessing V1 phải được giữ đúng; nếu đầu vào rất khác miền nguồn, so lại với baseline.

Detector dùng `--task detector`, `kind=fasterrcnn_resnet50_fpn_coco_v1`, danh sách class ID khớp 91 outputs của checkpoint. Ảnh được đưa thành RGB float 0–1, box output là `xyxy` theo ảnh gốc. `--score-threshold` chỉ là ngưỡng hiển thị; muốn dùng để đếm phải chọn trên validation theo metric count. Model có hậu xử lý của chính nó; không thêm NMS lần nữa mà chưa kiểm.

CLIP dùng `--task clip --model-dir <local-clip-dir> --image <image.png> --texts "ảnh một chai nước" "ảnh một quyển sách"`. Thư mục cần config, processor/tokenizer và weights safetensors của cùng model. Recipe đặt offline và `local_files_only=True`, không cho custom remote code. Score phụ thuộc prompt và tập ứng viên. Để retrieval, normalize embedding, cache vector ảnh, kiểm cosine/top-k và metric trên query validation; không dùng top class của hai prompt làm benchmark toàn kho.

Diffusion dùng `--task diffusion --model-dir <local-pipeline-dir> --prompt "..." --output <new-image.png> --run`. Cần package diffusers và **Stable Diffusion pipeline tương thích** gồm model_index.json, tokenizer, text_encoder, unet, vae, scheduler và weights safetensors. Recipe chỉ chạy CPU float32, một ảnh 256×256, 10 bước để kiểm đường nạp và inference; trên CPU bước này có thể chậm và cần RAM đáng kể, nên đo thời gian của chính máy trước khi tăng số bước hay kích thước. Pipeline/asset yêu cầu kích thước khác phải sửa có chủ đích. Giữ safety checker theo asset, không gọi ảnh tạo được là dữ liệu thật.

## Fine-tune U-Net trên ảnh và mask

[unet_finetune.py](unet_finetune.py) cung cấp U-Net một mức **đúng cấu trúc mạng nhỏ của bài 5.6**, không tự nạp encoder lớn. Asset pretrained tùy chọn chỉ được nạp nếu là state dict của chính TinyUNet này, kèm SHA-256. Nếu không có asset, `--from-scratch` phải được ghi tường minh để tránh gọi nhầm random model là pretrained.

Dữ liệu cần các thư mục `train/images`, `train/masks`, `valid/images`, `valid/masks`. Recipe khớp basename, ảnh xám, mask chỉ có 0/255 hoặc 0/1, cùng kích thước trước resize; resize ảnh bilinear, mask nearest. Các nhóm người/video phải được chia sẵn trước; script không tự suy ra nhóm.

```powershell
python -B -X utf8 content/phase-5/recipes/unet_finetune.py --data <data-dir>
python -B -X utf8 content/phase-5/recipes/unet_finetune.py --data <data-dir> --checkpoint <tiny-unet.pth> --sha256 <hash> --output <new-checkpoint.pth> --run
```

Lệnh đầu chỉ kiểm dữ liệu. Chạy từ đầu phải thay checkpoint/hash bằng `--from-scratch`. Script dùng CPU, batch 2, tối đa số epoch đã chọn, lưu checkpoint theo mean Dice validation rồi nạp lại để suy luận một batch. Chương không kèm asset TinyUNet hay ảnh thật; dữ liệu và (nếu có) checkpoint do người chạy chuẩn bị. Với U-Net encoder pretrained từ thư viện khác, cần adapter kiến trúc, preprocessing và checkpoint riêng.

## Đọc nguồn và kết quả

Các API được đối chiếu với [TorchVision models](https://docs.pytorch.org/vision/stable/models.html), [CLIP](https://huggingface.co/docs/transformers/model_doc/clip), [Diffusers](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/overview). Phiên bản ở máy thực hành có thể khác; preflight và strict load giúp phát hiện điều đó. Sau chạy thật, lưu cấu hình, phiên bản, asset hash, split, metric và runtime vào hồ sơ thí nghiệm; số của ví dụ nhỏ trong bài không thay được số đo trên asset thật.
