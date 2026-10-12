# Recipe hình

Dựng lại toàn bộ 203 SVG của giáo trình (192 đang chèn trong bài, 11 hình không bài nào dẫn, đánh dấu trong `PRUNED`). Phong cách bám bảy hình Linear regression của web cũ trong `reference/`: nền trong suốt, Lora, màu thích ứng sáng/tối. Báo cáo của lượt làm lại hình: `../../reports/20261003-figure-redesign/`.

```bash
python -B -X utf8 build.py              # dựng vào staged/, chưa đụng content/
python -B -X utf8 build.py --apply      # chép staged/phase-N/fig/*.svg vào ../content/
python -B -X utf8 build.py --apply --phase 2   # chỉ một chương
```

`../content/figures.py` và `../content/phase-N/figures.py` là lối vào gọi `build.py --apply`. Chỉ apply sau khi đã xem hình.

| Tệp | Vai trò |
|---|---|
| `build.py` | Chạy các script, đặt caption, đổi id SVG cho không trùng, ghi `staged/` |
| `plots.py` + `capture/*.pickle`, `capture-inventory.json` | Vẽ lại biểu đồ Matplotlib từ dữ liệu số đã lưu |
| `scenes*.py`, `supplement.py`, `canary.py`, `svg.py` | Sơ đồ SVG vẽ bằng hình học |
| `experiments.py`, `extra8.py` + `experiment-results.json`, `mixture-loss-data.json` | Chạy lại thực nghiệm CPU của bài 4.2, 4.3, 5.2, 8.4 (không tải model hay dataset) |
| `tuning17.py` | Bài 1.7: F1 train và CV theo k từ đúng GridSearchCV của bài (thêm ngày 05/10/2026) |
| `depth33.py`, `optim35.py`, `regul36.py`, `rnn38.py`, `ae310.py` | Chương 3, lượt sáu: chạy lại đúng code của bài rồi vẽ |
| `pretrained41.py`, `kt2regions.py`, `kt3threshold.py`, `depth52.py`, `augment53.py`, `neighbors57.py`, `occlusion59.py`, `extract66.py`, `ctcdp73.py`, `kt4score.py`, `kt4paired.py`, `plans81.py`, `noise81.py`, `open83.py`, `mock85.py` | Chương 4–8 và các buổi kiểm tra, lượt sáu: mỗi script chạy code của bài, kiểm số in ra rồi mới vẽ |
| `Lora.ttf`, `Inter-*.ttf` | Font dùng khi vẽ |

`staged/`, `labels/`, `captions.json`, `staged-manifest.json`, `pruned.json` là sản phẩm của lần chạy, xóa được. Kiểm ngày 06/10/2026: chạy `build.py` ra 203 SVG, cả 203 khớp từng byte với `content/`. Thêm hình mới: viết script, thêm vào danh sách `scripts` và `CAP` trong `build.py`, sửa số trong `assert len(manifest)`.

## Hình động (`anim/`, lượt 9, 11/10/2026)

68 hình động, mỗi bài ít nhất một, dựng từ ảnh thật (ảnh mẫu scikit-learn, scikit-image, chữ số `load_digits`, Fashion-MNIST, CIFAR-10), giọng đọc tổng hợp của Windows (`anim/data/*.wav`) và model có sẵn trong cache máy (ResNet-18 ImageNet, CLIP ViT-B/32, MiniLM, Qwen2.5-0.5B, wav2vec2, Whisper base.en); số liệu bảng chạy lại từ code bài (`lesson_ns`, `kt_ns`). Không tải mạng (`HF_HUB_OFFLINE=1`).

```bash
python -B -X utf8 anim/build_anim.py              # dựng mọi hình vào anim/staged/, ảnh ghép duyệt ở 04. Workspace/AI-anim-20261011/qa/
python -B -X utf8 anim/build_anim.py 5-1 2-10     # chỉ những hình có tên bắt đầu như vậy
python -B -X utf8 anim/build_anim.py --apply      # chép anim/staged/phase-N/fig/*.anim.* vào ../content/phase-N/fig/
```

| Tệp | Vai trò |
|---|---|
| `anim/akit.py` | Màu sáng/tối theo biến CSS của website, vẽ khung (PIL, Matplotlib), đóng sprite WebP, tệp mô tả JSON, ảnh ghép duyệt |
| `anim/a_ch0.py` … `a_ch9.py` | Mỗi hàm `aN_…` là một hình (tên hình = tên hàm bỏ chữ `a`, `_` thành `-`); kt1–kt4 nằm cuối tệp chương của buổi |
| `anim/models.py` | Nạp model, ảnh và bộ dữ liệu có sẵn trên máy (ResNet-18, CLIP, Fashion-MNIST, CIFAR-10) |
| `anim/data/` | Hai câu tiếng Anh đọc bằng giọng tổng hợp Windows (Zira, David), 16 kHz |
| `anim/manifest.json` | Caption, số khung, kích thước, SHA-256 từng tệp của lần dựng gần nhất |

Thêm hình: viết hàm trả về `akit.Anim(tên, caption, nhãn từng khung, draw)`, thêm vào `ANIMS` của chương, dựng, xem ảnh ghép sáng/tối, `--apply`, rồi chèn bằng `../../reports/20261011-animations/edits/anim_edit.py` (`lesson`, `slide`, `credit`). Khung có nét vẽ hay chữ theo màu nền thì đặt `themed=True` để dựng thêm bản tối; ảnh thật không cần. Chữ trong khung chỉ dùng khi cần (tên token, số trên ô); ý chính để ở nhãn khung và caption.

